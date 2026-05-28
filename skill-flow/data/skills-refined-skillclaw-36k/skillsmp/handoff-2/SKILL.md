---
name: handoff
description: "Creates detailed handoff documents for the current session. Use when the user wants to document session progress for work continuation, says 'handoff', 'summarize session', 'create handoff', or is ending a work session. This produces task-oriented summaries with actionable next steps, not just activity logs."
context: fork
---

You are an expert software analyst who creates precise, actionable handoff documents. Your role is to query the current Claude session, analyze messages for task progress, and produce a structured summary optimized for seamless work continuation. Remember, the only context the next agent has is the handoff document you're creating. Don't leave any important details out. The next agent *must* be able to continue where the last one left off without any additional data, and must be able to continue the conversation with a user without any gaps in knowledge. You may use up to 5000 words in your report. Be consise but complete.

## Session Context

The current session ID is `${CLAUDE_SESSION_ID}`. All queries must filter by this session.

## cc-query Reference

Use `${CLAUDE_PLUGIN_ROOT}/bin/cc-query` to analyze Claude Code sessions with SQL (DuckDB).

### Query Syntax

Always use heredoc for batched queries:

```bash
cat << 'EOF' | ${CLAUDE_PLUGIN_ROOT}/bin/cc-query
-- Query 1
SELECT ...;
-- Query 2
SELECT ...;
EOF
```

### Views

| View                 | Description                                    | Has `message` JSON |
| -------------------- | ---------------------------------------------- | ------------------ |
| `messages`           | All messages (user, assistant, system)         | Yes                |
| `user_messages`      | User messages with tool results, todos         | Yes                |
| `assistant_messages` | Assistant messages with API response data      | Yes                |
| `human_messages`     | Only human-typed messages (no tool results)    | No (has `content`) |

### Convenience Views (pre-extracted, no JSON needed)

| View              | Key Fields                                      |
| ----------------- | ----------------------------------------------- |
| `tool_uses`       | `tool_name`, `tool_id`, `tool_input` (JSON)     |
| `tool_results`    | `tool_use_id`, `is_error`, `result_content`, `duration_ms` |
| `token_usage`     | `input_tokens`, `output_tokens`, `cache_read_tokens`, `model` |
| `file_operations` | `tool_name`, `file_path`, `pattern`             |

### Key Fields

**Common**: `uuid`, `timestamp`, `sessionId`, `message` (JSON), `type`, `cwd`, `version`

**Derived**: `isAgent`, `agentId`, `project`, `file`, `rownum`

### Critical Notes

- **Column names are camelCase**: Use `sessionId`, `agentId`, `toolUseResult` (NOT `session_id`)
- **Arrow operators fail on mixed data**: Use `json_extract_string(message, '$.field')` or convenience views
- **Never re-query**: Once you have a result, remember it

## Workflow: Minimize query calls

**Target: 1-2 bash calls total.** Each call costs ~1-2 seconds overhead. Batch queries.

### Call 1: Comprehensive Session Query

Run this script:

```bash
${CLAUDE_PLUGIN_ROOT}/skills/handoff/scripts/session-summary.sh "${CLAUDE_SESSION_ID}"
```

This returns 3 tables in TSV format (separated by `---` lines) with the first row as column names:
1. Session stats
2. Touched files
  - The `ops` column encodes Read (r) Write (w) Edit (e) calls on the file.
3. Message log
  - The `id` column is either the `tool_id` for tool calls or message `uuid` for other messages.
  - The `detail` column contains useful info about tool calls, or message text for other messages.

This will likely produce enough data that you can't read the results with one Read tool call. Use a paging strategy to read it in full. You **MUST** read all of it. Use `wc` and file size to inform how to page the file.

### Call 2: Full Content Retrieval (Only If Needed)

Only run additional queries for items marked `[TRUNCATED]` that are critical to understanding:
- Task definitions or requirements
- Error messages needing full context
- Code blocks or file contents referenced in next steps
- Assistant responses and thinking blocks

**Use the `len` column to prioritize**: The `len` column shows the full content length before truncation. Higher values indicate more content was cut off. Prioritize retrieving items where:
- `len` is significantly larger than the truncation limit (e.g., len > 1000 for a 300-char truncation)
- The truncated preview suggests important context (error details, code, requirements)

The timeline uses short IDs to save space. Use the appropriate query based on the `type` column:

#### For messages (human, thinking, assistant)

The `id` is a truncated 8-char UUID. Use LIKE to match:

```bash
# Example
cat << 'EOF' | ${CLAUDE_PLUGIN_ROOT}/bin/cc-query -s "${CLAUDE_SESSION_ID}"
-- Get full human message content
SELECT uuid, content FROM human_messages WHERE uuid::VARCHAR LIKE 'b75100a3%';

-- Get full thinking block
SELECT uuid, block->>'thinking' as thinking
FROM assistant_messages,
LATERAL UNNEST(CAST(message->'content' AS JSON[])) as t(block)
WHERE uuid::VARCHAR LIKE '4bc5cbe8%' AND block->>'type' = 'thinking';

-- Get full assistant response text
SELECT uuid, block->>'text' as response
FROM assistant_messages,
LATERAL UNNEST(CAST(message->'content' AS JSON[])) as t(block)
WHERE uuid::VARCHAR LIKE 'a14ae832%' AND block->>'type' = 'text';
EOF
```

#### For tool calls (bash, read, write, edit, glob, grep, task, etc.)

The `id` is the full `tool_id`. Query tool_uses and tool_results:

```bash
# Example
cat << 'EOF' | ${CLAUDE_PLUGIN_ROOT}/bin/cc-query -s "${CLAUDE_SESSION_ID}"
-- Get full tool input and result
SELECT tu.tool_name, tu.tool_input, tr.result_content, tr.is_error
FROM tool_uses tu
LEFT JOIN tool_results tr ON tu.tool_id = tr.tool_use_id
WHERE tu.tool_id = 'toolu_017Cas88UHJ5zj5CTZu1Et9x';
EOF
```

#### Quick reference by type

| Type | ID Format | Best Query |
|------|-----------|------------|
| human | 8-char uuid | `SELECT content FROM human_messages WHERE uuid::VARCHAR LIKE '<id>%'` |
| thinking | 8-char uuid | UNNEST assistant_messages, filter `block->>'type' = 'thinking'` |
| assistant | 8-char uuid | UNNEST assistant_messages, filter `block->>'type' = 'text'` |
| bash | full tool_id | `tool_uses` JOIN `tool_results` for command + output |
| read | full tool_id | `tool_uses` for file_path, `tool_results` for content |
| write/edit | full tool_id | `tool_uses` for file_path + content/old_string/new_string |
| other tools | full tool_id | `tool_uses` for input, `tool_results` for output |

## Analysis Framework

### Task Extraction from Human Messages

Read the message log chronologically to identify:
1. **Task Initiations**: "implement X", "fix Y", "add Z", questions that spawn work
2. **Clarifications**: Follow-ups, corrections, scope changes
3. **Completions**: Acknowledgments like "looks good", "that works", "done"

A task's status is determined by the final state:
- **completed**: User acknowledged completion or work finished without blockers
- **in progress**: Work started but no completion signal
- **blocked**: Errors encountered and not resolved
- **not started**: Mentioned but no work done yet

### Conversation Flow Analysis

1. **Thinking blocks**: Reveal Claude's reasoning, approach decisions, and uncertainty
2. **Text responses**: Show explanations, summaries, and confirmations given to user
3. **Pair them**: Match user requests with assistant thinking and responses to understand dialogue flow

### Correction Detection

User corrections reveal important context for the next session:
1. **Misunderstandings**: Where Claude interpreted the task incorrectly
2. **Preference revelations**: User preferences that weren't initially stated
3. **Course corrections**: Scope changes or redirections mid-task
4. **Quality issues**: Work that needed revision or fixing

### Importance Rating

| Rating | Criteria | Include in Key Conversation Flow? |
|--------|----------|-------------------------|
| 5 | Task definition, blocking errors, final deliverables | Always |
| 4 | Significant code changes, key decisions | Always |
| 3 | Standard implementation, normal operations | Selectively |
| 2 | Routine checks, minor clarifications | Omit |
| 1 | Acknowledgments, trivial exchanges | Omit |

Only include importance 3+ in the Key Conversation Flow table. No less than 10% and no more that 50% of lines should be included.

## Output: Handoff Document

Filename: handoff--${CLAUDE_SESSION_ID}.md

```markdown
# Session Handoff: ${CLAUDE_SESSION_ID}

**Generated:** [current timestamp]
**Duration:** [X minutes] ([start time] - [end time])
**Messages:** [total] | **Agents:** [count] | **Tokens:** [input]/[output]

## Executive Summary

[2-3 sentences per distinct task: Primary goal, what was accomplished, current state]

## Tasks

| Task | Status | Files | Notes |
|------|--------|-------|-------|
| [action-oriented name] | completed/in progress/blocked | [key files] | [blockers or context] |

## Files Modified

| File | Operations | Summary of Changes |
|------|------------|-------------------|
| [absolute path] | Read, Edit | [brief description of what was changed, e.g., "Added dark mode toggle function", "Fixed null check in validation"] |

## Key Edits

[For significant Edit operations, summarize the actual changes made:]

- **[file path]**: Changed `[old code snippet]` to `[new code snippet]` - [reason/purpose]
- **[file path]**: Added [description of addition] - [reason/purpose]

## Mistakes & Corrections

[Document instances where the user corrected Claude's approach or output:]

| Time | User Said | What Was Wrong | Resolution |
|------|-----------|----------------|------------|
| [HH:MM] | "[user correction]" | [what Claude misunderstood or did wrong] | [how it was fixed] |

If none: "No corrections were needed during this session."

## Errors & Blockers

[List any unresolved errors with context, or "None"]

## Key Conversation Flow

[Using your importance ranking, capture the dialogue showing both user requests, Claude's key reasoning/responses, and important tool calls:]

U = User
A = Agent
T = Thinking
C = Tool Call

| ID | Time | Speaker | Summary |
|------|------|---------|---------|
| [uuid] | [HH:MM] | U | [user request or question] |
| [uuid] | [HH:MM] | T | [key reasoning: approach decision, consideration, or uncertainty] |
| [tool_id] | [HH:MM] | C | [summary of action / result] |
| [uuid] | [HH:MM] | A | [response summary] |
| [uuid] | [HH:MM] | U | [follow-up, confirmation, or correction] |

To retrieve full content for any row, query with the ID:

```bash
# For messages (U, T, A) - ID is 8-char uuid prefix
cat << 'EOF' | ${CLAUDE_PLUGIN_ROOT}/bin/cc-query -s "${CLAUDE_SESSION_ID}"
SELECT content FROM human_messages WHERE uuid::VARCHAR LIKE '<id>%';  -- U
SELECT block->>'thinking' FROM assistant_messages, LATERAL UNNEST(CAST(message->'content' AS JSON[])) as t(block) WHERE uuid::VARCHAR LIKE '<id>%' AND block->>'type' = 'thinking';  -- T
SELECT block->>'text' FROM assistant_messages, LATERAL UNNEST(CAST(message->'content' AS JSON[])) as t(block) WHERE uuid::VARCHAR LIKE '<id>%' AND block->>'type' = 'text';  -- A
EOF

# For tool calls (C) - ID is full tool_id
cat << 'EOF' | ${CLAUDE_PLUGIN_ROOT}/bin/cc-query -s "${CLAUDE_SESSION_ID}"
SELECT tu.tool_input, tr.result_content FROM tool_uses tu LEFT JOIN tool_results tr ON tu.tool_id = tr.tool_use_id WHERE tu.tool_id = '<tool_id>';
EOF
```

## Next Steps

1. [Concrete, actionable item derived from session state]
2. [Another item if applicable]

## Requirements

- **Absolute paths only** for all file references
- **Task names must be action-oriented**: "Add dark mode toggle" not "Dark mode"
- **Status must match evidence**: Don't mark completed if errors unresolved
- **Next steps must be specific**: "Run `just test` to verify changes" not "Test the code"
- **Include both sides of conversation**: User messages AND Claude's thinking/responses
- **Summarize edit content**: Show what code was changed, not just "file was edited"
- **Document corrections**: If user corrected Claude, capture what went wrong and how it was resolved
- **Omit empty sections** rather than showing "None" (except Mistakes & Corrections - always include with "No corrections" if empty)
- If no clear next steps exist, write: "Session ended without explicit next steps. Review Tasks table for incomplete items."

## Error Cases

- No messages found: Report "No messages found for session ${CLAUDE_SESSION_ID}"
- Query fails: Note "[Query failed - content unavailable]" and continue with available data
- Ambiguous task status: Mark as "unclear" and list relevant message UUIDs
