---
name: cip-document-generation
description: Generate professional contract analysis reports (.docx) for the Contract Intelligence Platform. Three report types: (1) Contract Risk Review - initial analysis with risk ratings, heat map, clause analysis, negotiation playbook; (2) Suggested Redlines and Revisions - proposed changes with before/after risk matrix, implementation notes, negotiation guide; (3) Version Comparison - compare two contract versions with delta analysis and grouped comparison tables. Use when user requests contract risk analysis, redline suggestions, or version comparison reports.
---

# CIP Document Generation Skill

Generate three contract analysis report types as professional .docx documents with consistent formatting, visual risk indicators, and structured data storage.

## Report Types

| Report | Trigger | Output |
|--------|---------|--------|
| Contract Risk Review | "analyze risk", "review contract", "risk assessment" | Risk ratings, heat map, clause analysis, negotiation playbook |
| Suggested Redlines and Revisions | "suggest changes", "redline", "revisions needed" | Proposed changes, before/after risk, negotiation guide |
| Version Comparison | "compare versions", "what changed", "V1 vs V2" | Delta analysis, grouped comparison table |

## Workflow

### Phase 1: Gather Requirements

Ask **one at a time**, wait for response:

1. **Report type?** (Risk Review / Redlines / Comparison)
2. **Contract name?**
3. **Your entity name** (or token from document, e.g., [COMPANY_A])
4. **Counterparty name** (or token, e.g., [COMPANY_B])
5. **Your position/role?** (Buyer, Seller, Integrator, Vendor, etc.)
6. **For Comparison only:** Version identifiers (e.g., "October Draft" → "November Final")

### Phase 2: Extract Contract

Read docx skill first:
```bash
cat /mnt/skills/public/docx/SKILL.md
```

Extract text:
```bash
pandoc --track-changes=accept contract.docx -o contract.md
```

### Phase 3: Analyze by Clause Type

Detect clauses using taxonomy keywords. Classify each by:

**Three-tier clause weighting:**

| Weight | Clause Types |
|--------|--------------|
| **Critical** | Indemnification, Limitation of Liability, IP/Work Ownership |
| **High** | Termination, Insurance, Vendor Displacement, Non-Solicitation |
| **Standard** | Confidentiality, Payment/Fees, Warranties, Force Majeure, Governing Law |

**Risk levels:** 🔴 CRITICAL, 🟠 HIGH, 🔵 MODERATE, 🟢 LOW

### Phase 4: Generate Report

Read docx-js documentation:
```bash
cat /mnt/skills/public/docx/docx-js.md
```

Generate .docx using report structure below.

### Phase 5: Save to Database

On user finalization:
1. Save to `reports` table with `status: finalized`
2. Extract findings to `report_findings` table
3. For comparisons, save deltas to `report_deltas` table

### Phase 6: Deliver

```
✅ REPORT COMPLETE

[View Report](computer:///mnt/user-data/outputs/[filename].docx)

SUMMARY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Report-specific summary]
```

---

## Report Structures

### Report 1: Contract Risk Review

```
1. Title Page
2. Executive Summary
3. Risk Heat Map
4. Clause Analysis Table (grouped by clause type)
5. Negotiation Playbook
6. Disclaimers
```

### Report 2: Suggested Redlines and Revisions

```
1. Title Page
2. Executive Summary
3. Combined Risk Matrix (Before | After | Delta)
4. Redline Table (grouped by clause type)
5. Implementation Notes
6. Negotiation Guide
7. Disclaimers
```

### Report 3: Version Comparison

```
1. Title Page
2. Executive Summary
3. Combined Risk Matrix (V1 | V2 | Delta)
4. Detailed Comparison Table (grouped by clause type)
5. Disclaimers
```

---

## Component Specifications

### Title Page

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│                    [CONTRACT NAME]                          │
│                                                             │
│              [REPORT TYPE TITLE]                            │
│                                                             │
│            [Version info - comparison only]                 │
│                                                             │
│              Date: [Date]                                   │
│                                                             │
│              Our Entity: [COMPANY_A]                        │
│              Counterparty: [COMPANY_B]                      │
│              Position: [Role]                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

Report type titles:
- CONTRACT RISK REVIEW
- SUGGESTED REDLINES AND REVISIONS
- VERSION COMPARISON REPORT

### Executive Summary: Contract Risk Review

```
┌─────────────────────────────────────────────────────────────┐
│ OVERALL RISK ASSESSMENT: [CRITICAL / HIGH / MODERATE / LOW]│
├─────────────────────────────────────────────────────────────┤
│ TOP CONCERNS                                                │
│ 1. [Clause type]: [One-line concern]                       │
│ 2. [Clause type]: [One-line concern]                       │
│ 3. [Clause type]: [One-line concern]                       │
├─────────────────────────────────────────────────────────────┤
│ RISK DISTRIBUTION                                           │
│ 🔴 CRITICAL: [n]  🟠 HIGH: [n]  🔵 MODERATE: [n]  🟢 LOW: [n]│
└─────────────────────────────────────────────────────────────┘
```

**Overall Risk Scoring (adjectival, clause-weighted):**
```
IF any Critical-weight clause has CRITICAL risk → Overall: CRITICAL
ELSE IF any Critical-weight clause has HIGH risk → Overall: HIGH
ELSE IF any High-weight clause has CRITICAL risk → Overall: HIGH
ELSE IF multiple High-weight clauses have HIGH risk → Overall: HIGH
ELSE IF any clause has HIGH risk → Overall: MODERATE
ELSE → Overall: LOW
```

### Executive Summary: Suggested Redlines and Revisions

```
┌─────────────────────────────────────────────────────────────┐
│ REVISION IMPACT                                             │
│              │ Before │ After │                             │
│ 🔴 CRITICAL  │   [n]  │  [n]  │                             │
│ 🟠 HIGH      │   [n]  │  [n]  │                             │
│ 🔵 MODERATE  │   [n]  │  [n]  │                             │
│ 🟢 LOW       │   [n]  │  [n]  │                             │
├─────────────────────────────────────────────────────────────┤
│ CHANGES PROPOSED                                            │
│ Total: [n]  Dealbreaker: [n] | Industry Standard: [n] | Nice-to-Have: [n]│
├─────────────────────────────────────────────────────────────┤
│ KEY REVISIONS                                               │
│ 1. [Clause type]: [One-line change summary]                │
│ 2. [Clause type]: [One-line change summary]                │
│ 3. [Clause type]: [One-line change summary]                │
└─────────────────────────────────────────────────────────────┘
```

### Executive Summary: Version Comparison

```
┌─────────────────────────────────────────────────────────────┐
│ VERSION DELTA                                               │
│              │  V1  │  V2  │ Delta │                        │
│ 🔴 CRITICAL  │  [n] │  [n] │ [±n]  │                        │
│ 🟠 HIGH      │  [n] │  [n] │ [±n]  │                        │
│ 🔵 MODERATE  │  [n] │  [n] │ [±n]  │                        │
│ 🟢 LOW       │  [n] │  [n] │ [±n]  │                        │
├─────────────────────────────────────────────────────────────┤
│ CHANGES DETECTED                                            │
│ Total: [n]  Additions: [n] | Modifications: [n] | Deletions: [n]│
├─────────────────────────────────────────────────────────────┤
│ KEY THEMES (by clause priority)                             │
│                                                             │
│ Critical Weight:                                            │
│ • Indemnification: [change summary or "No changes"]        │
│ • Limitation of Liability: [change summary or "No changes"]│
│ • IP/Work Ownership: [change summary or "No changes"]      │
│                                                             │
│ High Weight:                                                │
│ • Termination: [change summary or "No changes"]            │
│ • Insurance: [change summary or "No changes"]              │
│ • Vendor Displacement: [change summary or "No changes"]    │
│ • Non-Solicitation: [change summary or "No changes"]       │
│                                                             │
│ Standard Weight: [n] changes across [n] clause types       │
└─────────────────────────────────────────────────────────────┘
```

### Combined Risk Matrix

Used in: Reports 2 and 3

```
┌──────────────────────────────────────────────────────────────┐
│ RISK MATRIX                                                  │
├──────────────────────────┬──────────┬──────────┬────────┐   │
│ Clause Type              │ Before/V1│ After/V2 │ Delta  │   │
├──────────────────────────┼──────────┼──────────┼────────┤   │
│ [Clause with findings]   │    🔴    │    🟠    │   ▼    │   │
│ [Clause with findings]   │    🟠    │    🔵    │   ▼    │   │
└──────────────────────────┴──────────┴──────────┴────────┘   │
├──────────────────────────────────────────────────────────────┤
│ NO CHANGES REQUIRED                                          │
│ • [Section] [Title]           • [Section] [Title]           │
└──────────────────────────────────────────────────────────────┘
```

Delta symbols: ▲ (increased), ▼ (decreased), ● (unchanged)

### Risk Heat Map

Used in: Report 1

```
┌─────────────────────────────────────────────────────────────┐
│ RISK HEAT MAP                                               │
├──────────────────────┬──────┬──────┬──────┬──────┐         │
│ Clause Type          │ CRIT │ HIGH │ MOD  │ LOW  │         │
├──────────────────────┼──────┼──────┼──────┼──────┤         │
│ [Clause type]        │  🔴  │      │      │      │         │
│ [Clause type]        │      │  🟠  │      │      │         │
└──────────────────────┴──────┴──────┴──────┴──────┘         │
├─────────────────────────────────────────────────────────────┤
│ NO FINDINGS                                                 │
│ • [Section] [Title]           • [Section] [Title]          │
└─────────────────────────────────────────────────────────────┘
```

### Clause Analysis Table

Used in: Report 1 (grouped by clause type)

```
┌─────────────────────────────────────────────────────────────┐
│ [CLAUSE TYPE]                                           🔴  │
├─────────┬──────┬──────────────────┬─────────────────────────┤
│ Section │ Risk │ Concern          │ Recommendation          │
├─────────┼──────┼──────────────────┼─────────────────────────┤
│ [#]     │  🔴  │ [Concern text]   │ [Recommendation text]   │
└─────────┴──────┴──────────────────┴─────────────────────────┘
```

### Redline Table

Used in: Report 2 (grouped by clause type)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ [CLAUSE TYPE]                                                           🔴  │
├─────────┬──────┬─────────────────┬─────────────────┬────────────────────────┤
│ Section │ Risk │ Original        │ Proposed Change │ Rationale              │
├─────────┼──────┼─────────────────┼─────────────────┼────────────────────────┤
│ [#]     │  🔴  │ [Original text] │ [Redlined text] │ [Rationale text]       │
└─────────┴──────┴─────────────────┴─────────────────┴────────────────────────┘
```

### Comparison Table

Used in: Report 3 (5-column, sequential with related clauses)

```
| # | Section / Category | V1 (Original) | V2 (Final) - Redlined | Business Impact |
|---|---------------------|---------------|----------------------|-----------------|
| [n] | [#] - [Title] | [V1 text] | [V2 redlined text] | [Impact narrative] |
|   | Related: [x.x, y.y] | | | |
```

### Negotiation Playbook

Used in: Report 1

```
┌─────────────────────────────────────────────────────────────┐
│ NEGOTIATION PLAYBOOK                                        │
├─────────────────────────────────────────────────────────────┤
│ YOUR LEVERAGE                                               │
│ • [Leverage point]                                         │
├─────────────────────────────────────────────────────────────┤
│ COUNTERPARTY LEVERAGE                                       │
│ • [Their leverage point]                                   │
├─────────────────────────────────────────────────────────────┤
│ RECOMMENDED SEQUENCE                                        │
│ 1. 🔴 [Critical clause first]                              │
│ 2. 🟠 [High clause second]                                 │
├─────────────────────────────────────────────────────────────┤
│ POTENTIAL TRADE-OFFS                                        │
│ • Give 🔵 [Moderate item] → Get 🔴 [Critical item]         │
└─────────────────────────────────────────────────────────────┘
```

### Negotiation Guide

Used in: Report 2

```
┌─────────────────────────────────────────────────────────────┐
│ NEGOTIATION GUIDE                                           │
├─────────────────────────────────────────────────────────────┤
│ TALKING POINTS                                              │
│ 🔴 [Clause] ([Section])                                    │
│    • [Key argument]                                        │
├─────────────────────────────────────────────────────────────┤
│ CONCESSION STRATEGY                                         │
│ ┌────────────────────────┬────────────────────────┐        │
│ │ GIVE                   │ GET                    │        │
│ ├────────────────────────┼────────────────────────┤        │
│ │ 🔵 [Moderate item]     │ 🔴 [Critical item]     │        │
│ └────────────────────────┴────────────────────────┘        │
├─────────────────────────────────────────────────────────────┤
│ WALK-AWAY TRIGGERS                                          │
│ • 🔴 [Dealbreaker condition]                               │
└─────────────────────────────────────────────────────────────┘
```

### Implementation Notes

Used in: Report 2

```
┌─────────────────────────────────────────────────────────────┐
│ IMPLEMENTATION NOTES                                        │
├─────────────────────────────────────────────────────────────┤
│ SEQUENCING                                                  │
│ 1. 🔴 [Section] - [Why first]                              │
│ 2. 🟠 [Section] - [Dependency note]                        │
├─────────────────────────────────────────────────────────────┤
│ DEPENDENCIES                                                │
│ • [Section] ← requires [Other section] first               │
├─────────────────────────────────────────────────────────────┤
│ NOTES                                                       │
│ • [Special considerations]                                 │
└─────────────────────────────────────────────────────────────┘
```

### Disclaimers

Used in: All reports

```
┌─────────────────────────────────────────────────────────────┐
│ DISCLAIMER                                                  │
├─────────────────────────────────────────────────────────────┤
│ Risk Advisory: This report applies generally accepted       │
│ contract risk categories and contract management best       │
│ practices. Stakeholders must use this analysis to make      │
│ informed business decisions regarding risk acceptance and   │
│ mitigation. Failure to address identified risks may result  │
│ in material financial, operational, or legal exposure.      │
│                                                             │
│ Legal: This analysis is for informational purposes only and │
│ does not constitute legal advice. Consult qualified legal   │
│ counsel before making decisions based on this report.       │
│                                                             │
│ AI-Generated: This report was generated with AI assistance. │
│ All findings should be verified against source documents.   │
│                                                             │
│ Confidential: This document contains confidential analysis. │
│ Do not distribute without authorization.                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Redline Notation

| Change Type | Markdown | .docx Format |
|-------------|----------|--------------|
| Deletion | `~~text~~` | Red #FF0000 strikethrough |
| Addition | `**text**` | Green #00B050 bold |
| New section | `**[NEW]**` prefix | Green bold |
| Deleted section | `~~[DELETED]~~` prefix | Red strikethrough |

Example: `The cure period shall be ~~fifteen (15)~~ **thirty (30)** calendar days.`

---

## Visual Specifications

### Risk Level Colors

| Risk Level | Symbol | Hex Color |
|------------|--------|-----------|
| CRITICAL | 🔴 | #C00000 |
| HIGH | 🟠 | #ED7D31 |
| MODERATE | 🔵 | #2E75B6 |
| LOW | 🟢 | #00B050 |

### Delta Symbols

| Symbol | Meaning |
|--------|---------|
| ▲ | Risk increased |
| ▼ | Risk decreased |
| ● | No change |

### Document Styling

| Element | Value |
|---------|-------|
| Header background | Navy #1F4E79 |
| Header text | White #FFFFFF |
| Body font | Arial |
| Margins | 0.75" |

---

## Clause Type Taxonomy

### Detection Keywords

| Clause Type | Keywords |
|-------------|----------|
| Indemnification | indemnify, hold harmless, defend |
| Limitation of Liability | limitation, liability cap, consequential, damages |
| IP/Work Ownership | intellectual property, work product, ownership, license |
| Termination | termination, cancel, cure period, breach |
| Insurance | insurance, coverage, policy, certificate |
| Vendor Displacement | transition, displacement, incumbent, handover |
| Non-Solicitation | non-solicit, non-compete, hiring, recruit |
| Confidentiality | confidential, NDA, proprietary, disclose |
| Payment/Fees | payment, fees, invoice, net, billing |
| Warranties | warrant, represent, guarantee, covenant |
| Force Majeure | force majeure, act of god, pandemic |
| Governing Law | governing law, jurisdiction, venue, choice of law |

---

## Database Storage

Reports saved to SQLite on finalization.

See `references/database-schema.md` for full schema.

**Tables:**
- `reports` - Core metadata, versioned
- `report_findings` - Queryable findings per clause
- `report_deltas` - Version comparison deltas

---

## File Output

**Naming convention:**
```
[ContractName]_[ReportType]_[Date].docx
```

Examples:
- `MSA_Risk_Review_20251129.docx`
- `MSA_Redlines_20251129.docx`
- `MSA_V1_to_V2_Comparison_20251129.docx`

**Output location:**
```
/mnt/user-data/outputs/
```

---

## References

- `references/clause-taxonomy.md` - Full keyword lists and classification rules
- `references/database-schema.md` - SQLite schema with versioning
- `references/color-specs.md` - Hex codes and styling details

## Scripts

- `scripts/extract_clauses.py` - Clause detection and classification
- `scripts/generate_risk_review.py` - Report 1 generation
- `scripts/generate_redline.py` - Report 2 generation
- `scripts/generate_comparison.py` - Report 3 generation
