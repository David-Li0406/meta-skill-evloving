# Documentation Site Architecture

Technical reference for our MkDocs-based documentation sites. Covers tech stack, structure, deployment, and configuration patterns.

## The Four Sites

| Site | Repository | Purpose |
|------|------------|---------|
| **bedbase** | `databio/bedbase` | Genomic interval tools and BED file platform |
| **pepspec** | `pepkit/pepspec` | PEP toolkit and related tools |
| **refgenie-docs** | `refgenie/refgenie-docs` | Reference genome management system |
| **refget** | `ga4gh/refget` | GA4GH Refget specifications |

All four sites follow identical patterns for framework, structure, and deployment.

---

## Tech Stack

**Core:**
- **Framework:** MkDocs
- **Theme:** Material for MkDocs
- **Python:** 3.11+
- **Hosting:** GitHub Pages (gh-pages branch) (or sometimes Cloudflare workers)

**Standard Plugins:**
```yaml
plugins:
  - search
  - mkdocstrings[python]    # Auto-generate Python API docs
  - mkdocs-jupyter          # Render Jupyter notebooks as pages
```

**Standard Markdown Extensions:**
```yaml
markdown_extensions:
  - admonition              # Callout boxes (note, warning, tip)
  - attr_list               # HTML attributes on elements
  - md_in_html              # Mix markdown with HTML
  - pymdownx.details        # Collapsible sections
  - pymdownx.highlight      # Code syntax highlighting
  - pymdownx.superfences    # Fenced code blocks + mermaid diagrams
  - pymdownx.tabbed         # Tabbed content sections
```

## Future Tech Stack

We intend to migrate from mkdocs/material-for-mkdocs to zensicle, from mkdocstrings to the equivalent version in zensicle, when it is released and mature, likely toward the end of 2025.

## Directory Structure

```
repo-root/
├── mkdocs.yml                 # Main config + navigation
├── requirements-docs.txt      # Python dependencies
├── .github/
│   └── workflows/
│       └── publish.yaml       # GitHub Actions deployment
├── docs/
│   ├── [tool1]/               # Major tool/topic section
│   │   ├── README.md          # Section landing page
│   │   ├── tutorials/         # Getting started guides
│   │   ├── how-to/            # Task-oriented guides
│   │   ├── code/              # Generated API docs
│   │   ├── notebooks/         # Jupyter notebooks
│   │   ├── img/               # Section-specific images
│   │   └── changelog.md       # Version history
│   ├── [tool2]/
│   ├── stylesheets/
│   │   └── extra.css          # Theme color overrides
│   └── img/                   # Shared images, logos
├── overrides/                 # Template customizations
│   ├── main.html              # Base template override
│   ├── home.html              # Custom hero landing page
│   └── partials/
│       └── footer.html        # Custom footer
└── autodoc.py                 # Build script (pepspec only)
```

**Key conventions:**
- Each major tool/project gets its own folder under `docs/`
- `README.md` in each folder serves as the section landing page
- Images live in `img/` subdirectories (global or section-specific)
- Notebooks stored as `.ipynb`, rendered as pages during build

---

## Configuration (mkdocs.yml)

### Minimal Template

```yaml
site_name: "Project Name"
site_url: https://example.org/

theme:
  name: material
  custom_dir: overrides
  logo: img/logo.svg
  favicon: img/favicon.svg
  features:
    - header.autohide
    - navigation.sections
    - navigation.footer
    - navigation.indexes
    - navigation.tabs
    - navigation.top
    - toc.follow
    - content.action.edit
    - content.action.view

extra_css:
  - stylesheets/extra.css

extra:
  generator: false

copyright: >
  <a href="http://databio.org/">
    <img src="https://databio.org/images/logo_databio_long.svg"
         style="height:60px;" alt="Databio logo">
  </a>

plugins:
  - search
  - mkdocstrings:
      default_handler: python
      handlers:
        python:
          options:
            docstring_style: google
            show_source: true
  - mkdocs-jupyter:
      include:
        - "*/notebooks/*.ipynb"

markdown_extensions:
  - admonition
  - attr_list
  - md_in_html
  - pymdownx.details
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true

nav:
  - Home: index.md
  - Tool Name:
    - Getting started:
      - Introduction: tool/README.md
      - Hello World: tool/tutorials/hello-world.md
    - How-to guides:
      - How to do X: tool/how-to/do-x.md
    - Reference:
      - API: tool/code/api.md
      - CLI: tool/code/cli.md
    - Changelog: tool/changelog.md
```

### Navigation Pattern

Follow the four documentation types in nav structure:

```yaml
nav:
  - Tool Name:
    - Getting started:        # Tutorials
      - Introduction
      - Hello World
    - How-to guides:          # How-to
      - How to validate
      - How to extend
    - Reference:              # Reference
      - Specification
      - Python API
      - CLI
    - Rationale: rationale.md # Explanation (if applicable)
```

---

## Deployment

All sites deploy via GitHub Actions on push to `master`.

### GitHub Actions Workflow

**File:** `.github/workflows/publish.yaml`

```yaml
name: Publish docs

on:
  push:
    branches:
      - master

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Configure Git Credentials
        run: |
          git config user.name github-actions[bot]
          git config user.email github-actions[bot]@users.noreply.github.com

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Cache MkDocs Material
        uses: actions/cache@v4
        with:
          key: mkdocs-material-${{ github.ref }}
          path: .cache
          restore-keys: mkdocs-material-

      - name: Install dependencies
        run: pip install -r requirements-docs.txt

      - name: Deploy
        run: mkdocs gh-deploy --force
```

**How it works:**
1. Push to `master` triggers the workflow
2. Installs Python dependencies from `requirements-docs.txt`
3. Runs `mkdocs gh-deploy --force`
4. MkDocs builds site and pushes to `gh-pages` branch
5. GitHub Pages serves from `gh-pages`

**No manual deployment needed** - every merge to master auto-deploys.

---

## Theme Customization

### Color Overrides (extra.css)

```css
:root {
  --md-primary-fg-color: #2c89a0;
  --md-primary-fg-color--light: #3a9db5;
  --md-primary-fg-color--dark: #1f6070;
  --md-typeset-a-color: #2c89a0;
}
```

Each site has its own primary color. Common palette:
- bedbase: `#2c89a0` (teal)
- pepspec: `#354a75` (dark blue)
- refgenie: `#354aa5` (blue)

### Custom Templates (overrides/)

**Custom landing page (home.html):**
```html
{% extends "main.html" %}
{% block content %}
<div class="hero">
  <h1>Project Name</h1>
  <p>Tagline goes here</p>
  <a href="getting-started/" class="md-button">Get Started</a>
</div>
{{ super() }}
{% endblock %}
```

**Custom footer (partials/footer.html):**
```html
{% extends "base.html" %}
{% block footer %}
<footer>
  <a href="https://databio.org">
    <img src="/img/databio-logo.svg" alt="Databio">
  </a>
</footer>
{% endblock %}
```

---

## Content Patterns

### Section README.md

Each `docs/[tool]/README.md` serves as the landing page:

```markdown
# Tool Name

<img src="img/logo.svg" alt="Logo" style="float:right; width:150px">

Brief description of what this tool does.

## Overview

- **Component 1:** Description
- **Component 2:** Description

## Quick Links

- [Getting Started](tutorials/hello-world.md)
- [API Reference](code/api.md)
- [GitHub Repository](https://github.com/org/repo)
```

### Auto-Generated API Docs

Use mkdocstrings to generate from docstrings:

```markdown
# Python API

::: mypackage.module
    options:
      show_source: true
      members:
        - ClassName
        - function_name
```

### Jupyter Notebooks

Store in `docs/[tool]/notebooks/`, configure in mkdocs.yml:

```yaml
plugins:
  - mkdocs-jupyter:
      include:
        - "bedbase/notebooks/*.ipynb"
        - "peppy/notebooks/*.ipynb"
```

Reference in nav like regular pages:

```yaml
nav:
  - Tutorials:
    - Basic Usage: tool/notebooks/basic-usage.ipynb
```

---

## Dependencies (requirements-docs.txt)

**Minimal:**
```
mkdocs-material
mkdocstrings[python]
```

**With notebooks:**
```
mkdocs-material
mkdocstrings[python]
mkdocs-jupyter
```

**With package API docs:**
```
mkdocs-material
mkdocstrings[python]
mkdocs-jupyter
mypackage  # The package being documented
```

---

## Adding a New Documentation Site

1. **Create repo structure:**
   ```bash
   mkdir -p docs/img docs/stylesheets .github/workflows overrides
   ```

2. **Copy template files:**
   - `mkdocs.yml` from existing site
   - `requirements-docs.txt`
   - `.github/workflows/publish.yaml`
   - `docs/stylesheets/extra.css`

3. **Customize mkdocs.yml:**
   - Set `site_name` and `site_url`
   - Update logo paths
   - Define nav structure
   - Configure plugins for your content types

4. **Add content:**
   - Create `docs/index.md` or `docs/[tool]/README.md`
   - Follow the directory conventions

5. **Enable GitHub Pages:**
   - Repository Settings → Pages → Source: `gh-pages` branch

6. **Push to master** - deployment is automatic

---

## Checklist for New Sites

- [ ] `mkdocs.yml` configured with site name, theme, plugins
- [ ] `requirements-docs.txt` with all dependencies
- [ ] `.github/workflows/publish.yaml` for deployment
- [ ] `docs/stylesheets/extra.css` with brand colors
- [ ] `docs/img/` with logo.svg and favicon.svg
- [ ] At least one content page (index.md or README.md)
- [ ] GitHub Pages enabled on gh-pages branch
- [ ] Nav structure follows Getting Started → How-to → Reference pattern
