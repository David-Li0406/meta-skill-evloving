# Audit Criteria

Scoring rubrics and quality gates for linear-audit.

---

## scoring weights

| criterion | weight | measurement |
|-----------|--------|-------------|
| test coverage | 25% | `verify --coverage` percentage |
| build health | 20% | `pnpm build` exit code + warnings |
| type safety | 15% | `pnpm typecheck` error count |
| architecture | 15% | cycles + dead code percentage |
| linear context | 15% | % issues with fresh `issue-context:` markers |
| documentation | 10% | AGENTS.md + README presence and accuracy |

---

## scoring formula

```
score = (
  coverage_score * 0.25 +
  build_score * 0.20 +
  type_score * 0.15 +
  arch_score * 0.15 +
  linear_score * 0.15 +
  docs_score * 0.10
)
```

### per-criterion scoring

**Coverage Score (0-100)**
```
coverage_score = min(100, (actual_coverage / target_coverage) * 100)
```

**Build Score (0-100)**
```
if build_fails: 0
elif warnings > 10: 70
elif warnings > 0: 90
else: 100
```

**Type Score (0-100)**
```
if type_errors > 0: max(0, 100 - (type_errors * 10))
else: 100
```

**Architecture Score (0-100)**
```
cycle_penalty = cycles * 20
dead_code_penalty = max(0, (dead_code_pct - 5) * 5)
arch_score = max(0, 100 - cycle_penalty - dead_code_penalty)
```

**Linear Score (0-100)**
```
with_context = issues_with_markers - stale_issues
linear_score = (with_context / total_issues) * 100
```

**Docs Score (0-100)**
```
if agents_md and readme: 100
elif agents_md or readme: 50
else: 0
```

---

## grade thresholds

| score | grade | status | meaning |
|-------|-------|--------|---------|
| 90-100 | A | ready | safe for autonomous execution |
| 80-89 | B | almost | minor gaps, proceed with caution |
| 70-79 | C | gaps | noticeable gaps, address before V1 |
| 50-69 | D | not ready | significant gaps, needs work |
| <50 | F | blocked | major issues, focus required |

---

## blocker classification

### P1 Blockers (must fix)

- Build fails
- Type errors > 5
- Dependency cycles > 0
- >30% issues missing context
- AGENTS.md missing or severely outdated

### P2 Gaps (should fix)

- Coverage < target by >10%
- Type errors 1-5
- Dead code > 10%
- 10-30% issues missing context
- Context staleness > 14 days

### P3 Improvements (nice to have)

- Coverage < target by <10%
- Build warnings > 5
- Dead code 5-10%
- <10% issues missing context
- Minor doc gaps

---

## quality gates

### gate: V1 ready

```yaml
required:
  - build: passing
  - types: clean (0 errors)
  - cycles: none (0 cycles)
  - context_coverage: >= 70%
  - blockers: 0

recommended:
  - coverage: >= target
  - dead_code: < 5%
  - context_freshness: all < 14 days
  - docs: complete
```

### gate: safe to proceed

```yaml
required:
  - build: passing
  - types: < 5 errors
  - cycles: <= 1
  - context_coverage: >= 50%

warnings_allowed:
  - coverage: any
  - dead_code: any
  - docs: any
```

---

## issue quality criteria

### well-formed issue

- [ ] Title is specific and actionable
- [ ] Description explains context and goal
- [ ] Acceptance criteria defined
- [ ] Has `<!-- issue-context:analysis -->` marker
- [ ] Context is < 14 days old

### vague issue indicators

- Title is generic ("fix bug", "update feature")
- No description
- No acceptance criteria
- No file references in comments
- No agent prompt in comments

### issue disposition rules

| condition | action |
|-----------|--------|
| well-formed + fresh context | ready for V1 |
| well-formed + stale context | re-enrich |
| no context markers | enrich |
| vague + no context | flag for HIL or delete |
| duplicate | flag for merge |
| outdated (old arch) | flag for delete |

---

## context freshness rules

| age | status | action |
|-----|--------|--------|
| < 7 days | fresh | none needed |
| 7-14 days | aging | consider refresh |
| 14-30 days | stale | refresh recommended |
| > 30 days | expired | must refresh |

---

## confidence scoring

| confidence | meaning |
|------------|---------|
| 9-10 | high certainty, proceed |
| 7-8 | good certainty, minor caveats |
| 5-6 | moderate certainty, verify |
| 3-4 | low certainty, investigate |
| 1-2 | unreliable, re-audit |

### confidence factors

**Increases confidence:**
- All commands succeeded
- Data is complete
- Numbers are consistent
- Clear patterns

**Decreases confidence:**
- Command failures
- Missing data
- Inconsistent numbers
- Ambiguous patterns

---

## aggregation rules

### combining specialist findings

```python
def aggregate_findings(specialists):
    findings = {}
    confidence_sum = 0

    for s in specialists:
        if s.status == "success":
            findings[s.domain] = s.findings
            confidence_sum += s.confidence
        elif s.status == "partial":
            findings[s.domain] = s.findings  # partial data
            confidence_sum += s.confidence * 0.7  # weight down
        else:
            # failed - exclude from aggregation
            confidence_sum += 0

    overall_confidence = confidence_sum / len([s for s in specialists if s.status != "failed"])
    return findings, overall_confidence
```

### combining gaps

```python
def combine_gaps(specialists):
    all_gaps = []
    blockers = []

    for s in specialists:
        for gap in s.gaps:
            all_gaps.append(gap)
        for blocker in s.v1_blockers:
            blockers.append(blocker)

    # Deduplicate
    unique_gaps = dedupe_by_item(all_gaps)
    unique_blockers = dedupe_by_item(blockers)

    # Prioritize
    sorted_gaps = sort_by_priority(unique_gaps)
    sorted_blockers = sort_by_priority(unique_blockers)

    return sorted_gaps, sorted_blockers
```

---

## reporting thresholds

| metric | show_in_summary | show_details |
|--------|-----------------|--------------|
| blockers | always | always |
| P2 gaps | if count > 0 | first 5 |
| P3 improvements | count only | on request |
| passing criteria | count only | on request |

---

## audit frequency

| trigger | recommended_frequency |
|---------|----------------------|
| pre-V1 push | once per project |
| weekly maintenance | once per team |
| post-major-refactor | after significant changes |
| stale context detected | immediate re-audit |
