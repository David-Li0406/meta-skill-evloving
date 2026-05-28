---
name: python-code-quality-scan
description: Run analyzer MCP tools (Ruff + optional dead-code scan) as a quality gate before QA/UAT/release.
---

# Skill Instructions

## Purpose

Provide a consistent, repeatable **code quality gate** for Python changes.

This skill is intended to be invoked by agents with `analyzer/*` tooling enabled.

## Inputs (Optional)

- `TARGETS` (string): paths to scan (default: `src tests run.py run_tests.py`)
- `MODE` (string): `check` (default) or `fix` (formats/fixes where safe)
- `FAIL_ON_FINDINGS` (string): `true` (default) or `false`

## Procedure

### 0) Scope selection (recommended)

Prefer scanning only Python files that changed (fast, relevant). If that’s not feasible, scan the default `TARGETS` set.

### 1) Ruff lint (required)

For each target Python file:
- Read the file contents.
- Run `analyzer/*` Ruff lint on that code.

Acceptance target: **no Ruff errors**. If `FAIL_ON_FINDINGS=true`, treat warnings as failures too.

### 2) Ruff format (optional)

If `MODE=fix`:
- Run Ruff format via `analyzer/*` on the same file contents.
- Apply formatting updates to the file.
- Re-run Ruff lint to confirm it’s clean.

### 3) Dead-code scan (optional)

If available and appropriate:
- Run a dead-code scan (e.g., Vulture) on the same target code.
- Treat **high-confidence** findings as failures when `FAIL_ON_FINDINGS=true`.

Notes:
- Keep scope reasonable (changed files first) to avoid huge scans.
- If findings are intentionally accepted, document the rationale and any follow-up.

## Output

Record:
- Which tools were run (ruff lint/format, dead-code scan)
- Targets scanned
- Pass/fail summary
- Any action taken (formatting, removal of unused imports, etc.)

## Acceptance Criteria

- Ruff reports clean results for the chosen targets
- If dead-code scan is run: no high-confidence dead-code findings (or documented exceptions)
