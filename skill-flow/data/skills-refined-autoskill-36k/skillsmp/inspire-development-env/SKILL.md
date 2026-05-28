---
name: inspire-development-env
description: Inspire team development environment setup, local configuration, and troubleshooting guides. Use when setting up dev environment or debugging local issues.
user-invocable: false
allowed-tools: Read
---

# Inspire Team Development Environment Context

When this skill is activated, load the following development environment documentation:

## Required Context Files

Read these files to understand the Inspire team's dev environment:

1. **Environment Overview**: `./references/env-overview.md`
   - Environment types (dev, staging, prod)
   - Infrastructure overview
   - Access requirements

2. **Local Setup**: `./references/local-setup.md`
   - Prerequisites
   - Installation steps
   - Configuration

3. **Troubleshooting**: `./references/troubleshooting.md`
   - Common issues
   - Debug techniques
   - Known workarounds

## Instructions

Before responding to dev environment questions:
1. Use the Read tool to load relevant files above
2. Follow the team's setup procedures
3. Reference troubleshooting guides for common issues

## When to Load This Context

- Setting up local development
- Debugging environment issues
- Onboarding new team members
- Configuring CI/CD pipelines
