# Linting & Validation of OpenAPI Contracts

## Redocly CLI
Redocly is the industry standard for linting OpenAPI files and generating beautiful documentation.

### 1. Linting
`bun x redocly lint openapi.yaml`

Checks for:
- Syntax errors.
- Missing descriptions/examples.
- Unused components.
- Version mismatches.

---

## Spectral (Custom Rules)
Spectral allows you to enforce organizational "API Style Guides" (e.g., "All endpoints must use camelCase").

### `.spectral.yaml`
```yaml
extends: ["spectral:oas", "spectral:asyncapi"]
rules:
  operation-description: error
  path-keys-camel-case:
    description: All path keys must be camelCase
    severity: error
    given: $.paths[*]~
    then:
      function: pattern
      functionOptions:
        match: "^/([a-z][a-z0-9]*)(/[a-z][a-z0-9]*)*$"
```

---

## CI/CD Integration
Never merge a PR that breaks the API contract.

```yaml
# GitHub Action
- name: Lint OpenAPI Spec
  run: bun x redocly lint openapi.yaml
  
- name: Spectral Check
  run: bun x spectral lint openapi.yaml
```

---

## Visualizing the Contract
Always provide a hosted version of the spec for human review during PRs.
`bun x redocly preview-docs openapi.yaml`
