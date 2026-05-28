# SIAS Setup Guide

## API Base URL

```
Production: https://28dayreset.com
```

## Authentication

Most debug endpoints require `X-User-ID` header with admin ID:

```bash
curl -s "https://28dayreset.com/api/admin/users" \
  -H "X-User-ID: 0f950f68-885c-47f9-9cb4-aabbb8bea55f"
```

## Admin Users

| Name | User ID | Role |
|------|---------|------|
| Russell Deming | `0f950f68-885c-47f9-9cb4-aabbb8bea55f` | Admin |

## Debug Endpoints (No Auth)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/debug/user-breakdown/:userId` | GET | Expected points from source |
| `/api/debug/ledger/:userId` | GET | Full ledger transactions |
| `/api/debug/rebuild-ledger/:userId` | POST | Rebuild ledger |
| `/api/debug/biometric-complete-fix/:userId` | POST | Fix biometric scoring |
| `/api/biometrics/history` | GET | Biometric entries (X-User-ID required) |

## Admin Endpoints (Auth Required)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/admin/users` | GET | List users with pagination |
| `/api/admin/users/:userId` | GET | Single user details |
| `/api/admin/enrollments/:id/onboarding` | PATCH | Fix onboarding status |
| `/api/debug/ledger-backups` | GET | List backups |
| `/api/debug/restore-ledger/:backupId` | POST | Restore backup |

## Common Workflows

### Audit Single User
```bash
# 1. Check breakdown
curl -s "https://28dayreset.com/api/debug/user-breakdown/{USER_ID}"

# 2. Fix biometrics if needed
curl -s -X POST "https://28dayreset.com/api/debug/biometric-complete-fix/{USER_ID}?dryRun=true"
curl -s -X POST "https://28dayreset.com/api/debug/biometric-complete-fix/{USER_ID}?dryRun=false"

# 3. Rebuild ledger if needed
curl -s -X POST "https://28dayreset.com/api/debug/rebuild-ledger/{USER_ID}?dryRun=true"
curl -s -X POST "https://28dayreset.com/api/debug/rebuild-ledger/{USER_ID}"

# 4. Verify
curl -s "https://28dayreset.com/api/debug/user-breakdown/{USER_ID}"
```

### Search for User
```bash
curl -s "https://28dayreset.com/api/admin/users?search=Bonnie&limit=10" \
  -H "X-User-ID: 0f950f68-885c-47f9-9cb4-aabbb8bea55f"
```

### Fix Incomplete Onboarding
```bash
# 1. Check enrollment
curl -s "https://28dayreset.com/api/admin/users/{USER_ID}" \
  -H "X-User-ID: 0f950f68-885c-47f9-9cb4-aabbb8bea55f"

# 2. Fix onboarding
curl -s -X PATCH "https://28dayreset.com/api/admin/enrollments/{ENROLLMENT_ID}/onboarding" \
  -H "X-User-ID: 0f950f68-885c-47f9-9cb4-aabbb8bea55f" \
  -H "Content-Type: application/json" \
  -d '{"onboardingComplete": true}'
```

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| "No active enrollment" | Incomplete onboarding | Fix enrollment status |
| "409 Conflict" | Rebuild in progress | Wait 5 mins, retry |
| "429 Rate Limit" | Too many rebuilds | Wait for cooldown (max 3/hr) |
| Empty biometrics response | Missing header | Add `X-User-ID` header |

## Source Files

| File | Purpose |
|------|---------|
| `shared/biometric-utils.ts` | Biometric scoring logic |
| `worker/user-routes.ts` | Debug/admin endpoints |
| `worker/sias-engine.ts` | SIAS audit engine |
| `worker/entities.ts` | Entity classes |
