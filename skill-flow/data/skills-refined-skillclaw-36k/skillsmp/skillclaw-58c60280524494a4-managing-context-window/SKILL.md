---
name: managing-context-window
description: Use this skill when you need to efficiently manage your context window by summarizing, focusing, and pruning information to stay within token limits.
---

# Managing Context Window Skill

## When to Use
- Context window is getting full
- Need to focus on specific files or tasks
- Long conversations requiring summarization
- Working with large files or codebases
- Memory constraints

## What This Skill Does
1. Analyzes current context usage and identifies relevant information.
2. Summarizes less-relevant or outdated information.
3. Focuses on high-priority items and current tasks.
4. Suggests pruning strategies to optimize context usage.
5. Recommends efficient tool usage for managing context.

## Strategies

### 1. Summarize Previous Work
- Create a summary of key decisions and tasks completed.
- Example:
  ```
  Summary of work so far:
  - Implemented activity recording service
  - Added GPS tracking functionality
  - Current task: Add activity statistics calculation
  ```

### 2. Selective File Reading
- Use offset and limit for large files:
  ```
  Read file_path offset=100 limit=50
  ```
- Use Grep to find specific sections instead of reading entire files:
  ```
  Grep pattern="function calculateTSS" path=packages/core/calculations/
  ```

### 3. Focus on Changed Files
- Use version control to identify modified files:
  ```
  git diff --name-only
  ```

### 4. Prune Redundant Information
- Remove completed tasks, duplicates, and outdated context.
- Keep only relevant error messages and specific questions.

### 5. Batch Operations
- Read multiple files in a single operation to reduce context usage:
  ```
  Read file1.ts, file2.ts, file3.ts in one message.
  ```

### 6. Efficient Tool Usage
- Use Glob for finding files by pattern.
- Use Grep for finding specific content with minimal context.
- Use targeted reading with offset/limit for large files.

### 7. Avoid Redundant Reads
- Keep track of what you've read to avoid unnecessary re-reads.
- Summarize key information from files and reference line numbers.

## Implementation Example
```typescript
// Use TodoWrite to track progress instead of comments
const todos = [
  { id: "1", content: "Implement activity recording", status: "completed" },
  { id: "2", content: "Add GPS tracking", status: "completed" },
  { id: "3", content: "Create activity detail view", status: "in_progress" },
];

// When switching tasks, update context
function switchTask(newTask: string) {
  return {
    task: newTask,
    relevantFiles: getRelevantFiles(newTask),
    summary: summarizeCompletedWork(),
  };
}
```

## Best Practices
1. Use TodoWrite for tracking.
2. Reference files instead of pasting full contents.
3. Summarize completed work and focus on current tasks.
4. Keep error messages relevant and prune outdated context.