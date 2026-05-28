# Meta-Learning

Reflection questions and patterns for continuous improvement.

## Session Reflection Questions

### After Major Features

Ask yourself:
1. What would be done differently next time?
2. What took longer than expected? Why?
3. What patterns emerged during implementation?
4. What should be automated?
5. What knowledge was missing at the start?

### After Debugging

Ask yourself:
1. How was the root cause discovered?
2. What debugging technique worked best?
3. What would have caught this earlier?
4. Is this a recurring pattern?
5. Can tooling prevent this?

### After Refactoring

Ask yourself:
1. What triggered the need to refactor?
2. What was the before/after improvement?
3. Was the scope appropriate?
4. What tests gave confidence?
5. Should this pattern be documented?

## Pattern Recognition

### Time Sinks

Track where time goes unexpectedly:

| Time Sink Category | Common Causes | Prevention |
|--------------------|---------------|------------|
| Configuration | Missing docs, edge cases | Document in LEARNINGS.md |
| Integration | API quirks, auth issues | Add to ERROR_HISTORY.md |
| Type errors | Library mismatches | Note type patterns |
| Test failures | Brittle tests, missing mocks | Improve test patterns |
| Build issues | Version conflicts | Lock versions, document |

### Success Patterns

Track what accelerates work:

| Accelerator | Example | Capture How |
|-------------|---------|-------------|
| Good abstractions | Reusable hook | Add to examples/ |
| Clear patterns | State machine structure | Add to references/ |
| Effective tools | Debugging technique | Add to CLAUDE.md |
| Prior knowledge | Past error fix | Keep ERROR_HISTORY.md current |

## Learning Extraction Framework

### The 5 Whys for Root Cause

When something went wrong:
1. Why did it fail? → [Immediate cause]
2. Why did that happen? → [Contributing factor]
3. Why was that possible? → [Systemic issue]
4. Why wasn't it caught? → [Process gap]
5. Why doesn't tooling help? → [Automation opportunity]

### The 3 Futures

When evaluating a learning:
1. **Recurrence:** Will this situation happen again?
2. **Impact:** If it does, how much time lost?
3. **Prevention:** Can future occurrence be prevented?

Log if: High recurrence OR High impact

### Insight Categories

| Category | Characteristics | Where to Log |
|----------|-----------------|--------------|
| Codebase-specific | Only applies here | LEARNINGS.md |
| Pattern | Applies to similar projects | Consider skill update |
| Universal | Applies to all projects | Definitely skill update |
| Tool-specific | About a particular tool | CLAUDE.md or LEARNINGS.md |

## Continuous Improvement Habits

### Daily

- Note any "aha" moments
- Check if current task matches past learnings
- Quick review of recent ERROR_HISTORY.md if debugging

### Weekly

- Review week's LEARNINGS.md additions
- Look for patterns across entries
- Consider if patterns warrant skill updates

### Monthly

- Review and prune LEARNINGS.md
- Update ERROR_HISTORY.md (remove solved issues)
- Refresh CLAUDE.md if needed
- Consider skill maintenance

### Per-Project

- At start: Review relevant learnings
- During: Log project-specific insights
- At end: Extract generalizable patterns

## Metrics to Track (Mental or Logged)

### Time Investment

| Activity | Target | Actual | Delta |
|----------|--------|--------|-------|
| Feature development | X hours | | |
| Debugging | < 20% | | |
| Configuration | < 10% | | |
| Testing | 20-30% | | |

### Quality Indicators

| Indicator | Good | Watch For |
|-----------|------|-----------|
| Same error twice | Never | Recurring patterns |
| Missing knowledge | Rare | Frequent surprises |
| Refactor frequency | Planned only | Unplanned refactors |
| Test failures | Rare | Frequent flakiness |

## Knowledge Gaps

### Identifying Gaps

Signs of missing knowledge:
- Repeated trial-and-error
- Searching documentation frequently
- Asking same question multiple times
- Surprise behaviors

### Filling Gaps

| Gap Type | Strategy |
|----------|----------|
| API/library | Read docs, create example |
| Pattern | Study examples, implement variant |
| Concept | Read article, take notes |
| Tool | Hands-on practice |

### Recording Filled Gaps

When gap is filled:
1. Document in appropriate location
2. Create example if helpful
3. Add to skill if generalizable
4. Share with team if applicable

## Retrospective Templates

### Quick Retro (5 min)

```markdown
## Session Date: YYYY-MM-DD

### What went well?
- [1 thing]

### What was challenging?
- [1 thing]

### What to log?
- LEARNINGS: [Y/N - topic]
- ERROR_HISTORY: [Y/N - error]
- SKILL: [Y/N - which skill]
```

### Standard Retro (15 min)

```markdown
## Session Date: YYYY-MM-DD

### Accomplishments
- [Task 1]
- [Task 2]

### Challenges
- [Challenge 1] → [Resolution/Learning]

### Time Distribution
- Feature work: X%
- Debugging: X%
- Config/setup: X%
- Other: X%

### Knowledge Gaps Identified
- [Gap 1]

### Logging Actions
- [ ] LEARNINGS.md: [entry or N/A]
- [ ] ERROR_HISTORY.md: [entry or N/A]
- [ ] CLAUDE.md: [update or N/A]
- [ ] Skill: [which skill, what update or N/A]
```

### Deep Retro (30+ min, after major work)

```markdown
## Project/Feature Retrospective

### Summary
[What was built]

### Duration
[Planned vs actual]

### What Worked Well
1. [Pattern/approach that succeeded]
2. [Pattern/approach that succeeded]

### What Could Improve
1. [Area for improvement]
2. [Area for improvement]

### Unexpected Challenges
1. [Challenge] → [How resolved] → [Prevention]

### Patterns Extracted
1. [Pattern] → [Where to document]

### Tool/Process Improvements
1. [Improvement idea]

### Follow-up Actions
- [ ] [Action item]
- [ ] [Action item]
```
