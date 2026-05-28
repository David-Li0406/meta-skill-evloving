---
name: auto-learner
description: Use this skill to learn from mistakes. Activate when Claude makes tool call errors, incorrect assumptions, oversights, or when the user corrects Claude. Maintains auto-learning.md as a knowledge base of lessons learned.
---

# Auto-Learner Skill

Learn from mistakes by maintaining a persistent knowledge base of lessons learned.

## When to Add a Learning

Add a note to `auto-learning.md` when:

- A tool call fails due to incorrect parameters or wrong assumptions
- You make an incorrect assumption about the codebase
- The user corrects you on something
- You discover a pattern that would have prevented an earlier mistake
- A retry was needed because of an oversight
- You realize you should have done something differently

## The auto-learning.md File

Located at project root. Create it if it doesn't exist.

### File Format

```markdown
# Auto-Learning Notes

Lessons learned from past mistakes. Priority scores (1-10) reflect importance.

---

## [P8] Short descriptive title
**Context:** Brief context of when this happened
**Mistake:** What went wrong
**Learning:** What to do instead
**Tags:** #tool-call #assumption #oversight (pick relevant tags)

---

## [P5] Another learning title
...
```

### Priority Scoring (1-10)

- **9-10**: Critical - caused significant issues, applies frequently
- **7-8**: Important - common mistake, high value to remember
- **5-6**: Moderate - useful but less frequent
- **3-4**: Minor - edge case or rare situation
- **1-2**: Low - might be project-specific or outdated

### Updating Priorities

When you encounter a situation where a past learning was valuable:
1. Read the existing note
2. Increment its priority by 1 (max 10)
3. Update the note if you have additional insight

When a learning proves irrelevant over time:
1. Decrement priority by 1
2. If it drops below 2, consider removing it

## Adding a New Learning

1. Read `auto-learning.md` (create if missing)
2. Add new note at the TOP (after the header)
3. Start with priority [P5] unless clearly more/less important
4. Keep notes compact - 2-4 lines max per section
5. Use specific, actionable language

### Example Entry

```markdown
## [P7] Always read files before editing
**Context:** Tried to edit a file without reading it first
**Mistake:** Edit tool failed because I hadn't read the file in this session
**Learning:** Always use Read tool before Edit tool on any file, even if it seems obvious
**Tags:** #tool-call #edit
```

## Size Management

Check file size periodically (every 3-5 learnings added):

1. If more than **25 entries**, prune the lowest priority ones
2. Remove entries with P1-P2 that haven't been referenced recently
3. Consider merging similar learnings into one higher-priority note
4. Target: Keep 15-20 high-value learnings

## When Starting a Session

When working on this project, briefly review `auto-learning.md` to refresh on past lessons. Pay attention to P7+ entries.

## Important

- Be honest about mistakes - this is for self-improvement
- Keep learnings actionable and specific
- Don't add learnings for one-off user preferences (those go in CLAUDE.md)
- Focus on patterns that will recur
