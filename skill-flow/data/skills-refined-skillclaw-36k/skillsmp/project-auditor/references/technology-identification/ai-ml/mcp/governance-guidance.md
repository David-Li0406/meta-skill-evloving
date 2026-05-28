# MCP Governance and Security Guidance

## Executive Summary

Model Context Protocol (MCP) enables AI assistants to connect to external tools, databases, and services. While powerful, MCP introduces security and governance considerations that organizations must address.

## Risk Assessment

### Data Exposure Risk

MCP servers can expose:
- **File Systems**: Local files, source code, configuration
- **Databases**: Production data, credentials, PII
- **APIs**: Internal services, third-party integrations
- **System Commands**: Shell access, process control

### Attack Surface

| Vector | Risk | Mitigation |
|--------|------|------------|
| Prompt Injection | AI manipulated to access unintended resources | Input validation, least privilege |
| Credential Theft | API keys exposed in configs | Secrets management, rotation |
| Data Exfiltration | Sensitive data sent to AI providers | Data classification, filtering |
| Privilege Escalation | MCP server runs with elevated permissions | Run as unprivileged user |

## Organizational Controls

### Discovery & Inventory

1. **Automated Scanning**: Use phantom to detect MCP usage across repositories
2. **Configuration Audit**: Search for `claude_desktop_config.json` and MCP server configs
3. **Package Monitoring**: Track MCP-related package installations

### Policy Framework

#### Approved MCP Servers

| Server | Purpose | Risk Level | Approval |
|--------|---------|------------|----------|
| mcp-server-filesystem | File access | HIGH | Security review required |
| mcp-server-github | Code access | MEDIUM | Engineering approval |
| mcp-server-time | Current time | LOW | Auto-approved |
| mcp-server-fetch | Web requests | MEDIUM | Network team approval |

#### Prohibited Patterns

- MCP servers with `shell=true` or command execution
- File servers with access to `/`, `~`, or sensitive directories
- Database servers connected to production data
- Servers storing credentials in plain text

### Technical Controls

```yaml
# Example MCP Policy Configuration
mcp_policy:
  allowed_servers:
    - mcp-server-time
    - mcp-server-fetch

  prohibited_capabilities:
    - shell_execution
    - file_write
    - database_write

  required_restrictions:
    file_servers:
      - must_use_allowlist
      - no_parent_traversal
      - sandbox_required

    network_servers:
      - https_only
      - domain_allowlist
```

## Security Checklist

### For Developers

- [ ] MCP server runs with minimum required permissions
- [ ] File access restricted to specific directories
- [ ] All inputs validated and sanitized
- [ ] No credentials hardcoded in configuration
- [ ] Audit logging enabled for all tool calls
- [ ] Network access limited to required domains

### For Security Teams

- [ ] Inventory of all MCP servers in organization
- [ ] Risk assessment for each server type
- [ ] Monitoring for unauthorized MCP installations
- [ ] Incident response plan for MCP-related breaches
- [ ] Regular security reviews of MCP configurations

### For Compliance

- [ ] Data classification for AI-accessible resources
- [ ] Audit trail requirements documented
- [ ] Privacy impact assessment completed
- [ ] Regulatory compliance verified (GDPR, HIPAA, etc.)
- [ ] Third-party AI provider agreements reviewed

## Detection Queries

### Find MCP Usage in Codebase

```bash
# Package detection
phantom.sh hydrate <repo> --quick

# Or manual search
grep -r "@modelcontextprotocol" --include="package.json"
grep -r "from mcp" --include="*.py"
```

### Find MCP Configurations

```bash
# Claude Desktop configs
find . -name "claude_desktop_config.json"

# MCP server manifests
find . -name "mcp.json" -o -name "mcp-config.json"
```

### Audit MCP Server Permissions

```bash
# Check for dangerous patterns
grep -r "exec\|spawn\|shell" mcp-server-*/
grep -r "allowedDirectories.*/" --include="*.json"
```

## Incident Response

### MCP Security Incident Types

1. **Unauthorized Data Access**: AI accessed data beyond intended scope
2. **Credential Exposure**: API keys or secrets leaked through MCP
3. **Command Execution**: Malicious commands executed via MCP server
4. **Data Exfiltration**: Sensitive data sent to external AI service

### Response Steps

1. **Contain**: Disable the MCP server immediately
2. **Assess**: Review audit logs for scope of access
3. **Notify**: Alert affected data owners
4. **Remediate**: Fix vulnerability, rotate credentials
5. **Review**: Update policies and detection rules

## Metrics & Reporting

### Key Metrics

- Number of MCP servers deployed
- MCP servers by risk category
- Data types accessible via MCP
- Unauthorized MCP installation attempts
- Security findings from MCP audits

### Reporting Template

```markdown
## MCP Security Report - [Date]

### Inventory
- Total MCP Servers: X
- High Risk: X | Medium Risk: X | Low Risk: X

### Findings
- New MCP servers detected: X
- Policy violations: X
- Security vulnerabilities: X

### Actions
- Servers requiring review: [list]
- Remediation in progress: [list]
- Policy updates needed: [list]
```

## Additional Resources

- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [MCP Security Best Practices](https://modelcontextprotocol.io/docs/security)
- [Anthropic Claude Security](https://www.anthropic.com/security)
