# OWASP Top 10 2025 Security Review (RC)

## Philosophy: Root Cause Analysis
Modern security review in 2025 focuses on **systemic design flaws** rather than isolated code bugs. Reviewers must look for "foot-guns" in architecture that enable whole classes of vulnerabilities.

## Review Checklist by Category

### A01: Broken Access Control (Including SSRF)
**Root Cause:** Design flaws in permission models and trust boundaries.
- [ ] **Deny-by-Default:** Are permissions explicitly granted? (Check for `allow *` or missing `else` blocks).
- [ ] **SSRF Validation:** Are URL inputs for server-side fetches (webhooks, proxies) restricted to allowlisted domains?
- [ ] **Object-Level Security (IDOR):** Does the backend verify that the current user owns the `id` being requested?
- [ ] **SSO/JWT Integrity:** Are tokens validated for signature *and* expiration on every request?

### A02: Security Misconfiguration (High Priority)
**Root Cause:** Cloud complexity and insecure "Infrastructure as Code" defaults.
- [ ] **Secrets Management:** Are API keys or DB strings in `.env` files or hardcoded? (Must use Vault/Secrets Manager).
- [ ] **Storage Exposure:** Are S3/R2 buckets or database ports exposed to `0.0.0.0/0`?
- [ ] **CORS Policy:** Is the `Access-Control-Allow-Origin` set to `*`? (Must be specific domains).
- [ ] **Default Creds:** Have default admin/test accounts been removed from the production manifest?

### A03: Software Supply Chain Failures
**Root Cause:** Untrusted dependencies and compromised build pipelines.
- [ ] **Slopsquatting Defense:** Have all AI-suggested packages been verified against official registries? (Look for <30 day old packages).
- [ ] **SBOM Check:** Does the project generate a current Software Bill of Materials?
- [ ] **Lockfile Integrity:** Are dependency versions pinned with hashes?
- [ ] **Pipeline Security:** Are CI/CD runners isolated and using short-lived credentials?

### A04: Cryptographic Failures
**Root Cause:** Use of deprecated algorithms or poor key lifecycle management.
- [ ] **Protocol Version:** Is TLS 1.3 enforced for all transit?
- [ ] **Algorithm Audit:** No MD5, SHA1, or RSA < 2048. Prefer AES-256-GCM.
- [ ] **Randomness:** Is `crypto.getRandomValues()` (not `Math.random`) used for nonces/salts?

### A05: Injection
**Root Cause:** Failure to separate data from instructions.
- [ ] **Parameterized Queries:** No string-concatenated SQL or NoSQL queries.
- [ ] **Prompt Injection:** Are system prompts segregated from user inputs in LLM calls?
- [ ] **Output Escaping:** Is data sanitized specifically for its destination (HTML vs. SQL vs. CLI)?

### A06: Insecure Design
**Root Cause:** Missing security requirements during the planning phase.
- [ ] **Trust Boundaries:** Are calls between microservices authenticated, or do they "blindly trust" internal IP traffic?
- [ ] **Business Logic:** Can users "discount stack" or manipulate prices via API parameters?

### A07: Authentication Failures
**Root Cause:** Weak identity lifecycle and session handling.
- [ ] **MFA Enforcement:** Is MFA required for admin actions or privilege changes?
- [ ] **Session Invalidation:** Do sessions terminate server-side upon logout?

### A08: Software and Data Integrity Failures
**Root Cause:** Unsigned code and unvetted third-party plugins.
- [ ] **Artifact Signing:** Are production builds signed to prevent tampering?
- [ ] **Auto-Updates:** Are third-party scripts loaded without Subresource Integrity (SRI) hashes?

### A09: Logging & Alerting Failures
**Root Cause:** Inability to detect active exploitation in real-time.
- [ ] **Audit Trail:** Are privilege changes, auth failures, and A10 exceptions logged with context?
- [ ] **No PII in Logs:** Are passwords, tokens, or emails stripped from logs?

### A10: Mishandling of Exceptional Conditions (New for 2025)
**Root Cause:** Unsafe fallback behavior and verbose error leaks.
- [ ] **Fail-Secure Logic:** If a database or auth service is down, does the code default to "Deny" (Fail-Closed) or "Allow" (Fail-Open)?
- [ ] **Exception Scrubbing:** Are stack traces and database schemas stripped from production error responses?
- [ ] **Fallback Integrity:** Does the application handle "partial transactions" correctly to prevent state corruption?

## Severity Matrix
| Severity | Action |
| :--- | :--- |
| **🔴 Critical** | Exploitable A01/A02. Data breach imminent. **Block PR.** |
| **🟠 High** | A03/A10 failures. Systemic risk. **Fix before release.** |
| **🟡 Medium** | A04/A09 gaps. Defense-in-depth issues. **Fix in sprint.** |
