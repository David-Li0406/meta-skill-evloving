#!/bin/bash
set -e

# Extract gameweek number from arguments
GAMEWEEK=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -g|--gameweek)
            GAMEWEEK="$2"
            shift 2
            ;;
        *)
            # If it's just a number, treat it as gameweek
            if [[ "$1" =~ ^[0-9]+$ ]]; then
                GAMEWEEK="$1"
            fi
            shift
            ;;
    esac
done

# Default to prompting if no gameweek specified
if [ -z "$GAMEWEEK" ]; then
    echo "Usage: deploy-gameweek <gameweek_number>"
    echo "Example: deploy-gameweek 22"
    exit 1
fi

echo "==================================================================="
echo "  🚀 DEPLOYING GAMEWEEK $GAMEWEEK"
echo "==================================================================="
echo

# Step 1: Run deployment script
echo "📦 Step 1: Building deployment package..."
python3 deploy-github-clean.py

# Step 2: Git operations
echo
echo "📝 Step 2: Committing changes..."

# Check if there are changes
if [[ -z $(git status -s) ]]; then
    echo "✓ No changes to commit (already up to date)"
else
    git add .
    git commit -m "Add GW${GAMEWEEK} data

- Final results and match scores
- Updated transfer history
- Player statistics and PL fixtures
- Generated summaries and AI roast

🤖 Generated with Claude Code
"
    echo "✓ Changes committed"
fi

# Step 3: Push to staging
echo
echo "📤 Step 3: Pushing to staging branch..."
git push origin staging
echo "✓ Pushed to staging"
echo "   Staging URL: Check your GitHub Pages staging site"

# Step 4: Ask about production
echo
read -p "🎯 Push to production (main branch)? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "📤 Pushing to production (main)..."
    git push origin main
    echo "✓ Pushed to main (production)"
    echo "   Production URL: Check your GitHub Pages site"
else
    echo "⏸️  Skipped production push"
    echo "   You can push manually later with: git push origin main"
fi

echo
echo "==================================================================="
echo "  ✅ DEPLOYMENT COMPLETE"
echo "==================================================================="
echo
echo "📊 GW${GAMEWEEK} is now deployed!"
echo "🌐 Check your GitHub Pages site for updates (may take 1-2 minutes)"
