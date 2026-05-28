---
id: stakeholder-analysis
name: "Stakeholder Analysis"
domain: BA
skill: faion-business-analyst
category: "business-analysis"
---

# Stakeholder Analysis

## Metadata
- **Category:** BA Framework / Business Analysis Planning and Monitoring
- **Difficulty:** Beginner
- **Tags:** #methodology #babok #stakeholders #analysis #business-analysis
- **Agent:** faion-ba-agent

---

## Problem

You gather requirements from the wrong people. Important perspectives are missed. Conflicting requirements arrive late without resolution. Some stakeholders feel ignored while others dominate. The solution does not meet the needs of those who will use it.

Without stakeholder analysis:
- Incomplete requirements
- Unresolved conflicts
- Resistance to change
- Failed adoption

---

## Framework

### Step 1: Identify Stakeholders

List all parties who:
- Are affected by the change
- Have influence over the change
- Need to approve the change
- Will implement the change
- Will use the solution

**Stakeholder categories:**

| Category | Role | Examples |
|----------|------|----------|
| **Customer** | External beneficiary | End users, buyers |
| **End User** | Direct solution users | Employees, customers |
| **Sponsor** | Provides resources/authority | Executive, budget owner |
| **Domain SME** | Subject matter expert | Process owners, specialists |
| **Implementation SME** | Technical expert | Developers, architects |
| **Tester** | Validates solution | QA team, UAT participants |
| **Regulator** | Compliance authority | Legal, audit, government |
| **Supplier** | External provider | Vendors, partners |

### Step 2: Analyze Stakeholder Characteristics

For each stakeholder, document:

| Attribute | Description |
|-----------|-------------|
| **Influence** | Power to affect decisions |
| **Impact** | How change affects them |
| **Attitude** | Support level for change |
| **Knowledge** | Expertise relevant to initiative |
| **Needs** | What they require from solution |
| **Communication style** | Preferred interaction method |

### Step 3: Assess Influence and Impact

Map stakeholders on a matrix:

```
HIGH INFLUENCE
    |
    | Manage Closely  |  Keep Satisfied
    |                 |
    |-----------------|-----------------
    |                 |
    | Keep Informed   |  Monitor
    |                 |
LOW INFLUENCE --- HIGH IMPACT --- LOW IMPACT
```

### Step 4: Identify Needs and Concerns

For each key stakeholder:

```markdown
## Stakeholder: [Name/Role]

**Needs:**
- [Need 1]
- [Need 2]

**Concerns:**
- [Concern 1]
- [Concern 2]

**Success Criteria:**
- [How they measure success]

**Pain Points:**
- [Current frustrations]
```

### Step 5: Plan Engagement

Define how to work with each stakeholder:

| Stakeholder | Engagement Approach | Frequency | Method |
|-------------|---------------------|-----------|--------|
| [Name] | [Active/Inform/Consult] | [Freq] | [How] |

### Step 6: Manage Relationships

Ongoing activities:
- Build trust and rapport
- Manage expectations
- Address concerns
- Resolve conflicts
- Maintain communication

---

## Templates

### Stakeholder Register Template

```markdown
# Stakeholder Register: [Initiative Name]

**Version:** [X.X]
**Date:** [Date]
**BA:** [Name]

| ID | Stakeholder | Role | Category | Influence | Impact | Attitude | Engagement |
|----|-------------|------|----------|-----------|--------|----------|------------|
| S-01 | [Name] | [Role] | [Cat] | H/M/L | H/M/L | +/0/- | [Approach] |
| S-02 | [Name] | [Role] | [Cat] | H/M/L | H/M/L | +/0/- | [Approach] |
```

### Stakeholder Profile Template

```markdown
# Stakeholder Profile: [Name/Role]

**Initiative:** [Name]
**Last Updated:** [Date]

## Basic Information
- **Name:** [Name]
- **Title:** [Title]
- **Department:** [Dept]
- **Contact:** [Email/Phone]

## Characteristics
- **Influence Level:** [High/Medium/Low]
- **Impact Level:** [High/Medium/Low]
- **Attitude:** [Supportive/Neutral/Resistant]
- **Knowledge Area:** [Expertise]

## Needs and Expectations
- [Need 1]
- [Need 2]

## Concerns
- [Concern 1]
- [Concern 2]

## Communication Preferences
- **Preferred Method:** [Email/Meeting/Phone]
- **Frequency:** [Daily/Weekly/As needed]
- **Detail Level:** [High/Summary]

## Engagement Strategy
[How to work with this stakeholder]

## Engagement History
| Date | Interaction | Notes |
|------|-------------|-------|
| [Date] | [Type] | [Notes] |
```

---

## Examples

### Example 1: CRM Implementation

**Stakeholders identified:**

| Stakeholder | Influence | Impact | Attitude | Strategy |
|-------------|-----------|--------|----------|----------|
| VP Sales | High | High | Supportive | Champion |
| Sales Reps | Low | High | Mixed | Training, involvement |
| IT Director | Medium | Medium | Neutral | Technical consultation |
| Finance | Medium | Low | Supportive | Reporting requirements |

### Example 2: Process Automation

**Stakeholder concerns:**

| Stakeholder | Primary Concern | How to Address |
|-------------|-----------------|----------------|
| Operations Manager | Job losses | Redeployment plan, automation as augmentation |
| Process Workers | Job security | Training, new role opportunities |
| Quality Team | Accuracy | Testing, quality metrics |
| Customers | Service continuity | Phased rollout |

---

## Common Mistakes

1. **Missing stakeholders** - Discovering late in project
2. **Assuming attitudes** - Not verifying with conversation
3. **Ignoring resistance** - Not addressing concerns
4. **One-size-fits-all** - Same approach for everyone
5. **Static analysis** - Not updating as things change

---

## Stakeholder Conflicts

When stakeholders have conflicting needs:

1. **Understand each position** - Why do they want what they want?
2. **Find common ground** - Shared goals or concerns
3. **Identify trade-offs** - What are the options?
4. **Escalate if needed** - Bring to sponsor for decision
5. **Document decision** - Record rationale

**Conflict resolution techniques:**
- Facilitated workshop
- One-on-one discussions
- Prototype/demo to clarify
- Prioritization exercise
- Sponsor decision

---

## RACI for BA Activities

| Activity | Sponsor | SME | User | BA |
|----------|---------|-----|------|-----|
| Define requirements | A | C | R | R |
| Approve requirements | A | C | I | R |
| Validate solution | A | C | R | R |
| Accept delivery | A | C | R | I |

R = Responsible, A = Accountable, C = Consulted, I = Informed

---

## Next Steps

After stakeholder analysis:
1. Validate list with sponsor
2. Begin stakeholder engagement
3. Schedule initial interviews
4. Monitor stakeholder dynamics
5. Connect to Elicitation Techniques methodology

---

## References

- BA Framework Guide v3 - Business Analysis Planning and Monitoring
- BA industry Stakeholder Analysis Guidelines
