---
model: sonnet
allowed-tools: Task, Glob, Grep, Read, Write, Bash(git diff:*), Bash(git log:*), Bash(git status:*), Bash(mkdir:*), AskUserQuestion
argument-hint: <spec file> [--no-agents] [--sequential]
description: Review implementation against spec and patterns (outputs JSON for iteration)
---

## Context

Arguments: `/navigator:review <SPEC_FILE> [OPTIONS]`
- **<spec_file>** - Path to spec file that was implemented
- **--no-agents** - Skip multi-agent review (faster, less thorough)
- **--sequential** - Run review agents sequentially instead of parallel

Current directory: !`pwd`
Current branch: !`git branch --show-current`

## Workflow

### 1. Pre-flight Checks

**Verify atlas exists:**
```bash
test -f ".claude/skills/atlas/references/schema.yaml" && echo "EXISTS" || echo "NOT_FOUND"
```

**If atlas not found:**
```
❌ Atlas required for navigator commands.

Run `/cartographer:chart` to generate an atlas first.
```
**STOP** - Do not proceed without atlas.

**Verify spec file exists:**
```bash
test -f "{spec_file}" && echo "EXISTS" || echo "NOT_FOUND"
```

### 2. Load Context

**Read spec file:**
- Extract success criteria
- Extract pattern guides referenced
- Extract expected files (new and modified)
- Extract composition ID if present

**Load atlas files:**
- `.claude/skills/atlas/references/schema.yaml` - Unified codebase structure
- Relevant pattern guides from spec

**Extract from schema.yaml patterns section for each pattern in spec:**
- File conventions (verify files created at correct locations)
- Test conventions (verify tests created)
- Registration steps (verify registration completed)
- Validation commands (run pattern-specific checks)

**Get implementation changes:**
```bash
git diff {base_branch}...HEAD --name-only
git diff {base_branch}...HEAD --stat
```

### 3. Review Against Spec

**Check success criteria:**

For each criterion in spec:
- Verify implementation meets criterion
- Document how it's verified
- Flag any gaps

```markdown
### Success Criteria Review

| Criterion | Status | Evidence |
|-----------|--------|----------|
| {criterion 1} | ✅/❌ | {how verified} |
| {criterion 2} | ✅/❌ | {how verified} |
```

**Check expected files:**

For each file in spec "New Files" / "Existing Files":
- Verify file was created/modified
- Check file follows expected patterns

```markdown
### File Coverage

| Expected | Status | Notes |
|----------|--------|-------|
| {file1} | ✅ Created | Follows pattern |
| {file2} | ✅ Modified | Changes appropriate |
| {file3} | ❌ Missing | Not implemented |
```

### 4. Review Against Patterns

**For each pattern in spec, check against schema.yaml patterns section:**

1. **File Convention Check:**
   - Expected location: `{file_convention from schema.yaml patterns}`
   - Actual file created: {path} → ✅/❌

2. **Test Convention Check:**
   - Expected test location: `{test_convention}`
   - Test file exists: ✅/❌

3. **Registration Check:**
   - For each registration step in schema.yaml patterns:
   - {action} in `{file}` → ✅/❌

4. **Critical Conventions Check (from pattern guide):**
   - For each convention listed in pattern guide:
   - Verify implementation follows the rule
   - Classify violations by severity

5. **Anti-Pattern Check (from pattern guide):**
   - For each anti-pattern listed in pattern guide:
   - Verify implementation does NOT exhibit the anti-pattern
   - Flag any violations as tech_debt or blocker

**Severity Classification:**

| Severity | Definition | Action Required |
|----------|------------|-----------------|
| `blocker` | Breaks functionality, security issue, fails validation | Must fix before PR |
| `tech_debt` | Works but violates patterns/conventions | Should fix, can defer |
| `skippable` | Style preferences, minor improvements | Optional |

```markdown
### Pattern Adherence: {pattern_name}

**Conventions checked (from schema.yaml patterns):**
- [ ] File at correct location (`{file_convention}`) - ✅/❌
- [ ] Test at correct location (`{test_convention}`) - ✅/❌
- [ ] Registration completed in `{registration_file}` - ✅/❌

**Critical conventions (from pattern guide):**
- [ ] {convention_1} - ✅/❌ [{severity if violated}]
- [ ] {convention_2} - ✅/❌ [{severity if violated}]

**Anti-patterns avoided (from pattern guide):**
- [ ] Does NOT {anti_pattern_1} - ✅/❌ [{severity if violated}]
- [ ] Does NOT {anti_pattern_2} - ✅/❌ [{severity if violated}]

**Reference implementation comparison:**
- Compared against: `{example_file from schema.yaml patterns}`
- Follows established patterns: ✅/❌

**Issues found:**
- `{file}:{line}` - {description} [**{severity}**]
```

### 5. Multi-Agent Review (default)

**Launch review agents (parallel by default, sequential with --sequential):**

Using Task tool, spawn these agents:

1. **pattern-enforcer** (`agents/review/pattern-enforcer.md`)
   - Input: Changed files, schema.yaml
   - Output: Pattern violations with atlas references

2. **convention-checker** (`agents/review/convention-checker.md`)
   - Input: New files, schema.yaml
   - Output: Naming/location violations

3. **architecture-auditor** (`agents/review/architecture-auditor.md`)
   - Input: Changed files, schema.yaml layers
   - Output: Layer boundary violations

4. **anti-pattern-detector** (`agents/review/anti-pattern-detector.md`)
   - Input: Changed files, schema.yaml anti_patterns_summary
   - Output: Codebase-specific anti-pattern detections

**Aggregate agent findings:**

```markdown
### Multi-Agent Review Results

| Agent | Findings | Severity |
|-------|----------|----------|
| Pattern Enforcer | {count} violations | {max_severity} |
| Convention Checker | {count} violations | {max_severity} |
| Architecture Auditor | {count} violations | {max_severity} |
| Anti-Pattern Detector | {count} detections | {max_severity} |

**Total Issues:** {sum}
```

**Classify findings by severity:**
- 🔴 `error` from any agent → **Blocker**
- 🟡 `warning` from any agent → **Tech Debt**
- Recommendations → **Skippable**

### 5b. Lightweight Review (if --no-agents)

**Skip agents and do manual quality check:**

- **Readability**: Is the code clear and self-documenting?
- **Consistency**: Does it match existing codebase style?
- **Completeness**: Are edge cases handled?
- **Testing**: Are new paths tested?

**Read changed files:**
- Identify potential issues
- Note positive patterns

### 6. Check for Regressions

**Run validation commands from spec:**
```bash
{type_check_command}
{test_command}
{lint_command}
{build_command}
```

**Report results:**
```markdown
### Validation Status

| Check | Status | Details |
|-------|--------|---------|
| Type check | ✅/❌ | {errors if any} |
| Tests | ✅/❌ | {failing tests if any} |
| Lint | ✅/❌ | {violations if any} |
| Build | ✅/❌ | {errors if any} |
```

### 7. Generate Review Report

```markdown
## Navigator Review: {spec_name}

**Spec:** `{spec_file}`
**Branch:** `{current_branch}`
**Base:** `{base_branch}`
**Review Mode:** {Standard | Multi-Agent}

---

### Summary

| Category | Score | Details |
|----------|-------|---------|
| Spec Compliance | {A/B/C/F} | {X}/{Y} criteria met |
| Pattern Adherence | {A/B/C/F} | {X}/{Y} conventions followed |
| Code Quality | {A/B/C/F} | {notes} |
| Validation | {A/B/C/F} | {pass/fail counts} |

{IF multi-agent review:}
### Agent Review Summary

| Agent | Violations | Max Severity |
|-------|------------|--------------|
| Pattern Enforcer | {count} | {error/warning/none} |
| Convention Checker | {count} | {error/warning/none} |
| Architecture Auditor | {count} | {error/warning/none} |
| Anti-Pattern Detector | {count} | {error/warning/none} |

**Overall Status:** {✅ Ready for PR | ⚠️ Needs attention | ❌ Significant issues}

---

### Issue Summary by Severity

| Severity | Count | Requires Action |
|----------|-------|-----------------|
| 🔴 Blocker | {count} | Must fix before PR |
| 🟡 Tech Debt | {count} | Should fix |
| 🟢 Skippable | {count} | Optional |

---

### Detailed Findings

#### 🔴 Blockers (must fix)
{list blocker issues with file:line references}

#### 🟡 Tech Debt (should fix)
{list tech_debt issues with file:line references}

#### 🟢 Skippable (optional)
{list skippable issues}

#### ✅ Successes
{list things done well}

{IF multi-agent review:}
---

### Agent-Specific Findings

#### Pattern Enforcer
{list pattern violations with atlas references}

#### Convention Checker
{list naming/location violations}

#### Architecture Auditor
{list layer boundary violations}

#### Anti-Pattern Detector
{list codebase-specific anti-patterns detected}

---

### Success Criteria Status

{table from step 3}

---

### Pattern Adherence Details

{sections from step 4}

---

### Files Changed

```
{git diff stat output}
```

---

### Validation Results

{table from step 6}

---

### Recommendations

{if ready for PR}
**Ready for PR.** No blocking issues found.

Suggested commit message:
```
{suggested commit message based on spec}
```

{if needs attention}
**Address before PR:**
1. {issue 1}
2. {issue 2}

{if significant issues}
**Significant issues found. Please address:**
1. {critical issue 1}
2. {critical issue 2}

Consider running `/navigator:build {spec_file}` again after fixes.
```

### 8. Write JSON Output

**Create reviews directory:**
```bash
mkdir -p specs/reviews
```

**Write JSON file:** `specs/reviews/{spec-name}-review.json`

```json
{
  "success": {true if no blockers, false otherwise},
  "spec_file": "{spec_file}",
  "base_branch": "{base_branch}",
  "current_branch": "{current_branch}",
  "timestamp": "{ISO-8601 timestamp}",
  "review_mode": "{standard|multi-agent}",
  "scores": {
    "spec_compliance": "{A/B/C/F}",
    "pattern_adherence": "{A/B/C/F}",
    "code_quality": "{A/B/C/F}",
    "validation": "{A/B/C/F}",
    "overall": "{A/B/C/F}"
  },
  "issue_counts": {
    "blocker": {count},
    "tech_debt": {count},
    "skippable": {count}
  },
  "issues": [
    {
      "issue_number": 1,
      "description": "{description}",
      "location": "{file}:{line}",
      "severity": "blocker|tech_debt|skippable",
      "resolution": "{how to fix}",
      "pattern_violated": "{pattern_id or null}",
      "source_agent": "{pattern-enforcer|convention-checker|architecture-auditor|anti-pattern-detector|manual}"
    }
  ],
  "agent_results": {
    "pattern_enforcer": {
      "violations": {count},
      "max_severity": "{error|warning|none}"
    },
    "convention_checker": {
      "violations": {count},
      "max_severity": "{error|warning|none}"
    },
    "architecture_auditor": {
      "violations": {count},
      "max_severity": "{error|warning|none}"
    },
    "anti_pattern_detector": {
      "detections": {count},
      "max_severity": "{error|warning|none}"
    }
  },
  "validation_results": [
    {
      "command": "{command}",
      "status": "passed|failed",
      "error": "{error message or null}"
    }
  ],
  "success_criteria": [
    {
      "criterion": "{description}",
      "met": true|false,
      "evidence": "{how verified}"
    }
  ]
}
```

**Report JSON output:**
```
📄 Review JSON written to: specs/reviews/{spec-name}-review.json
```

### 9. Iteration Loop Support

**If blockers exist, suggest iteration:**
```
🔄 Iteration cycle available:

1. Fix blockers listed above
2. Run `/navigator:build {spec_file}` to re-implement
3. Run `/navigator:review {spec_file}` to re-review

Or use the JSON output programmatically:
  specs/reviews/{spec-name}-review.json
```

### 10. Atlas Refinement - Incremental Pattern Learning

**See:** `references/review/discovery-protocol.md` for complete atlas refinement workflow.

**Summary:** During review, track discoveries that should improve the atlas:
- New patterns not yet documented
- New anti-patterns discovered during review
- Missing conventions the code follows but atlas doesn't capture
- Unclassified files that don't match any pattern

**Workflow:**
1. Detect undocumented patterns during review
2. Write discoveries to `.claude/skills/atlas/staging/discoveries.yaml`
3. Prompt user to capture discoveries to atlas
4. Include discoveries in JSON output

---

## Scoring Criteria

**See:** `references/review/scoring-criteria.md` for complete grading rubrics.

| Category | A | B | C | F |
|----------|---|---|---|---|
| Spec Compliance | 100% criteria met | 80%+ met | 60%+ met | <60% met |
| Pattern Adherence | All conventions | Most followed | Some followed | Largely ignored |
| Code Quality | Clean, readable | Minor issues | Needs improvement | Significant concerns |
| Validation | All pass | Warnings only | Non-critical failures | Critical failures |

---

## Error Handling

**See:** `references/review/error-recovery.md` for complete error handling and recovery procedures.

| Error | Action | Recovery |
|-------|--------|----------|
| No atlas | Block with message | Run /cartographer:chart |
| No spec | Error with path | User provides correct path |
| No changes | Note implementation may be missing | Check if on correct branch |
| Validation fails | Report failures | User fixes or accepts |
| Agent timeout | Retry once, then skip | Continue with partial |
| Parse error | Report parse issue | Check agent output manually |

**Key recovery behaviors:**
- Agent failures after 3 attempts → Continue with partial results
- Validation command failures → Report but don't block entire review
- Preserve partial state in `.claude/review-partial.json`

---

## JSON Output Specification

**See:** `references/review/json-schema.md` for complete JSON output specification.

**Output location:** `specs/reviews/{spec-name}-review.json`

**Key sections:**
- `summary` - Overall grade, blocker/debt/skippable counts, recommendation
- `scores` - Per-category grades (spec_compliance, pattern_adherence, code_quality, validation)
- `atlas_context` - Patterns involved, composition used
- `blockers[]`, `tech_debt[]`, `skippable[]` - Issue arrays with file:line references
- `validation_results` - Command execution results
- `discoveries` - Atlas learning opportunities
- `files_reviewed` - Per-file grades and violations

**Consumers:**
| Consumer | Purpose |
|----------|---------|
| CI/CD pipelines | Block merge on blockers |
| `/navigator:build --resume` | Continue after fixes |
| `/cartographer:capture` | Import discoveries |

## Responsibilities

**YOU (reviewer):**
- Load spec and atlas context
- Review implementation against spec criteria
- Check pattern adherence
- Run validations
- Generate comprehensive review report
- Provide clear recommendations

**You are an objective reviewer. Be thorough but constructive.**

---

## Output Parsing Protocol

**See:** `references/protocols/agent-output-parsing.md` for complete parsing specifications.

### Review Agents

| Agent | Delimiter | Purpose |
|-------|-----------|---------|
| pattern-enforcer | `---PATTERN-ENFORCEMENT---` | Validates code against documented patterns |
| architecture-auditor | `---ARCHITECTURE-AUDIT---` | Validates layer boundaries |
| anti-pattern-detector | `---ANTI-PATTERN-SCAN---` | Scans for documented anti-patterns |
| convention-checker | `---CONVENTION-CHECK---` | Validates file naming and locations |

### Aggregation

After parsing all agent outputs:
1. Collect all violations from all agents
2. Classify: `error` → blocker, `warning` → tech_debt, recommendations → skippable
3. Deduplicate same file:line from multiple agents
4. Sort by severity (desc), then file path

### Severity Mapping

| Agent Severity | Review Severity |
|----------------|-----------------|
| `error` | blocker |
| `warning` | tech_debt |
| (recommendations) | skippable |
