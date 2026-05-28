#!/bin/bash
# Sign a transaction using Sigil
# Usage: ./sign-tx.sh --hash <HASH> --chain-id <CHAIN_ID> --description <DESC>

set -e

SOCKET_PATH="${SIGIL_SOCKET:-/tmp/sigil.sock}"

# Parse arguments
HASH=""
CHAIN_ID=""
DESCRIPTION=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --hash)
            HASH="$2"
            shift 2
            ;;
        --chain-id)
            CHAIN_ID="$2"
            shift 2
            ;;
        --description)
            DESCRIPTION="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 --hash <HASH> --chain-id <CHAIN_ID> --description <DESC>"
            exit 1
            ;;
    esac
done

# Validate arguments
if [[ -z "$HASH" || -z "$CHAIN_ID" || -z "$DESCRIPTION" ]]; then
    echo "Error: Missing required arguments"
    echo "Usage: $0 --hash <HASH> --chain-id <CHAIN_ID> --description <DESC>"
    exit 1
fi

# Remove 0x prefix if present
HASH="${HASH#0x}"

# Check daemon is running
if ! pgrep -x sigil-daemon > /dev/null 2>&1; then
    echo "❌ Sigil daemon is not running"
    echo "   Start with: sigil-daemon"
    exit 1
fi

# Check disk status first
echo "Checking disk status..."
DISK_STATUS=$(echo '{"type":"GetDiskStatus"}' | nc -U "$SOCKET_PATH" 2>/dev/null)

DETECTED=$(echo "$DISK_STATUS" | jq -r '.detected // false')
VALID=$(echo "$DISK_STATUS" | jq -r '.is_valid // false')
REMAINING=$(echo "$DISK_STATUS" | jq -r '.presigs_remaining // 0')

if [[ "$DETECTED" != "true" ]]; then
    echo "❌ No signing disk detected"
    echo "   Please insert your Sigil floppy disk"
    exit 1
fi

if [[ "$VALID" != "true" ]]; then
    echo "❌ Disk is not valid for signing"
    echo "   It may be expired or require reconciliation"
    exit 1
fi

if [[ "$REMAINING" -lt 1 ]]; then
    echo "❌ No presignatures remaining"
    echo "   Generate a new disk from your mother device"
    exit 1
fi

# Perform signing
echo "✓ Disk ready ($REMAINING presigs remaining)"
echo "Signing..."

SIGN_REQUEST=$(cat <<EOF
{
  "type": "Sign",
  "message_hash": "$HASH",
  "chain_id": $CHAIN_ID,
  "description": "$DESCRIPTION"
}
EOF
)

SIGN_RESULT=$(echo "$SIGN_REQUEST" | nc -U "$SOCKET_PATH" 2>/dev/null)

# Check for error
if echo "$SIGN_RESULT" | jq -e '.type == "Error"' > /dev/null 2>&1; then
    ERROR_MSG=$(echo "$SIGN_RESULT" | jq -r '.message')
    echo "❌ Signing failed: $ERROR_MSG"
    exit 1
fi

# Extract signature components
SIGNATURE=$(echo "$SIGN_RESULT" | jq -r '.signature')
PRESIG_INDEX=$(echo "$SIGN_RESULT" | jq -r '.presig_index')
PROOF_HASH=$(echo "$SIGN_RESULT" | jq -r '.proof_hash')

# Split signature into r and s (each 32 bytes = 64 hex chars)
R="${SIGNATURE:0:64}"
S="${SIGNATURE:64:64}"

echo ""
echo "✓ Signing... ✓ Proving... ✓ Done"
echo ""
echo "Signature Details:"
echo "├─ Signature: 0x$SIGNATURE"
echo "├─ r: 0x$R"
echo "├─ s: 0x$S"
echo "├─ Presig Index: $PRESIG_INDEX"
echo "└─ Proof Hash: 0x$PROOF_HASH"
echo ""
echo "Logged to disk. You may remove it after broadcasting."
