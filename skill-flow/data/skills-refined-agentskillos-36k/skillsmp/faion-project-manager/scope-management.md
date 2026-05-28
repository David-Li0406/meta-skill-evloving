---
id: scope-management
name: "Scope Management"
domain: PM
skill: faion-project-manager
category: "project-management"
---

# Scope Management

## Metadata
- **Category:** Project Management Framework / Planning Performance Domain
- **Difficulty:** Intermediate
- **Tags:** #methodology #pmbok #scope #requirements #project-management
- **Agent:** faion-pm-agent

---

## Problem

The project delivers something different from what stakeholders expected. Features are added without impact assessment. Requirements are vague and interpreted differently. At the end, everyone argues about what was supposed to be built. Scope creep consumes budget and schedule.

Without scope management:
- Unclear deliverables
- Uncontrolled changes
- Misaligned expectations
- Budget and schedule overruns

---

## Framework

### Scope Concepts

| Term | Definition |
|------|------------|
| **Product Scope** | Features and functions of the product |
| **Project Scope** | Work required to deliver the product |
| **Scope Baseline** | Approved scope statement + WBS + WBS dictionary |
| **Scope Creep** | Uncontrolled expansion without formal approval |

### Step 1: Collect Requirements

Gather stakeholder needs:

**Techniques:**
- Interviews
- Workshops
- Questionnaires
- Document analysis
- Observation
- Prototyping

**Requirement types:**

| Type | Description | Example |
|------|-------------|---------|
| **Business** | Why the project exists | Increase revenue 20% |
| **Stakeholder** | What stakeholders need | Dashboard for executives |
| **Solution** | Functional capabilities | System calculates totals |
| **Transition** | Moving to new solution | Data migration, training |

### Step 2: Define Scope

Create the scope statement:

```markdown
## Project Scope Statement

### Project Objectives
[Measurable goals]

### Product Scope Description
[What will be delivered]

### Deliverables
- [Deliverable 1]
- [Deliverable 2]

### Acceptance Criteria
[How completion is verified]

### Exclusions
[What is NOT included]

### Constraints
[Limitations on the project]

### Assumptions
[Conditions assumed true]
```

### Step 3: Create WBS

Break scope into manageable pieces (see Work Breakdown Structure).

### Step 4: Validate Scope

Get formal acceptance of deliverables:

| Deliverable | Criteria | Reviewed By | Status | Date |
|-------------|----------|-------------|--------|------|
| [Deliverable] | [Criteria] | [Name] | Accepted | [Date] |

### Step 5: Control Scope

Manage changes through change control (see Change Control).

**Scope control activities:**
- Monitor scope baseline
- Evaluate change requests
- Update scope documents
- Communicate changes

---

## Templates

### Requirements Documentation Template

```markdown
# Requirements Document: [Project Name]

**Version:** [X.X]
**Date:** [Date]
**Author:** [Name]

## 1. Business Requirements

| ID | Requirement | Priority | Source |
|----|-------------|----------|--------|
| BR-01 | [Requirement] | Must/Should/Could | [Stakeholder] |
| BR-02 | [Requirement] | Must/Should/Could | [Stakeholder] |

## 2. Stakeholder Requirements

| ID | Stakeholder | Requirement | Priority |
|----|-------------|-------------|----------|
| SR-01 | [Stakeholder] | [Need] | Must/Should/Could |
| SR-02 | [Stakeholder] | [Need] | Must/Should/Could |

## 3. Functional Requirements

| ID | Feature | Description | Acceptance Criteria |
|----|---------|-------------|---------------------|
| FR-01 | [Feature] | [Description] | [Criteria] |
| FR-02 | [Feature] | [Description] | [Criteria] |

## 4. Non-Functional Requirements

| ID | Category | Requirement | Measure |
|----|----------|-------------|---------|
| NFR-01 | Performance | [Requirement] | [Metric] |
| NFR-02 | Security | [Requirement] | [Metric] |
| NFR-03 | Usability | [Requirement] | [Metric] |

## 5. Constraints
- [Constraint 1]
- [Constraint 2]

## 6. Assumptions
- [Assumption 1]
- [Assumption 2]

## 7. Dependencies
- [Dependency 1]
- [Dependency 2]
```

### Scope Statement Template

```markdown
# Project Scope Statement: [Project Name]

**Version:** [X.X]
**Date:** [Date]
**Project Manager:** [Name]
**Approved By:** [Name]

## 1. Project Objectives
[What the project aims to achieve - measurable]

## 2. Product Scope Description
[Detailed description of the product/service]

## 3. Deliverables

| ID | Deliverable | Description | Acceptance Criteria |
|----|-------------|-------------|---------------------|
| D1 | [Name] | [Description] | [How verified] |
| D2 | [Name] | [Description] | [How verified] |

## 4. Project Boundaries

### In Scope
- [Item 1]
- [Item 2]

### Out of Scope
- [Exclusion 1]
- [Exclusion 2]

## 5. Constraints
- Budget: $[X]
- Timeline: [X months]
- Resources: [Limits]
- Technology: [Constraints]

## 6. Assumptions
- [Assumption 1]
- [Assumption 2]

## 7. Risks Related to Scope
- [Risk 1]
- [Risk 2]

## Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Project Sponsor | | | |
| Project Manager | | | |
```

---

## Examples

### Example 1: Website Redesign Scope

**In Scope:**
- Redesign of 20 main pages
- Mobile responsive design
- Content migration (existing content)
- Basic SEO optimization
- Analytics integration

**Out of Scope:**
- E-commerce functionality
- New content creation
- Marketing campaigns
- Social media integration
- Third-party system integrations

**Constraints:**
- Budget: $50,000
- Timeline: 3 months
- Must use existing hosting

### Example 2: Mobile App MVP Scope

**Product Scope:**
- User registration and login
- Profile management
- Core feature X
- Push notifications
- Basic analytics

**Explicitly Excluded:**
- Social features
- Offline mode
- Tablet optimization
- Localization
- Premium features

---

## Common Mistakes

1. **Vague scope** - "Make it better" is not scope
2. **No exclusions** - Everything seems in scope
3. **Verbal agreements** - Undocumented promises
4. **Gold plating** - Adding unrequested features
5. **No baseline** - Cannot measure changes

---

## Scope Creep Prevention

| Technique | Description |
|-----------|-------------|
| **Clear documentation** | Written scope statement |
| **Change control** | Formal process for changes |
| **Stakeholder sign-off** | Agreement on scope |
| **Regular reviews** | Monitor scope baseline |
| **Say no** | Reject out-of-scope requests |

**How to say no professionally:**
1. Acknowledge the request
2. Explain scope constraints
3. Offer alternatives (future phase, separate project)
4. Document the decision

---

## Requirements Traceability

Track requirements from origin to delivery:

| Req ID | Source | Design | Build | Test | Status |
|--------|--------|--------|-------|------|--------|
| FR-01 | [Stakeholder] | [Design ref] | [Code ref] | [Test ref] | Done |
| FR-02 | [Stakeholder] | [Design ref] | [Code ref] | [Test ref] | In Progress |

Benefits:
- Ensures all requirements are addressed
- Tracks impact of changes
- Verifies coverage in testing
- Supports acceptance decisions

---

## Next Steps

After scope definition:
1. Get stakeholder sign-off
2. Baseline the scope
3. Create WBS from scope
4. Establish change control
5. Connect to Performance Domains Overview methodology

---

## References

- Project Management Framework Guide 7th Edition - Planning Performance Domain
- PM industry practice standard for Project Scope Management
