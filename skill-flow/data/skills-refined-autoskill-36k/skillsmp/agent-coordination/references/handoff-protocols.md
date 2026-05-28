# Handoff Protocols

Patterns for transitioning work between agents and maintaining context.

## Agent Transition Patterns

### Design → Implementation

| From           | To              | Handoff Content                                                         |
| -------------- | --------------- | ----------------------------------------------------------------------- |
| game-designer  | code-architect  | Rule specifications, design constraints, player experience requirements |
| code-architect | scene-builder   | Class design, namespace assignments, component requirements             |
| code-architect | input-developer | Event patterns, interface contracts, coordinate requirements            |
| code-architect | test-engineer   | Test scope, edge cases, coverage expectations                           |

### Investigation → Fix

| From            | To             | Handoff Content                                |
| --------------- | -------------- | ---------------------------------------------- |
| input-developer | code-architect | SDK behavior findings, event flow analysis     |
| ui-ux-developer | scene-builder  | Coordinate calculations, visual specifications |
| test-engineer   | code-architect | Failure analysis, root cause hypothesis        |

### Implementation → Verification

| From                     | To               | Handoff Content                            |
| ------------------------ | ---------------- | ------------------------------------------ |
| code-architect           | test-engineer    | Implementation details, testable behaviors |
| scene-builder            | test-engineer    | Component setup, expected hierarchy        |
| Any implementation agent | project-producer | Changes made, documentation needs          |

---

## Context Transfer Guidelines

### What to Include in Agent Prompts

1. **Previous findings** - Relevant conclusions from earlier agents
2. **Specific focus** - What this agent should investigate/implement
3. **Constraints** - Design decisions already made
4. **Agent IDs** - For potential resumption

### What NOT to Include

1. **Full conversation history** - Agents have limited context
2. **Unrelated findings** - Focus on relevant information
3. **Implementation details** from other domains

---

## Attribution Table Format

After multi-agent work, summarize with attribution:

```markdown
| Agent           | Key Finding                                        | Agent ID |
| --------------- | -------------------------------------------------- | -------- |
| input-developer | Handle Stationary phase for glyphs                 | abc123   |
| code-architect  | State belongs in GameManager, not TokenManager     | def456   |
| ui-ux-developer | NodeSnapDistance 0.5 appropriate for TokenSize 0.4 | ghi789   |
| game-designer   | Center tile cannot rotate (game rule)              | jkl012   |
```

---

## Resumption Patterns

### When to Resume an Agent

- Follow-up questions on same topic
- Expanding on previous findings
- Clarifying ambiguous results

### How to Resume

Use the agent ID from previous invocation:

```text
Resume agent [ID] to clarify [specific question]
```

### When to Start Fresh

- New topic or domain
- Different phase of work
- Agent context would be stale

---

## Parallel vs Sequential Execution

### Use Parallel When

- Agents investigate independent aspects
- No dependency between agent findings
- Gathering multiple perspectives on same problem

### Use Sequential When

- Later agent needs earlier agent's findings
- Design must be approved before implementation
- MCP tools need to be enabled first

### Example: Parallel Investigation

```text
Launch simultaneously:
- input-developer: SDK contact behavior
- ui-ux-developer: Coordinate calculations
- game-designer: Rule validation
```

### Example: Sequential Implementation

```text
1. game-designer: Validate design (wait for approval)
2. code-architect: System design (depends on #1)
3. scene-builder: Unity setup (depends on #2)
4. test-engineer: Test coverage (depends on #3)
```

---

## Cross-Domain Coordination

### Architecture Review Triggers

Always include `code-architect` when:

- Adding new classes or systems
- Modifying existing architecture
- Cross-layer changes

### Game Design Validation Triggers

Always consult `game-designer` when:

- Changes affect gameplay
- New mechanics being added
- Rule interpretations needed

### Documentation Triggers

Always include `project-producer` when:

- New patterns established
- Architecture decisions made
- Learnings worth capturing

---

## Conflict Resolution

### When Agents Disagree

1. Identify the conflict clearly
2. Determine which agent has domain authority
3. Escalate to user if genuinely ambiguous

### Domain Authority

| Domain          | Authority       |
| --------------- | --------------- |
| Game rules      | game-designer   |
| Code structure  | code-architect  |
| Visual design   | ui-ux-developer |
| SDK behavior    | input-developer |
| Unity hierarchy | scene-builder   |
| Test strategy   | test-engineer   |

---

## Common Handoff Mistakes

### Mistake: Skipping code-architect

**Problem:** Implementing without architecture review leads to layer violations.

**Solution:** Always include code-architect for implementation plans.

### Mistake: Not loading skills first

**Problem:** Agents lack domain knowledge they need.

**Solution:** Load relevant skills BEFORE launching agents.

### Mistake: Enabling MCP after agent spawn

**Problem:** Agent can't use tools that weren't enabled when it started.

**Solution:** Enable MCP tools BEFORE spawning agents that need them.

### Mistake: Not attributing findings

**Problem:** Can't trace recommendations back to source.

**Solution:** Always create attribution table after multi-agent work.

### Mistake: Resuming stale agents

**Problem:** Agent context doesn't match current state.

**Solution:** Start fresh when significant time has passed or topic has shifted.
