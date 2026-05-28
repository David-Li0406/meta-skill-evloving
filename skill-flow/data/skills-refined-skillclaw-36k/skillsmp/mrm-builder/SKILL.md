---
name: mrm-builder
description: Build Management Review Meeting structures, agendas, and workflows. Use when the user asks to "build MRM", "create review agenda", "design MRM flow", "management review structure", or needs to implement MRM-related features.
---

# MRM Builder Skill

Build Management Review Meeting (MRM) structures that make compliance reviews "seamless and engaging" - following the proven methodology from Sirius consultants that BSI rated "exceptional."

## When to Use

- Designing MRM dashboard sections
- Creating MRM agenda generators
- Building MRM workflow features
- Implementing MRM reporting
- Structuring QMS review processes

## MRM Fundamentals

### What is an MRM?

Management Review Meetings are required by ISO 9001:2015 clause 9.3. Top management must review the QMS at planned intervals to ensure its continuing suitability, adequacy, effectiveness, and alignment with strategic direction.

### Why MRM-Centric Design?

From Sirius: "By being in this kind of tab format where it goes through each of these elements in a systematic order... it just makes that MRM a seamless process. It engages therefore the people in it and therefore it engages people in the quality management system as a whole."

**Key insight:** Structure the platform around MRM flow, not document storage.

## MRM Agenda Structure

### Required Inputs (ISO 9001:2015 9.3.2)

The standard requires these inputs to be reviewed:

| Input | Description | Platform Section |
|-------|-------------|------------------|
| a) Status of previous actions | Actions from last MRM | Actions tracker |
| b) Changes in external/internal issues | Context changes | Context/Changes |
| c.1) Customer satisfaction | Feedback and satisfaction | Customer Feedback |
| c.2) Quality objectives | Progress against objectives | Objectives |
| c.3) Process performance | Metrics and KPIs | Quality Metrics |
| c.4) Nonconformities | NCRs and corrective actions | NCR Register |
| c.5) Monitoring results | Audit and inspection results | Internal Audit |
| c.6) Audit results | Internal and external | Audit Results |
| c.7) External provider performance | Supplier metrics | Suppliers |
| d) Adequacy of resources | Resource constraints | Resources |
| e) Risk/opportunity actions | Risk treatment status | Risk Register |
| f) Improvement opportunities | CI suggestions | Improvements |

### Required Outputs (ISO 9001:2015 9.3.3)

MRM must produce decisions/actions related to:
- Improvement opportunities
- Need for changes to QMS
- Resource needs

### Complete Agenda Order (22 Items)

Based on Sirius MRM Playbook (BSI-rated "exceptional"):

```
1. Actions               - Central register - everything flows here
2. Objectives            - Quality objectives review
3. Interested Parties    - Stakeholder requirements (4.2)
4. Legal Compliance      - Regulatory compliance register
5. Risk & Opportunities  - Risk register review (6.1)
6. SWOT Analysis         - Strategic context
7. Human Resources       - QMS resource planner
8. Roles & Responsibilities - Organizational structure (5.3)
9. Training & Competence - Skills matrix review (7.2)
10. Approved Suppliers   - Supplier scorecard (Quality/Delivery/Cost)
11. Communications       - Communication plan matrix (7.4)
12. Process Performance  - KPIs and metrics (9.1.3)
13. Internal Audits      - Schedule + Tracker by clause (9.2)
14. Non-conformances     - NCR register with CAPA (10.2)
15. External Audit Points - BSI/certification body findings
16. QMS Changes          - Change management (6.3)
17. Improvement          - Continual improvement register (10.3)
18. Business Continuity  - BCP review
19. Document Control     - Documentation status (7.5)
20. Safety Actions       - H&S integration (45001)
21. Assets               - Maintenance + Calibration (7.1.5)
22. AOB                  - Any other business
```

## Building MRM Sections

### Section Template

For each MRM section, implement:

```typescript
interface MRMSection {
  id: string;
  name: string;
  isoClause: string;
  order: number;

  // Status calculation
  status: 'green' | 'amber' | 'red';
  statusReason: string;

  // Summary data
  summary: {
    totalItems: number;
    attentionRequired: number;
    trend: 'improving' | 'stable' | 'declining';
  };

  // Review tracking
  lastReviewed?: Date;
  reviewedBy?: string;

  // Links
  detailUrl: string;
  relatedSections: string[];
}
```

### Status Logic Examples

**Actions Section:**
```
Green: No overdue actions
Amber: Actions due within 7 days
Red: Overdue actions exist
```

**Quality Metrics:**
```
Green: All KPIs meeting targets
Amber: 1-2 KPIs below target
Red: 3+ KPIs below target OR critical KPI failed
```

**Supplier Performance:**
```
Green: All approved suppliers meeting criteria
Amber: 1-2 suppliers below threshold
Red: Critical supplier issue OR supplier removed
```

## MRM Agenda Generator

### Agenda Content Structure

```markdown
# Management Review Meeting Agenda

**Date:** [Scheduled date]
**Attendees:** [Required attendees]
**Previous MRM:** [Date of last MRM]

---

## 1. Actions from Previous MRM
- **Status:** [X] Open / [Y] Closed since last MRM
- **Overdue:** [Z] actions
- **Key items requiring discussion:**
  - [Action with context]

## 2. Business Objectives
- **Status:** [Overall status]
- **Progress highlights:**
  - [Objective]: [% complete]
- **Items requiring discussion:**
  - [Objective needing attention]

[Continue for each section...]

---

## Summary of Items Requiring Decision
1. [Item needing management decision]
2. [Resource request]
3. [Change proposal]

## Proposed Actions
1. [Suggested action from this MRM]
```

### Auto-Generation Logic

```typescript
interface MRMAgendaItem {
  section: string;
  status: 'green' | 'amber' | 'red';
  summary: string;
  itemsRequiringDiscussion: string[];
  suggestedActions: string[];
  dataPoints: {
    label: string;
    value: string | number;
    trend?: string;
  }[];
}

function generateAgenda(orgId: string): MRMAgenda {
  // Collect status from each section
  // Identify items needing attention
  // Suggest discussion points
  // Propose actions based on status
}
```

## MRM Review Flow

### During Review

Each section should support:

1. **Status overview** - Quick visual status
2. **Key metrics** - Important numbers
3. **Attention items** - What needs discussion
4. **Drill-down** - Click for details
5. **Add notes** - Capture discussion
6. **Record actions** - Create new actions
7. **Mark reviewed** - Timestamp completion

### Review Recording

```typescript
interface MRMReview {
  id: string;
  mrmDate: Date;
  attendees: string[];

  sectionReviews: {
    sectionId: string;
    reviewedAt: Date;
    reviewedBy: string;
    status: string;
    notes: string;
    actionsCreated: string[];
  }[];

  outputs: {
    improvements: string[];
    qmsChanges: string[];
    resourceNeeds: string[];
  };

  completedAt: Date;
}
```

## MRM Minutes Generation

After review, generate minutes:

```markdown
# Management Review Meeting Minutes

**Date:** [Date]
**Attendees:** [Names]
**Duration:** [Time]

---

## Sections Reviewed

### 1. Actions
- **Status at review:** [Status]
- **Key discussion:** [Notes]
- **Decisions:** [Decisions made]

[Continue for each section...]

---

## Meeting Outputs

### Improvement Opportunities Identified
1. [Improvement]

### QMS Changes Required
1. [Change]

### Resource Needs
1. [Resource request]

### Actions Assigned
| Action | Owner | Due Date |
|--------|-------|----------|
| ... | ... | ... |

---

**Next MRM:** [Scheduled date]
**Minutes prepared by:** [Name]
**Approved by:** [Name]
```

## Implementation Checklist

When building MRM features:

- [ ] All ISO 9001:2015 9.3.2 inputs represented
- [ ] Logical flow order (actions first, improvements last)
- [ ] Status indicators for each section
- [ ] Drill-down to detail from summary
- [ ] Cross-references between related sections
- [ ] Review timestamp capture
- [ ] Notes/discussion capture
- [ ] Action creation workflow
- [ ] Agenda generation
- [ ] Minutes generation
- [ ] Attendance tracking
- [ ] Historical MRM records

## Output Format

### MRM Section Design
```markdown
## MRM Section: [Name]

### Position & Flow
- **Order:** [Number in sequence]
- **Follows:** [Previous section]
- **Precedes:** [Next section]
- **Why this position:** [Logic]

### ISO Alignment
- **Clause:** 9.3.2 [letter]
- **Requirement:** [What standard requires]

### Status Logic
- **Green:** [Condition]
- **Amber:** [Condition]
- **Red:** [Condition]

### Summary Display
- [Metric 1]: [What to show]
- [Metric 2]: [What to show]

### Attention Triggers
- [Condition that highlights item]

### Cross-References
- Links to: [Related sections]
- Creates: [What actions/records]
```

## Reference Documentation

- `docs/customer-research/sirius-mrm-playbook-analysis.md` - Complete breakdown of 31 playbook sheets
- `docs/customer-research/mrm-database-mapping.md` - Table-by-table mapping with SQL definitions
- `docs/customer-research/qms-feature-requirements.md` - Feature requirements from Sirius

## Related Agents

- `mrm-specialist` - MRM workflow expertise
- `sirius-tester` - Test from Sirius consultant perspective
- `auditor-simulator` - Test MRM evidence
