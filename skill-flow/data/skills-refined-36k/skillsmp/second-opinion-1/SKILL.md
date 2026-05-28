---
name: second-opinion
description: "Automatically initiates Codex review sessions in tmux for implementation plans and significant code changes. Use this skill proactively when: (1) Exiting plan mode with a completed implementation plan, (2) Making substantial code changes that would benefit from peer review (multi-file refactors, architectural changes, complex features), (3) User explicitly requests Codex review. The skill manages tmux panes, polls for Codex responses, iterates on feedback, and closes the session when review is complete."
---

# Second Opinion

Automatically leverage Codex for code review by launching review sessions in tmux panes, managing the review conversation, and iterating until approval.

## When to Use

Use this skill proactively in these scenarios:

1. **After creating an implementation plan** - Automatically when exiting plan mode
2. **Significant code changes** - Multi-file refactors, architectural changes, new features
3. **User request** - When explicitly asked to get Codex feedback

**Decision heuristic:** If the change is non-trivial and would benefit from a second opinion, use this skill.

## Workflow

1. **Start Review Session**
   - Create tmux horizontal split with Codex in right pane
   - Send initial review prompt with context (plan file or code changes)
   - Set up output monitoring

2. **Poll for Response**
   - Check Codex output every 3-5 seconds
   - Wait for response completion (detect output pause)
   - Read and analyze feedback

3. **Iterate on Feedback**
   - If issues found: Address them and send updated version
   - If questions raised: Provide clarifications or counterarguments
   - If approved: Proceed to closure

4. **Close Session**
   - When review complete (no more concerns, implicit approval)
   - Kill Codex pane
   - Clean up session files

## Implementation

### Starting a Review

```bash
# Create review session with tmux split
OUTPUT_DIR="/tmp/codex-review-$(date +%s)"
./scripts/start_codex_review.sh "$REVIEW_PROMPT" "$OUTPUT_DIR"
```

The script creates:
- Horizontal tmux split (left: Claude Code, right: Codex)
- Output directory with session metadata
- Log file for Codex responses

### Monitoring Progress

```bash
# Poll for new output (call every 3-5 seconds)
STATUS=$(./scripts/check_codex_status.sh "$OUTPUT_DIR")

if echo "$STATUS" | head -1 | grep -q "new_output"; then
    # New response available
    NEW_CONTENT=$(echo "$STATUS" | tail -n +2)
    # Analyze and respond
fi
```

### Sending Follow-ups

```bash
# Send response to Codex
./scripts/send_to_codex.sh "$OUTPUT_DIR" "Updated the plan to address your concerns: ..."
```

### Ending the Session

```bash
# Close Codex pane when done
./scripts/close_codex_session.sh "$OUTPUT_DIR"
```

## Review Prompts

### For Implementation Plans

```
Review the following implementation plan for potential issues, architectural concerns,
or improvements. Focus on:
- Correctness and completeness
- Potential edge cases or bugs
- Better approaches or patterns
- Security or performance concerns

[Plan content here]

Provide specific, actionable feedback. If the plan looks good, say so clearly.
```

### For Code Changes

```
Review these code changes:

Files modified:
- [List of files]

Changes summary:
[Brief description]

Code diff:
[Actual changes]

Point out any issues, suggest improvements, or confirm if it looks good.
```

## Completion Detection

Determine review completion by analyzing Codex's response tone and content:

- **Approved**: "Looks good", "LGTM", "No issues", "Approved", positive without new concerns
- **Needs work**: Specific issues listed, questions raised, suggestions for changes
- **Ambiguous**: Ask follow-up to clarify

**Important**: Don't wait for explicit "DONE" signal. Use natural language understanding to detect completion.

## Error Handling

- **Tmux not running**: Error early, ask user to start tmux session
- **Codex not found**: Verify `codex` command is in PATH
- **Pane closed unexpectedly**: Detect in polling loop, restart if needed
- **Codex hangs**: Timeout after 60s of no output, prompt user

## Scripts

- `start_codex_review.sh` - Initialize tmux split and Codex session
- `check_codex_status.sh` - Poll for new Codex output
- `send_to_codex.sh` - Send follow-up message to Codex
- `close_codex_session.sh` - Clean up tmux pane and session files
