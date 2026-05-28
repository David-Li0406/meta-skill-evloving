---
name: tm-report
description: Generate comprehensive prioritized risk reports with executive summaries, threat details, gap analysis, and recommendations. Use when creating security reports, generating executive summaries, documenting risk assessments, or preparing audit documentation.
allowed-tools: Read, Write, Glob
---

# Risk Report Generation

## Purpose

Generate comprehensive risk reports that:

- Prioritize risks by severity and business impact
- Provide actionable countermeasures
- Include executive summaries for leadership
- Document evidence for audit compliance

## Usage

```
/tm-report [--format markdown|html|json] [--level executive|standard|detailed] [--output <path>]
```

**Arguments**:
- `--format`: Output format (default: markdown)
- `--level`: Detail level (default: standard)
- `--output`: Custom output path

## Report Sections

### Executive Summary
- High-level risk overview
- Critical findings count
- Compliance status
- Top 3-5 recommendations

### Risk Overview
- Risk distribution by severity
- Risk heat map
- Trend indicators (if baseline exists)

### Critical Findings
- Detailed threat descriptions
- Attack scenarios
- Business impact
- Recommended countermeasures

### Gap Analysis
- Missing controls
- Partial implementations
- Remediation priorities

### Compliance Status
- Framework coverage percentages
- Key compliance gaps

### Recommendations
- Prioritized action items
- Effort estimates
- Quick wins vs strategic improvements

### Technical Appendix
- Full threat catalog
- Control inventory
- Architecture diagrams

## Report Templates

### Executive Level
```markdown
# Security Risk Report - Executive Summary

**Project**: [Name]
**Date**: [Date]
**Classification**: Confidential

## Overview

This assessment identified [X] security risks across [Y] system components.
[N] risks are rated as **critical** and require immediate attention.

## Key Findings

| Finding | Risk Level | Business Impact |
|---------|------------|-----------------|
| [Title] | Critical | [Impact] |
| [Title] | High | [Impact] |
| [Title] | High | [Impact] |

## Compliance Status

- OWASP Top 10: [X]%
- SOC2: [Y]%

## Recommendations

1. **Immediate** (0-30 days): [Action]
2. **Short-term** (30-90 days): [Action]
3. **Strategic** (90+ days): [Action]

## Resource Requirements

[Brief estimate of resources needed]
```

### Standard Level
```markdown
# Threat Model Risk Report

**Project**: [Name]
**Version**: [Version]
**Generated**: [Date]
**Framework**: STRIDE

---

## Executive Summary

[2-3 paragraphs summarizing findings]

## Risk Overview

### At a Glance

```
RISK POSTURE: [LEVEL]
═══════════════════════════════════════════════════════════

Threats:    47 identified
Controls:   29 analyzed
Gaps:       11 found

SEVERITY DISTRIBUTION
─────────────────────────────────────────────────────────
CRITICAL │██████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░│  5
    HIGH │████████████████████████░░░░░░░░░░░░░░░░│ 12
  MEDIUM │████████████████████████████████████░░░░│ 18
     LOW │████████████████████████░░░░░░░░░░░░░░░░│ 12

CONTROL STATUS
─────────────────────────────────────────────────────────
✓ Verified:     18 controls
⚠ Partial:       7 controls
✗ Missing:       4 controls

COMPLIANCE
─────────────────────────────────────────────────────────
OWASP Top 10:   ████████░░ 82%
SOC2:           █████████░ 88%
```

### Risk Distribution Table

| Severity | Count | Mitigated | Unmitigated |
|----------|-------|-----------|-------------|
| Critical | X | Y | Z |
| High | X | Y | Z |
| Medium | X | Y | Z |
| Low | X | Y | Z |

---

## Critical Findings

### THREAT-001: [Title]

**Risk Score**: X/25 (Critical)
**Category**: [STRIDE category]
**Target**: [Component]

#### Description
[Detailed description of the threat]

#### Attack Scenario
1. [Step 1]
2. [Step 2]
3. [Step 3]

#### Business Impact
- **Confidentiality**: [Impact]
- **Integrity**: [Impact]
- **Availability**: [Impact]

#### Current Controls
| Control | Status | Effectiveness |
|---------|--------|---------------|
| [Name] | [Status] | [%] |

#### Gaps
- [Gap description]

#### Recommended Countermeasures
1. **[Priority]**: [Recommendation]
   - Effort: [Low/Medium/High]
   - Implementation: [Details]

---

## Gap Analysis

### Critical Gaps

#### GAP-001: [Title]

**Severity**: [Level]
**Control**: [Control ID]

**Expected**: [What should exist]
**Actual**: [What was found]

**Remediation**:
[Recommendation]

---

## Compliance Status

### OWASP Top 10 2021

| Requirement | Coverage | Gaps |
|-------------|----------|------|
| A01 | X% | N |
| ... | | |

---

## Recommendations

### Immediate Actions (0-30 days)

1. [Action with details]

### Short-term Improvements (30-90 days)

1. [Action with details]

### Strategic Initiatives (90+ days)

1. [Action with details]

---

## Appendix A: Threat Catalog

[Full list of threats]

## Appendix B: Control Inventory

[Full list of controls]

## Appendix C: Architecture Diagrams

[Mermaid diagrams]
```

## Output Files

- `.threatmodel/reports/risk-report.md`
- `.threatmodel/reports/executive-summary.md`
- `.threatmodel/reports/risk-report.json` (if JSON format)

## Instructions for Claude

When executing this skill:

1. **Load all threat model state**:
   - Read all files from `.threatmodel/state/`
   - Read diagrams from `.threatmodel/diagrams/`

2. **Aggregate and analyze**:
   - Count threats by severity
   - Count controls by status
   - Count gaps by priority
   - Calculate compliance percentages

3. **Prioritize findings**:
   - Sort threats by risk score
   - Identify top critical findings
   - Group recommendations by urgency

4. **Generate report sections**:
   - Write executive summary first
   - Detail critical findings
   - Document gaps
   - Provide recommendations

5. **Include visualizations IN THE REPORT FILES** (not just console):
   - Use ASCII progress bars: `████████░░ 82%`
   - Use status indicators: `✓`, `⚠`, `✗`
   - Use box-drawing characters for visual separation
   - Include Mermaid diagrams for architecture
   - The "At a Glance" section with visual bars MUST be in the written report file

6. **Write report files**:
   - Create reports directory if needed
   - Write main report
   - Write executive summary separately

7. **Report summary**:
   ```
   Report Generated
   ================

   Reports Created:
     .threatmodel/reports/risk-report.md
     .threatmodel/reports/executive-summary.md

   Report Contents:
     - Executive Summary
     - X Critical Findings detailed
     - Y Gaps documented
     - Z Recommendations provided
     - Compliance status for N frameworks
     - Full appendices

   Report Statistics:
     Total Threats: X
     Total Controls: Y
     Total Gaps: Z
     Overall Risk Level: [Level]

   The report is ready for review.
   ```
