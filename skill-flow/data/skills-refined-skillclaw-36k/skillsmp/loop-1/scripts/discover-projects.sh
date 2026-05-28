#!/usr/bin/env bash
# discover-projects.sh - Find and score Convex projects for pattern extraction
# Usage: ./discover-projects.sh [base_dir]
# Output: JSON array of projects with maturity scores

set -euo pipefail

BASE_DIR="${1:-$HOME/Developer}"
OUTPUT_FILE="${2:-$HOME/.loop/discovered-projects.json}"

# Ensure output dir exists
mkdir -p "$(dirname "$OUTPUT_FILE")"

echo "🔍 Discovering Convex projects in $BASE_DIR..." >&2

# Find all directories with convex/ subdirectory
projects=()
while IFS= read -r convex_dir; do
    project_root=$(dirname "$convex_dir")
    projects+=("$project_root")
done < <(find "$BASE_DIR" -type d -name "convex" -not -path "*/node_modules/*" -not -path "*/.next/*" 2>/dev/null)

echo "📊 Found ${#projects[@]} Convex projects, scoring maturity..." >&2

# Start JSON array
echo "["

first=true
for project in "${projects[@]}"; do
    # Skip if not a git repo
    [[ ! -d "$project/.git" ]] && continue
    
    project_name=$(basename "$project")
    
    # Calculate maturity score (0-100)
    score=0
    
    # 1. Commit activity (0-30 points)
    commits_3mo=$(git -C "$project" log --since="3 months ago" --oneline 2>/dev/null | wc -l | tr -d ' ')
    commit_score=$((commits_3mo > 100 ? 30 : commits_3mo * 30 / 100))
    score=$((score + commit_score))
    
    # 2. Test coverage (0-30 points)
    test_files=$(find "$project" -name "*.test.ts" -o -name "*.test.tsx" -o -name "*.spec.ts" 2>/dev/null | wc -l | tr -d ' ')
    test_score=$((test_files > 30 ? 30 : test_files))
    score=$((score + test_score))
    
    # 3. Code quality indicators (0-20 points)
    quality_score=0
    [[ -f "$project/turbo.json" ]] && quality_score=$((quality_score + 5))
    [[ -f "$project/.prettierrc" || -f "$project/prettier.config.js" ]] && quality_score=$((quality_score + 3))
    [[ -f "$project/.eslintrc.js" || -f "$project/eslint.config.js" ]] && quality_score=$((quality_score + 3))
    [[ -f "$project/tsconfig.json" ]] && quality_score=$((quality_score + 3))
    [[ -f "$project/vitest.config.ts" ]] && quality_score=$((quality_score + 3))
    [[ -f "$project/playwright.config.ts" ]] && quality_score=$((quality_score + 3))
    score=$((score + quality_score))
    
    # 4. Documentation (0-10 points)
    doc_score=0
    [[ -f "$project/README.md" ]] && doc_score=$((doc_score + 5))
    [[ -f "$project/CONTRIBUTING.md" ]] && doc_score=$((doc_score + 5))
    score=$((score + doc_score))
    
    # 5. Recent activity (0-10 points)
    last_commit=$(git -C "$project" log -1 --format="%ct" 2>/dev/null || echo 0)
    now=$(date +%s)
    days_ago=$(( (now - last_commit) / 86400 ))
    recency_score=$((days_ago < 7 ? 10 : days_ago < 30 ? 5 : days_ago < 90 ? 2 : 0))
    score=$((score + recency_score))
    
    # Get metadata
    total_commits=$(git -C "$project" rev-list --count HEAD 2>/dev/null || echo 0)
    last_commit_date=$(git -C "$project" log -1 --format="%ci" 2>/dev/null || echo "unknown")
    convex_functions=$(find "$project/convex" -name "*.ts" -not -name "*.test.ts" 2>/dev/null | wc -l | tr -d ' ')
    
    # Output JSON object (comma before all but first)
    if [[ "$first" == true ]]; then
        first=false
    else
        echo ","
    fi
    
    cat <<EOF
  {
    "name": "$project_name",
    "path": "$project",
    "score": $score,
    "metadata": {
      "commits_total": $total_commits,
      "commits_3mo": $commits_3mo,
      "test_files": $test_files,
      "convex_functions": $convex_functions,
      "last_commit": "$last_commit_date",
      "days_since_commit": $days_ago,
      "has_turbo": $([ -f "$project/turbo.json" ] && echo true || echo false),
      "has_tests": $([ $test_files -gt 0 ] && echo true || echo false),
      "has_vitest": $([ -f "$project/vitest.config.ts" ] && echo true || echo false),
      "has_playwright": $([ -f "$project/playwright.config.ts" ] && echo true || echo false)
    }
  }
EOF
done

# Close JSON array
echo ""
echo "]"

# Also save to file
{
    echo "["
    first=true
    for project in "${projects[@]}"; do
        [[ ! -d "$project/.git" ]] && continue
        
        project_name=$(basename "$project")
        score=0
        commits_3mo=$(git -C "$project" log --since="3 months ago" --oneline 2>/dev/null | wc -l | tr -d ' ')
        commit_score=$((commits_3mo > 100 ? 30 : commits_3mo * 30 / 100))
        score=$((score + commit_score))
        test_files=$(find "$project" -name "*.test.ts" -o -name "*.test.tsx" -o -name "*.spec.ts" 2>/dev/null | wc -l | tr -d ' ')
        test_score=$((test_files > 30 ? 30 : test_files))
        score=$((score + test_score))
        quality_score=0
        [[ -f "$project/turbo.json" ]] && quality_score=$((quality_score + 5))
        [[ -f "$project/.prettierrc" || -f "$project/prettier.config.js" ]] && quality_score=$((quality_score + 3))
        [[ -f "$project/.eslintrc.js" || -f "$project/eslint.config.js" ]] && quality_score=$((quality_score + 3))
        [[ -f "$project/tsconfig.json" ]] && quality_score=$((quality_score + 3))
        [[ -f "$project/vitest.config.ts" ]] && quality_score=$((quality_score + 3))
        [[ -f "$project/playwright.config.ts" ]] && quality_score=$((quality_score + 3))
        score=$((score + quality_score))
        doc_score=0
        [[ -f "$project/README.md" ]] && doc_score=$((doc_score + 5))
        [[ -f "$project/CONTRIBUTING.md" ]] && doc_score=$((doc_score + 5))
        score=$((score + doc_score))
        last_commit=$(git -C "$project" log -1 --format="%ct" 2>/dev/null || echo 0)
        now=$(date +%s)
        days_ago=$(( (now - last_commit) / 86400 ))
        recency_score=$((days_ago < 7 ? 10 : days_ago < 30 ? 5 : days_ago < 90 ? 2 : 0))
        score=$((score + recency_score))
        total_commits=$(git -C "$project" rev-list --count HEAD 2>/dev/null || echo 0)
        last_commit_date=$(git -C "$project" log -1 --format="%ci" 2>/dev/null || echo "unknown")
        convex_functions=$(find "$project/convex" -name "*.ts" -not -name "*.test.ts" 2>/dev/null | wc -l | tr -d ' ')
        
        if [[ "$first" == true ]]; then
            first=false
        else
            echo ","
        fi
        
        cat <<EOF
  {
    "name": "$project_name",
    "path": "$project",
    "score": $score,
    "metadata": {
      "commits_total": $total_commits,
      "commits_3mo": $commits_3mo,
      "test_files": $test_files,
      "convex_functions": $convex_functions,
      "last_commit": "$last_commit_date",
      "days_since_commit": $days_ago,
      "has_turbo": $([ -f "$project/turbo.json" ] && echo true || echo false),
      "has_tests": $([ $test_files -gt 0 ] && echo true || echo false),
      "has_vitest": $([ -f "$project/vitest.config.ts" ] && echo true || echo false),
      "has_playwright": $([ -f "$project/playwright.config.ts" ] && echo true || echo false)
    }
  }
EOF
    done
    echo ""
    echo "]"
} > "$OUTPUT_FILE"

echo "✅ Discovery complete. Results saved to $OUTPUT_FILE" >&2
echo "📈 Top projects by maturity score:" >&2
cat "$OUTPUT_FILE" | grep -E '"name"|"score"' | paste - - | sort -t: -k2 -nr | head -5 >&2
