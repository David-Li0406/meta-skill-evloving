---
id: resource-management
name: "Resource Management"
domain: PM
skill: faion-project-manager
category: "project-management"
---

# Resource Management

## Metadata
- **Category:** Project Management Framework / Team Performance Domain
- **Difficulty:** Intermediate
- **Tags:** #methodology #pmbok #resources #team #project-management
- **Agent:** faion-pm-agent

---

## Problem

You need a developer but none are available. Your best people are overloaded while others sit idle. Skills do not match tasks. Team members burn out from unrealistic workloads. Resources are promised but never materialize.

Without resource management:
- Bottlenecks from missing skills
- Uneven workload distribution
- Schedule delays from unavailability
- Budget overruns from inefficiency

---

## Framework

### Resource Categories

| Type | Examples | Considerations |
|------|----------|----------------|
| **Human** | Team members, contractors | Skills, availability, cost |
| **Physical** | Equipment, facilities | Location, capacity, scheduling |
| **Material** | Supplies, software | Lead time, inventory |
| **Financial** | Budget, cash flow | Timing, approval process |

### Step 1: Identify Resource Requirements

For each work package:

| Question | Output |
|----------|--------|
| What skills are needed? | Skill requirements |
| How many people? | Quantity |
| For how long? | Duration |
| Any special needs? | Constraints |

### Step 2: Assess Resource Availability

**For each resource:**
- Current commitments
- Capacity (hours/week available)
- Skills and experience
- Cost (hourly/daily rate)

**Availability matrix:**

| Resource | Role | Available From | Hours/Week | Rate |
|----------|------|----------------|------------|------|
| Alice | Backend Dev | Now | 40 | $80 |
| Bob | Frontend Dev | Week 3 | 30 | $70 |
| Carol | Designer | Now | 20 | $65 |

### Step 3: Create Resource Plan

Map resources to activities:

```markdown
Week 1-2: Design Phase
- Carol: 40 hours (UI/UX design)
- Alice: 8 hours (technical consultation)

Week 3-6: Development Phase
- Alice: 160 hours (backend)
- Bob: 120 hours (frontend)
- Carol: 20 hours (design support)

Week 7-8: Testing Phase
- Alice: 40 hours (bug fixes)
- Bob: 40 hours (bug fixes)
```

### Step 4: Level Resources

Resolve conflicts where demand exceeds capacity:

| Technique | When to Use |
|-----------|-------------|
| **Delay tasks** | Non-critical path, flexible deadline |
| **Split tasks** | Work can be interrupted |
| **Add resources** | Budget allows, skill available |
| **Reduce scope** | Features can be cut |
| **Extend timeline** | Deadline flexible |

### Step 5: Develop the Team

Build team capability:

| Activity | Purpose |
|----------|---------|
| Training | Develop missing skills |
| Mentoring | Transfer knowledge |
| Team building | Improve collaboration |
| Clear expectations | Reduce confusion |
| Recognition | Maintain motivation |

### Step 6: Manage the Team

Ongoing activities:

- Track utilization vs. plan
- Address performance issues
- Handle conflicts
- Adjust assignments
- Communicate changes

---

## Templates

### Resource Plan Template

```markdown
# Resource Plan: [Project Name]

**Version:** [X.X]
**Date:** [Date]

## Resource Summary

| Role | Name | Allocation | Start | End | Rate |
|------|------|------------|-------|-----|------|
| [Role] | [Name] | [%/hours] | [Date] | [Date] | $[X] |

## Resource Calendar

| Week | [Resource 1] | [Resource 2] | [Resource 3] |
|------|--------------|--------------|--------------|
| W1 | 40h (Design) | - | 20h (Consult) |
| W2 | 40h (Design) | 40h (Dev) | 20h (Consult) |

## Skill Requirements

| Skill | Level | Resource(s) | Gap? |
|-------|-------|-------------|------|
| [Skill] | [Jr/Mid/Sr] | [Name] | [Yes/No] |

## Resource Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| [Person] leaves | High | Cross-train [backup] |
| [Skill] shortage | Medium | Hire contractor |
```

### Resource Request Form

```markdown
# Resource Request: [Project Name]

**Date:** [Date]
**Requestor:** [PM Name]
**Priority:** [High/Medium/Low]

## Request Details

| Field | Value |
|-------|-------|
| Role Required | [Role] |
| Skills Needed | [Specific skills] |
| Experience Level | [Jr/Mid/Sr] |
| Start Date | [Date] |
| End Date | [Date] |
| Allocation | [Hours/week or %] |

## Justification
[Why is this resource needed?]

## Impact if Not Filled
[What happens without this resource?]

## Alternatives Considered
- [Alternative 1]
- [Alternative 2]
```

---

## Examples

### Example 1: Software Project Resource Plan

| Phase | Duration | Resources | Total Hours |
|-------|----------|-----------|-------------|
| Planning | 2 weeks | PM (40h), Lead (20h) | 60h |
| Design | 2 weeks | Designer (80h), Lead (16h) | 96h |
| Development | 6 weeks | 2 Devs (480h), Lead (60h) | 540h |
| Testing | 2 weeks | QA (80h), Devs (40h) | 120h |
| **Total** | **12 weeks** | | **816h** |

### Example 2: Resource Leveling

**Before leveling:**
```
Week 3: Alice assigned 60 hours (overload!)
        - Task A: 30 hours
        - Task B: 30 hours
```

**After leveling:**
```
Week 3: Alice - Task A: 30 hours
Week 4: Alice - Task B: 30 hours
        (Task B moved to Week 4, non-critical path)
```

---

## Common Mistakes

1. **100% allocation** - People need time for meetings, email, breaks
2. **Skill mismatch** - Assigning wrong person to task
3. **No backup plan** - Single point of failure for critical skills
4. **Ignoring vacation** - Forgetting holidays and time off
5. **Late resource requests** - Waiting until last minute to ask

---

## Resource Utilization Guidelines

| Utilization | Interpretation |
|-------------|----------------|
| < 50% | Underutilized, find more work or reduce allocation |
| 50-75% | Healthy, room for meetings and unexpected work |
| 75-85% | Optimal for most roles |
| 85-100% | Full capacity, risk of burnout |
| > 100% | Overloaded, unsustainable, address immediately |

---

## Next Steps

After resource planning:
1. Confirm resource availability with managers
2. Document assignments in project plan
3. Set up time tracking
4. Monitor utilization weekly
5. Connect to Procurement Management methodology

---

## References

- Project Management Framework Guide 7th Edition - Team Performance Domain
- PM industry practice standard for Project Resource Management
