#!/usr/bin/env bash
#
# validate-yaml.sh - Validate GitHub Actions workflow YAML syntax
# Usage: bash validate-yaml.sh <workflow-file>
#

set -e

# Check if file is provided
if [ -z "$1" ]; then
    echo "❌ Error: No workflow file provided"
    echo ""
    echo "Usage: bash validate-yaml.sh <workflow-file>"
    echo ""
    echo "Examples:"
    echo "  bash validate-yaml.sh .github/workflows/ci.yml"
    echo "  bash validate-yaml.sh .github/workflows/*.yml"
    exit 1
fi

WORKFLOW_FILE="$1"

# Check if file exists
if [ ! -f "$WORKFLOW_FILE" ]; then
    echo "❌ Error: File not found: $WORKFLOW_FILE"
    exit 1
fi

echo "🔍 Validating workflow: $WORKFLOW_FILE"
echo ""

# Check if yq is installed
if command -v yq &> /dev/null; then
    echo "Using yq for validation..."

    if yq eval '.' "$WORKFLOW_FILE" > /dev/null 2>&1; then
        echo "✅ YAML syntax is valid"
    else
        echo "❌ YAML syntax error detected"
        yq eval '.' "$WORKFLOW_FILE"
        exit 1
    fi

    # Check required GitHub Actions fields
    echo ""
    echo "Checking required fields..."

    if yq eval '.name' "$WORKFLOW_FILE" > /dev/null 2>&1; then
        NAME=$(yq eval '.name' "$WORKFLOW_FILE")
        echo "✅ name: $NAME"
    else
        echo "❌ Missing required field: name"
    fi

    if yq eval '.on' "$WORKFLOW_FILE" > /dev/null 2>&1; then
        echo "✅ on: $(yq eval '.on' "$WORKFLOW_FILE" | head -1)"
    else
        echo "❌ Missing required field: on"
    fi

    JOBS_COUNT=$(yq eval '.jobs | length' "$WORKFLOW_FILE" 2>/dev/null || echo "0")
    if [ "$JOBS_COUNT" -gt 0 ]; then
        echo "✅ jobs: $JOBS_COUNT job(s) defined"
    else
        echo "❌ No jobs defined"
    fi

# Check if python is available for PyYAML validation
elif command -v python3 &> /dev/null; then
    echo "Using Python for validation..."

    python3 <<EOF
import sys
import yaml

try:
    with open('$WORKFLOW_FILE', 'r') as f:
        data = yaml.safe_load(f)

    # Check required fields
    if 'name' not in data:
        print('❌ Missing required field: name')
        sys.exit(1)
    else:
        print(f'✅ name: {data["name"]}')

    if 'on' not in data:
        print('❌ Missing required field: on')
        sys.exit(1)
    else:
        print(f'✅ on: {str(data["on"])[:50]}...')

    if 'jobs' not in data:
        print('❌ No jobs defined')
        sys.exit(1)
    else:
        job_count = len(data['jobs'])
        print(f'✅ jobs: {job_count} job(s) defined')

    print('')
    print('✅ YAML syntax is valid')

except yaml.YAMLError as e:
    print(f'❌ YAML syntax error: {e}')
    sys.exit(1)
except Exception as e:
    print(f'❌ Error: {e}')
    sys.exit(1)
EOF

# Fallback: basic syntax check
else
    echo "⚠️  Warning: yq or Python not found, performing basic syntax check..."

    # Check for basic YAML syntax errors
    if grep -P '\t' "$WORKFLOW_FILE"; then
        echo "❌ Error: Tabs detected (use spaces for indentation in YAML)"
        exit 1
    fi

    # Check for common YAML errors
    if ! grep -q '^name:' "$WORKFLOW_FILE"; then
        echo "❌ Missing required field: name"
        exit 1
    fi

    if ! grep -q '^on:' "$WORKFLOW_FILE"; then
        echo "❌ Missing required field: on"
        exit 1
    fi

    if ! grep -q '^jobs:' "$WORKFLOW_FILE"; then
        echo "❌ Missing required field: jobs"
        exit 1
    fi

    echo "✅ Basic validation passed"
    echo "⚠️  Install yq or Python for comprehensive validation"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "       VALIDATION COMPLETE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✅ Workflow file: $WORKFLOW_FILE"
echo "✅ Syntax: Valid"
echo ""

# Additional checks
echo "Performing additional checks..."

# Check for pinned action versions
if grep -E '@(main|master)' "$WORKFLOW_FILE" > /dev/null 2>&1; then
    echo "⚠️  Warning: Using @main/@master is not recommended"
    echo "   Pin action versions (e.g., @v4) for reproducibility"
fi

# Check for secrets usage
if grep -E '\${{\s*secrets\.' "$WORKFLOW_FILE" > /dev/null 2>&1; then
    SECRET_COUNT=$(grep -oE '\${{\s*secrets\.[A-Z_]+' "$WORKFLOW_FILE" | sort -u | wc -l)
    echo "ℹ️  Found $SECRET_COUNT secret(s) referenced"
    echo "   Ensure these are configured in repository settings"
fi

# Check for permissions
if grep -q '^permissions:' "$WORKFLOW_FILE"; then
    echo "✅ Permissions explicitly set"
else
    echo "⚠️  Warning: No permissions specified"
    echo "   Add 'permissions:' block for least privilege"
fi

echo ""
echo "Recommendation: Test workflow with 'act' before pushing"
echo "  brew install act  # macOS"
echo "  act -n -W $WORKFLOW_FILE"
echo ""
