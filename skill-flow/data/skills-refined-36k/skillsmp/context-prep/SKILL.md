---
name: context-prep
description: Prepare optimal context package before delegating tasks to sub-agents
version: 1.0.0
author: Claude-Orch-Prime
---

# Context Preparation Skill

## Purpose

Prepare optimal context package before delegating a task to a sub-agent. This skill ensures sub-agents receive precisely the information they need — no more, no less.

## When to Use

- Before any `/delegate` command
- When spawning parallel agents via `/parallel`
- When task requires specialized agent with isolated context

## Input Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `task` | Yes | The task to delegate |
| `agent_type` | Yes | Target sub-agent type (from catalog) |
| `files` | No | Specific files to include |
| `constraints` | No | Time/scope/format constraints |

## Execution Steps

### Step 1: Analyze Task Complexity

```
TASK COMPLEXITY ASSESSMENT
─────────────────────────────────────────────────────
□ Single file operation → Minimal context
□ Multi-file operation → Include all relevant files
□ Cross-domain task → Include domain documentation
□ Decision-making task → Include decision history
□ Creative task → Include examples/patterns
```

### Step 2: Select Relevant Context

```
CONTEXT SELECTION MATRIX
─────────────────────────────────────────────────────
Agent Type        | Always Include           | Optional
──────────────────┼──────────────────────────┼─────────────
Claude-Analyst    | Requirements, user stories| Existing specs
Claude-Architect  | System docs, dependencies | Tech stack refs
Claude-Dev        | Code files, tests        | API docs
Claude-PM         | Timeline, risks          | Resource allocation
Claude-PO         | Backlog, priorities      | Stakeholder feedback
Claude-QA         | Test plans, criteria     | Bug history
Claude-Editor     | Document, terminology std | Style guide
Claude-Consolidator| All agent outputs       | Original task
```

### Step 3: Apply Context Minimization

```
MINIMIZATION RULES
─────────────────────────────────────────────────────
1. Include ONLY files mentioned in task
2. If file > 500 lines, extract relevant sections only
3. Summarize history instead of full transcripts
4. Use references ("see CLAUDE.md section X") for stable docs
5. Remove internal notes not relevant to sub-agent's task
```

### Step 4: Generate Context Package

Output format:

```markdown
## Sub-Agent Context Package

### Agent Assignment
- **Agent**: {agent_type}
- **Task ID**: {generated_uuid}
- **Parent**: {parent_agent_id}
- **Depth**: {delegation_depth}

### Task Description
{Clear, actionable task description}

### Success Criteria
- [ ] {Specific criterion 1}
- [ ] {Specific criterion 2}
- [ ] {Specific criterion N}

### Constraints
- **Scope**: {what to do / what NOT to do}
- **Format**: {expected output format}
- **Time**: {deadline if any}

### Context Files
{List of files with brief description of why included}

### Anti-Loop Check
- Chain: {Orch → ... → current}
- Same agent type in chain: {yes/no}
- Task similarity to parent: {low/medium/high}

### Escalation Trigger
Return control to parent if:
- Task cannot be completed with given context
- Loop detected
- Clarification needed from user
```

## Example Usage

**Input**:
```
/context-prep task="Analyze VKS-550 for inclusion in MVP" agent_type="Claude-PO"
```

**Output**:
```markdown
## Sub-Agent Context Package

### Agent Assignment
- **Agent**: Claude-PO
- **Task ID**: ctx-2026-01-06-001
- **Parent**: Claude-Orch-Prime
- **Depth**: 1

### Task Description
Analyze whether VKS-550 (Precificacao/Pricing) should be included in the MVP scope.
Provide recommendation with justification based on value, effort, and dependencies.

### Success Criteria
- [ ] Clear recommendation: Include / Exclude / Merge
- [ ] Impact analysis on timeline
- [ ] Dependency mapping
- [ ] Risk assessment

### Constraints
- **Scope**: Only VKS-550 decision, not re-planning entire roadmap
- **Format**: Structured recommendation with pros/cons
- **Time**: Single response

### Context Files
- `02_processed_data/roadmap_macro_2027Q3.csv` — Timeline baseline
- `03_documents/analise_critica_recursiva_2027Q3.md` — Previous analysis (section 8)
- `01_source_data/BacklogInicialVekSales_ALFA.md` — VKS-550 description

### Anti-Loop Check
- Chain: Orch-Prime → Claude-PO
- Same agent type in chain: No
- Task similarity to parent: Low (specific sub-task)

### Escalation Trigger
Return if:
- Missing business context for decision
- Conflicting requirements discovered
- Need stakeholder input
```

## Integration with Orchestrator

This skill is automatically invoked by Claude-Orch-Prime before any delegation. Sub-agents receiving a context package should:

1. Verify they have all needed context
2. Request missing info via `/escalate` if needed
3. Execute task within defined scope
4. Return structured output matching success criteria

---

*Skill created by Claude-Orch-Prime | 2026-01-06*
