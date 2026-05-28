---
name: breaking-apart-systems
description: Use when decomposing a system into C4-model containers and components. Covers System → Container → Component with approval gates, container-type-specific questions, and design doc integration.
---

# Breaking Apart Systems

**Load `designing-software` before starting** — it provides property discovery and C4 model context this skill builds on.

## Overview

C4 decomposition turns vague system descriptions into concrete, buildable architectures. This skill guides interactive decomposition through three levels (System → Container → Component) with approval gates at each level. The output — diagrams and design decisions — integrates back into the design document's Plan section.

## When to Use

- After design doc review, before milestone identification
- When a system's internal structure is unclear
- When preparing to identify milestones for implementation
- When the Plan section lacks container/component diagrams

## Entry Point

When the user invokes `/c4-the-design`, follow this sequence:

1. **Locate the source document.** If the user provided a path, read it. If not, use `AskUserQuestion`:
   - Point to a design document with a Plan section
   - Point to an existing system/container diagram to decompose further
   - Describe a system interactively (no document)
   - Stop

2. **Create a companion diagram file.** Create `<design-doc-name>-c4-diagrams.md` next to the source document. This file will hold all Mermaid diagrams so users can view rendered output in their markdown viewer.

3. **Level 1: System Context.** Identify the system boundary, users, and external dependencies. Write to diagram file, then get user approval.

4. **Level 2: Containers.** Decompose the system into deployable units. Write to diagram file, then get user approval.

5. **Level 3: Components.** Decompose each container into internal modules. Write to diagram file, then get user approval for each container.

6. **Integrate outputs.** Ask the user how to integrate diagrams and decisions back into the design doc.

## Diagram Output Process

Mermaid diagrams cannot be rendered in terminal environments. Follow this process for each level:

1. **Write the diagram** to the companion `*-c4-diagrams.md` file
2. **Ask the user to review** by opening the file in a markdown viewer
3. **Accept feedback** and iterate on the diagram as needed
4. **Get explicit approval** before proceeding to the next level

This ensures users can actually see the rendered diagrams before approving them.

## Diagram Clarity Guidelines

Make C4 levels visually distinct in Mermaid diagrams:

**Container diagrams should**:
- Use explicit labels like "📦 CONTAINER:" in each box name
- Include technology and role in each container box
- Use color coding: blue (`#438DD5`) for system containers, gray (`#999`) for external systems
- Add a legend explaining the color scheme
- Use `style` directives to apply colors

**Example container box**:
```
CLI["📦 CONTAINER: CLI Application<br/>─────────────<br/>Technology: Python/typer<br/>Role: Command interface"]
style CLI fill:#438DD5,color:#fff
```

**Component diagrams should**:
- Use "🧩 COMPONENT:" labels to distinguish from containers
- Show which container each component belongs to via subgraph
- Include one-sentence responsibility for each component

## Core Pattern: Level-by-Level Decomposition

### Level 1: System Context

**Goal**: Define what's inside vs outside the system.

**Questions to surface**:
1. What is the system? (one sentence)
2. Who uses it? (personas)
3. What external systems does it depend on?
4. What external systems depend on it?

**Output**: System context diagram (Mermaid) showing:
- The system as a single box
- Users/personas
- External dependencies with relationship labels

**Validation**:
- [ ] System boundary is clear
- [ ] All users/personas identified
- [ ] External dependencies named and relationships labeled
- [ ] User approves before proceeding to Level 2

### Level 2: Containers

**Goal**: Identify deployable units within the system.

**Key question**: "Could this become independently deployable?"
- If yes → Container
- If no → Component (handle at Level 3)

**Questions to surface**:
1. What are the major deployable units? (apps, services, databases)
2. What's the data flow pattern? (see Data Flow Patterns below)
3. Which containers talk to external systems?
4. What protocols/formats do containers use to communicate?

**Heuristics**:
- Databases are containers (even embedded ones like SQLite, DuckDB)
- Data Access Layers are components, not containers
- "Future flexibility" that crosses deployment boundaries → container
- Code organization without deployment boundary → component

**Output**: Container diagram (Mermaid) showing:
- Each container with technology choice (e.g., "Python/typer")
- Communication arrows with protocols
- External system connections

**Validation**:
- [ ] Each container is independently deployable
- [ ] Data flow pattern identified and documented
- [ ] No premature containers (code organization masquerading as deployment units)
- [ ] User approves before proceeding to Level 3

### Level 3: Components

**Goal**: Decompose each container into internal modules.

Decompose one container at a time, getting user approval before moving to the next.

**Questions to surface**:
1. What's the organizing principle for this container? (see Container Taxonomy)
2. What components does it contain?
3. What are each component's responsibilities?
4. How do components depend on each other?

**Output**: Component diagram (Mermaid) for each container showing:
- Components with responsibilities
- Internal dependencies
- External connections (to other containers)

**Validation**:
- [ ] Components follow the organizing principle for this container type
- [ ] No "SharedUtilities" or "CommonHelpers" components
- [ ] Dependencies flow in one direction (no cycles)
- [ ] User approves before proceeding to next container

## Data Flow Patterns

Identify the data flow pattern early — it affects container and component boundaries.

| Pattern | Description | When to Use |
|---------|-------------|-------------|
| **Orchestrator** | One container coordinates others | CLI apps, API gateways |
| **Pipeline** | Data flows through containers in sequence | ETL, processing chains |
| **Hub-and-spoke** | Central container with satellite containers | Microservices with shared DB |

**Question to ask**: "Does one container coordinate all data flow, or does data flow through containers sequentially?"

## Container Taxonomy

Different container types have different organizing principles. Ask the type-specific question to identify components.

| Container Type | Organizing Question | Component Pattern |
|----------------|---------------------|-------------------|
| **User-facing** (CLI, UI) | "What does the user do?" | Command/feature components |
| **External API client** | "What operations does it perform?" | Operation-based components |
| **Data handler** | "What's the data lifecycle?" | Lifecycle stage components |
| **Service/API** | "What resources does it manage?" | Resource-based components |

### User-Facing Containers (CLI, UI)

**Organizing principle**: User actions, not internal concerns.

**Heuristic**: "If a user would describe it as a feature, it's probably a component boundary."

**Pattern**: Separate command components from infrastructure components:
- **Command components**: Map to user actions (auth, activities, export)
- **Infrastructure components**: Internal concerns (data access, transformation, caching)

Command components depend on infrastructure, not the reverse.

### External API Client Containers

**Organizing principle**: Operations, not endpoints.

**Why**: Endpoints are implementation details that change. Operations are stable domain abstractions.

**Exception**: If endpoints have fundamentally different auth/protocols, separate components may be warranted.

**Example**:
- Good: `SessionManager`, `ActivityFetcher`, `ReportFetcher` (operations)
- Bad: `LoginEndpoint`, `GraphQLEndpoint`, `RESTEndpoint` (endpoints)

### Data Handler Containers

**Organizing principle**: Data lifecycle stages.

**Question**: "What's the data lifecycle?"

| Lifecycle | Components |
|-----------|------------|
| Store raw → transform → serve | RawStore, Transformer, Repository |
| Transform → store | Transformer, Repository |
| Store and query only | Repository |

**ELT vs ETL**: If you need to preserve raw data for re-transformation, use ELT (Extract-Load-Transform). Each stage becomes a component.

### Configuration vs Runtime State

**Question to ask early**: "Is this configuration (external to the system) or runtime state (managed by the system)?"

| Type | Characteristics | Component Impact |
|------|-----------------|------------------|
| **Configuration** | External (`.env`, config files) | Component reads/verifies only |
| **Runtime state** | Managed by the system | Component needs storage, CRUD operations |

This distinction affects component responsibilities. A credentials component that just reads `.env` is simpler than one that manages credential lifecycle.

## Identifying the Real UI

**Question**: "How will humans actually interact with this data?"

The answer affects where complexity lives:
- If UI is a rich app → display logic in that container
- If UI is raw queries/exports → transformation must produce query-ready output

**Example**: When the "UI" is DuckDB queries + spreadsheet exports, the Transformer component becomes the real presentation layer. It must produce human-friendly column names, converted units, and flat structures.

## Output Integration

After completing all three levels, ask the user how to integrate outputs:

**Options**:
1. **Update the Plan section** — Add diagrams and design decisions inline
2. **Create a separate architecture document** — New `*-c4-diagrams.md` file
3. **Both** — Architecture doc with summary in Plan section

**What to integrate**:
- System context diagram
- Container diagram with responsibilities table
- Component diagrams for each container
- Data flow integration diagram (how containers/components work together)
- Design decisions with rationale
- Resolved questions

Use `AskUserQuestion` to determine placement if the Plan section structure is unclear.

## Self-Consistency Check

After completing integration, verify the C4 architecture is consistent with the design document:

1. **Containers match the Plan section's description** — Every container should appear in or align with the system overview described in the Plan.

2. **Components map to milestones** — Each milestone should have corresponding component(s) that implement it. If a milestone doesn't map to any component, either the component decomposition missed something or the milestone is out of scope.

3. **Data flows match the described workflow** — The data flow diagram should align with any workflow or sequence described in the design doc.

4. **Technology choices are consistent** — Technologies mentioned in the design doc should match container/component technology annotations.

If inconsistencies are found, ask the user whether to:
- Update the C4 diagrams to match the design doc
- Update the design doc to match the C4 analysis
- Flag as an open question for later resolution

## Anti-Patterns

| Anti-pattern | Problem | Fix |
|--------------|---------|-----|
| Decomposing before container boundaries are solid | Components assigned to wrong containers | Complete Level 2 before Level 3 |
| Organizing API clients by endpoint | Brittle to external API changes | Organize by operation |
| Creating "SharedUtilities" components | Becomes dumping ground, unclear ownership | Each component owns its utilities; refactor after 3+ duplications |
| DAL as separate container | Code organization, not deployment boundary | DAL is a component; database is the container |
| Skipping data flow pattern identification | Component boundaries won't make sense | Ask "orchestration or pipeline?" early |
| "Future flexibility" containers | Premature complexity | Only containerize if deployment boundary exists today |

## Common Mistakes

| Mistake | Why It Fails | Correct Approach |
|---------|--------------|------------------|
| Skipping System Context (Level 1) | External dependencies unclear | Always start at Level 1 |
| All-at-once decomposition | No validation checkpoints | Level-by-level with approval gates |
| Generic container names | Unclear responsibilities | Name by purpose: "Trackman Client" not "API Layer" |
| Components without responsibilities | Can't validate completeness | Every component needs a one-sentence responsibility |
| Ignoring data flow pattern | Wrong boundaries | Identify orchestration vs pipeline first |
| User-facing components by tech layer | Doesn't match user mental model | Organize by user action |

## Anti-Rationalizations

- "The system is too simple for C4" — Simple systems still have containers and components. Clarity helps even for small projects.
- "I'll figure out components during implementation" — You'll discover missing work too late. Decompose now.
- "This could become a service later" — Is it a deployment boundary today? If not, it's a component.
- "We need a shared utilities component" — You don't. Wait for duplication to actually cause pain.
- "The user provided a diagram, I'll just use it" — Validate it. User diagrams often mix levels or miss containers.

## Quick Reference

```
Level 1: System Context
  → What's inside/outside? Users? External dependencies?
  → Output: System context diagram
  → Gate: User approval

Level 2: Containers
  → "Could this be independently deployed?"
  → Identify data flow pattern (orchestration/pipeline)
  → Output: Container diagram + responsibilities
  → Gate: User approval

Level 3: Components (per container)
  → Container type → organizing question:
    - User-facing: "What does the user do?"
    - API client: "What operations?"
    - Data handler: "What's the lifecycle?"
  → Output: Component diagram + responsibilities
  → Gate: User approval per container

Integration:
  → Update Plan section OR create architecture doc
  → Include: diagrams, decisions, resolved questions
```

## Handoff

When C4 decomposition is complete:

1. Summarize the architecture (containers, components, data flow pattern)
2. Verify diagrams are integrated into the design document
3. Present the handoff instructions using the exact format below

**Handoff Instructions (present verbatim, substituting the actual filename):**

---

**C4 decomposition complete.**

Your system architecture is now defined with containers and components. The next step is refining your milestones to align with this architecture.

**Next steps:**

1. **Copy this command now** (before clearing):
   ```
   /start-milestone-review @path/to/your-design-doc.md
   ```

2. **Clear context:**
   ```
   /clear
   ```

3. **Paste and run** the command you copied in step 1

This hands off your architecture to milestone refinement, which will:
- Validate milestones cover all components
- Add job stories, descriptions, and acceptance criteria
- Ensure milestones are in correct dependency order

---

**The full workflow:**
```
/review-and-validate-design → /c4-the-design → /start-milestone-review → /build-work-plan → /execute-work-plan
```

## Summary

1. **Complete each level before proceeding.** System → Container → Component, with user approval at each gate.
2. **Containers are deployable; components are not.** DALs are components; databases are containers.
3. **Identify data flow pattern early.** Orchestration vs pipeline affects all boundaries.
4. **Use container-type-specific questions.** User-facing = user actions; API client = operations; data handler = lifecycle.
5. **No premature shared utilities.** Each component owns its code; refactor after 3+ duplications.
