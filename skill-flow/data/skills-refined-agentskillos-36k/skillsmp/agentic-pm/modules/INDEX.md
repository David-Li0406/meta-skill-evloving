# PM Skill Modules Index

**Last Updated:** 2024-12-24

This index lists all available PM skill modules. Load only the module you need for your current task.

---

## Module Reference

| Module | File | When to Use |
|--------|------|-------------|
| **Backlog Prioritization** | `backlog-prioritization.md` | Reprioritizing backlog items using MoSCoW/RICE |
| **Sprint Selection** | `sprint-selection.md` | Selecting tasks for a sprint, phase planning |
| **Project Plan** | `project-plan.md` | Assembling a complete project plan |
| **Dependency Graph** | `dependency-graph.md` | Analyzing task dependencies |
| **Task File Authoring** | `task-file-authoring.md` | Creating task files for engineers |
| **Engineer Questions** | `engineer-questions.md` | Handling engineer Q&A, scope clarification |
| **Testing & Quality** | `testing-quality-planning.md` | Planning tests and quality gates |
| **Backlog Maintenance** | `backlog-maintenance.md` | Adding items, marking complete, cleanup |
| **Sprint Management** | `sprint-management.md` | Creating/closing sprints, moving tasks |

---

## Templates

Templates are in the `templates/` directory:

| Template | File | Purpose |
|----------|------|---------|
| Sprint Plan | `sprint-plan.template.md` | Sprint planning document |
| Task File | `task-file.template.md` | Engineer task assignment |
| Testing Plan | `testing-quality-plan.template.md` | Quality and test planning |
| Risk Register | `risk-register.template.md` | Risk tracking |
| Decision Log | `decision-log.template.md` | Decision documentation |
| Engineer Assignment | `engineer-assignment-message.template.md` | Task assignment message |
| Testing Expectations | `testing-expectations.template.md` | Test requirements |

---

## Guardrails

Guardrails are validation checks in `guardrails/`:

| Guardrail | File | Purpose |
|-----------|------|---------|
| Plan Completeness | `plan-completeness-check.md` | Validates plan has all required elements |
| Task File Quality | `task-file-quality-check.md` | Validates task files are complete |
| Testing Sanity | `testing-sanity-check.md` | Validates testing is planned |

---

## Sub-Skills

| Sub-Skill | Directory | Purpose |
|-----------|-----------|---------|
| Phase Retrospective | `skills/phase-retro-guardrail-tuner/` | End-of-phase retrospectives and guardrail tuning |

---

## Usage Pattern

```markdown
1. Identify the PM activity needed
2. Load the appropriate module from this index
3. Follow the module's instructions
4. Use templates as needed
5. Run guardrails before finalizing
```

---

## Related Documentation

| Document | Location |
|----------|----------|
| PM Agent Config | `.claude/agents/agentic-pm.md` |
| Main PM Skill | `.claude/skills/agentic-pm/SKILL.md` |
| Plan-First Protocol | `.claude/docs/shared/plan-first-protocol.md` |
| Metrics Templates | `.claude/docs/shared/metrics-templates.md` |
