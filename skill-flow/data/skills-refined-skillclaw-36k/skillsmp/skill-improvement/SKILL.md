---
name: skill-improvement
description: MCP-based skill improvement during retrospective - research and update agent skills
category: coordination
depends-on: [retrospective]
---

# Skill Improvement Skill

> "Continuous learning – improve ALL agent capabilities based on real-world experience."

## MANDATORY: Skill Improvement After Every Retrospective

**This is NOT optional.** After synthesizing every retrospective, you MUST:

1. **ALWAYS** set `currentTask.status` to `"skill_research"`
2. **RESEARCH** using MCP tools from these sources:
   - https://github.com/bmad-code-org/BMAD-METHOD
   - https://agents.md/
   - https://agent-skills.md/
   - WebSearch for relevant patterns
3. **UPDATE** at least ONE skill file for EACH agent (PM, Developer, QA, Game Designer):
   - `agents/*/AGENT.md` (process improvement)
   - `agents/*/skills/*.md` (knowledge addition)
   - `agents/*/SKILLS.md` (core competencies)
   - `.claude/settings.*.json` (MCP tool configuration)
4. **COMMIT** the improvements
5. **ONLY THEN** set `currentTask = null` and assign next task

**Minimum per retrospective**: At least **FIVE** skill files updated (one per agent: PM, Developer, Tech Artist, QA, Game Designer).

**PM Self-Improvement**: The PM MUST also improve at least ONE of its OWN skills each retrospective. See [pm-self-improvement.md](./pm-self-improvement.md).

---

## When to Use This Skill

Use during `skill_research` phase when:

- A task revealed knowledge gaps in ANY agent's skills
- New patterns or anti-patterns were discovered
- External references could improve success rate
- Agent struggled with a specific domain (R3F, physics, shaders, design)
- PM coordination needs improvement

## Quick Start

```markdown
## Retrospective: Skill Improvement Check

1. Identify skill gaps for ALL FIVE agents (PM, Developer, Tech Artist, QA, Game Designer)
2. Use MCP (WebSearch, fetch) to research best practices
3. Update at least ONE skill file per agent
4. PM must improve at least ONE of its own skills
5. Document changes in action items
```

## Agent Skill Priority Matrix

Use this matrix to identify which skills to improve for each agent:

| Agent | Skill Areas to Improve | When to Trigger |
|-------|------------------------|-----------------|
| **PM** | task-selection.md, retrospective.md, prd-reorganization.md, pm-self-improvement.md, git-worktree-coordination.md, AGENT.md | Task assignment issues, retrospective gaps, PRD not reorganized, agent workspace conflicts |
| **Developer** | r3f-fundamentals.md, feedback-loops.md, typescript-patterns.md, r3f-physics.md, AGENT.md | Code quality issues, failed builds, type errors, worktree violations |
| **Tech Artist** | r3f-materials.md, shader-development.md, asset-workflow.md, visual-polish.md, AGENT.md | Visual quality issues, shader errors, asset workflow problems, worktree violations |
| **QA** | validation-workflow.md, browser-testing.md, bug-reporting.md, AGENT.md | Missed bugs, incomplete validation, test failures, build conflicts from parallel agents |
| **Game Designer** | gdd-creation.md, thermite-integration.md, playtest-validation.md, AGENT.md | GDD unclear, playtest issues, design violations |

## Decision Framework

| Signal                              | Action                                      |
| ----------------------------------- | ------------------------------------------- |
| Developer asked many clarifications | Improve Developer SKILLS.md with patterns   |
| QA missed edge cases                | Add testing patterns to QA SKILLS.md        |
| Performance issues discovered       | Research and add optimization skill         |
| New library/API used                | Create reference doc in agent's references/ |
| Anti-pattern repeated               | Add explicit anti-pattern section           |
| PM task assignment struggled        | Improve PM task-selection.md                |
| PRD not reorganized                 | Improve PM prd-reorganization.md            |
| GDD gaps in implementation          | Improve Game Designer gdd-creation.md       |
| **Build conflicts from parallel agents** | **Improve PM git-worktree-coordination.md** |
| **QA reports unexpected changes**   | **Verify agents using separate worktrees**   |

## Progressive Guide

### Level 1: Identify Skill Gaps

During retrospective synthesis, identify gaps for ALL FIVE agents:

```markdown
### Skill Gap Analysis

**PM Gaps**:

- [ ] Missing: PRD reorganization after GDD updates
- [ ] Missing: Git worktree coordination for parallel agents
- [ ] Unclear: Task prioritization algorithms
- [ ] Missing: Risk assessment procedures

**Developer Gaps**:

- [ ] Missing: R3F instancing patterns
- [ ] Missing: Git worktree setup/verification procedures
- [ ] Unclear: Shader uniform management
- [ ] Missing: TypeScript error patterns

**Tech Artist Gaps**:

- [ ] Missing: R3F material optimization patterns
- [ ] Missing: Git worktree setup/verification procedures
- [ ] Unclear: Shader performance profiling
- [ ] Missing: Asset workflow best practices

**QA Gaps**:

- [ ] Missing: WebGL performance profiling
- [ ] Unclear: Mobile device testing
- [ ] Missing: Browser compatibility patterns

**Game Designer Gaps**:

- [ ] Missing: Playtest validation procedures
- [ ] Unclear: GDD-to-PRD task extraction
- [ ] Missing: Thermite editor integration patterns

**Domain Gaps**:

- [ ] Need: Physics collision layers reference
- [ ] Need: Material comparison table
```

### Level 2: Research with MCP

Use available MCP tools to research:

```markdown
## Research Tasks

### Reference URLs to Fetch

- https://agent-skills.md/skills/Bbeierle12/Skill-MCP-Claude/r3f-fundamentals
- https://agent-skills.md/skills/wollfoo/setup-factory/threejs
- https://agent-skills.md/skills/ovachiever/droid-tings/threejs-graphics-optimizer
- https://github.com/bmad-code-org/BMAD-METHOD

### Web Search Queries

- "React Three Fiber best practices 2026"
- "Three.js mobile optimization techniques"
- "Rapier physics collision layers guide"
```

### Level 3: Update Agent Skills

Create or update skill files based on research:

**Files to Update (PICK AT LEAST ONE PER AGENT):**

**PM Agent** (MUST improve at least one):
- `agents/pm/AGENT.md` — Core PM behavior
- `agents/pm/skills/task-selection.md` — Task assignment
- `agents/pm/skills/retrospective.md` — Retrospective process
- `agents/pm/skills/prd-reorganization.md` — GDD-to-PRD extraction
- `agents/pm/skills/pm-self-improvement.md` — PM self-improvement

**Developer Agent**:
- `agents/developer/AGENT.md` — Core developer behavior
- `agents/developer/skills/r3f-fundamentals.md` — R3F patterns
- `agents/developer/skills/feedback-loops.md` — Development workflow
- `agents/developer/skills/typescript-patterns.md` — TypeScript best practices
- `agents/developer/skills/r3f-physics.md` — Physics integration

**QA Agent**:
- `agents/qa/AGENT.md` — Core QA behavior
- `agents/qa/skills/validation-workflow.md` — Testing process
- `agents/qa/skills/browser-testing.md` — Browser validation
- `agents/qa/skills/bug-reporting.md` — Bug documentation

**Game Designer Agent**:
- `agents/gamedesigner/AGENT.md` — Core Game Designer behavior
- `agents/gamedesigner/skills/gdd-creation.md` — GDD writing
- `agents/gamedesigner/skills/thermite-integration.md` — Thermite editor
- `agents/gamedesigner/skills/playtest-validation.md` — Playtest process

**Tech Artist Agent**:
- `agents/techartist/AGENT.md` — Core Tech Artist behavior
- `agents/techartist/skills/r3f-materials.md` — R3F materials
- `agents/techartist/skills/shader-development.md` — Shader creation
- `agents/techartist/skills/asset-workflow.md` — Asset pipeline
- `agents/techartist/skills/visual-polish.md` — Visual polish

**Shared Skills**:
- `.claude/skills/*.md` — Orchestration skills

**Update Template:**

```markdown
---
name: { { skill-name } }
description: { { one-line with triggers } }
category: { { development|validation|optimization } }
depends-on: [{ { related-skills } }]
---

# {{Skill Title}}

## When to Use

- {{trigger 1}}
- {{trigger 2}}

## Quick Start

{{minimal example}}

## Anti-Patterns

❌ **DON'T:** {{common mistake}}
✅ **DO:** {{best practice}}

## Reference

- {{external-url}} — {{description}}
```

### Level 4: Scale-Adaptive Updates

Adjust skill depth based on PRD complexity:

| PRD Size   | Skill Update Depth                        |
| ---------- | ----------------------------------------- |
| 1-5 tasks  | Minimal — add anti-patterns only          |
| 6-15 tasks | Standard — update relevant skills         |
| 16+ tasks  | Deep — create new skill files, references |

## Anti-Patterns

❌ **DON'T:**

- Skip skill improvement even if task passed
- Only improve one agent's skills
- Forget to improve PM's own skills
- Skip Game Designer skill improvements
- Update skills without verifying information
- Add duplicate content already in skills
- Create skills for one-off edge cases

✅ **DO:**

- Research before updating
- Improve skills for ALL FIVE agents
- Always improve at least one PM skill
- Verify patterns work in practice
- Cross-reference multiple sources
- Focus on reusable patterns

## Minimum Requirements Checklist

During `skill_research` phase, verify:

- [ ] At least ONE PM skill file updated (MANDATORY)
- [ ] At least ONE Developer skill file updated
- [ ] At least ONE Tech Artist skill file updated
- [ ] At least ONE QA skill file updated
- [ ] At least ONE Game Designer skill file updated
- [ ] Total: At least FIVE skill files improved
- [ ] All improvements committed to git
- [ ] Changes documented in action items

## Reference URLs for Research

### Agent Skills Directory

- https://agent-skills.md/skills/Bbeierle12/Skill-MCP-Claude/r3f-fundamentals
- https://agent-skills.md/skills/xenitV1/claude-code-maestro/game-development
- https://agent-skills.md/skills/anthropics/skills/frontend-design
- https://agent-skills.md/skills/xenitV1/claude-code-maestro/nodejs-best-practices
- https://agent-skills.md/skills/alinaqi/claude-bootstrap/nodejs-backend
- https://agent-skills.md/skills/skillcreatorai/Ai-Agent-Skills/javascript-typescript
- https://agent-skills.md/skills/samhvw8/dot-claude/3d-graphics
- https://agent-skills.md/skills/wollfoo/setup-factory/threejs
- https://agent-skills.md/skills/Bbeierle12/Skill-MCP-Claude/building-router
- https://agent-skills.md/skills/Bbeierle12/Skill-MCP-Claude/structural-physics
- https://agent-skills.md/skills/Bbeierle12/Skill-MCP-Claude/r3f-materials
- https://agent-skills.md/skills/Bbeierle12/Skill-MCP-Claude/terrain-integration
- https://agent-skills.md/skills/ovachiever/droid-tings/threejs-graphics-optimizer

### Method References

- https://github.com/bmad-code-org/BMAD-METHOD — Scale-adaptive agent methodology

## Reference

- [agents/pm/skills/retrospective.md](retrospective.md) — Retrospective process
- [agents/pm/skills/prd-reorganization.md](prd-reorganization.md) — PRD reorganization
- [agents/pm/skills/pm-self-improvement.md](pm-self-improvement.md) — PM self-improvement
- [agents/pm/skills/scale-adaptive.md](scale-adaptive.md) — Scale-adaptive planning
