# ar5iv / ar5ivist pipeline cheat‑sheet

Goal: understand the closest public analogue to arXiv’s HTML pipeline and how to mirror its look in our LaTeXML builds.

## Repos of interest
- `dginev/ar5iv` — Rocket/Redis service that serves pre‑converted LaTeXML HTML for arXiv papers; conversion still LaTeXML. https://github.com/dginev/ar5iv
- `dginev/ar5iv-css` — CSS/theme used by ar5iv and imported by arXiv HTML pages. https://github.com/dginev/ar5iv-css
- `dginev/ar5ivist` — Turnkey CLI (Docker) that runs LaTeXML with ar5iv bindings + CSS; shows flags/commits ar5iv uses. https://github.com/dginev/ar5ivist
- `arXiv/zzzArchived_arxiv-readability` — archived Engrafo fork from the early arXiv HTML pilot. https://github.com/arXiv/zzzArchived_arxiv-readability

## What we now do by default (local pipeline)
- We run `scripts/build.sh` with the ar5ivist flag set (preloads, token/time limits) and vendored ar5iv bindings cloned to `assets/latexml/ar5iv-bindings` (commit 847b4835…).
- HTML DOM is postprocessed to match arXiv: `<nav class="ltx_page_navbar"><nav class="ltx_TOC active">…</nav></nav><div class="ltx_page_main">…</div>`.
- CSS is the vendored arXiv/ar5iv bundle (`assets/html/css/*`) copied into the output; no CDN dependency.
- PDF builds are unchanged; no feedback/overlay JS is loaded.
- LaTeXML remains the system 0.8.8 for now (not pinned to the ar5ivist commit).

## ar5ivist (what arXiv-like conversion looks like)
- Docker image: `latexml/ar5ivist:2509.16`.
- Entry point (from `ar5ivist/Dockerfile`):
  - `latexmlc --preload=[nobibtex,rawstyles,nobreakuntex,magnify=1.3,zoomout=1.3,tokenlimit=249999999,iflimit=3999999,absorblimit=1299999,pushbacklimit=599999]latexml.sty`
  - `--preload=ar5iv.sty`
  - `--path=/opt/ar5iv-bindings/bindings --path=/opt/ar5iv-bindings/supported_originals`
  - `--format=html5 --pmml --mathtex --timeout=2700`
  - `--noinvisibletimes --nodefaultresources`
  - `--css=https://cdn.jsdelivr.net/gh/dginev/ar5iv-css@0.8.4/css/ar5iv.min.css`
  - `--css=https://cdn.jsdelivr.net/gh/dginev/ar5iv-css@0.8.4/css/ar5iv-fonts.min.css`
- Base image pins:
  - LaTeXML commit `25ec2b0e9070cc05cbb5e5e22bebf5ba98a0d86c`.
  - ar5iv-bindings commit `847b4835448d17065d612c04b52c4a373ec0fd15`.
  - Ubuntu 24.04 with full texlive.

## How to approximate locally (what we now do)
- Keep using `latexmlc` for conversion.
- Postprocess HTML to load the arXiv/​ar5iv CSS bundle (`arxiv-html-papers-20250916.css`, which imports `ar5iv.0.8.4.css` and a small theme file).
- Wrap the TOC in a `ltx_page_navbar` container to get the left-rail layout.
- Opt-out via `USE_HTML_SKIN=0` if pure LaTeXML output is desired.

### Quick contrast: us vs. ar5iv/arXiv
- **We do (default in scripts/build.sh):** plain `latexmlc` + post-injected ar5iv/​arXiv CSS + TOC-left wrapper; no special LaTeXML preloads, timeouts, or binding paths.
- **ar5ivist does:** `latexmlc` with ar5iv-specific preloads (`latexml.sty` options, `ar5iv.sty`), custom binding paths, high token/time limits, and remote CSS from ar5iv-css CDN.
- **arXiv production likely does:** LaTeXML 0.8.x with proprietary static assets/JS; not publicly published. Presentation layer matches ar5iv-css + arXiv theme we vendor here.

## How to reproduce ar5ivist exactly (if needed)
```bash
docker run -v \"$PWD\":/docdir -w /docdir --user \"$(id -u):$(id -g)\" \
  latexml/ar5ivist:2509.16 --source=main.tex --destination=html/main.html
```
Notes: Docker is confined to the working dir; no `../` paths. Logs land in `main.latexml.log`.

## What’s still private
- arXiv’s production converter container is not published; only static assets (CSS/JS) are public. The approach above matches presentation and LaTeXML version/flags closely without depending on private images.
