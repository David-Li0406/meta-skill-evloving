---
name: skill-audit
description: This skill should be used for periodic review of all Claude Code skills. Triggers include "audit my skills", "which skills need work", "skill inventory", or when starting a skill improvement session. Identifies staleness, gaps, redundancy, and prioritizes improvements.
---

# skill-audit

systematic inventory and health check of all Claude Code skills. surfaces stale skills, identifies gaps in coverage, finds redundancies, and prioritizes improvement work.

## philosophy

> "you can't improve what you don't measure"

| principle | application |
|-----------|-------------|
| evidence-based | check file dates and line counts, not memory |
| comprehensive | audit ALL skills, not just suspicious ones |
| actionable output | produce prioritized list with specific actions |
| periodic | run monthly or after major skill changes |

## when to use

| use | skip |
|-----|------|
| starting skill improvement session | mid-improvement on specific skill |
| monthly maintenance | just finished audit recently |
| "which skills need work" | know exactly which skill to improve |
| noticing skill quality variance | single skill question |
| after creating multiple new skills | just created one skill (use pair quick) |

## decision tree: audit trigger

```
Why am I auditing?
├── Periodic (monthly)?
│   ├── Run full audit
│   ├── Compare to last audit report
│   └── Focus on regression (previously healthy → now stale)
├── Pre-improvement session?
│   ├── Run full audit
│   ├── Generate prioritized improvement list
│   └── Output: skill-improve targets
├── Post-skill-creation batch?
│   ├── Run focused audit on new skills
│   ├── Check for redundancy with existing
│   └── Verify integration with skill-chain
├── Suspected quality issue?
│   ├── Run depth check on suspicious skill
│   ├── Compare to healthy reference skill
│   └── Determine: improve or delete?
└── User asked "which skills"?
    ├── Run full audit
    ├── Present summary table
    └── Recommend top 3 improvement targets
```

## decision tree: skill categorization

```
How healthy is this skill?
├── Depth score 9-10?
│   ├── Has decision trees: yes
│   ├── Has concrete values: yes
│   ├── References substantive: yes
│   ├── Updated < 30 days: likely
│   └── Status: HEALTHY → periodic review only
├── Depth score 7-8?
│   ├── Missing 1-2 key elements
│   ├── May lack decision trees OR concrete values
│   └── Status: ADEQUATE → improve when time permits
├── Depth score 5-6?
│   ├── Missing multiple key elements
│   ├── Procedural but not conditional
│   └── Status: SHALLOW → prioritize for skill-improve
├── Depth score 3-4?
│   ├── Stub or placeholder content
│   ├── No actionable guidance
│   └── Status: NEEDS REWRITE → immediate attention
├── Depth score 1-2?
│   ├── Essentially empty or wrong
│   └── Status: CONSIDER DELETION → evaluate necessity
└── Updated > 90 days AND low depth?
    └── Status: STALE → check if still relevant
```

## decision tree: action routing

```
What action for this skill?
├── HEALTHY (9-10)?
│   ├── Log in audit report
│   ├── Schedule next review: 60 days
│   └── No immediate action
├── ADEQUATE (7-8)?
│   ├── Add to backlog
│   ├── Note specific gap (usually: needs decision tree)
│   └── Improve during slack time
├── SHALLOW (5-6)?
│   ├── Add to improvement queue
│   ├── Estimate effort: medium (30-60 min)
│   └── Use skill-improve workflow
├── NEEDS REWRITE (3-4)?
│   ├── Add to immediate queue
│   ├── Estimate effort: high (1-2 hours)
│   └── May need source research first
├── CONSIDER DELETION (1-2)?
│   ├── Check usage: is this skill ever triggered?
│   ├── If unused + low quality → delete
│   └── If used but broken → prioritize rewrite
└── STALE (any score, old date)?
    ├── Check if domain changed
    ├── If outdated info → update or delete
    └── If still valid → update date, minor refresh
```

## concrete values

| value | meaning | source |
|-------|---------|--------|
| decision tree weight | ×2 | heuristic: decision trees transform skills from "procedural" to "conditional" - the key differentiator for autonomous agents |
| concrete values weight | ×2 | heuristic: sourced numbers enable reproducibility and prevent cargo cult thresholds |
| other criteria weight | ×1 | heuristic: important but secondary to decision logic and measurable values |
| substantive reference | >50 lines | convention: aligns with claude-code-guide minimum for reference files |
| healthy threshold | 9-10 (87%+) | heuristic: A-grade equivalent; skills at this level rarely cause agent confusion |
| adequate threshold | 7-8 (68-81%) | heuristic: B-grade equivalent; functional but has gaps agents may stumble on |
| shallow threshold | 5-6 (50-62%) | heuristic: C-grade equivalent; procedural only, lacks conditional guidance |
| staleness threshold | >90 days + low depth | empirical: tool APIs and patterns shift materially within a quarter |
| review interval | 60 days (healthy) | heuristic: 2x staleness detection buffer; catch decay before it matters |
| audit frequency | monthly | convention: matches sprint/cycle boundaries in most workflows |

**sourcing legend**: `heuristic` = practical experience from skill authoring; `empirical` = measured from actual tool/API usage; `convention` = widely adopted standard

## concrete scoring criteria

| criterion | 0 points | 1 point | 2 points | weight |
|-----------|----------|---------|----------|--------|
| decision trees | none | 1 tree | 2+ trees with branches | ×2 |
| concrete values | none | some values | values with sources | ×2 |
| anti-patterns | none | listed | listed with fixes | ×1 |
| references | none/stub | exist but thin | substantive (>50 lines) | ×1 |
| tool integration | none | mentioned | working examples | ×1 |
| when to use | none | listed | table with use/skip | ×1 |

**max raw score:** 16 points
**depth score:** `raw / 16 × 10` (rounded)

| raw | depth | interpretation |
|-----|-------|----------------|
| 14-16 | 9-10 | healthy |
| 11-13 | 7-8 | adequate |
| 8-10 | 5-6 | shallow |
| 5-7 | 3-4 | needs rewrite |
| 0-4 | 1-2 | consider deletion |

## workflow

### 1. enumerate skills

```bash
# list all skills with stats
echo "| skill | lines | refs | modified |"
echo "|-------|-------|------|----------|"
for skill_dir in ~/.claude/skills/*/; do
  skill_name=$(basename "$skill_dir")
  if [ -f "$skill_dir/SKILL.md" ]; then
    lines=$(wc -l < "$skill_dir/SKILL.md" | tr -d ' ')
    ref_count=$(find "$skill_dir/references" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    mod_date=$(stat -f "%Sm" -t "%Y-%m-%d" "$skill_dir/SKILL.md" 2>/dev/null)
    echo "| $skill_name | $lines | $ref_count | $mod_date |"
  fi
done
```

### 2. score each skill

for each skill, compute depth score using criteria table:

```bash
# read skill and score
skill_content=$(cat ~/.claude/skills/$SKILL_NAME/SKILL.md)

# check decision trees (look for ├── pattern)
trees=$(echo "$skill_content" | grep -c "├──" || echo 0)

# check concrete values (look for tables with numbers)
has_values=$(echo "$skill_content" | grep -E "\|.*[0-9]+.*\|" | wc -l)

# check anti-patterns section
has_antipatterns=$(echo "$skill_content" | grep -c "## anti-patterns" || echo 0)

# check references exist
ref_count=$(find ~/.claude/skills/$SKILL_NAME/references -name "*.md" 2>/dev/null | wc -l)

# compute raw score (simplified)
# full scoring requires reading content depth
```

### 3. quick validation via pair quick

for borderline skills (score 5-7), get AI assessment:

```bash
cat <<'EOF' | copilot -p --model gemini-3-pro
Skill depth assessment.

Skill: $SKILL_NAME
Content preview:
```
[first 100 lines of SKILL.md]
```

Score 1-10 using these weights:
- Decision trees (×2): actionable if/then logic?
- Concrete values (×2): specific numbers with sources?
- Anti-patterns (×1): what NOT to do with fixes?
- References (×1): substantive (>50 lines each)?
- Tool integration (×1): working code examples?
- When to use (×1): clear use/skip guidance?

Output JSON: {
  skill: string,
  raw_score: number,
  depth_score: number,
  missing: string[],
  status: "healthy" | "adequate" | "shallow" | "needs_rewrite" | "consider_deletion",
  priority: "immediate" | "soon" | "backlog" | "none"
}
EOF
```

### 4. check coverage gaps

map skills to workflow activities:

```
Daily activities:
├── Linear issues → issue-context ✓
├── Code review → pr-audit ✓
├── Testing → ? (gap if no TDD skill)
├── Slack comms → slack ✓
├── Design work → emil-kowalski ✓
├── Skill management → skill-create, skill-improve, skill-audit ✓
├── Agent delegation → agent-pair ✓
├── Autonomous work → loop ✓
└── [user activity] → [skill]? (check coverage)

Missing coverage = gap to fill with new skill
```

### 5. detect redundancy

```
Redundancy signals:
├── Same triggers in different skills?
│   └── Merge into one with sections
├── One skill constantly references another?
│   └── Consider absorbing smaller into larger
├── >50% content overlap?
│   └── Merge and deduplicate
├── Same domain, different scope?
│   └── May be valid (light vs deep) - keep separate
└── Created for same task?
    └── Delete less complete version
```

### 6. generate audit report

```markdown
# Skill Audit Report
**Date:** YYYY-MM-DD
**Total skills:** N
**Health distribution:** healthy: X, adequate: Y, shallow: Z, needs work: W

## Summary Table

| skill | depth | lines | refs | status | action |
|-------|-------|-------|------|--------|--------|
| loop | 9/10 | 450 | 6 | healthy | none |
| imessage | 5/10 | 80 | 0 | shallow | improve |

## Improvement Queue

### Immediate (depth < 5, blocking issues)
1. **skill-name** - issue - effort: high

### Soon (depth 5-7, quality issues)
1. **skill-name** - issue - effort: medium

### Backlog (depth 7-8, minor gaps)
1. **skill-name** - issue - effort: low

## Coverage Gaps
- [ ] No skill for: [activity]
- [ ] Weak coverage for: [domain]

## Redundancies Found
- skill-a overlaps skill-b → recommend: merge

## Next Audit
Scheduled: YYYY-MM-DD (30 days)
```

### 7. route to skill-improve

for each skill in improvement queue:

```bash
# hand off to skill-improve
# include audit findings in context

echo "Improve $SKILL_NAME"
echo "Current depth: $DEPTH_SCORE/10"
echo "Missing: $MISSING_ELEMENTS"
echo "Priority: $PRIORITY"
```

## quality checklist

before completing audit:

- [ ] all skills enumerated (none skipped)
- [ ] each skill scored using criteria table
- [ ] borderline cases validated via pair quick
- [ ] coverage gaps identified
- [ ] redundancies checked
- [ ] prioritized improvement list generated
- [ ] next audit date scheduled

## tool integration

| tool | command | purpose |
|------|---------|---------|
| copilot | `copilot -p --model gemini-3-pro` | quick skill assessment |
| fd | `fd -e md . ~/.claude/skills/` | enumerate skill files |
| wc | `wc -l < SKILL.md` | measure skill depth |
| trails | `trails trail record` | audit history persistence |

### trails integration

persist audit results for trend tracking:

```bash
# record audit completion
trails trail record --agent claude --action completed \
  --task "skill-audit: $SKILL_COUNT skills, $HEALTHY healthy, $SHALLOW shallow" \
  --confidence $CONFIDENCE --json -q
```

**trails enables**:
- tracking skill health over time
- measuring improvement velocity
- correlating audits with skill creation

### with skill-improve (post-audit)

```
skill-audit → skill-improve × N
     │              │
     │              └── improve each flagged skill
     └── provides prioritized list
```

### with skill-chain (routing)

skill-chain may invoke skill-audit when:
- user asks "which skills need work"
- starting improvement session
- unclear which skill to invoke

### with pair (validation)

for borderline scores, use pair quick for AI assessment before categorizing.

## automation

### monthly audit cron

```bash
# add to monthly task
skill-audit → generate report → slack dm luke "Monthly skill audit ready"
```

### post-improvement verification

after using skill-improve on a skill:
```bash
# re-score the improved skill
# verify depth increased to target
skill-audit --focus=$SKILL_NAME --verify
```

## references

- [references/scoring-rubric.md](references/scoring-rubric.md) - detailed scoring criteria with examples
- [references/coverage-map.md](references/coverage-map.md) - workflow-to-skill mapping template
- [references/audit-checklist.md](references/audit-checklist.md) - pre-audit verification checklist

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| audit from memory | miss stale skills, bias toward recent | check file dates and content |
| skip healthy skills | miss regression | include all skills in audit |
| audit without action | waste of time | produce prioritized list with next steps |
| one-time audit | skills decay | schedule periodic audits (monthly) |
| vague scoring | "feels shallow" not actionable | use concrete criteria table |
| ignore redundancy | skill sprawl | check for overlap, merge when >50% |
| skip coverage check | gaps in workflow | map activities to skills |
