---
name: create-epic
description: Use when creating new Epic documents. Groups related user stories, includes risk analysis, integration points, and story breakdown with PROBE estimation.
version: 1.0.0
---
# <!-- Powered by PRISMâ„¢ System -->

# Create Epic Task

## When to Use

- When starting a new major feature or initiative
- When grouping related user stories into a cohesive unit
- When breaking down PRD requirements into epics
- When planning multi-sprint work packages
- When defining business value delivery milestones

## Quick Start

1. Load core configuration from `core-config.yaml`
2. Identify epic source (PRD or new requirement)
3. Gather epic details (title, business value, constraints)
4. Perform risk analysis and integration mapping
5. Break down into stories with PROBE estimation
6. Generate epic document with story breakdown

## Purpose

To create a new Epic document that groups related user stories into a cohesive unit of work. Epics represent large features or initiatives that deliver significant business value and typically span multiple sprints. This task ensures epics are properly structured with clear goals, risk analysis, integration points, and a well-defined story breakdown.

## SEQUENTIAL Task Execution (Do not proceed until current Task is complete)

### 0. Load Core Configuration

- Load `../core-config.yaml` (relative to tasks folder) if it exists
- Extract key configurations: `epicLocation`, `devStoryLocation`, `prd.*`, `architecture.*`
- If config doesn't exist, use defaults: `docs/epics/` for epics, `docs/stories/` for stories

### 1. Gather Epic Information

#### 1.1 Identify Epic Source

- Check if epic is derived from an existing PRD (reference `docs/prd.md` or sharded PRD location)
- If from PRD: Extract epic details from the Epic List section
- If new epic: Gather information through elicitation

#### 1.2 Elicit Epic Details

If creating a new epic (not from PRD), gather:

- **Epic Title**: Clear, concise name describing the initiative
- **Business Value**: What value does this epic deliver?
- **Target Project/System**: Which codebase or system does this affect?
- **Priority**: High/Medium/Low
- **Dependencies**: External dependencies or prerequisites
- **Constraints**: Time, technical, or resource constraints

### 2. Analyze Current State (For Migration/Upgrade Epics)

If the epic involves migration or upgrade work:

- Scan target project for current versions and configurations
- Identify breaking changes and compatibility issues
- Document current state vs. target state
- List affected files and components

### 3. Risk Analysis

Assess and document risks:

- **Technical Risks**: Complexity, unknowns, new technologies
- **Integration Risks**: Dependencies on external systems or teams
- **Timeline Risks**: Factors that could cause delays
- **Mitigation Strategies**: How each risk will be addressed

### 4. Define Integration Points

Document how this epic integrates with:

- Existing system components
- External APIs or services
- Other epics or ongoing work
- CI/CD pipelines and deployment processes

### 5. Story Decomposition

Break the epic into user stories following these principles:

- Each story delivers a vertical slice of functionality
- Stories are sized for completion in 1-2 days (2-8 story points)
- Stories follow logical sequence (no forward dependencies)
- Include acceptance criteria for each story
- Apply PROBE estimation to each story

#### 5.1 Story Sizing Guidelines

| Size | Points | Typical Duration | Description |
|------|--------|------------------|-------------|
| XS | 1 | 1-2 hours | Trivial change, single file |
| S | 2 | 2-4 hours | Small change, few files |
| M | 3 | 4-8 hours | Moderate complexity |
| L | 5 | 1-2 days | Significant work |
| XL | 8 | 2-3 days | Complex, consider splitting |

### 6. Populate Epic Template

Create the epic document using `epic-tmpl.yaml`:

- Fill in all metadata fields
- Document goals and success criteria
- Include risk analysis results
- Add integration points
- List all stories with summaries
- Create dependency graph if stories have prerequisites

### 7. Create Story Files (Optional)

If requested, create individual story files:

- Use `story-tmpl.yaml` as the template
- Place in `{devStoryLocation}/{epic-id}/` subdirectory
- Include cross-references to parent epic
- Apply PROBE estimation to each story

### 8. Epic Completion and Review

- Review all sections for completeness
- Verify story sequencing is logical
- Ensure total story points align with epic complexity
- Generate summary for user including:
  - Epic location: `{epicLocation}/{epic-id}.md`
  - Total stories: count
  - Total story points: sum
  - Estimated duration range
  - Key risks identified
  - Recommended execution order

