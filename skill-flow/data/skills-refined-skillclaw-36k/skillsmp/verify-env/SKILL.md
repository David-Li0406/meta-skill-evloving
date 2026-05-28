---
name: verify-env
description: Checks if critical environment variables are set for the project.
---

# Verify Environment Variables

This skill checks for the presence of essential environment variables required for the application to run correctly, specifically focusing on Supabase and Google Cloud credentials.

## Usage

Run the check script from the project root:

```bash
node skills/verify-env/scripts/check-env.js
```

## Checked Variables

- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `GOOGLE_SERVICE_ACCOUNT_EMAIL`
- `GOOGLE_SERVICE_ACCOUNT_PRIVATE_KEY`
- `VITE_SUPABASE_URL` (Warning only)
- `VITE_SUPABASE_ANON_KEY` (Warning only)
