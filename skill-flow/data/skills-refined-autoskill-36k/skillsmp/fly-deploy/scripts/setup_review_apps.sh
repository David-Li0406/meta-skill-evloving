#!/bin/bash

# Setup GitHub Actions workflow for fly.io review apps
# Usage: ./setup_review_apps.sh [--org ORG_NAME] [--region REGION]

set -e

ORG="personal"
REGION="ord"
CONFIG_FILE="fly.toml"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --org)
      ORG="$2"
      shift 2
      ;;
    --region)
      REGION="$2"
      shift 2
      ;;
    --config)
      CONFIG_FILE="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 [--org ORG_NAME] [--region REGION] [--config CONFIG_FILE]"
      exit 1
      ;;
  esac
done

echo "🚀 Setting up fly.io review apps workflow"
echo "   Organization: $ORG"
echo "   Region: $REGION"
echo "   Config: $CONFIG_FILE"
echo ""

# Create .github/workflows directory if it doesn't exist
mkdir -p .github/workflows

# Create review apps workflow
cat > .github/workflows/review-apps.yml << 'EOF'
name: Review Apps

on:
  pull_request:
    types: [opened, reopened, synchronize, closed]

env:
  FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}

jobs:
  review-app:
    runs-on: ubuntu-latest

    # Only run for PRs from the same repository (not forks)
    if: github.event.pull_request.head.repo.full_name == github.repository

    steps:
      - uses: actions/checkout@v4

      - name: Deploy review app
        uses: superfly/fly-pr-review-apps@1.2.0
        with:
          region: __REGION__
          org: __ORG__
EOF

# Replace placeholders
sed -i.bak "s/__REGION__/$REGION/g" .github/workflows/review-apps.yml
sed -i.bak "s/__ORG__/$ORG/g" .github/workflows/review-apps.yml
rm .github/workflows/review-apps.yml.bak 2>/dev/null || true

echo "✅ Created .github/workflows/review-apps.yml"
echo ""

# Create optional fly.review.toml if fly.toml exists
if [ -f "$CONFIG_FILE" ]; then
  echo "📝 Creating fly.review.toml for review app configuration..."

  cat > fly.review.toml << 'EOF'
# Review app configuration (optimized for low cost)
app = "${FLY_APP_NAME}"
primary_region = "__REGION__"

[build]
  dockerfile = "Dockerfile"

[env]
  NODE_ENV = "staging"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = "stop"
  auto_start_machines = true
  min_machines_running = 0  # Scale to zero to save costs

[[vm]]
  memory = "256mb"  # Minimal resources for review apps
  cpus = 1
EOF

  sed -i.bak "s/__REGION__/$REGION/g" fly.review.toml
  rm fly.review.toml.bak 2>/dev/null || true

  echo "✅ Created fly.review.toml"
  echo ""

  # Update workflow to use custom config
  cat >> .github/workflows/review-apps.yml << 'EOF'
          config: fly.review.toml
EOF
fi

echo "🔑 Next steps:"
echo ""
echo "1. Create a fly.io API token:"
echo "   fly tokens create deploy"
echo ""
echo "2. Add the token to GitHub secrets:"
echo "   - Go to your repository on GitHub"
echo "   - Settings → Secrets and variables → Actions"
echo "   - New repository secret: FLY_API_TOKEN"
echo "   - Paste your token"
echo ""
echo "3. (Optional) Configure staging secrets for review apps:"
echo "   - Go to GitHub repository secrets"
echo "   - Add secrets like STAGING_DATABASE_URL, STAGING_API_KEY, etc."
echo "   - Update the workflow to pass these secrets to the action"
echo ""
echo "4. Push changes and create a pull request to test!"
echo ""
echo "📚 For more details, see: references/github-integration.md"
