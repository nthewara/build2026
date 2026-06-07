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
