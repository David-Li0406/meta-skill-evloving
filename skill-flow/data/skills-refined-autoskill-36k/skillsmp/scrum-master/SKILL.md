---
name: scrum-master
description: Breaks down product development plans into agile sprints with story point estimation. Creates sprint plans, organizes work into manageable user stories, and provides sprint structure for iterative development. Use when given a development plan, roadmap, or feature list that needs to be organized into sprints, when planning agile development cycles, or when the user asks for sprint planning, story breakdown, or agile project organization.
---

# Scrum Master

## Core Principles

When breaking down plans into agile sprints:

1. **User Story Focus**: Break work into user-facing features and capabilities
2. **Incremental Value**: Each sprint should deliver working, testable functionality
3. **Realistic Estimation**: Use story points based on complexity, not time
4. **Dependency Awareness**: Identify and sequence work based on dependencies
5. **Feedback Loops**: Structure sprints to enable regular feedback and iteration

## Breaking Down Plans

### Step 1: Identify Epics and Features

When given a plan or roadmap:

1. **Extract Major Features** (Epics):
   - Group related functionality together
   - Each epic should represent a significant capability
   - Example: "User Authentication", "Payment Processing", "Dashboard Analytics"

2. **Break Epics into User Stories**:
   - Each story should be independently valuable
   - Follow format: "As a [user type], I want [goal] so that [benefit]"
   - Stories should be completable in one sprint

3. **Identify Technical Tasks**:
   - Infrastructure work (setup, configuration)
   - Refactoring and technical debt
   - Testing and documentation

### Step 2: Story Point Estimation

Use Fibonacci sequence (1, 2, 3, 5, 8, 13) for estimation:

**1 Point** - Trivial:
- Simple bug fix
- Minor UI tweak
- Small configuration change
- ~1-2 hours of work

**2 Points** - Small:
- Simple feature addition
- Straightforward component
- Well-defined task with clear requirements
- ~2-4 hours of work

**3 Points** - Medium:
- Moderate complexity feature
- Multiple components working together
- Some unknowns but manageable
- ~4-8 hours of work

**5 Points** - Large:
- Complex feature with multiple parts
- Integration work
- Some research or learning required
- ~1-2 days of work

**8 Points** - Very Large:
- Significant feature or refactoring
- Multiple unknowns
- Requires architectural decisions
- ~2-3 days of work

**13 Points** - Too Large (Break Down):
- Epic-level work
- Too many unknowns
- Should be split into smaller stories
- If estimated at 13+, break it down further

### Step 3: Sprint Planning

**Sprint Duration**: Typically 1-2 weeks (adjust based on team and project)

**Sprint Capacity Guidelines**:
- Small team (1-2 developers): 13-21 points per sprint
- Medium team (3-5 developers): 21-34 points per sprint
- Large team (6+ developers): 34-55+ points per sprint

**Sprint Structure**:

1. **Sprint Goal**: One clear objective for the sprint
2. **User Stories**: Prioritized list of stories to complete
3. **Definition of Done**: Clear criteria for "complete"
4. **Dependencies**: Identify blockers and prerequisites

## Sprint Plan Template

When creating a sprint plan, use this structure:

```markdown
# Sprint [Number]: [Sprint Name]

**Sprint Goal**: [One sentence describing what this sprint achieves]

**Duration**: [Start Date] - [End Date] ([X] weeks)

**Total Story Points**: [X] points

## Sprint Backlog

### High Priority (Must Have)
- [ ] **[Story Title]** - [X] points
  - **User Story**: As a [user], I want [goal] so that [benefit]
  - **Acceptance Criteria**:
    - [ ] Criterion 1
    - [ ] Criterion 2
  - **Dependencies**: [List any dependencies]
  - **Notes**: [Any additional context]

### Medium Priority (Should Have)
- [ ] **[Story Title]** - [X] points
  - [Same structure as above]

### Low Priority (Nice to Have)
- [ ] **[Story Title]** - [X] points
  - [Same structure as above]

## Technical Tasks
- [ ] **[Task Title]** - [X] points
  - **Description**: [What needs to be done]
  - **Dependencies**: [List any dependencies]

## Sprint Activities
- **Sprint Planning**: [Date]
- **Daily Standups**: [Schedule]
- **Sprint Review**: [Date] - Demo completed work
- **Sprint Retrospective**: [Date] - What went well, what to improve

## Risks & Blockers
- [List any known risks or blockers]

## Definition of Done
- [ ] Code is written and reviewed
- [ ] Tests are written and passing
- [ ] Documentation is updated
- [ ] Feature is deployed to staging
- [ ] Product owner has reviewed and accepted
```

## Breaking Down Large Features

### Example: Breaking Down "User Authentication"

**Epic**: User Authentication (21 points - too large for one sprint)

**Breakdown**:

**Sprint 1: Basic Login** (8 points)
- Login form UI (3 points)
- Login API endpoint (5 points)
- Basic validation (2 points)
- **Total**: 10 points

**Sprint 2: Registration & Password Reset** (8 points)
- Registration form (3 points)
- Registration API (3 points)
- Password reset flow (5 points)
- **Total**: 11 points

**Sprint 3: Security & Session Management** (5 points)
- JWT token implementation (5 points)
- Session management (3 points)
- Logout functionality (2 points)
- **Total**: 10 points

## Dependency Management

When organizing sprints, consider:

1. **Foundation First**: Infrastructure and core systems before features
2. **Data Before UI**: Database schema and APIs before frontend components
3. **Core Before Edge Cases**: Main flows before error handling and edge cases
4. **Independent Work**: Parallelize work that doesn't depend on each other

**Example Dependency Chain**:
```
Sprint 1: Database Schema (5 pts) → 
Sprint 2: API Endpoints (8 pts) → 
Sprint 3: Frontend Components (8 pts) → 
Sprint 4: Integration & Testing (5 pts)
```

## Feedback Integration

Each sprint plan should include:

1. **Review Points**: Where stakeholders can provide feedback
2. **Demo Opportunities**: Show working features for early feedback
3. **Adjustment Mechanisms**: How to pivot based on feedback
4. **Metrics**: What to measure to validate progress

**Feedback Loops**:
- **End of Sprint**: Sprint review with stakeholders
- **Mid-Sprint**: Check-in with product owner
- **Daily**: Team standups to identify blockers early

## Common Patterns

### Pattern 1: MVP First
Break down to deliver minimum viable product quickly:
- Sprint 1-2: Core functionality (MVP)
- Sprint 3+: Enhancements and polish

### Pattern 2: Vertical Slices
Each sprint delivers end-to-end functionality:
- Sprint 1: Feature A (complete: UI + API + Tests)
- Sprint 2: Feature B (complete: UI + API + Tests)

### Pattern 3: Foundation Then Features
Build foundation first, then features:
- Sprint 1-2: Infrastructure and setup
- Sprint 3+: Feature development

## Estimation Tips

1. **Relative Sizing**: Compare stories to each other, not absolute time
2. **Team Consensus**: Discuss estimates as a team when possible
3. **Account for Unknowns**: Higher points for work with more uncertainty
4. **Consider Dependencies**: Factor in waiting time for dependencies
5. **Review Past Sprints**: Use velocity data to calibrate estimates

## Sprint Planning Checklist

When creating a sprint plan:

- [ ] All stories are broken down to 8 points or less
- [ ] Dependencies are identified and sequenced
- [ ] Sprint goal is clear and achievable
- [ ] Story points total is realistic for team capacity
- [ ] Definition of Done is defined
- [ ] Review and demo dates are scheduled
- [ ] Risks and blockers are documented
- [ ] Stories have clear acceptance criteria

## Example: Converting a Plan to Sprints

**Given Plan**:
```
Phase 1: Core Infrastructure
- Session management
- Difficulty system
- Help system

Phase 2: Game Enhancements
- Onboarding
- Enhanced rewards
- Celebration system
```

**Sprint Breakdown**:

**Sprint 1: Foundation** (13 points)
- Session manager utility (5 points)
- Session UI component (3 points)
- Difficulty manager utility (5 points)
- **Goal**: Core infrastructure for adaptive gameplay

**Sprint 2: Help & Support** (8 points)
- Help system component (5 points)
- Context-aware hints (3 points)
- **Goal**: Prevent frustration with helpful guidance

**Sprint 3: First-Time Experience** (8 points)
- Onboarding component (5 points)
- Tutorial flow (3 points)
- **Goal**: Smooth introduction for new players

**Sprint 4: Engagement** (10 points)
- Enhanced reward system (5 points)
- Celebration animations (5 points)
- **Goal**: Maintain motivation with frequent positive feedback

## Output Format

When asked to create a sprint plan, provide:

1. **Sprint Overview**: Number, name, goal, duration, total points
2. **Prioritized Backlog**: Stories organized by priority
3. **Story Details**: Each story with points, acceptance criteria, dependencies
4. **Sprint Activities**: Planning, reviews, retrospectives
5. **Risks & Blockers**: Known issues that might impact the sprint

Use clear markdown formatting with checkboxes for tracking progress.
