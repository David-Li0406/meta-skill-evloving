---
name: yaml-master
description: Use this skill when working with YAML files, configuration management, or CI/CD pipelines to automatically validate, convert, and infer schemas without needing explicit commands.
---

# YAML Master Agent

**⚡ This skill activates AUTOMATICALLY when you work with YAML files!**

## Automatic Trigger Conditions

This skill proactively activates when Claude detects:

1. **File Operations**: Reading, writing, or editing `.yaml` or `.yml` files
2. **Configuration Management**: Working with Ansible, Kubernetes, Docker Compose, GitHub Actions
3. **CI/CD Workflows**: GitLab CI, CircleCI, Travis CI, Azure Pipelines configurations
4. **Schema Validation**: Validating configuration files against schemas
5. **Format Conversion**: Converting between YAML, JSON, TOML, XML formats
6. **User Requests**: Explicit mentions of "yaml", "validate yaml", "fix yaml syntax", "convert yaml"

**No commands needed!** Just work with YAML files naturally, and this skill activates automatically.

---

## Core Capabilities

### 1. Intelligent YAML Validation

**What It Does**:
- Detects syntax errors (indentation, duplicate keys, invalid scalars)
- Validates against YAML 1.2 specification
- Identifies common anti-patterns (tabs vs spaces, anchors/aliases issues)
- Provides detailed error messages with line numbers and fix suggestions

**Example**:
```yaml
# ❌ INVALID YAML
services:
  web:
    image: nginx
	  ports:  # Mixed tabs and spaces - ERROR!
      - "80:80"
```

**Agent Action**: Automatically detects mixed indentation, suggests fix:
```yaml
# ✅ FIXED YAML
services:
  web:
    image: nginx
    ports:  # Consistent 2-space indentation
      - "80:80"
```

### 2. Schema Inference & Generation

**What It Does**:
- Analyzes YAML structure and infers JSON Schema
- Generates OpenAPI/Swagger schemas from YAML
- Creates type definitions for TypeScript/Python from YAML configs
- Validates instances against inferred or provided schemas

**Example**:
```yaml
# Input YAML
user:
  name: Jeremy
  age: 35
  roles:
    - admin
    - developer
```

**Agent Action**: Infers schema:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "user": {
      "type": "object",
      "properties": {
        "name": { "type": "string" },
        "age": { "type": "integer" },
        "roles": { "type": "array", "items": { "type": "string" } }
      }
    }
  }
}
```