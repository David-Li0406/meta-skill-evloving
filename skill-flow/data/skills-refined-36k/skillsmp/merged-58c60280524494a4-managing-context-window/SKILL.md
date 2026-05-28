---
name: managing-context-window
description: Use this skill to efficiently manage context windows by summarizing, focusing, and pruning information to stay within token limits.
---

# Managing Context Window Skill

## When to Use

- Context window is approaching token limits
- Need to focus on specific files or tasks
- Long conversations requiring summarization
- Working with large files or codebases
- Memory constraints

## What This Skill Does

1. Analyzes current context usage
2. Identifies non-essential information
3. Creates summaries of conversation history
4. Focuses context on high-priority items
5. Suggests pruning strategies
6. Optimizes tool usage for context efficiency

## Strategies

### 1. Summarize Previous Work

When conversation gets long, summarize key decisions made, list modified files, and note important patterns discovered.

### 2. Selective File Reading

Instead of reading entire large files, use offset and limit to read specific sections. For example:
```
Read file_path offset=<offset_value> limit=<limit_value>
```
Use Grep to find specific sections instead of reading entire files:
```
Grep pattern="<search_pattern>" path=<file_path>
```

### 3. Focus on Changed Files

Use version control commands to focus on files that have changed:
```
git diff --name-only
```

### 4. Prune Redundant Information

Remove completed sub-tasks, duplicate information, and outdated context. Keep only relevant decisions and error messages.

### 5. Use Task Agents for Large Searches

Instead of multiple tool calls, delegate exploration to a Task agent to handle thorough searches and report back.

### 6. Batch Operations

Read multiple files in a single message with parallel tool calls to reduce context usage.

### 7. Efficient Pattern Matching

Use Grep to find specific functions or patterns, then read only the relevant sections.

## Context Management Checklist

When context is getting full:

- [ ] Have I read files I don't need?
- [ ] Can I use Grep instead of Read?
- [ ] Can I use offset/limit for large files?
- [ ] Can I delegate exploration to a Task agent?
- [ ] Have I summarized previous context?
- [ ] Am I batching tool calls efficiently?
- [ ] Am I focusing on high-priority files?

## Example: Efficient File Exploration

**❌ BAD (High context usage):**
```
1. Read entire 3000-line file to understand structure
2. Read 10 more files to find related code
3. Read test files to understand usage
4. Summarize findings
```

**✅ GOOD (Low context usage):**
```
1. Grep pattern="class ActivityRecorder" to find main file
2. Read just the class definition (offset/limit)
3. Grep pattern="useActivityRecorder" to find usage
4. Read only relevant usage examples
5. Use Task agent to explore test patterns
```

## Critical Don'ts

- ❌ Don't read entire large files without good reason
- ❌ Don't re-read files unnecessarily
- ❌ Don't use Read when Grep would suffice
- ❌ Don't explore exhaustively without strategy
- ❌ Don't include long code blocks in responses unless needed
- ❌ Don't make multiple sequential tool calls when parallel would work

## Pro Tips

- **Use Grep first** to locate code, then Read specific sections
- **Batch file reads** in a single message with multiple tool calls
- **Use Task agents** for exploratory work
- **Summarize aggressively** as conversation grows
- **Reference files by path + line number** instead of including full content
- **Use offset/limit** for large files
- **Focus on changed files** in git repos