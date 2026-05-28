---
name: product-planning
description: Strategic product planning skill for creating Product Requirements Documents (PRDs). This skill should be used when users want to plan new features, understand requirements, or create comprehensive product documentation before implementation begins.
---

# Product Planning

Enable strategic product planning through a structured workflow to build comprehensive Product Requirements Documents (PRDs).

## Core Workflow

Follow this sequential process when creating a PRD:

### 1. Understand & Clarify

Ask 5-7 concise clarifying questions across these domains:
- **Problem & Motivation**: What problem does this solve? Cost of NOT solving? Why now?
- **Users & Stakeholders**: Primary/secondary users?
- **End State & Success**: What does "done" look like? How measure success?
- **Scope & Boundaries**: What's explicitly OUT of scope? Adjacent features to protect?
- **Constraints & Requirements**: Performance, Security, Compatibility, Accessibility
- **Risks & Dependencies**: Technical risks, external dependencies

### 2. Explore

Use explore agents to understand:
- Architectural patterns in the codebase
- Technical constraints and dependencies
- Existing systems that may be affected
- Integration points and boundaries

### 3. Strategic Planning

Identify and document:
- **Core Components**: What systems need change?
- **Dependencies**: Map interactions between components
- **Milestones**: Logical groupings of work phases
- **Complexity**: Highlight areas requiring research

### 4. Generate Document

Create the PRD following this structure:

```
## Project Name

## 1. Problem & Motivation
- **Context**: Why are we doing this?
- User Pain Points

## 2. Success Criteria & End State
- What does success look like?
- Key User Stories / Workflows

## 3. Scope, Constraints & Risks
- In Scope / Out of Scope
- Technical Constraints (Performance, Security, etc.)
- Risks & Mitigation Strategies

## 4. High Level Implementation Strategy
- Architecture & Component Overview
- Key Technical Decisions
- Data Flow / System Diagrams (Mermaid if applicable)

## 5. Implementation Roadmap (Milestones)

### Phase 1: [Milestone Name]
- **Goal**: [Brief description]
- Key Deliverables:
  - [ ] **[Feature / Component Name]**: [Brief but clear description of the requirement or functionality. What does this achieve?]
  - [ ] **[Feature / Component Name]**: [Description...]

### Phase 2: [Milestone Name]
...
```

## Task Breakdown Guidelines

- **Focus on Logic**: Ensure the logical flow of features makes sense
- **Identify Complexity**: Highlight areas that are complex or require research
- **Milestones > Steps**: Group work into meaningful deliverables (e.g., "Backend API", "Frontend UI", "Integration")
- **Descriptive Tasks**: Every task/checkbox must have a description explaining *what* is being delivered, not just a title

## Mode Guidelines

- **READ-ONLY during planning**: Do not edit implementation files
- **EXCEPTION**: May create/update the PRD/Plan document itself
- Focus on architecture and milestones, not line-by-line code
