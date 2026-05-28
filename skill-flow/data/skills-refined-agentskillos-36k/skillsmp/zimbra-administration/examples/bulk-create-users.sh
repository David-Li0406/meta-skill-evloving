#!/bin/bash
# Bulk create Zimbra users from CSV file
# CSV format: email,password,displayName,givenName,sn,cosId
#
# Usage: ./bulk-create-users.sh users.csv
#
# Example CSV:
# john@domain.com,SecurePass123,John Doe,John,Doe,cos-id-here
# jane@domain.com,SecurePass456,Jane Smith,Jane,Smith,cos-id-here

CSV_FILE="${1:-users.csv}"

if [ ! -f "$CSV_FILE" ]; then
    echo "Error: CSV file not found: $CSV_FILE"
    echo "Usage: $0 <csv-file>"
    exit 1
fi

# Skip header line and process each user
tail -n +2 "$CSV_FILE" | while IFS=',' read -r email password displayName givenName sn cosId; do
    # Skip empty lines
    [ -z "$email" ] && continue

    echo "Creating account: $email"

    # Build zmprov command
    cmd="zmprov ca '$email' '$password'"
    [ -n "$displayName" ] && cmd="$cmd displayName '$displayName'"
    [ -n "$givenName" ] && cmd="$cmd givenName '$givenName'"
    [ -n "$sn" ] && cmd="$cmd sn '$sn'"
    [ -n "$cosId" ] && cmd="$cmd zimbraCOSid '$cosId'"

    # Execute
    if eval "$cmd" 2>&1; then
        echo "  ✓ Created successfully"
    else
        echo "  ✗ Failed to create"
    fi
done

echo ""
echo "Bulk creation complete. Verify with: zmprov -l gaa <domain>"
