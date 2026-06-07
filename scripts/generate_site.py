#!/usr/bin/env python3
"""
Static site generator for Microsoft Build 2026 session notes.

Reads markdown/*.md (Obsidian-flavoured GitHub Markdown with YAML frontmatter
and Obsidian callouts), and produces:
  - index.html            (landing page with search + cards)
  - pages/<CODE>.html      (one polished page per session)
  - assets/style.css       (shared stylesheet)

Re-runnable / idempotent: clears pages/ and regenerates everything each run.

Usage:
  python3 scripts/generate_site.py
"""

from __future__ import annotations

import html
import re
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Make sure we import the *real* `markdown` PyPI package and not the local
# ./markdown/ source directory (which would shadow it as a namespace package).
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
MARKDOWN_DIR = REPO_ROOT / "markdown"
PAGES_DIR = REPO_ROOT / "pages"
ASSETS_DIR = REPO_ROOT / "assets"

# Drop any sys.path entries that would let `import markdown` resolve to the
# notes directory, then import.
_clean_path = [p for p in sys.path if Path(p or ".").resolve() != REPO_ROOT]
sys.path = _clean_path

try:
    import markdown as md_lib  # type: ignore
except Exception as exc:  # pragma: no cover
    print(f"FATAL: could not import the `markdown` library: {exc}", file=sys.stderr)
    print("Install it with: python3 -m pip install markdown --break-system-packages", file=sys.stderr)
    sys.exit(1)

try:
    import yaml  # type: ignore
    _HAVE_YAML = True
except Exception:  # pragma: no cover
    yaml = None  # type: ignore
    _HAVE_YAML = False


SITE_TITLE = "Microsoft Build 2026"
SITE_SUBTITLE = "Session Notes &amp; Summaries"
SITE_BLURB = (
    "Curated, deep-dive notes from Microsoft Build 2026 sessions \u2014 key takeaways, "
    "demos, announcements, and the stats worth remembering. Search, skim, and dive in."
)

# Obsidian callout type -> (css-modifier, default-title, emoji icon)
CALLOUT_TYPES = {
    "info": ("info", "Info", "\u2139\ufe0f"),
    "note": ("note", "Note", "\U0001f4dd"),
    "tip": ("tip", "Tip", "\U0001f4a1"),
    "warning": ("warning", "Warning", "\u26a0\ufe0f"),
    "caution": ("warning", "Caution", "\u26a0\ufe0f"),
    "danger": ("warning", "Danger", "\u26a0\ufe0f"),
    "important": ("important", "Important", "\U0001f4cc"),
    "quote": ("quote", "Quote", "\u201c\u201d"),
    "example": ("example", "Example", "\U0001f9ea"),
    "summary": ("summary", "Summary", "\U0001f9fe"),
    "abstract": ("summary", "Summary", "\U0001f9fe"),
    "tldr": ("summary", "TL;DR", "\U0001f9fe"),
}
GENERIC_CALLOUT = ("generic", "Note", "\U0001f5d2\ufe0f")


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------
def split_frontmatter(text: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body_markdown).

    Handles a leading YAML block delimited by `---` lines. Missing/blank
    frontmatter is tolerated and yields an empty dict.
    """
    if text.startswith("\ufeff"):
        text = text.lstrip("\ufeff")
    # Normalise line endings.
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    if not text.startswith("---\n") and text.strip() != "---":
        return {}, text

    # Find the closing delimiter.
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return {}, text
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        # No closing fence; treat whole thing as body.
        return {}, text

    fm_text = "\n".join(lines[1:end_idx])
    body = "\n".join(lines[end_idx + 1:])
    fm = parse_yaml_frontmatter(fm_text)
    return fm, body.lstrip("\n")


def parse_yaml_frontmatter(fm_text: str) -> dict:
    if _HAVE_YAML:
        try:
            data = yaml.safe_load(fm_text)
            if isinstance(data, dict):
                return data
            return {}
        except Exception:
            pass  # fall through to the tiny parser
    return _tiny_yaml(fm_text)


def _tiny_yaml(fm_text: str) -> dict:
    """A minimal, safe fallback YAML parser for the simple frontmatter used
    here: scalars, `key: value`, and `key:` followed by `  - item` lists."""
    out: dict = {}
    cur_key = None
    cur_list: list | None = None
    for raw in fm_text.split("\n"):
        if not raw.strip():
            continue
        if re.match(r"^\s+-\s", raw) and cur_key is not None:
            item = raw.strip()[1:].strip()
            item = _strip_quotes(item)
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
            if val == "":
                # Possibly a list follows.
                out[cur_key] = ""
            else:
                out[cur_key] = _coerce_scalar(_strip_quotes(val))
    return out


def _strip_quotes(s: str) -> str:
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    return s


def _coerce_scalar(s: str):
    if s.lower() in ("true", "false"):
        return s.lower() == "true"
    if re.fullmatch(r"-?\d+", s):
        try:
            return int(s)
        except ValueError:
            return s
    return s


# ---------------------------------------------------------------------------
# Callout pre-pass: turn Obsidian `> [!type] Title` blocks into HTML divs
# *before* handing the rest of the text to the markdown converter.
# ---------------------------------------------------------------------------
CALLOUT_START_RE = re.compile(r"^>\s?\[!([A-Za-z]+)\]([+-]?)\s*(.*)$")


def transform_callouts(text: str, md_inline) -> str:
    """Replace contiguous blockquote callout blocks with HTML placeholders.

    We emit raw HTML wrapped so the markdown lib leaves it intact. The inner
    body is itself rendered to HTML via `md_inline` (a fresh Markdown instance)
    so bold/links/lists inside callouts work.
    """
    lines = text.split("\n")
    out: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        m = CALLOUT_START_RE.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue

        ctype = m.group(1).lower()
        title_text = m.group(3).strip()

        # Gather the rest of the contiguous `>` block.
        body_lines: list[str] = []
        i += 1
        while i < n and (lines[i].startswith(">")):
            # Strip the leading '>' and a single optional space.
            stripped = lines[i][1:]
            if stripped.startswith(" "):
                stripped = stripped[1:]
            body_lines.append(stripped)
            i += 1

        modifier, default_title, icon = CALLOUT_TYPES.get(ctype, GENERIC_CALLOUT)
        title = title_text if title_text else default_title

        body_md = "\n".join(body_lines).strip()
        md_inline.reset()
        body_html = md_inline.convert(body_md) if body_md else ""

        title_html = render_inline(html.escape(title), md_inline)

        block = (
            f'\n<div class="callout callout-{modifier}">\n'
            f'  <div class="callout-title">'
            f'<span class="callout-icon" aria-hidden="true">{icon}</span>'
            f'<span class="callout-title-text">{title_html}</span></div>\n'
            f'  <div class="callout-body">\n{body_html}\n  </div>\n'
            f"</div>\n"
        )
        out.append(block)
        # Note: we already advanced past the block.

    return "\n".join(out)


def render_inline(escaped_text: str, md_inline) -> str:
    """Render a short inline string (already HTML-escaped) for things like a
    callout title that may contain **bold** or `code`. Strips wrapping <p>."""
    md_inline.reset()
    out = md_inline.convert(escaped_text)
    out = out.strip()
    if out.startswith("<p>") and out.endswith("</p>"):
        out = out[3:-4]
    return out


# ---------------------------------------------------------------------------
# Wikilinks: [[Target]] or [[Target|Label]]
# Resolve to an internal page if Target matches a known session; else render
# as a subtle non-link chip-ish span.
# ---------------------------------------------------------------------------
WIKILINK_RE = re.compile(r"\[\[([^\]|]+?)(?:\|([^\]]+))?\]\]")


def replace_wikilinks(text: str, resolver) -> str:
    def _sub(m: re.Match) -> str:
        target = m.group(1).strip()
        label = (m.group(2) or target).strip()
        href = resolver(target)
        esc_label = html.escape(label)
        if href:
            # Links only to another session page that exists in THIS repo.
            return f'<a class="wikilink wikilink--resolved" href="{href}">{esc_label}</a>'
        # Target is a vault concept/MOC note that is NOT part of this repo.
        # Render as plain text so nothing points to (or implies) an external
        # Obsidian note. No link, no broken-reference styling, no tooltip.
        return esc_label

    return WIKILINK_RE.sub(_sub, text)


# ---------------------------------------------------------------------------
# Strip vault-only wikilinks BEFORE rendering.
#
# A wikilink whose target resolves to another session page in THIS repo is a
# real cross-link and is kept (replace_wikilinks turns it into an <a>).
# A wikilink whose target is a vault concept/MOC note (e.g. [[Azure AI Foundry]],
# [[2026 Build Session List]], [[32.02 Content]]) does NOT belong in this repo
# and is removed entirely here — including dropping list items / headings that
# would otherwise be left empty.
# ---------------------------------------------------------------------------
LIST_ITEM_RE = re.compile(r"^(\s*(?:[-*+]|\d+[.)])\s+)(.*)$")
RELATED_HEADING_RE = re.compile(r"^#{1,6}\s+.*$")


def strip_unresolved_wikilinks(text: str, resolver) -> str:
    def has_unresolved(s: str) -> bool:
        return any(resolver(m.group(1).strip()) is None
                   for m in WIKILINK_RE.finditer(s))

    def remove_unresolved_tokens(s: str) -> str:
        # Drop only the [[...]] tokens whose target does NOT resolve in-repo.
        def _sub(m: re.Match) -> str:
            target = m.group(1).strip()
            return m.group(0) if resolver(target) else ""
        return WIKILINK_RE.sub(_sub, s)

    out_lines: list[str] = []
    for line in text.split("\n"):
        if "[[" not in line or not has_unresolved(line):
            out_lines.append(line)
            continue

        li = LIST_ITEM_RE.match(line)
        if li:
            marker, content = li.group(1), li.group(2)
            cleaned = remove_unresolved_tokens(content)
            # Tidy leftover join punctuation/dashes from removed tokens.
            cleaned = re.sub(r"\s*[/|,;–—-]\s*(?=$)", "", cleaned)
            cleaned = re.sub(r"^\s*[/|,;–—-]\s*", "", cleaned)
            cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()
            # Strip a leftover leading em-dash descriptor like "— sibling ...".
            cleaned = re.sub(r"^[–—-]\s*", "", cleaned).strip()
            # A bullet reduced to just a dangling label like "Source list:" (a
            # label that only introduced the removed vault ref) is dropped too.
            is_dangling_label = bool(re.fullmatch(r"[A-Za-z][\w ./&-]*:", cleaned))
            if cleaned and not is_dangling_label and not re.fullmatch(r"[/|,;:.–—-]*", cleaned):
                out_lines.append(f"{marker}{cleaned}")
            # else: the bullet was only a vault reference → drop the whole line.
        else:
            # Inline (non-list) line: remove just the unresolved tokens.
            cleaned = remove_unresolved_tokens(line)
            cleaned = re.sub(r"\s{2,}", " ", cleaned).rstrip()
            out_lines.append(cleaned)

    text = "\n".join(out_lines)

    # Remove now-empty list markers (e.g. a leftover '- ' with nothing after,
    # or a bullet that held only a removed vault ref).
    text = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s*$", "", text, flags=re.MULTILINE)

    # Drop any now-empty trailing-style section headings (e.g. '## 🔗 Related')
    # that have no remaining real content before the next heading / EOF.
    lines = text.split("\n")
    keep = [True] * len(lines)
    for i, line in enumerate(lines):
        if RELATED_HEADING_RE.match(line):
            has_content = False
            for j in range(i + 1, len(lines)):
                nxt = lines[j]
                if RELATED_HEADING_RE.match(nxt):
                    break
                # An empty / whitespace-only / bare-list-marker line is NOT content.
                if nxt.strip() and not re.fullmatch(r"(?:[-*+]|\d+[.)])\s*", nxt.strip()):
                    has_content = True
                    break
            if not has_content:
                keep[i] = False
    text = "\n".join(l for l, k in zip(lines, keep) if k)

    # Collapse 3+ blank lines left behind into at most 2.
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "page"


def first_h1(body: str) -> str | None:
    for line in body.split("\n"):
        m = re.match(r"^#\s+(.*)$", line)
        if m:
            return m.group(1).strip()
        # Stop scanning if we hit a fenced code block start to be safe-ish.
    return None


def clean_title(h1: str, code: str | None) -> str:
    """Strip a leading 'CODE \u2014 ' / 'CODE - ' prefix from the H1 so the card
    title isn't redundant with the badge."""
    t = h1.strip()
    if code:
        # Match 'CODE', optional spaces, an em/en dash or hyphen, spaces.
        pat = re.compile(rf"^{re.escape(code)}\s*[\u2014\u2013\-:]\s*", re.IGNORECASE)
        t2 = pat.sub("", t)
        if t2:
            t = t2
    return t


def as_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    s = str(value).strip()
    return [s] if s else []


def split_speakers(value) -> list[str]:
    items = as_list(value)
    if len(items) == 1 and ("," in items[0]):
        # comma-separated string
        # Avoid splitting parenthetical commas badly: simple split is fine for
        # the data we have; keep it readable.
        parts = [p.strip() for p in re.split(r",(?![^()]*\))", items[0]) if p.strip()]
        return parts
    return items


def topic_tags(tags) -> list[str]:
    out = []
    for t in as_list(tags):
        if t.startswith("topic/"):
            label = t[len("topic/"):]
            out.append(label)
    # De-dup preserving order.
    seen = set()
    res = []
    for x in out:
        if x not in seen:
            seen.add(x)
            res.append(x)
    return res


def pretty_tag(label: str) -> str:
    """topic slug -> human label. Keep known acronyms uppercase."""
    special = {
        "ai": "AI",
        "dotnet": ".NET",
        "devops": "DevOps",
        "mcp": "MCP",
        "sdk": "SDK",
        "m365-copilot": "M365 Copilot",
        "github-copilot": "GitHub Copilot",
        "github": "GitHub",
        "azure-ai-foundry": "Azure AI Foundry",
        "microsoft-purview": "Microsoft Purview",
        "responsible-ai": "Responsible AI",
        "arm": "Arm",
        "cobalt": "Cobalt",
    }
    if label in special:
        return special[label]
    return label.replace("-", " ").title()


def fmt_duration(total_min: int) -> str:
    if total_min <= 0:
        return "0m"
    h, m = divmod(total_min, 60)
    if h and m:
        return f"{h}h {m}m"
    if h:
        return f"{h}h"
    return f"{m}m"


def youtube_id(url: str) -> str | None:
    m = re.search(r"[?&]v=([A-Za-z0-9_\-]{6,})", url or "")
    if m:
        return m.group(1)
    m = re.search(r"youtu\.be/([A-Za-z0-9_\-]{6,})", url or "")
    if m:
        return m.group(1)
    return None


# ---------------------------------------------------------------------------
# Markdown instances
# ---------------------------------------------------------------------------
def make_md() -> "md_lib.Markdown":
    return md_lib.Markdown(
        extensions=[
            "extra",        # includes tables, fenced_code, footnotes, attr_list, etc.
            "tables",
            "fenced_code",
            "toc",
            "sane_lists",
        ],
        extension_configs={
            "toc": {"permalink": False},
        },
        output_format="html5",
    )


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------
class Session:
    def __init__(self, path: Path):
        self.path = path
        raw = path.read_text(encoding="utf-8")
        self.fm, self.body = split_frontmatter(raw)
        self.missing_fields: list[str] = []

        self.code = self._get_str("session_code")
        self.event = self._get_str("event") or "Microsoft Build 2026"
        self.source = self._get_str("source")
        self.duration_min = self._get_int("duration_min")
        self.speakers = split_speakers(self.fm.get("speakers"))
        self.aliases = as_list(self.fm.get("aliases"))
        self.tags_all = as_list(self.fm.get("tags"))
        self.topics = topic_tags(self.fm.get("tags"))

        h1 = first_h1(self.body)
        if not h1:
            self.missing_fields.append("h1-title")
        fallback_title = (self.aliases[0] if self.aliases else path.stem)
        self.h1 = h1 or fallback_title
        self.title = clean_title(self.h1, self.code)

        # Stable output filename.
        if self.code:
            self.slug = self.code
        else:
            self.missing_fields.append("session_code")
            self.slug = slugify(path.stem)
        self.filename = f"{self.slug}.html"

    def _get_str(self, key: str) -> str:
        v = self.fm.get(key)
        if v is None or (isinstance(v, str) and not v.strip()):
            self.missing_fields.append(key)
            return ""
        return str(v).strip()

    def _get_int(self, key: str) -> int:
        v = self.fm.get(key)
        if v is None or (isinstance(v, str) and not v.strip()):
            self.missing_fields.append(key)
            return 0
        try:
            return int(str(v).strip())
        except ValueError:
            self.missing_fields.append(f"{key}(non-int)")
            return 0

    @property
    def sort_key(self):
        # Sort by code: split letters vs digits so BRK203 < DEM331 < OD806,
        # and numbers compare numerically.
        code = self.code or self.slug
        m = re.match(r"^([A-Za-z]+)(\d+)", code)
        if m:
            return (m.group(1), int(m.group(2)), code)
        return (code, 0, code)


# ---------------------------------------------------------------------------
# Rendering: body HTML
# ---------------------------------------------------------------------------
def render_body_html(session: Session, resolver) -> str:
    body = session.body

    # Remove the first H1 from the body (it's shown in the page header already).
    body = re.sub(r"^#\s+.*$", "", body, count=1, flags=re.MULTILINE).lstrip("\n")

    # Remove vault-only concept/MOC wikilinks entirely (drops empty list items
    # and now-empty 'Related' headings). Keeps in-repo session cross-links.
    body = strip_unresolved_wikilinks(body, resolver)

    # Resolve the remaining (in-repo) wikilinks to <a> links.
    body = replace_wikilinks(body, resolver)

    md_block = make_md()
    md_inline = make_md()

    # Callout pre-pass -> injects raw HTML blocks.
    body = transform_callouts(body, md_inline)

    md_block.reset()
    html_out = md_block.convert(body)
    html_out = convert_task_lists(html_out)
    return html_out


def convert_task_lists(html_out: str) -> str:
    """Convert GitHub task-list items rendered as literal '[ ]'/'[x]' at the
    start of an <li> into real disabled checkboxes."""
    def _sub(m: re.Match) -> str:
        mark = m.group(1)
        checked = " checked" if mark.lower() == "x" else ""
        return (f'<li class="task-list-item">'
                f'<input type="checkbox" disabled{checked}> ')
    # Handles <li>[ ] text  and <li>\n[ ] text variants.
    return re.sub(r'<li>\s*\[([ xX])\]\s*', _sub, html_out)


# ---------------------------------------------------------------------------
# HTML templates
# ---------------------------------------------------------------------------
def page_shell(title: str, css_rel: str, body_html: str, extra_head: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="{css_rel}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='48' height='48' x='2' y='2' fill='%23f25022'/%3E%3Crect width='48' height='48' x='50' y='2' fill='%237fba00'/%3E%3Crect width='48' height='48' x='2' y='50' fill='%2300a4ef'/%3E%3Crect width='48' height='48' x='50' y='50' fill='%23ffb900'/%3E%3C/svg%3E">
{extra_head}
</head>
<body>
{body_html}
<footer class="site-footer">
  <div class="container">
    Microsoft Build 2026 \u00b7 Session notes &amp; summaries \u00b7 Generated static site \u2014 no tracking, no CDNs.
  </div>
</footer>
</body>
</html>
"""


def speakers_html(speakers: list[str]) -> str:
    if not speakers:
        return ""
    chips = "".join(
        f'<span class="speaker">{html.escape(s)}</span>' for s in speakers
    )
    return f'<div class="speakers">{chips}</div>'


def tag_chips_html(topics: list[str]) -> str:
    if not topics:
        return ""
    chips = "".join(
        f'<span class="chip" data-tag="{html.escape(t)}">{html.escape(pretty_tag(t))}</span>'
        for t in topics
    )
    return f'<div class="chips">{chips}</div>'


def build_card(session: Session) -> str:
    code = session.code or session.slug
    speakers_join = ", ".join(session.speakers)
    search_blob = " ".join(
        [code, session.title, speakers_join, " ".join(session.topics),
         " ".join(pretty_tag(t) for t in session.topics)]
    ).lower()
    search_blob = html.escape(search_blob, quote=True)

    dur = fmt_duration(session.duration_min) if session.duration_min else "\u2014"

    return f"""    <a class="card" href="pages/{html.escape(session.filename)}" data-search="{search_blob}">
      <div class="card-top">
        <span class="badge">{html.escape(code)}</span>
        <span class="card-duration">\u23f1\ufe0f {dur}</span>
      </div>
      <h2 class="card-title">{html.escape(session.title)}</h2>
      <div class="card-speakers">\U0001f3a4 {html.escape(speakers_join) or "\u2014"}</div>
      {tag_chips_html(session.topics)}
      <span class="card-cta">Read notes \u2192</span>
    </a>
"""


def build_index(sessions: list[Session]) -> str:
    sessions_sorted = sorted(sessions, key=lambda s: s.sort_key)
    total = len(sessions_sorted)
    total_min = sum(s.duration_min for s in sessions_sorted)
    speakers_set = set()
    for s in sessions_sorted:
        for sp in s.speakers:
            speakers_set.add(sp)
    n_speakers = len(speakers_set)

    cards = "\n".join(build_card(s) for s in sessions_sorted)

    stats = f"""
      <div class="stat">
        <div class="stat-num">{total}</div>
        <div class="stat-label">Sessions</div>
      </div>
      <div class="stat">
        <div class="stat-num">{fmt_duration(total_min)}</div>
        <div class="stat-label">Total runtime</div>
      </div>
      <div class="stat">
        <div class="stat-num">{n_speakers}</div>
        <div class="stat-label">Speakers</div>
      </div>
"""

    body = f"""
<header class="hero">
  <div class="container">
    <div class="hero-badge">Build 2026</div>
    <h1 class="hero-title">{SITE_TITLE}</h1>
    <p class="hero-subtitle">{SITE_SUBTITLE}</p>
    <p class="hero-blurb">{SITE_BLURB}</p>
    <div class="stats">{stats}</div>
    <div style="margin-top:26px;display:flex;flex-wrap:wrap;gap:12px;align-items:center;">
      <a href="wiki/index.html" style="display:inline-flex;align-items:center;gap:9px;background:#50e6ff;color:#003a66;font-weight:700;font-size:1rem;text-decoration:none;padding:12px 22px;border-radius:999px;box-shadow:0 6px 20px rgba(0,0,0,.18);transition:transform .15s ease,box-shadow .15s ease;" onmouseover="this.style.transform='translateY(-2px)';this.style.boxShadow='0 10px 28px rgba(0,0,0,.26)';" onmouseout="this.style.transform='';this.style.boxShadow='0 6px 20px rgba(0,0,0,.18)';">
        \U0001f578️  Explore the LLM Wiki
        <span aria-hidden="true">&rarr;</span>
      </a>
      <a href="wiki/graph.html" style="display:inline-flex;align-items:center;gap:8px;background:rgba(255,255,255,.14);color:#eaf6ff;font-weight:600;font-size:.95rem;text-decoration:none;padding:12px 20px;border-radius:999px;border:1px solid rgba(255,255,255,.28);">
        \U0001f579️  Concept graph
      </a>
    </div>
    <p style="margin-top:12px;font-size:.88rem;color:#cfe6f5;max-width:640px;">
      A Karpathy-style <strong>LLM&nbsp;Wiki</strong> compiled from these session notes — ~90 cross-linked concept pages plus an interactive knowledge graph. Same content, reorganized to explore by idea.
    </p>
  </div>
</header>

<main class="container">
  <div class="toolbar">
    <input id="search" class="search" type="search"
           placeholder="&#128269;  Filter by title, code, speaker, or topic&hellip;"
           aria-label="Filter sessions" autocomplete="off">
    <div class="result-count" id="resultCount"></div>
  </div>

  <section class="grid" id="grid">
{cards}
  </section>

  <p class="no-results" id="noResults" hidden>No sessions match your filter.</p>
</main>
"""

    search_js = """
<script>
(function () {
  var input = document.getElementById('search');
  var cards = Array.prototype.slice.call(document.querySelectorAll('.card'));
  var noResults = document.getElementById('noResults');
  var countEl = document.getElementById('resultCount');
  var total = cards.length;

  function update() {
    var q = (input.value || '').trim().toLowerCase();
    var shown = 0;
    for (var i = 0; i < cards.length; i++) {
      var blob = cards[i].getAttribute('data-search') || '';
      var match = q === '' || blob.indexOf(q) !== -1;
      cards[i].style.display = match ? '' : 'none';
      if (match) shown++;
    }
    noResults.hidden = shown !== 0;
    if (countEl) {
      countEl.textContent = (q === '')
        ? (total + ' sessions')
        : (shown + ' of ' + total + ' sessions');
    }
  }

  input.addEventListener('input', update);
  // Keyboard shortcut: "/" focuses search.
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && document.activeElement !== input) {
      e.preventDefault();
      input.focus();
    }
  });
  update();
})();
</script>
"""

    return page_shell(
        title=f"{SITE_TITLE} \u2014 Session Notes",
        css_rel="assets/style.css",
        body_html=body,
        extra_head="",
    ).replace("</body>", search_js + "\n</body>")


def build_session_page(session: Session, body_html: str,
                       prev_s: Session | None, next_s: Session | None) -> str:
    code = session.code or session.slug
    dur = fmt_duration(session.duration_min) if session.duration_min else None

    # Meta row pieces.
    meta_items = []
    if session.event:
        meta_items.append(f'<span class="meta-item">\U0001f3e2 {html.escape(session.event)}</span>')
    if session.speakers:
        meta_items.append(
            f'<span class="meta-item">\U0001f3a4 {html.escape(", ".join(session.speakers))}</span>'
        )
    if dur:
        meta_items.append(f'<span class="meta-item">\u23f1\ufe0f {html.escape(dur)}</span>')
    meta_row = "\n      ".join(meta_items)

    watch_btn = ""
    if session.source:
        watch_btn = (
            f'<a class="btn btn-youtube" href="{html.escape(session.source)}" '
            f'target="_blank" rel="noopener noreferrer">'
            f'<span class="yt-glyph" aria-hidden="true">\u25b6</span> Watch on YouTube</a>'
        )

    # Prev / next.
    prev_html = ""
    if prev_s:
        prev_code = prev_s.code or prev_s.slug
        prev_html = (
            f'<a class="pager pager-prev" href="{html.escape(prev_s.filename)}">'
            f'<span class="pager-dir">\u2190 Previous</span>'
            f'<span class="pager-code">{html.escape(prev_code)}</span>'
            f'<span class="pager-title">{html.escape(prev_s.title)}</span></a>'
        )
    else:
        prev_html = '<span class="pager pager-empty"></span>'

    next_html = ""
    if next_s:
        next_code = next_s.code or next_s.slug
        next_html = (
            f'<a class="pager pager-next" href="{html.escape(next_s.filename)}">'
            f'<span class="pager-dir">Next \u2192</span>'
            f'<span class="pager-code">{html.escape(next_code)}</span>'
            f'<span class="pager-title">{html.escape(next_s.title)}</span></a>'
        )
    else:
        next_html = '<span class="pager pager-empty"></span>'

    body = f"""
<nav class="topnav">
  <div class="container topnav-inner">
    <a class="back-link" href="../index.html">\u2190 All sessions</a>
    <a class="topnav-title" href="../index.html">{SITE_TITLE} <span>\u00b7 Notes</span></a>
  </div>
</nav>

<header class="session-header">
  <div class="container">
    <div class="session-head-top">
      <span class="badge badge-lg">{html.escape(code)}</span>
      {watch_btn}
    </div>
    <h1 class="session-title">{html.escape(session.title)}</h1>
    <div class="meta-row">
      {meta_row}
    </div>
    {tag_chips_html(session.topics)}
  </div>
</header>

<main class="container">
  <article class="prose">
{body_html}
  </article>

  <nav class="pager-nav">
    {prev_html}
    {next_html}
  </nav>
</main>
"""
    return page_shell(
        title=f"{code} \u2014 {session.title}",
        css_rel="../assets/style.css",
        body_html=body,
    )


# ---------------------------------------------------------------------------
# Stylesheet
# ---------------------------------------------------------------------------
CSS = r""":root {
  --blue:        #0067b8;
  --blue-dark:   #004e8c;
  --blue-deep:   #003a66;
  --cyan:        #50e6ff;
  --ink:         #1b1a19;
  --body:        #2f2e2d;
  --muted:       #605e5c;
  --line:        #e6e3df;
  --bg:          #f6f7f9;
  --card:        #ffffff;
  --chip-bg:     #eaf3fb;
  --chip-ink:    #0a5ca8;
  --radius:      14px;
  --radius-sm:   9px;
  --shadow:      0 1px 2px rgba(16,24,40,.06), 0 8px 24px rgba(16,24,40,.06);
  --shadow-lg:   0 2px 6px rgba(16,24,40,.08), 0 18px 48px rgba(16,24,40,.12);
  --maxw:        1120px;
  --font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial,
          "Apple Color Emoji", "Segoe UI Emoji", sans-serif;
  --mono: "SF Mono", ui-monospace, SFMono-Regular, "Cascadia Code", Menlo, Consolas, monospace;
}

* { box-sizing: border-box; }

html { scroll-behavior: smooth; }

body {
  margin: 0;
  font-family: var(--font);
  color: var(--body);
  background: var(--bg);
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}

.container {
  width: 100%;
  max-width: var(--maxw);
  margin: 0 auto;
  padding: 0 24px;
}

a { color: var(--blue); text-decoration: none; }
a:hover { text-decoration: underline; }

/* ---------- Hero (landing) ---------- */
.hero {
  background:
    radial-gradient(1200px 400px at 80% -10%, rgba(80,230,255,.20), transparent 60%),
    linear-gradient(135deg, var(--blue-deep) 0%, var(--blue-dark) 45%, var(--blue) 100%);
  color: #fff;
  padding: 72px 0 88px;
  position: relative;
  overflow: hidden;
}
.hero::after {
  content: "";
  position: absolute; inset: auto 0 -1px 0; height: 40px;
  background: linear-gradient(to bottom, transparent, var(--bg));
}
.hero-badge {
  display: inline-block;
  font-size: .8rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase;
  background: rgba(255,255,255,.14);
  border: 1px solid rgba(255,255,255,.28);
  padding: 6px 14px; border-radius: 999px; margin-bottom: 18px;
  backdrop-filter: blur(4px);
}
.hero-title {
  margin: 0;
  font-size: clamp(2.2rem, 5vw, 3.6rem);
  font-weight: 800; letter-spacing: -.02em; line-height: 1.05;
}
.hero-subtitle {
  margin: 10px 0 0;
  font-size: clamp(1.1rem, 2.4vw, 1.5rem);
  font-weight: 600; color: var(--cyan);
}
.hero-blurb {
  margin: 18px 0 0; max-width: 720px;
  font-size: 1.06rem; color: rgba(255,255,255,.88);
}

/* ---------- Stats ---------- */
.stats {
  display: flex; flex-wrap: wrap; gap: 14px; margin-top: 34px;
}
.stat {
  background: rgba(255,255,255,.10);
  border: 1px solid rgba(255,255,255,.20);
  border-radius: var(--radius);
  padding: 16px 22px; min-width: 140px;
  backdrop-filter: blur(6px);
}
.stat-num { font-size: 1.9rem; font-weight: 800; line-height: 1; }
.stat-label {
  margin-top: 6px; font-size: .82rem; letter-spacing: .06em;
  text-transform: uppercase; color: rgba(255,255,255,.82);
}

/* ---------- Toolbar / search ---------- */
.toolbar {
  display: flex; align-items: center; gap: 16px;
  margin: 36px 0 22px; flex-wrap: wrap;
}
.search {
  flex: 1 1 320px;
  font-size: 1rem; font-family: var(--font);
  padding: 13px 16px;
  border: 1px solid var(--line); border-radius: 999px;
  background: var(--card); color: var(--ink);
  box-shadow: var(--shadow);
  transition: border-color .15s, box-shadow .15s;
}
.search:focus {
  outline: none; border-color: var(--blue);
  box-shadow: 0 0 0 4px rgba(0,103,184,.14);
}
.result-count { color: var(--muted); font-size: .92rem; font-weight: 600; white-space: nowrap; }

/* ---------- Card grid ---------- */
.grid {
  display: grid; gap: 20px;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  padding-bottom: 8px;
}
.card {
  display: flex; flex-direction: column;
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 20px 20px 18px;
  box-shadow: var(--shadow);
  color: var(--body) !important;
  transition: transform .16s ease, box-shadow .16s ease, border-color .16s ease;
  position: relative;
}
.card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
  border-color: #cfe2f3;
  text-decoration: none;
}
.card-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.card-duration { font-size: .82rem; color: var(--muted); font-weight: 600; }
.card-title {
  margin: 0 0 10px; font-size: 1.16rem; font-weight: 750;
  color: var(--ink); line-height: 1.32; letter-spacing: -.01em;
}
.card-speakers { font-size: .9rem; color: var(--muted); margin-bottom: 14px; }
.card-cta {
  margin-top: auto; padding-top: 12px;
  font-size: .9rem; font-weight: 700; color: var(--blue);
}
.card:hover .card-cta { text-decoration: underline; }

/* ---------- Badges & chips ---------- */
.badge {
  display: inline-block;
  font-family: var(--mono); font-weight: 700; font-size: .78rem; letter-spacing: .02em;
  color: #fff; background: linear-gradient(135deg, var(--blue) 0%, var(--blue-dark) 100%);
  padding: 4px 10px; border-radius: 7px;
}
.badge-lg { font-size: .95rem; padding: 6px 14px; border-radius: 9px; }

.chips { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 4px; }
.chip {
  font-size: .76rem; font-weight: 650;
  background: var(--chip-bg); color: var(--chip-ink);
  padding: 4px 10px; border-radius: 999px; white-space: nowrap;
}

.speakers { display: flex; flex-wrap: wrap; gap: 8px; }
.speaker {
  font-size: .85rem; background: #f0f0ee; color: #444;
  padding: 3px 10px; border-radius: 999px;
}

.no-results {
  text-align: center; color: var(--muted); font-size: 1.05rem;
  padding: 48px 0 64px;
}

/* ---------- Top nav (session pages) ---------- */
.topnav {
  background: var(--card);
  border-bottom: 1px solid var(--line);
  position: sticky; top: 0; z-index: 20;
  box-shadow: 0 1px 0 rgba(16,24,40,.02);
}
.topnav-inner { display: flex; align-items: center; justify-content: space-between; height: 58px; }
.back-link { font-weight: 650; color: var(--blue); }
.topnav-title { font-weight: 750; color: var(--ink); }
.topnav-title span { color: var(--muted); font-weight: 500; }
.topnav-title:hover { text-decoration: none; }

/* ---------- Session header ---------- */
.session-header {
  background:
    radial-gradient(900px 300px at 90% -40%, rgba(80,230,255,.16), transparent 60%),
    linear-gradient(135deg, var(--blue-deep), var(--blue-dark) 70%);
  color: #fff;
  padding: 38px 0 34px;
}
.session-head-top {
  display: flex; align-items: center; justify-content: space-between;
  gap: 16px; flex-wrap: wrap; margin-bottom: 16px;
}
.session-title {
  margin: 0 0 14px;
  font-size: clamp(1.6rem, 3.4vw, 2.5rem);
  font-weight: 800; line-height: 1.16; letter-spacing: -.015em;
}
.meta-row { display: flex; flex-wrap: wrap; gap: 8px 20px; margin-bottom: 14px; }
.meta-item { font-size: .95rem; color: rgba(255,255,255,.92); }
.session-header .chips .chip {
  background: rgba(255,255,255,.16); color: #eaf6ff;
}

.btn {
  display: inline-flex; align-items: center; gap: 8px;
  font-weight: 700; font-size: .92rem;
  padding: 9px 16px; border-radius: 999px;
  transition: transform .12s, box-shadow .12s, background .12s;
}
.btn-youtube {
  background: #ff0033; color: #fff !important;
  box-shadow: 0 6px 18px rgba(255,0,51,.32);
}
.btn-youtube:hover { transform: translateY(-1px); text-decoration: none; box-shadow: 0 8px 22px rgba(255,0,51,.40); }
.yt-glyph { font-size: .8rem; }

/* ---------- Prose (rendered markdown) ---------- */
.prose {
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 36px 44px 40px;
  margin: 28px 0;
  box-shadow: var(--shadow);
  max-width: 860px;
}
.prose > *:first-child { margin-top: 0; }
.prose h2 {
  margin: 2em 0 .6em; font-size: 1.5rem; font-weight: 750; color: var(--ink);
  letter-spacing: -.01em; padding-bottom: .3em; border-bottom: 2px solid var(--line);
}
.prose h3 { margin: 1.6em 0 .5em; font-size: 1.2rem; font-weight: 700; color: var(--ink); }
.prose h4 { margin: 1.4em 0 .4em; font-size: 1.04rem; font-weight: 700; color: var(--blue-dark); }
.prose p { margin: .9em 0; }
.prose ul, .prose ol { margin: .8em 0; padding-left: 1.5em; }
.prose li { margin: .35em 0; }
.prose li > ul, .prose li > ol { margin: .3em 0; }
.prose strong { color: var(--ink); font-weight: 700; }
.prose a { color: var(--blue); font-weight: 500; word-break: break-word; }
.prose hr { border: none; border-top: 1px solid var(--line); margin: 2em 0; }
.prose blockquote {
  margin: 1.2em 0; padding: .2em 1.1em;
  border-left: 4px solid #cfe2f3; color: var(--muted);
}
.prose img { max-width: 100%; height: auto; border-radius: 8px; }

.prose code {
  font-family: var(--mono); font-size: .88em;
  background: #f1f3f5; color: #b1004e;
  padding: .15em .4em; border-radius: 5px;
}
.prose pre {
  background: #0d1117; color: #e6edf3;
  padding: 16px 18px; border-radius: 10px;
  overflow-x: auto; margin: 1.1em 0; line-height: 1.5;
}
.prose pre code { background: none; color: inherit; padding: 0; font-size: .86em; }

.prose table {
  border-collapse: collapse; width: 100%; margin: 1.2em 0;
  font-size: .94rem; display: block; overflow-x: auto;
}
.prose th, .prose td { border: 1px solid var(--line); padding: 9px 13px; text-align: left; }
.prose thead th { background: #f3f6f9; font-weight: 700; color: var(--ink); }
.prose tbody tr:nth-child(even) { background: #fafbfc; }

/* task list checkboxes from "- [ ]" */
.prose input[type="checkbox"] { margin-right: .5em; transform: translateY(1px); }
.prose li.task-list-item { list-style: none; margin-left: -1.2em; }

/* ---------- Callouts ---------- */
.callout {
  border: 1px solid var(--line);
  border-left: 5px solid var(--muted);
  border-radius: var(--radius-sm);
  background: #fbfcfd;
  margin: 1.4em 0; padding: 14px 18px 4px;
  box-shadow: 0 1px 2px rgba(16,24,40,.04);
}
.callout-title {
  display: flex; align-items: center; gap: 9px;
  font-weight: 750; color: var(--ink);
  margin-bottom: 2px; font-size: 1.02rem;
}
.callout-icon { font-size: 1.05rem; line-height: 1; }
.callout-body > *:first-child { margin-top: .4em; }
.callout-body > *:last-child { margin-bottom: .9em; }
.callout-body p { margin: .5em 0; }

.callout-info     { border-left-color: #0067b8; background: #f1f8fe; }
.callout-info .callout-title { color: #024a86; }
.callout-note     { border-left-color: #6b6f76; background: #f7f8f9; }
.callout-tip      { border-left-color: #1aa179; background: #f0faf6; }
.callout-tip .callout-title { color: #0c7a59; }
.callout-warning  { border-left-color: #d98300; background: #fff7ec; }
.callout-warning .callout-title { color: #9a5b00; }
.callout-important{ border-left-color: #8a3ffc; background: #f7f2ff; }
.callout-important .callout-title { color: #5f1bb8; }
.callout-quote    { border-left-color: #9aa0a6; background: #fafafa; font-style: italic; }
.callout-example  { border-left-color: #c026d3; background: #fdf2fd; }
.callout-example .callout-title { color: #8a1a96; }
.callout-summary  { border-left-color: #0aa2c0; background: #eefbfe; }
.callout-summary .callout-title { color: #07748a; }
.callout-generic  { border-left-color: #6b6f76; background: #f7f8f9; }

/* ---------- Wikilinks ---------- */
.wikilink--resolved { font-weight: 600; }
.wikilink--unresolved {
  color: var(--muted); border-bottom: 1px dotted #b9bcc0; cursor: help;
}

/* ---------- Pager ---------- */
.pager-nav {
  display: grid; grid-template-columns: 1fr 1fr; gap: 16px;
  margin: 12px 0 48px;
}
.pager {
  display: flex; flex-direction: column; gap: 3px;
  background: var(--card); border: 1px solid var(--line);
  border-radius: var(--radius); padding: 16px 18px;
  box-shadow: var(--shadow); color: var(--body) !important;
  transition: transform .14s, box-shadow .14s, border-color .14s;
  min-height: 1px;
}
a.pager:hover { transform: translateY(-2px); box-shadow: var(--shadow-lg); border-color: #cfe2f3; text-decoration: none; }
.pager-next { text-align: right; }
.pager-empty { background: transparent; border: none; box-shadow: none; }
.pager-dir { font-size: .82rem; font-weight: 700; color: var(--blue); }
.pager-code { font-family: var(--mono); font-size: .8rem; color: var(--muted); }
.pager-title { font-weight: 650; color: var(--ink); font-size: .96rem; line-height: 1.3; }

/* ---------- Footer ---------- */
.site-footer {
  border-top: 1px solid var(--line);
  background: var(--card);
  padding: 26px 0; margin-top: 24px;
  color: var(--muted); font-size: .88rem; text-align: center;
}

/* ---------- Responsive ---------- */
@media (max-width: 640px) {
  .container { padding: 0 16px; }
  .hero { padding: 52px 0 64px; }
  .prose { padding: 24px 20px 28px; }
  .pager-nav { grid-template-columns: 1fr; }
  .pager-next { text-align: left; }
  .stat { flex: 1 1 calc(50% - 14px); min-width: 0; }
}
"""


# ---------------------------------------------------------------------------
# Wikilink resolver factory
# ---------------------------------------------------------------------------
def make_resolver(sessions: list[Session]):
    """Build a lookup that maps an Obsidian wikilink target to an internal
    page href, or None if it doesn't correspond to a known session.

    Matches against: filename stem, session_code, each alias, and the H1/title.
    Returned hrefs are RELATIVE TO a page inside pages/ (so just '<file>')."""
    table: dict[str, str] = {}

    def add(key: str, filename: str):
        if not key:
            return
        table.setdefault(key.strip().lower(), filename)

    for s in sessions:
        add(s.path.stem, s.filename)
        add(s.code, s.filename)
        add(s.h1, s.filename)
        add(s.title, s.filename)
        for a in s.aliases:
            add(a, s.filename)

    def resolve(target: str):
        return table.get(target.strip().lower())

    return resolve


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    if not MARKDOWN_DIR.is_dir():
        print(f"FATAL: markdown dir not found: {MARKDOWN_DIR}", file=sys.stderr)
        return 1

    md_files = sorted(MARKDOWN_DIR.glob("*.md"))
    if not md_files:
        print(f"FATAL: no .md files in {MARKDOWN_DIR}", file=sys.stderr)
        return 1

    # Parse all sessions.
    sessions: list[Session] = []
    for f in md_files:
        try:
            sessions.append(Session(f))
        except Exception as exc:
            print(f"ERROR parsing {f.name}: {exc}", file=sys.stderr)
            raise

    sessions_sorted = sorted(sessions, key=lambda s: s.sort_key)
    resolver = make_resolver(sessions_sorted)

    # --- Clean & recreate output dirs (idempotent) ---
    if PAGES_DIR.exists():
        shutil.rmtree(PAGES_DIR)
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    # --- Stylesheet ---
    (ASSETS_DIR / "style.css").write_text(CSS, encoding="utf-8")

    # --- Per-session pages ---
    for idx, s in enumerate(sessions_sorted):
        prev_s = sessions_sorted[idx - 1] if idx > 0 else None
        next_s = sessions_sorted[idx + 1] if idx < len(sessions_sorted) - 1 else None
        body_html = render_body_html(s, resolver)
        page = build_session_page(s, body_html, prev_s, next_s)
        (PAGES_DIR / s.filename).write_text(page, encoding="utf-8")

    # --- Landing page ---
    index_html = build_index(sessions_sorted)
    (REPO_ROOT / "index.html").write_text(index_html, encoding="utf-8")

    # --- Report ---
    print("=" * 64)
    print(f"Built site for {len(sessions_sorted)} sessions.")
    print(f"  index.html        -> {REPO_ROOT / 'index.html'}")
    print(f"  assets/style.css  -> {ASSETS_DIR / 'style.css'}")
    print(f"  pages/            -> {len(list(PAGES_DIR.glob('*.html')))} HTML files")
    total_min = sum(s.duration_min for s in sessions_sorted)
    print(f"  total runtime     -> {fmt_duration(total_min)} ({total_min} min)")
    print("=" * 64)

    # Frontmatter completeness report.
    any_missing = False
    for s in sessions_sorted:
        if s.missing_fields:
            any_missing = True
            print(f"  [missing] {s.path.name}: {', '.join(s.missing_fields)}")
    if not any_missing:
        print("  All sessions had complete frontmatter (session_code, event, "
              "speakers, duration_min, source, tags, aliases) + an H1.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
