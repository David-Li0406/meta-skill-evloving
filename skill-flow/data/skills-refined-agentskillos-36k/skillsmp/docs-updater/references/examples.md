# Documentation Update Examples

## Example 1: New Database Table

**Trigger:** Added `token_pools` table via migration

**Update `Docs/03-API.md`:**
```markdown
### Token Management (public)

| Table | Primary Key | Notes |
|-------|-------------|-------|
| `token_pools` | `id` (UUID) | **NEW** User token balances with expiry |
| `token_transactions` | `id` (UUID) | **NEW** Token usage history |
```

**Update `CLAUDE.MD` (if significant):**
```markdown
### Database Schemas

**public** - User data and application tables:
- Token management: `token_pools`, `token_transactions`
```

## Example 2: New RPC Function

**Trigger:** Created `check_token_balance(user_id)`

**Update `Docs/03-API.md`:**
```markdown
### Token RPCs

**check_token_balance** — Get user's current token balance:
\`\`\`sql
check_token_balance(p_user_id UUID DEFAULT auth.uid())
→ { available_tokens INT, expires_at TIMESTAMPTZ, plan_name TEXT }
\`\`\`

**TypeScript:**
\`\`\`typescript
const { data } = await supabase.rpc('check_token_balance');
// { available_tokens: 450, expires_at: '...', plan_name: 'pro' }
\`\`\`
```

## Example 3: New Edge Function

**Trigger:** Deployed `generate-study-plan` Edge Function

**Update `Docs/02-DESIGN.md`:**
```markdown
### Edge Functions

| Function | Auth | Purpose |
|----------|------|---------|
| `generate-study-plan` | JWT | **NEW** AI-powered study plan generation |
```

**Update `Docs/03-API.md`:**
```markdown
## Edge Function: generate-study-plan

**Endpoint:** `POST /functions/v1/generate-study-plan`
**Auth:** JWT required

### Request
\`\`\`json
{
  "duration_days": 30,
  "focus_topic": "grace"
}
\`\`\`

### Response
\`\`\`json
{
  "success": true,
  "plan": { "id": "...", "chapters": [...] }
}
\`\`\`
```

## Example 4: New Admin Page

**Trigger:** Created `/admin/subscriptions` page

**Update `Docs/07-ADMIN-GUIDE.md`:**
```markdown
## Subscriptions Page

**Path:** `/admin/subscriptions`

Manage subscription plans, token allocations, and feature access.

### Tabs
- **Plans** — Configure plan token limits
- **Operations** — Set token costs per AI operation
- **Access** — Control feature availability per plan
```

## Example 5: Feature Enhancement

**Trigger:** Added playback speed control to audio player

**Update `README.md`:**
```markdown
## Key Features

- Audio Bible with ElevenLabs TTS
  - Playback speed control (0.5x - 2.0x)
  - Chapter-by-chapter playback
```

## Example 6: Subscription System Change

**Trigger:** Changed from per-feature quotas to token pools

**Update `Docs/13-SUBSCRIPTION-SYSTEM.md` TL;DR:**
```markdown
> **TL;DR:** Unified token pool replaces per-feature quotas.
>
> **Key Points:**
> - Single token balance per user (not per-feature)
> - Fixed costs: Search=20, Study=100, Translation=10
> - 6-hour rolling window for token refresh
> - Admin configures via `/admin/subscriptions`
```

## Multi-Doc Update Checklist

When making significant changes, update in order:

1. [ ] `Docs/03-API.md` — Schema/RPC changes
2. [ ] `Docs/02-DESIGN.md` — Architecture diagrams
3. [ ] `Docs/06-AI-ARCHITECTURE.md` — AI-specific changes
4. [ ] `Docs/07-ADMIN-GUIDE.md` — Admin UI changes
5. [ ] `README.md` — User-facing features
6. [ ] `CLAUDE.MD` — AI context (major changes only)
