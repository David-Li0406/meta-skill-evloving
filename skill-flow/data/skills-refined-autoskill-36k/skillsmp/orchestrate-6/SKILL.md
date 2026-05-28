---
name: orchestrate
description: Manage development phases and quality gates. Use for starting new projects, advancing phases, and navigating the development lifecycle.
---

# Orchestrate Skill

Manage the 12-phase development lifecycle with quality gate validation.

## Usage

```
/orchestrate new-project     # Start Phase -1 (Project Identity)
/orchestrate next-phase      # Advance to next phase (validates gates)
/orchestrate [phase-name]    # Navigate directly to a phase
/orchestrate status          # Show current phase and gate status
```

## Available Phases

| Phase | Name | Primary Agent | Gate to Next |
|-------|------|---------------|--------------|
| -1 | Project Identity | - | All 5 identity fields captured |
| 0 | Brand Discovery | Product Visionary | Visual identity established |
| 1 | Conception | Product Visionary | Tech stack confirmed |
| 2 | Requirements | Requirements Analyst | All user stories defined |
| 3 | Architecture | Solution Architect | Technical design approved |
| 4 | Planning | Technical Planner | Tasks estimated and prioritized |
| 5 | Development | Software Engineer | All features implemented |
| 6 | Testing | QA Engineer | >80% coverage, tests passing |
| 7 | Security Audit | Security Auditor | No critical vulnerabilities |
| 8 | Code Review | Code Reviewer | All feedback addressed |
| 9 | Deployment | DevOps Engineer | Staging verified |
| 10 | Monitoring | SRE | Observability configured |

## Workflow

### Starting a New Project (`/orchestrate new-project`)

1. Set phase to -1 (Project Identity)
2. Present the 5 required identity questions using AskUserQuestion:

```
| # | Question | Required |
|---|----------|----------|
| 1 | What is the application name? | Yes |
| 2 | What is the company/organization name? | Yes |
| 3 | Who is the author/creator? | Yes |
| 4 | What license type? (Default: Proprietary) | Yes |
| 5 | What is the contact email? | Yes |
```

3. Update `CLAUDE-activeContext.md` with:
   - Current Phase: -1
   - Phase Name: Project Identity
   - Project Identity fields as answered
   - Session Log entry

4. After all identity fields captured, prompt to advance to Phase 0

### Advancing Phases (`/orchestrate next-phase`)

1. Read current phase from `CLAUDE-activeContext.md`
2. Check quality gate criteria for current phase
3. If gate NOT passed:
   - List unmet criteria
   - Do NOT advance
   - Suggest actions to meet criteria
4. If gate passed:
   - Advance to next phase
   - Update `CLAUDE-activeContext.md`
   - Announce the primary agent for new phase
   - Present phase-specific intake questions

### Direct Navigation (`/orchestrate [phase-name]`)

Valid phase names: `identity`, `brand`, `conception`, `requirements`, `architecture`, `planning`, `development`, `testing`, `security`, `review`, `deployment`, `monitoring`

1. Validate ALL gates from current phase to target phase
2. If any gate fails, report which gate and why
3. If all gates pass, jump to target phase
4. Update `CLAUDE-activeContext.md`

### Status Check (`/orchestrate status`)

Display:
- Current phase number and name
- Primary agent assigned
- Quality gate status (passed/pending for each)
- Active tasks count
- Parallel execution slots (available/occupied)

## Quality Gate Validation

### Gate: Identity Complete (-1 → 0)
```
Check CLAUDE-activeContext.md for:
- [ ] Application Name is not "Not Set"
- [ ] Company Name is not "Not Set"
- [ ] Author Name is not "Not Set"
- [ ] License Type is not "Not Set"
- [ ] Contact Email is not "Not Set"
```

### Gate: Brand Defined (0 → 1)
```
Check for brand deliverables:
- [ ] Color palette defined
- [ ] Typography selected
- [ ] Logo/visual identity documented
```

### Gate: Tech Selected (1 → 2)
```
Check for technology decisions:
- [ ] Application type confirmed (web, mobile, API, etc.)
- [ ] Tech stack documented
- [ ] Deployment target identified
```

### Gate: Requirements Complete (2 → 3)
```
Check setup/docs/USER_STORIES.md or equivalent:
- [ ] At least one user story defined
- [ ] Acceptance criteria included
```

### Gate: Architecture Approved (3 → 4)
```
Check setup/docs/ARCHITECTURE.md or equivalent:
- [ ] High-level design documented
- [ ] Key components identified
```

### Gate: Sprint Ready (4 → 5)
```
Check for planning artifacts:
- [ ] Tasks broken down
- [ ] At least one task ready for development
```

### Gate: Code Complete (5 → 6)
```
Check development is complete:
- [ ] All planned features implemented
- [ ] Code compiles without errors
```

### Gate: Standards Compliance (5 → 6)
```
Check code against loaded coding standards:
- [ ] Code follows CRITICAL rules from applicable standards
- [ ] No obvious violations of HIGH impact rules
- [ ] Standards compliance noted in PR descriptions

How to validate:
1. Read `.claude/config/coding-standards.json` for detection rules
2. Identify technologies from TECHSTACK.md
3. Load matching `setup/skills/*/AGENTS.md` files
4. Review code against CRITICAL and HIGH impact rules
5. Flag any violations for remediation before testing phase
```

### Gates 6-10: Testing through Monitoring
```
Check appropriate artifacts and completion status for each phase.
```

## Memory Bank Updates

On every phase transition, update `CLAUDE-activeContext.md`:

```markdown
## Current Phase

| Field | Value |
|-------|-------|
| **Phase** | [New Phase Number] |
| **Phase Name** | [Phase Name] |
| **Primary Agent** | [Agent for Phase] |
| **Started** | [ISO Timestamp] |
| **Last Updated** | [ISO Timestamp] |

## Session Log

| Timestamp | Event | Details |
|-----------|-------|---------|
| [ISO] | Phase Transition | Moved from Phase X to Phase Y |
```

## Error Handling

- If `CLAUDE-activeContext.md` doesn't exist, create it with Phase -1
- If phase number is invalid, show available phases
- If gate validation fails, provide specific actionable feedback
