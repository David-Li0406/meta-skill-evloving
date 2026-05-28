---
name: anti-conflict
description: Prevent file conflicts between multiple AI agents working in parallel
version: 3.2.0
---

# Anti-Conflict Protocol Skill

## Purpose

Prevent file conflicts between multiple AI agents working in parallel. Implements a 7-phase workflow with mandatory worktree usage, lock files, and QA validation.

## When to Use

- At session start (Phase 1)
- Before any file edit (Phase 2)
- When editing coordination-required files (Phase 3)
- Before commits (Phase 4)
- During long sessions (Phase 5)
- At session end (Phase 6)
- Before closing session (Phase 7)

## 7-Phase Protocol

### Phase 1: Session Start
```bash
git worktree list              # Check active worktrees
cat .worktrees/tasks.md        # Check IN_PROGRESS tasks
cat .worktrees/sessions.json   # Check active sessions
ls .worktrees/*.lock           # Check lock files
git status                     # Check uncommitted changes
git log --oneline -3           # Verify expected state
```

### Phase 1.2: Worktree Creation (Mandatory)
```bash
git worktree add .worktrees/{agent-hex}-{feature} -b {tipo}/{name}
cd .worktrees/{agent-hex}-{feature}
```

### Phase 1.5: Lock File Protocol
For protected files (CLAUDE.md, README.md, CSVs):
1. Create lock: `cp .worktrees/session_lock.template.json .worktrees/{id}.lock`
2. Update heartbeat every 15 min
3. Remove lock when done
4. Stale detection: >30 min without heartbeat

### Phase 2: Pre-Edit Validation
```bash
git status --short | grep {file}
# M or MM → DO NOT EDIT (another agent working)
# ?? or CLEAN → Safe to edit
```

### Phase 3: Coordination-Required Files
High-risk files requiring explicit coordination:
- CLAUDE.md
- README.md
- 02_processed_data/*.csv
- .worktrees/tasks.md

### Phase 4: Commit Discipline
- ALWAYS: `git add {specific-files}` (NEVER `git add .`)
- Atomic commits (one purpose per commit)
- Include agent: `tipo(escopo): desc - Agent: {name}`

### Phase 5: Frequent Integration
For sessions >1 hour:
```bash
git fetch origin
git log HEAD..origin/main --oneline
```

### Phase 6: Session End
1. Commit all pending changes
2. Update tasks.md: IN_PROGRESS → COMPLETED
3. Decide: keep or remove worktree
4. Sign modified documents

### Phase 7: QA Validation (Mandatory)
Before closing session:
1. Spawn Claude-QA-{prime-hex}-final
2. Provide list of completed tasks
3. Wait for validation report
4. Register QA result in sessions.json

## QA Checklist
- [ ] Commits realizados (git log)
- [ ] Arquivos modificados consistentes
- [ ] tasks.md atualizado
- [ ] sessions.json sem inconsistências
- [ ] Documentos assinados
- [ ] Worktrees limpos
- [ ] Nenhum arquivo órfão ou conflito

---

*Skill based on Anti-Conflict Protocol v3.2 | multi-agent-os*
