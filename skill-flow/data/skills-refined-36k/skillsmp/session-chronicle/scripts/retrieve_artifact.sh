#!/usr/bin/env bash
# retrieve_artifact.sh - Download and decompress session chronicle artifacts from S3
# Usage: ./retrieve_artifact.sh <s3_uri> <output_dir>
#
# Downloads artifacts from S3 and decompresses Brotli-compressed files.
# Uses 1Password for credential injection.
# ADR: /docs/adr/2026-01-02-session-chronicle-s3-sharing.md

set -euo pipefail

S3_URI="${1:-}"
OUTPUT_DIR="${2:-./artifacts}"

# 1Password configuration
OP_VAULT="Claude Automation"
OP_ITEM_ID="ise47dxnkftmxopupffavsgby4"
AWS_REGION="us-west-2"

if [[ -z "$S3_URI" ]]; then
  echo "Usage: $0 <s3_uri> [output_dir]" >&2
  echo "" >&2
  echo "Arguments:" >&2
  echo "  s3_uri      S3 URI (e.g., s3://eonlabs-findings/sessions/id)" >&2
  echo "  output_dir  Local directory for downloaded artifacts (default: ./artifacts)" >&2
  echo "" >&2
  echo "Required tools: brotli, aws, op (1Password CLI)" >&2
  echo "" >&2
  echo "Example:" >&2
  echo "  $0 s3://eonlabs-findings/sessions/2026-01-01-multiyear-momentum ./artifacts" >&2
  exit 1
fi

# Validate S3 URI format
if [[ ! "$S3_URI" =~ ^s3:// ]]; then
  echo "ERROR: Invalid S3 URI format. Must start with s3://" >&2
  exit 1
fi

# Preflight checks
echo "=== Preflight Checks ==="

# Check brotli
if ! command -v brotli &>/dev/null; then
  echo "ERROR: brotli not installed (brew install brotli)" >&2
  exit 1
fi
echo "✓ brotli: $(brotli --version 2>&1 | head -1)"

# Check aws
if ! command -v aws &>/dev/null; then
  echo "ERROR: aws CLI not installed (brew install awscli)" >&2
  exit 1
fi
echo "✓ aws: $(aws --version 2>&1)"

# Check op (1Password CLI)
if ! command -v op &>/dev/null; then
  echo "ERROR: 1Password CLI not installed (brew install 1password-cli)" >&2
  exit 1
fi
echo "✓ op: $(op --version 2>&1)"

# Check 1Password sign-in
if ! op whoami &>/dev/null; then
  echo "ERROR: Not signed in to 1Password. Run: op signin" >&2
  exit 1
fi
echo "✓ 1Password: Signed in"

echo ""
echo "=== Loading Credentials ==="

# Load credentials from 1Password
export AWS_ACCESS_KEY_ID=$(op read "op://$OP_VAULT/$OP_ITEM_ID/access key id")
export AWS_SECRET_ACCESS_KEY=$(op read "op://$OP_VAULT/$OP_ITEM_ID/secret access key")
export AWS_DEFAULT_REGION="$AWS_REGION"

echo "✓ AWS credentials loaded from 1Password"

# Verify AWS identity
IDENTITY=$(aws sts get-caller-identity --output json 2>&1)
if [[ "$IDENTITY" == *"error"* ]]; then
  echo "ERROR: AWS authentication failed" >&2
  echo "$IDENTITY" >&2
  exit 1
fi
ACCOUNT=$(echo "$IDENTITY" | jq -r '.Account')
echo "✓ AWS Account: $ACCOUNT"

echo ""
echo "=== Downloading Artifacts ==="

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Ensure S3 URI ends with /
S3_URI_CLEAN="${S3_URI%/}/"

# Download all artifacts
echo "Downloading from: $S3_URI_CLEAN"
echo "To: $OUTPUT_DIR/"
echo ""

if ! aws s3 sync "$S3_URI_CLEAN" "$OUTPUT_DIR/"; then
  echo "ERROR: S3 sync failed" >&2
  exit 1
fi

# Count downloaded files
TOTAL_FILES=$(find "$OUTPUT_DIR" -type f | wc -l | tr -d ' ')
BR_FILES=$(find "$OUTPUT_DIR" -name "*.br" -type f | wc -l | tr -d ' ')

echo ""
echo "Downloaded $TOTAL_FILES files ($BR_FILES Brotli-compressed)"

echo ""
echo "=== Decompressing Brotli Files ==="

# Decompress all .br files
DECOMPRESSED=0
for br_file in "$OUTPUT_DIR"/*.br; do
  if [[ -f "$br_file" ]]; then
    output_file="${br_file%.br}"
    echo "  Decompressing: $(basename "$br_file")"
    brotli -d -o "$output_file" "$br_file"
    ((DECOMPRESSED++))
  fi
done

if [[ $DECOMPRESSED -eq 0 ]]; then
  echo "  No .br files found to decompress"
else
  echo ""
  echo "Decompressed $DECOMPRESSED files"
fi

echo ""
echo "=== Retrieval Complete ==="
echo "Output directory: $OUTPUT_DIR"
echo ""

# Show manifest if available
if [[ -f "$OUTPUT_DIR/manifest.json" ]]; then
  echo "Manifest summary:"
  jq -r '
    "  Sessions: \(.total_sessions // "N/A")",
    "  Total lines: \(.total_lines // "N/A")",
    "  Chain depth: \(.chain_depth // "N/A")",
    "  First timestamp: \(.first_timestamp // "N/A")",
    "  Last timestamp: \(.last_timestamp // "N/A")",
    "  Project: \(.project_path // "N/A")"
  ' "$OUTPUT_DIR/manifest.json"
fi

echo ""
echo "Contents:"
ls -la "$OUTPUT_DIR/"
