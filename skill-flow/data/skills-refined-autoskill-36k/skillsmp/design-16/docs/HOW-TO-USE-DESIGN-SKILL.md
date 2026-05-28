# How to Use the /design Skill

Complete reference for all `/design` commands.

---

## Prerequisites

1. Claude Code skill loaded: Add `design.md` from the DesignOps directory to your skills
2. Scripts executable: `chmod +x enforcement/*.sh tools/*.sh`
3. Project follows Design Ops structure

---

## Commands

### /design init {project-name}

**Purpose**: Bootstrap a new Design Ops project.

**Usage**:
```bash
/design init user-dashboard
/design init healthcare-app
```

**What it creates**:
```
{project}/
├── docs/design/
│   ├── research.md (template)
│   ├── constraints.md (template)
│   ├── personas/
│   ├── journeys/
│   ├── tokens.md (template)
│   ├── specs/
│   ├── tests/
│   ├── PRPs/
│   └── retrospective.md (template)
└── CONVENTIONS.md (if codebase exists)
```

**Next steps after init**:
1. Complete research.md
2. Define constraints.md
3. Create personas and journeys
4. Define tokens
5. Write specs

---

### /design validate {spec-file} [--domain domain-file]

**Purpose**: Validate spec against invariants before PRP generation.

**Usage**:
```bash
# Universal invariants only
/design validate specs/S-001-dashboard.md

# With domain-specific invariants
/design validate specs/S-002-house.md --domain domains/physical-construction.md
```

**What it checks**:
- 10 universal invariants (always)
- Domain-specific invariants (if --domain specified)

**Output - Success**:
```
✅ No blocking violations
✅ Spec can proceed (address warnings before production)

Next: /design prp specs/S-001-dashboard.md
```

**Output - Failure**:
```
❌ 3 violations found:

Invariant #1 (Ambiguity is Invalid)
  Line 12: "process data properly"
  → Fix: Replace 'properly' with objective criteria

Spec rejected. Fix violations before generating PRP.
```

**Exit codes**:
- 0: Passed (or warnings only)
- 1: Failed (blocking violations)

---

### /design prp {spec-file} [--output path]

**Purpose**: Generate PRP from validated spec.

**Usage**:
```bash
# Auto-output to PRPs/ folder
/design prp specs/S-001-dashboard.md

# Custom output location
/design prp specs/S-001-dashboard.md --output custom/path/prp.md
```

**Process**:
1. Validates spec first (runs validator.sh)
2. Gathers context (spec, tokens, CONVENTIONS, codebase)
3. Generates PRP with confidence score
4. Runs quality check
5. Saves to PRPs/ folder

**Output**:
```
📄 Reading spec: S-001-dashboard.md
✅ Spec validation: PASSED (0 violations)

🔍 Gathering context...
   ├── tokens.md found
   ├── CONVENTIONS.md found
   └── Scanned 15 files for patterns

🔧 Generating PRP...
   ├── Template: user-feature
   ├── Requirements: 12 extracted
   └── Tasks: 23 generated

📊 Confidence Score: 8/10
   ✅ Requirement clarity: 9/10
   ✅ Pattern availability: 9/10
   ⚠️  Edge cases: 6/10

✅ PRP generated: PRPs/dashboard-prp.md
🔍 Quality score: 95/100

📝 Next: Review PRP, then implement
```

---

### /design review {spec-file} {implementation-path}

**Purpose**: Verify implementation matches spec.

**Usage**:
```bash
# Review directory
/design review specs/S-001-dashboard.md src/dashboard/

# Review specific file
/design review specs/S-001-dashboard.md src/dashboard.py
```

**What it checks**:
- Requirements coverage
- Validation commands pass
- Conventions followed
- Tests adequate
- Error handling present

**Output**:
```
📋 Reviewing implementation...

Spec: S-001-dashboard.md
Implementation: src/dashboard/

✅ Requirements Coverage: 11/12 (92%)
   ✅ Display user statistics
   ✅ Show trend charts
   ...
   ❌ MISSING: API rate limit handling

✅ Validation Commands: 5/5 passed
⚠️  Conventions: 2 violations
✅ Tests: 87% coverage

📊 Overall Score: 88/100

🔧 Recommended fixes:
   1. Add API rate limit handling
   2. Fix convention violations

Status: PASS WITH WARNINGS
```

---

### /design report {project-name}

**Purpose**: Generate project status summary.

**Usage**:
```bash
/design report user-dashboard
```

**Output**:
```
📊 Project Report: user-dashboard

Phase            Status        Notes
─────────────────────────────────────
Research         Complete      3 domains
Specs            Complete      3 specs
Validation       Passed        0 violations
PRPs             Generated     Avg confidence: 8.2/10
Implementation   In Progress   2/3 complete
Review           Pending
─────────────────────────────────────

Next: Complete S-003, run /design review
```

---

## Domain Reference

| Domain | File | Invariants | Use For |
|--------|------|------------|---------|
| Consumer | consumer-product.md | 11-15 | User-facing apps |
| Construction | physical-construction.md | 16-21 | Physical builds |
| Data | data-architecture.md | 22-26 | Databases, ETL |
| Integration | integration.md | 27-30 | APIs, services |
| Remote | remote-management.md | 31-36 | Remote teams |
| Skill Gap | skill-gap-transcendence.md | 37-43 | New tech |

---

## Tips

### Writing Specs That Pass Validation

1. **Be specific** - Use metrics, not adjectives
   - ❌ "Fast response"
   - ✅ "Response time < 200ms (p95)"

2. **Define states** - Use → notation
   - ❌ "Update preferences"
   - ✅ `prefs={} → set_theme(dark) → prefs={theme:dark}`

3. **Compile emotions** - Use := notation
   - ❌ "Users feel confident"
   - ✅ `confidence := progress_bar + success_rate + undo_button`

4. **Bound scope** - Add limits
   - ❌ "Display all records"
   - ✅ "Display records (max 1000, paginated)"

5. **Add recovery** - For destructive actions
   - ❌ "Delete user data"
   - ✅ "soft_delete(30_day_retention)"

### Maximizing Confidence Scores

High confidence (8-9) comes from:
- Crystal clear requirements
- Existing codebase patterns
- Complete test plans
- Documented edge cases
- Familiar technology

Low confidence (3-5) means:
- Do more research
- Find similar patterns
- Clarify requirements

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Command not found" | `chmod +x enforcement/*.sh` |
| Validation fails | Check violation messages, fix one at a time |
| Low confidence | Add detail to spec, find similar patterns |
| PRP missing sections | Check template, fill placeholders |

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more.

---

*For methodology details, see the main README.md*
