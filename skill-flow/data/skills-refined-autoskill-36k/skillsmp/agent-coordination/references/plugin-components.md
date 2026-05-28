# Plugin Components Reference

Complete reference for zero-day-dev plugin agents, skills, and commands.

## Agents (9)

### code-architect

| Property      | Value                                            |
| ------------- | ------------------------------------------------ |
| **Domain**    | Code structure, patterns, namespace organization |
| **Skills**    | project-architecture                             |
| **Model**     | inherit                                          |
| **MCP Needs** | Rarely (uses code files, not Unity operations)   |

**Use When:**

- Planning code structure
- Reviewing architecture
- Refactoring decisions
- Organizing namespaces
- Layer separation questions

**Key Outputs:** System design tables, code review checklists, namespace recommendations

---

### game-designer

| Property      | Value                                    |
| ------------- | ---------------------------------------- |
| **Domain**    | Game rules, mechanics, player experience |
| **Skills**    | zero-day-rules                           |
| **Model**     | sonnet                                   |
| **MCP Needs** | Never (advisory role only)               |

**Use When:**

- Questions about game rules
- Designing new mechanics
- Balance considerations
- Player experience decisions
- Feature validation against game design

**Key Outputs:** Rule interpretations, design recommendations, player experience analysis

---

### input-developer

| Property      | Value                                             |
| ------------- | ------------------------------------------------- |
| **Domain**    | Board SDK, touch input, piece detection           |
| **Skills**    | unity-mcp-tools                                   |
| **Model**     | inherit                                           |
| **MCP Needs** | Sometimes (for component inspection/modification) |

**Use When:**

- Touch gesture implementation
- Glyph/piece handling
- Simulator testing setup
- Contact phase handling
- Coordinate conversion

**Key Outputs:** Event flow diagrams, input implementation code, simulator testing instructions

---

### ui-ux-developer

| Property      | Value                                        |
| ------------- | -------------------------------------------- |
| **Domain**    | Layout, sizing, visual feedback, positioning |
| **Skills**    | layout-sizing                                |
| **Model**     | inherit                                      |
| **MCP Needs** | Sometimes (for visual component setup)       |

**Use When:**

- Layout calculations
- Coordinate positioning
- Visual feedback design
- Screen dimension considerations
- Player orientation optimization

**Key Outputs:** Coordinate calculations, layout specifications, visual feedback recommendations

---

### scene-builder

| Property      | Value                                   |
| ------------- | --------------------------------------- |
| **Domain**    | Unity hierarchy, GameObjects, prefabs   |
| **Skills**    | unity-mcp-tools                         |
| **Model**     | inherit                                 |
| **MCP Needs** | Always (direct Unity Editor operations) |

**Use When:**

- Creating/modifying GameObjects
- Setting up scene hierarchy
- Component configuration
- Prefab management

**Key Outputs:** Hierarchy structure, component configurations, prefab modifications

---

### test-engineer

| Property      | Value                                 |
| ------------- | ------------------------------------- |
| **Domain**    | Writing and running tests             |
| **Skills**    | unity-testing                         |
| **Model**     | inherit                               |
| **MCP Needs** | Sometimes (for running tests via MCP) |

**Use When:**

- Writing new tests
- Analyzing test failures
- Test coverage review
- Test architecture decisions

**Key Outputs:** Test code, test coverage analysis, test failure diagnosis

---

### deployment-specialist

| Property      | Value                                   |
| ------------- | --------------------------------------- |
| **Domain**    | Building APK, Board hardware deployment |
| **Skills**    | (none required)                         |
| **Model**     | inherit                                 |
| **MCP Needs** | Rarely                                  |

**Use When:**

- Building APK
- Deploying to Board hardware
- Using bdb commands
- Deployment troubleshooting

**Key Outputs:** Build instructions, deployment commands, troubleshooting steps

---

### mcp-advisor

| Property      | Value                                  |
| ------------- | -------------------------------------- |
| **Domain**    | MCP tool selection, troubleshooting    |
| **Skills**    | unity-mcp-tools                        |
| **Model**     | inherit                                |
| **MCP Needs** | Advisory (doesn't execute, recommends) |

**Use When:**

- Deciding which MCP tool groups to enable
- MCP connection troubleshooting
- Understanding MCP tool capabilities

**Key Outputs:** Tool group recommendations, troubleshooting guidance

---

### project-producer

| Property      | Value                                |
| ------------- | ------------------------------------ |
| **Domain**    | Documentation, workflow coordination |
| **Skills**    | documentation                        |
| **Model**     | inherit                              |
| **MCP Needs** | Rarely                               |

**Use When:**

- Documentation updates
- Workflow orchestration
- Quality oversight
- Compliance monitoring

**Key Outputs:** Documentation updates, workflow coordination, quality reports

---

## Skills (8 + agent-coordination)

| Skill                    | Domain                                   | Primary Agents                              |
| ------------------------ | ---------------------------------------- | ------------------------------------------- |
| **zero-day-rules**       | Game mechanics, phases, scoring          | game-designer                               |
| **project-architecture** | Namespaces, singletons, layers           | code-architect                              |
| **board-sdk**            | Touch input, pieces, contacts, simulator | input-developer                             |
| **layout-sizing**        | Screen dimensions, coordinates, SVG      | ui-ux-developer                             |
| **visual-style-guide**   | Colors, rendering order, visual design   | ui-ux-developer, scene-builder              |
| **unity-mcp-tools**      | MCP tool usage and patterns              | mcp-advisor, scene-builder, input-developer |
| **unity-testing**        | EditMode/PlayMode tests                  | test-engineer                               |
| **documentation**        | Doc conventions, CLAUDE.md maintenance   | project-producer                            |

---

## Commands (10)

### MCP Management

| Command                        | Purpose                                         |
| ------------------------------ | ----------------------------------------------- |
| `/unity-mcp-status`            | Show currently enabled tool groups              |
| `/unity-mcp-enable [groups]`   | Enable specific tool groups                     |
| `/unity-mcp-enable-all`        | Enable all tool groups                          |
| `/unity-mcp-reset`             | Disable all tools (minimal context)             |
| `/unity-mcp-scene-info [path]` | Query scene via MCP Resource (always available) |

### Development

| Command                  | Purpose                       |
| ------------------------ | ----------------------------- |
| `/start-unity-mcp`       | Start MCP server before Unity |
| `/run-unity-test [mode]` | Run Unity tests via MCP       |
| `/update-documentation`  | Update project documentation  |

### Deployment

| Command       | Purpose                      |
| ------------- | ---------------------------- |
| `/build-apk`  | Build APK for Board hardware |
| `/deploy-apk` | Deploy to Board via bdb      |

---

## MCP Tool Groups (11)

| Group       | Purpose                 | Common Agents                  |
| ----------- | ----------------------- | ------------------------------ |
| scene-read  | Inspect scene hierarchy | scene-builder, input-developer |
| scene-write | Modify scenes           | scene-builder                  |
| gameobject  | GameObject operations   | scene-builder                  |
| component   | Component operations    | scene-builder, input-developer |
| script      | Script operations       | code-architect                 |
| prefab      | Prefab operations       | scene-builder                  |
| assets      | Asset management        | scene-builder                  |
| testing     | Run Unity tests         | test-engineer                  |
| editor      | Full editor control     | scene-builder                  |
| packages    | Package management      | deployment-specialist          |
| reflection  | Advanced operations     | (rare)                         |

---

## Architecture Constraints

### Subagent Capabilities

**Subagents CAN:**

- Use MCP tools directly (when enabled by orchestrator)
- Access skills declared in their frontmatter
- Use all standard Claude Code tools (Read, Edit, Bash, etc.)

**Subagents CANNOT:**

- Execute slash commands
- Enable/disable MCP tools themselves
- Invoke the Skill tool

### MCP Workflow

```text
1. Orchestrator enables tools: /unity-mcp-enable [groups]
2. Orchestrator spawns agent with MCP-related task
3. Agent uses MCP tools directly
4. Orchestrator resets: /unity-mcp-reset
```

### MCP Resource (Always Available)

The MCP Resource "GameObject from Current Scene by Path" provides read-only scene inspection without tool enablement. Access via `/unity-mcp-scene-info {path}`.

---

## Directory Structure

```text
commands/                   # Slash commands
├── build-apk.md
├── deploy-apk.md
├── run-unity-test.md
├── start-unity-mcp.md
├── unity-mcp-enable.md
├── unity-mcp-enable-all.md
├── unity-mcp-reset.md
├── unity-mcp-scene-info.md
├── unity-mcp-status.md
└── update-documentation.md

agents/                     # Specialized agents
├── code-architect.md
├── deployment-specialist.md
├── game-designer.md
├── input-developer.md
├── mcp-advisor.md
├── project-producer.md
├── scene-builder.md
├── test-engineer.md
└── ui-ux-developer.md

skills/                     # Domain knowledge
├── agent-coordination/     # This skill
├── board-sdk/
├── documentation/
├── layout-sizing/
├── project-architecture/
├── unity-mcp-tools/
├── unity-testing/
├── visual-style-guide/
└── zero-day-rules/
```
