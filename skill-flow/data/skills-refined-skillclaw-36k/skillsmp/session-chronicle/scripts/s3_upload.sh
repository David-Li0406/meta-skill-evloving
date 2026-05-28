#!/usr/bin/env bash
# s3_upload.sh - Upload session chronicle artifacts to S3
# Usage: ./s3_upload.sh <artifact_dir> [finding_id]
#
# Uploads all artifacts from a session chronicle extraction to S3.
# Uses 1Password for credential injection.
# ADR: /docs/adr/2026-01-02-session-chronicle-s3-sharing.md

set -euo pipefail

ARTIFACT_DIR="${1:-}"
FINDING_ID="${2:-$(date +%Y%m%d-%H%M%S)}"

# S3 configuration
S3_BUCKET="eonlabs-findings"
S3_PREFIX="sessions"
AWS_REGION="us-west-2"
OP_VAULT="Claude Automation"
OP_ITEM_ID="ise47dxnkftmxopupffavsgby4"

if [[ -z "$ARTIFACT_DIR" ]]; then
  echo "Usage: $0 <artifact_dir> [finding_id]" >&2
  echo "" >&2
  echo "Arguments:" >&2
  echo "  artifact_dir  Directory containing session chronicle artifacts" >&2
  echo "  finding_id    Unique identifier for this finding (default: timestamp)" >&2
  echo "" >&2
  echo "Required tools: brotli, aws, op (1Password CLI)" >&2
  exit 1
fi

if [[ ! -d "$ARTIFACT_DIR" ]]; then
  echo "ERROR: Artifact directory not found: $ARTIFACT_DIR" >&2
  exit 1
fi

if [[ ! -f "$ARTIFACT_DIR/manifest.json" ]]; then
  echo "ERROR: manifest.json not found in $ARTIFACT_DIR" >&2
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
echo "=== Uploading Artifacts ==="

S3_DEST="s3://$S3_BUCKET/$S3_PREFIX/$FINDING_ID"

# Count artifacts
ARTIFACT_COUNT=$(find "$ARTIFACT_DIR" -type f | wc -l | tr -d ' ')
echo "Uploading $ARTIFACT_COUNT files to $S3_DEST"
echo ""

# Upload all artifacts
aws s3 sync "$ARTIFACT_DIR" "$S3_DEST/" --quiet

# List uploaded files
echo "Uploaded files:"
aws s3 ls "$S3_DEST/" --recursive | while read -r line; do
  echo "  $line"
done

# Update manifest with S3 location
MANIFEST_TMP=$(mktemp)
jq --arg s3_location "$S3_DEST" \
   --arg bucket "$S3_BUCKET" \
   --arg prefix "$S3_PREFIX/$FINDING_ID" \
   --arg uploaded_at "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
   '. + {
     s3_location: $s3_location,
     s3_bucket: $bucket,
     s3_prefix: $prefix,
     uploaded_at: $uploaded_at
   }' "$ARTIFACT_DIR/manifest.json" > "$MANIFEST_TMP"

# Upload updated manifest
aws s3 cp "$MANIFEST_TMP" "$S3_DEST/manifest.json" --quiet
rm "$MANIFEST_TMP"

echo ""
echo "=== Upload Complete ==="
echo "S3 Location: $S3_DEST"
echo ""
echo "Retrieval command (requires 1Password access):"
echo ""
cat << 'RETRIEVAL_TEMPLATE'
/usr/bin/env bash << 'RETRIEVE_EOF'
export AWS_ACCESS_KEY_ID=$(op read "op://Claude Automation/ise47dxnkftmxopupffavsgby4/access key id")
export AWS_SECRET_ACCESS_KEY=$(op read "op://Claude Automation/ise47dxnkftmxopupffavsgby4/secret access key")
export AWS_DEFAULT_REGION="us-west-2"
RETRIEVAL_TEMPLATE
echo "aws s3 sync $S3_DEST/ ./artifacts/"
echo "for f in ./artifacts/*.br; do brotli -d \"\$f\"; done"
echo "RETRIEVE_EOF"

# Output S3 location for piping to other scripts
echo ""
echo "SESSION_CHRONICLE_S3=$S3_DEST"
