---
name: security
description: Run security scans and vulnerability analysis using Gemini's security extension. Scan dependencies, generate PoCs, and document findings.
allowed-tools: Bash, Read, Glob, Write
user-invocable: true
proactive: false
---

# Security Review

Run security scans and vulnerability analysis using Gemini CLI's security extension. Supports dependency scanning, vulnerability PoC generation, and security note documentation.

## Usage

```
/security scan <path>           # Full security scan of directory
/security deps                  # Scan dependencies for known CVEs
/security poc <vulnerability>   # Generate PoC for a vulnerability
/security note <finding>        # Document a security finding
```

## Available Commands

### Branch Analysis

Analyze code changes on the current branch for security issues:

```bash
gemini -e security "security:analyze"
```

This compares your current branch against the base branch and scans all changes for:
- Common security vulnerabilities
- Privacy violations
- Injection flaws
- Authentication issues

Best used after making changes, before committing or opening a PR.

### GitHub PR Analysis

For CI/CD integration with GitHub Actions:

```bash
gemini -e security "security:analyze-github-pr"
```

Only for use with the `run-gemini-cli` GitHub Action. Analyzes PR diffs automatically.

### Dependency Scanning

Scan project dependencies for known vulnerabilities (CVEs):

```bash
gemini -e security "scan_deps"
gemini -e security "security:scan_deps"
```

Run from the project root or specify a path. Checks:
- Python: `requirements.txt`, `pyproject.toml`, `setup.py`
- Node: `package.json`, `package-lock.json`
- Other package managers as supported

### Security Notes

Create or append to security documentation:

```bash
gemini -e security "security:note-adder <description>"
```

Use this to document:
- Identified vulnerabilities
- Risk assessments
- Remediation recommendations
- False positive notes

### Proof of Concept Generation

**[Experimental]** Generate a PoC for a specific vulnerability:

```bash
gemini -e security "security:poc <vulnerability_description>"
```

Use responsibly for:
- Validating reported vulnerabilities
- Testing remediation effectiveness
- Security research and education

## Workflow

### Quick Dependency Check

```
/security deps
```

Runs `scan_deps` on the current project and reports any known CVEs.

### Full Directory Review

```
/security scan sentinel-campaign
```

1. Scans dependencies in the target directory
2. Analyzes code for common vulnerability patterns:
   - Injection flaws (SQL, command, path traversal)
   - Authentication/authorization issues
   - Sensitive data exposure
   - Insecure deserialization
   - SSRF, XSS, CSRF patterns
3. Documents findings with `security:note-adder`

### Investigate Specific Vulnerability

```
/security poc "path traversal in wiki_adapter.py update_wiki function"
```

Generates a proof-of-concept to validate the vulnerability.

## Step-by-Step: Full Scan

1. **Scan dependencies first:**
   ```bash
   gemini -e security "scan_deps"
   ```

2. **Review code for patterns:**
   Ask Gemini to analyze specific files or directories:
   ```bash
   gemini -e security "Review sentinel-campaign/src/sentinel_campaign/tools/ for security vulnerabilities including injection, path traversal, and access control issues"
   ```

3. **Document findings:**
   ```bash
   gemini -e security "security:note-adder Found potential path traversal in update_wiki - user input used in file path without validation"
   ```

4. **Generate PoC if needed:**
   ```bash
   gemini -e security "security:poc path traversal in update_wiki allowing arbitrary file write"
   ```

## SENTINEL-Specific Targets

Priority areas for security review:

| Component | Risk Areas |
|-----------|------------|
| `sentinel-campaign/src/sentinel_campaign/tools/` | MCP tool handlers accept external input |
| `sentinel-campaign/src/sentinel_campaign/resources/` | Resource handlers, file reads |
| `sentinel-agent/src/state/manager.py` | Campaign state persistence |
| `sentinel-agent/src/state/wiki_adapter.py` | Wiki file operations |
| `sentinel-agent/src/tools/registry.py` | Tool handler implementations |
| `scripts/create_character.py` | YAML file writes from user input |

### Common Patterns to Check

1. **Path Traversal:** Any file path built from user input
2. **Command Injection:** Subprocess calls with user data
3. **YAML/JSON Deserialization:** Loading untrusted data
4. **MCP Tool Input:** All tool parameters from external callers
5. **Wiki Overlays:** Campaign-specific file writes

## Output Location

Security notes are typically saved to:
- `security-notes/` in the project root
- Or specify a custom location

## Example Session

```
User: /security scan sentinel-campaign

Claude: Running security scan on sentinel-campaign...

1. Dependency scan:
   [runs gemini -e security "scan_deps" in sentinel-campaign/]

2. Code review:
   [runs gemini -e security "Review the MCP server tools for injection and access control vulnerabilities"]

3. Findings documented to security-notes/

Results:
- 0 known CVEs in dependencies
- 2 potential issues identified:
  - wiki.py:45 - path construction from user input
  - tools.py:123 - campaign_id used without validation
```

## Integration with /council

For architecture-level security review, combine with `/council`:

```
/council "Review the security architecture of sentinel-campaign MCP server"
```

This gets perspectives from multiple AI agents on the overall security design.
