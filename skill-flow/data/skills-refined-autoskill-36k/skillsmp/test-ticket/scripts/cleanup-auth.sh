#!/bin/bash
# cleanup-auth.sh
# Cleans up authentication state when tests fail with 401 errors
# Zero context cost - executed, not loaded into conversation

set -e

AUTH_DIR="${1:-.auth}"

if [ ! -d "$AUTH_DIR" ]; then
    echo "Auth directory not found: $AUTH_DIR"
    echo "Nothing to clean up."
    exit 0
fi

echo "Cleaning up authentication state..."
echo "Directory: $AUTH_DIR"

# List files to be removed
echo ""
echo "Files to remove:"
ls -la "$AUTH_DIR"

# Confirm and remove
echo ""
read -p "Remove all auth state files? (y/N) " confirm

if [[ "$confirm" =~ ^[Yy]$ ]]; then
    rm -rf "$AUTH_DIR"
    echo "Auth state cleaned up successfully."
    echo ""
    echo "Next steps:"
    echo "1. Run: npx playwright test --project=setup"
    echo "2. Or let the test-ticket workflow recreate auth"
else
    echo "Cleanup cancelled."
fi

exit 0
