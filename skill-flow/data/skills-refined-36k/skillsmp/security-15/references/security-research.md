# security Research

Research document for the security specialist skill.

## Phase 1: Upstream Survey

### VoltAgent/awesome-claude-code-subagents

The [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) repository contains several security-related subagents in the **Security & Quality Category (04)**:

| Subagent | Description |
|----------|-------------|
| `security-auditor` | Security vulnerability expert focused on identifying and assessing security flaws in code and systems |
| `security-engineer` | Specializes in infrastructure security for protecting cloud and on-premises environments |
| `penetration-tester` | Ethical hacking specialist who tests systems for vulnerabilities |
| `ad-security-reviewer` | Active Directory security and GPO audit specialist |
| `powershell-security-hardening` | PowerShell security hardening and compliance specialist |
| `compliance-auditor` | Expert in regulatory compliance ensuring systems meet security standards |
| `incident-responder` | Handles system incident response and recovery from security events |
| `devops-incident-responder` | Specializes in DevOps incident management for infrastructure issues |

These agents are available through the `voltagent-qa-sec` plugin, which bundles testing, security, and code quality specialists together.

### obra/superpowers

The [obra/superpowers](https://github.com/obra/superpowers) repository does **not contain dedicated security-focused skills**. However, it includes security-adjacent functionality:

- **test-driven-development** - Enforces RED-GREEN-REFACTOR cycle, indirectly supporting code quality
- **systematic-debugging** - Implements 4-phase root cause process with defense-in-depth techniques
- **code-review processes** - Skills for requesting and receiving code reviews enable peer validation

The framework emphasizes "Evidence over claims—Verify before declaring success," which aligns with security verification practices, though no explicit security audit skill exists.

---

## Phase 2: Research Findings

### 1. Secret Management Best Practices

#### The Problem

According to [GitGuardian](https://blog.gitguardian.com/secrets-api-management/), the number of detected hard-coded secrets increased 67% from 2021 to 2022, with 10 million new secrets found solely within public commits on GitHub.

#### Core Principles

From the [OWASP DevSecOps Guideline](https://owasp.org/www-project-devsecops-guideline/latest/01a-Secrets-Management):
- Never store unencrypted secrets in git
- Enforce automated secrets scanning
- Avoid plaintext sharing in messaging systems
- Use dedicated secrets management tools
- Apply least privilege and short-lived keys
- Implement robust rotation and monitoring strategies

#### Layered Security Approach

Source: [GitHub Community Discussion](https://github.com/orgs/community/discussions/158668)

1. **.gitignore** - Prevent untracked files from being committed
2. **Pre-commit hooks** - Block mistakes during commits
3. **GitHub Secret Scanning** - Continuous protection after push
4. **git filter-repo** - Emergency response if secrets are exposed

#### Insecure vs Secure Patterns

```python
# INSECURE: Hardcoded secrets
API_KEY = "sk-1234567890abcdef"
DATABASE_URL = "postgres://admin:password123@localhost/db"

# SECURE: Environment variables
import os
API_KEY = os.environ.get("API_KEY")
DATABASE_URL = os.environ.get("DATABASE_URL")
```

```yaml
# SECURE: .gitignore example
.env
.env.local
.env.*.local
*.pem
*.key
credentials.json
secrets.yaml
config/secrets/
```

#### Secret Scanning Tools

From [Jit's Git Secrets Scanners Guide](https://www.jit.io/resources/appsec-tools/git-secrets-scanners-key-features-and-top-tools-):

| Tool | Description | Use Case |
|------|-------------|----------|
| [Gitleaks](https://github.com/gitleaks/gitleaks) | Fast, lightweight secret scanner | Pre-commit hooks, CI/CD |
| [TruffleHog](https://docs.trufflesecurity.com/pre-commit-hooks) | Comprehensive scanner with 800+ detectors and verification | Deep scanning, verification |
| [git-secret](https://sobolevn.me/git-secret/) | Encrypt secrets in-repo | Team secret sharing |
| [SOPS](https://github.com/mozilla/sops) | Encrypt secrets in YAML/JSON files | GitOps workflows |

#### Pre-commit Hook Configuration

Source: [TruffleHog Docs](https://docs.trufflesecurity.com/pre-commit-hooks)

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.24.2
    hooks:
      - id: gitleaks

  - repo: local
    hooks:
      - id: trufflehog
        name: TruffleHog
        description: Detect secrets in your data
        entry: bash -c 'trufflehog git file://. --since-commit HEAD --only-verified --fail'
        language: system
        stages: ["commit", "push"]
```

#### Secrets Management Tools

From [Cycode Best Secrets Management Tools](https://cycode.com/blog/best-secrets-management-tools/):
- **HashiCorp Vault** - Industry standard for secret storage and rotation
- **AWS Secrets Manager** - Cloud-native for AWS environments
- **Azure Key Vault** - Microsoft ecosystem integration
- **Google Secret Manager** - GCP-native solution

---

### 2. Dependency Vulnerability Scanning

#### Overview

Source: [Shinagawa Labs Dependency Security](https://shinagawa-web.com/en/blogs/dependency-package-security-audit)

When using OSS packages, continuous security checks and proper management are essential. By adopting automatic scanning with Snyk/Dependabot and using npm audit/yarn audit, you can prevent vulnerabilities in advance and maintain a secure development environment.

#### Tool Comparison

| Tool | Language | Source | Notes |
|------|----------|--------|-------|
| [npm audit](https://docs.npmjs.com/auditing-package-dependencies-for-security-vulnerabilities/) | JavaScript | npm | Built-in, may have false positives |
| [Snyk](https://snyk.io) | Multi-language | Snyk DB | Paid tiers, human-curated |
| [Dependabot](https://github.com/dependabot) | Multi-language | GitHub Advisories | Free for public repos, auto-PRs |
| [pip-audit](https://github.com/pypa/pip-audit) | Python | PyPI/OSV | Free, auto-fix support |
| [govulncheck](https://go.dev/doc/security/vuln/) | Go | Go Vulnerability DB | Official Go tool, call-graph analysis |
| [Safety](https://github.com/pyupio/safety) | Python | Safety DB | Comprehensive Python DB |

#### npm audit

Source: [npm Docs](https://docs.npmjs.com/auditing-package-dependencies-for-security-vulnerabilities/)

```bash
# Basic audit
npm audit

# Fix automatically (patch/minor versions)
npm audit fix

# Force fix (may include breaking changes)
npm audit fix --force

# JSON output for CI/CD
npm audit --json
```

#### pip-audit

Source: [pip-audit on PyPI](https://pypi.org/project/pip-audit/)

```bash
# Install
pip install pip-audit

# Audit current environment
pip-audit

# Audit requirements file
pip-audit -r requirements.txt

# Auto-fix vulnerabilities
pip-audit --fix

# JSON output
pip-audit --format=json

# Different output formats: columns, json, cyclonedx-json, cyclonedx-xml, markdown
pip-audit --format=cyclonedx-json > sbom.json
```

**Note from [Inedo](https://blog.inedo.com/python/pypi-package-vulnerabilities)**: pip-audit analyzes dependency trees, not code. Users must not assume it will defend against malicious packages or detect transitive vulnerabilities not part of the package itself.

#### govulncheck

Source: [Go Vulnerability Management](https://go.dev/doc/security/vuln/)

```bash
# Install
go install golang.org/x/vuln/cmd/govulncheck@latest

# Scan current module
govulncheck ./...

# Scan a binary
govulncheck -mode=binary ./myapp

# JSON output
govulncheck -json ./...

# SARIF output for CI integration
govulncheck -format=sarif ./...
```

Key feature from [Semaphore](https://semaphore.io/blog/govulncheck): govulncheck analyzes your codebase and **only surfaces vulnerabilities that actually affect you**, based on which functions in your code are transitively calling vulnerable functions.

#### Snyk CI/CD Integration

Source: [Snyk vs npm audit comparison](https://github.com/lirantal/snyk-vs-npm-audit)

```yaml
# GitHub Actions example
- name: Run Snyk
  uses: snyk/actions/node@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
  with:
    args: --severity-threshold=high
```

#### Dependabot Configuration

Source: [GitHub Dependabot](https://docs.github.com/en/code-security/dependabot)

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10

  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"

  - package-ecosystem: "gomod"
    directory: "/"
    schedule:
      interval: "weekly"
```

#### Best Practices

From [Shinagawa Labs](https://shinagawa-web.com/en/blogs/dependency-package-security-audit):
- **Patch releases**: Automatic updates acceptable
- **Minor updates**: Manual review recommended
- **Major version changes**: Extensive testing required

---

### 3. Code Injection Prevention

#### OWASP Top 10:2025 Context

Source: [OWASP Top 10:2025](https://owasp.org/Top10/2025/)

Injection (A05:2025) dropped from #3 to #5 but remains critical. It includes Cross-site Scripting (high frequency/low impact) to SQL Injection (low frequency/high impact).

#### SQL Injection Prevention

Source: [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)

**Primary Defense: Parameterized Queries**

```python
# INSECURE: String concatenation
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)

# SECURE: Parameterized query
query = "SELECT * FROM users WHERE username = %s"
cursor.execute(query, (username,))
```

```javascript
// INSECURE: String concatenation (Node.js)
const query = `SELECT * FROM users WHERE id = ${userId}`;
db.query(query);

// SECURE: Parameterized query
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);
```

```go
// INSECURE: String formatting (Go)
query := fmt.Sprintf("SELECT * FROM users WHERE id = %s", userID)
db.Query(query)

// SECURE: Parameterized query
query := "SELECT * FROM users WHERE id = $1"
db.Query(query, userID)
```

**Important caveat** from [PortSwigger](https://portswigger.net/web-security/sql-injection): Input filtering and escaping can help stop trivial attacks but does not fix the underlying vulnerability and can often be evaded.

#### Cross-Site Scripting (XSS) Prevention

Source: [OWASP Content Security Policy Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)

**Primary Defense: Output Encoding**

```javascript
// INSECURE: Direct innerHTML
element.innerHTML = userInput;

// SECURE: textContent (auto-escapes)
element.textContent = userInput;

// SECURE: Manual encoding for HTML context
function escapeHtml(text) {
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  return text.replace(/[&<>"']/g, m => map[m]);
}
element.innerHTML = escapeHtml(userInput);
```

```python
# SECURE: Using template engine auto-escaping (Jinja2)
from markupsafe import escape
safe_output = escape(user_input)

# Django templates auto-escape by default
# {{ user_input }} is safe
# {{ user_input|safe }} bypasses escaping - use with caution
```

#### Command Injection Prevention

Source: [SentinelOne Code Injection Guide](https://www.sentinelone.com/cybersecurity-101/cybersecurity/code-injection/)

```python
# INSECURE: Shell=True with user input
import subprocess
subprocess.run(f"ls {user_path}", shell=True)

# SECURE: Avoid shell, use list arguments
subprocess.run(["ls", user_path], shell=False)

# SECURE: Use shlex for necessary shell commands
import shlex
safe_path = shlex.quote(user_path)
subprocess.run(f"ls {safe_path}", shell=True)
```

```javascript
// INSECURE: exec with user input (Node.js)
const { exec } = require('child_process');
exec(`ls ${userPath}`);

// SECURE: execFile with arguments array
const { execFile } = require('child_process');
execFile('ls', [userPath]);
```

---

### 4. Authentication and Authorization Patterns

#### Authentication vs Authorization

Source: [Frontegg OAuth vs JWT](https://frontegg.com/blog/oauth-vs-jwt)

- **Authentication**: "Who are you?" - Verifying identity
- **Authorization**: "What can you do?" - Determining permissions

#### JWT (JSON Web Tokens)

Source: [Curity JWT Best Practices](https://curity.io/resources/learn/jwt-best-practices/)

**Structure**: Header + Payload + Signature

```javascript
// JWT Structure
{
  // Header
  "alg": "RS256",
  "typ": "JWT"
}
.
{
  // Payload
  "sub": "user123",
  "iat": 1704067200,
  "exp": 1704070800,
  "roles": ["user"]
}
.
[signature]
```

**Best Practices** from [LogRocket JWT Guide](https://blog.logrocket.com/jwt-authentication-best-practices/):

```javascript
// INSECURE: Long-lived tokens
const token = jwt.sign(payload, secret, { expiresIn: '30d' });

// SECURE: Short-lived access tokens + refresh tokens
const accessToken = jwt.sign(payload, secret, { expiresIn: '15m' });
const refreshToken = jwt.sign({ sub: userId }, refreshSecret, { expiresIn: '7d' });
```

```javascript
// INSECURE: Storing JWT in localStorage (XSS vulnerable)
localStorage.setItem('token', jwt);

// SECURE: HttpOnly cookie (not accessible via JavaScript)
res.cookie('token', jwt, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict',
  maxAge: 900000 // 15 minutes
});
```

**Critical warning** from [Stytch](https://stytch.com/blog/jwts-vs-sessions-which-is-right-for-you/): JWTs are not your authorization system. They carry identity—not permissions. Once signed, there is no way to invalidate the JWT until it expires.

#### OAuth 2.0 Integration

Source: [Coder Facts OAuth2 Best Practices](https://coderfacts.com/security-and-best-practices/oauth2-jwt-best-practices/)

```javascript
// OAuth 2.0 Authorization Code Flow (recommended for web apps)
// 1. Redirect to authorization server
const authUrl = `https://auth.example.com/authorize?
  client_id=${CLIENT_ID}&
  redirect_uri=${REDIRECT_URI}&
  response_type=code&
  scope=openid profile email&
  state=${generateSecureState()}`;

// 2. Exchange code for tokens (server-side)
const tokenResponse = await fetch('https://auth.example.com/token', {
  method: 'POST',
  body: new URLSearchParams({
    grant_type: 'authorization_code',
    code: authorizationCode,
    redirect_uri: REDIRECT_URI,
    client_id: CLIENT_ID,
    client_secret: CLIENT_SECRET
  })
});
```

#### Session Management Security

Source: [Medium Authentication Methods Compared](https://medium.com/@sarthakshah1920/authentication-methods-compared-session-vs-jwt-vs-oauth-2-0-4ce551ea3050)

```javascript
// SECURE: Session cookie configuration
app.use(session({
  secret: process.env.SESSION_SECRET,
  name: 'sessionId', // Don't use default 'connect.sid'
  cookie: {
    httpOnly: true,     // Prevents XSS access
    secure: true,       // HTTPS only
    sameSite: 'strict', // CSRF protection
    maxAge: 3600000     // 1 hour
  },
  resave: false,
  saveUninitialized: false,
  store: new RedisStore({ client: redisClient }) // External store for scalability
}));
```

#### When to Use What

Source: [Leapcell Auth Comparison](https://leapcell.io/blog/session-jwt-sso-oauth-pros-cons-and-use-cases)

| Method | Use Case |
|--------|----------|
| Sessions | Traditional web apps, need immediate invalidation |
| JWT | Stateless APIs, microservices, mobile apps |
| OAuth 2.0 | Third-party API access, delegated authorization |
| OpenID Connect | Single sign-on, user identity verification |

---

### 5. Security Headers and HTTPS

#### Essential Security Headers

Source: [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)

| Header | Purpose |
|--------|---------|
| Strict-Transport-Security | Enforce HTTPS |
| Content-Security-Policy | Prevent XSS, control resource loading |
| X-Content-Type-Options | Prevent MIME sniffing |
| X-Frame-Options | Prevent clickjacking |
| Referrer-Policy | Control referrer information |
| Permissions-Policy | Control browser features |

#### HTTP Strict Transport Security (HSTS)

Source: [MDN HSTS Documentation](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security)

```
# Basic HSTS (1 year)
Strict-Transport-Security: max-age=31536000

# Include subdomains
Strict-Transport-Security: max-age=31536000; includeSubDomains

# HSTS Preload (submit to browser preload list)
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

**Warning** from [DCHost Guide](https://www.dchost.com/blog/en/http-security-headers-guide-how-to-correctly-set-hsts-csp-x-frame-options-and-referrer-policy/): HSTS on domains without stable HTTPS can lock users out if certificates expire or subdomains are misconfigured.

#### Content Security Policy (CSP)

Source: [MDN CSP Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP)

```
# Strict CSP example
Content-Security-Policy: 
  default-src 'self';
  script-src 'self' 'nonce-randomValue123';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  font-src 'self';
  connect-src 'self' https://api.example.com;
  frame-ancestors 'none';
  base-uri 'self';
  form-action 'self';

# Report-Only mode for testing
Content-Security-Policy-Report-Only: default-src 'self'; report-uri /csp-report
```

**Best practice** from [OWASP CSP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html): Roll out CSP using Report-Only mode first, tune policies, then switch to enforcing mode when stable.

#### X-Frame-Options (Legacy)

Source: [MDN X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Frame-Options)

```
# Prevent all framing
X-Frame-Options: DENY

# Allow same-origin framing only
X-Frame-Options: SAMEORIGIN
```

**Note**: CSP `frame-ancestors` directive is the modern replacement but include X-Frame-Options for older browser support.

#### Complete Security Headers Example

Source: [OWASP HTTP Headers Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html)

```javascript
// Express.js middleware
app.use((req, res, next) => {
  // HSTS
  res.setHeader('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  
  // CSP
  res.setHeader('Content-Security-Policy', "default-src 'self'; script-src 'self'");
  
  // Prevent MIME sniffing
  res.setHeader('X-Content-Type-Options', 'nosniff');
  
  // Clickjacking protection
  res.setHeader('X-Frame-Options', 'DENY');
  
  // Referrer policy
  res.setHeader('Referrer-Policy', 'strict-origin-when-cross-origin');
  
  // Permissions policy
  res.setHeader('Permissions-Policy', 'geolocation=(), microphone=(), camera=()');
  
  next();
});

// Or use helmet.js
const helmet = require('helmet');
app.use(helmet());
```

#### Implementation Order

From [DCHost Guide](https://www.dchost.com/blog/en/http-security-headers-guide-how-to-correctly-set-hsts-csp-x-frame-options-and-referrer-policy/):

1. Enable X-Frame-Options and Referrer-Policy (low-risk, easy wins)
2. Confirm HTTPS is solid (valid certs, redirects, no mixed content)
3. Enable HSTS without preload
4. Introduce CSP in Report-Only mode
5. Tune CSP policies, then switch to enforcing mode

---

### 6. Security Linters and SAST Tools

#### Overview

Source: [Wiz Open-Source Security Tools Guide](https://www.wiz.io/academy/application-security/open-source-code-security-tools)

SAST (Static Application Security Testing) tools check code for known vulnerabilities before runtime. Code linters enforce best practices to prevent known issues in programming languages.

#### Semgrep

Source: [Semgrep GitHub](https://github.com/semgrep/semgrep)

Semgrep is a fast, open-source static analysis tool supporting 30+ languages. It can run in IDEs, as pre-commit checks, and in CI/CD workflows.

From [DevSecOps Pipelines Guide](https://www.johal.in/devsecops-pipelines-semgrep-python-sast-scans-2026/): For 2026 deployments, Semgrep delivers 12s/10k LoC speed, 92% recall accuracy, and can cut vulnerabilities by 70%+.

```bash
# Install
pip install semgrep

# Run with default rules
semgrep --config=auto .

# Run specific rulesets
semgrep --config=p/security-audit .
semgrep --config=p/owasp-top-ten .

# CI-friendly output
semgrep --config=auto --json --output=results.json .
```

```yaml
# .semgrep.yml custom rule example
rules:
  - id: hardcoded-password
    patterns:
      - pattern: password = "..."
    message: "Hardcoded password detected"
    severity: ERROR
    languages: [python]
```

#### Bandit (Python)

Source: [Semgrep Bandit Comparison](https://semgrep.dev/blog/2021/python-static-analysis-comparison-bandit-semgrep/)

Bandit (v1.7.1) ships with 68 security checks for Python.

```bash
# Install
pip install bandit

# Scan directory
bandit -r ./src

# Exclude tests
bandit -r ./src --exclude ./src/tests

# Specific severity
bandit -r ./src -ll  # Medium and above

# Output formats
bandit -r ./src -f json -o bandit-report.json
bandit -r ./src -f sarif -o bandit-report.sarif
```

```ini
# .bandit config file
[bandit]
exclude_dirs = tests,venv
skips = B101,B601
```

**Note** from [GitLab SAST Analyzers](https://github.com/diffblue/gitlab/blob/master/doc/user/application_security/sast/analyzers.md): In GitLab 15.4, Bandit was replaced by Semgrep with GitLab-managed rules for faster scanning and reduced compute usage.

#### Gosec (Go)

Source: [Gosec GitHub](https://github.com/securego/gosec)

Gosec inspects Go source code for security problems by scanning the Go AST.

```bash
# Install
go install github.com/securego/gosec/v2/cmd/gosec@latest

# Scan current module
gosec ./...

# Exclude tests
gosec -exclude-dir=test ./...

# Specific rules only
gosec -include=G101,G102 ./...

# Output formats
gosec -fmt=json -out=results.json ./...
gosec -fmt=sarif -out=results.sarif ./...
```

#### ESLint Security Plugin (JavaScript)

Source: [Aikido Semgrep Alternatives](https://www.aikido.dev/blog/semgrep-alternatives)

```bash
# Install
npm install --save-dev eslint-plugin-security
```

```javascript
// .eslintrc.js
module.exports = {
  plugins: ['security'],
  extends: ['plugin:security/recommended'],
  rules: {
    'security/detect-object-injection': 'error',
    'security/detect-non-literal-regexp': 'warn',
    'security/detect-eval-with-expression': 'error'
  }
};
```

#### Pre-commit Integration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/semgrep/semgrep
    rev: v1.50.0
    hooks:
      - id: semgrep
        args: ['--config', 'auto', '--error']

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ['-r', '-ll']

  - repo: https://github.com/securego/gosec
    rev: v2.18.2
    hooks:
      - id: gosec
```

#### CI/CD Integration Example

```yaml
# GitHub Actions
name: Security Scan
on: [push, pull_request]

jobs:
  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Semgrep Scan
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/secrets
            p/owasp-top-ten

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: semgrep.sarif
```

#### Tool Selection Recommendations

From [SAST Tools Gist](https://gist.github.com/ankitdn/554effe0d895ae542e207db4c0dea301):

Use a hybrid stack approach—running tools like semgrep, bandit, and pylint-security together, then aggregating findings in DefectDojo.

| Language | Recommended Tools |
|----------|------------------|
| Python | Semgrep, Bandit, pip-audit |
| JavaScript | Semgrep, ESLint-security, npm audit |
| Go | Semgrep, Gosec, govulncheck |
| Java | Semgrep, SpotBugs, FindSecBugs |
| Ruby | Semgrep, Brakeman |
| Multi-language | Semgrep, Snyk Code |

---

## Audit Checklist Summary

### Critical (Must Fix Immediately)

- [ ] **No hardcoded secrets** in code, configs, or environment files
- [ ] **Parameterized queries** used for all database operations (no string concatenation)
- [ ] **HTTPS enforced** with valid certificates and HSTS enabled
- [ ] **Authentication tokens** stored in HttpOnly cookies (not localStorage)
- [ ] **Input validation** on server-side for all user inputs
- [ ] **Output encoding** applied contextually (HTML, JavaScript, URL, CSS)
- [ ] **No known critical/high vulnerabilities** in dependencies
- [ ] **CSP header** configured to prevent inline script execution

### Important (Should Fix Soon)

- [ ] **Pre-commit hooks** configured with secret scanning (Gitleaks/TruffleHog)
- [ ] **Dependency scanning** integrated in CI/CD (npm audit, pip-audit, govulncheck)
- [ ] **SAST tools** running in pipeline (Semgrep, Bandit, Gosec as applicable)
- [ ] **Security headers** configured (X-Content-Type-Options, X-Frame-Options, Referrer-Policy)
- [ ] **JWT tokens** have short expiration (15-60 minutes for access tokens)
- [ ] **Session management** includes timeout and secure cookie flags
- [ ] **Least privilege** applied to database and service accounts
- [ ] **Dependabot/Renovate** enabled for automatic security updates
- [ ] **.gitignore** includes sensitive file patterns (.env, credentials, keys)

### Recommended (Best Practice)

- [ ] **Security linters** integrated in IDE (ESLint-security, Bandit VS Code extension)
- [ ] **SBOM generation** for dependency tracking (CycloneDX, SPDX)
- [ ] **Rate limiting** on authentication endpoints
- [ ] **Audit logging** for security-relevant events
- [ ] **Key rotation** strategy documented and automated
- [ ] **CSP report-uri** configured for policy violation monitoring
- [ ] **Permissions-Policy** header restricting browser features
- [ ] **Subresource Integrity (SRI)** for external scripts/styles
- [ ] **CORS** configured restrictively (not `*`)
- [ ] **Error messages** sanitized (no stack traces/internal details to users)
- [ ] **Regular penetration testing** or security audits scheduled

---

## Sources

### Secret Management
- [GitGuardian - API Key Management Best Practices](https://blog.gitguardian.com/secrets-api-management/)
- [GitHub Community - Enforce Secret Detection Discussion](https://github.com/orgs/community/discussions/158668)
- [Jit - Top Git Secrets Scanners 2026](https://www.jit.io/resources/appsec-tools/git-secrets-scanners-key-features-and-top-tools-)
- [OWASP DevSecOps Guideline - Secrets Management](https://owasp.org/www-project-devsecops-guideline/latest/01a-Secrets-Management)
- [Cycode - Best Secrets Management Tools 2026](https://cycode.com/blog/best-secrets-management-tools/)
- [TruffleHog Pre-commit Hooks](https://docs.trufflesecurity.com/pre-commit-hooks)
- [Gitleaks GitHub Repository](https://github.com/gitleaks/gitleaks)

### Dependency Scanning
- [npm Docs - Auditing Dependencies](https://docs.npmjs.com/auditing-package-dependencies-for-security-vulnerabilities/)
- [pip-audit on PyPI](https://pypi.org/project/pip-audit/)
- [pip-audit GitHub Repository](https://github.com/pypa/pip-audit)
- [Go Vulnerability Management](https://go.dev/doc/security/vuln/)
- [govulncheck Documentation](https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck)
- [Semaphore - Vulnerability Scanning with Govulncheck](https://semaphore.io/blog/govulncheck)
- [Shinagawa Labs - Dependency Package Security](https://shinagawa-web.com/en/blogs/dependency-package-security-audit)
- [Snyk vs npm audit Comparison](https://github.com/lirantal/snyk-vs-npm-audit)

### Injection Prevention
- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [PortSwigger - SQL Injection Tutorial](https://portswigger.net/web-security/sql-injection)
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [Salesforce - Prevent XSS and Injection Attacks](https://trailhead.salesforce.com/content/learn/modules/security-principles/prevent-crosssite-scripting-and-injection-attacks)
- [SentinelOne - Code Injection Guide](https://www.sentinelone.com/cybersecurity-101/cybersecurity/code-injection/)

### Authentication and Authorization
- [Curity - JWT Best Practices](https://curity.io/resources/learn/jwt-best-practices/)
- [Frontegg - OAuth vs JWT](https://frontegg.com/blog/oauth-vs-jwt)
- [Stytch - JWTs vs Sessions](https://stytch.com/blog/jwts-vs-sessions-which-is-right-for-you/)
- [LogRocket - JWT Authentication Best Practices](https://blog.logrocket.com/jwt-authentication-best-practices/)
- [Coder Facts - OAuth2 JWT Best Practices](https://coderfacts.com/security-and-best-practices/oauth2-jwt-best-practices/)
- [Leapcell - Auth Methods Comparison](https://leapcell.io/blog/session-jwt-sso-oauth-pros-cons-and-use-cases)
- [Permit.io - JWTs for Authorization](https://www.permit.io/blog/how-to-use-jwts-for-authorization-best-practices-and-common-mistakes)

### Security Headers
- [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)
- [OWASP HTTP Headers Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html)
- [MDN - Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP)
- [MDN - Strict-Transport-Security](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security)
- [MDN - X-Frame-Options](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Frame-Options)
- [OWASP CSP Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html)
- [DCHost - HTTP Security Headers Guide](https://www.dchost.com/blog/en/http-security-headers-guide-how-to-correctly-set-hsts-csp-x-frame-options-and-referrer-policy/)

### SAST Tools
- [Semgrep GitHub Repository](https://github.com/semgrep/semgrep)
- [Semgrep - Python Static Analysis Comparison](https://semgrep.dev/blog/2021/python-static-analysis-comparison-bandit-semgrep/)
- [DevSecOps Pipelines - Semgrep Python SAST 2026](https://www.johal.in/devsecops-pipelines-semgrep-python-sast-scans-2026/)
- [Aikido - Semgrep Alternatives 2026](https://www.aikido.dev/blog/semgrep-alternatives)
- [Wiz - Open-Source Security Tools Guide 2026](https://www.wiz.io/academy/application-security/open-source-code-security-tools)
- [Gosec GitHub Repository](https://github.com/securego/gosec)

### OWASP Resources
- [OWASP Top 10:2025](https://owasp.org/Top10/2025/)
- [OWASP Top 10:2025 Introduction](https://owasp.org/Top10/2025/0x00_2025-Introduction/)
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [OWASP Secure Coding Practices Quick Reference](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/stable-en/02-checklist/05-checklist)
