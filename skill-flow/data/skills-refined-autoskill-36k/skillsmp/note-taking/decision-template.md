# Decision Template

Use this template when recording major decisions in the AUDIT TRAIL section.

## Template

```markdown
### Decision: [Decision Title] (YYYY-MM-DD, Session X)

**Claude's Analysis:**
- [What research/analysis Claude performed]
- [What data/insights Claude provided]
- [What options Claude presented]

**Claude's Recommendation:**
[What Claude suggested and why]

**User Decision:**
[What the user actually decided]

**Rationale:**
[Why the user made this choice]

**Outcome:**
✅/❌ [What happened as a result]
```

## Example

```markdown
### Decision: Use "150+ hours" not "600 hours" (2025-11-03, Session 3)

**Claude's Analysis:**
- Git analysis: 79 commits across 36 days
- Found error: content is automated, not manually curated
- Revised estimate: 150-200 hours based on commit patterns
- GenAI assistance significantly reduced time

**Claude's Recommendation:**
Use "over 150 hours across several months" to be honest about uncertainty while showing AI's impact.

**User Decision:**
Approved. Changed "600 hours" to "over 150 hours" throughout Part 1.

**Rationale:**
More honest (admits no time tracking), shows AI's actual impact, still demonstrates significant investment. Better story: GenAI cut 70%+ but 150 hours is still substantial.

**Outcome:**
✅ More credible than 600-hour claim. Readers responded positively. Better supports the argument that GenAI reduces but doesn't eliminate cost.
```

## What to Include

**Claude's Analysis:**
- Research performed (git analysis, web search, data analysis)
- Data discovered (numbers, patterns, insights)
- Options identified (multiple approaches considered)
- Problems found (errors in assumptions, gaps in data)

**Claude's Recommendation:**
- What Claude suggested
- Why this approach (reasoning)
- Alternatives considered (what else was possible)

**User Decision:**
- What user actually chose (might differ from recommendation!)
- Actions taken based on decision

**Rationale:**
- Why user made this choice
- What factors influenced decision
- What tradeoffs were accepted

**Outcome:**
- ✅ Worked: What succeeded and why
- ❌ Didn't work: What failed and lesson learned
- Impact: How this affected the project
