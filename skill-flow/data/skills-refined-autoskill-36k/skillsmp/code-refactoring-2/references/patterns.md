# Refactoring Patterns

## Pattern 1: Rename & Move

### File Rename
```bash
# 1. Find all imports
grep -r "from.*oldName" --include="*.ts" --include="*.tsx"

# 2. Rename file
git mv src/oldName.ts src/newName.ts

# 3. Update all imports
# Use Edit tool with replace_all=true
```

### Directory Move
```bash
# 1. Find all imports from directory
grep -r "from.*oldDir/" --include="*.ts"

# 2. Move directory
git mv src/oldDir src/newDir

# 3. Update import paths
# Update tsconfig paths if aliased
```

## Pattern 2: Extract Component

**Before:** Monolithic component with multiple responsibilities

```tsx
// BigComponent.tsx (500 lines)
const BigComponent = () => {
  // State for feature A
  // State for feature B
  // Logic for A
  // Logic for B
  return (
    <div>
      {/* Feature A UI */}
      {/* Feature B UI */}
    </div>
  );
};
```

**After:** Split into focused components

```tsx
// FeatureA.tsx
export const FeatureA = () => { ... };

// FeatureB.tsx
export const FeatureB = () => { ... };

// BigComponent.tsx (now just composition)
const BigComponent = () => (
  <div>
    <FeatureA />
    <FeatureB />
  </div>
);
```

**Changelog:**
```markdown
### [COMPONENT] Extract FeatureA and FeatureB from BigComponent

**Before:** Single 500-line component
**After:** 3 focused components (<150 lines each)
**Impact:** Files: 3 | Breaking: No
```

## Pattern 3: Database Schema Migration

### Add Column
```sql
-- Migration: add_status_to_orders.sql
ALTER TABLE orders ADD COLUMN status TEXT DEFAULT 'pending';

-- Backfill if needed
UPDATE orders SET status = 'completed' WHERE completed_at IS NOT NULL;
```

### Rename Table
```sql
-- Migration: rename_quotas_to_token_pools.sql

-- 1. Create new table
CREATE TABLE token_pools (LIKE ai_plan_quotas INCLUDING ALL);

-- 2. Copy data
INSERT INTO token_pools SELECT * FROM ai_plan_quotas;

-- 3. Update foreign keys (if any)
-- 4. Drop old table
DROP TABLE ai_plan_quotas;
```

**Changelog:**
```markdown
### [SCHEMA] Rename ai_plan_quotas → token_pools

**Before:** `ai_plan_quotas` table
**After:** `token_pools` table with same structure
**Impact:** Files: 8 | Migration: Yes | Breaking: Yes
**Related:** #20260108_rename_quotas
```

## Pattern 4: API Signature Change

### RPC Parameter Change
```sql
-- Old signature
CREATE FUNCTION check_quota(p_user_id UUID, p_feature TEXT)

-- New signature
CREATE FUNCTION check_token_balance(
  p_user_id UUID DEFAULT auth.uid()
) RETURNS TABLE(available INT, expires_at TIMESTAMPTZ)
```

**Changelog:**
```markdown
### [API] Replace check_quota with check_token_balance

**Before:**
- `check_quota(user_id, feature)` → boolean

**After:**
- `check_token_balance(user_id?)` → {available, expires_at}

**Impact:** Files: 5 | Breaking: Yes (signature changed)
```

## Pattern 5: Hook Consolidation

**Before:** Multiple similar hooks

```tsx
const useAISearchQuota = () => { ... };
const useAIStudyQuota = () => { ... };
const useAITranslationQuota = () => { ... };
```

**After:** Single parameterized hook

```tsx
const useTokenBalance = () => {
  // Single source of truth for all token operations
  return { balance, deduct, canAfford };
};
```

**Changelog:**
```markdown
### [COMPONENT] Consolidate quota hooks into useTokenBalance

**Before:** 3 separate hooks (useAISearchQuota, useAIStudyQuota, useAITranslationQuota)
**After:** Single useTokenBalance hook
**Impact:** Files: 12 | Breaking: Yes (hook names changed)
```

## Pattern 6: Config Centralization

**Before:** Scattered constants

```tsx
// File A
const AI_TIMEOUT = 30000;

// File B
const aiTimeout = 30000;

// File C
const timeout = 30 * 1000;
```

**After:** Centralized config

```tsx
// config.ts
export const AI_CONFIG = {
  timeout: 30000,
  maxRetries: 3,
  models: { ... }
};

// All files import from config
import { AI_CONFIG } from '@/lib/config';
```

## Refactoring Safety Checklist

Before refactoring:
- [ ] Tests pass
- [ ] Identify all usages (use code-wizard)
- [ ] Plan rollback strategy

During refactoring:
- [ ] Make atomic commits
- [ ] Keep tests passing
- [ ] Update imports immediately

After refactoring:
- [ ] All tests pass
- [ ] Log to CHANGELOG.md
- [ ] Trigger docs-updater
