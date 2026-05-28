---
name: git-operator
description: Manages Git operations including commits with appropriate conventions, combining related changes logically and following project-specific policies
hooks:
  SessionStart:
    - type: command
      command: |
        if command -v yq &> /dev/null && [ -f ".claude/config.yaml" ]; then
          echo "=== Git Configuration ==="
          yq -o=json '.output.language' .claude/config.yaml 2>/dev/null || true
          yq -o=json '.git' .claude/config.yaml 2>/dev/null || true
        fi
---

# Generic Git Operator

A technology-agnostic skill for managing Git operations according to best practices and project-specific conventions.

## Configuration

This skill reads settings from `.claude/config.yaml`:

```yaml
git:
  operations:
    commit: auto          # auto|user_request_only|prohibited
    push: user_request_only
  commit_message:
    format: conventional  # conventional|simple|custom
```

**Defaults** (when config not set):
- commit: user_request_only
- push: user_request_only
- format: conventional

## Core Responsibilities

### 1. Commit Message Principles

**Focus on Role and Definition, Not Description**

```yaml
Good Examples:
  # Role-focused (what this commit accomplishes)
  - "Add user authentication"
  - "Fix race condition in data loader"
  - "Refactor database connection pooling"
  - "Remove deprecated API endpoints"

Bad Examples:
  # Descriptive (what you did, not what it accomplishes)
  - "Changed login function to use JWT tokens"  # ❌ Too descriptive
  - "Modified the database file to support pooling"  # ❌ Describes changes, not purpose
  - "Updated API routes because they were old"  # ❌ Explains process, not result
```

### 2. Commit Grouping Strategy

**Logical Grouping by Purpose**

```yaml
Grouping Rules:
  same_purpose:
    description: "Changes that accomplish the same goal belong in one commit"
    examples:
      - "Add validation: validator file + tests + integration"
      - "Fix bug: root cause fix + related edge case fixes"
      - "Refactor: extracted functions + updated call sites"

  separate_concerns:
    description: "Different purposes must be in separate commits"
    examples:
      - "feat: Add feature X" + "test: Add tests for feature X" # ❌ Should be one commit
      - "fix: Bug A" + "fix: Unrelated bug B" # ❌ Should be separate
      - "refactor: Module A" + "refactor: Module B" # ❌ Only combine if same refactoring goal

  atomic_commits:
    description: "Each commit should be independently functional"
    rules:
      - "Commit should not break the build"
      - "Tests should pass after the commit"
      - "Commit should be revertable without side effects"
```

**Conventional Commit Format**

```yaml
Format: "<type>: <subject>"

Types:
  feat:
    description: "New feature or capability"
    examples:
      - "feat: Add password reset functionality"
      - "feat: Add CSV export for reports"

  fix:
    description: "Bug fix"
    examples:
      - "fix: Resolve memory leak in cache"
      - "fix: Correct timezone calculation"

  refactor:
    description: "Code restructuring without behavior change"
    examples:
      - "refactor: Extract validation logic"
      - "refactor: Simplify error handling"

  docs:
    description: "Documentation changes only"
    examples:
      - "docs: Update API documentation"
      - "docs: Add architecture decision record"

  test:
    description: "Test additions or modifications only (when not part of feat/fix)"
    examples:
      - "test: Add edge cases for parser"
      - "test: Improve test coverage for auth module"

  chore:
    description: "Maintenance tasks, dependencies, configuration"
    examples:
      - "chore: Update dependencies"
      - "chore: Configure CI pipeline"

  perf:
    description: "Performance improvements"
    examples:
      - "perf: Optimize database queries"
      - "perf: Add caching layer"

  style:
    description: "Code style changes (formatting, whitespace)"
    examples:
      - "style: Apply code formatter"
      - "style: Fix linting errors"
```

### 3. Commit Message Language

**Follow Project Output Language**

```yaml
Language Policy:
  source: "Read from .claude/config.yaml -> output.language"

  examples:
    en:
      - "feat: Add user authentication"
      - "fix: Resolve race condition"
      - "refactor: Extract validation logic"

    ja:
      - "feat: ユーザー認証を追加"
      - "fix: 競合状態を解決"
      - "refactor: バリデーションロジックを抽出"

  guidelines:
    - "Use configured output language consistently"
    - "Keep technical terms in original language when appropriate"
    - "Maintain clarity and brevity regardless of language"
```

### 4. Claude Code Signature Policy

**Conditional Signature Inclusion**

```yaml
Signature Policy:
  source: "Read from .claude/config.yaml -> git.claude_signature"

  when_enabled:
    format: |
      commit message body

      🤖 Generated with [Claude Code](https://claude.com/claude-code)

      Co-Authored-By: Claude <noreply@anthropic.com>

    example: |
      feat: Add user authentication

      Implemented JWT-based authentication with refresh tokens.

      🤖 Generated with [Claude Code](https://claude.com/claude-code)

      Co-Authored-By: Claude <noreply@anthropic.com>

  when_disabled:
    format: |
      commit message body

    example: |
      feat: Add user authentication

      Implemented JWT-based authentication with refresh tokens.

  default: false  # If not specified in config, do not add signature
```

### 5. Git Push Policy

**Conditional Push Permission**

```yaml
Push Policy:
  source: "Read from .claude/config.yaml -> git.allow_push"

  when_allowed:
    - "Execute git push after successful commit"
    - "Confirm push was successful"
    - "Report remote branch status to user"

  when_disallowed:
    - "Do NOT execute git push"
    - "Inform user that commit is local only"
    - "Remind user to push manually if needed"

  default: false  # If not specified in config, do not push
```

### 6. Pre-Commit Workflow

**Standard Commit Process**

```yaml
Commit Workflow:
  step_1_status:
    command: "git status"
    purpose: "Identify all changes (staged, unstaged, untracked)"
    output: "Present to user for confirmation"

  step_2_diff:
    command: "git diff HEAD"
    purpose: "Review actual code changes"
    output: "Analyze for commit message creation"

  step_3_history:
    command: "git log --oneline -10"
    purpose: "Understand project's commit style"
    output: "Match existing conventions"

  step_4_group:
    action: "Group changes by logical purpose"
    rules:
      - "Same goal = one commit"
      - "Different goals = separate commits"
      - "Each commit should be atomic and functional"

  step_5_message:
    action: "Draft commit message(s)"
    rules:
      - "Follow conventional commit format"
      - "Use configured output language"
      - "Focus on role/purpose, not description"
      - "Include Claude signature if enabled in config"

  step_6_stage:
    command: "git add {files}"
    purpose: "Stage files for current commit"
    notes: "May need multiple add commands for grouped commits"

  step_7_commit:
    command: "git commit -m \"$(cat <<'EOF'\\n{message}\\nEOF\\n)\""
    purpose: "Create commit with formatted message"
    notes: "Use HEREDOC for multi-line messages"

  step_8_verify:
    command: "git status"
    purpose: "Confirm commit was created successfully"

  step_9_push:
    condition: "if git.allow_push is true"
    command: "git push"
    purpose: "Push commits to remote repository"
    fallback: "Inform user to push manually"
```

### 7. Configuration Integration

**Required Configuration Structure**

```yaml
# Example .claude/config.yaml structure

output:
  language: en  # or ja, etc.

git:
  claude_signature: false  # true to include Claude Code signature
  allow_push: false  # true to automatically push after commit

  commit_strategy:
    message_format: "conventional"  # conventional, semantic, custom
    examples:
      - "feat: Add new feature X"
      - "fix: Resolve bug in Y"
      - "refactor: Restructure Z"
```

### 8. Commit Quality Checklist

**Pre-Commit Validation**

```yaml
Quality Checklist:
  message:
    - [ ] Follows conventional commit format
    - [ ] Uses correct output language from config
    - [ ] Focuses on role/purpose, not description
    - [ ] Is clear and concise
    - [ ] Includes signature only if enabled in config

  changes:
    - [ ] All related changes are grouped logically
    - [ ] Unrelated changes are in separate commits
    - [ ] Commit is atomic (can be reverted independently)
    - [ ] Tests pass after commit (if applicable)
    - [ ] Build succeeds after commit

  process:
    - [ ] Reviewed git status before committing
    - [ ] Reviewed git diff to understand changes
    - [ ] Checked git log for convention consistency
    - [ ] Staged only files for current commit
    - [ ] Verified commit with git status after
    - [ ] Pushed only if allowed by config
```

## Workflow Examples

### Example 1: Feature Implementation with Tests

```yaml
Scenario: "Implemented user authentication with tests"

Analysis:
  changes:
    - backend/auth.py (new authentication module)
    - backend/tests/test_auth.py (tests for authentication)
    - backend/models/user.py (user model updates)
  purpose: "Add complete authentication feature"
  decision: "Single commit - all changes serve same purpose"

Commit Message (config.output.language: en, git.claude_signature: false):
  |
  feat: Add user authentication

  Implemented JWT-based authentication with refresh tokens and comprehensive test coverage.

Commands:
  - git add backend/auth.py backend/tests/test_auth.py backend/models/user.py
  - git commit -m "$(cat <<'EOF'
    feat: Add user authentication

    Implemented JWT-based authentication with refresh tokens and comprehensive test coverage.
    EOF
    )"
  - git status
  - (No push - git.allow_push: false)
```

### Example 2: Multiple Unrelated Fixes

```yaml
Scenario: "Fixed two unrelated bugs"

Analysis:
  changes:
    - frontend/components/DatePicker.js (timezone bug)
    - backend/services/email.py (SMTP connection bug)
  purpose: "Two different bug fixes"
  decision: "Two separate commits - different concerns"

Commit 1 (config.output.language: ja, git.claude_signature: true):
  |
  fix: DatePickerのタイムゾーン処理を修正

  ユーザーのローカルタイムゾーンを正しく適用するように修正。

  🤖 Generated with [Claude Code](https://claude.com/claude-code)

  Co-Authored-By: Claude <noreply@anthropic.com>

Commit 2:
  |
  fix: SMTP接続のタイムアウト処理を修正

  接続タイムアウト時に適切にリトライするように修正。

  🤖 Generated with [Claude Code](https://claude.com/claude-code)

  Co-Authored-By: Claude <noreply@anthropic.com>

Commands:
  # First commit
  - git add frontend/components/DatePicker.js
  - git commit -m "$(cat <<'EOF'
    fix: DatePickerのタイムゾーン処理を修正

    ユーザーのローカルタイムゾーンを正しく適用するように修正。

    🤖 Generated with [Claude Code](https://claude.com/claude-code)

    Co-Authored-By: Claude <noreply@anthropic.com>
    EOF
    )"

  # Second commit
  - git add backend/services/email.py
  - git commit -m "$(cat <<'EOF'
    fix: SMTP接続のタイムアウト処理を修正

    接続タイムアウト時に適切にリトライするように修正。

    🤖 Generated with [Claude Code](https://claude.com/claude-code)

    Co-Authored-By: Claude <noreply@anthropic.com>
    EOF
    )"

  - git status
  - (No push - git.allow_push: false)
```

### Example 3: Refactoring with Push Enabled

```yaml
Scenario: "Refactored validation logic across multiple files"

Analysis:
  changes:
    - backend/validators/__init__.py (new validator module)
    - backend/validators/email.py (extracted email validation)
    - backend/validators/phone.py (extracted phone validation)
    - backend/services/user.py (updated to use new validators)
    - backend/services/contact.py (updated to use new validators)
  purpose: "Extract and centralize validation logic"
  decision: "Single commit - all changes serve same refactoring goal"

Commit Message (config.output.language: en, git.claude_signature: false, git.allow_push: true):
  |
  refactor: Extract validation logic to dedicated module

  Centralized email and phone validation to improve reusability and maintainability.

Commands:
  - git add backend/validators/ backend/services/user.py backend/services/contact.py
  - git commit -m "$(cat <<'EOF'
    refactor: Extract validation logic to dedicated module

    Centralized email and phone validation to improve reusability and maintainability.
    EOF
    )"
  - git status
  - git push  # Executed because git.allow_push: true
```

## Agent Integration

### Agents That Should Load This Skill

```yaml
Recommended Agents:
  workflow-orchestrator:
    description: "Manages overall development workflow including commits"
    usage: "Loads skill to handle commit operations during workflow"

  code-developer:
    description: "Implements code changes"
    usage: "Loads skill to commit completed implementations"

  quality-reviewer:
    description: "Reviews code quality"
    usage: "Loads skill to commit approved changes after review"

  deliverable-evaluator:
    description: "Evaluates final deliverables"
    usage: "Loads skill to commit validated deliverables"
```

### When to Use This Skill

```yaml
Trigger Conditions:
  user_requests:
    - "commit these changes"
    - "create a commit"
    - "commit with message..."
    - "save these changes to git"

  agent_decisions:
    - "After completing feature implementation"
    - "After fixing bugs"
    - "After refactoring is complete"
    - "After code review approval"
    - "After deliverable validation"

  workflow_events:
    - "End of development cycle"
    - "Before switching branches"
    - "After significant milestone"
```

## Best Practices

1. **Read Configuration First**: Always check `.claude/config.yaml` for `output.language`, `git.claude_signature`, and `git.allow_push` before creating commits
2. **Review Before Commit**: Always run `git status` and `git diff` to understand full scope of changes
3. **Group Logically**: Combine related changes, separate unrelated changes
4. **Atomic Commits**: Each commit should be independently functional and revertable
5. **Clear Messages**: Focus on what the commit accomplishes, not what you did
6. **Verify After Commit**: Always check `git status` after committing to confirm success
7. **Respect Push Policy**: Only push if explicitly allowed by configuration

## Anti-Patterns to Avoid

```yaml
Bad Practices:
  splitting_logical_units:
    example: "Separating implementation and tests for same feature"
    why: "Tests verify the implementation - they belong together"
    correct: "One commit with both implementation and tests"

  combining_unrelated:
    example: "Fixing bug A and bug B in one commit"
    why: "Makes commits harder to revert and understand"
    correct: "Two separate commits, one for each bug"

  descriptive_messages:
    example: "Updated the login function to use new tokens"
    why: "Describes changes, not purpose"
    correct: "Add JWT-based authentication"

  ignoring_config:
    example: "Always including Claude signature"
    why: "Config specifies when to include signature"
    correct: "Check git.claude_signature in config"

  auto_pushing:
    example: "Always running git push after commit"
    why: "Config specifies whether to push"
    correct: "Only push if git.allow_push is true"
```

## Universal Application

This skill applies to any project using Git, regardless of:
- Programming language
- Framework
- Project size
- Team size
- Development methodology

The skill adapts through configuration rather than modification, ensuring consistent Git practices across all projects.
