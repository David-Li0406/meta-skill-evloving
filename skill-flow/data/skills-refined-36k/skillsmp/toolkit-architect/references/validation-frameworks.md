# Validation Frameworks

## Table of Contents

- [Overview](#overview)
- [Validation Framework Levels](#validation-framework-levels)
- [Validation Patterns](#validation-patterns)
- [Validation Reporting](#validation-reporting)
- [Automated Validation Hook](#automated-validation-hook)
- [Best Practices](#best-practices)
- [Validation Checklist](#validation-checklist)

## Overview

Comprehensive validation ensures plugin settings are correct, secure, and compatible. This guide covers validation patterns from simple type checking to complex business rules.

## Validation Framework Levels

### Level 1: Basic Type Validation

```bash
#!/bin/bash
basic_validation() {
    local config_file="$1"
    local -a errors=()
    
    # Check file exists
    if [[ ! -f "$config_file" ]]; then
        errors+=("Configuration file not found")
        return 1
    fi
    
    # Check YAML syntax
    if ! python3 -c "import yaml; yaml.safe_load(open('$config_file'))" 2>/dev/null; then
        errors+=("Invalid YAML syntax")
    fi
    
    # Check frontmatter exists
    if ! grep -q "^---$" "$config_file"; then
        errors+=("Missing YAML frontmatter")
    fi
    
    # Return errors
    if [[ ${#errors[@]} -gt 0 ]]; then
        printf '%s\n' "${errors[@]}"
        return 1
    fi
    
    return 0
}
```

### Level 2: Schema Validation

```python
#!/usr/bin/env python3
import yaml
import sys
from typing import Any, Dict, List, Union, Optional

class SchemaValidator:
    """Validate configuration against schema."""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
    
    def validate(self, config: Dict[str, Any], schema: Dict[str, Any]) -> bool:
        """Validate config against schema."""
        self.errors = []
        self.warnings = []
        
        # Validate required fields
        for field, rules in schema.items():
            if rules.get('required', False):
                if field not in config:
                    self.errors.append(f"Missing required field: '{field}'")
        
        # Validate each field
        for field, value in config.items():
            if field in schema:
                self._validate_field(field, value, schema[field])
            else:
                self.warnings.append(f"Unknown field: '{field}'")
        
        return len(self.errors) == 0
    
    def _validate_field(self, name: str, value: Any, rules: Dict[str, Any]):
        """Validate individual field."""
        # Type validation
        if 'type' in rules:
            if not self._check_type(value, rules['type']):
                expected = rules['type'].__name__
                actual = type(value).__name__
                self.errors.append(f"Field '{name}' must be {expected}, got {actual}")
                return
        
        # Range validation for numbers
        if isinstance(value, (int, float)):
            if 'min' in rules and value < rules['min']:
                self.errors.append(f"Field '{name}' must be >= {rules['min']}")
            if 'max' in rules and value > rules['max']:
                self.errors.append(f"Field '{name}' must be <= {rules['max']}")
        
        # String validation
        if isinstance(value, str):
            if 'pattern' in rules:
                import re
                if not re.match(rules['pattern'], value):
                    self.errors.append(f"Field '{name}' doesn't match pattern {rules['pattern']}")
            
            if 'min_length' in rules and len(value) < rules['min_length']:
                self.errors.append(f"Field '{name}' must be at least {rules['min_length']} characters")
            
            if 'max_length' in rules and len(value) > rules['max_length']:
                self.errors.append(f"Field '{name}' must be at most {rules['max_length']} characters")
            
            if 'allowed_values' in rules and value not in rules['allowed_values']:
                self.errors.append(f"Field '{name}' must be one of: {', '.join(rules['allowed_values'])}")
        
        # Array validation
        if isinstance(value, list):
            if 'min_items' in rules and len(value) < rules['min_items']:
                self.errors.append(f"Field '{name}' must have at least {rules['min_items']} items")
            if 'max_items' in rules and len(value) > rules['max_items']:
                self.errors.append(f"Field '{name}' must have at most {rules['max_items']} items")
            
            if 'items_type' in rules:
                for i, item in enumerate(value):
                    if not self._check_type(item, rules['items_type']):
                        self.errors.append(f"Field '{name}' item {i} must be {rules['items_type'].__name__}")
    
    def _check_type(self, value: Any, expected_type: type) -> bool:
        """Check if value matches expected type."""
        if expected_type == str:
            return isinstance(value, str)
        elif expected_type == int:
            return isinstance(value, int) and not isinstance(value, bool)
        elif expected_type == float:
            return isinstance(value, (int, float)) and not isinstance(value, bool)
        elif expected_type == bool:
            return isinstance(value, bool)
        elif expected_type == list:
            return isinstance(value, list)
        elif expected_type == dict:
            return isinstance(value, dict)
        else:
            return isinstance(value, expected_type)

# Schema definition
SCHEMA = {
    'enabled': {'type': bool, 'required': True},
    'mode': {'type': str, 'required': True, 'allowed_values': ['strict', 'standard', 'lenient']},
    'timeout': {'type': int, 'required': False, 'min': 1, 'max': 3600, 'default': 30},
    'retry_count': {'type': int, 'required': False, 'min': 0, 'max': 10, 'default': 3},
    'allowed_hosts': {'type': list, 'required': False, 'items_type': str},
    'settings': {'type': dict, 'required': False}
}

# Usage
def validate_config(file_path: str) -> bool:
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        if not content.startswith('---'):
            print("Missing YAML frontmatter", file=sys.stderr)
            return False
        
        _, frontmatter, _ = content.split('---', 2)
        config = yaml.safe_load(frontmatter) or {}
        
        validator = SchemaValidator()
        valid = validator.validate(config, SCHEMA)
        
        if validator.errors:
            print("Validation errors:", file=sys.stderr)
            for error in validator.errors:
                print(f"  - {error}", file=sys.stderr)
        
        if validator.warnings:
            print("Warnings:", file=sys.stderr)
            for warning in validator.warnings:
                print(f"  - {warning}", file=sys.stderr)
        
        return valid
    
    except Exception as e:
        print(f"Validation failed: {e}", file=sys.stderr)
        return False

# Run validation
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        if validate_config(sys.argv[1]):
            print("✅ Configuration is valid")
            sys.exit(0)
        else:
            print("❌ Configuration is invalid")
            sys.exit(1)
```

### Level 3: Business Rule Validation

```python
#!/usr/bin/env python3
import yaml
import sys
from typing import Any, Dict, List

class BusinessRuleValidator:
    """Validate business rules and constraints."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.errors = []
        self.warnings = []
    
    def validate(self) -> bool:
        """Run all business rule validations."""
        self.errors = []
        self.warnings = []
        
        # Rule 1: Production requires strict mode
        env = self.config.get('environment', 'development')
        if env == 'production':
            if self.config.get('mode') != 'strict':
                self.errors.append("Production environment requires 'strict' mode")
        
        # Rule 2: SSL required for production
        if env == 'production':
            if not self.config.get('ssl_enabled', False):
                self.errors.append("Production environment requires SSL to be enabled")
        
        # Rule 3: Timeout must be reasonable
        timeout = self.config.get('timeout', 30)
        if timeout < 1:
            self.errors.append("Timeout must be at least 1 second")
        if timeout > 3600:
            self.warnings.append("Timeout is very high (> 1 hour)")
        
        # Rule 4: Retry count and timeout relationship
        retry_count = self.config.get('retry_count', 3)
        if timeout * retry_count > 3600:
            self.warnings.append(f"Total retry time ({timeout * retry_count}s) is high")
        
        # Rule 5: Email validation (if present)
        if 'notification_email' in self.config:
            email = self.config['notification_email']
            import re
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                self.errors.append("Invalid email address format")
        
        # Rule 6: URL validation (if present)
        for field in ['api_url', 'webhook_url', 'callback_url']:
            if field in self.config:
                url = self.config[field]
                if not (url.startswith('http://') or url.startswith('https://')):
                    self.errors.append(f"{field} must be HTTP or HTTPS URL")
        
        # Rule 7: Security settings validation
        if self.config.get('auth_required', False):
            if not self.config.get('auth_token'):
                self.errors.append("Authentication required but no token configured")
        
        # Rule 8: Database connection validation
        if self.config.get('database_url'):
            url = self.config['database_url']
            if not any(url.startswith(prefix) for prefix in ['postgresql://', 'mysql://', 'sqlite://']):
                self.errors.append("Database URL must use postgresql://, mysql://, or sqlite://")
        
        # Rule 9: Resource limits sanity check
        limits = self.config.get('resource_limits', {})
        if limits:
            if limits.get('memory_mb', 0) < 0:
                self.errors.append("Memory limit cannot be negative")
            if limits.get('cpu_percent', 0) < 0 or limits.get('cpu_percent', 0) > 100:
                self.errors.append("CPU percent must be between 0 and 100")
        
        # Rule 10: Feature flag consistency
        features = self.config.get('features', {})
        if features.get('caching_enabled', False):
            if not features.get('cache_backend'):
                self.warnings.append("Caching enabled but no cache backend specified")
        
        return len(self.errors) == 0
    
    def get_report(self) -> Dict[str, List[str]]:
        """Get validation report."""
        return {
            'errors': self.errors,
            'warnings': self.warnings
        }

# Usage
def validate_business_rules(file_path: str) -> bool:
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        _, frontmatter, _ = content.split('---', 2)
        config = yaml.safe_load(frontmatter) or {}
        
        validator = BusinessRuleValidator(config)
        valid = validator.validate()
        
        report = validator.get_report()
        
        if report['errors']:
            print("Business rule errors:", file=sys.stderr)
            for error in report['errors']:
                print(f"  ❌ {error}", file=sys.stderr)
        
        if report['warnings']:
            print("Warnings:", file=sys.stderr)
            for warning in report['warnings']:
                print(f"  ⚠️ {warning}", file=sys.stderr)
        
        return valid
    
    except Exception as e:
        print(f"Validation failed: {e}", file=sys.stderr)
        return False
```

## Validation Patterns

### Pattern 1: Progressive Validation

```bash
#!/bin/bash
progressive_validation() {
    local config_file="$1"
    local level="${2:-basic}"  # basic, schema, business
    
    echo "🔍 Validating configuration (level: $level)"
    
    # Level 1: Basic validation
    if ! basic_validation "$config_file"; then
        echo "❌ Basic validation failed"
        return 1
    fi
    echo "✅ Basic validation passed"
    
    # Level 2: Schema validation
    if [[ "$level" == "schema" ]] || [[ "$level" == "business" ]]; then
        if ! python3 <<'PYTHON'
import sys
import yaml
sys.path.insert(0, '/path/to/validators')
from schema_validator import validate_config
validate_config(sys.argv[1])
PYTHON
        "$config_file"; then
            echo "❌ Schema validation failed"
            return 1
        fi
        echo "✅ Schema validation passed"
    fi
    
    # Level 3: Business rules
    if [[ "$level" == "business" ]]; then
        if ! python3 <<'PYTHON'
import sys
sys.path.insert(0, '/path/to/validators')
from business_validator import validate_business_rules
validate_business_rules(sys.argv[1])
PYTHON
        "$config_file"; then
            echo "❌ Business rule validation failed"
            return 1
        fi
        echo "✅ Business rule validation passed"
    fi
    
    echo "✅ All validations passed"
    return 0
}
```

### Pattern 2: Conditional Validation

```python
#!/usr/bin/env python3
import yaml
from typing import Any, Dict, List, Callable

class ConditionalValidator:
    """Apply validation rules conditionally."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.errors = []
    
    def add_rule(self, condition: Callable[[], bool], 
                 error_message: str,
                 field: str = None):
        """Add conditional validation rule."""
        if condition():
            if field:
                # Try to get field value for context
                value = self.config.get(field, '<undefined>')
                self.errors.append(f"{error_message} (current value: {value})")
            else:
                self.errors.append(error_message)
    
    def validate(self) -> bool:
        """Run all conditional rules."""
        self.errors = []
        
        # Rule 1: If caching enabled, require Redis URL
        self.add_rule(
            lambda: self.config.get('features', {}).get('caching_enabled', False) 
                    and not self.config.get('redis_url'),
            "Caching is enabled but Redis URL is not configured",
            'redis_url'
        )
        
        # Rule 2: If auth required, need token or credentials
        self.add_rule(
            lambda: self.config.get('auth_required', False) 
                    and not (self.config.get('auth_token') 
                             or (self.config.get('auth_user') 
                                 and self.config.get('auth_password'))),
            "Authentication is required but no credentials configured"
        )
        
        # Rule 3: Production requires additional security
        self.add_rule(
            lambda: self.config.get('environment') == 'production'
                    and not self.config.get('ssl_enabled', False),
            "Production environment requires SSL",
            'ssl_enabled'
        )
        
        # Rule 4: High timeout needs approval
        self.add_rule(
            lambda: self.config.get('timeout', 0) > 300,
            "Timeout > 300 seconds requires approval"
        )
        
        # Rule 5: Feature flags require documentation
        self.add_rule(
            lambda: 'experimental' in self.config.get('features', {})
                    and not self.config.get('feature_documentation'),
            "Experimental features require documentation"
        )
        
        return len(self.errors) == 0

# Usage
def validate_conditional(file_path: str) -> bool:
    with open(file_path, 'r') as f:
        _, frontmatter, _ = f.read().split('---', 2)
    
    config = yaml.safe_load(frontmatter) or {}
    validator = ConditionalValidator(config)
    
    if not validator.validate():
        print("Conditional validation errors:", file=sys.stderr)
        for error in validator.errors:
            print(f"  ❌ {error}", file=sys.stderr)
        return False
    
    print("✅ Conditional validation passed")
    return True
```

### Pattern 3: Multi-Stage Validation

```python
#!/usr/bin/env python3
import yaml
import sys
from typing import List, Dict, Any, Callable

class ValidationStage:
    """Represents a validation stage."""
    
    def __init__(self, name: str, validator: Callable[[Dict], bool], 
                 required: bool = True, severity: str = 'error'):
        self.name = name
        self.validator = validator
        self.required = required
        self.severity = severity  # error, warning, info
    
    def run(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Run validation stage."""
        try:
            result = self.validator(config)
            return {
                'stage': self.name,
                'passed': result,
                'required': self.required,
                'severity': self.severity
            }
        except Exception as e:
            return {
                'stage': self.name,
                'passed': False,
                'required': self.required,
                'severity': self.severity,
                'error': str(e)
            }

class MultiStageValidator:
    """Multi-stage validation pipeline."""
    
    def __init__(self):
        self.stages = []
    
    def add_stage(self, stage: ValidationStage):
        """Add validation stage."""
        self.stages.append(stage)
    
    def validate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Run all validation stages."""
        results = []
        failed_required = []
        all_passed = True
        
        for stage in self.stages:
            result = stage.run(config)
            results.append(result)
            
            if not result['passed']:
                all_passed = False
                if result['required']:
                    failed_required.append(result)
        
        return {
            'all_passed': all_passed,
            'results': results,
            'failed_required': failed_required
        }

# Stage definitions
def syntax_validator(config: Dict[str, Any]) -> bool:
    """Validate YAML syntax."""
    return True  # Already parsed

def schema_validator(config: Dict[str, Any]) -> bool:
    """Validate against schema."""
    required_fields = ['enabled', 'mode']
    return all(field in config for field in required_fields)

def security_validator(config: Dict[str, Any]) -> bool:
    """Validate security settings."""
    if config.get('environment') == 'production':
        return config.get('ssl_enabled', False) and config.get('mode') == 'strict'
    return True

def performance_validator(config: Dict[str, Any]) -> bool:
    """Validate performance settings."""
    timeout = config.get('timeout', 30)
    retry_count = config.get('retry_count', 3)
    return timeout * retry_count <= 3600

# Usage
def run_multi_stage_validation(file_path: str) -> bool:
    with open(file_path, 'r') as f:
        _, frontmatter, _ = f.read().split('---', 2)
    
    config = yaml.safe_load(frontmatter) or {}
    
    validator = MultiStageValidator()
    validator.add_stage(ValidationStage('syntax', syntax_validator, required=True, severity='error'))
    validator.add_stage(ValidationStage('schema', schema_validator, required=True, severity='error'))
    validator.add_stage(ValidationStage('security', security_validator, required=True, severity='error'))
    validator.add_stage(ValidationStage('performance', performance_validator, required=False, severity='warning'))
    
    results = validator.validate(config)
    
    # Report results
    print("Validation results:")
    for result in results['results']:
        status = "✅" if result['passed'] else "❌"
        severity = result['severity'].upper()
        required = "[REQUIRED]" if result['required'] else "[OPTIONAL]"
        print(f"{status} {required} {severity}: {result['stage']}")
        
        if 'error' in result:
            print(f"    Error: {result['error']}")
    
    if results['failed_required']:
        print("\n❌ Required validations failed:", file=sys.stderr)
        for result in results['failed_required']:
            print(f"  - {result['stage']}", file=sys.stderr)
        return False
    
    print("\n✅ All required validations passed")
    return True
```

## Validation Reporting

### Structured Report Format

```bash
#!/bin/bash
generate_validation_report() {
    local config_file="$1"
    local report_file="${2:-.claude/validation-report.json}"
    
    python3 <<'PYTHON_SCRIPT'
import yaml
import json
import sys
from datetime import datetime

config_file = sys.argv[1]
report_file = sys.argv[2]

try:
    with open(config_file, 'r') as f:
        content = f.read()
    
    _, frontmatter, body = content.split('---', 2)
    config = yaml.safe_load(frontmatter) or {}
    
    # Run validations
    errors = []
    warnings = []
    
    # Basic checks
    if not config.get('enabled'):
        warnings.append("Plugin is disabled")
    
    # Schema checks
    required_fields = ['enabled', 'mode']
    for field in required_fields:
        if field not in config:
            errors.append(f"Missing required field: {field}")
    
    # Business rules
    env = config.get('environment', 'development')
    if env == 'production':
        if config.get('mode') != 'strict':
            errors.append("Production requires strict mode")
        if not config.get('ssl_enabled', False):
            errors.append("Production requires SSL")
    
    # Generate report
    report = {
        'timestamp': datetime.now().isoformat(),
        'config_file': config_file,
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'summary': {
            'total_errors': len(errors),
            'total_warnings': len(warnings)
        },
        'configuration': config
    }
    
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print(f"Validation report: {report_file}")
    print(f"Valid: {report['valid']}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    
    sys.exit(0 if report['valid'] else 1)

except Exception as e:
    print(f"Validation failed: {e}", file=sys.stderr)
    sys.exit(1)
PYTHON_SCRIPT

    "$config_file" "$report_file"
}
```

## Automated Validation Hook

```bash
#!/bin/bash
# Validate on every hook execution
validate_on_hook() {
    local config_file=".claude/my-plugin.local.md"
    
    # Only validate if file exists
    if [[ ! -f "$config_file" ]]; then
        return 0
    fi
    
    # Run validation
    if ! python3 -c "
import yaml
import sys

try:
    with open('$config_file', 'r') as f:
        content = f.read()
    
    _, frontmatter, _ = content.split('---', 2)
    config = yaml.safe_load(frontmatter) or {}
    
    # Quick checks
    if 'enabled' not in config:
        print('⚠️ Missing enabled field, defaulting to true', file=sys.stderr)
    
    if config.get('enabled', True) == False:
        print('Plugin disabled, skipping', file=sys.stderr)
        sys.exit(0)
    
    print('✅ Validation passed')
    sys.exit(0)
    
except Exception as e:
    print(f'❌ Validation failed: {e}', file=sys.stderr)
    sys.exit(1)
"; then
        echo "❌ Configuration validation failed" >&2
        return 1
    fi
    
    return 0
}

# Call at start of hook
validate_on_hook || exit 1
```

## Best Practices

### 1. Fail Fast

```bash
# Check for obvious errors first
if [[ ! -f "$STATE_FILE" ]]; then
    echo "❌ Configuration file not found" >&2
    exit 1
fi

# Validate YAML syntax
if ! python3 -c "import yaml; yaml.safe_load(open('$STATE_FILE'))" 2>/dev/null; then
    echo "❌ Invalid YAML syntax" >&2
    exit 1
fi
```

### 2. Provide Clear Error Messages

```python
# Good
errors.append(f"Field '{field}' must be one of: {', '.join(allowed_values)}")

# Bad
errors.append(f"Invalid value")
```

### 3. Validate Early and Often

```bash
# Validate at file load
validate_config "$STATE_FILE" || exit 1

# Validate before use
validate_timeout "$TIMEOUT" || exit 1

# Validate before critical operations
validate_before_deploy "$CONFIG" || exit 1
```

### 4. Use Appropriate Validation Levels

```bash
# Interactive use: Full validation
validate_config "$FILE" "business"

# CI/CD: Schema validation
validate_config "$FILE" "schema"

# Runtime: Minimal validation
validate_config "$FILE" "basic"
```

### 5. Log Validation Results

```python
import logging

logging.basicConfig(
    filename='.claude/validation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def validate_with_logging(config_file):
    result = validate_config(config_file)
    logging.info(f"Validation {'passed' if result else 'failed'} for {config_file}")
    return result
```

### 6. Support Configuration Migration

```python
def migrate_config(config):
    """Migrate old config format to new format."""
    migrated = config.copy()
    
    # Migrate v1.0 to v2.0
    if 'version' not in migrated or migrated['version'] == '1.0':
        # Add new fields with defaults
        migrated['version'] = '2.0.0'
        migrated.setdefault('timeout', 30)
        migrated.setdefault('retry_count', 3)
        
        # Rename fields
        if 'log_level' in migrated:
            migrated['logging_level'] = migrated.pop('log_level')
    
    return migrated
```

## Validation Checklist

### Pre-Deployment Checklist

- [ ] YAML syntax is valid
- [ ] All required fields present
- [ ] Types match schema
- [ ] Values within allowed ranges
- [ ] No deprecated fields
- [ ] Security settings validated
- [ ] Production requirements met
- [ ] Business rules satisfied
- [ ] Documentation updated
- [ ] Tests passing

### Runtime Checklist

- [ ] Configuration file exists
- [ ] Plugin is enabled
- [ ] Required environment variables set
- [ ] Dependencies available
- [ ] Permissions correct
- [ ] Paths validated
- [ ] Network connectivity confirmed

### Maintenance Checklist

- [ ] Configuration backup created
- [ ] Validation report generated
- [ ] Changes documented
- [ ] Rollback plan ready
- [ ] Monitoring configured
- [ ] Alerts configured

These validation frameworks ensure plugin configurations are correct, secure, and maintainable across all environments and deployment stages.
