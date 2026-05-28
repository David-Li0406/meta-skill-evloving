---
name: inspire-security-compliance
description: Inspire team security guidelines and secrets management. Use when handling sensitive data, authentication, or security reviews.
user-invocable: false
allowed-tools: Read
---

# Inspire Team Security & Compliance Context

When this skill is activated, load the following security documentation:

## Required Context Files

Read these files to understand the Inspire team's security practices:

1. **Security Guidelines**: `./references/security-guidelines.md`
   - Security best practices
   - Common vulnerabilities to avoid
   - Authentication/authorization patterns

2. **Secrets Management**: `./references/secrets-management.md`
   - How to handle secrets
   - Secret storage solutions
   - Rotation policies

## Instructions

Before responding to security questions:
1. Use the Read tool to load relevant files above
2. Follow the team's security guidelines
3. Never expose sensitive information

## When to Load This Context

- Implementing authentication
- Handling sensitive data
- Security code reviews
- Compliance requirements
