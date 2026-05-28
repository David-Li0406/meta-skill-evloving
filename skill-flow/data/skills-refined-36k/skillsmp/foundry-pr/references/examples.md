# Examples

## Example 1: Feature Addition

```bash
# Skill invoked after spec completion
Skill(foundry:foundry-pr) "Create PR for oauth-feature-2025-11-03-001"

# Agent analyzes context and shows draft
# User reviews and approves
# PR created automatically
```

**Generated PR**: Comprehensive description with OAuth implementation details, security considerations, and testing approach.

## Example 2: Bug Fix

```bash
# Skill invoked for bug fix spec
Skill(foundry:foundry-pr) "Create PR for memory-leak-fix-2025-11-03-002"

# Agent analyzes and shows draft
# PR explains root cause, fix approach, and verification
```

**Generated PR**: Detailed bug analysis with root cause from journal entries, fix implementation, and memory usage improvements.

## Example 3: Manual Invocation

```bash
# Invoke skill directly with prompt
Skill(foundry:foundry-pr) "Create PR for spec refactor-api-2025-11-03-003"

# Agent gathers context, analyzes, and shows draft
# Review and approve
# PR created
```
