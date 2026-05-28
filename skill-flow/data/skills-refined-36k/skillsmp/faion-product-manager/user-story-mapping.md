---
id: user-story-mapping
name: "User Story Mapping"
domain: PRD
skill: faion-product-manager
category: "product"
---

# User Story Mapping

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Product |
| **Difficulty** | Intermediate |
| **Tags** | #product, #user-stories, #mapping |
| **Domain Skill** | faion-product-manager |
| **Agents** | faion-mlp-spec-analyzer-agent |

---

## Problem

Flat backlogs lose context of user workflows. Common issues:
- Stories prioritized without seeing full picture
- Missing critical steps in user journeys
- No visualization of release scope
- Disconnect between stories and user goals

**The root cause:** Linear lists can't represent the multi-dimensional nature of user experience.

---

## Framework

### What is User Story Mapping?

User story mapping is a technique that arranges user stories into a visual model showing user activities horizontally and story priority vertically. It answers: "How does our backlog connect to the user's journey?"

### Story Map Structure

```
                    BACKBONE (User Activities)
    ═══════════════════════════════════════════════════
    [Activity 1]     [Activity 2]     [Activity 3]
    ─────────────    ─────────────    ─────────────

    WALKING SKELETON (Minimum viable flow)
    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
    │  Task 1.1   │  │  Task 2.1   │  │  Task 3.1   │
    └─────────────┘  └─────────────┘  └─────────────┘

    RELEASE 1 ═══════════════════════════════════════
    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
    │  Task 1.2   │  │  Task 2.2   │  │  Task 3.2   │
    └─────────────┘  └─────────────┘  │  Task 3.3   │
                                      └─────────────┘

    RELEASE 2 ═══════════════════════════════════════
    │  Task 1.3   │  │  Task 2.3   │  │  Task 3.4   │
    │  Task 1.4   │  │  Task 2.4   │  │  Task 3.5   │
```

### Story Map Components

#### 1. Backbone (Top Row)

**What:** High-level user activities
**Example:** Sign Up → Create Project → Invite Team → Track Progress

**Rules:**
- Left to right = user's journey
- Verb phrases ("Create Project" not "Project")
- 5-10 activities typically

#### 2. User Tasks (Under Each Activity)

**What:** Specific things user does within each activity
**Example under "Create Project":** Name project, Set deadline, Add description

**Rules:**
- Vertical = priority (higher = more important)
- Each task is testable
- Maps to user stories

#### 3. Walking Skeleton

**What:** Minimum tasks to complete the entire journey end-to-end
**Purpose:** Earliest version that proves the concept

**Rules:**
- One task per activity minimum
- Complete journey (not just start)
- Foundation for releases

#### 4. Release Slices

**What:** Horizontal lines grouping tasks for each release
**Purpose:** Define what's in each version

**Rules:**
- Each slice is shippable value
- Earlier slices = higher priority
- Validates scope decisions

### Story Mapping Process

#### Step 1: Frame the Journey

**Define:**
- Who is the user?
- What's their big goal?
- Where does the journey start/end?

#### Step 2: Build the Backbone

**Workshop activity:**
1. Write activities on cards
2. Arrange left to right in order
3. Verify: "Does this feel like the user's journey?"

#### Step 3: Add Tasks

**For each activity:**
1. What does the user DO here?
2. Write each task on a card
3. Place under activity column
4. Arrange vertically by importance

#### Step 4: Identify the Walking Skeleton

**Draw a line separating:**
- Absolute minimum to work end-to-end
- Everything else

#### Step 5: Slice Releases

**For each release:**
1. What value does this deliver?
2. Draw horizontal line
3. Name the release goal
4. Validate: "Is this shippable?"

---

## Templates

### Story Map Template

```markdown
## Story Map: [Product/Feature]

### Context
- **User:** [Primary persona]
- **Goal:** [What they're trying to achieve]
- **Scope:** [What journey this covers]

### Backbone

| Step | Activity 1 | Activity 2 | Activity 3 | Activity 4 |
|------|------------|------------|------------|------------|
| Name | [Activity] | [Activity] | [Activity] | [Activity] |

### Walking Skeleton
| Activity 1 | Activity 2 | Activity 3 | Activity 4 |
|------------|------------|------------|------------|
| [Task 1.1] | [Task 2.1] | [Task 3.1] | [Task 4.1] |

**Delivers:** [Minimum viable outcome]

### Release 1: [Name/Theme]
| Activity 1 | Activity 2 | Activity 3 | Activity 4 |
|------------|------------|------------|------------|
| [Task] | [Task] | [Task] | [Task] |
| [Task] | [Task] | | [Task] |

**Delivers:** [Value statement]
**Target:** [Date/Sprint]

### Release 2: [Name/Theme]
| Activity 1 | Activity 2 | Activity 3 | Activity 4 |
|------------|------------|------------|------------|
| [Task] | [Task] | [Task] | [Task] |

**Delivers:** [Value statement]
**Target:** [Date/Sprint]

### Parking Lot
Tasks not yet mapped to a release:
- [Task]
- [Task]
```

### Story Card Template

```markdown
## User Story: [Task Name]

### Placement
- **Activity:** [Which backbone item]
- **Release:** [Which slice]
- **Priority:** [1-N within release]

### Story
**As a** [user type]
**I want to** [action]
**So that** [benefit]

### Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

### Dependencies
- Depends on: [Other stories]
- Blocks: [Other stories]

### Estimate
[Size: XS/S/M/L/XL]

### Notes
[Additional context]
```

---

## Examples

### Example 1: E-commerce Story Map

**Backbone:**
Browse Products → View Product → Add to Cart → Checkout → Receive Order

**Walking Skeleton:**
| Browse | View | Cart | Checkout | Receive |
|--------|------|------|----------|---------|
| See product list | See details | Add item | Enter payment | Get confirmation |

**Release 1 (MVP):**
| Browse | View | Cart | Checkout | Receive |
|--------|------|------|----------|---------|
| Filter by category | See images | Update quantity | Enter shipping | Email receipt |
| Basic search | See price | Remove item | Choose shipping | |

**Release 2 (Enhanced):**
| Browse | View | Cart | Checkout | Receive |
|--------|------|------|----------|---------|
| Advanced filters | Reviews | Save for later | Apple Pay | Track shipment |
| Sort options | Size guide | Recommendations | Guest checkout | |

### Example 2: Project Management Story Map

**Backbone:**
Create Project → Add Tasks → Track Progress → Complete Project

**Walking Skeleton:**
| Create | Add Tasks | Track | Complete |
|--------|-----------|-------|----------|
| Name project | Add task | See task status | Mark done |

**Release 1 (Core):**
| Create | Add Tasks | Track | Complete |
|--------|-----------|-------|----------|
| Description | Due dates | Kanban board | Archive project |
| Invite member | Assign owner | Basic filters | |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Starting with tasks | Build backbone first |
| Only happy path | Include error handling tasks |
| Too detailed backbone | Keep to 5-10 activities |
| No walking skeleton | Always identify minimum path |
| Releases too big | Slice smaller, deliver faster |
| Solo mapping | Involve team for shared understanding |
| Static map | Update as you learn |

---

## Related Methodologies

- **jobs-to-be-done:** Jobs to Be Done
- **use-case-mapping:** Use Case Mapping
- **mvp-scoping:** MVP Scoping
- **writing-specifications:** Writing Specifications
- **user-journey-mapping:** User Journey Mapping

---

## Agent

**faion-mlp-spec-analyzer-agent** helps with story mapping. Invoke with:
- "Create a story map for [product/feature]"
- "Help me identify the walking skeleton for [journey]"
- "How should I slice releases for [story map]?"
- "Review my story map: [content]"

---

*Methodology | Product | Version 1.0*
