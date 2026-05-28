---
name: doc
description: 'This skill should be used when the user asks to "generate documentation", "validate docs", "check doc coverage", "find missing docs", "create code-map", "sync documentation", "update docs", or needs guidance on documentation generation and validation for any repository type. Triggers: doc, documentation, code-map, doc coverage, validate docs.'
---

# Doc Skill

Universal documentation generation and validation for any project structure.

## Overview

Auto-detects project type (CODING, INFORMATIONAL, OPS), discovers documentable features, generates documentation, and validates coverage.

## Commands

| Command | Action |
|---------|--------|
| `discover` | Find undocumented features |
| `discover --create` | Generate stubs for undocumented |
| `gen [feature]` | Generate/update specific doc |
| `all` | Update all docs (CODING/OPS) or validate (INFORMATIONAL) |
| `sync` | Pull from canonical source |
| `coverage` | Validate docs match code |
| `coverage --create-issues` | Create tracking issues for gaps |
