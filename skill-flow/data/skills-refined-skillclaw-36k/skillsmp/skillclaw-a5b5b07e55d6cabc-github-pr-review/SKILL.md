---
name: github-pr-review
description: Use this skill when you need to conduct a systematic review of a pull request (PR) and provide actionable feedback.
---

# Skill body

## Execution Steps

### 1. Retrieve PR Information

Use the following commands to gather information about the PR:

```bash
gh pr view --comments
gh pr diff
gh pr checks
```

### 2. Conduct Codex Analysis

If you are using tmux, run:

```bash
TMUX_MGR=~/.claude/skills/tmux-codex-review/scripts/tmux-manager.sh
$TMUX_MGR ensure
$TMUX_MGR send "Please review the gh pr diff. Classify issues by priority P0-P3, and report each comment in the format [PX] file:line - summary of the issue."
$TMUX_MGR wait_response 180
$TMUX_MGR capture 300
```

If you are not using tmux, run:

```bash
codex exec "Please review the gh pr diff. Classify issues by priority P0-P3, and report each comment in the format [PX] file:line - summary of the issue."
```

### 3. Create Integrated Review

Combine the Codex analysis with your own evaluation and output in the following format:

```markdown
## Review Results

Changes: X files (+XXX/-XXX lines) | CI: Pass/Fail
Overall Rating: X/10

### Summary
Summarize the purpose and changes of the PR in 1-2 sentences.

### Review Status
- [ ] Request Changes (Re-review after fixing P0 items)
- [ ] Approval Pending (Waiting for answers to questions)
- [ ] Approved (LGTM - Ready to merge)

---

## P0: Must Fix Before Merging
### [file:line] Summary of the Issue
Issue: What is the problem?
Fix Proposal: Specific method of correction.

## P1: To Address in Next Cycle
### [file:line] Summary of the Issue
Issue: What is the problem?
Fix Proposal: Improvement suggestions.

## P2: To Fix Eventually
- [file:line] Brief suggestion.

## P3: If Time Permits
- [file:line] Brief suggestion.

---

## Positive Aspects (Optional)
- [file:line] Reason for good implementation.

## Notes (Optional)
- Breaking Changes: None/Yes
- Rollback: Easy/Requires caution
```

### Priority Criteria

| Priority | Description | Example |
|----------|-------------|---------|
| P0       | Must fix before merging | Security vulnerabilities, data loss, critical bugs |
| P1       | To address in next cycle | Performance issues, lack of error handling |
| P2       | To fix eventually | Design improvements, maintainability, documentation |
| P3       | If time permits | Naming improvements, minor refactoring |

### Important Principles

- Validate Codex suggestions rather than accepting them blindly.
- Exclude false positives (AI misdetections).
- Consider project-specific context and constraints.
- Ultimately, you are responsible for the final review content.