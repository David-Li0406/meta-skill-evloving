# Work Breakdown Structure (WBS) Analysis Skill

## Purpose
Analyze implementation plans and generate structured work breakdowns that integrate directly with the `bd` (beads) issue tracker. This skill decomposes projects into schedulable tasks with proper dependencies, priorities, and estimates.

## When to Use This Skill
- User provides an implementation plan, project proposal, or feature specification
- User asks to "break down" work, create a WBS, or analyze task structure
- User needs to understand project scope before scheduling
- Before creating issues in beads to track implementation work

## Core Principles

### 1. Deliverable-Oriented Decomposition
- Focus on tangible outputs, not activities
- Each task should produce a verifiable result
- Name tasks by what they produce: "User authentication endpoint" not "Work on auth"

### 2. Appropriate Granularity
- **Atomic tasks**: 30-480 minutes (0.5-8 hours)
- **Too small**: "Write one function" (unless complex)
- **Too large**: "Build entire backend"
- **Just right**: "Implement user registration endpoint with validation"

### 3. bd-Compatible Structure
All tasks map directly to bd issue fields:
- **type**: bug | feature | task | epic | chore
- **priority**: 0-4 (0=critical, 4=backlog)
- **estimate**: minutes (60=1hr, 240=4hrs)
- **dependencies**: blocking relationships between tasks

---

## Analysis Process

### Step 1: Extract Project Structure
Read the implementation plan and identify:
- **Objective**: What is the end goal?
- **Scope boundaries**: What's included/excluded?
- **Key deliverables**: Major components or milestones
- **Constraints**: Technical, timeline, resource limitations
- **Success criteria**: How is completion defined?

### Step 2: Identify Major Work Packages (Epics)
Organize work into 3-7 high-level packages:
- Infrastructure/Setup
- Core functionality modules
- Integration points
- Testing/Quality assurance
- Documentation/Deployment

Each work package becomes an **epic** in beads.

### Step 3: Decompose to Schedulable Tasks
For each work package, break down into tasks that:
- Can be completed in one focused session (30-480 minutes)
- Have clear start/end criteria
- Can be assigned to a single executor
- Produce testable/verifiable output

### Step 4: Analyze Dependencies
For each task, identify:
- **Hard dependencies**: Must complete X before starting Y (use `bd dep add`)
- **Soft dependencies**: Y benefits from X being done first (note but don't block)
- **Parallel opportunities**: Tasks that can run concurrently
- **External blockers**: Waiting on third parties, approvals, etc.

### Step 5: Estimate Effort
Provide estimates in minutes for bd compatibility:
- **Small**: 30-120 minutes (simple, well-defined)
- **Medium**: 120-240 minutes (moderate complexity)
- **Large**: 240-480 minutes (complex, may need further breakdown)
- **Extra Large**: >480 minutes (must be broken down further)

### Step 6: Assign Priorities
Use bd priority levels:
- **P0 (Critical)**: Security issues, data loss, broken builds
- **P1 (High)**: Major features, important bugs, blockers
- **P2 (Medium)**: Default for most work
- **P3 (Low)**: Polish, optimization, nice-to-have
- **P4 (Backlog)**: Future ideas, low-impact improvements

### Step 7: Identify Risks
Flag tasks with:
- **Technical uncertainty**: Untested approaches, new technology
- **Integration risk**: Multiple systems/components interacting
- **External dependencies**: Third-party APIs, services
- **Knowledge gaps**: Areas requiring research/learning

---

## Output Format

Generate the work breakdown in this structure:

```markdown
# Work Breakdown: [Project Name]

## Summary
- **Objective**: [Clear statement of goal]
- **Total Tasks**: [N tasks across M epics]
- **Estimated Effort**: [X-Y hours]
- **Critical Path**: [Sequence of blocking tasks]
- **Key Risks**: [Top 3-5 risks]

## Epics

### Epic 1: [Epic Name]
**Purpose**: [Why this epic exists]
**Estimated Effort**: [X hours total]

| ID | Title | Type | Priority | Estimate | Depends On | Risk |
|----|-------|------|----------|----------|------------|------|
| E1.1 | [Task title] | task | P2 | 120m | - | Low |
| E1.2 | [Task title] | task | P1 | 240m | E1.1 | Medium |
| E1.3 | [Task title] | task | P2 | 60m | E1.1 | Low |

### Epic 2: [Epic Name]
...

## Dependency Graph
[Text representation of critical dependencies]

## Parallel Opportunities
- Tasks [E1.2, E1.3] can run after E1.1 completes
- Epic 2 can start in parallel with Epic 1 after E1.1

## Execution Commands

To create these issues in beads, run the following commands:

### Create Epics
```bash
bd create "Epic 1: [Name]" -t epic -p 1 -e 720 -d "Purpose: ..."
bd create "Epic 2: [Name]" -t epic -p 2 -e 480 -d "Purpose: ..."
```

### Create Tasks (run in order for dependency resolution)
```bash
# Epic 1 tasks
bd create "[E1.1 Title]" -t task -p 2 -e 120 --parent $EPIC1_ID -d "..."
bd create "[E1.2 Title]" -t task -p 1 -e 240 --parent $EPIC1_ID -d "..."
bd create "[E1.3 Title]" -t task -p 2 -e 60 --parent $EPIC1_ID -d "..."

# Add dependencies (after tasks exist)
bd dep add $E1_2_ID $E1_1_ID  # E1.2 depends on E1.1
bd dep add $E1_3_ID $E1_1_ID  # E1.3 depends on E1.1
```

### Parallel Task Creation (for efficiency)
The following tasks have no dependencies and can be created in parallel:
- E1.1, E2.1, E3.1 (first tasks of each epic)
```

---

## Direct bd Integration

When the user approves the work breakdown, execute bd commands directly:

### Step 1: Create Epics First
```bash
# Create all epics to get their IDs
bd create "Epic Name" -t epic -p [priority] -e [total_estimate] -d "Purpose" --json
```

### Step 2: Create Tasks with Parent References
```bash
# Create tasks as children of epics
bd create "Task Title" -t task -p [priority] -e [estimate] --parent [epic_id] -d "Description" --json
```

### Step 3: Add Dependencies
```bash
# Add blocking dependencies
bd dep add [dependent_id] [blocker_id]  # dependent depends on blocker
```

### Step 4: Verify Structure
```bash
bd dep tree [epic_id]  # Visualize dependency tree
bd ready              # Show tasks ready to start
```

---

## Quality Checklist

Before presenting the WBS, verify:
- [ ] All tasks are deliverable-oriented (produce something tangible)
- [ ] Task granularity is appropriate (30-480 minute chunks)
- [ ] Dependencies are clearly identified
- [ ] No orphaned tasks (everything connects to an epic)
- [ ] Estimates account for testing, debugging, and integration
- [ ] Risks are called out explicitly
- [ ] Critical path is identifiable
- [ ] Parallel work opportunities are highlighted
- [ ] All fields map to valid bd values (types, priorities 0-4, estimates in minutes)

---

## Common Pitfalls to Avoid

### Anti-patterns
- **Activity-oriented tasks**: "Research options" -> Better: "Decision document: Database selection"
- **Vague deliverables**: "Work on API" -> Better: "User authentication endpoints with JWT"
- **Hidden dependencies**: Assuming tasks are independent when they're not
- **Optimistic estimates**: Forgetting testing, debugging, integration time
- **Over-decomposition**: Breaking 30-minute tasks into 5-minute pieces
- **Under-decomposition**: Leaving 8+ hour chunks as single tasks

### Missing elements to include
- Testing tasks (unit, integration, end-to-end)
- Documentation work (README, API docs, runbooks)
- Infrastructure setup (environments, CI/CD, monitoring)
- Code review and refinement time
- Buffer for unknowns and learning

---

## bd Field Reference

| Field | CLI Flag | Values | Notes |
|-------|----------|--------|-------|
| type | `-t, --type` | bug, feature, task, epic, chore | Default: task |
| priority | `-p, --priority` | 0-4 or P0-P4 | 0=highest, default: 2 |
| estimate | `-e, --estimate` | minutes | e.g., 60 for 1 hour |
| parent | `--parent` | issue ID | Creates hierarchical child |
| deps | `--deps` | type:id or id | e.g., "blocks:bd-123" |
| labels | `-l, --labels` | comma-separated | e.g., "backend,security" |
| description | `-d, --description` | text | Task details |
| assignee | `-a, --assignee` | username | Who owns this |

### Dependency Types
| Type | Usage | Example |
|------|-------|---------|
| blocks | Hard dependency | `bd dep add child parent` (child depends on parent) |
| related | Soft connection | For reference, doesn't block |
| discovered-from | AI-discovered work | Links to source issue |
| parent-child | Hierarchy | Use `--parent` flag on create |

---

## Example: Breaking Down a Feature

**Input**: "Add user profile photo upload feature"

**Output**:

```markdown
# Work Breakdown: Profile Photo Upload

## Summary
- **Objective**: Allow users to upload and display profile photos
- **Total Tasks**: 9 tasks across 3 epics
- **Estimated Effort**: 20-26 hours
- **Critical Path**: E1.1 -> E1.2 -> E1.3 -> E3.1 -> E3.2
- **Key Risks**: S3 configuration, image processing performance

## Epics

### Epic 1: Backend Infrastructure
**Purpose**: API endpoints and storage integration
**Estimated Effort**: 8-10 hours

| ID | Title | Type | Priority | Estimate | Depends On | Risk |
|----|-------|------|----------|----------|------------|------|
| E1.1 | Image upload endpoint with validation | task | P1 | 180m | - | Low |
| E1.2 | S3 storage integration | task | P2 | 120m | E1.1 | Medium |
| E1.3 | Image processing service (resize/optimize) | task | P2 | 240m | E1.2 | Medium |

### Epic 2: Frontend Components
**Purpose**: User interface for photo management
**Estimated Effort**: 8-10 hours

| ID | Title | Type | Priority | Estimate | Depends On | Risk |
|----|-------|------|----------|----------|------------|------|
| E2.1 | Photo upload UI component | task | P2 | 180m | E1.1 | Low |
| E2.2 | Image preview and crop interface | task | P2 | 240m | E2.1 | Low |
| E2.3 | Profile page integration | task | P2 | 120m | E2.2 | Low |

### Epic 3: Quality & Polish
**Purpose**: Testing and documentation
**Estimated Effort**: 4-6 hours

| ID | Title | Type | Priority | Estimate | Depends On | Risk |
|----|-------|------|----------|----------|------------|------|
| E3.1 | Unit tests for upload endpoints | task | P2 | 120m | E1.3 | Low |
| E3.2 | E2E tests for upload flow | task | P2 | 180m | E2.3, E3.1 | Low |
| E3.3 | API documentation update | task | P3 | 60m | E3.2 | Low |

## Parallel Opportunities
- E2.1 can start after E1.1 (doesn't need S3 or processing)
- E1.2/E1.3 and E2.1/E2.2 can run in parallel tracks

## Execution Commands

### Create Epics
```bash
bd create "Backend Infrastructure: Photo Upload" -t epic -p 1 -e 540 -d "API endpoints and S3 storage for profile photos"
bd create "Frontend Components: Photo Upload" -t epic -p 2 -e 540 -d "UI for photo upload, preview, and profile display"
bd create "Quality & Polish: Photo Upload" -t epic -p 2 -e 360 -d "Testing and documentation"
```

### Create Tasks (substitute actual IDs)
```bash
# Epic 1 tasks
bd create "Image upload endpoint with validation" -t task -p 1 -e 180 --parent EPIC1 -d "POST /api/users/photo with size/type validation, max 5MB, jpg/png only"
bd create "S3 storage integration" -t task -p 2 -e 120 --parent EPIC1 -d "Configure S3 bucket, implement upload service, handle presigned URLs"
bd create "Image processing service" -t task -p 2 -e 240 --parent EPIC1 -d "Resize to standard dimensions (thumbnail, medium, large), optimize for web"

# Epic 2 tasks
bd create "Photo upload UI component" -t task -p 2 -e 180 --parent EPIC2 -d "Drag-drop upload, progress indicator, error handling"
bd create "Image preview and crop interface" -t task -p 2 -e 240 --parent EPIC2 -d "Client-side crop tool, aspect ratio lock, preview before upload"
bd create "Profile page integration" -t task -p 2 -e 120 --parent EPIC2 -d "Display photo, edit button, fallback avatar"

# Epic 3 tasks
bd create "Unit tests for upload endpoints" -t task -p 2 -e 120 --parent EPIC3 -d "Test validation, S3 mocking, error cases"
bd create "E2E tests for upload flow" -t task -p 2 -e 180 --parent EPIC3 -d "Full upload flow, crop, display verification"
bd create "API documentation update" -t task -p 3 -e 60 --parent EPIC3 -d "Document new endpoints, request/response schemas"

# Add dependencies (after all tasks created)
bd dep add E1.2_ID E1.1_ID  # S3 depends on upload endpoint
bd dep add E1.3_ID E1.2_ID  # Processing depends on S3
bd dep add E2.1_ID E1.1_ID  # Frontend depends on backend endpoint
bd dep add E2.2_ID E2.1_ID  # Crop depends on upload UI
bd dep add E2.3_ID E2.2_ID  # Profile depends on crop
bd dep add E3.1_ID E1.3_ID  # Unit tests depend on processing
bd dep add E3.2_ID E3.1_ID  # E2E depends on unit tests
bd dep add E3.2_ID E2.3_ID  # E2E depends on frontend
bd dep add E3.3_ID E3.2_ID  # Docs depend on E2E
```
```

---

## Skill Workflow

1. **Receive implementation plan** from user
2. **Analyze and decompose** using the process above
3. **Present WBS** for user review
4. **Ask for confirmation** before creating issues
5. **Execute bd commands** to create epics, tasks, and dependencies
6. **Run `bd ready`** to show first available tasks
7. **Track progress** with `bd list --status in_progress`

---

## Handling Large Projects

For projects that are too large to break down at once:

1. **Create phase structure**:
   ```bash
   bd create "Phase 0: Architecture Design" -t epic -p 0
   bd create "Phase 1: Core Implementation" -t epic -p 1
   bd create "Phase 2: Integration" -t epic -p 2
   ```

2. **Break down Phase 0 fully** (current work)

3. **Create placeholder epics** for future phases with `P4` priority

4. **Add phase dependencies**:
   ```bash
   bd dep add PHASE1_ID PHASE0_ID  # Phase 1 depends on Phase 0
   bd dep add PHASE2_ID PHASE1_ID  # Phase 2 depends on Phase 1
   ```

5. **Defer detailed breakdown** of future phases until current phase completes

---

## Skill Maintenance Notes

This skill should be updated when:
- bd command syntax or flags change
- New task patterns emerge from completed projects
- Estimation accuracy improves with historical data
- User feedback identifies gaps or improvements needed
