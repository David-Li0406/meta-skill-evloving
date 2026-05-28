#!/usr/bin/env bash
# extract-file-structure.sh - Extract file structure patterns from projects

set -euo pipefail

echo "# File Structure Patterns"
echo ""
echo "Extracted from mature Convex projects on $(date +%Y-%m-%d)"
echo ""

while IFS= read -r project; do
    [[ -z "$project" ]] && continue
    project_name=$(basename "$project")
    
    echo "## $project_name"
    echo ""
    echo '```'
    
    # Show root structure
    echo "Root:"
    ls -1 "$project" 2>/dev/null | grep -v node_modules | head -20 || true
    
    # Show app/package structure
    if [[ -d "$project/apps" ]]; then
        echo ""
        echo "Apps:"
        ls -1 "$project/apps" 2>/dev/null | head -10 || true
    fi
    
    if [[ -d "$project/packages" ]]; then
        echo ""
        echo "Packages:"
        ls -1 "$project/packages" 2>/dev/null | head -10 || true
    fi
    
    # Show convex structure
    if [[ -d "$project/convex" ]]; then
        echo ""
        echo "Convex:"
        find "$project/convex" -maxdepth 2 -name "*.ts" | sed "s|$project/convex/||" | grep -v node_modules | sort || true
    fi
    
    # Show test structure
    echo ""
    echo "Tests:"
    find "$project" -name "*.test.ts" -o -name "*.test.tsx" | sed "s|$project/||" | grep -v node_modules | head -10 || true
    
    echo '```'
    echo ""
done < <(echo "$1")

echo "## Common Patterns"
echo ""
echo "### Turborepo Structure"
echo '```'
echo "project-root/"
echo "├── apps/"
echo "│   ├── app/          # Next.js app"
echo "│   └── web/          # Alternative main app"
echo "├── packages/"
echo "│   ├── backend/      # Convex functions"
echo "│   ├── ui/           # Shared components"
echo "│   └── tsconfig/"
echo "├── convex/           # Monorepo convex dir"
echo "└── turbo.json"
echo '```'
echo ""
echo "### Standalone Structure"
echo '```'
echo "project-root/"
echo "├── convex/           # Convex functions"
echo "├── src/"
echo "│   ├── components/"
echo "│   ├── lib/"
echo "│   └── app/"
echo "├── __tests__/"
echo "└── e2e/"
echo '```'
