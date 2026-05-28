---
name: x07-lint-repair
description: Lint X07 x07AST JSON and converge via deterministic quickfixes (`x07 fix`) or explicit JSON Patch (`x07 ast apply-patch`).
metadata:
  short-description: Lint + fix + patch loop
  version: 0.1.0
  kind: docs
---

# x07-lint-repair

Use this skill when an X07 file fails linting and the agent needs a deterministic converge loop.

## Canonical converge loop

1. Lint (machine-readable JSON report):
   - `x07 lint --input src/main.x07.json --world solve-pure --report-json`

2. Apply tool-provided quickfixes (when diagnostics include JSON Patch quickfixes):
   - `x07 fix --input src/main.x07.json --world solve-pure --write --report-json`

3. If a custom fix is needed, apply an explicit JSON Patch (RFC 6902):
   - `x07 ast apply-patch --in src/main.x07.json --patch /tmp/repair.patch.json --validate`

4. Canonicalize after patching:
   - `x07 fmt --input src/main.x07.json --write --report-json`

Repeat (max 3 iterations). If still failing, stop and change strategy (reduce scope, regenerate the x07AST cleanly, or ask for clarification).
