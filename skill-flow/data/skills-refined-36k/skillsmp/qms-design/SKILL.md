---
name: qms-design
description: Design QMS features following MRM-centric architecture. Use when the user asks to "design QMS feature", "build compliance feature", "create MRM section", or needs to ensure features align with ISO 9001 requirements and Management Review Meeting workflows.
---

# QMS Design Skill

Design Quality Management System features that align with ISO 9001 requirements and follow MRM (Management Review Meeting) agenda flow - the approach that consultants like Sirius have proven makes compliance "seamless and engaging."

## When to Use

- Designing new QMS-related features
- Adding sections to the QMS dashboard
- Creating compliance tracking functionality
- Building audit preparation features
- Ensuring features meet real audit workflows

## Design Principles

### 1. MRM-Centric, Not Document-Centric

**Wrong approach:**
```
├── Documents
├── Folders
├── Categories
└── Search
```

**Right approach (22-item MRM agenda from Sirius Playbook):**
```
├── 1. Actions (central register - everything flows here)
├── 2. Objectives
├── 3. Interested Parties
├── 4. Legal Compliance
├── 5. Risk & Opportunities
├── 6. SWOT Analysis
├── 7. Human Resources
├── 8. Roles & Responsibilities
├── 9. Training & Competence
├── 10. Approved Suppliers (Quality/Delivery/Cost scorecard)
├── 11. Communications
├── 12. Process Performance (KPIs)
├── 13. Internal Audits (Schedule + Tracker by clause)
├── 14. Non-conformances (NCR register with CAPA)
├── 15. External Audit Points
├── 16. QMS Changes (with rollback plans)
├── 17. Improvement
├── 18. Business Continuity
├── 19. Document Control
├── 20. Safety Actions
├── 21. Assets (Maintenance + Calibration)
└── 22. AOB
```

### 2. Status at a Glance

Every section should immediately answer: "Is this area healthy?"

| Status | Meaning | Visual |
|--------|---------|--------|
| Green | On track, no attention needed | ✓ |
| Amber | Needs review, approaching deadline | ⚠ |
| Red | Requires immediate action | ✗ |

### 3. Drill-Down Capability

Every summary links to evidence. Auditors will click through.

```
Summary View → Detail List → Individual Record → Source Document
```

### 4. Cross-References

QMS elements interconnect. Design relationships:

```
NCR → triggers → Action
Metric decline → links to → Objective
Audit finding → creates → NCR
Customer complaint → maps to → Supplier
```

### 5. Audit Trail Built-In

Every interaction must capture:
- **What** was done
- **Who** did it
- **When** it happened
- **Why** (context/notes)

## Feature Design Template

When designing a QMS feature, work through:

### Step 1: Identify ISO Clause
```markdown
## Feature: [Name]

### ISO 9001:2015 Clause
- Primary: [Clause number and title]
- Related: [Related clauses]

### Requirement Summary
[What the standard requires in plain language]
```

### Step 2: Define MRM Position
```markdown
### MRM Agenda Position
- Comes after: [Previous section]
- Comes before: [Next section]
- Why this position: [Logical reason]
```

### Step 3: Define Data Model
```markdown
### Required Data Fields
| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| ... | ... | Y/N | ... |

### Relationships
- Links to: [Related tables]
- Referenced by: [What uses this data]
```

### Step 4: Define Status Logic
```markdown
### Status Calculation
- Green when: [Conditions]
- Amber when: [Conditions]
- Red when: [Conditions]
```

### Step 5: Define Evidence Trail
```markdown
### Audit Evidence Requirements
- What auditors ask: [Typical questions]
- Evidence needed: [What to show]
- Drill-down path: [How to get to detail]
```

### Step 6: Define User Interactions
```markdown
### Key User Actions
1. [Action]: [What happens]
2. [Action]: [What happens]

### MRM Review Flow
[How this section is reviewed in an MRM]
```

## Common QMS Features

### Actions Tracker
**Clause:** 9.3.3 (MRM outputs), 10.2 (Corrective action)
**Purpose:** Track all actions from MRMs, audits, NCRs
**Key fields:** Description, Owner, Due date, Source, Status, Evidence

### Quality Metrics Dashboard
**Clause:** 9.1.3 (Analysis and evaluation)
**Purpose:** Track KPIs like defect rate, OTD, customer satisfaction
**Key fields:** Metric name, Target, Actual, Trend, Period

### Supplier Register
**Clause:** 8.4 (External providers)
**Purpose:** Manage approved suppliers and evaluations
**Key fields:** Supplier name, Category, Status, Last evaluation, Performance score

### Document Control
**Clause:** 7.5 (Documented information)
**Purpose:** Control QMS documents with version tracking
**Key fields:** Document title, Version, Author, Approved by, Review date

### NCR Register
**Clause:** 10.2 (Nonconformity)
**Purpose:** Track nonconformities and corrective actions
**Key fields:** Description, Source, Root cause, Correction, Corrective action, Verification

### Internal Audit Schedule
**Clause:** 9.2 (Internal audit)
**Purpose:** Plan and track internal audits
**Key fields:** Audit area, Auditor, Scheduled date, Status, Findings

## Integration Checklist

Before completing a QMS feature design, verify:

- [ ] Maps to specific ISO 9001:2015 clause(s)
- [ ] Has clear position in MRM agenda flow
- [ ] Shows status at a glance (green/amber/red)
- [ ] Links to related QMS sections
- [ ] Supports drill-down to evidence
- [ ] Captures full audit trail (who, what, when)
- [ ] Uses correct ISO terminology
- [ ] Can answer typical auditor questions

## Output Format

```markdown
## QMS Feature Design: [Feature Name]

### ISO Alignment
- **Primary Clause:** ISO 9001:2015 X.X - [Title]
- **Related Clauses:** X.X, X.X

### MRM Integration
- **Position:** After [X], Before [Y]
- **Status Indicators:** [How green/amber/red calculated]
- **Review Flow:** [How reviewed in MRM]

### Data Model
[Entity diagram or table structure]

### User Interface
[Key screens/components]

### Audit Evidence
- **Questions addressed:** [What auditors ask]
- **Evidence provided:** [What system shows]
- **Drill-down path:** [How to get detail]

### Cross-References
- Links to: [Related features]
- Triggered by: [What creates records here]
- Triggers: [What this creates elsewhere]
```

## Reference Documentation

- `docs/customer-research/sirius-mrm-playbook-analysis.md` - Complete breakdown of 31 playbook sheets
- `docs/customer-research/mrm-database-mapping.md` - Table-by-table mapping with SQL definitions
- `docs/customer-research/qms-feature-requirements.md` - Feature requirements from Sirius

## Related Agents

- `mrm-specialist` - MRM workflow design expertise
- `sirius-tester` - Test from Sirius consultant perspective
- `auditor-simulator` - Test audit readiness
