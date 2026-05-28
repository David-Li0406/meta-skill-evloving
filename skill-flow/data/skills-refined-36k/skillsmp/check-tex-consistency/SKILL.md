---
name: check_tex_consistency
description: Systematically checks and enforces TeX format and style consistency across all note files in the L/ and T/ directories. Use when verifying note formatting after manual editing, or when performing batch audits of the notes directory.
---

# TeX Consistency Check & Fix

This skill audits the `L/` and `T/` directories for adherence to the project's strict LaTeX style, utilizing automated scripts and manual verification.

## Core Resources

- **Script**: `scripts/audit_notes.py` - Automates checking and fixing of common issues.
- **Style Guide**: `references/style_guide.md` - Defines the "Golden Standard" for document structure and strict environments.

## Workflow

### 1. Automated Audit & Remediation

Run the audit script to detect and automatically fix common structure and format violations.

```bash
# Run in dry-run mode first to see potential changes
./.agent/skills/check_tex_consistency/scripts/audit_notes.py L/

# Run with --fix to apply changes
./.agent/skills/check_tex_consistency/scripts/audit_notes.py L/ --fix

# Run with --verbose for detailed output
./.agent/skills/check_tex_consistency/scripts/audit_notes.py L/ --verbose
```

The script performs the following **4 core checks** (see `audit_notes.py` for logic):
1. **Preamble**: Ensures files are fragments (no `\documentclass`, `\begin{document}`).
2. **Header**: Ensures `\section{Notes X...}` matches the filename `LX.tex` (or `TX.tex`).
3. **Proof**: Detects active `\begin{proof}` environments (optionally comments them out with `--fix`).
4. **Indentation**: Ensures **no indentation** is present in the file. All lines must be flush left.

### 2. Secondary Verification (Human-in-the-Loop)

After running the script (especially with `--fix`), perform a secondary verification of the modified files.

1.  **Review Changes**:
    -   If the script executed fixes, use `git diff` or `view_file` on a sample of modified files to verify the changes are correct.
    -   Pay special attention to the **Header** consistency and **Proof** commenting logic.
    -   Ensure no content was accidentally deleted during Preamble removal.

2.  **Style Compliance Check**:
    -   Consult `references/style_guide.md` if in doubt about specific environments.
    -   Verify that theorem environments match the allowed set (`theorem`, `lemma`, `definition`, `remark`, etc.).
    -   If the script flagged issues it could not fix (e.g., "Missing section header"), fix them manually according to the Style Guide.

### 3. Final Consistency Verification

1.  **Main Index Check**:
    -   Read `ODE.tex`.
    -   Ensure **ALL** populated note files in `L/` and `T/` are `\input` in the main file.
    -   If any are missing, add them manually in the correct order.

### 4. Reporting

After completing the audit and fixes, **provide a CONCISE summary report**.
-   **Keep it Brief**: Do not list every single file processed.
-   **Highlight Significant Changes**: Only list specific files that had **non-indentation** repairs, such as:
    -   Active Proofs commented out.
    -   Commented Proofs re-indented.
    -   Structure (preamble/header) fixed.
-   **Group Routine Fixes**: For files with *only* simple indentation fixes, just give a total count (e.g., "Plus 12 other files with simple indentation fixes").
