---
name: managing-context-window
description: Helps manage context window efficiently by summarizing, focusing, and pruning
---

# Managing Context Window Skill

## When to Use
- Context window getting full
- Need to focus on specific files
- Long conversations requiring summarization
- Working with large files
- Memory constraints

## What This Skill Does
1. Identifies which files/context are most relevant
2. Summarizes less-relevant information
3. Focuses on high-priority items
4. Suggests pruning strategies
5. Optimizes tool usage for context efficiency

## Strategies

### 1. Selective File Reading

**Use offset and limit for large files:**
```
Instead of:
Read entire 5000-line file

Do this:
Read specific sections with offset/limit
Read file_path offset=100 limit=50
```

**Use Grep instead of reading entire files:**
```
Instead of:
Read file to find function

Do this:
Grep pattern="function calculateTSS" path=packages/core/calculations/
```

### 2. Focus on Changed Files

```
Instead of:
Reading all files in project

Do this:
git diff --name-only
Focus on files that actually changed
```

### 3. Summarize Previous Context

When conversation gets long:
- Summarize key decisions made
- List files modified
- Note important patterns discovered
- Prune old discussion not relevant to current task

### 4. Use Task Agents for Large Searches

```
Instead of:
Multiple Glob and Grep calls exploring codebase

Do this:
Use Task tool with Explore agent for thorough searches
Let agent handle the exploration and report back
```

### 5. Batch Operations

```
Instead of:
Read file1.ts
Read file2.ts
Read file3.ts
(3 separate messages)

Do this:
Read all 3 files in single message with parallel tool calls
```

### 6. Strategic Tool Usage

**Glob for finding files:**
- Use when you need to find files by pattern
- Returns just file paths (low context usage)

**Grep for finding content:**
- Use when you need to find specific code
- Use output_mode: "files_with_matches" for minimal context
- Use output_mode: "content" only when needed

**Read for targeted reading:**
- Use when you need full file content
- Use offset/limit for large files
- Read multiple files in parallel

### 7. Avoid Redundant Reads

**Keep track of what you've read:**
- Don't re-read files unnecessarily
- Summarize key information from files
- Reference line numbers for context

### 8. Efficient Pattern Matching

```
Instead of:
Read entire file to find one function

Do this:
Grep to find the function
Read only the relevant section
```

## Context Management Checklist

When context is getting full:

- [ ] Have I read files I don't need?
- [ ] Can I use Grep instead of Read?
- [ ] Can I use offset/limit for large files?
- [ ] Can I delegate exploration to Task agent?
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

## Example: Managing Long Conversations

**When conversation exceeds 50% context:**

1. **Summarize what's been done:**
   - Files created/modified
   - Key decisions made
   - Current task status

2. **Focus on current goal:**
   - What remains to be done
   - Which files are relevant
   - What context is needed

3. **Prune old context:**
   - Remove detailed discussions of completed tasks
   - Keep only relevant decisions
   - Summarize long explanations

## Tools for Context Efficiency

### High Context Usage
- Reading large files completely
- Multiple file reads without batching
- Redundant reads of same files
- Exploring without strategy

### Low Context Usage
- Glob with specific patterns
- Grep with files_with_matches mode
- Read with offset/limit
- Task agent for exploration
- Parallel tool calls

## When Context is Critical

If context is nearly full and task is incomplete:

1. **Prioritize ruthlessly:**
   - What information is absolutely necessary?
   - What can be inferred or looked up later?

2. **Summarize aggressively:**
   - Condense previous findings
   - Keep only essential information

3. **Use external memory:**
   - Write important information to files
   - Use task agents to handle sub-tasks
   - Reference line numbers instead of including code

4. **Focus on completion:**
   - Finish current task before exploring new areas
   - Defer nice-to-have information
   - Prioritize working code over perfect understanding

## Critical Don'ts

- ❌ Don't read entire large files without good reason
- ❌ Don't re-read files unnecessarily
- ❌ Don't use Read when Grep would suffice
- ❌ Don't explore exhaustively without strategy
- ❌ Don't include long code blocks in responses unless needed
- ❌ Don't make multiple sequential tool calls when parallel would work

## Pro Tips

- **Use Grep first** to locate code, then Read specific sections
- **Batch file reads** in single message with multiple tool calls
- **Use Task agents** for exploratory work
- **Summarize aggressively** as conversation grows
- **Reference files by path + line number** instead of including full content
- **Use offset/limit** for large files
- **Focus on changed files** in git repos
