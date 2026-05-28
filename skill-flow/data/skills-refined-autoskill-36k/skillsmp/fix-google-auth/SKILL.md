---
name: fix-google-auth
description: Diagnose and resolve Google OAuth 'server_error' caused by credential mismatches.
---

# Fix Google Auth Mismatch

If you encounter `server_error: Unable to exchange external code` during Google Sign-In, it is 99% likely due to a **Client Secret Mismatch** between your local environment (`.env.local`) and the **Supabase Dashboard**.

This usually happens after:
1.  Running `setup-google-oauth.ts` (which may create a new secret).
2.  Rotated keys in Google Cloud Console.

## Resolution Steps

### 1. Update Local Credentials
Run the helper script to securely update your local `.env.local` file with the correct Google Client Secret.

```bash
cd /Users/thelostunfounds/.gemini/antigravity/scratch/thelostandunfounds
npx tsx scripts/update-google-secret.ts
```

This script will prompt you to paste the secret (input is hidden) and save it correctly.

### 2. Update Supabase Dashboard
**CRITICAL**: Updating locally is not enough. You must sync Supabase.

1.  Copy the **SAME** secret you just used.
2.  Go to [Supabase Dashboard > Auth > Providers > Google](https://supabase.com/dashboard/project/nonaqhllakrckbtbawrb/auth/providers).
3.  Paste the secret into the **Client Secret** field.
4.  Click **Save**.

### 3. Verification
1.  Restart the dev server: `npm run dev`
2.  Attempt login at `http://localhost:3000`.

## Scripts
- `scripts/update-google-secret.ts`: Utility to update `.env.local` securely.
