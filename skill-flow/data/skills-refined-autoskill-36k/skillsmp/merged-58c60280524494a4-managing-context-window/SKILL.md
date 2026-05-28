---
name: managing-context-window
description: Use this skill when you need to efficiently manage context windows by summarizing, focusing, and pruning information to stay within token limits.
---

# Managing Context Window Skill

## When to Use

- Context window is getting full
- User requests a summary of conversation history
- Need to focus on specific tasks or files
- Working with large files or codebases
- Memory constraints

## What This Skill Does

1. Analyzes current context usage
2. Identifies non-essential information
3. Creates summaries of conversation history
4. Focuses context on high-priority items
5. Suggests pruning strategies to optimize context efficiency

## Strategies

### 1. Summarize Previous Work

- Summarize key decisions made
- List files modified
- Note important patterns discovered
- Prune old discussions not relevant to the current task

### 2. Selective File Reading

- Use offset and limit for large files:
  ```
  Read specific sections with offset/limit
  Read file_path offset=100 limit=50
  ```

- Use Grep instead of reading entire files:
  ```
  Grep pattern="function calculateTSS" path=packages/core/calculations/
  ```

### 3. Focus on Current Task

Keep only:
- Current implementation goals
- Relevant code files
- Recent error messages
- Specific questions to answer

### 4. Prune Redundant Information

- Remove completed sub-tasks
- Remove duplicate or outdated context
- Remove exploratory messages

### 5. Use Task Agents for Large Searches

- Instead of multiple Glob and Grep calls, use a Task tool with an Explore agent for thorough searches.

### 6. Batch Operations

- Instead of reading files separately, read multiple files in a single message with parallel tool calls.

### 7. Efficient Pattern Matching

- Use Grep to find specific code and read only the relevant sections.

## Context Management Checklist

When context is getting full:

- [ ] Have I read files I don't need?
- [ ] Can I use Grep instead of Read?
- [ ] Can I use offset/limit for large files?
- [ ] Can I delegate exploration to a Task agent?
- [ ] Have I summarized previous context?
- [ ] Am I batching tool calls efficiently?
- [ ] Am I focusing on high-priority files?

## Best Practices

1. Use TodoWrite for tracking progress.
2. Reference files instead of pasting full content.
3. Summarize completed work regularly.
4. Keep error messages relevant.
5. Use specific line ranges when reading.

## Critical Don'ts

- ❌ Don't read entire large files without good reason.
- ❌ Don't re-read files unnecessarily.
- ❌ Don't use Read when Grep would suffice.
- ❌ Don't explore exhaustively without strategy.

## Pro Tips

- **Use Grep first** to locate code, then Read specific sections.
- **Batch file reads** in a single message with multiple tool calls.
- **Summarize aggressively** as conversation grows.
- **Reference files by path + line number** instead of including full content.
- **Focus on changed files** in git repositories.