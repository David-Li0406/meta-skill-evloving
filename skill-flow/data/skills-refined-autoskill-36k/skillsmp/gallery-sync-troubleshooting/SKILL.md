---
name: Gallery Sync Troubleshooting
description: How to diagnose and fix Google Drive gallery sync issues in production and local
---

# Gallery Sync Troubleshooting

## Quick Test Commands

**Production:**
```bash
curl -s "https://www.thelostandunfounds.com/api/gallery/sync?slug=last-night"
```

**Local:**
```bash
curl -s "http://localhost:3001/api/gallery/sync?slug=last-night"
```

## Common Errors & Fixes

### 1. `DECODER routines::unsupported`
**Cause:** Private key newlines are not properly parsed from Vercel env vars.

**Fix:** Ensure key parsing in `api/gallery/[...path].ts` uses:
```typescript
let GOOGLE_KEY = (rawKey || '')
    .replace(/\\n/g, '\n')  // Handle literal \n strings
    .replace(/"/g, '')
    .trim();
```

**Re-upload key from local:**
```bash
source .env.local && echo "$GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY" | npx vercel env add GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY production --force
```

### 2. `invalid_grant: account not found`
**Cause:** Service account email doesn't match the private key.

**Fix:**
```bash
echo 'the-gallery-agent@the-lost-and-unf-1737406545588.iam.gserviceaccount.com' | npx vercel env add GOOGLE_SERVICE_ACCOUNT_EMAIL production --force
```

### 3. `Missing credentials`
**Cause:** Environment variables not set in Vercel.

**Verify with:**
```bash
npx vercel env ls production
```

Required vars:
- `GOOGLE_SERVICE_ACCOUNT_EMAIL`
- `GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY`
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`

### 4. `Library not found` or `No Google Drive folder ID`
**Cause:** Library doesn't exist in DB or missing `google_drive_folder_id`.

**Check in Supabase:**
```sql
SELECT slug, google_drive_folder_id FROM photo_libraries;
```

## After Updating Env Vars
Always trigger a redeploy:
```bash
git commit --allow-empty -m "Trigger redeploy" && git push origin main
```

## Key Files
- **Production API:** `api/gallery/[...path].ts` (inlined `syncGalleryPhotos`)
- **Local Server:** `local-server.js` → `/api/gallery/sync` handler
- **Original Utils:** `lib/api-handlers/_photo-sync-utils.ts`
