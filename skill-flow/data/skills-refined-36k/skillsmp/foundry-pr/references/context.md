# Context Sources

The skill analyzes several key sources (available via the MCP tool `mcp__plugin_foundry_foundry-mcp__pr action="context"`):

## 1. Spec Metadata
High-level information about the feature/change:
- Title and description
- Objectives and success criteria
- Phase and task structure

## 2. Completed Tasks
Granular details about implementation:
- File paths modified
- Changes made in each file
- Task completion timestamps

## 3. Commit History
Development progression:
- Commit messages and SHAs
- Task-to-commit associations
- Chronological flow

## 4. Journal Entries
Decision logs and notes:
- Technical approach decisions
- Challenges and solutions
- Implementation rationale

The MCP tool `mcp__plugin_foundry_foundry-mcp__journal action="list"` supplies recent entries (optionally scoped to a specific task).

## 5. Git Diff
Actual code changes:
- Full diff or file-level summary
- Code-level understanding
- Verification of changes
