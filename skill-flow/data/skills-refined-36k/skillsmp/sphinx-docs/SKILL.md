---
name: sphinx-docs
description: Generates documentation using Sphinx and reStructuredText. Supports API docs, user guides, and architecture documentation. Use when creating project documentation, API references, or technical guides.
---

# Sphinx Documentation

## Quick Setup

```bash
mkdir docs && cd docs
sphinx-quickstart --no-sep --project "My Project" --author "Team"
```

## Project Structure

```
docs/
├── conf.py           # Configuration
├── index.rst         # Root document
├── requirements.txt  # Doc dependencies
├── Makefile
├── api/              # API reference
├── guides/           # User guides
└── architecture/     # Architecture docs
```

## conf.py (Essential)

```python
project = 'My Project'
extensions = [
    'sphinx.ext.autodoc',       # Auto-generate from docstrings
    'sphinx.ext.napoleon',      # Google/NumPy style docstrings
    'sphinx.ext.viewcode',      # Source links
    'sphinx_copybutton',        # Copy button for code
    'myst_parser',              # Markdown support
]

source_suffix = {'.rst': 'restructuredtext', '.md': 'markdown'}
html_theme = 'sphinx_rtd_theme'
```

## requirements.txt

```
sphinx>=7.0
sphinx-rtd-theme>=2.0
sphinx-copybutton>=0.5
myst-parser>=2.0
```

## RST Basics

### Document Structure
```rst
Page Title
==========

Section
-------

Subsection
^^^^^^^^^^

Paragraph text with **bold** and *italic*.

.. note::
   A note callout.

.. warning::
   A warning callout.
```

### Links and References
```rst
External: `Link text <https://example.com>`_
Internal: :doc:`other-page`
Reference: :ref:`label-name`
```

### Code Blocks
```rst
.. code-block:: python

   def hello():
       print("Hello")

.. code-block:: bash

   npm install
```

### Tables
```rst
.. list-table::
   :header-rows: 1

   * - Header 1
     - Header 2
   * - Cell 1
     - Cell 2
```

### Toctree
```rst
.. toctree::
   :maxdepth: 2
   :caption: Contents

   guides/getting-started
   guides/configuration
   api/index
```

## index.rst Template

```rst
Welcome to My Project
=====================

.. toctree::
   :maxdepth: 2
   :caption: Guides

   guides/getting-started
   guides/configuration

.. toctree::
   :maxdepth: 2
   :caption: Reference

   api/index

.. toctree::
   :maxdepth: 1

   changelog
```

## API Documentation

```rst
API Reference
=============

.. automodule:: mypackage
   :members:
   :undoc-members:

.. autoclass:: mypackage.Client
   :members:
   :special-members: __init__
```

## CLI Documentation

```rst
Command Reference
=================

.. option:: -c, --config <path>

   Configuration file path.

.. option:: -v, --verbose

   Enable verbose output.

Example::

   myapp --config config.yaml serve
```

## Build Commands

```bash
# Build HTML
make html

# Watch mode (auto-rebuild)
sphinx-autobuild . _build/html

# Check links
make linkcheck

# Clean
make clean
```

## Hosting

### GitHub Pages
```yaml
# .github/workflows/docs.yml
name: Docs
on:
  push:
    branches: [main]
    paths: [docs/**]

permissions:
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r docs/requirements.txt
      - run: make -C docs html
      - uses: actions/upload-pages-artifact@v3
        with:
          path: docs/_build/html

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/deploy-pages@v4
        id: deployment
```

### Read the Docs
```yaml
# .readthedocs.yaml
version: 2
build:
  os: ubuntu-22.04
  tools:
    python: "3.11"
sphinx:
  configuration: docs/conf.py
python:
  install:
    - requirements: docs/requirements.txt
```

## Integration with Diagrams

Include PlantUML/Mermaid diagrams:

```rst
.. uml::

   @startuml
   Alice -> Bob: Hello
   @enduml

.. mermaid::

   flowchart LR
     A --> B
```

Requires: `sphinxcontrib-plantuml`, `sphinxcontrib-mermaid`
