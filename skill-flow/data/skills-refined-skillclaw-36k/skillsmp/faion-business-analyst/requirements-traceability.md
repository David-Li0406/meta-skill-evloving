---
id: requirements-traceability
name: "Requirements Traceability"
domain: BA
skill: faion-business-analyst
category: "business-analysis"
---

# Requirements Traceability

## Metadata
- **Category:** BA Framework / Requirements Analysis and Design Definition
- **Difficulty:** Intermediate
- **Tags:** #methodology #babok #traceability #requirements #business-analysis
- **Agent:** faion-ba-agent

---

## Problem

A business goal changes, and nobody knows which requirements are affected. Testing misses critical functionality because coverage is unclear. Developers ask why a requirement exists, and nobody can explain. At the end, stakeholders question if their needs were addressed.

Without traceability:
- Impact of changes unknown
- Test coverage gaps
- Requirements without justification
- No verification of completeness

---

## Framework

### What is Traceability?

Traceability links requirements to their origins and to downstream artifacts. It answers:
- Where did this requirement come from?
- What does this requirement affect?
- Is every business need covered?
- Is every component justified?

### Traceability Directions

```
Business Need → Stakeholder Requirement → Solution Requirement → Design → Code → Test
      ↑                    ↑                      ↑                ↑        ↑       ↑
      └──────────────────────────────────────────────────────────────────────────────┘
                              Bi-directional traceability
```

| Direction | Purpose |
|-----------|---------|
| **Forward** | From need to implementation (coverage) |
| **Backward** | From implementation to need (justification) |

### Step 1: Define Traceability Strategy

Determine what to trace:

| Level | Typical Links |
|-------|---------------|
| **Minimum** | Business req → Functional req |
| **Standard** | + Design → Test |
| **Full** | + Code → User story → Epic |

### Step 2: Create Traceability Matrix

Map relationships between artifacts:

| Business Req | Stakeholder Req | Solution Req | Design | Test |
|--------------|-----------------|--------------|--------|------|
| BR-01 | SR-01, SR-02 | REQ-101, REQ-102 | DES-01 | TC-01, TC-02 |
| BR-02 | SR-03 | REQ-103, REQ-104, REQ-105 | DES-02 | TC-03 |

### Step 3: Maintain Traceability

Update when changes occur:
- New requirement added → Link to parent
- Requirement changed → Check downstream
- Requirement deleted → Update all links
- Test created → Link to requirement

### Step 4: Analyze Traceability

**Coverage analysis:**
- Are all business requirements traced to solution requirements?
- Are all solution requirements traced to tests?
- Are there orphan requirements (no parent)?

**Gap analysis:**
- Business requirements without solution requirements = Gap
- Solution requirements without tests = Testing gap
- Tests without requirements = Possible gold plating

---

## Templates

### Requirements Traceability Matrix (RTM)

```markdown
# Requirements Traceability Matrix: [Project Name]

**Version:** [X.X]
**Date:** [Date]
**Author:** [Name]

## Traceability Links

| Bus Req ID | Bus Req Name | Stkhldr Req | Func Req | Design | Test Case | Status |
|------------|--------------|-------------|----------|--------|-----------|--------|
| BR-01 | [Name] | SR-01 | FR-01, FR-02 | D-01 | TC-01 | Complete |
| BR-02 | [Name] | SR-02 | FR-03 | D-02 | TC-02, TC-03 | In Progress |
| BR-03 | [Name] | SR-03, SR-04 | FR-04 | - | - | Not Started |

## Coverage Summary

| Level | Total | Linked | Not Linked | Coverage |
|-------|-------|--------|------------|----------|
| Business Requirements | 10 | 10 | 0 | 100% |
| Solution Requirements | 25 | 23 | 2 | 92% |
| Test Cases | 40 | 38 | 2 | 95% |

## Orphan Requirements
Requirements with no upstream link:
- FR-24: [Description] - needs linking to stakeholder requirement
- FR-25: [Description] - needs justification

## Gaps
Business requirements without full coverage:
- BR-08: Missing test cases
- BR-09: No design document
```

### Simple Traceability Table

```markdown
# Requirement Traceability: [Requirement ID]

**Requirement:** [REQ-XXX]
**Description:** [Description]

## Upstream Trace (Where it came from)
| Type | ID | Description |
|------|-----|-------------|
| Business Requirement | BR-01 | [Description] |
| Stakeholder Requirement | SR-02 | [Description] |

## Downstream Trace (What it affects)
| Type | ID | Description | Status |
|------|-----|-------------|--------|
| Design | D-05 | [Description] | Complete |
| Code Module | M-12 | [Description] | In Progress |
| Test Case | TC-15 | [Description] | Not Started |
| Test Case | TC-16 | [Description] | Not Started |

## Change History
| Date | Change | Impact |
|------|--------|--------|
| [Date] | [Change description] | [Affected artifacts] |
```

---

## Examples

### Example 1: E-commerce Checkout Traceability

**Business Requirement:** BR-05 - Enable customers to complete purchases online

**Trace:**
```
BR-05: Online purchase capability
  └── SR-12: Customer can checkout cart
        ├── FR-30: Display cart summary
        │     ├── D-15: Cart component design
        │     └── TC-45: Verify cart displays correctly
        ├── FR-31: Accept payment information
        │     ├── D-16: Payment form design
        │     └── TC-46: Verify payment entry
        └── FR-32: Confirm order
              ├── D-17: Confirmation page design
              └── TC-47: Verify order confirmation
```

### Example 2: Impact Analysis Using Traceability

**Scenario:** Business requirement BR-03 is changing.

**Impact analysis:**

| Artifact Type | Affected Items | Impact |
|---------------|----------------|--------|
| Stakeholder Requirements | SR-05, SR-06 | Needs review |
| Solution Requirements | FR-10, FR-11, FR-12 | May need update |
| Design Documents | D-08, D-09 | Needs revision |
| Test Cases | TC-20, TC-21, TC-22 | Needs update |

**Effort estimate:** 3 requirements, 2 designs, 3 test cases = ~16 hours

---

## Common Mistakes

1. **Not maintaining** - Matrix becomes outdated
2. **Too granular** - Tracing every detail
3. **Too sparse** - Missing important links
4. **No tooling** - Manual tracking breaks down
5. **One-time exercise** - Not updating with changes

---

## Traceability Benefits

| Benefit | How |
|---------|-----|
| **Impact analysis** | Know what changes affect |
| **Coverage verification** | Ensure nothing missed |
| **Justification** | Every artifact has purpose |
| **Audit trail** | Track requirement evolution |
| **Test planning** | Know what to test |

---

## Tools for Traceability

| Tool Type | Examples |
|-----------|----------|
| **Requirements Management** | Jira, Azure DevOps, Jama |
| **Spreadsheets** | Excel, Google Sheets |
| **Documents** | Word, Confluence |
| **Specialized** | IBM DOORS, Polarion |

**Tool selection factors:**
- Team size
- Project complexity
- Integration needs
- Budget

---

## Traceability Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Forward coverage | (Linked req / Total req) x 100 | > 95% |
| Backward coverage | (Justified items / Total items) x 100 | 100% |
| Test coverage | (Req with tests / Total req) x 100 | > 90% |
| Orphan count | Items with no links | 0 |

---

## Next Steps

After establishing traceability:
1. Set up traceability tool/template
2. Define maintenance process
3. Integrate with change control
4. Generate coverage reports
5. Connect to Strategy Analysis methodology

---

## References

- BA Framework Guide v3 - Requirements Analysis and Design Definition
- BA industry Requirements Traceability Guidelines
