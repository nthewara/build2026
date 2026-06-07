#!/usr/bin/env python3
"""
Build-time search artifacts for the Microsoft Build 2026 static site.

Implements "Option D" (GitHub issue #1): a fully *offline-first* search upgrade
that does its semantic / heavy work at BUILD TIME and ships only static
artifacts the browser can use with zero network calls and zero external libs.

Two committed JSON artifacts are produced:

  assets/search-index.json
      Lean, deterministic search corpus for the landing-page client search.
      One entry per SESSION (markdown/*.md) and one per WIKI CONCEPT page
      (wiki/concepts/*.html), plus a small static synonym map for Build-domain
      terms. The landing page inlines this (so it works from file:// with no
      fetch) and ranks results with a BM25-lite scorer.

  assets/related.json
      Precomputed semantic "Related sessions" neighbours per session, computed
      with QMD vector search (vsearch) at build time. scripts/generate_site.py
      reads this and bakes a static "Related sessions" block into each
      pages/<CODE>.html. No client-side vector math is shipped -- only the
      *results* are baked in statically.

Design goals:
  * DETERMINISTIC + IDEMPOTENT: running twice yields byte-identical JSON.
    Everything sorted; scores rounded to fixed precision; keys stable.
  * LEAN: keep search-index.json well under ~2 MB.
  * NO raw embedding vectors shipped to the browser.
  * Reuses the frontmatter parsing approach/helpers from generate_site.py.

QMD:
  Shells out to the local `qmd` binary (vector search over the already-built
  `markdown` collection) and parses its JSON output (`--json`). If qmd is not
  available, related.json is still written (degraded) so the rest of the
  pipeline degrades gracefully rather than failing.

Usage:
  python3 scripts/build_search_index.py
"""

from __future__ import annotations

import html
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
MARKDOWN_DIR = REPO_ROOT / "markdown"
PAGES_DIR = REPO_ROOT / "pages"
ASSETS_DIR = REPO_ROOT / "assets"
WIKI_CONCEPTS_DIR = REPO_ROOT / "wiki" / "concepts"

SEARCH_INDEX_PATH = ASSETS_DIR / "search-index.json"
RELATED_PATH = ASSETS_DIR / "related.json"

# QMD config
QMD_COLLECTION = "markdown"
RELATED_TOP_N = 5           # related sessions baked per page
QMD_FETCH_N = 12            # over-fetch (drops self + a few)
SCORE_DECIMALS = 4          # rounding for deterministic JSON
BODY_MAX_TOKENS = 450       # cap body token stream per session (leanness)


def _find_qmd():
    for c in (os.path.expanduser("~/.bun/bin/qmd"), shutil.which("qmd") or ""):
        if c and Path(c).exists():
            return c
    return None


QMD_BIN = _find_qmd()

# ---------------------------------------------------------------------------
# Import the *real* yaml, not the local ./markdown/ notes dir (which would
# shadow `import markdown`/namespace-shadow site-packages).
# ---------------------------------------------------------------------------
sys.path = [p for p in sys.path if Path(p or ".").resolve() != REPO_ROOT]
try:
    import yaml  # type: ignore
    _HAVE_YAML = True
except Exception:  # pragma: no cover
    yaml = None  # type: ignore
    _HAVE_YAML = False


# ---------------------------------------------------------------------------
# Frontmatter parsing -- same approach/helpers as scripts/generate_site.py.
# ---------------------------------------------------------------------------
def split_frontmatter(text):
    if text.startswith("\ufeff"):
        text = text.lstrip("\ufeff")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if not text.startswith("---\n") and text.strip() != "---":
        return {}, text
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}, text
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return {}, text
    fm_text = "\n".join(lines[1:end_idx])
    body = "\n".join(lines[end_idx + 1:])
    return parse_yaml_frontmatter(fm_text), body.lstrip("\n")


def parse_yaml_frontmatter(fm_text):
    if _HAVE_YAML:
        try:
            data = yaml.safe_load(fm_text)
            if isinstance(data, dict):
                return data
            return {}
        except Exception:
            pass
    return _tiny_yaml(fm_text)


def _tiny_yaml(fm_text):
    out = {}
    cur_key = None
    cur_list = None
    for raw in fm_text.split("\n"):
        if not raw.strip():
            continue
        if re.match(r"^\s+-\s", raw) and cur_key is not None:
            item = _strip_quotes(raw.strip()[1:].strip())
            if cur_list is None:
                cur_list = []
                out[cur_key] = cur_list
            cur_list.append(item)
            continue
        m = re.match(r"^([A-Za-z0-9_\-]+):\s*(.*)$", raw)
        if m:
            cur_key = m.group(1)
            val = m.group(2).strip()
            cur_list = None
            out[cur_key] = "" if val == "" else _coerce_scalar(_strip_quotes(val))
    return out


def _strip_quotes(s):
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    return s


def _coerce_scalar(s):
    if s.lower() in ("true", "false"):
        return s.lower() == "true"
    if re.fullmatch(r"-?\d+", s):
        try:
            return int(s)
        except ValueError:
            return s
    return s


# ---------------------------------------------------------------------------
# Shared helpers (mirroring generate_site.py semantics).
# ---------------------------------------------------------------------------
def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    s = str(value).strip()
    return [s] if s else []


def split_speakers(value):
    items = as_list(value)
    if len(items) == 1 and ("," in items[0]):
        return [p.strip() for p in re.split(r",(?![^()]*\))", items[0]) if p.strip()]
    return items


def topic_tags(tags):
    out = [t[len("topic/"):] for t in as_list(tags) if t.startswith("topic/")]
    seen, res = set(), []
    for x in out:
        if x not in seen:
            seen.add(x)
            res.append(x)
    return res


def pretty_tag(label):
    special = {
        "ai": "AI", "dotnet": ".NET", "devops": "DevOps", "mcp": "MCP",
        "sdk": "SDK", "m365-copilot": "M365 Copilot",
        "github-copilot": "GitHub Copilot", "github": "GitHub",
        "azure-ai-foundry": "Azure AI Foundry",
        "microsoft-purview": "Microsoft Purview",
        "responsible-ai": "Responsible AI", "arm": "Arm", "cobalt": "Cobalt",
    }
    return special.get(label, label.replace("-", " ").title())


def first_h1(body):
    for line in body.split("\n"):
        m = re.match(r"^#\s+(.*)$", line)
        if m:
            return m.group(1).strip()
    return None


def clean_title(h1, code):
    t = h1.strip()
    if code:
        pat = re.compile(rf"^{re.escape(code)}\s*[\u2014\u2013\-:]\s*", re.IGNORECASE)
        t2 = pat.sub("", t)
        if t2:
            t = t2
    return t


# ---------------------------------------------------------------------------
# Body -> tokens.
# ---------------------------------------------------------------------------
STOPWORDS = frozenset("""
a an and the of to in on for with without by from at as is are was were be been
being this that these those it its they them their there here what which who
whom whose how why when where can could should would may might must will shall do
does did done doing have has had having you your yours we our ours us i me my mine
he she his her hers theirs not no nor so than too very just also into over under
out up down off about across after before between during through above below again
further then once each few more most other some such only own same don dont
re ll ve ain aren couldn didn doesn hadn hasn haven isn ma mightn mustn needn
shan shouldn wasn weren won wouldn via vs etc eg ie per get got new use using used
like one two three first second way ways make makes made thing things lot lots
""".split())

MD_STRIP_RES = [
    (re.compile(r"```.*?```", re.DOTALL), " "),
    (re.compile(r"`[^`]*`"), " "),
    (re.compile(r"!\[[^\]]*\]\([^)]*\)"), " "),
    (re.compile(r"\[([^\]]*)\]\([^)]*\)"), r"\1"),
    (re.compile(r"\[\[([^\]|]+?)(?:\|([^\]]+))?\]\]"), r"\1"),
    (re.compile(r"https?://\S+"), " "),
    (re.compile(r"[>#*_~`\-]+"), " "),
    (re.compile(r"&[a-z]+;"), " "),
]

TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9.+#/-]*[a-z0-9]|[a-z0-9]")


def strip_markdown(text):
    for rx, repl in MD_STRIP_RES:
        text = rx.sub(repl, text)
    return text


def tokenize(text):
    """Lowercase tokenizer; keeps c#, .net, gpt-5.5, ci/cd, etc."""
    toks = TOKEN_RE.findall(text.lower())
    out = []
    for tk in toks:
        tk = tk.strip(".-/")
        if len(tk) < 2:
            continue
        if tk in STOPWORDS:
            continue
        out.append(tk)
    return out


def keyword_set(body, title, topics, speakers):
    blob = " ".join([title, " ".join(topics),
                     " ".join(pretty_tag(t) for t in topics),
                     " ".join(speakers)])
    cleaned = strip_markdown(body)
    toks = set(tokenize(blob)) | set(tokenize(cleaned))
    return sorted(toks)


def body_text_blob(body, max_tokens=BODY_MAX_TOKENS):
    """Compact lowercased body token stream (keeps term-frequency signal),
    capped for leanness. Deterministic: first max_tokens meaningful tokens."""
    toks = tokenize(strip_markdown(body))
    if len(toks) > max_tokens:
        toks = toks[:max_tokens]
    return " ".join(toks)


# ---------------------------------------------------------------------------
# Session model.
# ---------------------------------------------------------------------------
class SessionDoc:
    def __init__(self, path):
        self.path = path
        raw = path.read_text(encoding="utf-8")
        self.fm, self.body = split_frontmatter(raw)
        self.code = str(self.fm.get("session_code") or "").strip()
        self.aliases = as_list(self.fm.get("aliases"))
        self.topics = topic_tags(self.fm.get("tags"))
        self.speakers = split_speakers(self.fm.get("speakers"))
        try:
            self.duration_min = int(str(self.fm.get("duration_min") or "0").strip() or 0)
        except ValueError:
            self.duration_min = 0
        h1 = first_h1(self.body)
        fallback = self.aliases[0] if self.aliases else path.stem
        self.h1 = h1 or fallback
        self.title = clean_title(self.h1, self.code)

    @property
    def url(self):
        return f"pages/{self.code}.html"

    @property
    def sort_key(self):
        m = re.match(r"^([A-Za-z]+)(\d+)", self.code or "")
        if m:
            return (m.group(1), int(m.group(2)), self.code)
        return (self.code, 0, self.code)


# ---------------------------------------------------------------------------
# Static synonym map (build-time domain data, NOT facts injected into pages).
# Used by the client to expand a query lexically. Deterministic + sorted.
# ---------------------------------------------------------------------------
SYNONYMS_RAW = {
    "vector db": ["vector database", "embeddings", "pgvector", "cosmos db",
                  "vector search", "similarity search", "horizondb", "postgres",
                  "postgresql"],
    "vector database": ["vector db", "embeddings", "pgvector", "cosmos db",
                         "vector search", "horizondb", "postgres", "postgresql"],
    "embeddings": ["vector", "vector database", "vector db", "pgvector",
                   "embedding", "rag", "retrieval"],
    "observability": ["opentelemetry", "otel", "monitoring", "telemetry",
                      "application insights", "app insights", "tracing",
                      "logging", "metrics", "observe"],
    "observe": ["observability", "monitoring", "telemetry", "opentelemetry",
                "tracing", "metrics"],
    "monitoring": ["observability", "opentelemetry", "telemetry",
                   "application insights", "metrics", "observe"],
    "serverless": ["azure functions", "functions", "container apps",
                   "aca", "consumption", "faas"],
    "k8s": ["kubernetes", "aks", "azure kubernetes service", "containers"],
    "kubernetes": ["k8s", "aks", "azure kubernetes service", "containers"],
    "aks": ["kubernetes", "k8s", "azure kubernetes service"],
    "rag": ["retrieval augmented generation", "retrieval", "embeddings",
            "grounding", "vector search"],
    "agents": ["agent", "agentic", "autonomous", "copilot", "ai agents"],
    "agent": ["agents", "agentic", "copilot"],
    "llm": ["large language model", "model", "gpt", "foundation model"],
    "ci/cd": ["ci", "cd", "pipeline", "pipelines", "github actions",
              "azure devops", "continuous integration", "continuous delivery"],
    "cicd": ["ci", "cd", "pipeline", "github actions", "azure devops"],
    "devops": ["ci/cd", "pipeline", "github actions", "azure devops"],
    "security": ["defender", "purview", "governance", "compliance",
                 "advanced security", "supply chain"],
    "governance": ["purview", "compliance", "policy", "security",
                   "responsible ai"],
    "copilot": ["github copilot", "m365 copilot", "agent", "agents"],
    "foundry": ["azure ai foundry", "ai foundry", "model catalog"],
    "database": ["db", "sql", "postgres", "postgresql", "cosmos db",
                 "azure sql", "horizondb"],
    "frontend": ["ui", "web", "blazor", "react", "client"],
    "production": ["prod", "deploy", "deployment", "ship", "shipping",
                   "operations"],
    "testing": ["test", "tests", "qa", "playwright", "unit test"],
    "mcp": ["model context protocol", "tools", "tool calling"],
}


def normalized_synonyms():
    out = {}
    for k in sorted(SYNONYMS_RAW.keys()):
        members = sorted(set(m.strip().lower() for m in SYNONYMS_RAW[k] if m.strip()))
        out[k.strip().lower()] = members
    return out


# ---------------------------------------------------------------------------
# Wiki concept extraction (for unified global search).
# ---------------------------------------------------------------------------
TITLE_RE = re.compile(r'<h1 class="wk-concept-title">(.*?)<span', re.DOTALL)
TITLE_FALLBACK_RE = re.compile(r"<title>(.*?)</title>", re.DOTALL)
CLUSTER_RE = re.compile(r"Cluster:\s*<strong>(.*?)</strong>", re.DOTALL)
SESSION_CODE_RE = re.compile(r'href="\.\./\.\./pages/([A-Za-z0-9]+)\.html"')
TAG_CODE_RE = re.compile(r"<code>topic/([a-z0-9\-]+)</code>")
TAG_STRIP_RE = re.compile(r"<[^>]+>")


def visible_text_from_html(htmltext):
    htmltext = re.sub(r"<script.*?</script>", " ", htmltext, flags=re.DOTALL | re.IGNORECASE)
    htmltext = re.sub(r"<style.*?</style>", " ", htmltext, flags=re.DOTALL | re.IGNORECASE)
    text = html.unescape(TAG_STRIP_RE.sub(" ", htmltext))
    return re.sub(r"\s+", " ", text).strip()


class ConceptDoc:
    def __init__(self, path):
        self.path = path
        self.slug = path.stem
        raw = path.read_text(encoding="utf-8")
        m = TITLE_RE.search(raw)
        if m:
            self.title = html.unescape(TAG_STRIP_RE.sub("", m.group(1))).strip()
        else:
            fb = TITLE_FALLBACK_RE.search(raw)
            self.title = (html.unescape(fb.group(1)).split("\u2014")[0].strip()
                          if fb else self.slug)
        cm = CLUSTER_RE.search(raw)
        self.cluster = html.unescape(cm.group(1)).strip() if cm else ""
        self.member_codes = sorted(set(SESSION_CODE_RE.findall(raw)))
        tm = TAG_CODE_RE.search(raw)
        self.topic = tm.group(1) if tm else ""
        toks = tokenize(visible_text_from_html(raw))
        self.keywords = sorted(set(toks))[:200]
        self.body_blob = " ".join(toks[:300])

    @property
    def url(self):
        return f"wiki/concepts/{self.slug}.html"


# ---------------------------------------------------------------------------
# QMD vector search -> related sessions per code.
# ---------------------------------------------------------------------------
def code_from_qmd_file(qmd_file):
    base = qmd_file.split("/")[-1]
    m = re.match(r"^([a-zA-Z]+[0-9]+)", base)
    return m.group(1).upper() if m else None


def code_from_qmd_title(title):
    m = re.match(r"^\s*([A-Za-z]+[0-9]+)\b", title or "")
    return m.group(1).upper() if m else None


def qmd_vsearch_codes(query_text, valid_codes):
    """Run qmd vsearch (JSON); return [(CODE, score), ...] limited to valid
    session codes, in qmd's ranked order, de-duped."""
    if not QMD_BIN:
        return []
    try:
        proc = subprocess.run(
            [QMD_BIN, "vsearch", query_text,
             "-c", QMD_COLLECTION, "--json", "-n", str(QMD_FETCH_N)],
            capture_output=True, text=True, timeout=180,
        )
    except Exception as exc:  # pragma: no cover
        print(f"  [qmd error] {query_text[:40]!r}: {exc}", file=sys.stderr)
        return []
    if proc.returncode != 0:
        print(f"  [qmd rc={proc.returncode}] {query_text[:40]!r}: "
              f"{proc.stderr.strip()[:160]}", file=sys.stderr)
        return []
    try:
        data = json.loads(proc.stdout)
    except Exception:
        return []
    results = []
    seen = set()
    for row in (data if isinstance(data, list) else []):
        code = code_from_qmd_file(str(row.get("file", ""))) \
            or code_from_qmd_title(str(row.get("title", "")))
        if not code or code not in valid_codes or code in seen:
            continue
        try:
            score = float(row.get("score", 0.0))
        except (TypeError, ValueError):
            score = 0.0
        results.append((code, round(score, SCORE_DECIMALS)))
        seen.add(code)
    return results


def build_related(sessions):
    """For each session, query qmd with the session's own title+topics and keep
    the top RELATED_TOP_N OTHER sessions. Deterministic given a fixed qmd index.
    """
    valid_codes = {s.code for s in sessions}
    title_by_code = {s.code: s.title for s in sessions}
    related = {}
    for s in sorted(sessions, key=lambda s: s.sort_key):
        topic_words = " ".join(pretty_tag(t) for t in s.topics)
        query = f"{s.title} {topic_words}".strip()
        neigh = qmd_vsearch_codes(query, valid_codes)
        picked = []
        for code, score in neigh:
            if code == s.code:
                continue
            picked.append({"code": code,
                           "title": title_by_code.get(code, code),
                           "score": score})
            if len(picked) >= RELATED_TOP_N:
                break
        if picked:
            related[s.code] = picked
    return {k: related[k] for k in sorted(related.keys())}


# ---------------------------------------------------------------------------
# Build the search index (lean, deterministic).
# ---------------------------------------------------------------------------
def build_index(sessions, concepts):
    docs = []

    for s in sorted(sessions, key=lambda s: s.sort_key):
        # For sessions we ship a frequency-bearing body token stream (`text`)
        # plus the (already title+tag+speaker-augmented) keyword set folded in.
        # We DO NOT ship a separate `keywords` array for sessions: it is a
        # deduped superset of `text` and roughly doubles the index size for no
        # ranking benefit (BM25-lite uses term frequencies from `text`). We
        # prepend the title/tag/speaker terms to `text` so they carry weight.
        head_terms = " ".join(tokenize(" ".join(
            [s.title, " ".join(s.topics),
             " ".join(pretty_tag(t) for t in s.topics),
             " ".join(s.speakers)])))
        text_blob = (head_terms + " " + body_text_blob(s.body)).strip()
        entry = {
            "id": s.code,
            "type": "session",
            "code": s.code,
            "title": s.title,
            "url": s.url,
            "tags": [pretty_tag(t) for t in s.topics],
            "speakers": list(s.speakers),
            "duration": s.duration_min,
            "text": text_blob,
        }
        docs.append(entry)

    for c in sorted(concepts, key=lambda c: c.slug):
        entry = {
            "id": c.slug,
            "type": "concept",
            "title": c.title,
            "url": c.url,
            "cluster": c.cluster,
            "tags": [pretty_tag(c.topic)] if c.topic else [],
            "members": c.member_codes,
            "keywords": c.keywords,
            "text": c.body_blob,
        }
        docs.append(entry)

    return {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "counts": {
            "sessions": sum(1 for d in docs if d["type"] == "session"),
            "concepts": sum(1 for d in docs if d["type"] == "concept"),
            "total": len(docs),
        },
        "synonyms": normalized_synonyms(),
        "docs": docs,
    }


# ---------------------------------------------------------------------------
# Deterministic JSON writer.
# ---------------------------------------------------------------------------
def write_json(path, obj):
    """Write compact-but-readable JSON deterministically.

    sort_keys is intentionally False because we already emit lists/dicts in a
    stable, meaningful order (docs sorted by code/slug; synonyms sorted; per-doc
    fields in a fixed insertion order). ensure_ascii=False keeps it compact and
    human-diffable while staying valid UTF-8.
    """
    text = json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=False)
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text, encoding="utf-8")
    return len(text.encode("utf-8"))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    skip_related = "--skip-related" in sys.argv[1:]
    if not MARKDOWN_DIR.is_dir():
        print(f"FATAL: markdown dir not found: {MARKDOWN_DIR}", file=sys.stderr)
        return 1

    # --- Sessions (only docs that carry a session_code) ---
    sessions = []
    skipped = 0
    for f in sorted(MARKDOWN_DIR.glob("*.md")):
        try:
            doc = SessionDoc(f)
        except Exception as exc:
            print(f"ERROR parsing {f.name}: {exc}", file=sys.stderr)
            raise
        if not doc.code:
            skipped += 1
            continue
        sessions.append(doc)

    # --- Wiki concepts (unified global search scope) ---
    concepts = []
    if WIKI_CONCEPTS_DIR.is_dir():
        for f in sorted(WIKI_CONCEPTS_DIR.glob("*.html")):
            # The wiki index.html lives one level up; only concept pages here.
            try:
                concepts.append(ConceptDoc(f))
            except Exception as exc:
                print(f"ERROR parsing concept {f.name}: {exc}", file=sys.stderr)
                raise

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    # --- search-index.json ---
    index_obj = build_index(sessions, concepts)
    idx_bytes = write_json(SEARCH_INDEX_PATH, index_obj)

    # --- related.json (QMD semantic neighbours) ---
    # The QMD pass is the slow part (one vsearch per session). Pass
    # --skip-related to rebuild only the index and KEEP the committed
    # assets/related.json untouched (useful when only index tuning changed).
    if skip_related and RELATED_PATH.exists():
        rel_bytes = RELATED_PATH.stat().st_size
        related_obj = json.loads(RELATED_PATH.read_text(encoding="utf-8"))
        print("NOTE: --skip-related set; reused existing assets/related.json.")
    else:
        if not QMD_BIN:
            print("WARN: qmd binary not found; writing empty related.json "
                  "(Related blocks will be omitted).", file=sys.stderr)
        related_obj = build_related(sessions)
        rel_bytes = write_json(RELATED_PATH, related_obj)

    # --- Report ---
    print("=" * 64)
    print("Search artifacts built.")
    print(f"  markdown/*.md scanned   -> {len(sessions) + skipped} "
          f"({len(sessions)} sessions, {skipped} non-session skipped)")
    print(f"  wiki concepts indexed   -> {len(concepts)}")
    print(f"  assets/search-index.json -> {idx_bytes:,} bytes "
          f"({idx_bytes / 1024:.1f} KiB)")
    print(f"  assets/related.json      -> {rel_bytes:,} bytes "
          f"({len(related_obj)} sessions with related neighbours)")
    print(f"  synonyms                 -> {len(index_obj['synonyms'])} terms")
    if idx_bytes > 2 * 1024 * 1024:
        print("  WARNING: search-index.json exceeds 2 MB budget!", file=sys.stderr)
    print("=" * 64)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
