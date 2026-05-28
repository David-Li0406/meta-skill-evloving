---
name: Agent Coordination
description: |
  This skill should be used when working on the Zero-Day Attack Unity project.
  Provides guidance for coordinating specialized agents across ALL development
  activities including bug investigation, implementation, design exploration,
  architecture decisions, Unity/MCP integration, and multi-phase planning.

  Trigger phrases: "fix this bug", "implement", "design", "investigate",
  "refactor", "review", "plan", "coordinate", "which agent", "help me with",
  "explore the codebase", or any development work on this Unity game project.
version: 0.3.0
---

# Agent Coordination for Zero-Day Attack

This skill provides guidance for selecting and coordinating agents and skills when working on Zero-Day Attack. For structured planning workflows, use the `/start-planning` command.

## Available Agents

| Agent                     | Domain                                     | Best Skills to Load First         |
| ------------------------- | ------------------------------------------ | --------------------------------- |
| **code-architect**        | Code structure, patterns, layer separation | project-architecture              |
| **game-designer**         | Game rules, mechanics, player experience   | zero-day-rules                    |
| **ui-ux-developer**       | Layout, sizing, visual feedback            | layout-sizing, visual-style-guide |
| **input-developer**       | Board SDK, touch input, piece detection    | board-sdk                         |
| **scene-builder**         | Unity hierarchy, GameObjects, prefabs      | unity-mcp-tools                   |
| **test-engineer**         | Writing and running tests                  | unity-testing                     |
| **deployment-specialist** | Building APK, Board deployment             | (none required)                   |
| **mcp-advisor**           | MCP tool selection, troubleshooting        | unity-mcp-tools                   |
| **project-producer**      | Documentation, workflow coordination       | documentation                     |

## Available Skills

| Skill                    | Domain                                   | Relevant Agents                          |
| ------------------------ | ---------------------------------------- | ---------------------------------------- |
| **zero-day-rules**       | Game mechanics, phases, scoring          | game-designer, code-architect            |
| **project-architecture** | Namespaces, singletons, layers           | code-architect, any implementation agent |
| **board-sdk**            | Touch input, pieces, contacts, simulator | input-developer, code-architect          |
| **layout-sizing**        | Screen dimensions, coordinates, SVG      | ui-ux-developer, scene-builder           |
| **visual-style-guide**   | Colors, rendering order, visual design   | ui-ux-developer, scene-builder           |
| **unity-mcp-tools**      | MCP tool usage and patterns              | mcp-advisor, scene-builder               |
| **unity-testing**        | EditMode/PlayMode tests                  | test-engineer, code-architect            |
| **documentation**        | Doc conventions, CLAUDE.md maintenance   | project-producer                         |

## Agent Selection by Context

Agents trigger automatically based on context:

| When Working On              | Primary Agent         | Supporting Agents                |
| ---------------------------- | --------------------- | -------------------------------- |
| Architecture decisions       | code-architect        | game-designer                    |
| Game rules or mechanics      | game-designer         | code-architect                   |
| Token or tile implementation | code-architect        | input-developer, ui-ux-developer |
| Touch/glyph handling         | input-developer       | code-architect                   |
| Layout or positioning        | ui-ux-developer       | code-architect                   |
| Unity scene hierarchy        | scene-builder         | mcp-advisor                      |
| Writing tests                | test-engineer         | code-architect                   |
| Build or deployment          | deployment-specialist | -                                |
| MCP issues or tool selection | mcp-advisor           | -                                |
| Documentation updates        | project-producer      | -                                |

**Note:** For any implementation work, include `code-architect` to ensure proper layer separation and architectural consistency.

## Skill and Agent Pairing Examples

**Bug in token placement:**

- Load: `board-sdk`, `project-architecture`
- Agents: `input-developer` (SDK behavior), `code-architect` (state flow)

**New game feature:**

- Load: `zero-day-rules`, `project-architecture`
- Agents: `game-designer` (rules), `code-architect` (implementation)

**Visual/layout issue:**

- Load: `layout-sizing`, `visual-style-guide`
- Agents: `ui-ux-developer` (visuals), `code-architect` (if code changes needed)

**Unity scene work:**

- Load: `unity-mcp-tools`
- Agents: `scene-builder` (hierarchy), `mcp-advisor` (tool selection)
- Enable MCP tools first: `/unity-mcp-enable scene-read gameobject`

**Writing tests:**

- Load: `unity-testing`, `project-architecture`
- Agents: `test-engineer`

## Technical Notes

### Subagent Capabilities

**Subagents CAN:**

- Use MCP tools directly when enabled by orchestrator
- Access skills declared in their frontmatter
- Use standard Claude Code tools (Read, Edit, Bash, etc.)

**Subagents CANNOT:**

- Execute slash commands
- Enable/disable MCP tools

### MCP Tool Workflow

1. Orchestrator enables tools with this command: `/unity-mcp-enable [groups]`
2. Spawn agent with MCP-related task
3. Agent uses MCP tools directly
4. Orchestrator resets toools with this commmand: `/unity-mcp-reset`

### Agent Results

After agents complete, consider:

- Which agent provided which insight (attribution)
- Agent IDs for potential resumption
- Consensus or conflicts among findings

## Commands

| Command                      | Purpose                        |
| ---------------------------- | ------------------------------ |
| `/start-planning [task]`     | Structured planning workflow   |
| `/unity-mcp-enable [groups]` | Enable MCP tools before agents |
| `/unity-mcp-reset`           | Disable MCP tools after work   |
| `/update-documentation`      | Document changes               |

## Reference Files

- **`references/plugin-components.md`** - Full component reference
- **`references/workflow-patterns.md`** - Example workflow sequences
- **`references/handoff-protocols.md`** - Agent transition patterns
