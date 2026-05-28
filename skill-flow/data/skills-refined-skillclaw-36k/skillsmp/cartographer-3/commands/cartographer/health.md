---
model: sonnet
allowed-tools: Task, Glob, Grep, Read, Write, Edit, Bash(test:*), Bash(find:*), Bash(wc:*), Bash(mkdir:*), AskUserQuestion
argument-hint: [--drift-only | --structure-only | --skip-quality] [--fix] [--strict]
description: Comprehensive atlas health check (drift, structure, and quality)
---

## Context

Arguments: `/cartographer:health [OPTIONS]`
- **--drift-only** - Only check drift (paths exist, file counts match)
- **--structure-only** - Only validate structure (links valid, required fields)
- **--skip-quality** - Skip quality review (faster)
- **--fix** - Auto-fix simple issues (missing timestamps, broken links)
- **--strict** - Fail on warnings, not just errors
- **(empty)** - Run ALL checks: drift + structure + quality

Current directory: !`pwd`

## Purpose

Single command to answer: **"Is my atlas healthy?"**

Consolidates three concerns:
1. **Drift detection** - Does atlas match codebase reality?
2. **Structure validation** - Is atlas well-formed?
3. **Quality review** - Is atlas content useful?

## Workflow

### 1. Pre-flight Checks

**Verify atlas exists:**
```bash
test -d ".claude/skills/atlas" && echo "EXISTS" || echo "NOT_FOUND"
```

**If atlas not found:**
```
❌ No atlas found to validate.

Run `/cartographer:chart` to generate an atlas first.
```
**STOP** - Cannot validate non-existent atlas.

### 2. Determine Check Scope

| Flag | Drift | Structure | Quality |
|------|-------|-----------|---------|
| (default) | ✓ | ✓ | ✓ |
| `--drift-only` | ✓ | - | - |
| `--structure-only` | - | ✓ | - |
| `--skip-quality` | ✓ | ✓ | - |

### 3. Run Drift Detection (if enabled)

**Invoke auditor agent:**

Using Task tool with `agents/auditor.md`:

```
Atlas location: .claude/skills/atlas/
Schema path: .claude/skills/atlas/references/schema.yaml

Return structured audit in ---AUDIT--- format.
```

**Parse auditor output:**
- Extract summary, issues by severity
- Validate domain paths and file counts
- Detect orphan directories

### 4. Run Structure Validation (if enabled)

**Invoke atlas-validator agent:**

Using Task tool with `agents/review/atlas-validator.md`:

```
Atlas location: .claude/skills/atlas/
Validation mode: {standard|strict based on --strict flag}
```

**Parse validator output:**
- Extract errors (blocking) and warnings (advisory)
- Check reference integrity
- Validate completeness

### 5. Run Quality Review (if enabled)

**Inline quality checks (no separate agent):**

Read schema.yaml and check:

**Anti-pattern quality:**
- Each pattern has 2-4 anti-patterns
- Anti-patterns start with "Don't"
- Anti-patterns are codebase-specific (not generic)

**Generic anti-patterns to flag:**
- "Don't use any types"
- "Don't skip error handling"
- "Don't use magic numbers"
- "Don't leave unused variables"
- "Don't forget to add tests"

**Pattern completeness:**
- `keywords` present (at least 2)
- `file_convention` present
- `validation_commands` present (at least 1)
- `example_files` present (at least 2, recommended)
- `anti_patterns_summary` present (2-4, recommended)

**Verify example files exist:**
```bash
test -f "{example_file}" && echo "EXISTS" || echo "MISSING"
```

### 6. Handle Auto-Fix (if --fix)

**For each auto-fixable issue:**

| Issue Type | Auto-Fix Action |
|------------|-----------------|
| Missing timestamp | Add `generated: {current_timestamp}` |
| Missing atlas_version | Add `atlas_version: '3.0'` |
| Broken relative link | Attempt path correction |
| Missing observations.md | Create from template |
| Generic anti-pattern | Prompt for codebase-specific replacement |
| Stale example files | Remove from list or find alternatives |

**Apply fixes and report:**
```
🔧 Auto-fixed {count} issues:
- Added missing timestamp to schema.yaml
- Corrected link path in SKILL.md
```

### 7. Generate Consolidated Report

```markdown
## Atlas Health Report

**Atlas:** `.claude/skills/atlas/`
**Mode:** {Full | Drift Only | Structure Only | Skip Quality} {+ Strict if enabled}

---

### Overall Status

{🟢 Healthy | 🟡 Warning | 🔴 Critical}

| Check | Status | Summary |
|-------|--------|---------|
| Drift | ✅/⚠️/❌/⏭️ | {summary or "Skipped"} |
| Structure | ✅/⚠️/❌/⏭️ | {summary or "Skipped"} |
| Quality | ✅/⚠️/❌/⏭️ | {summary or "Skipped"} |

---

### Drift Detection {if enabled}

**Staleness:** {score}/1.0 ({days} days old)

| Domain | Path | Documented | Actual | Drift | Status |
|--------|------|------------|--------|-------|--------|
{for each domain}
| {name} | {path} | {documented} | {actual} | {drift%} | {✅|⚠️|❌} |
{/for}

{if critical/high drift issues}
#### Issues Found

**🔴 Critical:**
{list critical issues}

**🟠 High:**
{list high issues}
{/if}

---

### Structure Validation {if enabled}

| Check | Status | Details |
|-------|--------|---------|
| SKILL.md | ✅/❌ | {details} |
| schema.yaml | ✅/❌ | {details} |
| Reference Integrity | ✅/❌ | {X}/{Y} links valid |
| Completeness | ✅/❌ | {details} |

{if errors or warnings}
#### Issues Found

**Errors (must fix):**
{list errors}

**Warnings (should fix):**
{list warnings}
{/if}

---

### Quality Review {if enabled}

| Aspect | Score | Status |
|--------|-------|--------|
| Anti-Pattern Quality | {X}% codebase-specific | ✅/⚠️/❌ |
| Pattern Completeness | {X}/{Y} complete | ✅/⚠️/❌ |
| Example Coverage | {X}/{Y} with examples | ✅/⚠️/❌ |

{if quality issues}
#### Issues Found

**Generic anti-patterns (should be specific):**
{list generic anti-patterns with pattern they belong to}

**Incomplete patterns:**
| Pattern | Missing |
|---------|---------|
{list patterns with missing fields}

**Stale examples (files don't exist):**
{list stale example files}
{/if}

---

### Recommendations

{prioritized list of actions}

1. **{priority}**: {description}
   - Action: {what to do}
   - Command: `{suggested command}`

---

### Quick Actions

{based on overall status}
```

### 8. Offer Quick Actions

**If critical issues found:**
```
Use AskUserQuestion:

Critical health issues detected. How to proceed?

Options:
1. Run /cartographer:rechart now to regenerate atlas
2. Run /cartographer:health --fix to auto-fix simple issues
3. Show detailed report for manual review
4. Dismiss (acknowledge issues, continue using atlas)
```

**If warning status:**
```
Use AskUserQuestion:

Atlas has moderate issues. Recommended action?

Options:
1. Run /cartographer:health --fix to auto-fix issues
2. Run /cartographer:rechart to regenerate
3. Dismiss for now
```

---

## Status Determination

### Individual Check Status

| Status | Criteria |
|--------|----------|
| ✅ Pass | No errors, no critical/high issues |
| ⚠️ Warning | No errors, has warnings or medium issues |
| ❌ Fail | Has errors or critical issues |
| ⏭️ Skipped | Check was not run (flag excluded it) |

### Overall Status

| Status | Criteria |
|--------|----------|
| 🟢 Healthy | All enabled checks pass |
| 🟡 Warning | No failures, at least one warning |
| 🔴 Critical | Any enabled check fails |

### Strict Mode

When `--strict` is enabled:
- Warnings are treated as failures
- All recommended fields are required
- Quality thresholds are higher

---

## Quality Thresholds

| Aspect | ✅ Good | ⚠️ Warning | ❌ Fail |
|--------|---------|------------|---------|
| Anti-pattern specificity | >80% | 50-80% | <50% |
| Pattern completeness | All required + recommended | All required | Missing required |
| Example coverage | All patterns | >50% patterns | <50% patterns |
| Staleness | <30 days | 30-60 days | >60 days |
| Drift | <20% | 20-50% | >50% |

---

## Error Handling

| Error | Action | Recovery |
|-------|--------|----------|
| No atlas | Block with message | Run /cartographer:chart |
| Agent fails | Report which agent, continue others | Retry or manual inspection |
| Parse error | Report parse issue | Check atlas format manually |

## Responsibilities

**YOU (handler):**
- Verify atlas exists
- Determine check scope from flags
- Invoke agents (auditor, atlas-validator)
- Run inline quality checks
- Apply auto-fixes if requested
- Generate consolidated report
- Offer quick actions based on severity

**Auditor agent:**
- Validate paths exist
- Check file counts
- Detect orphan directories
- Calculate staleness

**Atlas-validator agent:**
- Validate document structure
- Check reference integrity
- Verify schema compliance

**You orchestrate the agents and present unified results.**

---

## Output Parsing Protocol

**See:** `references/protocols/agent-output-parsing.md` for complete parsing specifications.

### Agents Used

| Agent | Delimiter | Purpose |
|-------|-----------|---------|
| auditor | `---AUDIT---` | Drift detection (paths, counts) |
| atlas-validator | `---ATLAS-VALIDATION---` | Structure validation (links, fields) |

### Key Fields Summary

**Auditor output:**
- `summary.status` - healthy/warning/critical
- `critical_issues`, `high_issues` - Blocking problems
- `domain_status` - Per-domain validation results
- `recommendations` - Suggested actions

**Atlas-validator output:**
- `summary.status` - valid/warnings/errors
- `errors` - Blocking issues
- `warnings` - Advisory issues
- `reference_integrity` - Link validation results
- `completeness` - Field coverage stats
