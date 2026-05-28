---
id: schedule-development
name: "Schedule Development"
domain: PM
skill: faion-project-manager
category: "project-management"
---

# Schedule Development

## Metadata
- **Category:** Project Management Framework 7 - Planning Performance Domain
- **Difficulty:** Intermediate
- **Tags:** #product, #methodology, #pmbok
- **Read Time:** 8 min
- **Agent:** faion-pm-agent

---

## Problem

Without proper scheduling:
- Deadlines are arbitrary guesses
- Dependencies cause cascading delays
- Critical path is unknown
- Resources are over/under-allocated

## Framework

### Step 1: Define Activities

Convert WBS work packages into specific activities:

| Work Package | Activities |
|--------------|------------|
| User authentication | Design auth flow, Implement login, Implement logout, Add password reset |

### Step 2: Sequence Activities

Identify dependencies between activities:

| Type | Description | Example |
|------|-------------|---------|
| **FS** | Finish-to-Start | Code must finish before testing starts |
| **FF** | Finish-to-Finish | Documentation finishes with development |
| **SS** | Start-to-Start | Testing starts when dev starts |
| **SF** | Start-to-Finish | (Rare) Night shift starts, day shift finishes |

### Step 3: Estimate Durations

Use multiple estimation techniques:

**Three-Point Estimation (PERT):**
```
Duration = (Optimistic + 4×Most Likely + Pessimistic) / 6

Example:
O = 3 days, M = 5 days, P = 10 days
Duration = (3 + 4×5 + 10) / 6 = 5.5 days
```

**Analogous Estimation:**
- Compare to similar past tasks
- "Login feature took 3 days last project"

**Parametric Estimation:**
- Use metrics: "1 API endpoint = 4 hours"
- "10 endpoints × 4 hours = 40 hours"

### Step 4: Identify Critical Path

The Critical Path is the longest sequence of dependent activities.

```
Activity Network:
    A(3) → B(2) → D(4)
    ↓           ↗
    C(5) ──────┘

Path 1: A → B → D = 3+2+4 = 9 days
Path 2: A → C → D = 3+5+4 = 12 days ← CRITICAL PATH

Project duration: 12 days minimum
```

**Critical Path Rules:**
- Any delay on critical path delays the project
- Critical activities have zero float
- Focus management attention here

### Step 5: Add Buffers

**Project Buffer:** Add at end of project (typically 10-20%)

**Feeding Buffer:** Add where non-critical paths join critical path

```
Non-Critical → [BUFFER] → Critical Path → [PROJECT BUFFER] → Deadline
```

---

## Templates

### Activity List

```markdown
## Activity List - [Project Name]

| ID | Activity | Duration | Dependencies | Resources |
|----|----------|----------|--------------|-----------|
| A1 | Requirements review | 2d | None | BA |
| A2 | Database design | 3d | A1 | Architect |
| A3 | API design | 2d | A1 | Dev Lead |
| A4 | Frontend wireframes | 4d | A1 | Designer |
| A5 | Database implementation | 5d | A2 | Backend |
| A6 | API development | 8d | A2, A3 | Backend |
| A7 | Frontend development | 10d | A3, A4 | Frontend |
| A8 | Integration | 3d | A6, A7 | Team |
| A9 | Testing | 5d | A8 | QA |
| A10 | Deployment | 2d | A9 | DevOps |
```

### Gantt Chart (Text-Based)

```
Week:     1    2    3    4    5    6    7
         |----|----|----|----|----|----|
A1       ██
A2           ███
A3           ██
A4           ████
A5               █████
A6               ████████
A7               ██████████
A8                              ███
A9                                 █████
A10                                     ██
         |----|----|----|----|----|----|
                              ↑ Critical Milestone
```

---

## Examples

### Example 1: MVP Development Schedule

| Phase | Duration | Dependencies | Buffer |
|-------|----------|--------------|--------|
| Discovery | 2 weeks | None | 0 |
| Design | 2 weeks | Discovery | 2 days |
| Development Sprint 1 | 2 weeks | Design | 0 |
| Development Sprint 2 | 2 weeks | Sprint 1 | 0 |
| Testing | 1 week | Sprint 2 | 3 days |
| Launch | 3 days | Testing | 2 days |
| **Total** | **9 weeks** | | **1 week buffer** |

### Example 2: Solopreneur Schedule

For a solopreneur, time is split across projects:

```
Daily allocation:
- Morning (3h): Deep work (critical path)
- Afternoon (2h): Support tasks (non-critical)
- Evening (1h): Admin (buffer time)

Weekly schedule:
Mon-Wed: Current project A (critical)
Thu-Fri: Project B (secondary)
Weekend: Learning/planning (investment)
```

---

## Common Mistakes

1. **No dependencies defined** - Everything looks parallel
2. **Optimistic estimates** - Real world takes longer
3. **Ignoring critical path** - Equal focus on all tasks
4. **No buffers** - First delay breaks everything
5. **Resource conflicts** - Same person on parallel tasks

---

## Related Methodologies

- **Work Breakdown Structure:** Source for schedule activities
- **Cost Estimation:** Budget aligned with schedule
- **Earned Value Management:** Schedule performance tracking

---

*Methodology from Project Management Framework 7 - Planning Performance Domain*
