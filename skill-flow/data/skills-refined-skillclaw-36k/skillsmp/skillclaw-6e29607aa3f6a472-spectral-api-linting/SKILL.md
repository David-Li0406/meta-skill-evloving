---
name: spectral-api-linting
description: Use this skill when configuring Spectral for API linting, creating custom rulesets, and validating OpenAPI specifications.
---

# Skill body

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
     # Critical rules (errors)
     oas3-valid-schema-example: error
     operation-operationId: error
     operation-success-response: error

     # Important rules (warnings)
     operation-description: warn
     operation-tags: warn
     info-description: error
   ```

3. **Zero Errors Before Merge**  
   - ❌ API specs with linting errors CANNOT be merged.
   - ⚠️ Warnings should be fixed but don't block merge.
   - ℹ️ Info-level issues are optional.

### 🟡 STANDARD RULES

**Standard .spectral.yml Template:**

```yaml
# .spectral.yml - OpenAPI linting configuration

extends: spectral:oas

rules:
  # ========================================
  # Critical Rules (error = must fix)
  # ========================================

  oas3-valid-schema-example: error
  operation-operationId: error
  operation-success-response: error
  operation-tag-defined: error
  info-description: error

  # ========================================
  # Important Rules (warn = should fix)
  # ========================================

  operation-description: warn
  operation-tags: warn
  operation-parameters: warn
  path-keys-no-trailing-slash: warn

  # ========================================
  # Optional Rules (info = nice to have)
  # ========================================

  info-contact: info
  info-license: info
```

### Custom Rules

You can create custom rules in your `.spectral.yml`:

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
    given: $.paths[*]~
    then:
      function: pattern
      functionOptions:
        match: "^(/[a-z0-9-]+)+$"
```

### CLI Usage

To lint your OpenAPI specifications, use the following commands:

```bash
spectral lint openapi.yaml
spectral lint openapi.yaml --ruleset .spectral.yml
spectral lint openapi.yaml -f json  # JSON output
```

### Built-in Functions

Spectral provides several built-in functions for validation:

- `truthy` / `falsy` - Value exists / is empty
- `pattern` - Regex matching
- `length` - String/array length constraints
- `enumeration` - Value in allowed list
- `schema` - Validate against JSON Schema
- `alphabetical` - Keys in order
- `undefined` - Property must not exist