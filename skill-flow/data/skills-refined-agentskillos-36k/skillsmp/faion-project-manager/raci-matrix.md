---
id: raci-matrix
name: "RACI Matrix"
domain: PM
skill: faion-project-manager
category: "project-management"
---

# RACI Matrix

## Metadata
- **Category:** Project Management Framework 7 - Team Performance Domain
- **Difficulty:** Beginner
- **Tags:** #product, #methodology, #pmbok
- **Read Time:** 6 min
- **Agent:** faion-pm-agent

---

## Problem

Projects suffer from unclear responsibilities:
- "I thought you were handling that"
- Multiple people doing the same work
- Critical tasks with no owner
- Approval bottlenecks from undefined decision makers

## Framework

### What is RACI?

RACI assigns one of four roles to each person for each task:

| Role | Description | Rule |
|------|-------------|------|
| **R** - Responsible | Does the work | Can be multiple people |
| **A** - Accountable | Final decision maker | Only ONE per task |
| **C** - Consulted | Provides input before decision | Asked for opinion |
| **I** - Informed | Notified after decision | One-way communication |

### Step 1: List All Tasks/Deliverables

Break down project into discrete activities:
- Requirements gathering
- Design approval
- Development
- Testing
- Deployment
- Documentation

### Step 2: Identify All Roles

List every role (not people) involved:
- Project Manager
- Product Owner
- Lead Developer
- QA Engineer
- DevOps Engineer
- Business Analyst

### Step 3: Assign RACI Values

For each task-role combination, assign R, A, C, or I.

**Rules:**
- Every task must have exactly ONE "A"
- Every task must have at least one "R"
- "A" can also be "R" (but not ideal)
- Minimize "C" to avoid bottlenecks
- Be generous with "I"

### Step 4: Validate the Matrix

Check for issues:

| Issue | Problem | Solution |
|-------|---------|----------|
| No "A" | No decision maker | Assign accountable person |
| Multiple "A" | Confusion on authority | Pick one |
| No "R" | Work won't get done | Assign responsible party |
| Too many "C" | Bottleneck | Reduce to essential only |
| All "I" in row | Person not needed | Remove from matrix |
| No "I" anywhere | People in the dark | Add stakeholders |

---

## Templates

### Basic RACI Matrix

```markdown
## RACI Matrix - [Project Name]

| Task | PM | PO | Dev Lead | QA | DevOps | BA |
|------|----|----|----------|----|---------|----|
| Requirements | C | A | C | I | I | R |
| Design | I | A | R | C | C | C |
| Development | I | C | A/R | I | I | I |
| Testing | I | I | C | A/R | I | I |
| Deployment | C | A | C | C | R | I |
| Go-Live | A | C | R | R | R | I |
```

### RACI with Extended Roles

Some teams add:
- **S** - Support (provides resources)
- **V** - Verify (checks work quality)
- **O** - Omitted (explicitly excluded)

---

## Examples

### Example 1: Feature Development RACI

| Activity | PM | Product | Engineering | Design | QA |
|----------|----|---------|--------------|---------|----|
| Define requirements | C | A | C | C | I |
| Create mockups | I | C | I | R | I |
| Approve design | I | A | C | R | I |
| Write code | I | C | R | I | I |
| Code review | I | I | A | I | I |
| Write tests | I | I | C | I | R |
| Deploy to staging | C | I | R | I | C |
| UAT sign-off | I | A | I | I | R |
| Production deploy | A | I | R | I | C |

### Example 2: Solopreneur RACI

Even solopreneurs benefit from RACI when working with contractors:

| Task | You | Designer | Developer | VA |
|------|-----|----------|-----------|-----|
| Product vision | A/R | I | I | I |
| UI design | A | R | C | I |
| Development | A | C | R | I |
| Testing | A | I | C | R |
| Launch | A/R | I | I | C |

---

## Common Mistakes

1. **Multiple Accountables** - Creates confusion, delays
2. **Responsible without Authority** - People can't deliver
3. **Too many Consulteds** - Slows everything down
4. **Forgetting RACI updates** - Matrix becomes stale
5. **No communication of RACI** - People don't know their roles

---

## Related Methodologies

- **Stakeholder Engagement:** Identifying who is involved
- **Work Breakdown Structure:** Defining what needs RACI
- **Requirements Traceability:** Linking requirements to responsibilities

---

*Methodology from Project Management Framework 7 - Team Performance Domain*
