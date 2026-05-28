#!/usr/bin/env bash
# extract-import-patterns.sh - Extract import/export patterns from projects

set -euo pipefail

echo "# Import/Export Patterns"
echo ""
echo "Extracted from mature Convex projects on $(date +%Y-%m-%d)"
echo ""

while IFS= read -r project; do
    [[ -z "$project" ]] && continue
    project_name=$(basename "$project")
    
    echo "## $project_name"
    echo ""
    
    # Sample imports from convex functions
    if [[ -d "$project/convex" ]]; then
        echo "### Convex Imports"
        echo '```typescript'
        find "$project/convex" -name "*.ts" -not -name "*.test.ts" 2>/dev/null | \
            head -3 | \
            xargs head -20 2>/dev/null | \
            grep "^import" | \
            sort -u | \
            head -10 || echo "// No imports found"
        echo '```'
        echo ""
    fi
    
    # Sample imports from React components
    react_files=$(find "$project/src" "$project/app" "$project/apps" -name "*.tsx" 2>/dev/null | grep -v node_modules | head -3 || true)
    if [[ -n "$react_files" ]]; then
        echo "### React Imports"
        echo '```typescript'
        echo "$react_files" | \
            xargs head -20 2>/dev/null | \
            grep "^import" | \
            sort -u | \
            head -10 || echo "// No imports found"
        echo '```'
        echo ""
    fi
    
done < <(echo "$1")

echo "## Common Import Patterns"
echo ""
echo "### Convex Functions"
echo '```typescript'
cat <<'EOF'
// Convex core
import { mutation, query, internalMutation } from './_generated/server'
import { v } from 'convex/values'
import { api, internal } from './_generated/api'
import { Id } from './_generated/dataModel'

// Auth
import { auth } from './auth'

// Utilities
import { paginationOptsValidator } from 'convex/server'
EOF
echo '```'
echo ""
echo "### React Components"
echo '```typescript'
cat <<'EOF'
// React
import { useState, useEffect, useCallback } from 'react'

// Convex
import { useQuery, useMutation, useConvexAuth } from 'convex/react'
import { api } from '@/convex/_generated/api'
import { Id } from '@/convex/_generated/dataModel'

// UI Components
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

// Utils
import { cn } from '@/lib/utils'
EOF
echo '```'
echo ""
echo "### Path Aliases"
echo ""
echo "Common tsconfig.json patterns:"
echo '```json'
cat <<'EOF'
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"],
      "@/convex/*": ["./convex/*"],
      "@/components/*": ["./src/components/*"],
      "@/lib/*": ["./src/lib/*"]
    }
  }
}
EOF
echo '```'
echo ""
echo "### Export Patterns"
echo ""
echo "#### Barrel Exports (index.ts)"
echo '```typescript'
cat <<'EOF'
// components/ui/index.ts
export { Button } from './button'
export { Input } from './input'
export { Card } from './card'
EOF
echo '```'
echo ""
echo "#### Named Exports (preferred)"
echo '```typescript'
cat <<'EOF'
export const myFunction = () => { /* ... */ }
export const MyComponent = () => { /* ... */ }
EOF
echo '```'
echo ""
echo "#### Default Exports (Next.js pages only)"
echo '```typescript'
cat <<'EOF'
// app/page.tsx
export default function HomePage() {
  return <div>Home</div>
}
EOF
echo '```'
