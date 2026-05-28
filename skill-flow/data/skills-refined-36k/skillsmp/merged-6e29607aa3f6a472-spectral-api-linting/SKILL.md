---
name: spectral-api-linting
description: Use this skill when configuring Spectral for API linting, creating custom rulesets, and validating OpenAPI or AsyncAPI specifications.
---

# Spectral API Linting

## Quick Start

```yaml
# .spectral.yml
extends: spectral:oas
rules:
  operation-operationId: error
  info-contact: warn
  oas3-api-servers: off
```

## Core Concepts

- **Rulesets**: Collections of rules; extend built-in (`spectral:oas`, `spectral:asyncapi`).
- **Severity**: `error`, `warn`, `info`, `hint`, or `off` to disable.
- **Given**: JSONPath expression targeting what to validate.
- **Then**: Functions and conditions to check.

## API Linting Configuration

### 🚨 CRITICAL RULES

1. **Use Spectral for OpenAPI Linting**  
   All `api.yml` files MUST be linted with Spectral before merge.

   **Install Spectral:**
   ```bash
   npm install -g @stoplight/spectral-cli
   # or use npx
   npx @stoplight/spectral-cli lint api.yml
   ```

2. **Minimum .spectral.yml Configuration**  
   Every module SHOULD have a `.spectral.yml` file in the module root:

   ```yaml
   extends: spectral:oas

   rules:
     oas3-valid-schema-example: error
     operation-operationId: error
     operation-success-response: error
   ```

3. **Zero Errors Before Merge**  
   - ❌ API specs with linting errors CANNOT be merged.
   - ⚠️ Warnings should be fixed but don't block merge.
   - ℹ️ Info-level issues are optional.

### 🟡 STANDARD RULES

**Standard .spectral.yml Template:**

```yaml
extends: spectral:oas

rules:
  oas3-valid-schema-example: error
  operation-operationId: error
  operation-success-response: error
  operation-description: warn
  operation-tags: warn
  info-description: error
```

### Custom Rules

**Add custom rules for project-specific requirements:**

```yaml
rules:
  must-have-description:
    description: All operations must have descriptions
    given: $.paths[*][get,post,put,patch,delete]
    severity: error
    then:
      field: description
      function: truthy

  path-must-be-kebab-case:
    given: $.paths[*]
    then:
      function: pattern
      functionOptions:
        match: "^(/[a-z0-9-]+)+$"
```

### Built-in Functions

- `truthy` / `falsy` - Value exists / is empty.
- `pattern` - Regex matching.
- `length` - String/array length constraints.
- `enumeration` - Value in allowed list.
- `schema` - Validate against JSON Schema.

## Running Spectral

**Basic usage:**
```bash
# Lint single file
npx @stoplight/spectral-cli lint api.yml

# Lint with custom config
npx @stoplight/spectral-cli lint -r .spectral.yml api.yml

# Output formats
npx @stoplight/spectral-cli lint api.yml -f json
npx @stoplight/spectral-cli lint api.yml -f html > report.html

# Lint multiple files
npx @stoplight/spectral-cli lint **/*.yml
```

## Validation

### Complete Validation Script
```bash
#!/bin/bash
# validate-spectral.sh - Validate Spectral configuration and run linting

echo "=== Spectral API Linting Validation ==="
echo ""

ERRORS=0

# Check .spectral.yml exists
if [ -f .spectral.yml ]; then
  echo "✅ .spectral.yml exists"
else
  echo "⚠️ No .spectral.yml (using default rules)"
fi

# Check Spectral is available
if command -v spectral &> /dev/null; then
  echo "✅ Spectral installed"
else
  echo "❌ Spectral not available (install with: npm install -g @stoplight/spectral-cli)"
  ERRORS=$((ERRORS + 1))
fi

# Run lint on api.yml
if [ -f api.yml ]; then
  echo "Found api.yml, running lint..."
  if npx @stoplight/spectral-cli lint api.yml; then
    echo "✅ API spec passes linting"
  else
    echo "❌ API spec has linting errors"
    ERRORS=$((ERRORS + 1))
  fi
else
  echo "⚠️ No api.yml found to lint"
fi

# Summary
if [ $ERRORS -eq 0 ]; then
  echo "=== ✅ VALIDATION PASSED ==="
else
  echo "=== ❌ VALIDATION FAILED ($ERRORS errors) ==="
fi
```

## Common Issues

### Issue: Spectral not found
**Solution:**
```bash
npm install -g @stoplight/spectral-cli
```

### Issue: Valid spec fails linting
**Common causes:**
1. Example doesn't match schema.
2. Missing operationId.
3. Missing success response.

**Fix:**
```yaml
paths:
  /users:
    get:
      operationId: listUsers
      responses:
        '200':
          description: Success
```

## Integration

### Pre-commit Hook
```bash
# .git/hooks/pre-commit
#!/bin/bash

if [ -f api.yml ]; then
  echo "Linting API spec..."
  if ! npx @stoplight/spectral-cli lint api.yml; then
    echo "❌ API linting failed. Fix errors before committing."
    exit 1
  fi
fi
```

### GitHub Actions
```yaml
# .github/workflows/lint-api.yml
name: Lint API Spec

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - name: Lint API
        run: npx @stoplight/spectral-cli lint api.yml
```