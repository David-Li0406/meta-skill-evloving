# Configuration Patterns

Common configuration patterns for the Requirements Framework.

## Configuration Locations

The framework uses a three-layer configuration cascade:

```
1. Global (~/.claude/requirements.yaml)
        ↓ (merge if inherit=true)
2. Project (.claude/requirements.yaml) - Version controlled
        ↓ (always merge)
3. Local (.claude/requirements.local.yaml) - Gitignored
```

**Priority**: Local > Project > Global (later files override earlier ones)

---

## Pattern: Project with Multiple Requirements

Full project configuration with all common requirements:

```yaml
# .claude/requirements.yaml
version: "1.0"
inherit: true   # Inherit from global config
enabled: true

requirements:
  commit_plan:
    enabled: true
    scope: session
    checklist:
      - "Plan created via EnterPlanMode"
      - "Atomic commits identified"
      - "TDD approach documented"

  github_ticket:
    enabled: true
    scope: branch
    message: |
      🎫 **Link this branch to a GitHub issue**

      Use: `req satisfy github_ticket --metadata '{"ticket":"#123"}'`

  tests_passing:
    enabled: true
    scope: session
    trigger_tools:
      - Edit
      - Write
    message: |
      ✅ **Run tests before making changes**

      Verify all tests pass: `npm test`

  adr_reviewed:
    enabled: true
    scope: session
    message: |
      📚 **Review relevant Architecture Decision Records**

      Check `docs/adr/` for applicable decisions.
```

---

## Pattern: Personal Override

Disable specific requirements for yourself while team uses them:

```yaml
# .claude/requirements.local.yaml (gitignored)
requirements:
  commit_plan:
    enabled: false   # Disable for myself only

  github_ticket:
    scope: permanent  # Keep across sessions (personal preference)
```

---

## Pattern: Team Default with Opt-Out

```yaml
# Global (~/.claude/requirements.yaml): enabled: false (opt-in default)
# Project (.claude/requirements.yaml): enabled: true (team requires it)
# Local (.claude/requirements.local.yaml): enabled: false (I opt-out temporarily)
```

---

## Pattern: Bash Command Triggers

Block specific Bash commands until requirements are met:

```yaml
requirements:
  pre_commit_review:
    enabled: true
    scope: single_use   # Must satisfy before EACH commit
    trigger_tools:
      - tool: Bash
        command_pattern: "git\\s+commit"
    message: |
      📝 **Pre-commit review required**

      Run `/requirements-framework:pre-commit` before committing.

  pre_deploy_check:
    enabled: true
    scope: single_use
    trigger_tools:
      - tool: Bash
        command_pattern: "npm\\s+publish|yarn\\s+publish|npm\\s+run\\s+deploy"
    message: |
      🚀 **Deployment check required**

      Verify all tests pass and review changes.

  pr_quality:
    enabled: true
    scope: single_use
    trigger_tools:
      - tool: Bash
        command_pattern: "gh\\s+pr\\s+create"
    message: |
      🔍 **PR quality check required**

      Run `/requirements-framework:quality-check` before creating PR.
```

**Regex Pattern Tips**:
- `\\s+` matches whitespace
- `|` for OR patterns
- Case-insensitive matching
- Examples:
  - `git\\s+commit` → matches `git commit -m "msg"`
  - `gh\\s+pr\\s+create` → matches `gh pr create --title "..."`
  - `npm\\s+(publish|deploy)` → matches `npm publish` or `npm deploy`

---

## Pattern: Dynamic Branch Size Limit

Warn when branch changes exceed threshold:

```yaml
requirements:
  branch_size_limit:
    enabled: true
    type: dynamic
    scope: session
    threshold: 400           # Max lines changed
    calculation_cache_ttl: 30  # Cache results (seconds)
    message: |
      📊 **Branch has {size} changes (threshold: {threshold})**

      Consider splitting into smaller, focused branches.
```

---

## Pattern: Protected Branch Guard

Prevent direct edits on protected branches:

```yaml
requirements:
  protected_branch:
    enabled: true
    type: guard
    branches: [main, master, production, release/*]
    message: |
      🚫 **Cannot edit files on protected branch**

      Please create a feature branch:
      ```bash
      git checkout -b feature/your-feature
      ```
```

**Guard vs Blocking**:
- **Blocking**: Requires manual `req satisfy`
- **Guard**: Condition auto-evaluated (no manual satisfy)

---

## Pattern: Checklist Configuration

Add checklists to guide users through requirements:

```yaml
requirements:
  commit_plan:
    enabled: true
    scope: session
    checklist:
      - "Plan created via EnterPlanMode"
      - "Atomic commits identified"
      - "Tests written (TDD approach)"
      - "Relevant ADRs reviewed"
      - "Linting commands known"
```

**Checklist Best Practices**:
1. **Keep items concise** - 5-10 words per item
2. **Make actionable** - Each item verifiable
3. **Order logically** - Steps should flow naturally
4. **Limit quantity** - 5-10 items max
5. **Project-specific** - Customize for team workflows

---

## Pattern: Auto-Satisfaction via Skills

Configure skills to automatically satisfy requirements:

```yaml
requirements:
  pre_commit_review:
    enabled: true
    scope: single_use
    auto_satisfy:
      on_skill_complete:
        - "requirements-framework:pre-commit"
        - "code-reviewer"
```

**Built-in Skill Mappings** (in `auto-satisfy-skills.py`):
- `requirements-framework:pre-commit` → `pre_commit_review`
- `requirements-framework:quality-check` → `pre_pr_review`
- `requirements-framework:codex-review` → `codex_reviewer`

---

## Pattern: Inheritance Control

Control how configurations inherit from parent levels:

```yaml
# Project config that extends global
version: "1.0"
inherit: true    # Merge with global config

requirements:
  # Override global setting
  commit_plan:
    checklist:
      - "Project-specific step 1"
      - "Project-specific step 2"

  # Add project-specific requirement
  frontend_review:
    enabled: true
    scope: session
    trigger_tools: [Edit, Write]
    glob_patterns: ["src/components/**/*.tsx"]
    message: "Frontend component review required"
```

---

## Pattern: Minimal Starter

Simple configuration for getting started:

```yaml
# .claude/requirements.yaml
version: "1.0"
enabled: true

requirements:
  commit_plan:
    enabled: true
    scope: session
    message: |
      📋 **No commit plan found**

      Create a plan using EnterPlanMode before making changes.

      **To satisfy**: `req satisfy commit_plan`
```

---

## Pattern: Strict Team Configuration

Comprehensive configuration for strict team workflows:

```yaml
# .claude/requirements.yaml
version: "1.0"
enabled: true
inherit: false   # Don't inherit global (team controls everything)

hooks:
  stop:
    verify_requirements: true
    verify_scopes: [session]

requirements:
  commit_plan:
    enabled: true
    scope: session
    checklist:
      - "Plan created via EnterPlanMode"
      - "Atomic commits identified"
      - "TDD approach documented"

  adr_reviewed:
    enabled: true
    scope: session
    adr_path: docs/adr/
    message: "Review relevant ADRs before implementation"

  pre_commit_review:
    enabled: true
    scope: single_use
    trigger_tools:
      - tool: Bash
        command_pattern: "git\\s+commit"
    auto_satisfy:
      on_skill_complete: ["requirements-framework:pre-commit"]

  pre_pr_review:
    enabled: true
    scope: single_use
    trigger_tools:
      - tool: Bash
        command_pattern: "gh\\s+pr\\s+create"
    auto_satisfy:
      on_skill_complete: ["requirements-framework:quality-check"]

  branch_size_limit:
    enabled: true
    type: dynamic
    threshold: 400

  protected_branch:
    enabled: true
    type: guard
    branches: [main, master]
```
