# Checkpoint Context Prompt v1

## Purpose

Summarize the **context of a checkpoint** (an assistant response boundary) so it can be indexed and routed to later. Focus on semantic retrieval: title, description, keywords, entities, topics, tools used, and files touched.

## Input

- **Checkpoint metadata**: source, session ID, message index
- **Conversation context**: short summary or excerpt leading up to the checkpoint
- **Assistant response**: full text of the checkpoint response
- **Tool calls (ordered)**: tool name + high-level args + exit status
- **Files touched**: file path + operation type

## Task

Extract:

1. **Title** (3-5 words)
2. **Description** (one sentence)
3. **Keywords** (5-10 terms)
4. **Entities** (people, projects, files, systems)
5. **Topics** (high-level themes)
6. **Tools invoked** (names + purpose, in order)
7. **Files touched** (path + operation type)

## Output Format (JSON)

```json
{
  "title": "Worktree setup for dark-mode",
  "description": "Created a worktree for the dark-mode branch and configured environment setup.",
  "keywords": ["worktree", "git", "dark-mode", "env", "setup"],
  "entities": ["dark-mode", "worktree", "nexus"],
  "topics": ["repo setup", "branch workflows"],
  "tools_invoked": [
    {"name": "git", "purpose": "create worktree", "order": 1},
    {"name": "cp", "purpose": "copy env files", "order": 2}
  ],
  "files_touched": [
    {"path": "apps/web/.env", "operation": "read"},
    {"path": "apps/web/.env.local", "operation": "write"}
  ]
}
```

## Rules

- Output **valid JSON only**
- Keep title short and specific
- Favor semantic keywords that will help retrieval later
- Tools/files should be minimal, relevant, and ordered

---

## Checkpoint Input

{{{segment_text}}}
