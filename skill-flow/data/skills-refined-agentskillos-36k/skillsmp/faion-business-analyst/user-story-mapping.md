---
id: user-story-mapping
name: "User Story Mapping"
domain: BA
skill: faion-business-analyst
category: "business-analysis"
---

# User Story Mapping

## Metadata
- **Category:** BA Framework / Requirements Analysis and Design Definition
- **Difficulty:** Intermediate
- **Tags:** #methodology #babok #user-stories #agile #business-analysis
- **Agent:** faion-ba-agent

---

## Problem

User stories exist as a flat list with no context. The team cannot see how stories connect to user journeys. Release planning is difficult because there is no big picture. Important stories get lost among hundreds of backlog items. The user experience is fragmented.

Without user story mapping:
- No journey context
- Difficult release planning
- Lost stories
- Fragmented experience

---

## Framework

### What is User Story Mapping?

User Story Mapping arranges user stories along two dimensions:
- **Horizontal:** User journey (activities and tasks)
- **Vertical:** Priority (essential to nice-to-have)

The result shows the complete user experience and enables release planning.

### Story Map Structure

```
Activities:    [Activity 1]    [Activity 2]    [Activity 3]
                    |               |               |
Tasks:         [Task 1.1]      [Task 2.1]      [Task 3.1]
               [Task 1.2]      [Task 2.2]      [Task 3.2]
                    |               |               |
               --------------- Release 1 ---------------
Stories:       [Story A]       [Story D]       [Story G]
               [Story B]       [Story E]       [Story H]
               --------------- Release 2 ---------------
               [Story C]       [Story F]       [Story I]
```

### Step 1: Identify User Activities

Map high-level activities in the user journey:

**Questions:**
- What does the user do with the product?
- What is the sequence of major activities?
- What goals does the user have?

**Example activities:** Browse → Select → Purchase → Track → Return

### Step 2: Break Down into Tasks

For each activity, identify specific tasks:

**Activity: Purchase**
- Tasks: Add to cart, Enter shipping, Enter payment, Confirm order

### Step 3: Write User Stories

For each task, write stories that deliver functionality:

**Task: Enter shipping**
- Story: As a customer, I want to enter my shipping address so that I receive my order
- Story: As a customer, I want to save my address for future orders
- Story: As a customer, I want to select from saved addresses

### Step 4: Arrange Vertically by Priority

Stack stories vertically:
- Top: Essential for minimum viable experience
- Middle: Important enhancements
- Bottom: Nice-to-have

### Step 5: Slice into Releases

Draw horizontal lines to define releases:
- Release 1: Walking skeleton (minimum viable)
- Release 2: Enhanced functionality
- Release 3: Polish and extras

---

## Templates

### Story Map Template

```markdown
# User Story Map: [Product Name]

**Version:** [X.X]
**Date:** [Date]
**Product Owner:** [Name]

## Personas
- [Persona 1]: [Brief description]
- [Persona 2]: [Brief description]

## User Journey

### Backbone (Activities)

| Step | Activity | Goal |
|------|----------|------|
| 1 | [Activity 1] | [What user wants to achieve] |
| 2 | [Activity 2] | [What user wants to achieve] |
| 3 | [Activity 3] | [What user wants to achieve] |

### Walking Skeleton (Tasks)

| Activity 1 | Activity 2 | Activity 3 |
|------------|------------|------------|
| Task 1.1 | Task 2.1 | Task 3.1 |
| Task 1.2 | Task 2.2 | Task 3.2 |

## Story Map

### Activity 1: [Name]

**Task 1.1: [Name]**

| Release | Story | Priority | Size |
|---------|-------|----------|------|
| R1 | [Story title] | Must | S/M/L |
| R1 | [Story title] | Must | S/M/L |
| R2 | [Story title] | Should | S/M/L |
| R3 | [Story title] | Could | S/M/L |

**Task 1.2: [Name]**
[Same structure]

### Activity 2: [Name]
[Same structure]

## Release Plan

### Release 1: [Name/Theme]
**Goal:** [What this release achieves]
**Stories:**
- [Story list from above]

**Estimated Duration:** [X sprints]

### Release 2: [Name/Theme]
[Same structure]
```

### User Story Template

```markdown
# User Story: [ID]

**Title:** [Short descriptive title]
**Epic:** [Parent epic]
**Activity:** [From story map]
**Task:** [From story map]

## Story
**As a** [user type/persona]
**I want** [goal/desire]
**So that** [benefit/value]

## Acceptance Criteria

**Scenario 1: [Happy path]**
- Given [context]
- When [action]
- Then [expected result]

**Scenario 2: [Alternative]**
- Given [context]
- When [action]
- Then [expected result]

## Additional Details
- **Priority:** [Must/Should/Could/Won't]
- **Size:** [Story points or T-shirt]
- **Dependencies:** [Related stories]
- **Notes:** [Any other information]
```

---

## Examples

### Example 1: E-commerce Story Map

**Backbone (Activities):**
1. Discover Products
2. Evaluate Products
3. Purchase
4. Receive Order
5. Handle Issues

**Release 1 (MVP):**

| Discover | Evaluate | Purchase | Receive | Issues |
|----------|----------|----------|---------|--------|
| Browse catalog | View product | Add to cart | Track order | Contact support |
| Search | See price | Checkout | | |
| | | Pay | | |

**Release 2:**

| Discover | Evaluate | Purchase | Receive | Issues |
|----------|----------|----------|---------|--------|
| Filter products | Compare items | Save cart | Get notifications | Return item |
| See categories | Read reviews | Apply coupon | | |

### Example 2: Walking Skeleton

**Goal:** User can complete basic flow end-to-end

| Activity | Minimum Task | Story |
|----------|--------------|-------|
| Sign up | Basic registration | Email/password signup |
| Create | Add one item | Create simple item |
| Share | Basic share | Share via link |
| View | See shared item | View shared content |

**Note:** Each release should deliver a complete user experience, just with fewer features.

---

## Common Mistakes

1. **Flat backlog** - No journey context
2. **Technical stories on map** - Should be user-focused
3. **No releases defined** - Just prioritized list
4. **Missing tasks** - Incomplete journey
5. **Too detailed too early** - Mapping low-priority stories

---

## Story Mapping Workshop

**Duration:** 2-4 hours

**Participants:**
- Product Owner
- Business Analyst
- Developers
- UX Designer
- Key stakeholders

**Materials:**
- Large wall or whiteboard
- Sticky notes (3 colors)
- Markers

**Agenda:**
1. Review personas and goals (15 min)
2. Map activities (backbone) (30 min)
3. Add tasks (30 min)
4. Write stories (60 min)
5. Prioritize vertically (30 min)
6. Define releases (30 min)

---

## Release Planning with Story Maps

### Slicing Strategies

| Strategy | Description | When to Use |
|----------|-------------|-------------|
| **Horizontal** | Slice off entire activities | When activities are independent |
| **Vertical** | Thin slice through all activities | When need full journey |
| **Mixed** | Combination | Most common approach |

### Minimum Viable Product (MVP)

The first release line should represent:
- Complete user journey (thin slice)
- Core value proposition
- Testable with real users
- Foundation to build upon

---

## Integration with Other Techniques

| Technique | How It Relates |
|-----------|----------------|
| **Use cases** | Activities often map to use cases |
| **Personas** | Stories written for specific personas |
| **Process maps** | Activities follow process flow |
| **Epics** | Activities or tasks become epics |

---

## Next Steps

After story mapping:
1. Validate with stakeholders
2. Estimate story sizes
3. Plan first release
4. Create sprint backlog
5. Connect to Acceptance Criteria methodology

---

## References

- BA Framework Guide v3 - Requirements Analysis and Design Definition
- Jeff Patton - User Story Mapping (Book)
