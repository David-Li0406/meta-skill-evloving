---
name: security-review
description: This skill should be used when the user asks to "security review", "check for vulnerabilities", "audit security", "find security issues", "security scan", "check for injection", "find hardcoded secrets", "OWASP check", or mentions reviewing code specifically for security concerns.
version: 3.1.1
---

# Security Code Review Skill

Identify vulnerabilities, insecure coding patterns, and security misconfigurations through targeted security-focused code review.

## When to Use

Use this skill to:
- Audit code for security vulnerabilities
- Detect injection attacks (SQL, command, XSS)
- Find hardcoded secrets and credentials
- Verify authentication and authorization
- Analyze cryptographic implementations
- Assess input validation coverage

## Process Overview

1. **Determine scope** - Identify code requiring security review
2. **Gather context** - Collect project type, AI instructions, and related code
3. **Launch security agent** - Execute thorough mode, then gaps mode
4. **Validate findings** - Filter false positives from results
5. **Report results** - Generate severity-prioritized output with fixes

For detailed procedures on steps 1, 2, 4, and 5, see `${CLAUDE_PLUGIN_ROOT}/shared/skill-common-workflow.md`.

---

## Security-Specific Configuration

### Agent Parameters

- **Agent:** `${CLAUDE_PLUGIN_ROOT}/agents/security-agent.md`
- **Model:** Opus (for thorough vulnerability detection)
- **Modes:** thorough (first pass), gaps (second pass)

### Security Categories Checked

**Injection Vulnerabilities (Critical):**
- SQL injection via string concatenation
- Command injection through shell execution
- XSS via unescaped HTML output
- Template injection, LDAP injection

**Authentication & Authorization (Critical):**
- Missing authentication on endpoints
- Broken access control (IDOR)
- Session management weaknesses
- Missing CSRF protection

**Sensitive Data Exposure (Critical):**
- Hardcoded secrets, API keys, passwords
- Sensitive data in logs
- Unencrypted data transmission
- Excessive data exposure in APIs

**Cryptographic Issues (Major):**
- Weak hashing (MD5, SHA1 for passwords)
- Insecure random number generation
- Missing encryption for sensitive data

**Input Validation (Major):**
- Path traversal vulnerabilities
- ReDoS (regex denial of service)
- Unsafe deserialization
- Missing input sanitization

---

## Auto-Validated Patterns

These high-confidence patterns skip validation:

| Pattern | Description |
|---------|-------------|
| `hardcoded_password` | `password = "..."` assignments |
| `hardcoded_api_key` | `api_key = "..."` assignments |
| `sql_injection_concat` | SQL + string concatenation with user input |
| `eval_untrusted` | `eval()` with request/user input |

---

## Scope Prioritization

When reviewing directories, automatically prioritize:
- Files with "auth", "login", "password", "api", "db" in names
- Configuration files (`config/*.ts`, `appsettings.json`)
- Environment handling (`.env.example`, environment loading code)
- Middleware and interceptor definitions

---

## Security-Specific False Positives

Do NOT flag:
- Security issues in test files (usually intentional)
- Internal-only code with no untrusted input exposure
- Code with explicit security comments explaining design
- Placeholder values (`"changeme"`, `"TODO"`)
- Vulnerabilities already mitigated elsewhere

---

## OWASP Top 10 Quick Reference

| OWASP Category | Key Patterns |
|----------------|--------------|
| A01 Broken Access Control | Missing authz checks, IDOR, directory traversal |
| A02 Cryptographic Failures | Weak hashing, missing encryption, hardcoded keys |
| A03 Injection | SQL concat, eval(), exec(), template injection |
| A04 Insecure Design | Missing rate limits, business logic flaws |
| A05 Security Misconfiguration | Debug enabled, default credentials, verbose errors |
| A06 Vulnerable Components | Outdated dependencies (check with npm audit, dotnet list) |
| A07 Auth Failures | Missing session validation, weak passwords |
| A08 Data Integrity Failures | Unsafe deserialization, unsigned data |
| A09 Logging Failures | Missing audit logs, logging sensitive data |
| A10 SSRF | Unvalidated URL fetching, internal service access |

---

## Example Output

See `examples/example-output.md` for a sample showing:
- SQL injection finding with diff fix
- Hardcoded API key with prompt fix
- Missing rate limiting with prompt fix

---

## Additional Resources

### Reference Files

For detailed vulnerability patterns:
- **`references/common-vulnerabilities.md`** - OWASP vulnerabilities, injection patterns, auth issues, crypto problems

### Related Components

- **Agent Definition:** `${CLAUDE_PLUGIN_ROOT}/agents/security-agent.md`
- **Subagent Type:** `code-review:security-agent` (for Task tool invocation)
- **Language checks:** `${CLAUDE_PLUGIN_ROOT}/languages/nodejs.md`, `${CLAUDE_PLUGIN_ROOT}/languages/dotnet.md`
- **Common workflow:** `${CLAUDE_PLUGIN_ROOT}/shared/skill-common-workflow.md`
