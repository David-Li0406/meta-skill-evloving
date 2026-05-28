---
name: oe-playwright-e2e
description: Official Playwright E2E testing protocol. Triggers on "E2E", "Playwright", "browser test". Enforces fresh client state, hybrid mode, and clean ports.
---

# oe-playwright-e2e

## 1. Prerequisites (Port Hygiene)
**CRITICAL:** Before starting, ensure no zombie processes are blocking ports.
- **Frontend:** Port 3000 must be clean or running the *current* version.
- **Backend:** Port 8000 must be clean or running the *current* version.
- **Check:** `lsof -i :3000` and `lsof -i :8000`.
- **Action:** Kill unexpected processes if necessary (`kill -9 <PID>`).

## 2. Environment Setup (Hybrid Mode)
The standard E2E configuration is **Hybrid Mode** (Gemini for extraction, OpenAI for verbalization).
- Ensure `AGENT_MODE=gemini` is set in `.env` or passed to the backend.
- Ensure `DETECTION_MODE=unified`.
- Verify API keys for both providers are available (Keychain or env).

## 3. Fresh Client (Mandatory)
**NEVER reuse an email address from a previous run** unless explicitly testing "resume flow".
- **Why?** Existing emails trigger "Welcome back" flows, causing fallbacks and breaking "new inquiry" assertions.
- **How?** Generate a unique email: `e2e_test_<timestamp>@example.com` (e.g., `playwright-20260119-1234@test.com`).
- **Reset:** If the test requires a clean database state, consider using a dedicated test tenant or wiping the test user's data first.

## 4. Execution Steps
1.  **Start Backend:**
    ```bash
    ./scripts/dev/dev_server.sh
    ```
2.  **Start Frontend:**
    ```bash
    cd atelier-ai-frontend && npm run dev
    ```
3.  **Run Playwright (MCP or Shell):**
    - **Interactive:** Use `@playwright/mcp` to drive the browser and inspect the UI.
    - **Headless/Automated:**
      ```bash
      # In atelier-ai-frontend/
      npx playwright test tests/e2e/<specific_test>.spec.ts
      ```

## 5. Common Pitfalls
- **"Welcome back" message:** You used an old email. **FAIL.** Restart with a fresh one.
- **Backend 404/Connection Refused:** Check if port 8000 is running the correct server.
- **Frontend 404/Connection Refused:** Check if port 3000 is running.
