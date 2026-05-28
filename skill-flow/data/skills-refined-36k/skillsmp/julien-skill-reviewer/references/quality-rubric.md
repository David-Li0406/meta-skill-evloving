# Quality Assessment Rubric

Evaluate each dimension on 1-5 scale.

## Scoring Table

| Dimension | 1 (Poor) | 3 (Good) | 5 (Excellent) |
|-----------|----------|----------|---------------|
| **Clarity** | Vague, ambiguous | Clear workflow, some gaps | Crystal clear, no ambiguity |
| **Completeness** | Missing critical steps | Covers main use cases | Handles edge cases, errors |
| **Discoverability** | Hard to know when to use | Key scenarios mentioned | Name + desc trigger correctly |
| **Context Efficiency** | >500 lines, no refs | 300-500 lines, some refs | <300 lines, optimal refs |
| **Actionability** | Theoretical only | Step-by-step provided | Checklist-style, copy-paste |
| **Resource Organization** | All in SKILL.md | Good separation | Optimal progressive disclosure |
| **Examples** | None or abstract | 1-2 concrete | Multiple scenarios covered |
| **Skill Chaining** | Not documented | Mentions related skills | Full I/O/Dependencies |
| **Error Handling** | No guidance | Basic troubleshooting | Comprehensive scenarios |

## Check Criteria

### Clarity (1-5)

**Check for:**
- Clear objective stated upfront
- Unambiguous terminology
- Step-by-step with numbered steps
- Examples clarify instructions

**Red flags:**
- "Do something appropriate"
- "Handle this as needed"
- Multiple interpretations possible
- Unclear "this" or "it" references

### Completeness (1-5)

**Check for:**
- All workflow steps documented
- Error handling for common failures
- Edge cases addressed
- Prerequisites clearly stated

**Red flags:**
- "Assume X works"
- No error handling
- Critical steps skipped
- "And then it's done" (missing steps)

### Discoverability (1-5)

**Check for:**
- Description includes trigger keywords
- Use cases clearly stated
- Third-person description
- "Use when..." guidance

**Red flags:**
- Generic: "Helps with tasks"
- No usage scenarios
- Name doesn't reflect purpose
- Missing triggers

### Context Efficiency (1-5)

**Check for:**
- SKILL.md line count (target < 500)
- Appropriate references/ usage
- Progressive disclosure respected
- No duplicated content

**Red flags:**
- SKILL.md > 500 lines
- Long examples in main file
- API docs in SKILL.md
- Same info in SKILL.md and references/

### Actionability (1-5)

**Check for:**
- Imperative verbs (verb-first)
- Concrete commands/code
- Checklist format where appropriate
- Clear "do this, then that" flow

**Red flags:**
- "You might want to consider..."
- Theoretical without steps
- No concrete examples
- "Figure out how to..."

### Resource Organization (1-5)

**Check for:**
- `scripts/` for executable code
- `references/` for documentation
- `assets/` for templates/media
- Proper separation of concerns
- References one level deep
- TOC for files > 100 lines

**Red flags:**
- Python code in SKILL.md
- Long API docs in SKILL.md
- Templates in SKILL.md
- Nested references (A → B → C)
- Windows backslashes in paths

### Examples (1-5)

**Check for:**
- Concrete, realistic examples
- Different use cases covered
- Copy-paste ready code
- Expected output shown

**Red flags:**
- "For example, something like X"
- Placeholder examples (foo, bar)
- Abstract without context
- No examples at all

### Skill Chaining (1-5)

**Check for:**
- Skills Required Before
- Input Expected (precise format)
- Output Produced (format, side effects, duration)
- Compatible Skills After
- Called By (bidirectional)
- Tools Used
- Visual Workflow
- Usage Example

**Red flags:**
- No mention of other skills
- Input/output format unclear
- No workflow context
- Skill appears isolated

### Error Handling (1-5)

**Check for:**
- Common errors documented
- Error messages explained
- Solutions/workarounds provided
- Validation before critical ops

**Red flags:**
- "If it fails, debug it"
- No error scenarios
- No troubleshooting section
- Assumes everything works

## Score Calculation

```
Average = Sum of all 9 scores / 9
```

## Score Interpretation

| Range | Status | Action |
|-------|--------|--------|
| 1.0-2.4 | Needs major rework | Do not use |
| 2.5-3.4 | Functional | Significant improvements needed |
| 3.5-4.4 | Good | Minor refinements |
| 4.5-5.0 | Excellent | Production ready |

**Minimum for production**: 3.5/5
**No dimension < 3/5** (critical threshold)
