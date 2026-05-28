---
name: github-actions-testing
description: Use this skill when you need expert guidance for testing and validating GitHub Actions workflows before deployment, ensuring that common CI failures are caught early.
---

# Skill body

## Capabilities

This skill provides:

1. **Pre-Push Validation**: Complete workflow validation before pushing to GitHub.
2. **Cache Configuration**: Ensure cache-dependency-path is correctly specified.
3. **Monorepo Build Order**: Validate workspace dependency build sequences.
4. **Service Container Setup**: Guide proper service container configuration.
5. **Path Validation**: Verify all paths exist and are accessible.
6. **Local Testing**: Run workflows locally with act (Docker-based simulation).
7. **Static Analysis**: Lint workflows with actionlint and yamllint.

## When to Use This Skill

Invoke this skill when:
- Creating or modifying GitHub Actions workflows.
- Debugging workflow failures in CI.
- Setting up new repositories with CI/CD.
- Migrating to monorepo architecture.
- Adding service containers to workflows.
- Experiencing cache-related failures.
- Getting "module not found" errors in CI but not locally.

## Usage

### Quick Validation

"Validate my GitHub Actions workflows before I push"

I'll:
1. Run actionlint on all workflow files.
2. Check for missing cache-dependency-path configurations.
3. Validate all working-directory paths exist.
4. Verify monorepo build order is correct.
5. Check service container configurations.
6. Provide a pre-push checklist.

### Debugging Workflow Failures

"My GitHub Actions workflow is failing with [error message]"

I'll:
1. Analyze the error message.
2. Identify the root cause.
3. Explain why local testing didn't catch it.
4. Provide the correct configuration.
5. Show how to test the fix locally.

### Setup New Repository

"Set up GitHub Actions testing for my new project"

I'll:
1. Install required tools (act, actionlint, yamllint).
2. Create validation scripts.
3. Set up pre-push hooks.
4. Configure recommended workflows.
5. Provide testing procedures.

## Critical Rules I Enforce

### 1. Cache Configuration

**ALWAYS specify cache-dependency-path explicitly:**

```yaml
# Example configuration
```