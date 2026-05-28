---
name: architecture-health
description: Diagnoses project health, architecture risks, and technical debt. Use when starting a new session or analyzing the codebase structure.
---

# Architecture Health Skill

Follow this process to generate a "Project Health Diagnostic Report":

## 1. Structural Analysis

- **File Sizes**: Identify "God Class" files (>400 lines or mixed responsibilities).
- **Directory Structure**: Check if files are grouped by domain (e.g., `loaders/`, `processors/`).
- **Naming**: Ensure file names are specific (e.g., `pnm_adjacency.py` instead of `adjacency.py`).

## 2. Code Pattern Analysis

- **Dependencies**: grep for `import` statements to find circular or cross-layer violations (e.g., `core` importing `gui`).
- **Safety**: grep for `except:` (bare except) or `pass` blocks in error handling.
- **Performance**: Look for critical loops in Python that aren't vectorized.

## 3. Report Generation

Generate a Markdown table sorted by urgency (P0, P1, P2):

| Priority | Issue Type | Location | Recommendation |
| :--- | :--- | :--- | :--- |
| **P0** | Critical Safety | `disk_cache.py` | Replace bare `except:` with `OSError`. |
| **P1** | Refactoring | `pnm.py` | Split into `adjacency` and `throat` modules. |
| **P2** | Maintenance | `utils.py` | Add type hints. |

## 4. Action Plan

- Propose specific refactoring steps (Extract Method, Split File, Rename).
- Verify changes with imports and tests.
