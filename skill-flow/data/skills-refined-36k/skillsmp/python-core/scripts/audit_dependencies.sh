#!/usr/bin/env bash
set -euo pipefail

echo "🔍 Auditing Python dependencies..."

if ! command -v pip-audit &> /dev/null; then
    echo "Installing pip-audit..."
    pip install pip-audit
fi

echo "Running pip-audit..."
pip-audit

echo "✅ Audit complete!"
