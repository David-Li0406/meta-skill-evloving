#!/usr/bin/env bash
# extract-convex-schema.sh - Extract Convex schema patterns from projects

set -euo pipefail

echo "# Convex Schema Patterns"
echo ""
echo "Extracted from mature Convex projects on $(date +%Y-%m-%d)"
echo ""

while IFS= read -r project; do
    [[ -z "$project" ]] && continue
    project_name=$(basename "$project")
    
    # Find schema files
    schema_files=$(find "$project" -path "*/convex/schema.ts" 2>/dev/null | grep -v node_modules || true)
    
    if [[ -z "$schema_files" ]]; then
        continue
    fi
    
    echo "## $project_name"
    echo ""
    
    for schema_file in $schema_files; do
        echo "### $(dirname "$schema_file" | sed "s|$project/||")/schema.ts"
        echo '```typescript'
        # Show full schema (usually small)
        cat "$schema_file" | head -100
        echo '```'
        echo ""
    done
    
done < <(echo "$1")

echo "## Common Schema Patterns"
echo ""
echo "### Base Schema Structure"
echo '```typescript'
cat <<'EOF'
import { defineSchema, defineTable } from 'convex/server'
import { v } from 'convex/values'

export default defineSchema({
  users: defineTable({
    name: v.string(),
    email: v.string(),
    clerkId: v.string(),
    createdAt: v.number(),
  })
    .index('by_clerk_id', ['clerkId'])
    .index('by_email', ['email']),
  
  tasks: defineTable({
    text: v.string(),
    userId: v.id('users'),
    completed: v.boolean(),
    createdAt: v.number(),
  })
    .index('by_user', ['userId'])
    .index('by_user_completed', ['userId', 'completed']),
})
EOF
echo '```'
echo ""
echo "### Patterns"
echo "- **Timestamps**: \`v.number()\` for \`createdAt\`, \`updatedAt\`"
echo "- **References**: \`v.id('tableName')\` for foreign keys"
echo "- **Indexes**: by user, by status, compound for common queries"
echo "- **Auth**: \`clerkId\` field with index for Clerk integration"
echo "- **Enums**: \`v.union(v.literal('a'), v.literal('b'))\`"
echo "- **Optional**: \`v.optional(v.string())\` for nullable fields"
echo ""
echo "### Auth Pattern"
echo '```typescript'
cat <<'EOF'
// In schema
users: defineTable({
  clerkId: v.string(),
  // ...
}).index('by_clerk_id', ['clerkId'])

// In function
export const myFunction = mutation({
  args: { /* ... */ },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity()
    if (!identity) throw new Error('Unauthorized')
    
    const user = await ctx.db
      .query('users')
      .withIndex('by_clerk_id', (q) => q.eq('clerkId', identity.subject))
      .unique()
    
    if (!user) throw new Error('User not found')
    // ...
  }
})
EOF
echo '```'
