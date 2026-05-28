#!/usr/bin/env bash
set -euo pipefail

# Initialize semantic-release in a project
# Level 4 (Project): Creates .releaserc.yml with optional extends
# See SKILL.md for complete 4-level architecture
# Usage:
#   ./init_project.sh [OPTIONS]
#
# Options:
#   --user              Use user config (@username/semantic-release-config)
#   --org ORG/CONFIG    Use org config (@org/config-name)
#   --inline            Use inline config (no extends)
#
# Examples:
#   ./init_project.sh --user
#   ./init_project.sh --org mycompany/semantic-release-config
#   ./init_project.sh --inline

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
TEMPLATES_DIR="$SKILL_DIR/assets/templates"

MODE=""
CONFIG_PACKAGE=""

# Check authentication (Priority 1: HTTPS + Token, Priority 2: SSH fallback)
# Per authentication.md (2025-12-19+): HTTPS-first is primary method
echo "🔍 Checking authentication..."
echo ""

# Priority 1: Check HTTPS + GH_TOKEN (per authentication.md 2025-12-19+)
echo "Priority 1: HTTPS + Token (primary)"
if git remote -v 2>/dev/null | grep -q "https://github.com"; then
    echo "✅ Git remote uses HTTPS"
    if gh api user --jq '.login' &>/dev/null; then
        ACCOUNT=$(gh api user --jq '.login')
        echo "✅ GH_TOKEN active for account: $ACCOUNT"
    else
        echo "⚠️  GH_TOKEN not set or invalid"
        echo "   Check mise [env] configuration for this directory"
        echo "   See: $SKILL_DIR/references/authentication.md"
    fi
elif git remote -v 2>/dev/null | grep -q "git@github.com"; then
    echo "ℹ️  Git remote uses SSH (legacy)"
    echo "   Consider: git-ssh-to-https (HTTPS-first recommended)"
    echo "   See: $SKILL_DIR/references/authentication.md"
    if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
        echo "✅ SSH authentication working"
    else
        echo "⚠️  SSH remote configured but authentication may not be working"
        echo "   Test: ssh -T git@github.com"
    fi
else
    echo "ℹ️  Not in a git repo yet, or no remote configured"
fi
echo ""

# Priority 2: Check GitHub CLI web authentication (for API operations)
echo "Priority 2: GitHub CLI (API operations)"
if command -v gh &> /dev/null; then
    if gh auth status &> /dev/null; then
        echo "✅ GitHub CLI authenticated (web-based)"
        echo "   ⚠️  AVOID creating manual tokens - gh CLI handles credentials"
    else
        echo "⚠️  GitHub CLI installed but not authenticated"
        echo "   Run: gh auth login"
        echo "   See: $SKILL_DIR/references/authentication.md"
        echo ""
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
else
    echo "⚠️  GitHub CLI (gh) not found"
    echo "   Install: brew install gh"
    echo "   Then run: gh auth login (web-based, AVOID manual tokens)"
    echo "   See: $SKILL_DIR/references/authentication.md"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
echo ""

# Priority 3: Check global semantic-release (macOS only - avoids Gatekeeper issues)
if [[ "$(uname)" == "Darwin" ]]; then
    echo "Priority 3: Global semantic-release (macOS Gatekeeper workaround)"
    if command -v semantic-release &> /dev/null; then
        echo "✅ semantic-release installed globally"
        echo "   Use 'semantic-release --no-ci' directly for local releases"
    else
        echo "⚠️  semantic-release not installed globally"
        echo "   macOS Gatekeeper blocks npx .node files. Install globally:"
        echo ""
        echo "   npm install -g semantic-release @semantic-release/changelog \\"
        echo "     @semantic-release/git @semantic-release/github @semantic-release/exec"
        echo ""
        echo "   Then clear quarantine (one-time after install or node upgrade):"
        echo "   xattr -r -d com.apple.quarantine ~/.local/share/mise/installs/node/"
        echo ""
        echo "   See: $SKILL_DIR/references/troubleshooting.md#macos-gatekeeper-blocks-node-files"
        echo ""
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    echo ""
fi

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --user)
            MODE="user"
            CONFIG_PACKAGE="@${USER}/semantic-release-config"
            shift
            ;;
        --org)
            MODE="org"
            CONFIG_PACKAGE="@$2"
            shift 2
            ;;
        --inline)
            MODE="inline"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo ""
            echo "Usage: $0 [--user | --org ORG/CONFIG | --inline]"
            exit 1
            ;;
    esac
done

# Default to inline if not specified
if [ -z "$MODE" ]; then
    MODE="inline"
fi

echo "==================================================================="
echo "semantic-release Project Initialization (Level 4)"
echo "==================================================================="
echo ""

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo "ERROR: package.json not found"
    echo "Run 'npm init' first"
    exit 1
fi

# Install semantic-release
echo "Installing semantic-release v25+..."
case $MODE in
    user|org)
        echo "  Mode: Shareable config ($CONFIG_PACKAGE)"
        npm install --save-dev semantic-release@^25.0.0 "$CONFIG_PACKAGE"
        ;;
    inline)
        echo "  Mode: Inline configuration"
        npm install --save-dev \
            semantic-release@^25.0.0 \
            @semantic-release/changelog@^6.0.3 \
            @semantic-release/commit-analyzer@^13.0.0 \
            @semantic-release/exec@^6.0.3 \
            @semantic-release/git@^10.0.1 \
            @semantic-release/github@^11.0.1 \
            @semantic-release/release-notes-generator@^14.0.1
        ;;
esac

# Configure package.json
echo "Configuring package.json..."
npm pkg set scripts.release="semantic-release --no-ci"
npm pkg set scripts.release:dry="semantic-release --no-ci --dry-run"
npm pkg set scripts.postrelease="git fetch origin main:refs/remotes/origin/main --no-tags || true"
npm pkg set version="0.0.0-development"
npm pkg set engines.node=">=22.14.0"

# Create .releaserc.yml with backup + traceability
# ADR: /docs/adr/2025-12-07-idempotency-backup-traceability.md
echo "Creating .releaserc.yml..."
BACKUP_REF="none"
if [ -f .releaserc.yml ]; then
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP=".releaserc.yml.bak.${TIMESTAMP}"
    cp .releaserc.yml "$BACKUP"
    BACKUP_REF="./$BACKUP"
    echo "INFO: Backed up existing .releaserc.yml to $BACKUP"
fi

case $MODE in
    user|org)
        cat > .releaserc.yml <<EOF
# Previous version: $BACKUP_REF
# Extends: $CONFIG_PACKAGE
# Level: Project (extends Level 2/3)
extends: "$CONFIG_PACKAGE"
EOF
        ;;
    inline)
        cat > .releaserc.yml <<EOF
# Previous version: $BACKUP_REF
# Inline configuration
# Level: Project (standalone)

branches:
  - main
  - name: beta
    prerelease: true

plugins:
  - "@semantic-release/commit-analyzer"
  - "@semantic-release/release-notes-generator"
  - - "@semantic-release/changelog"
    - changelogFile: CHANGELOG.md
  - "@semantic-release/exec"
  - - "@semantic-release/git"
    - assets:
        - CHANGELOG.md
        - package.json
  # Push commit and tags after @semantic-release/git creates them
  # Belt-and-suspenders: ensures push happens even in --no-ci mode
  - - "@semantic-release/exec"
    - successCmd: "/usr/bin/env bash -c 'git push --follow-tags origin main'"
  - "@semantic-release/github"
EOF
        ;;
esac

# Create GitHub Actions workflow
echo "Creating .github/workflows/release.yml..."
mkdir -p .github/workflows
cp "$TEMPLATES_DIR/github-workflow.yml" .github/workflows/release.yml

# Update .gitignore - exact line match to prevent false positives
# ADR: /docs/adr/2025-12-07-idempotency-backup-traceability.md
if [ -f .gitignore ]; then
    grep -qx "node_modules/" .gitignore || echo "node_modules/" >> .gitignore
else
    echo "node_modules/" > .gitignore
fi

echo ""
echo "==================================================================="
echo "✅ Project initialized successfully!"
echo "==================================================================="
echo ""
echo "Configuration Level: 4 (Project)"
case $MODE in
    user)
        echo "  Extends: Level 2 (User - $CONFIG_PACKAGE)"
        echo ""
        echo "  If $CONFIG_PACKAGE doesn't exist:"
        echo "    cd $SKILL_DIR"
        echo "    ./scripts/init_user_config.sh"
        ;;
    org)
        echo "  Extends: Level 3 (Organization - $CONFIG_PACKAGE)"
        echo ""
        echo "  If $CONFIG_PACKAGE doesn't exist:"
        echo "    cd $SKILL_DIR"
        echo "    ./scripts/create_org_config.sh ORG CONFIG"
        ;;
    inline)
        echo "  Standalone: No extends (all config in .releaserc.yml)"
        ;;
esac
echo ""
echo "Next steps:"
echo "  1. git add ."
echo "  2. git commit -m 'chore: setup semantic-release'"
echo "  3. git push origin main"
echo ""

# Detect mise-managed release workflow (Priority 1)
HAS_MISE_RELEASE=false
if command -v mise &>/dev/null && [[ -f ".mise.toml" ]]; then
    if grep -q '\[tasks\."release' .mise.toml 2>/dev/null || grep -q '\[tasks\.release\]' .mise.toml 2>/dev/null; then
        HAS_MISE_RELEASE=true
    fi
fi

if [[ "$HAS_MISE_RELEASE" == "true" ]]; then
    echo "✅ mise-managed release detected (.mise.toml)"
    echo ""
    echo "Local release (Priority 1 - mise):"
    echo "  mise run release:version    # Semantic-release version bump only"
    if grep -q '\[tasks\."release:full' .mise.toml 2>/dev/null; then
        echo "  mise run release:full       # Full workflow (version → build → smoke → publish)"
    fi
    echo ""
    echo "Alternative (Priority 2 - npm):"
    echo "  npm run release:dry   # Preview changes"
    echo "  npm run release       # Create release (auto-pushes)"
else
    echo "Local release (auto-pushes via successCmd + postrelease):"
    echo "  npm run release:dry   # Preview changes"
    echo "  npm run release       # Create release (auto-pushes)"
    echo ""
    echo "  Or with global install (macOS Gatekeeper workaround):"
    echo "  /usr/bin/env bash -c 'GITHUB_TOKEN=\$(gh auth token) semantic-release --no-ci'"
    echo ""
    echo "💡 TIP: Add mise tasks for integrated release workflow:"
    echo "  See: $SKILL_DIR/SKILL.md#mise-task-detection-priority-1-task-runner"
fi
echo ""
echo "CI release (GitHub Actions):"
echo "  Automatically runs on push to main"
echo ""
echo "Conventional Commits format:"
echo "  feat: → MINOR (0.1.0 → 0.2.0)"
echo "  fix: → PATCH (0.1.0 → 0.1.1)"
echo "  BREAKING CHANGE: → MAJOR (0.1.0 → 1.0.0)"
echo ""
echo "See: $SKILL_DIR/references/local-release-workflow.md for canonical 4-phase workflow"
echo ""
