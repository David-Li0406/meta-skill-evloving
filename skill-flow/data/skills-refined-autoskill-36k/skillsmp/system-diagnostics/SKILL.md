---
name: system-diagnostics
description: How to gather and analyze system information for debugging
tags: [system, diagnostics, debugging, environment]
---

# System Diagnostics Skill

Use this skill when you need to understand the local system environment,
debug environment-related issues, or gather system information.

## When to Use

- Debugging environment-specific issues
- Understanding system capabilities
- Checking available resources (memory, disk, etc.)
- Verifying tool installations

## Available Information

The `system-info` tool provides:

1. **Operating System**: OS type, version, architecture
2. **Python Environment**: Version, interpreter path, virtual env
3. **Resource Availability**: Memory, disk space
4. **Environment Variables**: Key config values

## Best Practices

1. **Check environment first**: When debugging, start by gathering system info
2. **Compare environments**: Use this to identify differences between dev/prod
3. **Document requirements**: Use gathered info to document system requirements
