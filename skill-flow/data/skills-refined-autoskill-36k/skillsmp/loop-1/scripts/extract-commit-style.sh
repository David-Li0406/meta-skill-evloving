#!/usr/bin/env bash
# extract-commit-style.sh - Extract commit message patterns from projects

set -euo pipefail

echo "# Commit Style Patterns"
echo ""
echo "Extracted from mature Convex projects on $(date +%Y-%m-%d)"
echo ""

while IFS= read -r project; do
    [[ -z "$project" ]] && continue
    project_name=$(basename "$project")
    
    echo "## $project_name"
    echo ""
    
    # Get recent commits
    commits=$(git -C "$project" log --oneline --no-merges -30 2>/dev/null || echo "")
    
    if [[ -z "$commits" ]]; then
        echo "No commits found"
        echo ""
        continue
    fi
    
    echo "### Recent Commits"
    echo '```'
    echo "$commits" | head -10
    echo '```'
    echo ""
    
done < <(echo "$1")

# Analyze patterns across all projects
echo "## Style Analysis"
echo ""

all_commits=""
while IFS= read -r project; do
    [[ -z "$project" ]] && continue
    commits=$(git -C "$project" log --format="%s" --no-merges -100 2>/dev/null || echo "")
    all_commits="$all_commits"$'\n'"$commits"
done < <(echo "$1")

# Count conventional commit prefixes
echo "### Common Prefixes"
echo '```'
echo "$all_commits" | grep -oE "^[a-z]+:" | sort | uniq -c | sort -rn | head -15 || echo "Mixed styles"
echo '```'
echo ""

echo "### Common Patterns"
echo ""
echo "Based on analysis of actual commits:"
echo ""
echo "#### Conventional Commits Style"
echo '```'
echo "add: new feature or component"
echo "update: enhance existing feature"
echo "fix: bug fix"
echo "refactor: code restructuring"
echo "test: add or update tests"
echo "docs: documentation changes"
echo "chore: maintenance tasks"
echo "perf: performance improvement"
echo "style: formatting, no logic change"
echo '```'
echo ""
echo "#### Lowercase Style (Your preference per AGENTS.md)"
echo '```'
echo "add task creation flow"
echo "update auth to use clerk"
echo "fix race condition in query"
echo "refactor schema for new pattern"
echo "test task mutations"
echo '```'
echo ""
echo "#### Guidelines"
echo "- **Imperative mood**: 'add', not 'added' or 'adds'"
echo "- **Lowercase**: except acronyms (API, UI, TDD)"
echo "- **Concise**: focus on 'why', not 'what'"
echo "- **Specific**: mention file/feature if helpful"
echo "- **No periods**: at end of subject line"
echo ""
echo "#### Examples"
echo '```'
cat <<'EOF'
Good:
  add clerk auth provider
  update schema to include user roles
  fix infinite loop in task query
  refactor auth helpers into lib/
  test task creation with mock user

Avoid:
  Added new feature
  Updated files
  Fixed bug
  Changes
  WIP
EOF
echo '```'
