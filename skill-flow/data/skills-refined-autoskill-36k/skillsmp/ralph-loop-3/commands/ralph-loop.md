---
description: "Start Ralph Loop in current session"
argument-hint: "PROMPT [--max-iterations N] [--completion-promise TEXT]"
allowed-tools: ["Bash(${CLAUDE_PLUGIN_ROOT}/scripts/setup-ralph-loop.sh:*)"]
hide-from-slash-command-tool: "true"
---

# Ralph Loop Command

Execute the setup script to initialize the Ralph loop:

```!
"${CLAUDE_PLUGIN_ROOT}/scripts/setup-ralph-loop.sh" $ARGUMENTS
```

Please work on the task. When you try to exit, the Ralph loop will feed the SAME PROMPT back to you for the next iteration. You'll see your previous work in files and git history, allowing you to iterate and improve.

CRITICAL RULE: If a completion promise is set, you may ONLY output it when the statement is completely and unequivocally TRUE. Do not output false promises to escape the loop, even if you think you're stuck or should exit for other reasons. The loop is designed to continue until genuine completion.

## Review Mode (`--mode review`)

When running in review mode, you can ask the user questions at decision points. The loop will pause until they respond.

### How to Ask Questions

1. **Write a steering file** at `.claude/ralph-steering-{task-id}.md`:

```markdown
---
status: pending
---

## Question

Your question here. Be specific about what you need to know.

**Options:**
1. Option A - description
2. Option B - description

## Response

(awaiting user response)
```

2. **Use AskUserQuestion tool** to wait for the response:
   - When you see `⚠️ PENDING QUESTION FOR USER` in the system message, use the `AskUserQuestion` tool
   - This properly pauses the loop until the user responds
   - Do NOT just output text - the loop will continue without waiting

3. **Update the steering file** after getting the answer:
   - Change `status: pending` to `status: answered`
   - Add the user's response under `## Response`

### Example Flow

```
Iteration 1: Write steering file with status: pending
Iteration 2: See pending question → Use AskUserQuestion → Update file with answer
Iteration 3+: Continue with user's decision
```
