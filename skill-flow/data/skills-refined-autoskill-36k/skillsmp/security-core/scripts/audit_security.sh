#!/bin/bash
set -euo pipefail

# Security audit script for TypeScript, Python, and Rust projects
# Runs appropriate security scanners based on detected project type

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="${1:-.}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔒 Security Audit for: $PROJECT_DIR"
echo ""

# Detect project type
HAS_PACKAGE_JSON=false
HAS_REQUIREMENTS=false
HAS_CARGO_TOML=false

[[ -f "$PROJECT_DIR/package.json" ]] && HAS_PACKAGE_JSON=true
[[ -f "$PROJECT_DIR/requirements.txt" ]] || [[ -f "$PROJECT_DIR/pyproject.toml" ]] && HAS_REQUIREMENTS=true
[[ -f "$PROJECT_DIR/Cargo.toml" ]] && HAS_CARGO_TOML=true

# TypeScript/Node.js audit
if [[ "$HAS_PACKAGE_JSON" == true ]]; then
  echo -e "${GREEN}📦 Detected TypeScript/Node.js project${NC}"

  # Check if npm audit is available
  if command -v npm &> /dev/null; then
    echo "Running npm audit..."
    cd "$PROJECT_DIR"
    npm audit --json > .security-audit-npm.json 2>/dev/null || true

    if [[ -s .security-audit-npm.json ]]; then
      VULNERABILITIES=$(jq '.metadata.vulnerabilities | .total // 0' .security-audit-npm.json)
      if [[ "$VULNERABILITIES" -gt 0 ]]; then
        echo -e "${RED}⚠️  Found $VULNERABILITIES vulnerabilities${NC}"
        echo "Run 'npm audit' for details"
      else
        echo -e "${GREEN}✅ No npm vulnerabilities found${NC}"
      fi
    fi
  fi

  # Check for common security issues in code
  echo "Scanning for hardcoded secrets..."
  if command -v rg &> /dev/null; then
    SECRET_PATTERNS=(
      'password\s*=\s*["\047][^"\047]+["\047]'
      'api[_-]?key\s*=\s*["\047][^"\047]+["\047]'
      'secret\s*=\s*["\047][^"\047]+["\047]'
      'token\s*=\s*["\047][^"\047]+["\047]'
    )

    for pattern in "${SECRET_PATTERNS[@]}"; do
      if rg -i "$pattern" "$PROJECT_DIR" --type ts --type js 2>/dev/null | grep -v node_modules | grep -q .; then
        echo -e "${YELLOW}⚠️  Potential hardcoded secret found (pattern: $pattern)${NC}"
      fi
    done
  fi

  echo ""
fi

# Python audit
if [[ "$HAS_REQUIREMENTS" == true ]]; then
  echo -e "${GREEN}🐍 Detected Python project${NC}"

  # Check if pip-audit is available
  if command -v pip-audit &> /dev/null; then
    echo "Running pip-audit..."
    cd "$PROJECT_DIR"
    pip-audit --format json > .security-audit-pip.json 2>/dev/null || true

    if [[ -s .security-audit-pip.json ]]; then
      VULNERABILITIES=$(jq '. | length' .security-audit-pip.json 2>/dev/null || echo "0")
      if [[ "$VULNERABILITIES" -gt 0 ]]; then
        echo -e "${RED}⚠️  Found $VULNERABILITIES vulnerabilities${NC}"
        echo "Run 'pip-audit' for details"
      else
        echo -e "${GREEN}✅ No pip vulnerabilities found${NC}"
      fi
    fi
  else
    echo -e "${YELLOW}⚠️  pip-audit not installed. Install with: pip install pip-audit${NC}"
  fi

  # Check for common security issues
  echo "Scanning for hardcoded secrets..."
  if command -v rg &> /dev/null; then
    SECRET_PATTERNS=(
      'password\s*=\s*["\047][^"\047]+["\047]'
      'api[_-]?key\s*=\s*["\047][^"\047]+["\047]'
      'secret\s*=\s*["\047][^"\047]+["\047]'
      'SECRET_KEY\s*=\s*["\047][^"\047]+["\047]'
    )

    for pattern in "${SECRET_PATTERNS[@]}"; do
      if rg -i "$pattern" "$PROJECT_DIR" --type py 2>/dev/null | grep -v venv | grep -q .; then
        echo -e "${YELLOW}⚠️  Potential hardcoded secret found (pattern: $pattern)${NC}"
      fi
    done
  fi

  echo ""
fi

# Rust audit
if [[ "$HAS_CARGO_TOML" == true ]]; then
  echo -e "${GREEN}🦀 Detected Rust project${NC}"

  # Check if cargo-audit is available
  if command -v cargo-audit &> /dev/null; then
    echo "Running cargo-audit..."
    cd "$PROJECT_DIR"
    cargo audit --json > .security-audit-cargo.json 2>/dev/null || true

    if [[ -s .security-audit-cargo.json ]]; then
      VULNERABILITIES=$(jq '.vulnerabilities.count' .security-audit-cargo.json 2>/dev/null || echo "0")
      if [[ "$VULNERABILITIES" -gt 0 ]]; then
        echo -e "${RED}⚠️  Found $VULNERABILITIES vulnerabilities${NC}"
        echo "Run 'cargo audit' for details"
      else
        echo -e "${GREEN}✅ No cargo vulnerabilities found${NC}"
      fi
    fi
  else
    echo -e "${YELLOW}⚠️  cargo-audit not installed. Install with: cargo install cargo-audit${NC}"
  fi

  echo ""
fi

# Generic checks
echo "🔍 Running generic security checks..."

# Check for exposed secrets in environment files
if [[ -f "$PROJECT_DIR/.env" ]]; then
  echo -e "${YELLOW}⚠️  .env file found - ensure it's in .gitignore${NC}"

  if [[ -f "$PROJECT_DIR/.gitignore" ]]; then
    if ! grep -q "^\.env$" "$PROJECT_DIR/.gitignore"; then
      echo -e "${RED}⚠️  .env is NOT in .gitignore!${NC}"
    fi
  fi
fi

# Check for common debug endpoints
if command -v rg &> /dev/null; then
  if rg -i "(\/debug|\/test-auth|\/admin\/debug)" "$PROJECT_DIR" 2>/dev/null | grep -q .; then
    echo -e "${YELLOW}⚠️  Potential debug endpoints found${NC}"
  fi
fi

echo ""
echo -e "${GREEN}✅ Security audit complete${NC}"
echo ""
echo "For more comprehensive scanning, consider:"
echo "  - Snyk: https://snyk.io/"
echo "  - GitHub Security: https://docs.github.com/en/code-security"
echo "  - OWASP Dependency-Check: https://owasp.org/www-project-dependency-check/"
