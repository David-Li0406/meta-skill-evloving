# Specialist Briefs

Full prompts for each specialist in the 4-agent fanout.

---

## Code State Specialist

```markdown
# Code State Specialist Brief

**Team**: $TEAM
**Project Path**: $PROJECT_PATH
**V1 Template**: $PROJECT_TYPE-v1

## Your Focus

Assess the codebase health: test coverage, build status, type safety, and recent development trajectory.

## Tasks

1. **Test Coverage**
   ```bash
   verify --coverage --json -q | jq '.summary'
   ```
   Extract: line coverage %, branch coverage %, uncovered files

2. **Build Health**
   ```bash
   pnpm build 2>&1 | tail -30
   ```
   Extract: success/failure, warning count, error messages

3. **Type Safety**
   ```bash
   pnpm typecheck 2>&1 | tail -30
   ```
   Extract: error count, files with errors

4. **Lint Status**
   ```bash
   pnpm lint 2>&1 | tail -30
   # or: biome check . 2>&1 | tail -30
   ```
   Extract: error count, warning count

5. **Recent Activity**
   ```bash
   git log --oneline -20
   git log --since="7 days ago" --oneline | wc -l
   git log --since="30 days ago" --oneline | wc -l
   ```
   Extract: commit count, recent focus areas

6. **Structural Changes**
   ```bash
   outline --diff=HEAD~10 --format=yaml
   ```
   Extract: added/modified/removed symbols

## V1 Targets (from template)

- Test coverage: $COVERAGE_TARGET%
- Build: passing
- Types: clean
- Lint: clean

## Output Contract

```json
{
  "domain": "code-state",
  "status": "success | partial | failed",
  "findings": {
    "coverage": {
      "line": 82,
      "branch": 75,
      "target": 80,
      "gap": 0
    },
    "build": {
      "status": "passing | failing",
      "warnings": 3,
      "errors": 0
    },
    "types": {
      "errors": 0,
      "files_with_errors": []
    },
    "lint": {
      "errors": 0,
      "warnings": 5
    },
    "activity": {
      "commits_7d": 12,
      "commits_30d": 45,
      "focus_areas": ["auth", "api"]
    }
  },
  "gaps": [
    { "type": "below_target", "item": "branch coverage 75% < 80%", "fix": "add tests for uncovered branches" }
  ],
  "v1_blockers": [],
  "confidence": 8
}
```

## Constraints

- READ-ONLY: do not modify any files
- Use only the tools listed above
- Report actual numbers, not estimates
- Flag any command failures
```

---

## Architecture Specialist

```markdown
# Architecture Specialist Brief

**Team**: $TEAM
**Project Path**: $PROJECT_PATH
**V1 Template**: $PROJECT_TYPE-v1

## Your Focus

Assess the architectural health: package dependencies, cycles, dead code, and structural patterns.

## Tasks

1. **Package Dependencies**
   ```bash
   layer . --format=json -q
   ```
   Extract: package count, dependency depth, internal vs external deps

2. **Cycle Detection**
   ```bash
   layer . --check-cycles
   ```
   Extract: cycle count, affected packages

3. **Dead Code**
   ```bash
   outline --unused -r 2>&1 | head -50
   ```
   Extract: unused export count, affected files

4. **Import Graph**
   ```bash
   layer . --mode=files --files-only -q | wc -l
   ```
   Extract: file count, module organization

5. **Package Documentation**
   ```bash
   for pkg in packages/*/; do
     [ -f "$pkg/README.md" ] && echo "✓ $pkg" || echo "✗ $pkg"
   done
   ```
   Extract: documented packages, undocumented packages

## V1 Targets (from template)

- Cycles: none
- Dead code: <5%
- Packages: documented

## Output Contract

```json
{
  "domain": "architecture",
  "status": "success | partial | failed",
  "findings": {
    "packages": {
      "count": 8,
      "documented": 6,
      "undocumented": ["@repo/testing", "@repo/seo"]
    },
    "dependencies": {
      "internal": 12,
      "external": 45,
      "depth": 3
    },
    "cycles": {
      "count": 0,
      "affected": []
    },
    "dead_code": {
      "unused_exports": 15,
      "percentage": 3,
      "files": ["src/utils/legacy.ts"]
    }
  },
  "gaps": [
    { "type": "undocumented", "item": "@repo/testing lacks README", "fix": "add README.md" }
  ],
  "v1_blockers": [],
  "confidence": 9
}
```

## Constraints

- READ-ONLY: do not modify any files
- Use only the tools listed above
- Report actual numbers, not estimates
- Flag any command failures
```

---

## Linear State Specialist

```markdown
# Linear State Specialist Brief

**Team**: $TEAM
**Workspace**: luke-labs
**V1 Template**: $PROJECT_TYPE-v1

## Your Focus

Assess Linear issue quality: context markers, staleness, vague issues, and state distribution.

## Tasks

1. **Issue Distribution**
   ```bash
   linear issue list --team $TEAM --json -q | jq 'group_by(.state.name) | map({state: .[0].state.name, count: length})'
   ```
   Extract: count per state (Backlog, Todo, In Progress, Done)

2. **Context Markers Check**
   ```bash
   # For each issue, check for issue-context markers
   for ISSUE in $(linear issue list --team $TEAM --limit 50 --json -q | jq -r '.[].identifier'); do
     MARKERS=$(linear comment list $ISSUE --json -q 2>/dev/null | jq -r '.[].body' | grep -c "issue-context:" || echo "0")
     echo "$ISSUE: $MARKERS"
   done
   ```
   Extract: issues with context, issues without context

3. **Context Staleness**
   ```bash
   # Check comment dates for issues with markers
   # Flag any markers older than 14 days
   ```
   Extract: fresh context count, stale context count

4. **Vague Issues**
   ```bash
   linear issue list --team $TEAM --json -q | jq '[.[] | select(.description == null or .description == "")] | length'
   ```
   Extract: issues without description

5. **Priority Distribution**
   ```bash
   linear issue list --team $TEAM --json -q | jq 'group_by(.priority) | map({priority: .[0].priority, count: length})'
   ```
   Extract: count per priority level

## V1 Targets (from template)

- All issues have context: true
- Context freshness: <14 days
- No vague issues: true

## Output Contract

```json
{
  "domain": "linear-state",
  "status": "success | partial | failed",
  "findings": {
    "distribution": {
      "backlog": 15,
      "todo": 8,
      "in_progress": 3,
      "done": 20
    },
    "context": {
      "with_markers": 32,
      "without_markers": 14,
      "stale": 5,
      "fresh": 27
    },
    "quality": {
      "vague_issues": ["ARB-45", "ARB-67"],
      "no_description": 2,
      "no_acceptance_criteria": 5
    },
    "priority": {
      "urgent": 2,
      "high": 5,
      "medium": 15,
      "low": 24
    }
  },
  "gaps": [
    { "type": "missing_context", "item": "ARB-123 has no issue-context", "fix": "run issue-context skill" },
    { "type": "stale", "item": "ARB-456 context is 21 days old", "fix": "refresh with issue-context" },
    { "type": "vague", "item": "ARB-789 has no description", "fix": "add description or delete" }
  ],
  "v1_blockers": ["14 issues missing context"],
  "enrichment_queue": ["ARB-123", "ARB-456", "ARB-789"],
  "confidence": 8
}
```

## Constraints

- READ-ONLY: do not modify any issues
- Use only the tools listed above
- Sample up to 50 issues for context check (pagination)
- Flag any command failures
```

---

## V1 Gaps Specialist

```markdown
# V1 Gaps Specialist Brief

**Team**: $TEAM
**Project Path**: $PROJECT_PATH
**V1 Template**: $PROJECT_TYPE-v1

## Your Focus

Synthesize findings from other specialists and identify the delta between current state and V1 readiness.

## Inputs

You will receive findings from:
- Code State Specialist
- Architecture Specialist
- Linear State Specialist

## Tasks

1. **Load V1 Template**
   - Parse $PROJECT_TYPE-v1 requirements
   - Extract target values for each criterion

2. **Calculate Gaps**
   For each V1 requirement:
   - Compare current value to target
   - Calculate delta
   - Classify as: blocker | gap | ok

3. **Prioritize Blockers**
   - Blockers = must fix before V1
   - Gaps = should fix but not blocking
   - Ok = meets or exceeds target

4. **Generate Recommendations**
   - Order by impact and effort
   - Provide specific fix actions

## V1 Template: $PROJECT_TYPE-v1

```yaml
code:
  test_coverage: $COVERAGE_TARGET%
  build: passing
  types: clean
  lint: clean

architecture:
  cycles: none
  dead_code: <5%
  packages: documented

linear:
  all_issues_have_context: true
  context_freshness: <14 days
  no_vague_issues: true

docs:
  agents_md: present
  readme: present

ci:
  tests: automated
  deploy: automated
```

## Output Contract

```json
{
  "domain": "v1-gaps",
  "status": "success | partial | failed",
  "findings": {
    "template": "$PROJECT_TYPE-v1",
    "score": 78,
    "grade": "almost"
  },
  "gap_analysis": [
    {
      "category": "code",
      "criterion": "test_coverage",
      "current": 75,
      "target": 80,
      "delta": -5,
      "status": "gap"
    },
    {
      "category": "linear",
      "criterion": "all_issues_have_context",
      "current": false,
      "target": true,
      "delta": null,
      "status": "blocker"
    }
  ],
  "gaps": [
    { "type": "below_target", "item": "test coverage 75% < 80%", "fix": "add 5% more test coverage", "priority": "P2" }
  ],
  "v1_blockers": [
    { "item": "14 issues missing context", "fix": "run issue-context batch enrichment", "priority": "P1" },
    { "item": "2 dependency cycles detected", "fix": "refactor to break cycles", "priority": "P1" }
  ],
  "recommendations": [
    { "action": "Run batch issue-context enrichment", "impact": "high", "effort": "medium", "priority": "P1" },
    { "action": "Add tests for auth module", "impact": "medium", "effort": "low", "priority": "P2" }
  ],
  "v1_ready": false,
  "confidence": 8
}
```

## Constraints

- READ-ONLY: synthesis only, no modifications
- Base analysis on specialist findings, not direct tool calls
- Be specific in gap descriptions
- Prioritize by impact on autonomous execution
```

---

## spawning specialists

```bash
# Generate briefs
for SPECIALIST in code-state architecture linear-state v1-gaps; do
  cat > "$AUDIT_DIR/briefs/${SPECIALIST}.md" << EOF
$(cat ~/.agents/skills/linear-audit/references/specialist-briefs.md | sed -n "/${SPECIALIST^} Specialist/,/^---$/p" | head -n -1)
EOF
done

# Spawn with agents session start --await
for SPECIALIST in code-state architecture linear-state v1-gaps; do
  (
    RESULT=$(cat "$AUDIT_DIR/briefs/${SPECIALIST}.md" | \
      agents session start -a copilot -p $TEAM \
        -g "${SPECIALIST}: $TEAM audit" \
        --parent "$AUDIT_ID" \
        --timeout 180 \
        --await \
        --json -q)
    echo "$RESULT" >> "$AUDIT_DIR/results.jsonl"
  ) &
done
wait
```
