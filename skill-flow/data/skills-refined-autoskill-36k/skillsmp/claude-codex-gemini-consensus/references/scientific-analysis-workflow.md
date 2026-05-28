# Scientific Analysis Consensus Workflow

Complete workflow for conducting rigorous clinical research analysis with multi-AI consensus validation.

**IMPORTANT: Output Confidentiality**
Do NOT include references to multi-AI consensus, Codex, Gemini, Claude, or the validation workflow in any output files (plan.md, report.md). This methodology is proprietary. Generated documents should follow standard scientific manuscript style.

---

## CRITICAL: Preventing Infinite Loops

When invoking other agents for review, **always include REVIEWER_MODE** to prevent infinite loops:

```
REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS (claude, codex, gemini).
You MAY read files and web search. Provide YOUR expert review only.
```

**Reviewers can:** Read files, search code, web search for literature
**Reviewers cannot:** Invoke other AI agent CLIs

---

## Overview

This workflow ensures all analyses are validated by Claude, Codex, and Gemini before producing publication-ready scientific reports.

**Key Principle: ALL planned analyses must be completed correctly. No missing, incomplete, or wrong analyses allowed.**

## Directory Structure

```
project/
├── data/
│   ├── raw/
│   └── processed/
├── analysis/
│   ├── scripts/
│   ├── figures/
│   ├── tables/
│   ├── plan.md        # APPROVED PLAN (generated in Phase 2)
│   └── report.md          # FINAL REPORT (generated in Phase 4)
├── references/
│   └── citations.bib
└── GEMINI.md / AGENTS.md  # Project context
```

**Key Files:**
- `analysis/plan.md` - The approved analysis plan (contract for execution)
- `analysis/report.md` - The final publication-ready report

## Phase 1: Initial Analysis

### Step 1.1: Data Exploration

Claude performs preliminary data exploration:
- Data structure and quality assessment
- Missing data patterns
- Distribution of key variables
- Initial visualizations

### Step 1.2: Research Question Clarification

Validate the research question with both agents:

```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  --cd "$(pwd)" \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY read files and run sanity checks.

BE CONCISE. Review research question and data.

OUTPUT FORMAT:
- FEASIBLE: Y/N
- DATA GAPS: [list or 'None']
- SUGGESTED FOCUS: [recommendation]

Research question: [QUESTION]
Data summary: [DATA_SUMMARY]"
```

```bash
gemini --yolo \
  --model gemini-3-pro-preview \
  -p "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY read files and run sanity checks.

BE CONCISE. Review research question and data.

OUTPUT FORMAT:
- FEASIBLE: Y/N
- DATA GAPS: [list or 'None']
- SUGGESTED FOCUS: [recommendation]

Research question: [QUESTION]
Data summary: [DATA_SUMMARY]"
```

### Step 1.3: Initial Findings Summary

Document preliminary findings for analysis plan development.

## Phase 2: Analysis Plan Consensus

### Step 2.1: Draft Analysis Plan

Claude proposes comprehensive analysis plan.

### Step 2.2: Validate Plan with Codex

```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  --cd "$(pwd)" \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY read files and web search.

BE CONCISE. Review this analysis plan for publication.

OUTPUT FORMAT:
- STATISTICAL ISSUES: [list or 'None']
- MISSING ANALYSES: [list or 'None']
- BIAS CONCERNS: [list or 'None']
- POWER ISSUES: [list or 'None']
- VERDICT: APPROVED / NEEDS CHANGES

Plan:
[PASTE_PLAN]"
```

### Step 2.3: Validate Plan with Gemini

```bash
gemini --yolo \
  --model gemini-3-pro-preview \
  -p "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY read files and web search.

BE CONCISE. Review this analysis plan for publication.

OUTPUT FORMAT:
- STATISTICAL ISSUES: [list or 'None']
- MISSING ANALYSES: [list or 'None']
- BIAS CONCERNS: [list or 'None']
- POWER ISSUES: [list or 'None']
- VERDICT: APPROVED / NEEDS CHANGES

Plan:
[PASTE_PLAN]"
```

### Step 2.4: Synthesize and Save Plan to analysis/plan.md

After reaching consensus (internally), save the approved plan:

```markdown
# Analysis Plan: [Study Title]

## Metadata
- **Created**: [DATE]
- **Status**: APPROVED

## Objectives
1. Primary: [main research question]
2. Secondary: [additional questions]

## Data Description
- Source: [data source]
- Samples: [n=X]
- Variables: [list key variables]
- Data location: [path to data files]

## Planned Analyses

### 1. [Analysis Name]
- **Objective**: [what this answers]
- **Method**: [statistical test/approach]
- **Variables**: [input variables]
- **Expected output**: [tables, figures]
- **Code**: [script name if applicable]
- **Status**: ☐ Not started

### 2. [Analysis Name]
- **Objective**: ...
- **Method**: ...
- **Status**: ☐ Not started

[... repeat for all planned analyses ...]

## Quality Control Checks
- [ ] Data validation completed
- [ ] Missing data handling defined
- [ ] Outlier detection performed
- [ ] Assumptions checked

## Review Notes
- [Key methodological decisions]
- [Alternative approaches considered]

## Execution Instructions
When executing this plan:
1. Read each analysis section
2. Implement the specified method
3. Mark status as ✓ Complete when done
4. Validate results before proceeding
```

**IMPORTANT**: The analysis/plan.md file is the contract. During execution, compare results against this plan to ensure completeness.

**NOTE**: Do NOT include any references to multi-AI consensus, Codex, Gemini, or validation workflows in the output file (analysis/plan.md). This methodology is proprietary.

**INTERNAL TRACKING ONLY** (do not include in output files):

```markdown
## Internal Review Status

### Proposed Analyses
1. [Analysis 1] - Reviewed ✓
2. [Analysis 2] - Reviewed ✓

### Additional Analyses Suggested During Review
| Analysis | Rationale | Status |
|----------|-----------|--------|
| [Analysis A] | [reason] | Approved |
| [Analysis B] | [reason] | Approved |

### Follow-up Questions to Address
1. [Question 1] - To be answered by [Analysis X]
2. [Question 2] - To be answered by [Analysis Y]
```

## Phase 3: Execute Analysis

### Step 3.0: Load Plan from analysis/plan.md

Before executing, read the approved plan:

```bash
# Verify plan exists and is approved
cat analysis/plan.md | grep "Status: APPROVED"
```

If plan doesn't exist or isn't approved, return to Phase 2.

### Step 3.1: Implement Analyses

For each analysis in analysis/plan.md:
1. Read the analysis specification
2. Implement according to the defined method
3. Update status in analysis/plan.md: `☐ Not started` → `✓ Complete`

### Step 3.2: Validate Each Analysis Result

For each major analysis, submit results to both agents:

```bash
# Codex validation (concise) - REVIEWER_MODE allows sanity checks
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  --cd "$(pwd)" \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS.
You MAY read files and run quick sanity checks to verify calculations.

BE CONCISE. Validate this analysis result.

OUTPUT FORMAT:
- STATISTICAL ERRORS: [list or 'None']
- ASSUMPTION VIOLATIONS: [list or 'None']
- INTERPRETATION ISSUES: [list or 'None']
- VERDICT: VALID / INVALID

Analysis: [PASTE_ANALYSIS]
Code: [PASTE_CODE]"
```

```bash
# Gemini validation (concise) - REVIEWER_MODE allows sanity checks
gemini --yolo \
  --model gemini-3-pro-preview \
  -p "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS.
You MAY read files and run quick sanity checks to verify calculations.

BE CONCISE. Validate this analysis result.

OUTPUT FORMAT:
- STATISTICAL ERRORS: [list or 'None']
- ASSUMPTION VIOLATIONS: [list or 'None']
- INTERPRETATION ISSUES: [list or 'None']
- VERDICT: VALID / INVALID

Analysis: [PASTE_ANALYSIS]
Code: [PASTE_CODE]"
```

### Step 3.3: Fix Issues

If issues found:
1. Address each concern
2. Re-run analysis
3. Re-validate until consensus approval

## Phase 3.5: Analysis Completeness Verification

**CRITICAL CHECKPOINT: Ensure ALL planned analyses from analysis/plan.md are completed correctly.**

### Step 3.5.1: Generate Completeness Checklist

```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  --cd "$(pwd)" \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY read files.

BE CONCISE. Compare analysis/plan.md plan vs results.

OUTPUT FORMAT (table only):
| # | Analysis | Status | Issue | Action |
|---|----------|--------|-------|--------|
| 1 | [name] | ✓/⚠/✗/❌ | [brief] | [brief] |

STATUS: ✓=Complete ⚠=Incomplete ✗=Missing ❌=Wrong

No commentary. Table only."
```

### Step 3.5.2: Independent Verification with Gemini

```bash
gemini --yolo \
  --model gemini-3-pro-preview \
  -p "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY read files.

BE CONCISE. Verify completeness: analysis/plan.md vs results.

OUTPUT FORMAT (table only):
| # | Analysis | Status | Issue |
|---|----------|--------|-------|

STATUS: ✓/⚠/✗/❌

No commentary. Table only."
```

### Step 3.5.3: Reconcile Checklists

Compare Codex and Gemini checklists:
- Identify all flagged items from both
- Resolve any disagreements about status
- Create unified action list

Document in `analysis/plan.md`:

```markdown
## Analysis Completeness Verification

### Verification Date: [DATE]

### Status Summary

**INTERNAL TRACKING ONLY** (do not include in output files):

| Status | Count |
|--------|-------|
| ✓ Complete | X |
| ⚠ Incomplete | X |
| ✗ Missing | X |
| ❌ Wrong | X |

### Detailed Checklist (Internal)

| # | Planned Analysis | Review 1 | Review 2 | Status | Action |
|---|------------------|----------|----------|--------|--------|
| 1 | Survival analysis | ✓ | ✓ | ✓ Complete | None |
| 2 | Subgroup analysis | ⚠ | ⚠ | ⚠ Incomplete | Add age subgroups |
| 3 | Sensitivity analysis | ✗ | ✗ | ✗ Missing | Implement full |
| 4 | Correlation matrix | ❌ | ❌ | ❌ Wrong | Use Spearman not Pearson |

### Required Corrections

#### Missing Analyses
1. **[Analysis Name]**
   - Description: [what should be done]
   - Method: [statistical approach]
   - Priority: HIGH/MEDIUM

#### Incomplete Analyses
1. **[Analysis Name]**
   - Missing component: [what's missing]
   - Action: [specific steps]

#### Wrong Analyses  
1. **[Analysis Name]**
   - Error: [what's wrong]
   - Correction: [how to fix]
   - Impact: [how this affects results]
```

### Step 3.5.4: Conduct Corrections

For each flagged item:

1. **Missing analyses** → Implement from scratch following original plan
2. **Incomplete analyses** → Complete the missing components
3. **Wrong analyses** → 
   - Document the error
   - Implement correct analysis
   - Compare results (note if conclusions change)
   - Update all dependent analyses

### Step 3.5.5: Re-validate Corrections

Each corrected analysis must be validated:

```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS.
You MAY read files and run sanity checks to verify the correction.

Validate this CORRECTED analysis.

Original issue: [DESCRIBE WHAT WAS WRONG/MISSING]
Correction applied: [DESCRIBE THE FIX]

Verify:
1. Correction properly addresses the issue
2. Analysis now matches the original plan
3. Results are statistically valid
4. No new errors introduced

Corrected Analysis:
[PASTE_CORRECTED_ANALYSIS]"
```

### Step 3.5.6: Final Completeness Confirmation

```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  --cd "$(pwd)" \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY read files.

BE CONCISE. Final check: all analyses in analysis/plan.md complete?

OUTPUT: 'ALL COMPLETE' or list remaining: [#] [name] [issue]"
```

Only proceed to Phase 4 (Draft Report) when output is "ALL COMPLETE".

## Phase 4: Draft Report

### Step 4.1: Create Report Structure

Create `analysis/report.md`:

```markdown
# [Study Title]

## Abstract
[To be written after all sections complete]

## Introduction
- Background and rationale
- Current knowledge gaps
- Study objectives

## Methods

### Study Design
[Design description]

### Data Sources
[Data description, IRB if applicable]

### Statistical Analysis
[All methods with software versions]

### Quality Control
[Validation procedures and data quality checks]

## Results

### Patient/Sample Characteristics
[Table 1: Baseline characteristics]

### Primary Outcomes
[Main findings with statistics]

### Secondary Outcomes
[Additional findings]

### Exploratory Analyses
[Hypothesis-generating findings]

## Discussion

### Principal Findings
[Key results interpretation]

### Comparison with Literature
[How findings relate to prior work]

### Clinical Implications
[Actionable insights]

### Limitations
[Study limitations]

### Future Directions
[Next steps]

## Conclusions
[Summary statement]

## References
[PubMed citations in Vancouver style]

## Figures
[Publication-ready figures with captions]

## Tables
[Publication-ready tables with captions]

## Supplementary Material
[Additional analyses, code availability]
```

### Step 4.2: Write Each Section

For each section, draft then validate:

```bash
# Validate Methods section - REVIEWER_MODE
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY web search for standards.

Review this Methods section for scientific manuscript.

CHECK:
1. Reproducibility - Can another researcher replicate this?
2. Completeness - Are all methods described?
3. Statistical rigor - Are analyses appropriate?
4. Clarity - Is it understandable?
5. Journal standards - Does it meet publication standards?

Methods:
[PASTE_METHODS]

Suggest improvements."
```

## Phase 5: Figures and Tables

### CRITICAL: Standalone Scripts Requirement

**Every figure and table MUST have its own standalone script** that can be independently executed to regenerate the output. This ensures reproducibility and easy modification.

### Python Virtual Environment Requirement

**All Python scripts MUST use the project venv at `~/.venv`**

Setup (run once at project start):
```bash
# Create venv if it doesn't exist
if [ ! -d ~/.venv ]; then
    python3 -m venv ~/.venv
    source ~/.venv/bin/activate
    pip install --upgrade pip
    pip install pandas numpy matplotlib seaborn scipy lifelines scikit-learn statsmodels openpyxl xlsxwriter
fi
```

### Directory Structure

```
analysis/
├── scripts/
│   ├── setup_venv.sh           # Venv setup script
│   ├── generate_all.sh         # Master generation script
│   ├── figures/
│   │   ├── fig01_survival_curve.R
│   │   ├── fig02_forest_plot.py
│   │   └── ...
│   └── tables/
│       ├── tab01_baseline.R
│       ├── tab02_univariate.py
│       └── ...
├── figures/
│   ├── fig01_survival_curve.png
│   ├── fig01_survival_curve.pdf
│   └── ...
├── tables/
│   ├── tab01_baseline.csv
│   ├── tab01_baseline.docx
│   └── ...
└── report.md
```

### Naming Convention

```
fig[NN]_[descriptive_name].[ext]
tab[NN]_[descriptive_name].[ext]
```

### Standalone Figure Script Template (Python)

```python
#!/usr/bin/env python3
"""
=============================================================================
Figure 02: Forest Plot - Hazard Ratios
=============================================================================
Description: Forest plot showing hazard ratios from multivariate Cox model
Input:       analysis/data/processed/cox_results.csv
Output:      analysis/figures/fig02_forest_plot.png
             analysis/figures/fig02_forest_plot.pdf

USAGE:
    source ~/.venv/bin/activate && python analysis/scripts/figures/fig02_forest_plot.py
    OR: ~/.venv/bin/python analysis/scripts/figures/fig02_forest_plot.py

Author:      [Author]
Date:        [Date]
=============================================================================
"""
import sys, os

# --- Ensure venv is used ---
VENV_PYTHON = os.path.expanduser("~/.venv/bin/python")
if sys.executable != VENV_PYTHON and os.path.exists(VENV_PYTHON):
    print(f"WARNING: Not using project venv. Run with: {VENV_PYTHON} {__file__}")

# --- Configuration (MODIFY THESE) ---
INPUT_FILE  = "analysis/data/processed/cox_results.csv"
OUTPUT_PNG  = "analysis/figures/fig02_forest_plot.png"
OUTPUT_PDF  = "analysis/figures/fig02_forest_plot.pdf"

FIGURE_WIDTH  = 10      # inches
FIGURE_HEIGHT = 8       # inches
FIGURE_DPI    = 300     # publication quality
FONT_SIZE     = 12

# --- Libraries ---
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Ensure output directory exists ---
os.makedirs(os.path.dirname(OUTPUT_PNG), exist_ok=True)

# --- Load Data ---
data = pd.read_csv(INPUT_FILE)

# --- Create Figure ---
fig, ax = plt.subplots(figsize=(FIGURE_WIDTH, FIGURE_HEIGHT))
# [Figure creation code]
plt.tight_layout()

# --- Save Outputs ---
plt.savefig(OUTPUT_PNG, dpi=FIGURE_DPI, bbox_inches='tight')
plt.savefig(OUTPUT_PDF, bbox_inches='tight')
plt.close()

print(f"✓ Figure saved to: {OUTPUT_PNG}")
print(f"✓ Figure saved to: {OUTPUT_PDF}")
```

### Standalone Figure Script Template (R)

```r
#!/usr/bin/env Rscript
# =============================================================================
# Figure 01: Kaplan-Meier Overall Survival Curve
# =============================================================================
# Description: [Description]
# Input:       analysis/data/processed/survival_data.csv
# Output:      analysis/figures/fig01_kaplan_meier_os.png/pdf
# USAGE:       Rscript analysis/scripts/figures/fig01_survival_curve.R
# Author:      [Author]
# Date:        [Date]
# =============================================================================

# --- Configuration (MODIFY THESE) ---
INPUT_FILE  <- "analysis/data/processed/survival_data.csv"
OUTPUT_PNG  <- "analysis/figures/fig01_kaplan_meier_os.png"
OUTPUT_PDF  <- "analysis/figures/fig01_kaplan_meier_os.pdf"

FIGURE_WIDTH  <- 8
FIGURE_HEIGHT <- 6
FIGURE_DPI    <- 300

# --- Libraries ---
library(survival)
library(survminer)
library(ggplot2)

# --- Ensure output directory exists ---
dir.create(dirname(OUTPUT_PNG), recursive = TRUE, showWarnings = FALSE)

# --- Load Data & Create Figure ---
data <- read.csv(INPUT_FILE)
# [Figure creation code]

# --- Save Outputs ---
ggsave(OUTPUT_PNG, width = FIGURE_WIDTH, height = FIGURE_HEIGHT, dpi = FIGURE_DPI)
ggsave(OUTPUT_PDF, width = FIGURE_WIDTH, height = FIGURE_HEIGHT)

cat("✓ Figure saved to:", OUTPUT_PNG, "\n")
cat("✓ Figure saved to:", OUTPUT_PDF, "\n")
```

### Standalone Table Script Template (Python)

```python
#!/usr/bin/env python3
"""
=============================================================================
Table 02: Univariate Cox Regression Results
=============================================================================
Description: Univariate hazard ratios for all candidate predictors
Input:       analysis/data/processed/patient_data.csv
Output:      analysis/tables/tab02_univariate_cox.csv
             analysis/tables/tab02_univariate_cox.xlsx

USAGE:
    ~/.venv/bin/python analysis/scripts/tables/tab02_univariate_cox.py

Author:      [Author]
Date:        [Date]
=============================================================================
"""
import sys, os

VENV_PYTHON = os.path.expanduser("~/.venv/bin/python")
if sys.executable != VENV_PYTHON and os.path.exists(VENV_PYTHON):
    print(f"WARNING: Not using project venv. Run with: {VENV_PYTHON} {__file__}")

# --- Configuration (MODIFY THESE) ---
INPUT_FILE   = "analysis/data/processed/patient_data.csv"
OUTPUT_CSV   = "analysis/tables/tab02_univariate_cox.csv"
OUTPUT_XLSX  = "analysis/tables/tab02_univariate_cox.xlsx"

DECIMAL_PLACES = 2
P_VALUE_DIGITS = 3

# --- Libraries ---
import pandas as pd
import numpy as np

# --- Ensure output directory exists ---
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

# --- Load Data & Create Table ---
data = pd.read_csv(INPUT_FILE)
# [Table creation code]
results_df = pd.DataFrame(results)

# --- Save Outputs ---
results_df.to_csv(OUTPUT_CSV, index=False)
results_df.to_excel(OUTPUT_XLSX, index=False)

print(f"✓ Table saved to: {OUTPUT_CSV}")
print(f"✓ Table saved to: {OUTPUT_XLSX}")
```

### Venv Setup Script (analysis/scripts/setup_venv.sh)

```bash
#!/bin/bash
# Setup Python venv at ~/.venv
VENV_PATH="$HOME/.venv"

if [ ! -d "$VENV_PATH" ]; then
    python3 -m venv "$VENV_PATH"
fi

source "$VENV_PATH/bin/activate"
pip install --upgrade pip
pip install pandas numpy matplotlib seaborn scipy lifelines scikit-learn statsmodels openpyxl xlsxwriter plotly kaleido

echo "✓ Setup complete! Activate with: source ~/.venv/bin/activate"
```

### Master Generation Script (analysis/scripts/generate_all.sh)

```bash
#!/bin/bash
# Generate all figures and tables
set -e
VENV_PYTHON="$HOME/.venv/bin/python"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

[ ! -f "$VENV_PYTHON" ] && echo "ERROR: Run setup_venv.sh first" && exit 1

echo "--- Generating Figures ---"
for s in "$SCRIPT_DIR"/figures/*.py; do [ -f "$s" ] && "$VENV_PYTHON" "$s"; done
for s in "$SCRIPT_DIR"/figures/*.R; do [ -f "$s" ] && Rscript "$s"; done

echo "--- Generating Tables ---"
for s in "$SCRIPT_DIR"/tables/*.py; do [ -f "$s" ] && "$VENV_PYTHON" "$s"; done
for s in "$SCRIPT_DIR"/tables/*.R; do [ -f "$s" ] && Rscript "$s"; done

echo "✓ All figures and tables generated!"
```

### Script Requirements Checklist

Every figure/table script MUST include:

- [ ] **Shebang line** (`#!/usr/bin/env python3` or `#!/usr/bin/env Rscript`)
- [ ] **Header block** with description, input/output paths, USAGE, author, date
- [ ] **Venv check** (Python) - warn if not using ~/.venv
- [ ] **Configuration section** at top with ALL modifiable parameters
- [ ] **Directory creation** - create output dirs if missing
- [ ] **Self-contained** - runs independently
- [ ] **Multiple output formats** (PNG + PDF / CSV + XLSX)
- [ ] **300+ DPI** for publication quality
- [ ] **Confirmation message** showing output paths

### Step 5.1: Figure Requirements

All figures must be:
- High resolution (300+ DPI for print)
- Clear axis labels with units
- Appropriate color schemes (colorblind-friendly)
- Publication-ready captions

### Step 5.2: Figure Caption Template

```markdown
**Figure X. [Descriptive Title]**

[Description of what the figure shows, sample sizes (n=X), statistical tests, significance thresholds]

*Abbreviations: [Define all abbreviations]*
```

### Step 5.3: Table Requirements

All tables must include:
- Clear headers with units
- Appropriate precision
- Statistical comparisons where relevant
- Footnotes explaining symbols/abbreviations

### Step 5.4: Table Caption Template

```markdown
**Table X. [Descriptive Title]**

*Notes: Data presented as mean ± SD, median (IQR), or n (%) as appropriate.
Statistical comparisons: [tests used]. Abbreviations: [Define all].*
```

### Step 5.5: Validate Figures and Tables

```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  --cd "$(pwd)" \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY read files.

BE CONCISE. Review figures/tables for publication.

Output: | Item | Issue | Fix |

Check: accuracy, clarity, completeness, captions, standards."
```

## Phase 6: Final Validation

### Step 6.1: Clinical Assessment

```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS.
You MAY web search for clinical guidelines and literature.

Assess this analysis from a CLINICAL perspective.

EVALUATE:
1. Clinical relevance - Are findings actionable?
2. Effect sizes - Are they clinically meaningful (not just statistically significant)?
3. Patient impact - How does this affect patient care?
4. Generalizability - To which patient populations?
5. Implementation - Can findings be implemented in practice?
6. Risks - Any potential harms from applying these findings?

Report:
[PASTE_FULL_REPORT]

Provide clinical assessment."
```

### Step 6.2: Scientific Assessment

```bash
gemini --yolo \
  --model gemini-3-pro-preview \
  -p "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS.
You MAY web search for literature and methodology references.

Assess this analysis from a SCIENTIFIC perspective.

EVALUATE:
1. Rigor - Is methodology sound?
2. Validity - Are conclusions supported by evidence?
3. Novelty - What is the scientific contribution?
4. Reproducibility - Can others replicate this?
5. Limitations - Are they appropriately acknowledged?
6. Future work - What questions remain?

Report:
[PASTE_FULL_REPORT]

Provide scientific assessment."
```

### Step 6.3: Final Approval

Ensure all validations pass before finalizing the report.

**IMPORTANT**: Do NOT include any references to multi-AI consensus, Codex, Gemini, or the validation workflow in the final report. This methodology is proprietary.

The final report should follow standard scientific manuscript format without mentioning AI validation processes.

**Internal tracking only** (do not include in report.md):

```markdown
## Internal: Validation Checklist

| Aspect | Status |
|--------|--------|
| Methods | ✓ Validated |
| Statistical Analysis | ✓ Validated |
| Results Interpretation | ✓ Validated |
| Clinical Validity | ✓ Validated |
| Scientific Validity | ✓ Validated |

### Issues Identified and Resolved
1. [Issue] → [Resolution]
2. [Issue] → [Resolution]
```

## Phase 7: Citations

### PubMed Citation Format

Use Vancouver style for medical journals:

```
1. Author AA, Author BB, Author CC. Title of article. Journal Name. Year;Volume(Issue):Pages. doi:XX.XXXX/XXXXX. PMID: XXXXXXXX.
```

### Citation Validation

```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  --search \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS.
You MAY and SHOULD web search to verify citations.

Verify these PubMed citations are accurate and relevant.

For each citation:
1. Verify PMID exists and matches the claim
2. Check if citation supports the statement made
3. Suggest better citations if available
4. Flag any retracted papers

Citations:
[PASTE_CITATIONS_WITH_CONTEXT]"
```

## Quick Reference Commands

### Concise Output Pattern

Always prepend to prompts (REVIEWER_MODE prevents infinite loops):
```
REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY read files and web search.
BE CONCISE. No preamble. Output format: [specify structure]
```

### Full Consensus Review Cycle

```bash
# 1. Submit to Codex (REVIEWER_MODE)
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  --cd "$(pwd)" \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS.
BE CONCISE. [TASK]. Output: ISSUES: / VERDICT:"

# 2. Submit to Gemini (REVIEWER_MODE)
gemini --yolo \
  --model gemini-3-pro-preview \
  -p "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS.
BE CONCISE. [TASK]. Output: ISSUES: / VERDICT:"

# 3. Synthesize in Claude (orchestrator)
# 4. Iterate until consensus
```

### With Web Search (for literature)

```bash
# Codex with search (REVIEWER_MODE)
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  --search \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY web search.
BE CONCISE. Search [TOPIC]. Output: 1. [finding] PMID:X  2. [finding] PMID:Y"

# Gemini with search (REVIEWER_MODE)
gemini --yolo \
  --model gemini-3-pro-preview \
  -p "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY web search.
BE CONCISE. Search [TOPIC]. Output: 1. [finding] PMID:X  2. [finding] PMID:Y"
```

## Checklist Before Submission

### Analysis Completeness
- [ ] All planned analyses identified and tracked
- [ ] Completeness verification performed by Codex AND Gemini
- [ ] All missing analyses implemented
- [ ] All incomplete analyses completed
- [ ] All wrong analyses corrected and re-validated
- [ ] Final completeness confirmation obtained

### Validation
- [ ] All analyses validated by Claude, Codex, and Gemini
- [ ] Statistical methods appropriate and correctly applied
- [ ] Each corrected analysis re-validated

### Report Quality
- [ ] All figures publication-ready with complete captions
- [ ] All tables publication-ready with complete captions
- [ ] Clinical implications assessed
- [ ] Scientific validity confirmed
- [ ] All citations verified with PMIDs
- [ ] Limitations appropriately discussed
- [ ] Code availability documented

---

## Appendix: Domain-Specific Examples

> **Note:** All examples include REVIEWER_MODE to prevent infinite loops when agents have consensus skills installed.

### Example A: Cancer Type Hypothesis (Oncology)

For oncology research with molecular data, you may want to hypothesize the cancer type:

```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  --search \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY web search for PMIDs.

BE CONCISE. Hypothesize cancer type from this molecular data.

OUTPUT FORMAT:
1. [Cancer Type] - Confidence: HIGH/MED/LOW - Evidence: [key features] - PMID: [citation]
2. [Cancer Type] - Confidence: HIGH/MED/LOW - Evidence: [key features] - PMID: [citation]
3. [Cancer Type] - Confidence: HIGH/MED/LOW - Evidence: [key features] - PMID: [citation]

Data summary:
[PASTE_DATA_SUMMARY]"
```

Output for plan.md (if applicable):
```markdown
## Cancer Type Hypothesis

**Most likely cancer type**: [TYPE]
**Confidence**: HIGH / MEDIUM / LOW

**Supporting evidence**:
1. [Evidence 1] (PMID: XXXXX)
2. [Evidence 2] (PMID: XXXXX)

**Differential considerations**:
- [Alternative type 1]: [why less likely]
```

### Example B: Drug Mechanism Hypothesis (Pharmacology)

```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  --search \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY web search.

BE CONCISE. Based on this gene expression data, hypothesize the drug mechanism.

OUTPUT FORMAT:
1. [Mechanism] - Confidence: HIGH/MED/LOW - Evidence: [pathways] - PMID: [citation]

Data summary: [DATA]"
```

### Example C: Biomarker Discovery (Diagnostics)

```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  --search \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY web search.

BE CONCISE. Identify candidate biomarkers from this data.

OUTPUT FORMAT:
| Biomarker | AUC | Sensitivity | Specificity | Literature Support |

Data summary: [DATA]"
```

### Example D: Genetic Variant Classification (Genomics)

```bash
codex exec --dangerously-bypass-approvals-and-sandbox \
  --model gpt-5.2-codex \
  --skip-git-repo-check \
  --search \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY web search.

BE CONCISE. Classify this variant using ACMG criteria.

OUTPUT FORMAT:
- Classification: [Pathogenic/Likely Pathogenic/VUS/Likely Benign/Benign]
- Evidence: [ACMG codes]
- ClinVar: [concordance]

Variant: [VARIANT_INFO]"
```

These are examples only. Adapt the prompts to your specific domain and research question. **Always include REVIEWER_MODE when invoking other agents.**
