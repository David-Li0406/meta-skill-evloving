# Problem Decomposition Guide

## When to Decompose

Break down research when:
- Multiple independent areas need exploration
- Different expertise levels required (search vs analysis)
- Parallel investigation would speed up discovery

## Decomposition Strategies

### By Component
Split by system boundaries:
- Frontend vs backend
- API vs database
- Core logic vs utilities

### By Question Type
Split by investigation method:
- "What exists?" → Grep/Glob searches
- "How does it work?" → File reading + analysis
- "Why was it built this way?" → Git history + comments

### By Depth
Split by detail level:
- Surface scan → `haiku` subagent
- Code understanding → `sonnet` subagent
- Architecture analysis → `opus` subagent

## Subagent Prompts

### Search Subagent (haiku)
```
Find all files matching [pattern]. Return file paths only.
```

### Read Subagent (haiku)
```
Read [file] and extract:
1. Main purpose
2. Key functions/classes
3. Dependencies
Return bullet points, not full content.
```

### Analysis Subagent (sonnet/opus)
```
Analyze [component] focusing on:
1. How data flows through it
2. What patterns it uses
3. Where it connects to other parts
Return structured findings.
```

## Anti-Patterns

- **Over-decomposition**: 50 subagents for a simple question
- **Under-decomposition**: One giant exploration polluting context
- **Wrong model**: Using opus for simple grep tasks
