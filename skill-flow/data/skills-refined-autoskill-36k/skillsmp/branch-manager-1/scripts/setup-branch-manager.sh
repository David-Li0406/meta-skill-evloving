#!/bin/bash
# Setup script for branch-manager skill
# Configures git hooks, creates templates, and sets up the development environment

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
PLUGIN_DIR="$(dirname "$SKILL_DIR")"

echo "🌿 Setting up Branch Manager Skill"
echo "=================================="

# Check if we're in the right directory structure
validate_environment() {
    if [[ ! -d "$SKILL_DIR/references" ]] || [[ ! -d "$SKILL_DIR/examples" ]]; then
        echo "❌ Error: Script must be run from branch-manager/scripts/ directory"
        echo "   Current location: $SCRIPT_DIR"
        exit 1
    fi

    # Check if claude command is available
    if ! command -v claude &> /dev/null; then
        echo "⚠️  Warning: 'claude' command not found. Make sure Claude Code is installed."
        echo "   You can still use this skill manually by loading the SKILL.md file."
    fi
}

# Create configuration template
create_config_template() {
    local config_file=".claude/branch-manager.md"

    if [[ ! -f "$config_file" ]]; then
        echo "📝 Creating configuration template: $config_file"
        mkdir -p ".claude"

        cat > "$config_file" << 'EOF'
---
# Branch Manager Configuration
# Customize these settings for your team's branching strategy

# Branch naming patterns (supports regex)
patterns:
  feature: "^feature/[A-Z0-9]+-[0-9]+-.+$"
  bugfix: "^bugfix/[A-Z0-9]+-[0-9]+-.+$"
  hotfix: "^hotfix/[^/]+-.+$"
  release: "^release/[^/]+$"
  epic: "^epic/[A-Z0-9]+-[0-9]+-.+$"

# Cleanup policies
cleanup:
  merged_branches_older_than_days: 30
  stale_branches_older_than_days: 90
  keep_branches_with_open_prs: true
  protected_branches: ["main", "master", "develop", "staging", "production"]

# Issue tracking integration
issue_tracking:
  enabled: true
  patterns:
    - "PROJ-[0-9]+"
    - "ISSUE-[0-9]+"
    - "BUG-[0-9]+"
    - "TASK-[0-9]+"
    - "#[0-9]+"
    - "JIRA-[0-9]+"
  auto_detect_from_commits: true
  max_commit_history: 50

# Visualization settings
visualization:
  max_depth: 10
  show_merge_commits: true
  include_remote_branches: false
  show_commit_dates: true
  color_coding: true

# Merge strategy preferences
merge_strategies:
  feature: "rebase_merge"      # rebase then merge (clean history)
  bugfix: "squash_merge"       # squash into single commit
  hotfix: "regular_merge"      # keep full history for traceability
  release: "regular_merge"     # preserve release commit structure
  epic: "regular_merge"        # maintain epic development history

# Advanced settings
advanced:
  enable_branch_creation_hooks: true
  enable_cleanup_suggestions: true
  enable_merge_conflict_prediction: true
  enable_performance_monitoring: false
  log_level: "info"  # debug, info, warn, error

# Custom patterns (extend built-in types)
custom_patterns:
  # Example: spike research branches
  # spike: "^spike/.+$"

# Team-specific overrides
team_overrides:
  # Example: different cleanup policies for different teams
  # frontend:
  #   cleanup:
  #     merged_branches_older_than_days: 14
  # backend:
  #   cleanup:
  #     merged_branches_older_than_days: 45
---
EOF
        echo "✅ Configuration template created"
    else
        echo "ℹ️  Configuration file already exists: $config_file"
    fi
}

# Create pre-commit hook for branch validation
create_precommit_hook() {
    local hook_file=".git/hooks/pre-commit"

    if [[ ! -d ".git" ]]; then
        echo "ℹ️  Not a git repository, skipping git hooks setup"
        return
    fi

    if [[ ! -f "$hook_file" ]]; then
        echo "🔗 Creating pre-commit hook for branch validation"

        cat > "$hook_file" << 'EOF'
#!/bin/bash
# Pre-commit hook for branch name validation
# Ensures commits follow branch naming conventions

BRANCH_NAME=$(git branch --show-current)

# Check if claude command is available
if command -v claude &> /dev/null; then
    echo "🔍 Validating branch name: $BRANCH_NAME"

    # Run branch name validation
    if claude "validate branch name: $BRANCH_NAME" 2>/dev/null | grep -q "❌"; then
        echo "❌ Branch name validation failed"
        echo "   Branch: $BRANCH_NAME"
        echo "   Please rename your branch to follow naming conventions:"
        echo "   feature/PROJ-123-description"
        echo "   bugfix/PROJ-456-description"
        echo "   hotfix/v1.2.3-description"
        echo ""
        echo "   Or run: claude 'suggest new name for branch: $BRANCH_NAME'"
        exit 1
    else
        echo "✅ Branch name is valid"
    fi
else
    echo "⚠️  Claude command not available, skipping branch validation"
fi
EOF

        chmod +x "$hook_file"
        echo "✅ Pre-commit hook created and made executable"
    else
        echo "ℹ️  Pre-commit hook already exists: $hook_file"
    fi
}

# Create post-merge hook for cleanup suggestions
create_postmerge_hook() {
    local hook_file=".git/hooks/post-merge"

    if [[ ! -d ".git" ]]; then
        return
    fi

    if [[ ! -f "$hook_file" ]]; then
        echo "🧹 Creating post-merge hook for cleanup suggestions"

        cat > "$hook_file" << 'EOF'
#!/bin/bash
# Post-merge hook for branch cleanup suggestions
# Runs after successful merges to suggest branch cleanup

# Only run for actual merges (not fast-forwards or pulls)
if [[ $GIT_REFLOG_ACTION == "merge"* ]]; then
    # Check if claude command is available
    if command -v claude &> /dev/null; then
        echo ""
        echo "🧹 Checking for branches that can be cleaned up..."

        # Run cleanup check (non-blocking)
        claude "quick branch cleanup check" || true
    fi
fi
EOF

        chmod +x "$hook_file"
        echo "✅ Post-merge hook created and made executable"
    else
        echo "ℹ️  Post-merge hook already exists: $hook_file"
    fi
}

# Create VS Code workspace settings
create_vscode_settings() {
    local settings_file=".vscode/settings.json"
    local tasks_file=".vscode/tasks.json"

    if [[ ! -f "$settings_file" ]]; then
        echo "💻 Creating VS Code workspace settings"

        mkdir -p ".vscode"

        cat > "$settings_file" << 'EOF'
{
    "git.branchProtection": [
        "main",
        "master",
        "develop",
        "staging",
        "production"
    ],
    "git.branchProtectionPrompt": "This branch is protected. Are you sure you want to commit to it?",
    "git.confirmDeleteUnpublishedBranches": true,
    "git.branchPrefix": "",
    "git.branchRandomName.enable": false
}
EOF
        echo "✅ VS Code settings created"
    fi

    if [[ ! -f "$tasks_file" ]]; then
        echo "🛠️  Creating VS Code tasks for branch management"

        cat > "$tasks_file" << 'EOF'
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Create Feature Branch",
            "type": "shell",
            "command": "claude",
            "args": [
                "create feature branch for",
                "${input:featureDescription}"
            ],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            },
            "problemMatcher": []
        },
        {
            "label": "Create Bugfix Branch",
            "type": "shell",
            "command": "claude",
            "args": [
                "create bugfix branch for",
                "${input:bugDescription}"
            ],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            }
        },
        {
            "label": "Check Branch Health",
            "type": "shell",
            "command": "claude",
            "args": ["check branch health and suggest cleanup"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            }
        },
        {
            "label": "Show Branch Relationships",
            "type": "shell",
            "command": "claude",
            "args": ["show branch relationships"],
            "group": "build",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            }
        },
        {
            "label": "Validate Current Branch",
            "type": "shell",
            "command": "claude",
            "args": ["validate current branch name"],
            "group": "test",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            }
        }
    ],
    "inputs": [
        {
            "id": "featureDescription",
            "description": "Describe the feature you want to implement",
            "default": "new feature",
            "type": "promptString"
        },
        {
            "id": "bugDescription",
            "description": "Describe the bug you want to fix",
            "default": "bug fix",
            "type": "promptString"
        }
    ]
}
EOF
        echo "✅ VS Code tasks created"
    fi
}

# Create example CLAUDE.md with branching guidelines
create_example_claude_md() {
    local claude_file="CLAUDE.md"

    if [[ ! -f "$claude_file" ]]; then
        echo "📚 Creating example CLAUDE.md with branching guidelines"

        cat > "$claude_file" << 'EOF'
# CLAUDE.md - Development Guidelines

This document outlines our development practices, including branching strategy and code quality standards.

## Branching Strategy

### Branch Types

#### Feature Branches
- **Pattern**: `feature/<ISSUE-ID>-<description>`
- **Example**: `feature/PROJ-123-user-authentication`
- **Purpose**: New features and enhancements
- **Lifetime**: Until merged or abandoned
- **Merge Strategy**: Rebase and merge (maintains clean history)

#### Bugfix Branches
- **Pattern**: `bugfix/<ISSUE-ID>-<description>`
- **Example**: `bugfix/PROJ-456-fix-header-layout`
- **Purpose**: Bug fixes and patches
- **Lifetime**: Until merged
- **Merge Strategy**: Squash and merge (single commit)

#### Hotfix Branches
- **Pattern**: `hotfix/<VERSION>-<description>`
- **Example**: `hotfix/v1.2.3-security-patch`
- **Purpose**: Critical production fixes
- **Lifetime**: Until deployed and merged
- **Merge Strategy**: Regular merge (preserves hotfix history)

#### Release Branches
- **Pattern**: `release/<VERSION>`
- **Example**: `release/v2.0.0`
- **Purpose**: Release preparation and stabilization
- **Lifetime**: Until release is complete
- **Merge Strategy**: Regular merge

#### Epic Branches
- **Pattern**: `epic/<EPIC-ID>-<description>`
- **Example**: `epic/EPIC-789-new-dashboard`
- **Purpose**: Large features spanning multiple issues
- **Lifetime**: Until epic is complete
- **Merge Strategy**: Regular merge

### Branch Naming Rules

1. **Always use lowercase** for branch names
2. **Use hyphens as separators** in descriptions
3. **Include issue IDs** when available (PROJ-123, ISSUE-456, etc.)
4. **Keep names descriptive but concise** (max 50 characters)
5. **Use exact patterns** - no variations allowed

### Branch Lifecycle

#### Creation
1. Always create branches from `main` (or `develop` if using Git Flow)
2. Use the branch manager skill: `claude "create feature branch for user auth"`
3. Push branches immediately after creation for backup

#### Development
1. Regular commits with clear messages
2. Keep branches focused on single concerns
3. Rebase frequently to stay current with main
4. Run tests before pushing

#### Merging
1. Create pull request for review
2. Ensure CI passes and reviews are complete
3. Use appropriate merge strategy (see above)
4. Delete branch after successful merge

#### Cleanup
1. Delete merged branches within 30 days
2. Archive abandoned branches after 90 days
3. Use automated cleanup: `claude "cleanup old branches"`

## Code Quality Standards

### Commit Messages
- Use imperative mood: "Add feature" not "Added feature"
- First line < 50 characters
- Reference issue IDs: "Fix login bug (PROJ-123)"
- Separate subject from body with blank line

### Testing
- Unit tests for all new functions
- Integration tests for API changes
- E2E tests for user-facing features
- 80%+ code coverage required

### Code Review
- All changes require review
- Use branch manager for merge strategy advice
- Address all review comments
- No direct pushes to main/develop

## Tools and Automation

### Branch Manager Skill
Use the branch manager skill for:
- Creating properly named branches
- Validating branch naming
- Checking branch health
- Visualizing relationships
- Getting merge strategy advice

### Git Hooks
Pre-commit hooks enforce:
- Branch naming validation
- Code formatting
- Basic linting
- Test execution

### CI/CD Integration
Automated checks for:
- Branch naming compliance
- Code quality metrics
- Test coverage
- Security scanning

## Emergency Procedures

### Hotfix Process
1. Create hotfix branch: `claude "create emergency hotfix"`
2. Implement minimal fix
3. Get security review if needed
4. Deploy directly to production
5. Merge back to main and release branches

### Branch Recovery
If a branch becomes corrupted:
1. Create new branch from last good commit
2. Cherry-pick important commits
3. Delete corrupted branch
4. Update any open pull requests

## Metrics and Monitoring

### Branch Health Metrics
- Average branch lifetime
- Cleanup compliance rate
- Naming convention adherence
- Merge conflict frequency

### Quality Metrics
- Code review turnaround time
- Test coverage trends
- Bug fix time
- Deployment frequency

## References

- [Git Branching Strategies](https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows)
- [Conventional Commits](https://conventionalcommits.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
EOF
        echo "✅ Example CLAUDE.md created"
    else
        echo "ℹ️  CLAUDE.md already exists"
    fi
}

# Test the skill loading
test_skill_loading() {
    echo "🧪 Testing skill loading..."

    if command -v claude &> /dev/null; then
        # Test basic skill loading (non-interactive)
        if claude --help 2>/dev/null | grep -q "load-skill\|skill"; then
            echo "✅ Claude Code supports skill loading"
            echo "   To load this skill: claude --load-skill $SKILL_DIR/SKILL.md"
        else
            echo "⚠️  Claude Code skill loading not detected"
        fi
    else
        echo "ℹ️  Claude command not available - manual loading required"
    fi
}

# Run all setup steps
main() {
    validate_environment
    create_config_template
    create_precommit_hook
    create_postmerge_hook
    create_vscode_settings
    create_example_claude_md
    test_skill_loading

    echo ""
    echo "🎉 Branch Manager Skill setup complete!"
    echo ""
    echo "Next steps:"
    echo "1. Review and customize .claude/branch-manager.md"
    echo "2. Test the skill: claude \"create feature branch for testing\""
    echo "3. Commit your changes to activate git hooks"
    echo "4. Load the skill: claude --load-skill $SKILL_DIR/SKILL.md"
    echo ""
    echo "Documentation available in:"
    echo "  $SKILL_DIR/README.md          # Overview and usage"
    echo "  $SKILL_DIR/references/        # Technical details"
    echo "  $SKILL_DIR/examples/          # Real-world scenarios"
    echo ""
    echo "Happy branching! 🌿"
}

# Run main function
main "$@"

