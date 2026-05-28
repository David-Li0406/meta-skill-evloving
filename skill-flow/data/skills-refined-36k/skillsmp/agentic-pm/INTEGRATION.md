# Integration Guide

## How this skill fits into Magic Audit's development workflow

### Workflow Position

```
User Request
    │
    ▼
┌─────────────────────────────┐
│     agentic-pm skill        │  ← Creates sprint plans, task files
│  (this skill)               │
└─────────────────────────────┘
    │
    ▼
Engineer (LLM instance) executes task
    │
    ▼
┌─────────────────────────────┐
│  senior-engineer-pr-lead    │  ← Reviews PR per PR-SOP
│  agent                      │
└─────────────────────────────┘
    │
    ▼
Merge to develop
    │
    ▼
┌─────────────────────────────┐
│ phase-retro-guardrail-tuner │  ← Retrospective, improves process
│ (sub-skill)                 │
└─────────────────────────────┘
    │
    ▼
Next sprint benefits from improvements
```

## File Locations

| Artifact | Location | Notes |
|----------|----------|-------|
| Sprint plans | `.claude/plans/<name>-sprint-plan.md` | One per sprint |
| Task files | `.claude/plans/tasks/TASK-<ID>-<slug>.md` | One per backlog item |
| Task template | `.claude/plans/templates/task-file-template.md` | Canonical template |
| Decision logs | `.claude/plans/decision-log.md` | Append-only |
| Risk registers | `.claude/plans/risk-register.md` | Per sprint or ongoing |

## Related Documentation

| Document | Location | Purpose |
|----------|----------|---------|
| PR-SOP | `.claude/docs/PR-SOP.md` | Full PR checklist (8 phases) |
| Senior Engineer Agent | `.claude/agents/senior-engineer-pr-lead.md` | Architecture standards, PR review |
| Project Guide | `CLAUDE.md` | Branching, conventions, quick reference |

## Handoff Points

### PM → Engineer

When issuing a task:
1. Task file written to `.claude/plans/tasks/TASK-<ID>-<slug>.md`
2. Engineer assignment message sent (optional)
3. Engineer creates branch: `feature/<ID>-<slug>`

### Engineer → Senior Engineer

When PR is ready:
1. Engineer completes Implementation Summary in task file
2. PR created targeting `develop`
3. Senior engineer reviews using PR-SOP

### Senior Engineer → PM (via retro)

After phase completion:
1. PM runs `phase-retro-guardrail-tuner` skill
2. Patterns identified from engineer summaries, PR notes
3. Guardrail patches proposed
4. Templates/modules updated for next phase

## Branch Strategy Alignment

This skill follows Magic Audit's GitFlow:

```
main (production)
  │
  └── PR (traditional merge)
        │
develop (integration/staging)
  │
  └── PR (traditional merge)
        │
feature/*, fix/*, claude/* (work branches)
```

### Branch Naming

| Prefix | Example | Use Case |
|--------|---------|----------|
| `feature/` | `feature/101-types` | New features |
| `fix/` | `fix/102-login-crash` | Bug fixes |
| `claude/` | `claude/103-refactor-auth` | AI-assisted development |
| `int/` | `int/phase1-core` | Integration branches (if needed) |

### Merge Policy

**CRITICAL**: Always traditional merge, never squash.

## CI Pipeline Integration

### Required Checks

All task PRs must pass:
- [ ] Test & Lint (macOS + Windows, Node 18 + 20)
- [ ] Security Audit
- [ ] Build Application

### Native Module Handling

**Known issue**: `better-sqlite3-multiple-ciphers` requires rebuild after:
- `npm install`
- Node.js version change
- Electron version change

Task files should include prerequisite commands when relevant:
```bash
npm rebuild better-sqlite3-multiple-ciphers
npx electron-rebuild
```

## Template Synchronization

The canonical task file template lives at:
```
.claude/plans/templates/task-file-template.md
```

The skill's template at `templates/task-file.template.md` should stay synchronized.

When updating templates:
1. Update the skill's template first
2. Sync to `.claude/plans/templates/task-file-template.md`
3. Document change in decision log

## LLM-Specific Considerations

### Capacity Planning

When planning for agentic engineers (LLM instances):
- Estimate complexity in tokens (using category multipliers from metrics-templates.md)
- Budget ~200K-500K tokens per phase
- Include 20% buffer for exploration

### Context Management

- Tasks sharing contracts should be sequential
- Avoid parallel tasks that modify shared types
- Use integration branches when conflicts are unavoidable

### Checkpoints

Insert human review checkpoints:
- After complex tasks (>100K tokens estimated)
- Before integration merges
- When architectural decisions arise
