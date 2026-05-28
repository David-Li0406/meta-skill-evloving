---
name: plugin-auditor
description: Use this skill to automatically audit Claude Code plugins for security vulnerabilities, best practices, CLAUDE.md compliance, and quality standards when the user mentions audit plugin, security review, or best practices check.
---

# Plugin Auditor

## Purpose
Automatically audits Claude Code plugins for security vulnerabilities, best practice violations, CLAUDE.md compliance, and quality standards - optimized for claude-code-plugins repository requirements.

## Trigger Keywords
- "audit plugin"
- "security review" or "security audit"
- "best practices check"
- "plugin quality"
- "compliance check"
- "plugin security"

## Audit Categories

### 1. Security Audit

**Critical Checks:**
- ❌ No hardcoded secrets (passwords, API keys, tokens)
- ❌ No AWS keys (AKIA...)
- ❌ No private keys (BEGIN PRIVATE KEY)
- ❌ No dangerous commands (rm -rf /, eval(), exec())
- ❌ No command injection vectors
- ❌ No suspicious URLs (IP addresses, non-HTTPS)
- ❌ No obfuscated code (base64 decode, hex encoding)

**Security Patterns:**
```bash
# Check for hardcoded secrets
grep -r "password\s*=\s*['\"]" --exclude-dir=node_modules
grep -r "api_key\s*=\s*['\"]" --exclude-dir=node_modules
grep -r "secret\s*=\s*['\"]" --exclude-dir=node_modules

# Check for AWS keys
grep -r "AKIA[0-9A-Z]{16}" --exclude=README.md

# Check for private keys
grep -r "BEGIN.*PRIVATE KEY" --exclude=README.md

# Check for dangerous patterns
grep -r "rm -rf /" | grep -v "/var/" | grep -v "/tmp/"
grep -r "eval\s*\(" --exclude=README.md
```

### 2. Best Practices Audit

**Plugin Structure:**
- ✅ Proper directory hierarchy
- ✅ Required files present
- ✅ Semantic versioning (x.y.z)
- ✅ Clear, concise descriptions
- ✅ Proper LICENSE file (MIT/Apache-2.0)
- ✅ Comprehensive README
- ✅ At least 5 keywords

**Code Quality:**
- ✅ No TODO/FIXME without issue links
- ✅ No console.log() in production code
- ✅ No hardcoded paths (/home/, /Users/)
- ✅ Uses `${CLAUDE_PLUGIN_ROOT}` in hooks
- ✅ Scripts have proper shebangs
- ✅ All scripts are executable

**Documentation:**
- ✅ README has installation section
- ✅ README has usage examples
- ✅ README has clear description
- ✅ Commands have proper frontmatter
- ✅ Agents have model specified
- ✅ Skills have trigger keywords

### 3. CLAUDE.md Compliance

**Repository Standards:**
- ✅ Follows plugin structure from CLAUDE.md
- ✅ Uses correct marketplace slug
- ✅ Proper category assignment