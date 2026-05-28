#!/usr/bin/env bash
set -euo pipefail

# Audit Rust dependencies for security vulnerabilities and license issues

echo "🔍 Auditing Rust dependencies..."

# Check if cargo-audit is installed
if ! command -v cargo-audit &> /dev/null; then
    echo "cargo-audit not found. Installing..."
    cargo install cargo-audit
fi

# Check if cargo-deny is installed
if ! command -v cargo-deny &> /dev/null; then
    echo "cargo-deny not found. Installing..."
    cargo install cargo-deny
fi

# Run cargo-audit
echo ""
echo "Running cargo-audit (security vulnerabilities)..."
cargo audit

# Run cargo-deny if deny.toml exists
if [[ -f deny.toml ]]; then
    echo ""
    echo "Running cargo-deny (licenses, bans, sources)..."
    cargo deny check
else
    echo ""
    echo "⚠️  deny.toml not found. Skipping cargo-deny check."
    echo "   Create deny.toml with: cargo deny init"
fi

# Show outdated dependencies
if command -v cargo-outdated &> /dev/null; then
    echo ""
    echo "Checking for outdated dependencies..."
    cargo outdated
else
    echo ""
    echo "💡 Install cargo-outdated to check for updates:"
    echo "   cargo install cargo-outdated"
fi

echo ""
echo "✅ Dependency audit complete!"
