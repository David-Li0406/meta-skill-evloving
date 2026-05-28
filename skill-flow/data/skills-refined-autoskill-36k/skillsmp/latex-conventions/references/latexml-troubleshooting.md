# LaTeXML / latexmlc Troubleshooting Links (quick reference)

Curated links for diagnosing LaTeXML/latexmlc build issues, HTML output problems, and environment choices. Keep this link-heavy; minimal prose.

## Core resources
- Official repo (issues, releases, bindings): https://github.com/brucemiller/LaTeXML
- Official manual (0.8.8, Feb 26 2024): https://math.nist.gov/~BMiller/LaTeXML/manual/
- Release notes 0.8.8 (breaking changes, MathML tweaks): https://newreleases.io/project/github/brucemiller/LaTeXML/release/v0.8.8
- Contacts/support page (mailing list, issue tracker): https://math.nist.gov/~BMiller/LaTeXML/contact.html

## Docker images / environments
- kjarosh/latex-docker (Alpine TL2025 variants; easy `docker cp` for fresh latexml/tex binaries): https://github.com/kjarosh/latex-docker
- xu-cheng/latex-docker (TL latest + historic tags on Debian/Alpine): https://github.com/xu-cheng/latex-docker
- dante-ev/docker-texlive (full TL images with extras): https://github.com/dante-ev/docker-texlive
- maxkratz/docker_texlive (versioned TL 2016–2025 images): https://github.com/maxkratz/docker_texlive
- arXiv compiler/converter image (archived 2025-01-28; ECR-gated but documents layout): https://github.com/arXiv/arxiv-compiler

## HTML rendering stacks using LaTeXML
- arXiv Vanity / Engrafo Docker image (LaTeXML-based HTML renderer): https://github.com/arxiv-vanity/engrafo
- arXiv Vanity runner (uses engrafo image via docker-compose): https://github.com/arxiv-vanity/arxiv-vanity

## Common failure points & quick checks
- Class binding missing (e.g., `memoir`): verify binding list in manual’s Appendix B; consider `\iflatexml` class switch to `article` or ship a custom binding.
- Package not recognized: check for existing binding; if absent, add `--preload=<package>.ltxml` or create minimal binding in `local/`.
- Bibliography style unsupported: switch to `plain`/`alpha` for latexml, or pre-generate `.bbl` and call `latexmlc --bibtex --preload=... main.tex`.
- Stalls in post-processing: rerun with `--loglevel=info --debug`; add `--noparse` to isolate digestion vs postprocessing issues.
- Math layout regressions after 0.8.8: note `ltx:inline-para` renamed to `ltx:inline-logical-block` (see release notes above).

## Minimal reproduction templates
- Run inside fresh TL+LaTeXML container:
  ```bash
  docker run --rm -v "$PWD":/src -w /src kjarosh/latex:2025.1 latexmlc --destination=out.html main.tex
  ```
- If class binding missing, stub for HTML runs:
  ```tex
  \ifdefined\latexml
    \documentclass{article}
  \else
    \documentclass{memoir}
  \fi
  ```

## When to upgrade
- If latexmlc errors mention outdated LaTeX kernel: use a TL 2024+ image (above) or build LaTeXML from master; 0.8.8 release date 2024-02-29.
- For arXiv parity: target TL2023+; arXiv’s current toolchain is 2023-era according to their FAQ (see arXiv links above).
