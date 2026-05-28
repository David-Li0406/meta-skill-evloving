**Skill**: [Skill Architecture](../SKILL.md)

## Part 3: Security (Critical)

### 🚨 Security Threats

**1. Prompt Injection Attacks**

- Malicious input tricks Agent Skill into executing unintended actions
- **Recent CVEs**: CVE-2025-54794 (path bypass), CVE-2025-54795 (command injection)
- **Defense**: Validate inputs, use `allowed-tools` to restrict capabilities

**2. Tool Abuse**

- Adversary manipulates Agent Skill to run unsafe commands or exfiltrate data
- **Defense**: Minimize tool power, require confirmations for high-impact actions

**3. Data Exfiltration**

- Agent Skill could be tricked into leaking sensitive files
- **Defense**: Never hardcode secrets, use `allowed-tools` to block network commands

### Security Best Practices

**DO:**

- ✅ Run Claude Code in sandboxed environment (VM/container)
- ✅ Use `allowed-tools` to restrict dangerous tools (block WebFetch, Bash curl/wget)
- ✅ Validate all user inputs before file operations
- ✅ Use deny-by-default permission configs
- ✅ Audit downloaded Agent Skills before enabling
- ✅ Red-team test for prompt injection

**DON'T:**

- ❌ Hardcode API keys, passwords, or secrets in SKILL.md
- ❌ Run as root
- ❌ Trust Agent Skills from unknown sources
- ❌ Use unchecked `sudo` or `rm -rf` operations
- ❌ Enable all tools by default

### Security Example

**Insecure Agent Skill**:

```yaml
---
name: unsafe-api
description: Calls API with hardcoded key
---
API_KEY = "sk-1234..." # ❌ NEVER DO THIS
```

**Secure Agent Skill**:

```yaml
---
name: safe-api
description: Calls API using environment variables
allowed-tools: Read, Bash # Blocks WebFetch to prevent data exfiltration
---
# Safe API Client
Use environment variable $API_KEY from user's shell.
Validate all inputs before API calls.
```
