# Changelog Examples

## Full Entry Example

```markdown
## 2026-01-08 - Subscription System Overhaul

### [SCHEMA] [BREAKING] Replace per-feature quotas with unified token pool

**Context:**
The old system tracked quotas per AI feature (search, study, translation) with 40+ database rows per plan. Users found it confusing and admins struggled to manage.

**Before:**
- `ai_plan_quotas` table with feature-specific rows
- `check_ai_quota(user_id, feature)` RPC
- Per-feature quota hooks in frontend

**After:**
- `subscription_plans` table with plan definitions
- `token_pools` table with user balances
- `ai_operations` table with operation costs
- `check_token_balance(user_id)` RPC
- Single `useTokenBalance` hook

**Impact:**
- Files affected: 15
- Migration: 20260108_token_pool_system.sql
- Breaking: Yes
- Rollback: Restore ai_plan_quotas, revert RPC

**Related:**
- Migration: #20260108_token_pool_system
- PR: #142
- Issue: #98

---

### [API] Add deduct_tokens RPC

**Before:** No RPC existed
**After:** `deduct_tokens(user_id, operation, amount)` → success/failure

**Impact:**
- Files: 3 | Breaking: No

---

### [COMPONENT] Create TokenBalanceIndicator component

**Before:** Quota display scattered across 4 components
**After:** Single `<TokenBalanceIndicator />` component

**Impact:**
- Files: 5 | Breaking: No
```

## Compact Entry Examples

### Schema Change
```markdown
### [SCHEMA] Add expires_at column to token_pools

**Before:** No expiry tracking
**After:** `expires_at TIMESTAMPTZ` column with 6-hour default
**Impact:** Files: 2 | Migration: Yes | Breaking: No
```

### Structure Change
```markdown
### [STRUCTURE] Move admin components to dedicated directory

**Before:** `src/components/Admin*.tsx` (9 files in components root)
**After:** `src/components/admin/*.tsx` (organized subdirectory)
**Impact:** Files: 15 | Breaking: No (import paths updated)
```

### API Change
```markdown
### [API] Rename get_user_quota → get_token_balance

**Before:** `get_user_quota(user_id, feature)`
**After:** `get_token_balance(user_id)`
**Impact:** Files: 6 | Breaking: Yes (signature changed)
```

### Component Change
```markdown
### [COMPONENT] Split AdminAIPage into AIPromptsPage and AIQuotasPage

**Before:** Single 800-line page with 4 tabs
**After:** Two focused pages (~300 lines each)
**Impact:** Files: 4 | Breaking: No (routes updated)
```

### Dependency Change
```markdown
### [DEPS] Upgrade @tanstack/react-query 4.x → 5.x

**Before:** v4.36.1
**After:** v5.17.0
**Impact:** Files: 3 | Breaking: No (API compatible)
```

## Query Response Examples

### "What changed in subscription system?"

```markdown
## Subscription System Changes (Jan 2026)

### Breaking Changes
1. **[SCHEMA] Token pool migration** (Jan 8)
   - `ai_plan_quotas` → `subscription_plans` + `token_pools` + `ai_operations`
   - Migration: 20260108_token_pool_system.sql

2. **[API] RPC signature changes** (Jan 8)
   - `check_ai_quota` → `check_token_balance`
   - `use_ai_quota` → `deduct_tokens`

### Non-Breaking Changes
1. **[COMPONENT] TokenBalanceIndicator** (Jan 8)
   - New unified balance display component

2. **[API] plan_feature_access table** (Jan 8)
   - Feature gating per subscription tier
```

### "What database changes were made this week?"

```markdown
## Database Changes (Jan 6-12, 2026)

| Date | Change | Tables | Migration |
|------|--------|--------|-----------|
| Jan 8 | Token pool system | +3 tables, -1 table | 20260108_token_pool_system |
| Jan 7 | Add audit fields | profiles, bookmarks | 20260107_audit_fields |

### Details

**Jan 8: Token Pool System**
- Added: subscription_plans, token_pools, ai_operations, plan_feature_access
- Removed: ai_plan_quotas
- Breaking: Yes

**Jan 7: Audit Fields**
- Added: created_by, updated_by columns
- Breaking: No
```

### "What breaking changes need documentation?"

```markdown
## Breaking Changes Requiring Doc Updates

1. **[SCHEMA] ai_plan_quotas removed** (Jan 8)
   - Update: Docs/03-API.md (remove table reference)
   - Update: Docs/13-SUBSCRIPTION-SYSTEM.md (new schema)

2. **[API] check_ai_quota → check_token_balance** (Jan 8)
   - Update: Docs/03-API.md (RPC signature)
   - Update: Docs/05-DEV.md (usage examples)

Action: Run `/docs-updater sync-schemas`
```
