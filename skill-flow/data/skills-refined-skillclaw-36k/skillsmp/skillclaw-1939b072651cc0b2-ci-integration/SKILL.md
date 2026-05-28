---
name: ci-integration
description: Use this skill when setting up CI/CD integration with GitHub Actions for various services, including automated testing and deployment.
---

# CI Integration

## Overview
Set up CI/CD pipelines for various integrations with automated testing using GitHub Actions.

## Prerequisites
- GitHub repository with Actions enabled
- Relevant test API key for the service
- npm/pnpm project configured

## Instructions

### Step 1: Create GitHub Actions Workflow
Create a workflow file in `.github/workflows/{service}-integration.yml`:

```yaml
name: {Service} Integration Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  {SERVICE_API_KEY}: ${{ secrets.{SERVICE_API_KEY} }}

jobs:
  test:
    runs-on: ubuntu-latest
    env:
      {SERVICE_API_KEY}: ${{ secrets.{SERVICE_API_KEY} }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm test -- --coverage
      - run: npm run test:integration
```

### Step 2: Configure Secrets
Set the API key as a GitHub secret:

```bash
gh secret set {SERVICE_API_KEY} --body "sk_test_***"
```

### Step 3: Add Integration Tests
Add integration tests in your test suite:

```typescript
describe('{Service} Integration', () => {
  it.skipIf(!process.env.{SERVICE_API_KEY})('should connect', async () => {
    const client = get{Service}Client();
    const result = await client.healthCheck();
    expect(result.status).toBe('ok');
  });
});
```

## Output
- Automated test pipeline
- PR checks configured
- Coverage reports uploaded
- Release workflow ready

## Error Handling
| Issue | Cause | Solution |
|-------|-------|----------|
| Secret not found | Missing configuration | Add secret via `gh secret set` |
| Tests timeout | Network issues | Increase timeout or mock |
| Auth failures | Invalid key | Check secret value |

## Examples

### Release Workflow
```yaml
on:
  push:
    tags: ['v*']

jobs:
  release:
    runs-on: ubuntu-latest
    env:
      {SERVICE_API_KEY}: ${{ secrets.{SERVICE_API_KEY}_PROD }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - name: Verify {Service} production readiness
        run: npm run test:int
```

## Resources
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Relevant Service CI Guide](https://example.com)