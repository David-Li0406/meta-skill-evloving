#!/bin/bash
# Validate Dockerfile for best practices and common issues
# Usage: bash scripts/validate-dockerfile.sh [path/to/Dockerfile]

set -euo pipefail

DOCKERFILE="${1:-Dockerfile}"

echo "=== Dockerfile Validation ==="
echo "File: ${DOCKERFILE}"
echo ""

if [ ! -f "${DOCKERFILE}" ]; then
    echo "Error: ${DOCKERFILE} not found"
    exit 1
fi

ERRORS=0
WARNINGS=0

# Helper functions
error() { echo "  [ERROR] $1"; ((ERRORS++)); }
warn() { echo "  [WARN]  $1"; ((WARNINGS++)); }
pass() { echo "  [PASS]  $1"; }

# Check 1: Multi-stage build
echo ">> Checking multi-stage build..."
STAGE_COUNT=$(grep -c "^FROM" "${DOCKERFILE}" || true)
if [ "${STAGE_COUNT}" -lt 2 ]; then
    warn "Single-stage build detected. Use multi-stage for smaller images."
else
    pass "Multi-stage build with ${STAGE_COUNT} stages"
fi

# Check 2: Slim/Alpine base
echo ">> Checking base image..."
if grep -q "python:.*-slim\|python:.*-alpine" "${DOCKERFILE}"; then
    pass "Using slim/alpine base image"
elif grep -q "^FROM python:" "${DOCKERFILE}"; then
    error "Using full Python image. Switch to python:X.Y-slim"
fi

# Check 3: Non-root user
echo ">> Checking user configuration..."
if grep -q "^USER\|adduser\|useradd" "${DOCKERFILE}"; then
    pass "Non-root user configured"
else
    error "No non-root user. Add 'RUN adduser' and 'USER appuser'"
fi

# Check 4: PYTHONDONTWRITEBYTECODE
echo ">> Checking Python environment..."
if grep -q "PYTHONDONTWRITEBYTECODE" "${DOCKERFILE}"; then
    pass "PYTHONDONTWRITEBYTECODE set"
else
    warn "Missing PYTHONDONTWRITEBYTECODE=1"
fi

if grep -q "PYTHONUNBUFFERED" "${DOCKERFILE}"; then
    pass "PYTHONUNBUFFERED set"
else
    warn "Missing PYTHONUNBUFFERED=1"
fi

# Check 5: Cache mounts
echo ">> Checking build optimization..."
if grep -q "mount=type=cache" "${DOCKERFILE}"; then
    pass "BuildKit cache mounts used"
else
    warn "No cache mounts. Add --mount=type=cache for pip"
fi

# Check 6: COPY ordering (deps before source)
echo ">> Checking layer ordering..."
COPY_LINES=$(grep -n "^COPY\|^ADD" "${DOCKERFILE}" | head -5)
if echo "${COPY_LINES}" | grep -q "requirements\|pyproject\|Pipfile"; then
    pass "Dependency files copied before source"
else
    warn "Consider copying dependency files before source code for layer caching"
fi

# Check 7: .dockerignore exists
echo ">> Checking .dockerignore..."
DOCKERFILE_DIR=$(dirname "${DOCKERFILE}")
if [ -f "${DOCKERFILE_DIR}/.dockerignore" ]; then
    pass ".dockerignore exists"
    # Check for common exclusions
    IGNORE_FILE="${DOCKERFILE_DIR}/.dockerignore"
    for pattern in ".git" "__pycache__" ".venv" ".env" "node_modules"; do
        if ! grep -q "${pattern}" "${IGNORE_FILE}" 2>/dev/null; then
            warn ".dockerignore missing: ${pattern}"
        fi
    done
else
    error "No .dockerignore found. Create one to reduce build context."
fi

# Check 8: No secrets
echo ">> Checking for secrets..."
if grep -qi "password\|secret\|api_key\|token" "${DOCKERFILE}" | grep -v "^#"; then
    error "Possible secrets found in Dockerfile!"
else
    pass "No obvious secrets detected"
fi

# Check 9: EXPOSE directive
echo ">> Checking port exposure..."
if grep -q "^EXPOSE" "${DOCKERFILE}"; then
    PORTS=$(grep "^EXPOSE" "${DOCKERFILE}" | awk '{print $2}')
    pass "Ports exposed: ${PORTS}"
else
    warn "No EXPOSE directive. Consider adding for documentation."
fi

# Check 10: HEALTHCHECK
echo ">> Checking health check..."
if grep -q "HEALTHCHECK" "${DOCKERFILE}"; then
    pass "HEALTHCHECK configured"
else
    warn "No HEALTHCHECK. Consider adding for container orchestration."
fi

# Summary
echo ""
echo "=== Validation Summary ==="
echo "Errors:   ${ERRORS}"
echo "Warnings: ${WARNINGS}"

if [ "${ERRORS}" -gt 0 ]; then
    echo "Status: FAILED - Fix errors before deployment"
    exit 1
else
    echo "Status: PASSED"
    exit 0
fi
