---
name: create-roadmap
description: Create roadmap with phases for the project
allowed-tools:
  - Read
  - Write
  - Bash
  - AskUserQuestion
  - Glob
---

<objective>
Create project roadmap with phase breakdown.

Roadmaps define what work happens in what order. Phases map to requirements.

Run after `/ag4:define-requirements`.
</objective>

<execution_context>
@~/.claude/ag4one/references/principles.md
@~/.claude/ag4one/workflows/create-roadmap.md
@~/.claude/ag4one/templates/roadmap.md
@~/.claude/ag4one/templates/state.md
@~/.claude/ag4one/references/goal-backward.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/config.json
@.planning/REQUIREMENTS.md
@.planning/research/SUMMARY.md (if exists)
</context>

<process>

<step name="validate">
```bash
# Verify project exists
[ -f .planning/PROJECT.md ] || { echo "ERROR: No PROJECT.md found. Run /ag4:new-project first."; exit 1; }

# Verify requirements exist
[ -f .planning/REQUIREMENTS.md ] || { echo "ERROR: No REQUIREMENTS.md found. Run /ag4:define-requirements first."; exit 1; }
```
</step>

<step name="check_existing">
Check if roadmap already exists:

```bash
[ -f .planning/ROADMAP.md ] && echo "ROADMAP_EXISTS" || echo "NO_ROADMAP"
```

**If ROADMAP_EXISTS:**
Use AskUserQuestion:
- header: "Roadmap exists"
- question: "A roadmap already exists. What would you like to do?"
- options:
  - "View existing" - Show current roadmap
  - "Replace" - Create new roadmap (will overwrite)
  - "Cancel" - Keep existing roadmap

If "View existing": `cat .planning/ROADMAP.md` and exit
If "Cancel": Exit
If "Replace": Continue with workflow
</step>

<step name="create_roadmap">
Follow the create-roadmap.md workflow starting from identify_phases step.

The workflow handles:
- Loading requirements
- Phase identification mapped to requirements
- Requirement coverage validation (no orphaned requirements)
- Research flags for each phase
- Confirmation gates (respecting config mode)
- ROADMAP.md creation with requirement mappings
- STATE.md initialization
- REQUIREMENTS.md traceability update
- Phase directory creation
- Git commit
</step>

<step name="done">
```
Roadmap created:
- Roadmap: .planning/ROADMAP.md
- State: .planning/STATE.md
- [N] phases defined

---

## ▶ Next Up

**Phase 1: [Name]** — [Goal from ROADMAP.md]

`/ag4:plan-phase 1`

<sub>`/clear` first → fresh context window</sub>

---

**Also available:**
- `/ag4:discuss-phase 1` — gather context first
- `/ag4:research-phase 1` — investigate unknowns
- Review roadmap

---
```
</step>

</process>

<output>
- `.planning/ROADMAP.md`
- `.planning/STATE.md`
- `.planning/phases/XX-name/` directories
</output>

<success_criteria>
- [ ] PROJECT.md validated
- [ ] REQUIREMENTS.md validated
- [ ] All v1 requirements mapped to phases (no orphans)
- [ ] Success criteria derived for each phase (2-5 observable behaviors)
- [ ] Success criteria cross-checked against requirements (gaps resolved)
- [ ] ROADMAP.md created with phases, requirement mappings, and success criteria
- [ ] STATE.md initialized
- [ ] REQUIREMENTS.md traceability section updated
- [ ] Phase directories created
- [ ] Changes committed
</success_criteria>
