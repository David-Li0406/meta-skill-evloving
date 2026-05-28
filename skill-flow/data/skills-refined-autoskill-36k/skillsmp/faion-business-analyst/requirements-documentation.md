---
id: requirements-documentation
name: "Requirements Documentation"
domain: BA
skill: faion-business-analyst
category: "business-analysis"
---

# Requirements Documentation

## Metadata
- **Category:** BA Framework / Requirements Analysis and Design Definition
- **Difficulty:** Intermediate
- **Tags:** #methodology #babok #requirements #documentation #business-analysis
- **Agent:** faion-ba-agent

---

## Problem

Requirements exist only in people's heads. Different team members have different understanding. Developers build the wrong thing because requirements were unclear. Testing cannot verify because there is nothing to test against. Changes cannot be tracked because there is no baseline.

Without documentation:
- Ambiguous requirements
- Misunderstandings between teams
- No basis for testing
- Change control impossible

---

## Framework

### Requirements Hierarchy

```
Business Requirements
    ↓
Stakeholder Requirements
    ↓
Solution Requirements
    ├── Functional Requirements
    └── Non-Functional Requirements
```

| Level | Purpose | Example |
|-------|---------|---------|
| **Business** | Why are we doing this? | Increase revenue by 20% |
| **Stakeholder** | What do users need? | Sales reps need to create quotes faster |
| **Functional** | What should system do? | System shall calculate quote total |
| **Non-Functional** | How should system perform? | Page loads in < 2 seconds |

### Step 1: Choose Documentation Format

| Format | Best For | Tools |
|--------|----------|-------|
| **Text document** | Traditional, detailed | Word, Confluence |
| **User stories** | Agile, iterative | Jira, Azure DevOps |
| **Use cases** | Interactions, flows | Word, draw.io |
| **Models** | Complex processes | Visio, Lucidchart |

### Step 2: Write Clear Requirements

**Good requirement characteristics (SMART):**

| Attribute | Description | Test |
|-----------|-------------|------|
| **Specific** | Clear, unambiguous | Only one interpretation |
| **Measurable** | Can verify completion | Testable |
| **Achievable** | Technically feasible | Can be built |
| **Relevant** | Traces to business need | Has clear purpose |
| **Time-bound** | Has timeline context | Delivery prioritized |

**Writing tips:**
- Use active voice ("System shall..." not "It should be...")
- One requirement per statement
- Avoid subjective terms (fast, user-friendly, easy)
- Include acceptance criteria

### Step 3: Document Functional Requirements

**Template:**
```markdown
**REQ-XXX:** [Requirement Name]

**Description:** The system shall [action] when [trigger].

**Rationale:** [Why this is needed]

**Source:** [Stakeholder or document]

**Priority:** [Must/Should/Could/Won't]

**Acceptance Criteria:**
1. Given [context], when [action], then [outcome]
2. Given [context], when [action], then [outcome]
```

### Step 4: Document Non-Functional Requirements

| Category | Examples |
|----------|----------|
| **Performance** | Response time, throughput |
| **Scalability** | User capacity, data volume |
| **Security** | Authentication, authorization |
| **Usability** | Ease of use, accessibility |
| **Reliability** | Uptime, error handling |
| **Compatibility** | Browsers, devices |

### Step 5: Organize and Structure

```markdown
1. Introduction
   1.1 Purpose
   1.2 Scope
   1.3 Definitions

2. Business Requirements
   2.1 Business objectives
   2.2 Success metrics

3. Stakeholder Requirements
   3.1 User types
   3.2 User needs

4. Solution Requirements
   4.1 Functional requirements
       4.1.1 Feature A
       4.1.2 Feature B
   4.2 Non-functional requirements
       4.2.1 Performance
       4.2.2 Security

5. Constraints and Assumptions
6. Appendices
```

---

## Templates

### Business Requirements Document (BRD)

```markdown
# Business Requirements Document: [Project Name]

**Version:** [X.X]
**Date:** [Date]
**Author:** [Name]
**Status:** [Draft/Review/Approved]

## 1. Executive Summary
[Brief overview of the initiative]

## 2. Business Context

### 2.1 Current State
[Description of current situation]

### 2.2 Problem Statement
[What problem we are solving]

### 2.3 Business Objectives
| Objective | Measure | Target |
|-----------|---------|--------|
| [Objective] | [KPI] | [Target] |

## 3. Scope

### 3.1 In Scope
- [Item 1]
- [Item 2]

### 3.2 Out of Scope
- [Exclusion 1]
- [Exclusion 2]

## 4. Stakeholders
| Stakeholder | Role | Interest |
|-------------|------|----------|
| [Name/Group] | [Role] | [What they need] |

## 5. Business Requirements

| ID | Requirement | Priority | Source |
|----|-------------|----------|--------|
| BR-01 | [Requirement] | Must | [Source] |
| BR-02 | [Requirement] | Should | [Source] |

## 6. Constraints
- [Constraint 1]
- [Constraint 2]

## 7. Assumptions
- [Assumption 1]
- [Assumption 2]

## 8. Dependencies
- [Dependency 1]
- [Dependency 2]

## Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Sponsor | | | |
| Business Owner | | | |
```

### User Story Template

```markdown
**Story ID:** US-[XXX]
**Title:** [Short title]
**Epic:** [Parent epic]

## User Story
**As a** [user type]
**I want** [capability]
**So that** [benefit]

## Acceptance Criteria

**Scenario 1: [Name]**
- **Given** [precondition]
- **When** [action]
- **Then** [expected result]

**Scenario 2: [Name]**
- **Given** [precondition]
- **When** [action]
- **Then** [expected result]

## Additional Information
- **Priority:** [Must/Should/Could]
- **Estimate:** [Story points]
- **Dependencies:** [Related stories]
- **Notes:** [Additional context]
```

---

## Examples

### Example 1: Functional Requirement

**REQ-101: Quote Total Calculation**

**Description:** The system shall calculate the total quote amount by summing all line item amounts plus applicable taxes.

**Rationale:** Sales reps need accurate totals to provide quotes to customers.

**Source:** Sales Manager (Interview 2026-01-10)

**Priority:** Must

**Acceptance Criteria:**
1. Given a quote with multiple line items, when user clicks "Calculate", then total equals sum of all line amounts
2. Given applicable tax rate of 8%, when total is calculated, then tax amount equals total x 0.08
3. Given no line items, when user clicks "Calculate", then total displays as $0.00

### Example 2: Non-Functional Requirement

**NFR-015: Page Load Performance**

**Description:** All application pages shall load within 2 seconds under normal load conditions.

**Measure:** Time from user click to page fully rendered

**Target:** 95th percentile < 2 seconds

**Conditions:**
- Normal load: Up to 500 concurrent users
- Network: Standard corporate LAN

**Verification:** Load testing with 500 virtual users

---

## Common Mistakes

1. **Vague requirements** - "System should be fast"
2. **No acceptance criteria** - Cannot verify completion
3. **Implementation in requirements** - Specifying how, not what
4. **Missing non-functional** - Only documenting features
5. **No traceability** - Cannot link to business need

---

## Quality Checklist

Before finalizing requirements:

- [ ] Each requirement has unique ID
- [ ] Requirements are testable
- [ ] No ambiguous terms (fast, easy, user-friendly)
- [ ] Acceptance criteria defined
- [ ] Priority assigned
- [ ] Source documented
- [ ] No conflicts between requirements
- [ ] Traces to business objective
- [ ] Reviewed by stakeholders

---

## Next Steps

After documentation:
1. Review with stakeholders
2. Resolve conflicts and gaps
3. Get sign-off
4. Baseline requirements
5. Connect to Requirements Traceability methodology

---

## References

- BA Framework Guide v3 - Requirements Analysis and Design Definition
- BA industry Requirements Documentation Standards
