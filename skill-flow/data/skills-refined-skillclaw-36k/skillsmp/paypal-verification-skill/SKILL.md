---
name: PayPal Verification Skill
description: Tools and instructions for verifying PayPal credentials and catching hidden character issues.
---

# PayPal Verification Skill

This skill provides a way to verify that your PayPal environment variables are correctly configured and that the API connection is healthy.

## Usage

Run the verification script to check your local and production-ready credentials:

```bash
node skills/paypal-verify/scripts/verify-env.js
```

## What it Checks
1. **Hidden Characters**: Detects trailing newlines or spaces in Client IDs and Secrets (a common cause of `invalid_client` errors).
2. **Environment Match**: Ensures you are using Sandbox IDs with the Sandbox URL, or Live IDs with the Live URL.
3. **Token Validation**: Attempts to fetch an actual OAuth2 token from PayPal to prove the credentials work.

## Common Fixes
If you see an "Invalid Client" error:
- Run `node skills/paypal-verify/scripts/verify-env.js` to see if a newline is detected.
- Use the `sync-local-env-to-vercel.sh` script to re-upload keys using `printf` which strips newlines.
- Ensure `PAYPAL_ENVIRONMENT` is exactly `LIVE` or `SANDBOX`.
