---
name: validation-patterns
description: "Validation patterns and compliance checking for Kailash SDK including parameter validation, DataFlow pattern validation, connection validation, absolute import validation, workflow structure validation, and security validation. Use when asking about 'validation', 'validate', 'check compliance', 'verify', 'lint', 'code review', 'parameter validation', 'connection validation', 'import validation', 'security validation', or 'workflow validation'."
---

# Kailash Validation Patterns

Comprehensive validation patterns and compliance checking for Kailash SDK development.

## Overview

Validation tools and patterns for:
- Parameter validation
- DataFlow pattern compliance
- Connection validation
- Absolute import checking
- Workflow structure validation
- Security validation

## Reference Documentation

### Core Validations

#### Parameter Validation
- **[validate-parameters](validate-parameters.md)** - Node parameter validation
  - Required parameters checking
  - Type validation
  - Value range validation
  - Format validation
  - Default value handling

#### Connection Validation
- **[validate-connections](validate-connections.md)** - Connection validation
  - 4-parameter format check
  - Source/target node existence
  - Parameter name validation
  - Type compatibility
  - Circular dependency detection

#### Workflow Structure
- **[validate-workflow-structure](validate-workflow-structure.md)** - Workflow validation
  - Node ID uniqueness
  - Connection validity
  - Dead-end detection
  - Entry point validation
  - Exit point validation

### Framework-Specific Validations

#### DataFlow Patterns
- **[validate-dataflow-patterns](validate-dataflow-patterns.md)** - DataFlow compliance
  - Result access pattern: `results["node_id"]["result"]`
  - String ID preservation
  - Multi-instance isolation
  - Transaction patterns
  - Model decorator usage

#### Absolute Imports
- **[validate-absolute-imports](validate-absolute-imports.md)** - Import validation
  - Absolute vs relative imports
  - Module path correctness
  - Circular import detection
  - Missing import detection

#### Security Validation
- **[validate-security](validate-security.md)** - Security checks
  - Secret exposure
  - SQL injection risks
  - Code injection risks
  - File path traversal
  - API key handling

## Validation Patterns

### Parameter Validation Pattern

```python
def validate_node_parameters(node_type: str, params: dict) -> bool:
    """Validate node parameters."""
    required = NODE_REQUIREMENTS[node_type]

    # Check required parameters
    for param in required:
        if param not in params:
            raise ValueError(f"Missing required parameter: {param}")

    # Check types
    for param, value in params.items():
        expected_type = PARAM_TYPES[node_type][param]
        if not isinstance(value, expected_type):
            raise TypeError(f"Invalid type for {param}")

    return True
```

### Connection Validation Pattern

```python
def validate_connection(workflow, source_id, source_param,
                       target_id, target_param) -> bool:
    """Validate 4-parameter connection."""
    # Check nodes exist
    if source_id not in workflow.nodes:
        raise ValueError(f"Source node {source_id} not found")
    if target_id not in workflow.nodes:
        raise ValueError(f"Target node {target_id} not found")

    # Check parameters exist
    source_node = workflow.nodes[source_id]
    if source_param not in source_node.outputs:
        raise ValueError(f"Source param {source_param} not found")

    target_node = workflow.nodes[target_id]
    if target_param not in target_node.inputs:
        raise ValueError(f"Target param {target_param} not found")

    return True
```

### DataFlow Pattern Validation

```python
def validate_dataflow_result_access(code: str) -> bool:
    """Validate DataFlow result access pattern."""
    # ✅ CORRECT: results["node_id"]["result"]
    correct_pattern = r'results\[["\']\w+["\']\]\[["\'](result|data)["\']\]'

    # ❌ WRONG: results["node_id"].result
    wrong_pattern = r'results\[["\']\w+["\']\]\.\w+'

    if re.search(wrong_pattern, code):
        raise ValueError("Use results[id]['result'], not results[id].result")

    if not re.search(correct_pattern, code):
        warnings.warn("Consider using standard result access pattern")

    return True
```

### Security Validation Pattern

```python
def validate_security(workflow) -> list[str]:
    """Run security validations."""
    issues = []

    for node_id, node in workflow.nodes.items():
        # Check for hardcoded secrets
        if has_hardcoded_secrets(node.params):
            issues.append(f"{node_id}: Hardcoded secrets detected")

        # Check for SQL injection risks
        if node.type == "SQLQueryNode":
            if has_sql_injection_risk(node.params.get("query", "")):
                issues.append(f"{node_id}: SQL injection risk")

        # Check for code injection
        if node.type == "PythonCodeNode":
            if has_code_injection_risk(node.params.get("code", "")):
                issues.append(f"{node_id}: Code injection risk")

    return issues
```

## Validation Checklists

### Pre-Execution Checklist
- [ ] All required parameters provided
- [ ] All connections use 4-parameter format
- [ ] No missing node IDs
- [ ] No duplicate node IDs
- [ ] All referenced nodes exist
- [ ] No circular dependencies
- [ ] Called .build() before execute
- [ ] Using correct runtime type

### DataFlow Checklist
- [ ] Result access uses `results["id"]["result"]` pattern
- [ ] String IDs preserved (no UUID conversion)
- [ ] One DataFlow instance per database
- [ ] Deferred schema operations enabled
- [ ] Transaction boundaries correct
- [ ] Model decorators properly applied

### Security Checklist
- [ ] No hardcoded secrets
- [ ] No SQL injection risks
- [ ] No code injection risks
- [ ] No file path traversal risks
- [ ] API keys from environment
- [ ] Sensitive data encrypted
- [ ] Input validation present

### Import Checklist
- [ ] All imports are absolute
- [ ] No circular imports
- [ ] All modules exist
- [ ] Import paths correct
- [ ] No unused imports

## Validation Tools

### Automated Validation

```python
from kailash.validation import WorkflowValidator

validator = WorkflowValidator(workflow)

# Run all validations
results = validator.validate_all()

if not results.is_valid:
    for error in results.errors:
        print(f"Error: {error}")
    for warning in results.warnings:
        print(f"Warning: {warning}")
```

### Manual Validation

```python
# Parameter validation
validate_parameters(node_type, params)

# Connection validation
validate_connection(workflow, source_id, source_param,
                   target_id, target_param)

# DataFlow validation
validate_dataflow_patterns(workflow)

# Security validation
issues = validate_security(workflow)
```

## Critical Validation Rules

### Must Validate
- ✅ All parameters before execution
- ✅ All connections before building
- ✅ Security risks before deployment
- ✅ Import correctness before commit
- ✅ DataFlow patterns in code review

### Never Skip
- ❌ NEVER skip parameter validation
- ❌ NEVER skip connection validation
- ❌ NEVER skip security validation
- ❌ NEVER deploy without validation
- ❌ NEVER commit without import checks

## When to Use This Skill

Use this skill when you need to:
- Validate workflow before execution
- Check parameter correctness
- Verify connection format
- Audit security issues
- Review DataFlow patterns
- Check import compliance
- Perform code review
- Ensure gold standards compliance

## Integration with Development

### Pre-Commit Validation
```bash
# Run validation before commit
python -m kailash.validation.cli validate-all
```

### CI/CD Validation
```yaml
# In CI pipeline
steps:
  - name: Validate Workflows
    run: |
      python -m kailash.validation.cli validate-all
      python -m kailash.validation.cli check-security
```

### Code Review Validation
- Check parameter usage
- Verify connection format
- Audit security issues
- Validate DataFlow patterns
- Check import statements

## Related Skills

- **[17-gold-standards](../../17-gold-standards/SKILL.md)** - Compliance standards
- **[15-error-troubleshooting](../15-error-troubleshooting/SKILL.md)** - Error troubleshooting
- **[01-core-sdk](../../01-core-sdk/SKILL.md)** - Core patterns
- **[02-dataflow](../../02-dataflow/SKILL.md)** - DataFlow patterns

## Support

For validation help, invoke:
- `gold-standards-validator` - Compliance checking
- `pattern-expert` - Pattern validation
- `testing-specialist` - Test validation
- `sdk-navigator` - Find validation guides
