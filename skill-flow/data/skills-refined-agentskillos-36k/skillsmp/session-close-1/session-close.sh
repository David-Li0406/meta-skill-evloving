#!/usr/bin/env bash
# ABOUTME: Wrapper for legacy Claude skill path; delegates to scripts/session-close.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "${SCRIPT_DIR}/../../../scripts/session-close.sh"
