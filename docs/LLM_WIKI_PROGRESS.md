# LLM Wiki — Build & Progress Tracker

**Task:** Add a Karpathy-style **LLM Wiki** section to the Build 2026 static site, derived **only** from content already published at <https://nthewara.github.io/build2026/>. Additive — keep all existing content. New `wiki/` folder. Interconnected wiki links + an interactive visual graph. Link from the main landing page.

**Repo:** <https://github.com/nthewara/build2026> · **Live:** <https://nthewara.github.io/build2026/>
**Local:** `/Users/nthewara88agent/repos/main/build2026`
**Owner identity for commits:** `nthewara <nthewara@gmail.com>`
**Started:** 2026-06-07 (Australia/Perth, GMT+8)

---

## Concept (what we're building)

Andrej Karpathy's "LLM wiki" pattern: compile a corpus into a persistent, densely cross-linked knowledge base — concepts become nodes (each its own page), links express relationships, and a graph view shows the structure. Traverse by following links, not linear reading.
- Reference gist: <https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f>

**HARD RULE:** Only use content already in this repo (the 127 Build 2026 session notes + their pages). No new facts, no web search, no invention. This is a re-organization/synthesis of existing published content. We may *name/reference* the LLM-wiki concept and link the gist, but pull no new content from it.

## Data model (all derived from existing frontmatter)

- **Concepts** = `topic/<x>` frontmatter tags across the 127 sessions.
  - Topic on **≥2 sessions** → dedicated concept page (~90 expected).
  - Topic on exactly 1 session → folded into a "Long tail / emerging topics" section (no standalone page).
- **Concept → Session** edges = a session carries that topic tag (links to `pages/<code>.html`).
- **Concept → Concept** edges = two topics co-occur on the same session; **weight = # shared sessions**. (Genuinely derived; not fabricated.)

## Target structure (additive)

```
wiki/
  index.html            # wiki home: concept catalog grouped by cluster + stats + graph link
  concepts/<slug>.html  # one page per ≥2-session concept (sessions + related concepts)
  graph.html            # interactive force-directed graph (vanilla JS, no CDN)
assets/wiki.css         # NEW stylesheet (do NOT modify style.css)
scripts/generate_wiki.py# NEW idempotent generator
```
Plus: add a **link from `index.html`** to the wiki (separate, additive edit).

## Hard constraints

- ❌ Do NOT modify/delete: `markdown/*`, `pages/*`, `index.html`, `assets/style.css`.
- ✅ Only NEW files: `wiki/*`, `assets/wiki.css`, `scripts/generate_wiki.py` (+ the one additive nav link added to `index.html` by the parent at the end).
- ✅ No external CDNs/JS; offline-first (works from `file://` + GitHub Pages).
- ✅ All internal links must resolve.
- ✅ Commits use `nthewara <nthewara@gmail.com>`.

---

## Progress log

| # | Step | Status | Notes |
|---|------|--------|-------|
| 1 | Confirm LLM-wiki concept + analyze concept space (topic tags) from existing repo | ✅ Done | ~90 topics on ≥2 sessions; long tail of 1-session topics. Hubs: ai(91), agents(58), azure(25), dotnet(16), foundry(12), github-copilot(11). |
| 2 | Write `LLM_WIKI_PROGRESS.md` tracker | ✅ Done | This file. |
| 3 | Build `wiki/` via subagent (generator + concept pages + graph + wiki.css) | ✅ Done | 91 concept pages, 91-node graph, 364 drawn edges (407 total co-occurrence), 127 sessions, 152 long-tail topics. Clusters: AI&Agents 19, Data 14, Platforms 13, DevTools 12, Observability 12, Azure 9, Security 5, Other 5, Community 2. |
| 4 | Add link from main `index.html` → wiki (additive, no deletions) | ✅ Done | Added hero CTA: "Explore the LLM Wiki →" + "Concept graph" buttons + blurb. Patched BOTH rendered `index.html` AND `scripts/generate_site.py` hero template so it survives regeneration. |
| 5 | Verify: pages render, wikilinks interconnect, graph works, **existing content intact** (`git status` shows only new files) | ✅ Done | Independent checks: 1838 hrefs, **0 broken_file + 0 broken_anchor** (incl. cluster `#` anchors); all 91 graph node targets resolve; 0 out-of-range edges; only external href = Karpathy gist; no CDN refs. `git status`: only new `wiki/`, `assets/wiki.css`, `scripts/generate_wiki.py` + intentional `index.html`/`generate_site.py` edits. |
| 6 | Commit + push as `nthewara`; verify live on GitHub Pages | ✅ Done | Commit `da41f5e` as `nthewara <nthewara@gmail.com>`. Live: wiki home, graph, concept pages, wiki.css all HTTP 200; landing hero CTA links live. |

**✅ ALL STEPS COMPLETE — LLM Wiki shipped and live.**

**Legend:** ✅ done · 🔄 in progress · ⬜ pending · ⚠️ blocked

## Lessons / gotchas

- ⚠️ `sessions_spawn` with `thinking: "medium"` **fails instantly** for `github-copilot/claude-opus-4.8` (`Use one of: off`). Omit the thinking override for Opus subagents.
- Site convention: **no external CDNs** — graph must be hand-rolled vanilla JS.
- GitHub Pages CDN takes ~1–3 min to propagate after push; verify with cache-busting/polling.

## Verification checklist (before marking complete)

- [ ] `wiki/index.html`, `wiki/graph.html`, and ~90 `wiki/concepts/*.html` exist.
- [ ] `git status --porcelain` shows **no** `M`/`D` on `markdown/*`, `pages/*`, `index.html`, `assets/style.css`.
- [ ] All concept→session links (`../../pages/<code>.html`) resolve.
- [ ] All concept→concept links (`../concepts/<slug>.html`) resolve.
- [ ] Graph node-click targets all map to real concept pages.
- [ ] No external `<script src>`/`<link href>` CDN refs anywhere in `wiki/`.
- [ ] Main `index.html` has a working link to `wiki/index.html` (and existing content untouched).
- [ ] Live on GitHub Pages: wiki home, a concept page, and graph all serve HTTP 200.

## Next sync hook

This is also the same site that gets **incremental session syncs**. When the wiki is regenerated after new sessions land, re-run `scripts/generate_wiki.py` (and `scripts/generate_site.py` for the session pages) and push.

---

## Incremental Sync — 2026-06-07

**5 final sessions added** (the closing batch — 4 keynote segments + the opening keynote), taking the corpus from **127 → 132 sessions**. Source notes were dropped into `markdown/` and the site + wiki were regenerated purely via the two generator scripts. No content outside the Build 2026 set was introduced.

### New notes (in `markdown/`, rendered to `pages/`)

| File | Page | One-liner |
|------|------|-----------|
| `SEG01 - Frontier Tuning.md` | `pages/SEG01.html` | **Frontier Tuning** — enterprise AI via RL fine-tuning of model + harness on your own data/workflows; `M AI Thinking 1` in Foundry Model Catalog private preview; dataset → grader → submit flow + low-level training API sneak peek. |
| `SEG02 - MDASH.md` | `pages/SEG02.html` | **MDASH** — Microsoft's multi-agent code-security harness (Multi-agent Dynamic Application Security Harness). |
| `SEG03 - Microsoft Discovery.md` | `pages/SEG03.html` | **Microsoft Discovery** — agentic scientific-discovery platform segment. |
| `SEG04 - GitHub App and Rayfin.md` | `pages/SEG04.html` | **GitHub App + Rayfin** — segment; in-repo Related link to `BRK225` (Rayfin data apps & agents) resolves correctly. |
| `KEY01 - Satya Nadella Opening Keynote.md` | `pages/KEY01.html` | **Satya Nadella Opening Keynote** — the marquee note: ~10.5k words, 44 announcements, 91.5 KB rendered. Adds many topic tags (incl. a new **quantum** concept). |

### New totals after regen

- **Sessions:** **132** (`pages/*.html` count = 132; `wiki/index.html` shows `132`). Total runtime 66h 41m.
- **Wiki concept pages:** **92** (was 91 — KEY01 introduced a new `quantum` concept page; all other deltas were existing concepts gaining sessions).
- **Graph:** **92 nodes**, **373 drawn edges** (424 total co-occurrence pairs). (was 91 / 364 / 407.)
- **Long-tail topics:** 153 single-session topics (no page).
- Concept counts ticked up as expected — the wiki is derived from `topic`/frontmatter tags, and KEY01 is tag-rich, so several hub concepts (ai, agents, azure, copilot, fabric, foundry, github, security, windows) gained sessions.

**Exact script output captured:**
- `generate_site.py` → `Built site for 132 sessions.` · `pages/ -> 132 HTML files` · `total runtime -> 66h 41m (4001 min)` · all frontmatter complete.
- `generate_wiki.py` → `concept pages: 92` · `graph nodes: 92` · `graph edges (drawn): 373` · `cross-concept edges: 424` · `sessions covered: 132` · `long-tail topics: 153`. Cluster breakdown: AI&Agents 19, Data&Databases 14, Platforms&Devices 14, DevTools&Languages 12, Observability&Ops 12, Azure&Infra 9, Security&Governance 5, Other 5, Community&Career 2.

### Scope integrity — respected ✅

- **No out-of-Build2026 files or links introduced.** `git status --porcelain` shows **no `M`/`D` on any `markdown/*`**; the 5 new notes are untracked additions only. No hand-edits to `markdown/*`, `pages/*`, `index.html`, `assets/style.css`, or wiki HTML — all generated content was rebuilt by the scripts.
- **`assets/style.css` NOT modified** (verified — scripts left it untouched; would have been a red flag otherwise).
- **Vault-only link `[[2026 Build Session List]]`** present in the 5 notes' `## 🔗 Related` sections was **auto-stripped** by the generator's `strip_unresolved_wikilinks` — it does **not** appear in any of the 5 generated pages, and **no literal `[[` survives** in `pages/SEG0*.html` / `pages/KEY01.html`.
- **SEG04's in-repo link `[[BRK225 …]]`** correctly resolved to `<a class="wikilink wikilink--resolved" href="BRK225.html">` (target `pages/BRK225.html` exists).
- **Link integrity:** full scan of `pages/` + `wiki/` = **3094 navigational hrefs, 0 broken in-repo links** (in-page anchors, prev/next pager, concept↔session, concept↔concept all resolve). External links = 147, all legitimate (132 YouTube per-session videos, 5 GitHub repos, MS Learn/devblogs/NVIDIA/OpenTelemetry docs, and the single Karpathy gist in the wiki). The 226 "broken" hits in a naive first pass were inline `data:image/svg+xml` favicon URIs, not links.
- Prev/next pager verified on all 5 new pages; SEG04 is last alphabetically so its `next` is intentionally empty.

### Changed files (all in-scope)

- New: `markdown/{SEG01,SEG02,SEG03,SEG04,KEY01}` + `pages/{SEG01,SEG02,SEG03,SEG04,KEY01}.html` + `wiki/concepts/quantum.html`.
- Modified (by scripts): `index.html`; `pages/{DEMSP395,OD800,ODSP940}.html` (neighbour prev/next re-stitch); `wiki/index.html`, `wiki/graph.html`, and 9 `wiki/concepts/*.html` (ai, agents, azure, copilot, fabric, foundry, github, security, windows) for updated session lists/counts.
- Hand-edited: this `docs/LLM_WIKI_PROGRESS.md` only.

**Commit:** `Add 5 final sessions (SEG01-04 segments + KEY01 keynote); regen site + wiki to 132 sessions` as `nthewara <nthewara@gmail.com>`.
