#!/usr/bin/env bash
# validate-cross-references.sh - Cross-reference integrity validation
# ADR: /docs/adr/2026-01-02-session-chronicle-s3-sharing.md

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../../../.." && pwd)"

echo "=== Cross-Reference Integrity Validation ==="

PASSED=0
FAILED=0

# Check 1: ADR exists and has design spec link
ADR_FILE="$REPO_ROOT/docs/adr/2026-01-02-session-chronicle-s3-sharing.md"
if [[ -f "$ADR_FILE" ]]; then
  echo "✓ ADR file exists"
  ((PASSED++)) || true

  if grep -q "docs/design/2026-01-02-session-chronicle-s3-sharing" "$ADR_FILE"; then
    echo "✓ ADR links to design spec"
    ((PASSED++)) || true
  else
    echo "✗ ADR missing design spec link"
    ((FAILED++)) || true
  fi
else
  echo "✗ ADR file missing"
  ((FAILED++)) || true
fi

# Check 2: Design spec exists and has ADR backlink
SPEC_FILE="$REPO_ROOT/docs/design/2026-01-02-session-chronicle-s3-sharing/spec.md"
if [[ -f "$SPEC_FILE" ]]; then
  echo "✓ Design spec file exists"
  ((PASSED++)) || true

  if grep -q "adr:.*2026-01-02-session-chronicle-s3-sharing" "$SPEC_FILE"; then
    echo "✓ Design spec has ADR backlink"
    ((PASSED++)) || true
  else
    echo "✗ Design spec missing ADR backlink"
    ((FAILED++)) || true
  fi

  if grep -q "s3_artifacts:" "$SPEC_FILE"; then
    echo "✓ Design spec has S3 artifacts section"
    ((PASSED++)) || true
  else
    echo "✗ Design spec missing S3 artifacts section"
    ((FAILED++)) || true
  fi
else
  echo "✗ Design spec file missing"
  ((FAILED++)) || true
fi

# Check 3: SKILL.md has ADR reference
SKILL_FILE="$REPO_ROOT/plugins/devops-tools/skills/session-chronicle/SKILL.md"
if grep -q "2026-01-02-session-chronicle-s3-sharing" "$SKILL_FILE"; then
  echo "✓ SKILL.md references implementation ADR"
  ((PASSED++)) || true
else
  echo "✗ SKILL.md missing ADR reference"
  ((FAILED++)) || true
fi

# Check 4: provenance-schema.json has S3 fields
SCHEMA_FILE="$REPO_ROOT/plugins/devops-tools/skills/session-chronicle/references/provenance-schema.json"
if [[ -f "$SCHEMA_FILE" ]]; then
  if jq -e '.properties.s3_artifacts' "$SCHEMA_FILE" >/dev/null 2>&1; then
    echo "✓ provenance-schema has s3_artifacts field"
    ((PASSED++)) || true
  else
    echo "✗ provenance-schema missing s3_artifacts field"
    ((FAILED++)) || true
  fi

  if jq -e '.properties.related_adr' "$SCHEMA_FILE" >/dev/null 2>&1; then
    echo "✓ provenance-schema has related_adr field"
    ((PASSED++)) || true
  else
    echo "✗ provenance-schema missing related_adr field"
    ((FAILED++)) || true
  fi

  if jq -e '.properties.related_design_spec' "$SCHEMA_FILE" >/dev/null 2>&1; then
    echo "✓ provenance-schema has related_design_spec field"
    ((PASSED++)) || true
  else
    echo "✗ provenance-schema missing related_design_spec field"
    ((FAILED++)) || true
  fi
else
  echo "✗ provenance-schema.json not found"
  ((FAILED++)) || true
fi

# Check 5: s3-manifest-schema.json exists and has cross-ref fields
MANIFEST_SCHEMA="$REPO_ROOT/plugins/devops-tools/skills/session-chronicle/references/s3-manifest-schema.json"
if [[ -f "$MANIFEST_SCHEMA" ]]; then
  echo "✓ s3-manifest-schema.json exists"
  ((PASSED++)) || true

  if jq -e '.properties.related_documentation' "$MANIFEST_SCHEMA" >/dev/null 2>&1; then
    echo "✓ s3-manifest-schema has related_documentation field"
    ((PASSED++)) || true
  else
    echo "✗ s3-manifest-schema missing related_documentation field"
    ((FAILED++)) || true
  fi
else
  echo "✗ s3-manifest-schema.json not found"
  ((FAILED++)) || true
fi

# Check 6: README.md mentions S3 sharing
README_FILE="$REPO_ROOT/plugins/devops-tools/README.md"
if grep -qi "s3\|artifact sharing" "$README_FILE"; then
  echo "✓ README.md mentions S3/artifact sharing"
  ((PASSED++)) || true
else
  echo "✗ README.md missing S3/artifact sharing mention"
  ((FAILED++)) || true
fi

echo ""
if [[ $FAILED -eq 0 ]]; then
  echo "Cross-reference integrity validation PASSED ($PASSED checks)"
else
  echo "Cross-reference integrity validation FAILED ($FAILED failures, $PASSED passed)"
  exit 1
fi
