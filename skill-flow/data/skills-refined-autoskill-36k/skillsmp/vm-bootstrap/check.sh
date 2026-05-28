#!/usr/bin/env bash
# vm-bootstrap/check.sh - Wrapper for verify.sh check mode
# This is a convenience wrapper that calls verify.sh in check mode

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/verify.sh" check
