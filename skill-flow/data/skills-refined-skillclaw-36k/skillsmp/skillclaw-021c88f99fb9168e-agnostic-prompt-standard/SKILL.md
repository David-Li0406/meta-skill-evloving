---
name: agnostic-prompt-standard
description: Use this skill when you need to generate, compile, and lint prompts that conform to the Agnostic Prompt Standard (APS) v1.0.
---

# Agnostic Prompt Standard (APS) v1.0 — Skill Entry

This `SKILL.md` is the **entrypoint** for the Agnostic Prompt Standard (APS) v1.0.

- The APS **normative spec** is in `references/` (those documents define the standard).
- Everything else in this repository is **supporting material** (examples, templates, platform adapters).

## Normative spec (APS v1.0)

1. [00 Structure](references/00-structure.md)
2. [01 Vocabulary](references/01-vocabulary.md)
3. [02 Linting and formatting](references/02-linting-and-formatting.md)
4. [03 Agentic control](references/03-agentic-control.md)
5. [04 Schemas and types](references/04-schemas-and-types.md)
6. [05 Grammar](references/05-grammar.md)
7. [06 Logging and privacy](references/06-logging-and-privacy.md)
8. [07 Error taxonomy](references/07-error-taxonomy.md)

## Skill layout

- `SKILL.md` — this file (skill entrypoint).
- `references/` — the APS v1.0 normative documents (this is what an LSP/linter should ingest).
- `assets/` — reusable examples for `<format>` and `<constants>` blocks.
  - `constants/` — example constants blocks.
    - `constants-json-block-v1.0.0.example.md`
    - `constants-text-block-v1.0.0.example.md`
  - `formats/` — example format blocks.
    - `format-code-changes-full-v1.0.0.example.md`
    - `format-code-map-v1.0.0.example.md`
    - `format-error-v1.0.0.example.md`
    - `format-hierarchical-outline-v1.0.0.example.md`
    - `format-ideation-list-v1.0.0.example.md`
    - `format-markdown-table-v1.0.0.example.md`
    - `format-table-api-coverage-v1.0.0.example.md`
- `platforms/` — **non-normative** platform adapters (file conventions, frontmatter, tool registries, templates).
  - `README.md` — platforms overview and contract.
  - `_schemas/` — JSON Schemas for adapter validation.
    - `platform-manifest.schema.json`
    - `tools-registry.schema.json`
  - `_template/` — skeleton for new platform adapters.
    - `README.md`, `manifest.json`, `tools-registry.json`
  - `vscode-copilot/` — VS Code + GitHub Copilot adapter.
    - `README.md` — adapter quickstart and nuances.
    - `manifest.json` — file discovery rules.