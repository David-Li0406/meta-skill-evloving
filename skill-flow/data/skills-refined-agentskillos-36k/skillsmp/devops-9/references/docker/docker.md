# Dockerfile Best Practices

**Category**: devops/docker
**Description**: Dockerfile security and engineering best practices
**CWE**: CWE-250, CWE-798

---

## Security Patterns

### Using Latest Tag
**Pattern**: `(?i)^FROM\s+[^:]+:latest\s*$`
**Type**: regex
**Severity**: medium
**Languages**: [dockerfile]
- Using :latest tag makes builds non-reproducible
- Remediation: Use specific version tags like `FROM node:18.17.0-alpine`

### Running as Root
**Pattern**: `(?i)^USER\s+root\s*$`
**Type**: regex
**Severity**: high
**Languages**: [dockerfile]
- Explicitly running container as root is a security risk
- Remediation: Use a non-root user like `USER nonroot` or `USER 1000`
- CWE-250: Execution with Unnecessary Privileges

### Hardcoded Secret in Dockerfile
**Pattern**: `(?i)(?:PASSWORD|SECRET|API_KEY|TOKEN|PRIVATE_KEY)\s*=\s*['\"]\S+['\"]`
**Type**: regex
**Severity**: critical
**Languages**: [dockerfile]
- Secrets should never be hardcoded in Dockerfiles
- Remediation: Use build-time secrets or runtime environment variables
- CWE-798: Use of Hard-coded Credentials

### Secret in ENV Instruction
**Pattern**: `(?i)^ENV\s+(?:[^\s=]+\s+)?(?:PASSWORD|SECRET|API_KEY|TOKEN|PRIVATE_KEY|AWS_SECRET|GITHUB_TOKEN)`
**Type**: regex
**Severity**: critical
**Languages**: [dockerfile]
- ENV instructions persist secrets in image layers
- Remediation: Use --mount=type=secret for sensitive data

### Using ADD Instead of COPY
**Pattern**: `(?i)^ADD\s+(?!https?://)`
**Type**: regex
**Severity**: low
**Languages**: [dockerfile]
- ADD has implicit tar extraction and URL download
- Remediation: Use COPY for local files: `COPY package.json /app/`

### apt-get Without Cleanup
**Pattern**: `(?i)apt-get\s+install[^&]*(?:$|\\$)`
**Type**: regex
**Severity**: low
**Languages**: [dockerfile]
- Not cleaning apt cache increases image size
- Remediation: Add `&& rm -rf /var/lib/apt/lists/*` after install

### EXPOSE Wildcard Port
**Pattern**: `(?i)^EXPOSE\s+\*`
**Type**: regex
**Severity**: medium
**Languages**: [dockerfile]
- Wildcard EXPOSE may expose unintended ports
- Remediation: Explicitly list required ports: `EXPOSE 80 443`

### Piping to Shell
**Pattern**: `(?i)(?:curl|wget)[^|]*\|\s*(?:bash|sh)`
**Type**: regex
**Severity**: high
**Languages**: [dockerfile]
- Piping untrusted content directly to shell is dangerous
- Remediation: Download, verify, then execute

### COPY with Wildcards
**Pattern**: `(?i)^COPY\s+\*`
**Type**: regex
**Severity**: low
**Languages**: [dockerfile]
- Wildcard COPY may include unintended files
- Remediation: Use specific paths or .dockerignore file

---

## Best Practice Patterns

### Missing HEALTHCHECK
**Pattern**: `HEALTHCHECK`
**Type**: structural
**Severity**: informational
**Languages**: [dockerfile]
- Dockerfile should include HEALTHCHECK instruction
- Remediation: Add `HEALTHCHECK CMD curl -f http://localhost/ || exit 1`

### Missing Non-Root USER
**Pattern**: `USER`
**Type**: structural
**Severity**: high
**Languages**: [dockerfile]
- Dockerfile should specify non-root USER before CMD
- Remediation: Add `USER nonroot` or `USER 1000:1000` before CMD

### Untagged Base Image
**Pattern**: `(?i)^FROM\s+[^:]+\s*$`
**Type**: regex
**Severity**: medium
**Languages**: [dockerfile]
- Using untagged base image defaults to :latest
- Remediation: Always specify a version tag: `FROM node:18`

---

## References

- [CWE-250: Execution with Unnecessary Privileges](https://cwe.mitre.org/data/definitions/250.html)
- [CWE-798: Use of Hard-coded Credentials](https://cwe.mitre.org/data/definitions/798.html)
- [CIS Docker Benchmark](https://www.cisecurity.org/benchmark/docker)
- [Docker Security Best Practices](https://docs.docker.com/develop/security-best-practices/)
