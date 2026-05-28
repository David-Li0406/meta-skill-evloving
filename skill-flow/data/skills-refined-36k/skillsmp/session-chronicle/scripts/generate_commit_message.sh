#!/usr/bin/env bash
# generate_commit_message.sh - Generate git commit message with S3 provenance links
# Usage: ./generate_commit_message.sh <artifact_dir> <description> [related_adr]
#
# Generates a structured commit message with embedded S3 retrieval command.
# ADR: /docs/adr/2026-01-02-session-chronicle-s3-sharing.md

set -euo pipefail

ARTIFACT_DIR="${1:-}"
DESCRIPTION="${2:-Session provenance capture}"
RELATED_ADR="${3:-}"

if [[ -z "$ARTIFACT_DIR" ]]; then
  echo "Usage: $0 <artifact_dir> <description> [related_adr]" >&2
  echo "" >&2
  echo "Arguments:" >&2
  echo "  artifact_dir   Directory containing session chronicle artifacts" >&2
  echo "  description    Short description of the finding/change" >&2
  echo "  related_adr    Related ADR slug (e.g., 2025-12-15-feature-name)" >&2
  echo "" >&2
  echo "Output: Commit message to stdout" >&2
  exit 1
fi

if [[ ! -f "$ARTIFACT_DIR/manifest.json" ]]; then
  echo "ERROR: manifest.json not found in $ARTIFACT_DIR" >&2
  exit 1
fi

# Read manifest
MANIFEST="$ARTIFACT_DIR/manifest.json"

# Extract fields from manifest
S3_LOCATION=$(jq -r '.s3_location // empty' "$MANIFEST")
TOTAL_SESSIONS=$(jq -r '.total_sessions // "N/A"' "$MANIFEST")
TOTAL_LINES=$(jq -r '.total_lines // "N/A"' "$MANIFEST")
CHAIN_DEPTH=$(jq -r '.chain_depth // "N/A"' "$MANIFEST")
FIRST_TS=$(jq -r '.first_timestamp // "N/A"' "$MANIFEST")
LAST_TS=$(jq -r '.last_timestamp // "N/A"' "$MANIFEST")
PROJECT_PATH=$(jq -r '.project_path // "N/A"' "$MANIFEST")
COMPRESSION=$(jq -r '.compression // "brotli-9"' "$MANIFEST")

# Build file list
FILES=""
if [[ -n "$S3_LOCATION" ]]; then
  for f in "$ARTIFACT_DIR"/*.br "$ARTIFACT_DIR"/*.jsonl "$ARTIFACT_DIR"/*.json; do
    if [[ -f "$f" ]]; then
      FILES="${FILES}    - $(basename "$f")\n"
    fi
  done
fi

# Generate commit message
cat << EOF
feat(provenance): $DESCRIPTION

Session-Chronicle Provenance:
  sessions_traced: $TOTAL_SESSIONS
  total_lines: $TOTAL_LINES
  chain_depth: $CHAIN_DEPTH
  first_timestamp: $FIRST_TS
  last_timestamp: $LAST_TS
  project_path: $PROJECT_PATH
  compression: $COMPRESSION

EOF

if [[ -n "$S3_LOCATION" ]]; then
cat << EOF
Artifacts (S3):
  bucket: $S3_LOCATION
  files:
$(echo -e "$FILES")
EOF
fi

if [[ -n "$RELATED_ADR" ]]; then
cat << EOF

Related ADR: $RELATED_ADR
Design Spec: /docs/design/$RELATED_ADR/spec.md
EOF
fi

cat << 'EOF'

Retrieval (requires 1Password Employee vault access):
  /usr/bin/env bash << 'RETRIEVE_EOF'
  export AWS_ACCESS_KEY_ID=$(op read "op://Claude Automation/ise47dxnkftmxopupffavsgby4/access key id")
  export AWS_SECRET_ACCESS_KEY=$(op read "op://Claude Automation/ise47dxnkftmxopupffavsgby4/secret access key")
  export AWS_DEFAULT_REGION="us-west-2"
EOF

if [[ -n "$S3_LOCATION" ]]; then
cat << EOF
  aws s3 sync $S3_LOCATION/ ./sessions/
EOF
fi

cat << 'EOF'
  for f in ./sessions/*.br; do brotli -d "$f"; done
  RETRIEVE_EOF

EOF

if [[ -n "$S3_LOCATION" ]]; then
cat << EOF
Session-Chronicle-S3: $S3_LOCATION
EOF
fi
