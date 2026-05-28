# Branch Manager Implementation Guide

This guide provides detailed implementation strategies for the branch-manager skill, covering the core algorithms and git operations needed.

## Core Components Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Branch        │    │   Naming        │    │   Cleanup       │
│   Creator       │    │   Validator     │    │   Analyzer      │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └─────────┬────────────┘                      │
                    │                                   │
          ┌─────────▼────────────┐    ┌─────────────────▼────────────┐
          │   Relationship       │    │   Merge Strategy            │
          │   Visualizer         │    │   Advisor                   │
          └──────────────────────┘    └─────────────────────────────┘
```

## 1. Branch Creation Algorithm

### Issue ID Detection

```bash
# Extract issue IDs from various sources
detect_issue_ids() {
    # From commit messages (last 10 commits)
    git log --oneline -10 | grep -oE '(PROJ|ISSUE|EPIC)-[0-9]+' | sort | uniq

    # From current branch description (if available)
    # From PR descriptions, task descriptions, etc.
}

# Classify branch type based on task description
classify_branch_type() {
    local description="$1"

    if echo "$description" | grep -qi "fix\|bug\|issue"; then
        echo "bugfix"
    elif echo "$description" | grep -qi "hotfix\|critical\|emergency"; then
        echo "hotfix"
    elif echo "$description" | grep -qi "release\|version\|tag"; then
        echo "release"
    elif echo "$description" | grep -qi "refactor\|restructure\|reorganize\|cleanup"; then
        echo "refactor"
    elif echo "$description" | grep -qi "epic\|story\|feature.*set"; then
        echo "epic"
    else
        echo "feature"
    fi
}

# Generate branch name
generate_branch_name() {
    local type="$1"
    local issue_id="$2"
    local description="$3"

    # Clean description: lowercase, hyphens, remove special chars
    local clean_desc=$(echo "$description" | \
        tr '[:upper:]' '[:lower:]' | \
        sed 's/[^a-z0-9]/-/g' | \
        sed 's/-\+/-/g' | \
        sed 's/^-//;s/-$//')

    case "$type" in
        "feature")
            if [[ -n "$issue_id" ]]; then
                echo "feature/${issue_id}-${clean_desc}"
            else
                echo "feature/${clean_desc}"
            fi
            ;;
        "bugfix")
            if [[ -n "$issue_id" ]]; then
                echo "bugfix/${issue_id}-${clean_desc}"
            else
                echo "bugfix/${clean_desc}"
            fi
            ;;
        "hotfix")
            # For hotfix, use version from package.json or git tag
            local version=$(get_current_version)
            echo "hotfix/${version}-${clean_desc}"
            ;;
        "release")
            local version=$(get_next_version)
            echo "release/${version}"
            ;;
        "epic")
            if [[ -n "$issue_id" ]]; then
                echo "epic/${issue_id}-${clean_desc}"
            else
                echo "epic/${clean_desc}"
            fi
            ;;
        "refactor")
            if [[ -n "$issue_id" ]]; then
                echo "refactor/${issue_id}-${clean_desc}"
            else
                echo "refactor/${clean_desc}"
            fi
            ;;
    esac
}
```

### Branch Creation with Validation

```bash
create_validated_branch() {
    local task_description="$1"

    # Step 1: Analyze task description
    local branch_type=$(classify_branch_type "$task_description")
    local issue_ids=$(detect_issue_ids)
    local primary_issue=$(echo "$issue_ids" | head -1)

    # Step 2: Generate branch name
    local branch_name=$(generate_branch_name "$branch_type" "$primary_issue" "$task_description")

    # Step 3: Validate branch name
    if ! validate_branch_name "$branch_name"; then
        echo "❌ Generated branch name doesn't follow conventions: $branch_name"
        return 1
    fi

    # Step 4: Check if branch exists
    if git show-ref --verify --quiet "refs/heads/$branch_name"; then
        echo "⚠️  Branch already exists: $branch_name"
        echo "   Switching to existing branch..."
        git checkout "$branch_name"
        return 0
    fi

    # Step 5: Create and switch to branch
    echo "📝 Creating branch: $branch_name"
    git checkout -b "$branch_name"

    # Step 6: Show branch status
    echo "✅ Switched to new branch: $branch_name"
    echo "🔄 Branch follows naming conventions"
    echo "📋 Ready to implement: $task_description"

    # Optional: Set upstream if remote exists
    if git remote | grep -q origin; then
        git push -u origin "$branch_name" 2>/dev/null || true
    fi
}
```

## 2. Naming Convention Validation

### Pattern Definitions

```bash
# Branch naming patterns (configurable)
declare -A BRANCH_PATTERNS=(
    ["feature"]="^feature/[A-Z0-9]+-[0-9]+-.+$"
    ["bugfix"]="^bugfix/[A-Z0-9]+-[0-9]+-.+$"
    ["hotfix"]="^hotfix/[^/]+-.+$"
    ["release"]="^release/[^/]+$"
    ["epic"]="^epic/[A-Z0-9]+-[0-9]+-.+$"
)

validate_branch_name() {
    local branch_name="$1"

    # Extract type from branch name
    local branch_type=$(echo "$branch_name" | cut -d'/' -f1)

    # Check if type is recognized
    if [[ ! -v BRANCH_PATTERNS[$branch_type] ]]; then
        echo "❌ Unknown branch type: $branch_type"
        echo "   Supported types: feature, bugfix, hotfix, release, epic"
        return 1
    fi

    # Validate against pattern
    local pattern="${BRANCH_PATTERNS[$branch_type]}"
    if ! echo "$branch_name" | grep -qE "$pattern"; then
        echo "❌ Branch name doesn't match pattern: $branch_name"
        echo "   Expected: $branch_type/<ISSUE-ID>-<description>"
        echo "   Example: $branch_type/PROJ-123-user-authentication"
        return 1
    fi

    echo "✅ Branch name follows conventions: $branch_name"
    return 0
}

audit_branch_naming() {
    echo "## Branch Naming Audit"
    echo

    local total_branches=0
    local valid_branches=0
    local invalid_branches=()

    # Analyze all branches
    while IFS= read -r branch; do
        ((total_branches++))
        branch=$(echo "$branch" | sed 's/^[ *]*//') # Remove leading spaces/asterisks

        if validate_branch_name "$branch" >/dev/null 2>&1; then
            ((valid_branches++))
        else
            invalid_branches+=("$branch")
        fi
    done < <(git branch --format='%(refname:short)')

    # Report results
    echo "### Summary"
    echo "- Total branches: $total_branches"
    echo "- Valid branches: $valid_branches"
    echo "- Invalid branches: $((total_branches - valid_branches))"
    echo

    if [[ ${#invalid_branches[@]} -gt 0 ]]; then
        echo "### Branches Needing Rename"
        for branch in "${invalid_branches[@]}"; do
            echo "- \`$branch\` - $(get_rename_suggestion "$branch")"
        done
        echo
    fi

    local compliance_rate=$((valid_branches * 100 / total_branches))
    echo "### Compliance Rate: ${compliance_rate}%"

    if [[ $compliance_rate -lt 80 ]]; then
        echo "⚠️  Low compliance rate. Consider enforcing naming conventions."
    fi
}
```

## 3. Branch Cleanup Analysis

### Cleanup Detection Algorithm

````bash
analyze_branch_cleanup() {
    echo "## Branch Cleanup Analysis"
    echo

    local current_date=$(date +%s)
    local merged_cutoff=$((30 * 24 * 60 * 60))  # 30 days
    local stale_cutoff=$((90 * 24 * 60 * 60))   # 90 days

    local cleanup_candidates=()
    local total_savings=0

    # Analyze each branch
    while IFS= read -r line; do
        local branch=$(echo "$line" | awk '{print $1}')
        local commit_hash=$(echo "$line" | awk '{print $2}')
        local message=$(echo "$line" | cut -d' ' -f3-)

        # Skip current branch and protected branches
        if [[ "$branch" == *"*"* ]] || is_protected_branch "$branch"; then
            continue
        fi

        # Check if branch is merged
        if git merge-base --is-ancestor "$commit_hash" HEAD 2>/dev/null; then
            local merge_date=$(get_commit_date "$commit_hash")
            local days_since_merge=$(( (current_date - merge_date) / (24 * 60 * 60) ))

            if [[ $days_since_merge -gt 30 ]]; then
                cleanup_candidates+=("$branch|$days_since_merge|merged")
                ((total_savings++))
            fi
        else
            # Check if branch is stale (no commits in 90 days)
            local last_commit_date=$(get_commit_date "$commit_hash")
            local days_since_commit=$(( (current_date - last_commit_date) / (24 * 60 * 60) ))

            if [[ $days_since_commit -gt 90 ]]; then
                cleanup_candidates+=("$branch|$days_since_commit|stale")
                ((total_savings++))
            fi
        fi
    done < <(git branch -v | grep -v '^\*')

    # Report findings
    echo "### Cleanup Candidates: ${#cleanup_candidates[@]} branches"
    echo

    if [[ ${#cleanup_candidates[@]} -gt 0 ]]; then
        echo "| Branch | Days Old | Status | Action |"
        echo "|--------|----------|--------|--------|"

        for candidate in "${cleanup_candidates[@]}"; do
            IFS='|' read -r branch days status <<< "$candidate"
            echo "| \`$branch\` | $days | $status | \`git branch -D $branch\` |"
        done

        echo
        echo "### Automated Cleanup Script"
        echo '```bash'
        echo "# Safe cleanup (will fail if unmerged)"
        for candidate in "${cleanup_candidates[@]}"; do
            IFS='|' read -r branch days status <<< "$candidate"
            if [[ "$status" == "merged" ]]; then
                echo "git branch -d \"$branch\"  # Merged $days days ago"
            else
                echo "# git branch -D \"$branch\"  # Stale $days days ago (force delete)"
            fi
        done
        echo '```'
    else
        echo "✅ No branches need cleanup at this time."
    fi
}

get_commit_date() {
    local commit_hash="$1"
    git show -s --format=%ct "$commit_hash" 2>/dev/null || echo "0"
}

is_protected_branch() {
    local branch="$1"
    local protected=("main" "master" "develop" "staging" "production")

    for protected_branch in "${protected[@]}"; do
        if [[ "$branch" == "$protected_branch" ]]; then
            return 0
        fi
    done
    return 1
}
````

## 4. Branch Relationship Visualization

### ASCII Tree Generation

````bash
generate_branch_tree() {
    echo "## Branch Relationship Tree"
    echo
    echo '```ascii'
    echo "main (v$(get_current_version))"
    generate_tree_recursive "main" "" 0
    echo '```'
    echo
    echo "**Legend**: \`[merged]\` = safe to delete, \`[active]\` = in development"
}

generate_tree_recursive() {
    local branch="$1"
    local prefix="$2"
    local depth="$3"

    # Prevent infinite recursion
    if [[ $depth -gt 10 ]]; then
        echo "${prefix}└── ... (max depth reached)"
        return
    fi

    # Get child branches (branches that have this as ancestor but not main)
    local children=()
    while IFS= read -r child_branch; do
        if [[ "$child_branch" != "$branch" ]] && \
           git merge-base --is-ancestor "$branch" "$child_branch" 2>/dev/null && \
           ! git merge-base --is-ancestor "$child_branch" "$branch" 2>/dev/null; then
            children+=("$child_branch")
        fi
    done < <(git branch --format='%(refname:short)' | grep -v '^main$')

    # Sort children by creation date (newest first)
    children=($(printf '%s\n' "${children[@]}" | \
        xargs -I {} git show-ref --heads {} | \
        sort -k3nr | cut -d' ' -f2 | xargs basename))

    # Display children
    local child_count=${#children[@]}
    for i in "${!children[@]}"; do
        local child="${children[$i]}"
        local is_last=$([[ $i -eq $((child_count - 1)) ]] && echo true || echo false)
        local new_prefix="$prefix"

        if [[ "$is_last" == "true" ]]; then
            new_prefix="${prefix}└── "
            prefix="${prefix}    "
        else
            new_prefix="${prefix}├── "
            prefix="${prefix}│   "
        fi

        # Check branch status
        local status=""
        if git merge-base --is-ancestor "$child" HEAD 2>/dev/null; then
            status=" [merged]"
        elif [[ "$child" == "$(git branch --show-current)" ]]; then
            status=" [current]"
        else
            status=" [active]"
        fi

        echo "${new_prefix}${child}${status}"

        # Recurse for children of this child
        if [[ "$is_last" == "true" ]]; then
            generate_tree_recursive "$child" "${prefix}" $((depth + 1))
        else
            generate_tree_recursive "$child" "${prefix}" $((depth + 1))
        fi
    done
}
````

## 5. Merge Strategy Recommendation

### Conflict Analysis

````bash
analyze_merge_strategy() {
    local source_branch="$1"
    local target_branch="${2:-main}"

    echo "## Merge Strategy Analysis"
    echo
    echo "**Source**: \`$source_branch\` → **Target**: \`$target_branch\`"
    echo

    # Gather branch statistics
    local commit_count=$(git rev-list --count "$target_branch..$source_branch")
    local file_count=$(git diff --name-only "$target_branch..$source_branch" | wc -l)
    local conflict_files=$(detect_potential_conflicts "$source_branch" "$target_branch")

    echo "### Branch Statistics"
    echo "- Commits: $commit_count"
    echo "- Files changed: $file_count"
    echo "- Potential conflicts: ${#conflict_files[@]}"
    echo

    # Analyze based on characteristics
    if [[ $commit_count -eq 1 ]] && [[ $file_count -lt 5 ]]; then
        recommend_squash_merge "$source_branch" "$target_branch"
    elif [[ ${#conflict_files[@]} -eq 0 ]] && [[ $commit_count -lt 10 ]]; then
        recommend_rebase_merge "$source_branch" "$target_branch"
    elif [[ ${#conflict_files[@]} -gt 0 ]]; then
        recommend_manual_merge "$source_branch" "$target_branch" "${conflict_files[@]}"
    else
        recommend_regular_merge "$source_branch" "$target_branch"
    fi
}

detect_potential_conflicts() {
    local source="$1"
    local target="$2"
    local conflicts=()

    # Find files changed in both branches
    while IFS= read -r file; do
        if git show "$target:$file" >/dev/null 2>&1 && \
           git show "$source:$file" >/dev/null 2>&1; then

            # Check if both branches modified the file
            if ! git diff "$target..$source" -- "$file" | grep -q "^diff --git"; then
                conflicts+=("$file")
            fi
        fi
    done < <(git diff --name-only "$target..$source")

    echo "${conflicts[@]}"
}

recommend_rebase_merge() {
    local source="$1"
    local target="$2"

    echo "### Recommended: 🔄 Rebase and Merge"
    echo "**Why**: Clean linear history, no merge commits, good for feature branches"
    echo
    echo "**Commands**:"
    echo '```bash'
    echo "git checkout $source"
    echo "git rebase $target"
    echo "git checkout $target"
    echo "git merge $source  # Fast-forward merge"
    echo '```'
    echo
    echo "**Pros**: Linear history, clean commits"
    echo "**Cons**: Rewrites history (avoid on shared branches)"
}

recommend_squash_merge() {
    local source="$1"
    local target="$2"

    echo "### Recommended: 📋 Squash and Merge"
    echo "**Why**: Single commit on target, good for small features/bugfixes"
    echo
    echo "**Commands**:"
    echo '```bash'
    echo "git checkout $target"
    echo "git merge --squash $source"
    echo "git commit -m \"$(get_squash_message "$source")\""
    echo '```'
    echo
    echo "**Pros**: Clean target history, single commit"
    echo "**Cons**: Loses individual commit history"
}

recommend_manual_merge() {
    local source="$1"
    local target="$2"
    shift 2
    local conflicts=("$@")

    echo "### Recommended: 🔀 Manual Merge (with conflict resolution)"
    echo "**Why**: Conflicts detected, requires manual resolution"
    echo
    echo "**Conflicting files**:"
    for file in "${conflicts[@]}"; do
        echo "- \`$file\`"
    done
    echo
    echo "**Commands**:"
    echo '```bash'
    echo "git checkout $target"
    echo "git merge $source"
    echo "# Resolve conflicts in: ${conflicts[*]}"
    echo "git add <resolved-files>"
    echo "git commit"
    echo '```'
}
````

## Configuration Management

### Default Configuration

```bash
create_default_config() {
    local config_file=".claude/branch-manager.md"

    if [[ ! -f "$config_file" ]]; then
        cat > "$config_file" << 'EOF'
---
# Branch Manager Configuration

patterns:
  feature: "^feature/[A-Z]+-[0-9]+-.+$"
  bugfix: "^bugfix/[A-Z]+-[0-9]+-.+$"
  hotfix: "^hotfix/[^/]+-.+$"
  release: "^release/[^/]+$"
  epic: "^epic/[A-Z]+-[0-9]+-.+$"

cleanup:
  merged_branches_older_than_days: 30
  stale_branches_older_than_days: 90
  keep_branches_with_open_prs: true
  protected_branches: ["main", "master", "develop", "staging"]

issue_tracking:
  enabled: true
  patterns: ["PROJ-[0-9]+", "ISSUE-[0-9]+", "#[0-9]+"]
  auto_detect_from_commits: true

visualization:
  max_depth: 10
  show_merge_commits: true
  include_remote_branches: false

merge_strategies:
  feature: "rebase_merge"
  bugfix: "squash_merge"
  hotfix: "regular_merge"
  release: "regular_merge"
---
EOF
    fi
}
```

## Error Handling and Validation

### Git Repository Validation

````bash
validate_git_repo() {
    if ! git rev-parse --git-dir >/dev/null 2>&1; then
        echo "❌ Error: Not in a git repository"
        exit 1
    fi

    if ! git rev-parse HEAD >/dev/null 2>&1; then
        echo "❌ Error: Repository has no commits"
        exit 1
    fi
}

### Safe Git Operations
```bash
safe_git_operation() {
    local command="$1"
    local error_msg="${2:-Git operation failed}"

    if ! eval "$command" 2>/dev/null; then
        echo "❌ $error_msg"
        echo "   Command: $command"
        return 1
    fi
}
````

This implementation guide provides the core algorithms and git operations needed to build a comprehensive branch management system. The modular design allows for easy extension and customization based on team requirements.
