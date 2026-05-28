#!/bin/bash
# Terraform validation script
# Runs terraform fmt and terraform validate

set -e

TERRAFORM_DIR="${1:-.}"

echo "🔍 Validating Terraform code in: $TERRAFORM_DIR"
echo ""

# Change to terraform directory
cd "$TERRAFORM_DIR"

# Run terraform fmt
echo "📝 Running terraform fmt..."
if terraform fmt -check -recursive -diff; then
  echo "✅ Formatting check passed"
else
  echo "⚠️  Formatting issues found. Running terraform fmt to fix..."
  terraform fmt -recursive
  echo "✅ Formatting applied"
fi

echo ""

# Initialize if needed (skip backend)
if [ ! -d ".terraform" ]; then
  echo "🔧 Initializing Terraform..."
  terraform init -backend=false > /dev/null 2>&1 || true
fi

# Run terraform validate
echo "🔍 Running terraform validate..."
if terraform validate; then
  echo "✅ Validation passed"
else
  echo "❌ Validation failed"
  exit 1
fi

echo ""
echo "✅ All validation checks passed!"
