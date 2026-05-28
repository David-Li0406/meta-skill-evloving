---
name: sphinx-docs
description: Write and maintain Sphinx documentation and reStructuredText files, including configuring Sphinx (conf.py, extensions, toctrees) and updating CI/deployment workflows so documentation builds as part of deployment or release pipelines.
---

# Sphinx Documentation

## Workflow

- Inspect existing docs layout (docs/, conf.py, index.rst) and follow established patterns.
- Prefer incremental changes: update relevant .rst files and toctrees; avoid restructuring unless requested.
- Build docs locally or in CI using `sphinx-build -b html docs/ docs/_build/html` and fix warnings that indicate broken references or missing targets.

## Authoring Guidelines

- Use reStructuredText, keep headings consistent, and ensure each file is reachable from a toctree.
- Add `:ref:` targets for cross-references and keep labels unique.
- For API docs, use `autodoc` and `napoleon` (if enabled) and keep docstrings concise but complete.
- Prefer short, task-focused sections with examples; avoid large unbroken blocks.
- When introducing new pages, add them to the nearest index or section toctree.

## Non-Python Code

- Autodoc does not process Bash or other non-Python sources; document these with `literalinclude` or language-specific domains (e.g., `sphinxcontrib-bashdomain`) instead of relying on comments alone.
- When documenting shell scripts, add a dedicated RST page that lists functions, arguments, and usage with short examples.
- Treat inline comments as implementation notes; keep canonical API docs in Sphinx pages so they build deterministically.

## Build/Deploy Integration

- Locate deployment or release workflows in `.github/workflows/` and confirm where build artifacts are assembled.
- Add a docs build step that runs after dependencies are installed but before deployment/publish steps.
- Ensure docs dependencies are installed (e.g., `pip install -r docs/requirements.txt` or `pip install .[docs]`).
- Fail the pipeline on docs build errors to prevent deploying broken documentation.
- If docs are deployed separately, add an explicit job that depends on the main build and publishes the HTML output from `docs/_build/html`.

## Quality Checks

- Fix warnings for missing references, duplicate labels, or broken toctree entries.
- Keep the docs build deterministic by pinning versions in docs requirements when needed.
