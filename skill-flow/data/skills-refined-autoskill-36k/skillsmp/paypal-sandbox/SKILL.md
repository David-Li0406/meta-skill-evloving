---
name: paypal-sandbox
description: Manages PayPal sandbox environment for local testing and development. Ensures transactions do not use real money and routes to the correct PayPal sandbox endpoints.
---

# PayPal Sandbox Skill

This skill ensures that all local payment testing is safely isolated in the PayPal Sandbox environment.

## 1. Environment Configuration

To enable Sandbox mode, ensure your `.env.local` (or server environment) has the following variables set:

```bash
# Set to SANDBOX for testing, LIVE for production
PAYPAL_ENVIRONMENT=SANDBOX

# Sandbox Credentials (from developer.paypal.com)
PAYPAL_CLIENT_ID_SANDBOX=your_sandbox_client_id
PAYPAL_CLIENT_SECRET_SANDBOX=your_sandbox_client_secret

# Optional: Override return URLs for local testing
PAYPAL_RETURN_URL_SANDBOX=http://localhost:3000
```

### Critical Implementation Note
When loading environment variables in `local-server.js`, **ALWAYS load `.env.local` BEFORE `.env`**.
`dotenv` does not overwrite existing keys. If you load `.env` (Live) first, it will LOCK the environment to Live, ignoring your local Sandbox overrides.

**Correct Order:**
```javascript
dotenv.config({ path: resolve(__dirname, '.env.local') }); // Loads Sandbox/Overrides FIRST
dotenv.config({ path: resolve(__dirname, '.env') });       // Loads Defaults SECOND
```

## 2. Local Server Port Rule (CRITICAL)

**ALWAYS use port 3000 for local development.** If port 3000 is already in use, you MUST:

1. **Kill the existing process on port 3000:**
   ```bash
   lsof -ti:3000 | xargs kill -9 2>/dev/null || true
   ```

2. **Then start the dev server on port 3000:**
   ```bash
   npm run dev -- --port 3000
   ```

**Why this matters:**
- PayPal sandbox redirect URLs are configured for `localhost:3000`
- Vite will automatically pick a different port (e.g., 3001) if 3000 is busy, breaking PayPal redirects
- The entire payment flow assumes port 3000

## 3. Testing Workflow

### 3.1 Sanity Check
Before testing, verify the API is hitting the sandbox endpoint:
- `https://api.sandbox.paypal.com` (NOT `api.paypal.com`)

### 3.2 Test Accounts
Use "Personal" and "Business" sandbox accounts created at [developer.paypal.com](https://developer.paypal.com/dashboard/accounts).
- **Personal Account**: Use this to "buy" items in your local shop.
- **Business Account**: This is the "merchant" account receiving the fake funds.

### 3.3 Verification
1. Ensure the "Secure Checkout" button redirects to `sandbox.paypal.com`.
2. Complete a test transaction using the personal sandbox account.
3. Verify that the redirect back to `/payment/success` works correctly on localhost.

## 4. Critical Rules
- **NEVER** use real credit card numbers in the sandbox.
- **NEVER** set `PAYPAL_ENVIRONMENT=LIVE` in a local `.env.local` file.
- If a 401 Unauthorized occurs, refresh your Sandbox client credentials.
- Ensure `localhost:3000` is added as a valid redirect URI in your PayPal app settings if using OAuth.

## 5. Automated Testing & Bot Protection (Mitigation Strategy)

PayPal aggressively blocks automated browsers (used by AI agents), often resulting in a "You have been blocked" screen during testing. **This does NOT mean the feature failed.**

### Symptom
- Automated browser redirects to PayPal but shows a generic "Blocked" or "Security Challenge" message.
- URL is correct: `https://www.paypal.com/checkoutnow?token=...` or `https://www.sandbox.paypal.com/...`

### Validation Strategy (If Blocked)
**Do not attempt to bypass the block.** Instead, validate the success based on the **handoff state**:

1. **Check URL Structure**: If the browser reached `paypal.com` with a valid `?token=...` query parameter, the Application <-> PayPal handshake was **SUCCESSFUL**.
2. **Confirm API Handoff**: The presence of the token proves the backend successfully authenticated, created an order, and received a redirect URL.
3. **Report Success**: Inform the user that the "Blocked" screen is an expected artifact of automated testing. Direct the user to copy the URL into a regular browser to verify the visual interface.

**Example Report:**
> "The checkout flow is functioning correctly. The backend successfully initiated the session, and the browser redirected to PayPal with a valid token (`token=...`). The 'Blocked' screen is expected when using an automated agent. Please verify the visual checkout by determining the URL in a standard browser."
