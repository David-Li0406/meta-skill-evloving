#!/usr/bin/env bash
# extract-lint-patterns.sh - Extract lint patterns from projects

set -euo pipefail

echo "# Lint Patterns"
echo ""
echo "Extracted from mature Convex projects on $(date +%Y-%m-%d)"
echo ""

while IFS= read -r project; do
    [[ -z "$project" ]] && continue
    project_name=$(basename "$project")
    
    echo "## $project_name"
    echo ""
    
    found_lint=false

    # Check for Biome
    if [[ -f "$project/biome.json" ]]; then
        echo "### Biome Config"
        echo '```json'
        cat "$project/biome.json" | head -n 50
        echo '```'
        echo ""
        found_lint=true
    fi

    # Check for ESLint
    if [[ -f "$project/.eslintrc.js" ]]; then
        echo "### ESLint Config (.eslintrc.js)"
        echo '```javascript'
        cat "$project/.eslintrc.js" | head -n 50
        echo '```'
        echo ""
        found_lint=true
    elif [[ -f "$project/.eslintrc.json" ]]; then
        echo "### ESLint Config (.eslintrc.json)"
        echo '```json'
        cat "$project/.eslintrc.json" | head -n 50
        echo '```'
        echo ""
        found_lint=true
    elif [[ -f "$project/eslint.config.js" ]]; then
        echo "### ESLint Config (eslint.config.js)"
        echo '```javascript'
        cat "$project/eslint.config.js" | head -n 50
        echo '```'
        echo ""
        found_lint=true
    elif [[ -f "$project/.eslintrc" ]]; then
        echo "### ESLint Config (.eslintrc)"
        echo '```json'
        cat "$project/.eslintrc" | head -n 50
        echo '```'
        echo ""
        found_lint=true
    fi
    
    if [[ "$found_lint" == "false" ]]; then
        echo "No lint config found (checked biome.json, .eslintrc.*, eslint.config.js)"
        echo ""
    fi
    
done < <(echo "$1")

echo "## Common Patterns"
echo ""
echo "### Linting Strategy"
echo "- **Biome**: Used in newer/migrated projects for speed."
echo "- **ESLint**: Standard for projects with complex rule requirements."
