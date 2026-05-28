# Workflow Patterns

Common workflow sequences for different task types in Zero-Day Attack development.

## Bug Investigation

### Pattern: Diagnostic → Implementation

```text
1. Identify bug domain (input? visual? logic?)
2. Load relevant skill(s)
3. Launch diagnostic agent(s)
4. Analyze findings
5. Launch implementation agent (usually code-architect)
6. Test fix
```

### Example: Token not snapping to position

| Step | Action                                         |
| ---- | ---------------------------------------------- |
| 1    | Load `board-sdk`, `layout-sizing`              |
| 2    | Launch `input-developer` (contact handling)    |
| 3    | Launch `ui-ux-developer` (coordinate math)     |
| 4    | Synthesize findings                            |
| 5    | Launch `code-architect` for fix implementation |
| 6    | Test with simulator                            |

---

## Feature Implementation

### Pattern: Design → Architecture → Implementation → Test

```text
1. Load domain skill(s)
2. Consult game-designer (if gameplay-affecting)
3. Launch code-architect for design
4. Launch implementation agent(s)
5. Launch test-engineer
6. Update documentation
```

### Example: Adding scoring system

| Step | Action                                        |
| ---- | --------------------------------------------- |
| 1    | Load `zero-day-rules`, `project-architecture` |
| 2    | Launch `game-designer` for rules validation   |
| 3    | Launch `code-architect` for system design     |
| 4    | Implement based on design                     |
| 5    | Launch `test-engineer` for test coverage      |
| 6    | Launch `project-producer` for docs            |

---

## Unity Scene Work

### Pattern: Enable MCP → Scene Operations → Reset

```text
1. Run /unity-mcp-enable [groups]
2. Launch scene-builder or input-developer
3. Agent performs Unity operations
4. Run /unity-mcp-reset
```

### Example: Setting up new prefab

| Step | Action                                       |
| ---- | -------------------------------------------- |
| 1    | `/unity-mcp-enable gameobject prefab assets` |
| 2    | Launch `scene-builder`                       |
| 3    | Agent creates/modifies prefab                |
| 4    | `/unity-mcp-reset`                           |

---

## Layout/Visual Work

### Pattern: Coordinates → Visual Design → Implementation

```text
1. Load layout-sizing, visual-style-guide
2. Launch ui-ux-developer for calculations
3. Launch scene-builder for Unity setup (if needed)
4. Verify with code-architect
```

### Example: Positioning new UI element

| Step | Action                                       |
| ---- | -------------------------------------------- |
| 1    | Load `layout-sizing`, `visual-style-guide`   |
| 2    | Launch `ui-ux-developer` for coordinate math |
| 3    | `/unity-mcp-enable gameobject component`     |
| 4    | Launch `scene-builder` for setup             |
| 5    | `/unity-mcp-reset`                           |

---

## Input Handling

### Pattern: SDK Understanding → Implementation → Testing

```text
1. Load board-sdk skill
2. Launch input-developer for design
3. Implement in InputManager/TokenManager
4. Test with simulator
```

### Example: Adding new gesture

| Step | Action                      |
| ---- | --------------------------- |
| 1    | Load `board-sdk`            |
| 2    | Launch `input-developer`    |
| 3    | Implement gesture detection |
| 4    | Simulator testing           |

---

## Testing

### Pattern: Coverage Analysis → Implementation → Execution

```text
1. Load unity-testing skill
2. Launch test-engineer for analysis
3. Write/update tests
4. Run tests via /run-unity-test
```

### Example: Adding test coverage

| Step | Action                                       |
| ---- | -------------------------------------------- |
| 1    | Load `unity-testing`, `project-architecture` |
| 2    | Launch `test-engineer`                       |
| 3    | Write tests                                  |
| 4    | `/run-unity-test EditMode`                   |

---

## Deployment

### Pattern: Build → Deploy → Monitor

```text
1. /build-apk
2. /deploy-apk
3. Monitor logs
```

### Example: Deploying to Board

| Step | Action                               |
| ---- | ------------------------------------ |
| 1    | `/build-apk`                         |
| 2    | `/deploy-apk`                        |
| 3    | `bdb logs com.earplay.zerodayattack` |

---

## Documentation Updates

### Pattern: Identify Changes → Update Docs

```text
1. Load documentation skill
2. Launch project-producer
3. Update relevant files
```

### Example: After adding new system

| Step | Action                                     |
| ---- | ------------------------------------------ |
| 1    | Load `documentation`                       |
| 2    | Launch `project-producer`                  |
| 3    | Update CLAUDE.md, ARCHITECTURE-ANALYSIS.md |

---

## Multi-Agent Investigation

### Pattern: Parallel Exploration → Synthesis

```text
1. Load relevant skills
2. Launch multiple agents in parallel
3. Collect findings with attribution
4. Synthesize recommendations
```

### Example: Planning token placement

| Step | Action                                                                                      |
| ---- | ------------------------------------------------------------------------------------------- |
| 1    | Load `board-sdk`, `layout-sizing`, `zero-day-rules`, `project-architecture`                 |
| 2    | Launch in parallel: `input-developer`, `ui-ux-developer`, `game-designer`, `code-architect` |
| 3    | Create attribution table                                                                    |
| 4    | Synthesize into implementation plan                                                         |

---

## Formal Planning

### Pattern: /start-planning Command Workflow

```text
1. /start-planning [task description]
2. Command guides through:
   - Skill identification
   - Agent selection
   - MCP setup (if needed)
   - Parallel agent execution
   - Result synthesis
3. Write plan file
4. Get user approval
5. Execute plan
```

Use `/start-planning` for structured planning sessions with explicit checklist and workflow.
