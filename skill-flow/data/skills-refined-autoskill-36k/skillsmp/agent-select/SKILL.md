---
name: agent-select
description: Analyze tasks and recommend optimal sub-agent(s) for execution
version: 1.0.0
author: Claude-Orch-Prime-20260106-86fa
---

# Agent Selection Skill

## Purpose

Analyze a task and recommend the optimal sub-agent(s) for execution. Uses keyword matching, domain analysis, and task complexity assessment to select from the Sub-Agent Catalog.

## When to Use

- When orchestrator receives a new task
- Before decomposing complex tasks
- When multiple agents could handle a task (tiebreaker)

## Agent Selection Matrix

```
┌────────────────────────────────────────────────────────────────────────┐
│  AGENT SELECTION BY TASK KEYWORDS                                      │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  KEYWORDS                          │  RECOMMENDED AGENT                │
│  ──────────────────────────────────┼───────────────────────────────── │
│  analyze, requirements, gaps,      │  Claude-Analyst                   │
│  user story, acceptance criteria   │                                   │
│  ──────────────────────────────────┼───────────────────────────────── │
│  architecture, design, system,     │  Claude-Architect                 │
│  dependencies, integration, API    │                                   │
│  ──────────────────────────────────┼───────────────────────────────── │
│  code, implement, fix, test,       │  Claude-Dev                       │
│  refactor, debug, function         │                                   │
│  ──────────────────────────────────┼───────────────────────────────── │
│  timeline, schedule, risk,         │  Claude-PM                        │
│  resource, plan, milestone         │                                   │
│  ──────────────────────────────────┼───────────────────────────────── │
│  priority, value, backlog,         │  Claude-PO                        │
│  scope, MVP, feature, roadmap      │                                   │
│  ──────────────────────────────────┼───────────────────────────────── │
│  test, quality, validation,        │  Claude-QA                        │
│  coverage, bug, regression         │                                   │
│  ──────────────────────────────────┼───────────────────────────────── │
│  deploy, CI/CD, infrastructure,    │  Claude-DevOps                    │
│  pipeline, container, cloud        │                                   │
│  ──────────────────────────────────┼───────────────────────────────── │
│  UX, UI, design, flow, user,       │  Claude-UX                        │
│  interface, prototype, usability   │                                   │
│  ──────────────────────────────────┼───────────────────────────────── │
│  legal, contract, compliance,      │  Claude-Legal                     │
│  regulation, LGPD, terms           │                                   │
│  ──────────────────────────────────┼───────────────────────────────── │
│  document, write, edit, review,    │  Claude-Editor                    │
│  terminology, clarity, format      │                                   │
│  ──────────────────────────────────┼───────────────────────────────── │
│  executive, CEO, summary,          │  Claude-CEO                       │
│  strategy, ROI, business case      │                                   │
│  ──────────────────────────────────┼───────────────────────────────── │
│  consolidate, merge, compile,      │  Claude-Consolidator              │
│  synthesize, combine outputs       │                                   │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

## Multi-Agent Selection (Parallel Execution)

When task requires multiple perspectives:

```
┌────────────────────────────────────────────────────────────────────────┐
│  PARALLEL AGENT PATTERNS                                               │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  PATTERN: Multi-Perspective Analysis                                   │
│  Trigger: "analyze from multiple perspectives", "comprehensive review" │
│  Agents: [Analyst, Architect, PM, PO, QA, DevOps] + Consolidator      │
│                                                                        │
│  PATTERN: Document Review                                              │
│  Trigger: "review document", "check terminology"                       │
│  Agents: [Editor, Legal, QA] + Consolidator                           │
│                                                                        │
│  PATTERN: Technical Decision                                           │
│  Trigger: "technical decision", "architecture choice"                  │
│  Agents: [Architect, Dev, DevOps] + Consolidator                      │
│                                                                        │
│  PATTERN: Feature Evaluation                                           │
│  Trigger: "evaluate feature", "scope decision"                         │
│  Agents: [PO, Analyst, PM] + Consolidator                             │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

## Selection Algorithm

```python
def select_agent(task_description: str) -> list[str]:
    """
    Pseudo-code for agent selection logic
    """
    keywords = extract_keywords(task_description)
    scores = {}

    for agent in AGENT_CATALOG:
        score = calculate_keyword_match(keywords, agent.keywords)
        score += calculate_domain_match(task_description, agent.domain)
        score += calculate_complexity_match(task_description, agent.complexity_range)
        scores[agent.id] = score

    # If multiple agents score similarly, check for parallel pattern
    if requires_parallel_execution(task_description):
        return get_parallel_pattern_agents(task_description)

    # Single agent selection
    return [max(scores, key=scores.get)]
```

## Output Format

```markdown
## Agent Selection Result

### Task Analysis
- **Task**: {task_description}
- **Keywords detected**: {keyword_list}
- **Domain**: {detected_domain}
- **Complexity**: {low|medium|high}

### Recommendation

| Priority | Agent | Match Score | Reason |
|----------|-------|-------------|--------|
| 1 | {agent_id} | {score}% | {reason} |
| 2 | {agent_id} | {score}% | {reason} |

### Execution Mode
- [ ] Single agent (primary recommendation)
- [ ] Parallel agents (multi-perspective pattern)
- [ ] Sequential chain (dependent tasks)

### Suggested Delegation
```
/delegate {agent_id} "{refined_task_description}"
```
```

## Example Usage

**Input**:
```
/agent-select task="Review the MVP roadmap for timeline risks and dependencies"
```

**Output**:
```markdown
## Agent Selection Result

### Task Analysis
- **Task**: Review the MVP roadmap for timeline risks and dependencies
- **Keywords detected**: roadmap, timeline, risks, dependencies
- **Domain**: Project Management + Architecture
- **Complexity**: Medium

### Recommendation

| Priority | Agent | Match Score | Reason |
|----------|-------|-------------|--------|
| 1 | Claude-PM | 85% | "timeline", "risks" - core PM domain |
| 2 | Claude-Architect | 70% | "dependencies" - technical analysis |

### Execution Mode
- [x] Single agent (primary recommendation)
- [ ] Parallel agents
- [ ] Sequential chain

### Suggested Delegation
```
/delegate Claude-PM "Review the MVP roadmap for timeline risks and dependencies, focusing on critical path analysis and risk mitigation strategies"
```
```

## Integration

This skill is used by:
- Claude-Orch-Prime (orchestrator) for initial task routing
- Any sub-agent before re-delegating (anti-loop check)

---

*Skill created by Claude-Orch-Prime-20260106-86fa | 2026-01-06*
