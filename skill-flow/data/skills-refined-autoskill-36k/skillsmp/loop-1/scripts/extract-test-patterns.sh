#!/usr/bin/env bash
# extract-test-patterns.sh - Extract test patterns from projects

set -euo pipefail

echo "# Test Patterns"
echo ""
echo "Extracted from mature Convex projects on $(date +%Y-%m-%d)"
echo ""

while IFS= read -r project; do
    [[ -z "$project" ]] && continue
    project_name=$(basename "$project")
    
    echo "## $project_name"
    echo ""
    
    # Find test files
    test_files=$(find "$project" -name "*.test.ts" -o -name "*.test.tsx" 2>/dev/null | grep -v node_modules | head -5 || true)
    
    if [[ -z "$test_files" ]]; then
        echo "No test files found"
        echo ""
        continue
    fi
    
    # Show test locations
    echo "### Test Locations"
    echo '```'
    echo "$test_files" | sed "s|$project/||"
    echo '```'
    echo ""
    
    # Extract test patterns from first test file
    first_test=$(echo "$test_files" | head -1)
    if [[ -f "$first_test" ]]; then
        echo "### Example Test Structure"
        echo '```typescript'
        # Show imports and first test
        head -30 "$first_test" | grep -v "^//" | grep -v "^$" || echo "// content filtered"
        echo '```'
        echo ""
    fi
    
done < <(echo "$1")

echo "## Common Test Patterns"
echo ""
echo "### Convex Function Tests"
echo '```typescript'
cat <<'EOF'
import { convexTest } from 'convex-test'
import { describe, it, expect } from 'vitest'
import { api } from './_generated/api'
import schema from './schema'

describe('tasks', () => {
  it('creates task for authenticated user', async () => {
    const t = convexTest(schema)
    const asUser = t.withIdentity({ name: 'Luke', subject: 'user_123' })
    
    await asUser.mutation(api.tasks.create, { text: 'Test task' })
    
    const tasks = await asUser.query(api.tasks.list)
    expect(tasks).toHaveLength(1)
    expect(tasks[0].text).toBe('Test task')
  })
  
  it('rejects unauthenticated user', async () => {
    const t = convexTest(schema)
    
    await expect(
      t.mutation(api.tasks.create, { text: 'Test' })
    ).rejects.toThrow('Unauthorized')
  })
})
EOF
echo '```'
echo ""
echo "### React Component Tests"
echo '```typescript'
cat <<'EOF'
import { render, screen, waitFor } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import { ConvexProvider } from 'convex/react'
import { TaskList } from './TaskList'

describe('TaskList', () => {
  it('renders tasks', async () => {
    render(
      <ConvexProvider client={mockConvexClient}>
        <TaskList />
      </ConvexProvider>
    )
    
    await waitFor(() => {
      expect(screen.getByText('Test task')).toBeInTheDocument()
    })
  })
})
EOF
echo '```'
echo ""
echo "### Naming Conventions"
echo "- Files: \`*.test.ts\` or \`*.test.tsx\`"
echo "- Location: co-located with source or in \`__tests__/\` dir"
echo "- Describe blocks: function/component name"
echo "- Test names: behavior-driven (what it should do)"
