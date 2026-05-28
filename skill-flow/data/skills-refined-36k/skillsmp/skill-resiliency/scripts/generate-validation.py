#!/usr/bin/env python3
"""
Generate validation scripts from schema definitions.

This utility helps implement resiliency by automatically creating
validation scripts from JSON/YAML schemas.

Usage:
    python generate-validation.py schema.json --output validate-input.py
    python generate-validation.py schema.json --language bash --output validate.sh
"""

import argparse
import json
import sys
from pathlib import Path


PYTHON_TEMPLATE = '''#!/usr/bin/env python3
"""
Auto-generated validation script.
Generated from: {schema_file}
"""

import json
import sys
from jsonschema import validate, ValidationError, Draft7Validator


SCHEMA = {schema_json}


def validate_data(data_file):
    """Validate data file against schema."""
    try:
        with open(data_file) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON: {{e}}")
        return False
    except FileNotFoundError:
        print(f"❌ File not found: {{data_file}}")
        return False

    validator = Draft7Validator(SCHEMA)
    errors = list(validator.iter_errors(data))

    if errors:
        print(f"❌ Validation failed with {{len(errors)}} error(s):")
        for i, error in enumerate(errors, 1):
            path = " -> ".join(str(p) for p in error.path)
            print(f"   {{i}}. {{error.message}}")
            if path:
                print(f"      Path: {{path}}")
        return False
    else:
        print(f"✅ Validation passed: {{data_file}}")
        return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {{sys.argv[0]}} <data_file>")
        sys.exit(1)

    result = validate_data(sys.argv[1])
    sys.exit(0 if result else 1)
'''


BASH_TEMPLATE = '''#!/bin/bash
# Auto-generated validation script
# Generated from: {schema_file}

set -e

DATA_FILE="$1"

if [ -z "$DATA_FILE" ]; then
    echo "Usage: $0 <data_file>"
    exit 1
fi

if [ ! -f "$DATA_FILE" ]; then
    echo "❌ File not found: $DATA_FILE"
    exit 1
fi

echo "Validating: $DATA_FILE"

# Check if file is valid JSON
if ! jq empty "$DATA_FILE" 2>/dev/null; then
    echo "❌ Invalid JSON"
    exit 1
fi

{validation_checks}

echo "✅ Validation passed: $DATA_FILE"
exit 0
'''


def generate_bash_checks(schema):
    """Generate bash validation checks from schema."""
    checks = []

    # Check required fields
    if 'required' in schema:
        for field in schema['required']:
            check = f'''
# Check required field: {field}
if ! jq -e '.{field}' "$DATA_FILE" >/dev/null 2>&1; then
    echo "❌ Missing required field: {field}"
    exit 1
fi
'''
            checks.append(check)

    # Check property types and constraints
    if 'properties' in schema:
        for prop, prop_schema in schema['properties'].items():
            # Type checks
            if 'type' in prop_schema:
                prop_type = prop_schema['type']
                if prop_type == 'string':
                    check = f'''
# Check type of '{prop}' is string
FIELD_TYPE=$(jq -r '.{prop} | type' "$DATA_FILE" 2>/dev/null)
if [ "$FIELD_TYPE" != "string" ] && [ "$FIELD_TYPE" != "null" ]; then
    echo "❌ Field '{prop}' must be string, got: $FIELD_TYPE"
    exit 1
fi
'''
                    checks.append(check)

                elif prop_type == 'number' or prop_type == 'integer':
                    check = f'''
# Check type of '{prop}' is number
FIELD_TYPE=$(jq -r '.{prop} | type' "$DATA_FILE" 2>/dev/null)
if [ "$FIELD_TYPE" != "number" ] && [ "$FIELD_TYPE" != "null" ]; then
    echo "❌ Field '{prop}' must be number, got: $FIELD_TYPE"
    exit 1
fi
'''
                    checks.append(check)

            # Min/max checks for numbers
            if 'minimum' in prop_schema:
                min_val = prop_schema['minimum']
                check = f'''
# Check minimum value for '{prop}'
FIELD_VAL=$(jq -r '.{prop}' "$DATA_FILE" 2>/dev/null)
if [ "$FIELD_VAL" != "null" ] && [ $(echo "$FIELD_VAL < {min_val}" | bc) -eq 1 ]; then
    echo "❌ Field '{prop}' must be >= {min_val}, got: $FIELD_VAL"
    exit 1
fi
'''
                checks.append(check)

            if 'maximum' in prop_schema:
                max_val = prop_schema['maximum']
                check = f'''
# Check maximum value for '{prop}'
FIELD_VAL=$(jq -r '.{prop}' "$DATA_FILE" 2>/dev/null)
if [ "$FIELD_VAL" != "null" ] && [ $(echo "$FIELD_VAL > {max_val}" | bc) -eq 1 ]; then
    echo "❌ Field '{prop}' must be <= {max_val}, got: $FIELD_VAL"
    exit 1
fi
'''
                checks.append(check)

            # Enum checks
            if 'enum' in prop_schema:
                enum_values = prop_schema['enum']
                enum_str = '|'.join(enum_values)
                check = f'''
# Check enum value for '{prop}'
FIELD_VAL=$(jq -r '.{prop}' "$DATA_FILE" 2>/dev/null)
if [ "$FIELD_VAL" != "null" ] && ! echo "$FIELD_VAL" | grep -qE "^({enum_str})$"; then
    echo "❌ Field '{prop}' must be one of: {', '.join(enum_values)}, got: $FIELD_VAL"
    exit 1
fi
'''
                checks.append(check)

    return '\n'.join(checks) if checks else '# No specific validation checks'


def generate_python_script(schema, schema_file, output_file):
    """Generate Python validation script."""
    script = PYTHON_TEMPLATE.format(
        schema_file=schema_file,
        schema_json=json.dumps(schema, indent=4)
    )

    with open(output_file, 'w') as f:
        f.write(script)

    # Make executable
    output_file.chmod(0o755)
    print(f"✅ Generated Python validation script: {output_file}")


def generate_bash_script(schema, schema_file, output_file):
    """Generate Bash validation script."""
    validation_checks = generate_bash_checks(schema)

    script = BASH_TEMPLATE.format(
        schema_file=schema_file,
        validation_checks=validation_checks
    )

    with open(output_file, 'w') as f:
        f.write(script)

    # Make executable
    output_file.chmod(0o755)
    print(f"✅ Generated Bash validation script: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate validation scripts from JSON/YAML schemas'
    )
    parser.add_argument(
        'schema',
        help='Path to JSON/YAML schema file'
    )
    parser.add_argument(
        '--output', '-o',
        default='validate.py',
        help='Output script path (default: validate.py)'
    )
    parser.add_argument(
        '--language', '-l',
        choices=['python', 'bash'],
        default='python',
        help='Script language (default: python)'
    )

    args = parser.parse_args()

    # Load schema
    schema_file = Path(args.schema)
    if not schema_file.exists():
        print(f"❌ Schema file not found: {schema_file}")
        sys.exit(1)

    with open(schema_file) as f:
        if schema_file.suffix == '.json':
            schema = json.load(f)
        elif schema_file.suffix in ['.yml', '.yaml']:
            import yaml
            schema = yaml.safe_load(f)
        else:
            print(f"❌ Unsupported schema format: {schema_file.suffix}")
            print("   Supported: .json, .yml, .yaml")
            sys.exit(1)

    # Generate validation script
    output_file = Path(args.output)

    if args.language == 'python':
        generate_python_script(schema, schema_file.name, output_file)
    elif args.language == 'bash':
        generate_bash_script(schema, schema_file.name, output_file)

    print(f"\nUsage: {output_file} <data_file>")


if __name__ == "__main__":
    main()
