#!/bin/bash

# Setup Changesets for version management
# Usage: ./setup_changesets.sh

set -e

echo "📦 Setting up Changesets for version management"
echo ""

# Check if this is a Node.js project
if [ ! -f "package.json" ]; then
    echo "❌ No package.json found"
    echo "   Changesets requires a Node.js project"
    exit 1
fi

# Detect package manager
if [ -f "pnpm-lock.yaml" ]; then
    PKG_MGR="pnpm"
elif [ -f "yarn.lock" ]; then
    PKG_MGR="yarn"
elif [ -f "package-lock.json" ]; then
    PKG_MGR="npm"
else
    PKG_MGR="pnpm"  # Default
fi

echo "📦 Detected package manager: $PKG_MGR"
echo ""

# Check if changesets is installed
if command -v changeset &> /dev/null || [ -f "node_modules/.bin/changeset" ]; then
    echo "✓ @changesets/cli is already installed"
else
    echo "Installing @changesets/cli..."
    case $PKG_MGR in
        pnpm)
            pnpm add -D @changesets/cli
            ;;
        yarn)
            yarn add -D @changesets/cli
            ;;
        npm)
            npm install -D @changesets/cli
            ;;
    esac
    echo "✓ Installed @changesets/cli"
fi

echo ""

# Check if already initialized
if [ -d ".changeset" ]; then
    echo "✓ .changeset directory already exists"
    read -p "Reinitialize changesets? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Keeping existing configuration"
        exit 0
    fi
    rm -rf .changeset
fi

# Initialize changesets
echo "🔧 Initializing changesets..."
case $PKG_MGR in
    pnpm)
        pnpm changeset init
        ;;
    yarn)
        yarn changeset init
        ;;
    npm)
        npx changeset init
        ;;
esac

echo "✓ Changesets initialized"
echo ""

# Customize config for public packages
if [ -f ".changeset/config.json" ]; then
    echo "📝 Configuring for public npm packages..."

    # Use jq if available, otherwise sed
    if command -v jq &> /dev/null; then
        jq '.access = "public"' .changeset/config.json > .changeset/config.json.tmp
        mv .changeset/config.json.tmp .changeset/config.json
    else
        sed -i.bak 's/"access": "restricted"/"access": "public"/' .changeset/config.json
        rm -f .changeset/config.json.bak
    fi

    echo "✓ Configured for public access"
fi

# Add scripts to package.json
echo ""
echo "📝 Adding scripts to package.json..."

# Check if jq is available
if command -v jq &> /dev/null; then
    jq '.scripts.changeset = "changeset" |
        .scripts["changeset:version"] = "changeset version" |
        .scripts["changeset:publish"] = "changeset publish" |
        .scripts["changeset:status"] = "changeset status"' package.json > package.json.tmp
    mv package.json.tmp package.json
    echo "✓ Added changeset scripts"
else
    echo "⚠️  jq not found - please add scripts manually:"
    echo '  "changeset": "changeset",'
    echo '  "changeset:version": "changeset version",'
    echo '  "changeset:publish": "changeset publish",'
    echo '  "changeset:status": "changeset status"'
fi

echo ""
echo "✅ Changesets setup complete!"
echo ""
echo "📋 Next steps:"
echo "  1. Make code changes"
echo "  2. Run: $PKG_MGR changeset"
echo "  3. Commit the changeset file"
echo "  4. Merge to main"
echo "  5. Run: $PKG_MGR changeset version"
echo "  6. Run: $PKG_MGR changeset publish"
echo ""
echo "💡 For automated releases, see: references/version-management.md"
echo "   GitHub Actions workflow available in assets/workflows/"
