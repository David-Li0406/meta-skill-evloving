---
name: project-onboarding
description: Comprehensive initialization for new projects. Sets up directory hierarchy, safety hooks, documentation engines, and legal/standards boilerplate.
---

# Project Onboarding Protocol

## 1. Directory Structure
Create the following standard hierarchy:
- `src/`: Source code root.
- `scripts/`: Local automation and management scripts.
- `docs/en/product/`: Feature and requirement documentation.
- `docs/en/legal/`: Compliance and legal records.
- `docs/architecture/adr/`: Architectural Decision Records.

## 2. Configuration & Boilerplate Injection
- **README**: Create a `README.md` using the project name from $ARGUMENTS.
- **Gitignore**: Copy `templates/.gitignore.tmpl` to `.gitignore`.
- **Changelog**: Copy `templates/CHANGELOG.md.tmpl` to `CHANGELOG.md`.
- **Automation**: Copy the global `doc_manager.py` from the skill library to `scripts/doc_manager.py`.

## 3. Git & Safety Hooks
- **Initialize**: If the directory is not a git repo, run `git init`.
- **Local Hook**: Copy `templates/pre-commit.tmpl` to `.git/hooks/pre-commit`.
- **Permissions**: You **MUST** run `chmod +x .git/hooks/pre-commit`. 
- *Note: While the Global Hook handles laptop-wide safety, this local hook ensures project-specific scripts like `doc_manager.py` run even if the global hook is disabled.*

## 4. Documentation Initialization
- **Manifest**: Execute `python3 scripts/doc_manager.py` to generate the initial `docs_manifest.json`.
- **Index**: Ensure `docs/README.md` is generated as the Table of Contents.

## Definition of Done
- Standard folders exist.
- Git is initialized and local hook is executable.
- `CHANGELOG.md` and `README.md` are present.
- `docs_manifest.json` and `docs/README.md` reflect the initial state.
