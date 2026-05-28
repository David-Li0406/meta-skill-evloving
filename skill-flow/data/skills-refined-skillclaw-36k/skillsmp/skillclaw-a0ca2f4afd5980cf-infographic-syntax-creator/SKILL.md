---
name: infographic-syntax-creator
description: Use this skill when you need to generate AntV Infographic syntax outputs from user content, including template selection, data structuring, and theme application.
---

# Infographic Syntax Creator

## Overview

Generate AntV Infographic syntax output from user content, following the rules in `references/prompt.md`.

## Workflow

1. Read `references/prompt.md` for syntax rules, templates, and output constraints.
2. Extract the user's key structure: title, description, items, hierarchy, and metrics; infer any missing pieces if needed.
3. Select a template that matches the structure (sequence/list/compare/hierarchy/chart).
4. Compose the syntax using `references/prompt.md` as the formatting baseline.
5. Preserve hard constraints in every output:
   - Output is a single `infographic` markdown code block; no extra text.
   - First line is `infographic <template-name>`.
   - Use two-space indentation; key/value pairs are `key value`; arrays use `-`.
   - For compare templates (`compare-*`), ensure there are exactly two root nodes with children.