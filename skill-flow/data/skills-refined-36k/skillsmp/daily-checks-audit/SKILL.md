---
name: Daily Checks Audit
description: Audit SAP daily monitoring check reports to validate offshore team inputs, ensuring checks were performed correctly with proper justifications for any negative findings.
---

# Daily Checks Audit Skill

This skill enables senior consultants to validate SAP daily monitoring reports performed by offshore teams **without logging into the SAP systems**.

## Overview

The skill analyzes Excel-based daily monitoring reports and generates an audit report that identifies:
- ❌ **Critical Issues**: Negative (N) responses without justification
- ⚠️ **Warnings**: Threshold violations, missing explanations for anomalies
- ✅ **Passed Checks**: Validations that meet all criteria

## Supported Customers

| Customer | Filename Pattern | Config File |
|----------|-----------------|-------------|
| BSW | `BSW_*.xlsx` | `configs/BSW_config.json` |
| TBS | `TBS_*.xlsx` | `configs/TBS_config.json` |
| COREX | `COREX_*.xlsx` | `configs/COREX_config.json` |
| SONOCO | `*EVIOSYS*.xlsx` | `configs/SONOCO_config.json` |

## Prerequisites

- **Python 3.8+** installed
- **openpyxl** package: `pip install openpyxl`

## Usage

### Step 1: Place the Excel File

Place the daily monitoring Excel file in the project directory:
```
c:\GenAI\daily_checks_audit\
```

### Step 2: Run the Audit

```powershell
cd c:\GenAI\daily_checks_audit
python .agent/skills/daily-checks-audit/scripts/audit_checks.py <excel_filename>
```

**Examples:**
```powershell
# TBS customer
python .agent/skills/daily-checks-audit/scripts/audit_checks.py TBS_DAILY_MONITORING_20_JAN_2026.xlsx

# SONOCO customer (EVIOSYS files)
python .agent/skills/daily-checks-audit/scripts/audit_checks.py CENTIQ_SAP_EVIOSYS_DAILY_MONITORING_January_2026_01_20.xlsx
```

### Step 3: Review the Report

The script generates a markdown report: `audit_report_<timestamp>.md`

The report includes:
- **Executive Summary**: Total issues (critical/warnings)
- **Check Metadata**: Date, time, performer for each system
- **Per-System Findings**: Detailed issues by system/sheet
- **Recommendations**: Action items for critical issues

## Validation Rules

### Critical Issues (Require Immediate Action)

| Rule | Description |
|------|-------------|
| N without justification | Negative response in column D/E without explanation in column G |
| Failed updates > 0 | SM13 shows failed updates |
| tRFC errors | CPICERR or SYSFAIL errors detected |

### Warnings (Review Required)

| Rule | Threshold Source |
|------|-----------------|
| Response time exceeded | Customer config (default: 1000ms) |
| High dump count (today) | Customer config (varies by customer) |
| High dump count (yesterday) | Customer config (varies by customer) |
| Old locks without explanation | Lock count > 0 without status comment |

## Customer-Specific Thresholds

Each customer has different "normal" ranges based on historical data:

| Metric | BSW | TBS | COREX | SONOCO |
|--------|-----|-----|-------|--------|
| Response Time (max) | 1000ms | 1000ms | 1000ms | 1000ms |
| Dumps Today (max) | 10 | 50 | 25 | 25 |
| Dumps Yesterday (max) | 20 | 150 | 50 | 40 |
| Failed Jobs (max) | 5 | 10 | 5 | 5 |
| Old Locks (max) | 10 | 20 | 100 | 10 |

## Adding a New Customer

1. **Create config file**: Copy an existing config and modify:
   ```
   configs/<CUSTOMER>_config.json
   ```

2. **Update detection**: Edit `scripts/audit_checks.py`, add to `detect_customer()`:
   ```python
   for prefix in ['TBS', 'BSW', 'COREX', 'SONOCO', 'NEWCUSTOMER']:
   ```

3. **Analyze historical data**: Run analysis on 5-10 files to determine appropriate thresholds

## Output Example

```
[AUDIT] Auditing: TBS_DAILY_MONITORING_20_JAN_2026.xlsx
[CONFIG] Loaded TBS customer configuration
[INFO] Found 8 system sheets

[RESULTS] Audit Results:
   [!] Critical: 4
   [?] Warnings: 1
   Total Issues: 5

[OK] Report saved to: audit_report_20260120_113157.md
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: openpyxl` | Run `pip install openpyxl` |
| `[CONFIG] No config found` | Check filename matches pattern or create config file |
| `File not found` | Ensure Excel file is in the working directory |

## Report Interpretation Guide

### Critical Issues
- **Must be addressed immediately**
- Typically indicates checks were not performed properly
- Example: "Row 77: Negative (N) response without justification"

### Warnings
- **Review required but may be acceptable**
- Often indicates values outside normal range
- Example: "Old locks present (16) without explanation"

## AI Agent Usage

This skill is designed to be invoked by AI agents (e.g., Gemini, Claude). When a user mentions daily checks or monitoring audits, the agent should use this skill.

### Trigger Phrases

The agent should activate this skill when the user says things like:
- "Audit the daily checks for [filename]"
- "Validate the daily monitoring report"
- "Check if the offshore team did the daily checks correctly"
- "Review [customer] daily monitoring file"
- "@[filename.xlsx] - audit this daily check file"

### Agent Workflow

1. **Identify the Excel file** from user's message or @mention
2. **Run the audit script**:
   ```powershell
   cd c:\GenAI\daily_checks_audit
   python .agent/skills/daily-checks-audit/scripts/audit_checks.py <filename>
   ```
3. **Read the generated report** (audit_report_*.md)
4. **Summarize findings** for the user

### Expected Agent Response Format

After running the audit, the agent should provide:

```
**Audit Summary for [Customer] - [Date]**

📊 **Results**: X critical issues, Y warnings

**Critical Issues Requiring Action:**
1. [System] Row [N]: [Issue description]
2. ...

**Warnings to Review:**
1. [System] Row [N]: [Issue description]

**Recommendation**: [Follow-up action if needed]
```

### Example Agent Interaction

**User**: "Audit TBS_DAILY_MONITORING_20_JAN_2026.xlsx"

**Agent Actions**:
1. Runs: `python .agent/skills/daily-checks-audit/scripts/audit_checks.py TBS_DAILY_MONITORING_20_JAN_2026.xlsx`
2. Reads generated report
3. Responds:

> **Audit Summary for TBS - January 20, 2026**
> 
> 📊 **Results**: 4 critical issues, 1 warning
> 
> **Critical Issues:**
> 1. CRP Row 77: N response without justification (Response times check)
> 2. BIP Row 75: N response without justification
> 3. BOP Row 7: N response without justification
> 4. JIP Row 8: N response without justification (system OK check)
> 
> **Warnings:**
> 1. ERP Row 66: 16 old locks without explanation
> 
> **Recommendation**: Follow up with Preeti Zirwal and Shivam Srivastava regarding the missing justifications.

### Handling Multiple Files

If the user provides multiple files or asks for batch processing:
1. Run the audit script on each file sequentially
2. Summarize findings across all files
3. Highlight any patterns or recurring issues

### Error Handling

| Scenario | Agent Response |
|----------|----------------|
| File not found | "I couldn't find [filename]. Please check the file is in the daily_checks_audit directory." |
| Unknown customer | "This file doesn't match any configured customer. Using default thresholds." |
| No issues found | "Great news! All checks passed validation. No issues found." |

## File Structure

```
.agent/skills/daily-checks-audit/
├── SKILL.md                    # This instruction file
├── scripts/
│   └── audit_checks.py         # Main audit script
└── configs/
    ├── BSW_config.json         # BSW thresholds
    ├── TBS_config.json         # TBS thresholds
    ├── COREX_config.json       # COREX thresholds
    └── SONOCO_config.json      # SONOCO thresholds
```
