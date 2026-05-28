# MCP Security Patterns

Security concerns and vulnerability patterns for Model Context Protocol (MCP) implementations.

**Technology**: mcp
**Risk Level**: MEDIUM-HIGH
**Categories**: data_access, code_execution, credential_exposure
**Confidence**: 0.90

## Vulnerability Patterns

### Command Injection

**Severity**: HIGH
**CWE**: CWE-78

MCP servers executing shell commands with user input.

**Patterns**:
- `exec(`
- `spawn(`
- `execSync(`
- `child_process`
- `subprocess.run(`
- `os.system(`
- `shell=True`

### Path Traversal

**Severity**: HIGH
**CWE**: CWE-22

File access without path validation.

**Patterns**:
- `readFile.*$`
- `writeFile.*$`
- `fs.read`
- `fs.write`
- `open(.*+`
- `../`
- `path.join.*$`

### Credential Exposure

**Severity**: MEDIUM
**CWE**: CWE-798

Credentials in MCP configuration.

**Patterns**:
- `api_key`
- `apiKey`
- `secret`
- `password`
- `token`
- `credentials`
- `auth`

**Context**: mcpServers, env, args

### Overprivileged Access

**Severity**: MEDIUM
**CWE**: CWE-250

MCP server with excessive permissions.

**Patterns**:
- `allowedDirectories.*\*`
- `allowedDirectories.*/`
- `rootPath.*/`
- `basePath.*/`
- `command.*sudo`
- `command.*rm`
- `command.*chmod`

## Audit Checklist

- [ ] Review all tool implementations for input validation
- [ ] Check file system access restrictions
- [ ] Verify credential storage is secure
- [ ] Audit command execution paths
- [ ] Review network access capabilities
- [ ] Check for sensitive data in tool responses
- [ ] Verify transport security (stdio vs network)
