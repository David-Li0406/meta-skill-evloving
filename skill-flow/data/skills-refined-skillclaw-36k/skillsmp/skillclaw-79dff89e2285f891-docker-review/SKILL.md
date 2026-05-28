---
name: docker-review
description: Use this skill when you need to analyze Dockerfiles for best practices, security issues, and optimization opportunities.
---

# Docker Review Skill

Analyze Dockerfiles for best practices, security issues, and optimization opportunities.

## Modes

| Mode      | Command            | Purpose                                           |
|-----------|--------------------|---------------------------------------------------|
| Review    | `/docker-review`    | Analyze existing Dockerfile, produce findings report |
| Optimize  | `/docker-optimize`  | Suggest specific changes with before/after comparison |
| Build     | `/docker-build`     | Interactive step-by-step Dockerfile creation     |
| Scan      | `/docker-scan`      | Run security scanners on built images (requires Docker) |

## Review Mode

### Trigger

```
/docker-review [path/to/Dockerfile]
```
If no path is provided, the skill will search for `Dockerfile` in the project root.

### Procedure

1. **Locate Dockerfile**
   - Check the provided path or search common locations.
   - If not found, offer to create one (switches to Build mode).

2. **Static Analysis**
   - Parse Dockerfile instructions.
   - Check against best practices rules (see below).
   - Identify anti-patterns and security issues.

3. **Generate Report**
   - Output to `.agent/docker-review.md`.
   - Categorize findings by severity.
   - Provide fix suggestions for each finding.

### Output Format

```markdown
# Docker Review Report

**File:** Dockerfile  
**Date:** YYYY-MM-DD  
**Base Image:** python:3.11-slim  

## Summary

| Severity | Count |
|----------|-------|
| 🔴 Error | 2     |
| 🟡 Warning | 5    |
| 🔵 Info | 3      |

## Findings

### 🔴 Error: Running as root user

**Line 1-end**  
No USER instruction found. Container will run as root.

**Fix:**
```dockerfile
# Add before CMD/ENTRYPOINT
RUN useradd -r -s /bin/false appuser
USER appuser
```

### 🟡 Warning: Unpinned base image version
...

## Best Practices Rules

### Security (🔴 Error level)

| ID    | Rule                     | Description                                   |
|-------|--------------------------|-----------------------------------------------|
| SEC001| Non-root user            | Container must not run as root                |
| SEC002| No secrets in build      | No passwords, API keys, or tokens in Dockerfile |
| SEC003| COPY over ADD            | Use COPY unless ADD features are needed      |
| SEC004| Minimal base             | Prefer alpine, slim, or distroless images     |

### Optimization (🟡 Warning level)

| ID    | Rule                     | Description                                   |
|-------|--------------------------|-----------------------------------------------|
| OPT001| Pin versions             | Pin base image and package versions           |
...
```