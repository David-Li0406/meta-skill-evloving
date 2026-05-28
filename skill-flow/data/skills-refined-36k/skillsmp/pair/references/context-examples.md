# Context Packet Examples

concrete examples of context packets for each mode.

## consult mode

### quick check (copilot)

```json
{
  "mode": "consult",
  "tier": "quick",
  "session": {
    "issue": "ARB-456",
    "phase": "implementation",
    "step": "3/5"
  },
  "question": "Should I use a Convex mutation or action for this?",
  "context": {
    "operation": "calling external API then updating database",
    "current_pattern": "mutations for DB, actions for external"
  }
}
```

**expected output:**
```json
{
  "answer": "Use an action. External API calls need action context for retries and error handling. The action can then call an internal mutation for the DB update.",
  "confidence": 9,
  "reasoning": "External calls require action semantics",
  "escalate": false
}
```

### thorough analysis (codex)

```json
{
  "mode": "consult",
  "tier": "thorough",
  "codebase": {
    "type": "convex + nextjs",
    "structure": "layer . --format=json output"
  },
  "question": "How should I architect real-time notifications?",
  "context": {
    "requirements": "user gets notified when their content is liked",
    "scale": "100k users, 1M likes/day",
    "current_stack": "Convex, Next.js, Clerk"
  }
}
```

**expected output:**
```markdown
## Analysis

### Option A: Direct Convex subscriptions
- User subscribes to their notifications table
- Likes trigger mutation that writes notification
- **Pros:** Simple, real-time, Convex-native
- **Cons:** Scales to ~10k concurrent subscriptions

### Option B: Aggregated polling
- Batch notifications every 30s
- Client polls aggregated count
- **Pros:** Scales better, less connection overhead
- **Cons:** 30s delay, more complex

### Recommendation
Option A for current scale. Add aggregation layer at 50k+ concurrent users.

**Confidence:** 8/10
**Escalate:** No
```

## implement mode

### quick implementation (copilot)

```json
{
  "mode": "implement",
  "tier": "quick",
  "task": "Add loading state to useArtworks hook",
  "context": {
    "file": "packages/web/hooks/useArtworks.ts",
    "current": "returns data directly from useQuery",
    "target": "return { data, isLoading, error }"
  },
  "constraints": {
    "patterns": "follow existing hook patterns in hooks/",
    "avoid": "don't change return type signature for existing consumers"
  }
}
```

### heavy implementation (codex)

```json
{
  "mode": "implement",
  "tier": "thorough",
  "task": "Implement remix history feature",
  "codebase": {
    "structure": "layer output here",
    "relevant_files": [
      "convex/functions/mutations/remix.ts",
      "packages/web/components/remix-panel.tsx"
    ]
  },
  "requirements": {
    "backend": "track parent-child relationships between artworks",
    "frontend": "show remix tree visualization",
    "query": "getRemixHistory(artworkId) returns ancestry"
  },
  "patterns": {
    "mutations": "see ascii.ts for patterns",
    "components": "see artwork-card.tsx for patterns"
  },
  "verification": {
    "commands": ["npx convex codegen", "pnpm test"],
    "success": "all tests pass, remix history shows in UI"
  }
}
```

## review mode

### code work review (copilot)

```json
{
  "mode": "review",
  "tier": "quick",
  "task": "Implemented loading states for hooks",
  "changes": {
    "files": ["useArtworks.ts", "useCollections.ts"],
    "summary": "added isLoading return value to both hooks"
  },
  "tests": {
    "status": "passing",
    "coverage": "no new tests added"
  },
  "questions": [
    "Is the pattern correct?",
    "Should I add tests?"
  ]
}
```

**expected output:**
```json
{
  "pass": true,
  "issues": [
    "Consider adding tests for loading state transition"
  ],
  "confidence": 8,
  "reasoning": "Pattern is correct, tests would be nice-to-have"
}
```

### final PR review (codex)

```json
{
  "mode": "review",
  "tier": "thorough",
  "pr": {
    "title": "Add remix history feature",
    "files_changed": 8,
    "additions": 450,
    "deletions": 23
  },
  "diff_summary": "outline --pr=#123 output here",
  "audit_areas": [
    "correctness",
    "security",
    "performance",
    "test coverage"
  ]
}
```

**expected output:**
```markdown
## PR Review

### Correctness
- [x] Remix relationships stored correctly
- [x] History query returns proper ancestry
- [ ] Edge case: circular references not handled

### Security
- [x] No auth bypass
- [x] User can only see their own remix history

### Performance
- [!] getRemixHistory does N+1 queries for deep trees
- Suggestion: Use recursive CTE or denormalize depth

### Test Coverage
- [x] Happy path covered
- [ ] Missing: edge cases (orphan, circular, deep tree)

**Merge readiness:** 7/10
**Blocking issues:** N+1 query pattern
**Suggestions:** Add depth limit, consider caching
```

## parallel mode

### exploration with both agents

```json
{
  "mode": "explore",
  "tier": "parallel",
  "question": "Best approach for implementing search?",
  "codebase": {
    "type": "convex",
    "current": "no search implementation"
  },
  "explore_options": [
    "Convex full-text search",
    "External search service (Algolia)",
    "Simple LIKE queries"
  ]
}
```

**synthesis pattern:**
- copilot: quick pros/cons of each
- codex: deep implementation analysis
- combine: copilot speed + codex depth
