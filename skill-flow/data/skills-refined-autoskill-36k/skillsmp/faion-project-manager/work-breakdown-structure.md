---
id: work-breakdown-structure
name: "Work Breakdown Structure (WBS)"
domain: PM
skill: faion-project-manager
category: "project-management"
---

# Work Breakdown Structure (WBS)

## Metadata
- **Category:** Project Management Framework 7 - Planning Performance Domain
- **Difficulty:** Beginner
- **Tags:** #product, #methodology, #pmbok
- **Read Time:** 7 min
- **Agent:** faion-pm-agent

---

## Problem

Without structured planning, projects face:
- Scope creep from undefined boundaries
- Missed deliverables discovered too late
- Inaccurate estimates from unclear work
- Team confusion about what to build

## Framework

### What is WBS?

A Work Breakdown Structure breaks the project into smaller, manageable pieces:

```
Project
├── Phase 1: Discovery
│   ├── 1.1 Research
│   │   ├── 1.1.1 User interviews
│   │   └── 1.1.2 Competitor analysis
│   └── 1.2 Requirements
│       ├── 1.2.1 Functional specs
│       └── 1.2.2 Technical specs
└── Phase 2: Development
    ├── 2.1 Frontend
    └── 2.2 Backend
```

### Step 1: Start with Major Deliverables

What are the main outcomes?
- Working software
- Documentation
- Training materials
- Infrastructure

### Step 2: Decompose to Work Packages

Break each deliverable into smaller pieces until you reach the "work package" level.

**Work Package Criteria:**
- Assignable to one person/team
- Estimable (8-80 hours rule)
- Measurable completion
- Produces a tangible output

### Step 3: Create WBS Dictionary

For each work package, document:

| Element | Description |
|---------|-------------|
| ID | Unique identifier (1.2.3) |
| Name | Clear, action-oriented |
| Description | What's included/excluded |
| Acceptance Criteria | How to know it's done |
| Owner | Who's responsible |
| Estimate | Time/cost |
| Dependencies | What must come before |

### Step 4: Validate with 100% Rule

The 100% Rule: Each level must represent 100% of the parent.

**Example:**
- Project (100%)
  - Development (40%)
  - Testing (20%)
  - Documentation (15%)
  - Deployment (15%)
  - Training (10%)
  = 100%

---

## Templates

### WBS Template (Hierarchical)

```markdown
## WBS - [Project Name]

### 1.0 Project Management
- 1.1 Project planning
- 1.2 Status reporting
- 1.3 Risk management
- 1.4 Change control

### 2.0 Requirements
- 2.1 User research
  - 2.1.1 Interview 10 users
  - 2.1.2 Survey analysis
- 2.2 Requirement documentation
  - 2.2.1 User stories
  - 2.2.2 Acceptance criteria

### 3.0 Design
- 3.1 UX design
- 3.2 UI design
- 3.3 Technical architecture

### 4.0 Development
- 4.1 Frontend
- 4.2 Backend
- 4.3 Integration

### 5.0 Testing
- 5.1 Unit testing
- 5.2 Integration testing
- 5.3 User acceptance testing

### 6.0 Deployment
- 6.1 Environment setup
- 6.2 Release
- 6.3 Monitoring
```

### WBS Dictionary Entry

```markdown
## WBS Element: 2.1.1 Interview 10 users

| Field | Value |
|-------|-------|
| **ID** | 2.1.1 |
| **Parent** | 2.1 User research |
| **Description** | Conduct 30-min interviews with target users |
| **Acceptance Criteria** | 10 interviews completed, notes documented |
| **Owner** | UX Researcher |
| **Estimate** | 20 hours |
| **Dependencies** | Interview guide approved (2.1.0) |
| **Deliverable** | Interview transcripts, summary report |
```

---

## Examples

### Example 1: MVP Launch WBS

```
MVP Launch
├── 1.0 Planning (Week 1)
│   ├── 1.1 Define scope
│   ├── 1.2 Create timeline
│   └── 1.3 Assign resources
├── 2.0 Core Features (Weeks 2-6)
│   ├── 2.1 User authentication
│   ├── 2.2 Main dashboard
│   ├── 2.3 Core workflow
│   └── 2.4 Settings page
├── 3.0 Quality (Week 7)
│   ├── 3.1 Testing
│   ├── 3.2 Bug fixes
│   └── 3.3 Performance
├── 4.0 Launch (Week 8)
│   ├── 4.1 Production deploy
│   ├── 4.2 Monitoring setup
│   └── 4.3 Launch announcement
```

### Example 2: Solopreneur Content Product WBS

```
Online Course
├── 1.0 Content Creation
│   ├── 1.1 Outline (5 modules)
│   ├── 1.2 Lesson scripts
│   ├── 1.3 Video recording
│   └── 1.4 Worksheets
├── 2.0 Platform Setup
│   ├── 2.1 Teachable account
│   ├── 2.2 Course structure
│   └── 2.3 Payment integration
├── 3.0 Marketing
│   ├── 3.1 Sales page
│   ├── 3.2 Email sequence
│   └── 3.3 Social promo
└── 4.0 Launch
    ├── 4.1 Beta testers
    ├── 4.2 Feedback iteration
    └── 4.3 Public launch
```

---

## Common Mistakes

1. **Too detailed too early** - Start high-level, detail later
2. **Verb-based instead of noun-based** - WBS shows deliverables, not activities
3. **Missing the 100% rule** - Leaves gaps in scope
4. **No WBS dictionary** - Details get lost
5. **Treating WBS as schedule** - WBS shows what, not when

---

## Related Methodologies

- **Schedule Development:** Timeline planning from WBS
- **Cost Estimation:** Budget planning from work packages
- **Requirements Traceability:** Linking requirements to deliverables

---

*Methodology from Project Management Framework 7 - Planning Performance Domain*
