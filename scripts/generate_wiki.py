#!/usr/bin/env python3
"""
LLM Wiki generator for the Microsoft Build 2026 session-notes site.

Builds a Karpathy-style "LLM wiki" (a persistent, densely cross-linked
knowledge base) as a NEW, purely-additive section of the existing static site.
It is *re-organisation / synthesis of EXISTING published content only*: the
sole source is the frontmatter `topic/<x>` tags already present in the 127
session notes under ``markdown/``. No new facts, no web access, no invention.

Concepts  = ``topic/<x>`` tags. A concept gets its own page iff it appears on
            >= 2 sessions (~90 pages). Topics on exactly 1 session are folded
            into a "Long tail / emerging topics" list on the wiki index.
Edges     = tag co-occurrence: two concepts are related if they appear together
            on the same session; edge weight = number of shared sessions.

Outputs (all NEW, never touching existing files):
  wiki/index.html
  wiki/concepts/<slug>.html        (one per >= 2-session concept)
  wiki/graph.html                  (interactive force-directed graph)
  assets/wiki.css                  (new stylesheet; style.css untouched)

The generator is idempotent: it clears & recreates ``wiki/`` each run and
rewrites ``assets/wiki.css``, but NEVER reads-to-modify or deletes
``markdown/``, ``pages/``, ``index.html`` or ``assets/style.css``.

Usage:
    python3 scripts/generate_wiki.py
"""

from __future__ import annotations

import html
import re
import shutil
import sys
from collections import defaultdict
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths. Make sure `import yaml` does not resolve to the local ./markdown dir.
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
MARKDOWN_DIR = REPO_ROOT / "markdown"
PAGES_DIR = REPO_ROOT / "pages"
ASSETS_DIR = REPO_ROOT / "assets"
WIKI_DIR = REPO_ROOT / "wiki"
CONCEPTS_DIR = WIKI_DIR / "concepts"

_clean_path = [p for p in sys.path if Path(p or ".").resolve() != REPO_ROOT]
sys.path = _clean_path

try:
    import yaml  # type: ignore
    _HAVE_YAML = True
except Exception:  # pragma: no cover
    yaml = None  # type: ignore
    _HAVE_YAML = False

KARPATHY_GIST = "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"

# Only build a standalone concept page when a topic is on at least this many
# sessions. Everything below this threshold is "long tail".
MIN_SESSIONS_FOR_PAGE = 2

# How many related concepts to show on a concept page / how many edges to keep
# per node in the graph (top-K, to keep the graph legible while connected).
TOP_RELATED = 12
TOP_EDGES_PER_NODE = 6


# ===========================================================================
# Frontmatter parsing (mirrors generate_site.py; tolerant + safe fallback)
# ===========================================================================
def split_frontmatter(text: str) -> tuple[dict, str]:
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


def parse_yaml_frontmatter(fm_text: str) -> dict:
    if _HAVE_YAML:
        try:
            data = yaml.safe_load(fm_text)
            if isinstance(data, dict):
                return data
            return {}
        except Exception:
            pass
    return _tiny_yaml(fm_text)


def _tiny_yaml(fm_text: str) -> dict:
    out: dict = {}
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
            out[cur_key] = "" if val == "" else _strip_quotes(val)
    return out


def _strip_quotes(s: str) -> str:
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    return s


def as_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    s = str(value).strip()
    return [s] if s else []


def first_h1(body: str) -> str | None:
    for line in body.split("\n"):
        m = re.match(r"^#\s+(.*)$", line)
        if m:
            return m.group(1).strip()
    return None


def clean_title(h1: str, code: str | None) -> str:
    t = h1.strip()
    if code:
        pat = re.compile(rf"^{re.escape(code)}\s*[\u2014\u2013\-:]\s*", re.IGNORECASE)
        t2 = pat.sub("", t)
        if t2:
            t = t2
    return t


def topic_tags(tags) -> list[str]:
    out = []
    for t in as_list(tags):
        if t.startswith("topic/"):
            out.append(t[len("topic/"):])
    seen, res = set(), []
    for x in out:
        if x not in seen:
            seen.add(x)
            res.append(x)
    return res


# ===========================================================================
# Humanisation: topic slug -> pretty display name
# ===========================================================================
# Explicit overrides take priority. Anything not listed: if it is a known
# acronym -> uppercase; otherwise title-case with hyphens turned into spaces.
PRETTY_OVERRIDES = {
    "ai-foundry": "AI Foundry",
    "azure-ai-foundry": "Azure AI Foundry",
    "rag": "RAG",
    "mcp": "MCP",
    "dotnet": ".NET",
    "dotnet-maui": ".NET MAUI",
    "dotnet-aspire": ".NET Aspire",
    "ci-cd": "CI/CD",
    "aks": "AKS",
    "sre": "SRE",
    "npu": "NPU",
    "iot": "IoT",
    "kql": "KQL",
    "cli": "CLI",
    "sdk": "SDK",
    "api": "API",
    "apis": "APIs",
    "ui": "UI",
    "wsl": "WSL",
    "winui": "WinUI",
    "nosql": "NoSQL",
    "iac": "IaC",
    "llm": "LLM",
    "genai": "GenAI",
    "ai": "AI",
    "ai-coding": "AI Coding",
    "ai-sdk": "AI SDK",
    "ai-gateway": "AI Gateway",
    "ai-security": "AI Security",
    "ai-models": "AI Models",
    "ai-portal": "AI Portal",
    "microsoft-ai": "Microsoft AI",
    "windows-ai": "Windows AI",
    "edge-ai": "Edge AI",
    "on-device-ai": "On-Device AI",
    "open-source-models": "Open-Source Models",
    "sovereign-ai": "Sovereign AI",
    "github": "GitHub",
    "github-copilot": "GitHub Copilot",
    "github-actions": "GitHub Actions",
    "github-advanced-security": "GitHub Advanced Security",
    "m365": "M365",
    "m365-copilot": "M365 Copilot",
    "agent-365": "Agent 365",
    "devops": "DevOps",
    "devsecops": "DevSecOps",
    "devex": "DevEx",
    "devtools": "DevTools",
    "csharp": "C#",
    "aspnet-core": "ASP.NET Core",
    "cosmos-db": "Cosmos DB",
    "azure-sql": "Azure SQL",
    "azure-ai-search": "Azure AI Search",
    "azure-monitor": "Azure Monitor",
    "azure-database": "Azure Database",
    "azure-boost": "Azure Boost",
    "azure-devops": "Azure DevOps",
    "azure-integration": "Azure Integration",
    "azure-linux": "Azure Linux",
    "opentelemetry": "OpenTelemetry",
    "postgresql": "PostgreSQL",
    "postgres": "Postgres",
    "tidb": "TiDB",
    "documentdb": "DocumentDB",
    "nvidia": "NVIDIA",
    "redis": "Redis",
    "onelake": "OneLake",
    "fabric-iq": "Fabric IQ",
    "microsoft-iq": "Microsoft IQ",
    "real-time-intelligence": "Real-Time Intelligence",
    "responsible-ai": "Responsible AI",
    "low-code": "Low-Code",
    "no-code": "No-Code",
    "on-device": "On-Device",
    "webrtc": "WebRTC",
    "livekit": "LiveKit",
    "uipath": "UiPath",
    "devexpress": "DevExpress",
    "redhat": "Red Hat",
    "hashicorp": "HashiCorp",
    "newrelic": "New Relic",
    "hugging-face": "Hugging Face",
    "vector-search": "Vector Search",
    "agentic-web": "Agentic Web",
    "agentic-retrieval": "Agentic Retrieval",
    "agentic-coding": "Agentic Coding",
    "agent-framework": "Agent Framework",
    "agent-harness": "Agent Harness",
    "agent-memory": "Agent Memory",
    "multi-agent": "Multi-Agent",
    "coding-agents": "Coding Agents",
    "dotnet11": ".NET 11",
    "dotnetup": ".NET Upgrade",
    "winui": "WinUI",
    "windows-app-sdk": "Windows App SDK",
    "uno-platform": "Uno Platform",
    "copilot-pc": "Copilot+ PC",
    "cross-platform": "Cross-Platform",
    "cross-device": "Cross-Device",
    "real-time": "Real-Time",
    "open-source": "Open Source",
    "snapdragon": "Snapdragon",
    "qualcomm": "Qualcomm",
    "nemotron": "Nemotron",
    "anyscale": "Anyscale",
    "twilio": "Twilio",
    "oracle": "Oracle",
    "oracle-migration": "Oracle Migration",
    "intel": "Intel",
    "cobalt": "Cobalt",
    "arm": "Arm",
    "ray": "Ray",
    "mvp": "MVP",
    "java": "Java",
    "blazor": "Blazor",
    "entra": "Entra",
    "defender": "Defender",
    "purview": "Purview",
    "microsoft-purview": "Microsoft Purview",
    "policy-as-code": "Policy-as-Code",
    "pdf": "PDF",
    "teams": "Teams",
    "iot": "IoT",
}

# Acronyms (when not already overridden) → fully uppercase.
KNOWN_ACRONYMS = {
    "ai", "ml", "llm", "mcp", "rag", "aks", "sre", "npu", "iot", "kql",
    "cli", "sdk", "api", "ui", "ux", "wsl", "iac", "kpi", "sql", "ci",
    "cd", "ar", "vr", "os", "io", "cdn", "dns", "tls", "ssl", "vm",
}


def pretty(slug: str) -> str:
    s = slug.strip().lower()
    if s in PRETTY_OVERRIDES:
        return PRETTY_OVERRIDES[s]
    if s in KNOWN_ACRONYMS:
        return s.upper()
    # Default: hyphens -> spaces, title-case each word, but keep an all-acronym
    # token uppercase if it happens to be in the set.
    words = s.replace("_", "-").split("-")
    out = []
    for w in words:
        if w in KNOWN_ACRONYMS:
            out.append(w.upper())
        elif w:
            out.append(w[:1].upper() + w[1:])
    return " ".join(out) if out else slug


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "concept"


# ===========================================================================
# Clustering: map a concept (by slug + pretty name) into one thematic cluster.
# Pure keyword mapping over the concept name — deterministic, logical order.
# ===========================================================================
CLUSTER_ORDER = [
    "AI & Agents",
    "Azure & Infra",
    "Data & Databases",
    "Developer Tools & Languages",
    "Observability & Ops",
    "Security & Governance",
    "Platforms & Devices",
    "Community & Career",
    "Other",
]

# Distinct, accessible-ish palette over the Microsoft-blue family + accents.
CLUSTER_COLORS = {
    "AI & Agents":                    "#0067b8",  # primary blue
    "Azure & Infra":                  "#008575",  # teal
    "Data & Databases":               "#8661c5",  # purple
    "Developer Tools & Languages":    "#d83b01",  # orange-red
    "Observability & Ops":            "#c19c00",  # amber
    "Security & Governance":          "#a4262c",  # red
    "Platforms & Devices":            "#0a7c42",  # green
    "Community & Career":             "#5c2d91",  # deep violet
    "Other":                          "#605e5c",  # muted grey
}

# Ordered (cluster, keyword-substrings). First match wins, so order matters:
# put the more specific clusters before the broad AI bucket where needed.
_CLUSTER_RULES = [
    ("Security & Governance", [
        "security", "governance", "defender", "purview", "entra", "identity",
        "responsible", "compliance", "policy", "supply-chain", "supply chain",
        "confidential", "safety", "sovereign", "devsecops", "advanced-security",
    ]),
    ("Observability & Ops", [
        "observability", "opentelemetry", "telemetry", "monitor", "monitoring",
        "metrics", "tracing", "trace", "profiling", "sre", "reliability",
        "resilien", "incident", "production", "ci-cd", "ci/cd", "devops",
        "github-actions", "automation", "performance", "real-time-intelligence",
    ]),
    ("Data & Databases", [
        "data", "database", "databases", "sql", "postgres", "cosmos", "nosql",
        "redis", "fabric", "onelake", "lake", "warehouse", "vector", "search",
        "rag", "retrieval", "analytics", "ontology", "schema", "documentdb",
        "tidb", "oracle", "elastic", "semantic-cache", "real-time-intelligence",
        "unstructured", "content-understanding", "embeddings",
    ]),
    ("Platforms & Devices", [
        "windows", "winui", "maui", "wsl", "edge", "device", "on-device",
        "snapdragon", "qualcomm", "npu", "iot", "robotics", "hardware",
        "copilot-pc", "copilot+ pc", "mobile", "uno-platform", "windows-app-sdk",
        "cross-platform", "cross-device", "arm", "cobalt", "intel", "nvidia",
        "industrial", "quantum",
    ]),
    ("Developer Tools & Languages", [
        "dotnet", ".net", "csharp", "c#", "blazor", "aspire", "aspnet",
        "visual-studio", "devtools", "devex", "developer", "sdk", "cli",
        "tooling", "tools", "frameworks", "framework", "language", "java",
        "runtime", "debugging", "testing", "low-code", "design-systems",
        "devexpress", "code", "engineering-culture", "software-engineering",
        "app-dev", "app-development", "modernization", "migration", "blazor",
    ]),
    ("Azure & Infra", [
        "azure", "aks", "kubernetes", "containers", "cloud-native", "linux",
        "infrastructure", "iac", "terraform", "scaling", "networking",
        "storage", "app-service", "logic-apps", "hyperscale", "cloud",
        "distributed", "event-driven", "api-management", "ai-gateway",
    ]),
    ("Community & Career", [
        "community", "career", "mvp", "meetup", "learning", "skilling",
        "onboarding", "engineering-culture", "startups", "case-study",
        "support", "research",
    ]),
    ("AI & Agents", [
        "ai", "agent", "agents", "agentic", "copilot", "model", "models",
        "foundry", "mcp", "rag", "fine-tuning", "inference", "eval",
        "multimodal", "voice", "multi-agent", "memory", "distillation",
        "reinforcement", "nemotron", "genai", "llm", "orchestration",
        "conversational", "model-router", "foundation-models",
    ]),
]


def cluster_for(slug: str, name: str) -> str:
    hay = f" {slug} {name} ".lower()
    for cluster, keys in _CLUSTER_RULES:
        for k in keys:
            # word-ish containment; the haystack already has spaces padded.
            if k in hay:
                return cluster
    return "Other"


# ===========================================================================
# Data model
# ===========================================================================
class Session:
    def __init__(self, path: Path):
        self.path = path
        raw = path.read_text(encoding="utf-8")
        self.fm, self.body = split_frontmatter(raw)
        self.code = str(self.fm.get("session_code") or "").strip()
        self.aliases = as_list(self.fm.get("aliases"))
        h1 = first_h1(self.body)
        fallback = self.aliases[0] if self.aliases else path.stem
        self.h1 = h1 or fallback
        self.title = clean_title(self.h1, self.code)
        if not self.code:
            self.code = slugify(path.stem)
        self.page_file = f"{self.code}.html"
        self.topics = topic_tags(self.fm.get("tags"))

    @property
    def sort_key(self):
        m = re.match(r"^([A-Za-z]+)(\d+)", self.code)
        if m:
            return (m.group(1), int(m.group(2)), self.code)
        return (self.code, 0, self.code)


class Concept:
    def __init__(self, slug: str):
        self.slug = slug
        self.name = pretty(slug)
        self.page_slug = slugify(slug)          # filename-safe
        self.sessions: list[Session] = []        # sessions carrying this topic
        self.related: dict[str, int] = {}        # other-slug -> shared count
        self.cluster = "Other"

    @property
    def count(self) -> int:
        return len(self.sessions)

    @property
    def filename(self) -> str:
        return f"{self.page_slug}.html"


# ===========================================================================
# HTML scaffolding
# ===========================================================================
def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def page_shell(title: str, css_rel: str, body_html: str,
               extra_head: str = "", extra_tail: str = "") -> str:
    favicon = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
               "viewBox='0 0 100 100'%3E%3Crect width='48' height='48' x='2' "
               "y='2' fill='%23f25022'/%3E%3Crect width='48' height='48' x='50' "
               "y='2' fill='%237fba00'/%3E%3Crect width='48' height='48' x='2' "
               "y='50' fill='%2300a4ef'/%3E%3Crect width='48' height='48' x='50' "
               "y='50' fill='%23ffb900'/%3E%3C/svg%3E")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<link rel="stylesheet" href="{css_rel}">
<link rel="icon" href="{favicon}">
{extra_head}
</head>
<body>
{body_html}
<footer class="wiki-footer">
  <div class="wk-container">
    LLM Wiki \u00b7 a cross-linked knowledge base compiled from the
    <strong>Microsoft Build 2026</strong> session notes on this site.
    Re-organisation of existing content only \u2014 no new information added.
    Pattern after Andrej Karpathy\u2019s
    <a href="{KARPATHY_GIST}" target="_blank" rel="noopener noreferrer">LLM&#8209;wiki gist</a>.
    No tracking, no CDNs.
  </div>
</footer>
{extra_tail}
</body>
</html>
"""


def nav_bar(links: list[tuple[str, str]], active: str | None = None) -> str:
    items = []
    for label, href in links:
        cls = "wk-nav-link" + (" is-active" if label == active else "")
        items.append(f'<a class="{cls}" href="{esc(href)}">{esc(label)}</a>')
    return f'<nav class="wk-nav"><div class="wk-container wk-nav-inner">{"".join(items)}</div></nav>'


# ===========================================================================

# ===========================================================================
# Stylesheet (written to assets/wiki.css). Reuses the site's design tokens
# (redeclared :root subset) so the wiki matches the Microsoft-blue light
# theme, rounded cards and subtle shadows of the session pages.
# ===========================================================================
WIKI_CSS = r""":root {
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
  --maxw:        1180px;
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
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
}
a { color: var(--blue); text-decoration: none; }
a:hover { text-decoration: underline; }
code {
  font-family: var(--mono);
  font-size: .86em;
  background: #eef1f4;
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 1px 5px;
  color: #344;
}

.wk-container { width: 100%; max-width: var(--maxw); margin: 0 auto; padding: 0 24px; }

/* ---------- Top nav ---------- */
.wk-nav {
  background: rgba(255,255,255,.86);
  border-bottom: 1px solid var(--line);
  backdrop-filter: blur(8px);
  position: sticky; top: 0; z-index: 40;
}
.wk-nav-inner { display: flex; gap: 6px; flex-wrap: wrap; padding-top: 10px; padding-bottom: 10px; }
.wk-nav-link {
  font-size: .9rem; font-weight: 600; color: var(--blue-dark);
  padding: 7px 13px; border-radius: 999px; border: 1px solid transparent;
}
.wk-nav-link:hover { background: var(--chip-bg); text-decoration: none; }
.wk-nav-link.is-active { background: var(--blue); color: #fff; }

/* ---------- Hero (home) ---------- */
.wk-hero {
  background:
    radial-gradient(1100px 380px at 82% -12%, rgba(80,230,255,.20), transparent 60%),
    linear-gradient(135deg, var(--blue-deep) 0%, var(--blue-dark) 45%, var(--blue) 100%);
  color: #fff;
  padding: 54px 0 64px;
  position: relative; overflow: hidden;
}
.wk-hero::after {
  content: ""; position: absolute; inset: auto 0 -1px 0; height: 36px;
  background: linear-gradient(to bottom, transparent, var(--bg));
}
.wk-hero-badge {
  display: inline-block; font-size: .76rem; font-weight: 700;
  letter-spacing: .14em; text-transform: uppercase;
  background: rgba(255,255,255,.14); border: 1px solid rgba(255,255,255,.28);
  padding: 6px 14px; border-radius: 999px; margin-bottom: 16px;
}
.wk-hero-title {
  margin: 0; font-size: clamp(2rem, 4.4vw, 3.1rem);
  font-weight: 800; letter-spacing: -.02em; line-height: 1.06;
}
.wk-hero-sub { margin: 10px 0 0; font-size: clamp(1.05rem, 2.2vw, 1.35rem); font-weight: 600; color: var(--cyan); }
.wk-hero-blurb { margin: 18px 0 0; max-width: 78ch; font-size: 1.02rem; color: rgba(255,255,255,.94); }
.wk-hero-blurb a { color: #cfeeff; text-decoration: underline; }
.wk-hero-blurb code { background: rgba(255,255,255,.16); border-color: rgba(255,255,255,.28); color: #eaf6ff; }
.wk-howto {
  margin: 18px 0 0; max-width: 80ch; font-size: .96rem;
  background: rgba(255,255,255,.10); border: 1px solid rgba(255,255,255,.22);
  border-radius: var(--radius); padding: 14px 16px; color: #eef7ff;
}
.wk-howto a { color: #cfeeff; text-decoration: underline; }

.wk-cta-row { margin: 22px 0 0; display: flex; gap: 12px; flex-wrap: wrap; }
.wk-btn {
  display: inline-flex; align-items: center; gap: 8px;
  font-weight: 700; font-size: .95rem;
  padding: 11px 18px; border-radius: 999px;
  background: rgba(255,255,255,.14); color: #fff;
  border: 1px solid rgba(255,255,255,.30);
}
.wk-btn:hover { background: rgba(255,255,255,.24); text-decoration: none; }
.wk-btn-primary { background: #fff; color: var(--blue-dark); border-color: #fff; }
.wk-btn-primary:hover { background: #eaf3fb; }
.wk-btn-sm { padding: 7px 13px; font-size: .85rem; }

.wk-stats { margin: 26px 0 0; display: flex; gap: 14px; flex-wrap: wrap; }
.wk-stat {
  background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.22);
  border-radius: var(--radius); padding: 14px 20px; min-width: 130px;
}
.wk-stat-n { font-size: 1.8rem; font-weight: 800; line-height: 1; }
.wk-stat-l { font-size: .82rem; letter-spacing: .04em; text-transform: uppercase; color: rgba(255,255,255,.82); margin-top: 6px; }

/* ---------- Home body ---------- */
.wk-home-main { padding: 36px 24px 64px; }
.wk-section-head { margin: 8px 0 18px; }
.wk-h2 { font-size: 1.45rem; font-weight: 800; letter-spacing: -.01em; color: var(--ink); margin: 0 0 6px; }
.wk-note { margin: 0; color: var(--muted); font-size: .96rem; max-width: 84ch; }

.wk-cluster { margin: 30px 0 0; }
.wk-cluster-h {
  display: flex; align-items: center; gap: 10px;
  font-size: 1.12rem; font-weight: 800; color: var(--ink);
  margin: 0 0 14px; padding-bottom: 8px; border-bottom: 1px solid var(--line);
}
.wk-dot { width: 13px; height: 13px; border-radius: 50%; flex: none; box-shadow: 0 0 0 3px rgba(0,0,0,.04); }
.wk-cluster-n {
  margin-left: auto; font-size: .8rem; font-weight: 700; color: var(--chip-ink);
  background: var(--chip-bg); border-radius: 999px; padding: 2px 10px;
}
.wk-chip-wrap { display: flex; flex-wrap: wrap; gap: 10px; }
.wk-concept-chip {
  display: inline-flex; align-items: center; gap: 9px;
  background: var(--card); border: 1px solid var(--line);
  border-left: 4px solid var(--c, var(--blue));
  border-radius: var(--radius-sm); padding: 9px 12px;
  box-shadow: var(--shadow); transition: transform .08s ease, box-shadow .12s ease;
}
.wk-concept-chip:hover { transform: translateY(-2px); box-shadow: var(--shadow-lg); text-decoration: none; }
.wk-chip-name { font-weight: 650; color: var(--ink); font-size: .95rem; }
.wk-chip-count {
  font-size: .78rem; font-weight: 700; color: #fff; background: var(--c, var(--blue));
  border-radius: 999px; min-width: 22px; text-align: center; padding: 1px 7px;
}

/* ---------- Long tail ---------- */
.wk-longtail { margin: 46px 0 0; padding: 24px; background: var(--card); border: 1px solid var(--line); border-radius: var(--radius); box-shadow: var(--shadow); }
.wk-lt-wrap { margin: 14px 0 0; display: flex; flex-wrap: wrap; gap: 8px; }
.wk-lt-chip {
  font-size: .84rem; color: var(--muted);
  background: var(--bg); border: 1px solid var(--line);
  border-radius: 999px; padding: 4px 11px;
}

/* ---------- Concept page ---------- */
.wk-concept-hero {
  background:
    radial-gradient(900px 280px at 85% -20%, rgba(80,230,255,.14), transparent 60%),
    linear-gradient(135deg, var(--blue-deep), var(--blue-dark));
  color: #fff; padding: 34px 0 40px; position: relative; overflow: hidden;
  border-bottom: 5px solid var(--c, var(--blue));
}
.wk-breadcrumb { font-size: .85rem; color: rgba(255,255,255,.78); margin-bottom: 10px; }
.wk-breadcrumb a { color: #cfeeff; }
.wk-concept-title {
  margin: 0; font-size: clamp(1.7rem, 3.6vw, 2.6rem); font-weight: 800;
  letter-spacing: -.02em; display: flex; align-items: center; gap: 14px; flex-wrap: wrap;
}
.wk-count-badge {
  font-size: .82rem; font-weight: 700; letter-spacing: .02em;
  background: var(--c, rgba(255,255,255,.18)); color: #fff;
  border: 1px solid rgba(255,255,255,.34);
  border-radius: 999px; padding: 5px 14px;
}
.wk-concept-sub { margin: 12px 0 0; max-width: 80ch; color: rgba(255,255,255,.92); font-size: .98rem; }
.wk-concept-sub code { background: rgba(255,255,255,.16); border-color: rgba(255,255,255,.28); color: #eaf6ff; }

.wk-concept-main { padding: 30px 24px 56px; }
.wk-grid2 { display: grid; grid-template-columns: 1.6fr 1fr; gap: 22px; align-items: start; }
.wk-card {
  background: var(--card); border: 1px solid var(--line);
  border-radius: var(--radius); box-shadow: var(--shadow); padding: 22px 24px;
}
.wk-card .wk-h2 { font-size: 1.2rem; margin-bottom: 4px; }

.wk-session-list { list-style: none; margin: 14px 0 0; padding: 0; display: flex; flex-direction: column; gap: 8px; }
.wk-session a {
  display: flex; align-items: baseline; gap: 12px;
  padding: 9px 12px; border-radius: var(--radius-sm);
  border: 1px solid var(--line); background: #fcfdff;
}
.wk-session a:hover { background: var(--chip-bg); text-decoration: none; border-color: #cfe3f5; }
.wk-code {
  font-family: var(--mono); font-size: .78rem; font-weight: 700; color: var(--chip-ink);
  background: var(--chip-bg); border-radius: 6px; padding: 2px 8px; flex: none; min-width: 62px; text-align: center;
}
.wk-stitle { color: var(--ink); font-weight: 550; font-size: .96rem; }

.wk-card-rel { position: sticky; top: 64px; }
.wk-rel-list { list-style: none; margin: 14px 0 0; padding: 0; display: flex; flex-direction: column; gap: 7px; }
.wk-rel a {
  display: flex; align-items: center; justify-content: space-between; gap: 10px;
  padding: 8px 12px; border-radius: var(--radius-sm);
  border: 1px solid var(--line); border-left: 4px solid var(--c, var(--blue));
  background: #fcfdff;
}
.wk-rel a:hover { background: var(--chip-bg); text-decoration: none; }
.wk-rel-name { font-weight: 600; color: var(--ink); font-size: .94rem; }
.wk-rel-w { font-size: .76rem; color: var(--muted); white-space: nowrap; }
.wk-empty { color: var(--muted); font-style: italic; list-style: none; }
.wk-graphlink { display: inline-block; margin-top: 14px; font-weight: 700; font-size: .9rem; }

.wk-derived {
  margin: 26px 0 0; padding: 16px 18px; font-size: .9rem; color: var(--muted);
  background: #fbfcfe; border: 1px dashed var(--line); border-radius: var(--radius);
  max-width: 96ch;
}
.wk-derived code { font-size: .82em; }

/* ---------- Graph page ---------- */
.wk-graph-head { background: var(--card); border-bottom: 1px solid var(--line); padding: 22px 0 18px; }
.wk-graph-title { margin: 0; font-size: clamp(1.5rem, 3vw, 2.1rem); font-weight: 800; color: var(--ink); letter-spacing: -.01em; }
.wk-graph-sub { margin: 8px 0 0; color: var(--muted); max-width: 92ch; font-size: .95rem; }
.wk-graph-toolbar { margin: 16px 0 0; display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }
.wk-search {
  flex: 1 1 280px; min-width: 220px; max-width: 380px;
  font: inherit; font-size: .95rem; padding: 9px 14px;
  border: 1px solid var(--line); border-radius: 999px; background: #fff; color: var(--ink);
}
.wk-search:focus { outline: none; border-color: var(--blue); box-shadow: 0 0 0 3px rgba(0,103,184,.16); }
.wk-toggle { display: inline-flex; align-items: center; gap: 7px; font-size: .9rem; color: var(--muted); font-weight: 600; user-select: none; }
.wk-legend { display: flex; gap: 14px; flex-wrap: wrap; margin-left: auto; }
.wk-leg { display: inline-flex; align-items: center; gap: 6px; font-size: .82rem; color: var(--muted); }
.wk-leg-dot { width: 11px; height: 11px; border-radius: 50%; flex: none; }

.wk-graph-wrap { padding: 0; }
.wk-stage {
  position: relative; width: 100%;
  height: calc(100vh - 250px); min-height: 460px;
  background:
    radial-gradient(1000px 500px at 50% 0%, #ffffff, var(--bg) 70%);
  border-bottom: 1px solid var(--line);
}
#wk-svg { width: 100%; height: 100%; display: block; cursor: grab; }
.wk-edge { stroke: #9fb6cc; transition: stroke-opacity .15s ease; }
.wk-node { cursor: pointer; stroke: #fff; stroke-width: 1.5; transition: opacity .15s ease, stroke-width .1s ease; }
.wk-node:hover, .wk-node.wk-hot { stroke-width: 2.5; }
.wk-node:focus { outline: none; stroke: var(--ink); stroke-width: 3; }
.wk-label {
  font-family: var(--font); font-size: 11px; font-weight: 600; fill: #33414f;
  paint-order: stroke; stroke: #fff; stroke-width: 3px; stroke-linejoin: round;
  pointer-events: none; user-select: none;
}
/* focus/dim states */
.wk-has-focus .wk-node:not(.wk-hot) { opacity: .12; }
.wk-has-focus .wk-label:not(.wk-hot) { opacity: .08; }
.wk-has-focus .wk-edge:not(.wk-hot) { stroke-opacity: .04 !important; }
.wk-has-focus .wk-edge.wk-hot { stroke: var(--blue); stroke-opacity: .75 !important; }

.wk-tooltip {
  position: absolute; pointer-events: none; z-index: 5;
  background: rgba(27,26,25,.95); color: #fff;
  border-radius: 10px; padding: 8px 12px; font-size: .85rem;
  box-shadow: 0 8px 24px rgba(0,0,0,.28); max-width: 240px;
}
.wk-tooltip strong { display: block; font-size: .95rem; margin-bottom: 2px; }
.wk-tooltip span { color: #bcd; font-size: .8rem; }
.wk-caption {
  position: absolute; left: 16px; bottom: 12px;
  font-size: .8rem; color: var(--muted);
  background: rgba(255,255,255,.82); border: 1px solid var(--line);
  border-radius: 999px; padding: 4px 12px;
}

/* ---------- Footer ---------- */
.wk-footer {
  border-top: 1px solid var(--line); background: var(--card);
  color: var(--muted); font-size: .88rem; padding: 22px 0; margin-top: 0;
}
.wk-footer a { color: var(--blue); text-decoration: underline; }
.wk-footer .wk-container { max-width: 96ch; }

/* ---------- Responsive ---------- */
@media (max-width: 860px) {
  .wk-grid2 { grid-template-columns: 1fr; }
  .wk-card-rel { position: static; }
  .wk-legend { margin-left: 0; }
}
@media (max-width: 640px) {
  .wk-container { padding: 0 16px; }
  .wk-hero { padding: 40px 0 52px; }
  .wk-stat { flex: 1 1 calc(50% - 14px); min-width: 0; }
  .wk-stage { height: calc(100vh - 300px); min-height: 380px; }
}
"""

# ===========================================================================
# Concept page
# ===========================================================================
def build_concept_page(c: Concept, concepts_by_slug: dict) -> str:
    nav = nav_bar([
        ("\u2190 LLM Wiki home", "../index.html"),
        ("Graph view", "../graph.html"),
        ("Main site", "../../index.html"),
    ])

    # Sessions list (alpha by code), each links to the real session page.
    sess_sorted = sorted(c.sessions, key=lambda s: s.sort_key)
    sess_items = []
    for s in sess_sorted:
        href = f"../../pages/{esc(s.page_file)}"
        sess_items.append(
            f'<li class="wk-session">'
            f'<a href="{href}"><span class="wk-code">{esc(s.code)}</span>'
            f'<span class="wk-stitle">{esc(s.title)}</span></a></li>'
        )
    sessions_html = "\n      ".join(sess_items)

    # Related concepts (by shared-session weight, desc; tie-break alpha).
    rel = sorted(
        c.related.items(),
        key=lambda kv: (-kv[1], concepts_by_slug[kv[0]].name.lower()),
    )[:TOP_RELATED]
    rel_items = []
    for other_slug, w in rel:
        oc = concepts_by_slug[other_slug]
        href = f"{esc(oc.filename)}"
        noun = "session" if w == 1 else "sessions"
        rel_items.append(
            f'<li class="wk-rel">'
            f'<a href="{href}" style="--c:{CLUSTER_COLORS[oc.cluster]}">'
            f'<span class="wk-rel-name">{esc(oc.name)}</span>'
            f'<span class="wk-rel-w">{w} shared {noun}</span></a></li>'
        )
    related_html = "\n      ".join(rel_items) if rel_items else (
        '<li class="wk-empty">No co-occurring concepts.</li>'
    )

    n = c.count
    noun = "session" if n == 1 else "sessions"
    body = f"""
{nav}
<header class="wk-concept-hero" style="--c:{CLUSTER_COLORS[c.cluster]}">
  <div class="wk-container">
    <div class="wk-breadcrumb"><a href="../index.html">LLM Wiki</a> \u203a
      <a href="../index.html#cluster-{esc(slugify(c.cluster))}">{esc(c.cluster)}</a></div>
    <h1 class="wk-concept-title">{esc(c.name)}
      <span class="wk-count-badge" title="Sessions tagged with this concept">{n} {noun}</span>
    </h1>
    <p class="wk-concept-sub">A concept node in the Build 2026 LLM Wiki \u2014
      derived from the <code>topic/{esc(c.slug)}</code> tag across the session notes.
      Cluster: <strong>{esc(c.cluster)}</strong>.</p>
  </div>
</header>

<main class="wk-container wk-concept-main">
  <div class="wk-grid2">
    <section class="wk-card">
      <h2 class="wk-h2">Appears in {n} {noun}</h2>
      <p class="wk-note">Every session below carries the <code>topic/{esc(c.slug)}</code>
        tag in its notes. Links open the full session page on the main site.</p>
      <ul class="wk-session-list">
      {sessions_html}
      </ul>
    </section>

    <aside class="wk-card wk-card-rel">
      <h2 class="wk-h2">Related concepts</h2>
      <p class="wk-note">Concepts that co-occur with <strong>{esc(c.name)}</strong>
        on the same sessions, ranked by how many sessions they share.</p>
      <ul class="wk-rel-list">
      {related_html}
      </ul>
      <a class="wk-graphlink" href="../graph.html">Explore in the graph view \u2192</a>
    </aside>
  </div>

  <p class="wk-derived">
    Content on this page is a re-organisation of the
    <strong>Microsoft Build 2026</strong> session notes published on this site.
    Session membership and the "related concepts" weights are derived purely from
    the <code>topic/</code> tags in those notes \u2014 no new facts were added.
  </p>
</main>
"""
    return page_shell(
        title=f"{c.name} \u2014 Build 2026 LLM Wiki",
        css_rel="../../assets/wiki.css",
        body_html=body,
    )


# ===========================================================================
# Wiki index (home)
# ===========================================================================
def build_index_page(concepts: list, longtail: list,
                     n_sessions: int, n_edges: int) -> str:
    nav = nav_bar([
        ("LLM Wiki home", "index.html"),
        ("Graph view", "graph.html"),
        ("Main site", "../index.html"),
        ("All sessions", "../index.html"),
    ], active="LLM Wiki home")

    # Group concept pages by cluster.
    by_cluster: dict = defaultdict(list)
    for c in concepts:
        by_cluster[c.cluster].append(c)

    cluster_blocks = []
    for cluster in CLUSTER_ORDER:
        items = sorted(by_cluster.get(cluster, []), key=lambda c: c.name.lower())
        if not items:
            continue
        chips = []
        for c in items:
            noun = "session" if c.count == 1 else "sessions"
            chips.append(
                f'<a class="wk-concept-chip" href="concepts/{esc(c.filename)}" '
                f'style="--c:{CLUSTER_COLORS[cluster]}">'
                f'<span class="wk-chip-name">{esc(c.name)}</span>'
                f'<span class="wk-chip-count" title="{c.count} {noun}">{c.count}</span></a>'
            )
        cluster_blocks.append(
            f'<section class="wk-cluster" id="cluster-{esc(slugify(cluster))}">'
            f'<h3 class="wk-cluster-h"><span class="wk-dot" '
            f'style="background:{CLUSTER_COLORS[cluster]}"></span>{esc(cluster)}'
            f'<span class="wk-cluster-n">{len(items)}</span></h3>'
            f'<div class="wk-chip-wrap">{"".join(chips)}</div></section>'
        )
    clusters_html = "\n".join(cluster_blocks)

    # Long tail (single-session topics): plain text chips, no links.
    lt_sorted = sorted(longtail, key=lambda t: pretty(t).lower())
    lt_chips = "".join(
        f'<span class="wk-lt-chip">{esc(pretty(t))}</span>' for t in lt_sorted
    )

    n_concepts = len(concepts)
    body = f"""
{nav}
<header class="wk-hero">
  <div class="wk-container">
    <div class="wk-hero-badge">LLM Wiki</div>
    <h1 class="wk-hero-title">Microsoft Build 2026 &mdash; LLM Wiki</h1>
    <p class="wk-hero-sub">A densely cross-linked knowledge base compiled from the
      Build&nbsp;2026 session notes.</p>
    <p class="wk-hero-blurb">
      This is a <strong>Karpathy-style &ldquo;LLM wiki&rdquo;</strong>
      (<a href="{KARPATHY_GIST}" target="_blank" rel="noopener noreferrer">the pattern Andrej
      Karpathy popularised</a>): instead of reading notes linearly, knowledge is broken into
      <em>concept nodes</em> that link to the sessions they appear in and to each other, so you
      <em>traverse</em> the material by following links and the graph view. Every concept here is a
      <code>topic/</code> tag drawn from this site&rsquo;s 127 session notes &mdash; this page is purely a
      <strong>re-organisation of the existing content</strong>, with no new information added.
    </p>
    <div class="wk-howto">
      <strong>How to read it:</strong> start from a concept below or open the
      <a href="graph.html">graph view</a>; click a node to jump to its page; from there follow
      <em>Related concepts</em> to neighbouring ideas, or open any session to read the full notes
      on the main site.
    </div>
    <div class="wk-cta-row">
      <a class="wk-btn wk-btn-primary" href="graph.html">\U0001f578\ufe0f  Open the concept graph</a>
      <a class="wk-btn" href="../index.html">\u2190  Back to all sessions</a>
    </div>
    <div class="wk-stats">
      <div class="wk-stat"><div class="wk-stat-n">{n_concepts}</div><div class="wk-stat-l">Concept pages</div></div>
      <div class="wk-stat"><div class="wk-stat-n">{n_edges}</div><div class="wk-stat-l">Cross-concept links</div></div>
      <div class="wk-stat"><div class="wk-stat-n">{n_sessions}</div><div class="wk-stat-l">Sessions covered</div></div>
    </div>
  </div>
</header>

<main class="wk-container wk-home-main">
  <div class="wk-section-head">
    <h2 class="wk-h2">Concept catalog</h2>
    <p class="wk-note">{n_concepts} concepts that appear on two or more sessions, grouped into
      thematic clusters. The number on each chip is how many sessions mention that concept.</p>
  </div>
  {clusters_html}

  <section class="wk-longtail">
    <h2 class="wk-h2">Long tail / emerging topics</h2>
    <p class="wk-note">{len(lt_sorted)} topics that appear on exactly one session each. These don&rsquo;t
      get their own concept page (too few connections to be a useful node), but they show the breadth
      of the conference. Each is still tagged on its session in the main notes.</p>
    <div class="wk-lt-wrap">{lt_chips}</div>
  </section>
</main>
"""
    return page_shell(
        title="Microsoft Build 2026 \u2014 LLM Wiki",
        css_rel="assets/wiki.css",
        body_html=body,
    ).replace('href="assets/wiki.css"', 'href="../assets/wiki.css"')


# ===========================================================================
# Graph view (interactive, vanilla JS force sim, no external libs)
# ===========================================================================
def build_graph_page(concepts: list, edges: list) -> str:
    nav = nav_bar([
        ("\u2190 LLM Wiki home", "index.html"),
        ("Graph view", "graph.html"),
        ("Main site", "../index.html"),
    ], active="Graph view")

    # Build JSON-ish inline data (hand-serialised to keep it dependency-free
    # and to avoid importing json just for this — but json is stdlib, use it).
    import json
    idx_of = {c.page_slug: i for i, c in enumerate(concepts)}
    nodes = [
        {
            "id": c.page_slug,
            "name": c.name,
            "count": c.count,
            "cluster": c.cluster,
            "color": CLUSTER_COLORS[c.cluster],
            "file": c.filename,
        }
        for c in concepts
    ]
    links = [
        {"s": idx_of[a], "t": idx_of[b], "w": w}
        for (a, b, w) in edges
        if a in idx_of and b in idx_of
    ]
    legend_items = "".join(
        f'<span class="wk-leg"><span class="wk-leg-dot" style="background:{CLUSTER_COLORS[cl]}"></span>{esc(cl)}</span>'
        for cl in CLUSTER_ORDER if any(c.cluster == cl for c in concepts)
    )

    data_json = json.dumps({"nodes": nodes, "links": links}, ensure_ascii=False)

    body = f"""
{nav}
<header class="wk-graph-head">
  <div class="wk-container">
    <h1 class="wk-graph-title">Concept graph</h1>
    <p class="wk-graph-sub">Each node is a concept ({len(nodes)} of them); each edge means the two
      concepts share at least one session. <strong>Node size</strong> = number of sessions;
      <strong>colour</strong> = cluster; <strong>edge thickness</strong> = shared-session count.
      Hover to highlight neighbours, drag to rearrange, click a node to open its page.</p>
    <div class="wk-graph-toolbar">
      <input id="wk-search" class="wk-search" type="search" placeholder="\U0001f50d  Highlight concepts by name\u2026" autocomplete="off" aria-label="Search concepts">
      <label class="wk-toggle"><input type="checkbox" id="wk-labels" checked> Labels</label>
      <button id="wk-reheat" class="wk-btn wk-btn-sm" type="button">Reheat</button>
      <span class="wk-legend">{legend_items}</span>
    </div>
  </div>
</header>

<main class="wk-graph-wrap">
  <div id="wk-stage" class="wk-stage">
    <svg id="wk-svg" role="img" aria-label="Concept co-occurrence graph"></svg>
    <div id="wk-tooltip" class="wk-tooltip" hidden></div>
    <div class="wk-caption">edges = shared sessions \u00b7 click a node to open its page</div>
  </div>
</main>

<script id="wk-data" type="application/json">{data_json}</script>
{GRAPH_JS}
"""
    return page_shell(
        title="Concept graph \u2014 Build 2026 LLM Wiki",
        css_rel="assets/wiki.css",
        body_html=body,
    ).replace('href="assets/wiki.css"', 'href="../assets/wiki.css"')

# ===========================================================================
# Inline graph JavaScript — self-contained force-directed sim, no CDNs.
# ===========================================================================
GRAPH_JS = r"""<script>
(function () {
  "use strict";
  var raw = document.getElementById("wk-data").textContent;
  var data = JSON.parse(raw);
  var nodes = data.nodes, links = data.links;
  var svg = document.getElementById("wk-svg");
  var stage = document.getElementById("wk-stage");
  var tooltip = document.getElementById("wk-tooltip");
  var searchBox = document.getElementById("wk-search");
  var labelToggle = document.getElementById("wk-labels");
  var reheatBtn = document.getElementById("wk-reheat");
  var SVGNS = "http://www.w3.org/2000/svg";

  var W = 1000, H = 700;
  function measure() {
    var r = stage.getBoundingClientRect();
    W = Math.max(360, r.width);
    H = Math.max(420, r.height);
    svg.setAttribute("viewBox", "0 0 " + W + " " + H);
  }
  measure();

  // ---- node radius from session count ----
  var maxCount = 1, minCount = 1e9;
  nodes.forEach(function (n) { maxCount = Math.max(maxCount, n.count); minCount = Math.min(minCount, n.count); });
  function radius(n) {
    var t = (n.count - minCount) / Math.max(1, (maxCount - minCount));
    return 7 + Math.sqrt(t) * 22;   // 7 .. ~29 px
  }

  // ---- adjacency for highlight ----
  var nbr = nodes.map(function () { return {}; });
  links.forEach(function (l) { nbr[l.s][l.t] = 1; nbr[l.t][l.s] = 1; });

  // ---- initial layout: circle + jitter (deterministic-ish) ----
  var seed = 1337;
  function rnd() { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x7fffffff; }
  nodes.forEach(function (n, i) {
    var a = (i / nodes.length) * Math.PI * 2;
    var rad = Math.min(W, H) * 0.34;
    n.x = W / 2 + Math.cos(a) * rad + (rnd() - 0.5) * 60;
    n.y = H / 2 + Math.sin(a) * rad + (rnd() - 0.5) * 60;
    n.vx = 0; n.vy = 0;
    n.r = radius(n);
  });

  // ---- SVG groups: edges under nodes ----
  var gEdges = document.createElementNS(SVGNS, "g");
  var gNodes = document.createElementNS(SVGNS, "g");
  var gLabels = document.createElementNS(SVGNS, "g");
  svg.appendChild(gEdges); svg.appendChild(gNodes); svg.appendChild(gLabels);

  var maxW = 1; links.forEach(function (l) { maxW = Math.max(maxW, l.w); });
  var lineEls = links.map(function (l) {
    var ln = document.createElementNS(SVGNS, "line");
    ln.setAttribute("class", "wk-edge");
    var sw = 0.6 + (l.w / maxW) * 4.0;
    ln.setAttribute("stroke-width", sw.toFixed(2));
    ln.setAttribute("stroke-opacity", (0.18 + (l.w / maxW) * 0.4).toFixed(2));
    gEdges.appendChild(ln);
    return ln;
  });

  var nodeEls = [], labelEls = [];
  nodes.forEach(function (n, i) {
    var c = document.createElementNS(SVGNS, "circle");
    c.setAttribute("class", "wk-node");
    c.setAttribute("r", n.r);
    c.setAttribute("fill", n.color);
    c.setAttribute("data-i", i);
    c.setAttribute("tabindex", "0");
    c.setAttribute("role", "link");
    c.setAttribute("aria-label", n.name + ", " + n.count + " sessions");
    gNodes.appendChild(c);
    nodeEls.push(c);

    var t = document.createElementNS(SVGNS, "text");
    t.setAttribute("class", "wk-label");
    t.setAttribute("text-anchor", "middle");
    t.textContent = n.name;
    gLabels.appendChild(t);
    labelEls.push(t);
  });

  // ---- force simulation ----
  var alpha = 1.0, alphaMin = 0.005, alphaDecay = 0.0228, running = true;
  var CENTER_K = 0.012, LINK_K = 0.045, CHARGE = -1400, LINK_DIST = 90;

  function step() {
    // charge (repulsion) — O(n^2), fine for ~90 nodes
    for (var i = 0; i < nodes.length; i++) {
      var a = nodes[i];
      for (var j = i + 1; j < nodes.length; j++) {
        var b = nodes[j];
        var dx = a.x - b.x, dy = a.y - b.y;
        var d2 = dx * dx + dy * dy + 0.01;
        var d = Math.sqrt(d2);
        var force = (CHARGE * alpha) / d2;
        var fx = (dx / d) * force, fy = (dy / d) * force;
        a.vx += fx; a.vy += fy;
        b.vx -= fx; b.vy -= fy;
      }
    }
    // links (springs)
    for (var k = 0; k < links.length; k++) {
      var l = links[k];
      var s = nodes[l.s], t = nodes[l.t];
      var dx = t.x - s.x, dy = t.y - s.y;
      var d = Math.sqrt(dx * dx + dy * dy) + 0.01;
      var desired = LINK_DIST / (1 + Math.log(1 + l.w));
      var diff = (d - desired) / d;
      var f = LINK_K * diff * alpha;
      var fx = dx * f, fy = dy * f;
      s.vx += fx; s.vy += fy;
      t.vx -= fx; t.vy -= fy;
    }
    // centering + integrate
    for (var m = 0; m < nodes.length; m++) {
      var n = nodes[m];
      n.vx += (W / 2 - n.x) * CENTER_K * alpha;
      n.vy += (H / 2 - n.y) * CENTER_K * alpha;
      if (n.fx != null) { n.x = n.fx; n.y = n.fy; n.vx = 0; n.vy = 0; }
      else {
        n.vx *= 0.82; n.vy *= 0.82;
        n.x += n.vx; n.y += n.vy;
        var pad = n.r + 4;
        n.x = Math.max(pad, Math.min(W - pad, n.x));
        n.y = Math.max(pad, Math.min(H - pad, n.y));
      }
    }
    alpha = Math.max(0, alpha - alphaDecay * alpha);
  }

  function draw() {
    for (var k = 0; k < links.length; k++) {
      var l = links[k], s = nodes[l.s], t = nodes[l.t];
      var ln = lineEls[k];
      ln.setAttribute("x1", s.x.toFixed(1)); ln.setAttribute("y1", s.y.toFixed(1));
      ln.setAttribute("x2", t.x.toFixed(1)); ln.setAttribute("y2", t.y.toFixed(1));
    }
    for (var i = 0; i < nodes.length; i++) {
      var n = nodes[i];
      nodeEls[i].setAttribute("cx", n.x.toFixed(1));
      nodeEls[i].setAttribute("cy", n.y.toFixed(1));
      var lab = labelEls[i];
      lab.setAttribute("x", n.x.toFixed(1));
      lab.setAttribute("y", (n.y - n.r - 4).toFixed(1));
    }
  }

  var rafId = null;
  function tick() {
    step();
    draw();
    if (alpha > alphaMin && running) {
      rafId = requestAnimationFrame(tick);
    } else {
      running = false; rafId = null;
    }
  }
  function reheat(a) {
    alpha = a || 0.9; running = true;
    if (!rafId) rafId = requestAnimationFrame(tick);
  }
  tick();

  // ---- labels toggle ----
  function applyLabels() { gLabels.style.display = labelToggle.checked ? "" : "none"; }
  labelToggle.addEventListener("change", applyLabels);
  applyLabels();

  // ---- highlight logic ----
  function setHighlight(i) {
    if (i == null) {
      svg.classList.remove("wk-has-focus");
      nodeEls.forEach(function (e) { e.classList.remove("wk-dim", "wk-hot"); });
      labelEls.forEach(function (e) { e.classList.remove("wk-dim", "wk-hot"); });
      lineEls.forEach(function (e) { e.classList.remove("wk-dim", "wk-hot"); });
      return;
    }
    svg.classList.add("wk-has-focus");
    for (var k = 0; k < nodes.length; k++) {
      var on = (k === i) || nbr[i][k];
      nodeEls[k].classList.toggle("wk-hot", on);
      nodeEls[k].classList.toggle("wk-dim", !on);
      labelEls[k].classList.toggle("wk-hot", on);
      labelEls[k].classList.toggle("wk-dim", !on);
    }
    for (var e = 0; e < links.length; e++) {
      var l = links[e];
      var on2 = (l.s === i || l.t === i);
      lineEls[e].classList.toggle("wk-hot", on2);
      lineEls[e].classList.toggle("wk-dim", !on2);
    }
  }

  function showTip(n, px, py) {
    tooltip.innerHTML = '<strong>' + escapeHtml(n.name) + '</strong><span>' +
      n.count + (n.count === 1 ? ' session' : ' sessions') + ' \u00b7 ' + escapeHtml(n.cluster) + '</span>';
    tooltip.hidden = false;
    var sr = stage.getBoundingClientRect();
    var x = px - sr.left + 14, y = py - sr.top + 14;
    var tw = tooltip.offsetWidth, th = tooltip.offsetHeight;
    if (x + tw > sr.width) x = px - sr.left - tw - 14;
    if (y + th > sr.height) y = py - sr.top - th - 14;
    tooltip.style.left = x + "px";
    tooltip.style.top = y + "px";
  }
  function hideTip() { tooltip.hidden = true; }
  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  // ---- pointer interactions (hover, drag, click) ----
  var dragI = null, didDrag = false, downXY = null;
  nodeEls.forEach(function (el, i) {
    el.addEventListener("pointerenter", function (ev) {
      if (dragI == null) { setHighlight(i); showTip(nodes[i], ev.clientX, ev.clientY); }
    });
    el.addEventListener("pointermove", function (ev) {
      if (dragI == null) showTip(nodes[i], ev.clientX, ev.clientY);
    });
    el.addEventListener("pointerleave", function () {
      if (dragI == null) { setHighlight(null); hideTip(); }
    });
    el.addEventListener("pointerdown", function (ev) {
      dragI = i; didDrag = false; downXY = [ev.clientX, ev.clientY];
      nodes[i].fx = nodes[i].x; nodes[i].fy = nodes[i].y;
      el.setPointerCapture(ev.pointerId);
      reheat(0.5);
      ev.preventDefault();
    });
    el.addEventListener("pointermove", function (ev) {
      if (dragI !== i) return;
      var pt = clientToSvg(ev.clientX, ev.clientY);
      nodes[i].fx = pt.x; nodes[i].fy = pt.y;
      if (downXY) {
        var dd = Math.hypot(ev.clientX - downXY[0], ev.clientY - downXY[1]);
        if (dd > 4) didDrag = true;
      }
      reheat(0.4);
    });
    el.addEventListener("pointerup", function (ev) {
      if (dragI === i) {
        nodes[i].fx = null; nodes[i].fy = null;
        try { el.releasePointerCapture(ev.pointerId); } catch (e) {}
        dragI = null;
        if (!didDrag) { window.location.href = "concepts/" + nodes[i].file; }
      }
    });
    el.addEventListener("keydown", function (ev) {
      if (ev.key === "Enter" || ev.key === " ") {
        ev.preventDefault();
        window.location.href = "concepts/" + nodes[i].file;
      }
    });
    el.addEventListener("focus", function () { setHighlight(i); });
    el.addEventListener("blur", function () { setHighlight(null); });
  });

  function clientToSvg(cx, cy) {
    var r = svg.getBoundingClientRect();
    return { x: (cx - r.left) / r.width * W, y: (cy - r.top) / r.height * H };
  }

  // ---- search / filter highlight ----
  searchBox.addEventListener("input", function () {
    var q = searchBox.value.trim().toLowerCase();
    if (!q) {
      svg.classList.remove("wk-has-focus");
      nodeEls.forEach(function (e) { e.classList.remove("wk-dim", "wk-hot"); });
      labelEls.forEach(function (e) { e.classList.remove("wk-dim", "wk-hot"); });
      lineEls.forEach(function (e) { e.classList.remove("wk-dim", "wk-hot"); });
      return;
    }
    svg.classList.add("wk-has-focus");
    var hits = {};
    nodes.forEach(function (n, i) {
      var on = n.name.toLowerCase().indexOf(q) !== -1;
      hits[i] = on;
      nodeEls[i].classList.toggle("wk-hot", on);
      nodeEls[i].classList.toggle("wk-dim", !on);
      labelEls[i].classList.toggle("wk-hot", on);
      labelEls[i].classList.toggle("wk-dim", !on);
    });
    lineEls.forEach(function (e, k) {
      var l = links[k];
      var on = hits[l.s] && hits[l.t];
      e.classList.toggle("wk-hot", on);
      e.classList.toggle("wk-dim", !on);
    });
  });

  reheatBtn.addEventListener("click", function () { reheat(0.95); });

  // ---- responsive ----
  var rt = null;
  window.addEventListener("resize", function () {
    clearTimeout(rt);
    rt = setTimeout(function () { measure(); reheat(0.5); }, 160);
  });
})();
</script>"""


# ===========================================================================
# Main: parse -> build concepts/edges/clusters -> write outputs
# ===========================================================================
def main() -> int:
    if not MARKDOWN_DIR.is_dir():
        print(f"FATAL: markdown dir not found: {MARKDOWN_DIR}", file=sys.stderr)
        return 1
    md_files = sorted(MARKDOWN_DIR.glob("*.md"))
    if not md_files:
        print(f"FATAL: no .md files in {MARKDOWN_DIR}", file=sys.stderr)
        return 1

    sessions = [Session(f) for f in md_files]

    # topic-slug -> Concept (all topics, including single-session ones)
    all_concepts: dict = {}
    for s in sessions:
        for slug in s.topics:
            c = all_concepts.get(slug)
            if c is None:
                c = Concept(slug)
                all_concepts[slug] = c
            c.sessions.append(s)

    # Split into page-worthy concepts (>=2 sessions) vs long tail (==1).
    page_concepts = [c for c in all_concepts.values()
                     if c.count >= MIN_SESSIONS_FOR_PAGE]
    longtail = [slug for slug, c in all_concepts.items()
                if c.count < MIN_SESSIONS_FOR_PAGE]

    # Assign clusters.
    for c in page_concepts:
        c.cluster = cluster_for(c.slug, c.name)

    page_slugs = {c.slug for c in page_concepts}
    by_slug = {c.slug: c for c in page_concepts}

    # ---- co-occurrence edges (only between page-worthy concepts) ----
    pair_weight: dict = defaultdict(int)
    for s in sessions:
        present = sorted(t for t in set(s.topics) if t in page_slugs)
        for i in range(len(present)):
            for j in range(i + 1, len(present)):
                pair_weight[(present[i], present[j])] += 1

    # Fill each concept's related map.
    for (a, b), w in pair_weight.items():
        by_slug[a].related[b] = w
        by_slug[b].related[a] = w

    # ---- full edge list for the graph (threshold + top-K per node, keep
    #      graph connected by always keeping each node's single strongest edge).
    edges_full = [(a, b, w) for (a, b), w in pair_weight.items()]
    # Build candidate set: top-K strongest edges incident to each node, plus
    # all edges with weight above a small threshold. Union keeps it connected.
    THRESH = 2  # keep edges with weight >= 2 outright …
    keep = set()
    # per-node strongest edges (ensures connectivity even for weak nodes)
    incident: dict = defaultdict(list)
    for (a, b, w) in edges_full:
        incident[a].append((w, b))
        incident[b].append((w, a))
    for node in sorted(incident):
        lst = incident[node]
        # Sort by weight desc, then by neighbour slug for a stable tie-break.
        lst.sort(key=lambda wo: (-wo[0], wo[1]))
        for w, other in lst[:TOP_EDGES_PER_NODE]:
            key = tuple(sorted((node, other)))
            keep.add(key)
    for (a, b, w) in edges_full:
        if w >= THRESH:
            keep.add(tuple(sorted((a, b))))
    wmap = {tuple(sorted((a, b))): w for (a, b, w) in edges_full}
    # Deterministic order: strongest edges first, then alphabetical by endpoints.
    # Guarantees byte-identical output across runs (fully idempotent build).
    graph_edges = [
        (key[0], key[1], wmap[key])
        for key in sorted(keep, key=lambda k: (-wmap[k], k[0], k[1]))
    ]

    n_sessions = len(sessions)
    n_concepts = len(page_concepts)
    n_edges_total = len(edges_full)          # all cross-concept co-occurrence pairs
    n_edges_graph = len(graph_edges)

    # ---- clean & recreate wiki/ (idempotent). Never touch existing dirs. ----
    if WIKI_DIR.exists():
        shutil.rmtree(WIKI_DIR)
    CONCEPTS_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    # ---- stylesheet (new, separate file) ----
    (ASSETS_DIR / "wiki.css").write_text(WIKI_CSS, encoding="utf-8")

    # ---- concept pages ----
    concepts_sorted = sorted(page_concepts, key=lambda c: c.name.lower())
    for c in concepts_sorted:
        (CONCEPTS_DIR / c.filename).write_text(
            build_concept_page(c, by_slug), encoding="utf-8"
        )

    # ---- index + graph ----
    (WIKI_DIR / "index.html").write_text(
        build_index_page(concepts_sorted, longtail, n_sessions, n_edges_total),
        encoding="utf-8",
    )
    (WIKI_DIR / "graph.html").write_text(
        build_graph_page(concepts_sorted, graph_edges), encoding="utf-8"
    )

    # ---- report ----
    cluster_counts: dict = defaultdict(int)
    for c in page_concepts:
        cluster_counts[c.cluster] += 1
    print("=" * 64)
    print("Built Build 2026 LLM Wiki (purely additive; existing files untouched).")
    print(f"  concept pages       : {n_concepts}")
    print(f"  graph nodes         : {len(concepts_sorted)}")
    print(f"  graph edges (drawn) : {n_edges_graph}")
    print(f"  cross-concept edges : {n_edges_total}  (all co-occurrence pairs)")
    print(f"  sessions covered    : {n_sessions}")
    print(f"  long-tail topics    : {len(longtail)}  (single-session, no page)")
    print("  cluster breakdown   :")
    for cl in CLUSTER_ORDER:
        if cluster_counts.get(cl):
            print(f"      {cl:<32} {cluster_counts[cl]}")
    print("  outputs:")
    print(f"      wiki/index.html")
    print(f"      wiki/graph.html")
    print(f"      wiki/concepts/      ({n_concepts} pages)")
    print(f"      assets/wiki.css")
    print("=" * 64)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
