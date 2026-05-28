---
name: feature-discovery
description: Conduct feature discovery and planning for new game features. Use when designing new features, planning implementations, analyzing requirements, breaking down complex features into tasks, or conducting feasibility studies for the TripleDerby racing game.
---

# Feature Discovery and Planning

## When to Use
- Planning a new game feature or capability
- Analyzing feature requirements and scope
- Breaking down complex features into implementable tasks
- Conducting feasibility studies for new mechanics
- Designing game systems (race mechanics, betting, training, etc.)

## Process

### Phase 1: Discovery
1. **Gather Context**: Ask clarifying questions about feature goals and game design intent
2. **Identify Requirements**: Document what the feature must do (functional requirements)
3. **Explore Constraints**: Understand technical, gameplay, and performance constraints
4. **Map Use Cases**: Identify player interactions and game scenarios
5. **Review Codebase**: Examine existing patterns and systems that may be affected

### Phase 2: Technical Analysis
1. **Evaluate Feasibility**: Assess technical viability within the current architecture
2. **Identify Dependencies**: Map relationships to existing systems (Race, Horse, Betting, etc.)
3. **Review Data Model**: Consider database schema changes needed
4. **Assess Integration Points**: Identify where new code connects to existing systems
5. **Consider Performance**: Evaluate impact on race simulation, UI responsiveness

### Phase 3: Planning
1. **Break Down Tasks**: Decompose the feature into concrete, implementable tasks
2. **Sequence Work**: Identify logical implementation phases and dependencies
3. **Estimate Complexity**: Note particularly complex or risky areas
4. **Create Task List**: Use TodoWrite to create a structured task breakdown
5. **Define Milestones**: Identify testable checkpoints and deliverables

### Phase 4: Documentation
1. **Write Specification**: Create clear feature requirements document
2. **Document Assumptions**: Record decisions and assumptions made during planning
3. **Define Success Criteria**: Establish how to validate the feature works correctly
4. **Reference Templates**: Use PLANNING_TEMPLATE.md and DISCOVERY_CHECKLIST.md

## Output

Create a feature specification document in `/docs/features/` that includes:

1. **Feature Summary**: One-paragraph overview
2. **Requirements**: Functional and non-functional requirements
3. **Technical Approach**: Architecture and integration points
4. **Implementation Plan**: Phased task breakdown
5. **Success Criteria**: How to validate correctness
6. **Open Questions**: Items needing further clarification

Use PLANNING_TEMPLATE.md as a starting point.

## Diagram Guidelines

**Use Mermaid for all diagrams:**

- **Architecture**: `graph TB` or `graph LR`
- **Sequences**: `sequenceDiagram`
- **State machines**: `stateDiagram-v2`
- **Data models**: `erDiagram`

Benefits: Renders in GitHub, version control friendly, no external files needed.

## Integration with Existing Systems

When planning features, consider integration with:
- **Core Entities**: Horse, Race, RaceRun, RaceRunHorse, Player
- **Services**: RaceService, simulation logic, game flow
- **Data Layer**: Entity Framework, repositories, ModelBuilderExtensions
- **Game Balance**: Stats, probabilities, progression systems

## Tools Used
- Read, Grep, Glob to explore the codebase
- TodoWrite for structured planning
- AskUserQuestion to clarify ambiguous requirements

## Next Steps

After completing discovery, use `/plan-implementation` to create a detailed implementation roadmap with TDD phases.
