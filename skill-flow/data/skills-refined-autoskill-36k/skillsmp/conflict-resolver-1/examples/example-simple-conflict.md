# Example: Simple Merge Conflict Resolution

## Scenario
Two parallel tasks modified the same file with non-overlapping changes.

## Conflict Detected

```bash
$ git merge auto/task-2
Auto-merging src/components/index.ts
CONFLICT (content): Merge conflict in src/components/index.ts
Automatic merge failed; fix conflicts and then commit the result.
```

## Conflict Content

```typescript
// src/components/index.ts
export { Button } from './Button';
export { Card } from './Card';
<<<<<<< HEAD
export { Sidebar } from './Sidebar';  // Added by task-1
=======
export { Header } from './Header';    // Added by task-2
>>>>>>> auto/task-2
```

## Resolution Strategy

**Type: Additive (both additions are valid)**

Both tasks added new exports to the same file. These are non-conflicting
additions that can be combined.

## Automatic Resolution

```typescript
// src/components/index.ts (resolved)
export { Button } from './Button';
export { Card } from './Card';
export { Header } from './Header';    // From task-2
export { Sidebar } from './Sidebar';  // From task-1
```

## Resolution Commands

```bash
# Check the conflict
git diff

# Apply automatic resolution (alphabetical order)
cat > src/components/index.ts << 'EOF'
export { Button } from './Button';
export { Card } from './Card';
export { Header } from './Header';
export { Sidebar } from './Sidebar';
EOF

# Mark as resolved
git add src/components/index.ts

# Complete the merge
git commit -m "chore: merge task-2, resolved index.ts exports"
```

## Output

```
┌─────────────────────────────────────────────────────────────┐
│ Conflict Resolution                                         │
│                                                             │
│   File: src/components/index.ts                             │
│   Type: Additive (non-overlapping)                          │
│   Resolution: Automatic (combined both additions)           │
│                                                             │
│   Merged:                                                   │
│     + export { Header } from './Header';                    │
│     + export { Sidebar } from './Sidebar';                  │
│                                                             │
│   Status: ✅ Resolved automatically                         │
└─────────────────────────────────────────────────────────────┘
```
