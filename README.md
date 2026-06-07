# Microsoft Build 2026 — Session Notes

A static HTML site summarizing Microsoft Build 2026 sessions, generated from markdown notes.

- **`index.html`** — landing page with session cards, stats, and live search.
- **`pages/`** — one HTML page per session (with prev/next navigation).
- **`markdown/`** — source session notes (markdown with YAML frontmatter).
- **`assets/style.css`** — shared stylesheet (no external CDNs).
- **`scripts/generate_site.py`** — idempotent site generator.

## Regenerate

```bash
python3 scripts/generate_site.py
```

Re-running clears `pages/` and rebuilds `index.html` + all session pages from `markdown/`.

## View

Open `index.html` in any browser — fully self-contained, no internet required.
