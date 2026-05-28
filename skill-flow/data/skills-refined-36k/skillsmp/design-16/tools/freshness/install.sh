#!/bin/bash
#
# install.sh - Install Design Ops freshness system
#
# Usage: ./tools/freshness/install.sh
#
# This script:
# 1. Creates directory structure
# 2. Initializes source registry
# 3. Installs launchd plist for monthly reminders
# 4. Runs initial scan

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DESIGN_OPS_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
PLIST_NAME="com.designops.freshness.plist"

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║       DESIGN OPS FRESHNESS SYSTEM INSTALLER                   ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ============================================================================
# Step 1: Create directory structure
# ============================================================================
echo -e "${BLUE}[1/5] Creating directory structure...${NC}"

DIRS=(
    "$DESIGN_OPS_ROOT/docs/freshness/discoveries"
    "$DESIGN_OPS_ROOT/docs/freshness/validated"
    "$DESIGN_OPS_ROOT/docs/freshness/impact"
    "$DESIGN_OPS_ROOT/docs/freshness/actions"
    "$DESIGN_OPS_ROOT/docs/freshness/reports"
    "$DESIGN_OPS_ROOT/docs/freshness/trends"
)

for dir in "${DIRS[@]}"; do
    mkdir -p "$dir"
    echo "  Created: $dir"
done

echo -e "${GREEN}  ✓ Directory structure created${NC}"

# ============================================================================
# Step 2: Initialize source registry
# ============================================================================
echo -e "${BLUE}[2/5] Initializing source registry...${NC}"

REGISTRY_FILE="$DESIGN_OPS_ROOT/config/source-registry.yaml"

if [[ ! -f "$REGISTRY_FILE" ]]; then
    cat > "$REGISTRY_FILE" << 'EOF'
# Design Ops Source Registry
# ==========================
# Tracks sources for freshness validation
# Updated automatically by freshness system

metadata:
  version: "1.0"
  created: "2026-01-19"
  last_updated: "2026-01-19"

# Tier 1: Anthropic Official (always trusted)
tier_1:
  - name: "Anthropic Documentation"
    url: "https://docs.anthropic.com"
    type: "documentation"
    check_frequency: "monthly"

  - name: "Anthropic Cookbook"
    url: "https://github.com/anthropics/anthropic-cookbook"
    type: "examples"
    check_frequency: "monthly"

  - name: "Model Context Protocol"
    url: "https://modelcontextprotocol.io"
    type: "specification"
    check_frequency: "monthly"

  - name: "Anthropic Research Blog"
    url: "https://www.anthropic.com/research"
    type: "research"
    check_frequency: "monthly"

# Tier 2: Validated Sources (proven reliable)
tier_2:
  # Add validated sources here as discovered
  # Format:
  # - name: "Source Name"
  #   url: "https://..."
  #   discovered_date: "YYYY-MM-DD"
  #   last_checked: "YYYY-MM-DD"
  #   reliability_score: 8  # 1-10
  #   validation_evidence: "Why we trust this"
  #   decay_rate: 0.5  # Points lost per month without revalidation

# Tier 3: Watching (potential, not yet validated)
tier_3:
  # Add sources to watch here
  # Format:
  # - name: "Source Name"
  #   url: "https://..."
  #   discovered_date: "YYYY-MM-DD"
  #   notes: "Why watching, what would validate it"

# Archived: Previously valid, now stale/deprecated
archived: []
EOF
    echo -e "${GREEN}  ✓ Source registry created${NC}"
else
    echo -e "${YELLOW}  Registry already exists, skipping${NC}"
fi

# ============================================================================
# Step 3: Install launchd plist
# ============================================================================
echo -e "${BLUE}[3/5] Installing launchd schedule...${NC}"

mkdir -p "$LAUNCH_AGENTS_DIR"

PLIST_FILE="$LAUNCH_AGENTS_DIR/$PLIST_NAME"

# Escape path for plist
ESCAPED_PATH=$(echo "$SCRIPT_DIR/run-monthly.sh" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')

cat > "$PLIST_FILE" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.designops.freshness</string>

    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$ESCAPED_PATH</string>
    </array>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Day</key>
        <integer>1</integer>
        <key>Hour</key>
        <integer>10</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>

    <key>StandardOutPath</key>
    <string>$HOME/Library/Logs/design-ops-freshness.log</string>

    <key>StandardErrorPath</key>
    <string>$HOME/Library/Logs/design-ops-freshness.log</string>

    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
EOF

echo "  Created: $PLIST_FILE"

# Load the plist
launchctl unload "$PLIST_FILE" 2>/dev/null || true
launchctl load "$PLIST_FILE"

echo -e "${GREEN}  ✓ Monthly schedule installed (1st of month at 10:00 AM)${NC}"

# ============================================================================
# Step 4: Make scripts executable
# ============================================================================
echo -e "${BLUE}[4/5] Making scripts executable...${NC}"

chmod +x "$SCRIPT_DIR"/*.sh 2>/dev/null || true
echo -e "${GREEN}  ✓ Scripts are executable${NC}"

# ============================================================================
# Step 5: Run initial scan
# ============================================================================
echo -e "${BLUE}[5/5] Running initial scan...${NC}"

"$SCRIPT_DIR/scan-design-ops.sh" --output "$DESIGN_OPS_ROOT/docs/freshness/current-state.md"

# Initialize last scan date
echo "$(date +%Y-%m-%d)" > "$DESIGN_OPS_ROOT/config/.last-freshness-scan"

# Create initial dashboard
cat > "$DESIGN_OPS_ROOT/docs/freshness/dashboard.md" << EOF
# Design Ops Freshness Dashboard

> Auto-updated by freshness system

---

## Current Status

| Metric | Value |
|--------|-------|
| Last Scan | $(date +%Y-%m-%d) |
| Health Score | - (run full scan) |
| Sources Monitored | 4 (Tier 1) |
| Pending Actions | 0 |

---

## Quick Actions

- Run freshness check: \`/design freshness full\`
- View current state: \`docs/freshness/current-state.md\`
- Check source health: \`./tools/freshness/check-source-health.sh\`

---

## Schedule

- **Monthly reminder**: 1st of each month at 10:00 AM
- **Manual run**: \`./tools/freshness/run-monthly.sh\`

---

## Recent Activity

| Date | Action | Result |
|------|--------|--------|
| $(date +%Y-%m-%d) | Initial install | Complete |

---

_Dashboard updated: $(date '+%Y-%m-%d %H:%M:%S')_
EOF

echo -e "${GREEN}  ✓ Initial scan complete${NC}"

# ============================================================================
# Summary
# ============================================================================
echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                   INSTALLATION COMPLETE                       ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BOLD}What was installed:${NC}"
echo "  • Directory structure in docs/freshness/"
echo "  • Source registry in config/source-registry.yaml"
echo "  • Monthly reminder (1st of month at 10:00 AM)"
echo "  • Initial state scan"
echo ""
echo -e "${BOLD}Next steps:${NC}"
echo "  1. Run your first freshness check:"
echo -e "     ${CYAN}/design freshness full${NC}"
echo ""
echo "  2. View the dashboard:"
echo -e "     ${CYAN}cat docs/freshness/dashboard.md${NC}"
echo ""
echo -e "${BOLD}Files created:${NC}"
echo "  • $DESIGN_OPS_ROOT/docs/freshness/"
echo "  • $DESIGN_OPS_ROOT/config/source-registry.yaml"
echo "  • $PLIST_FILE"
echo ""
echo -e "${BOLD}To uninstall:${NC}"
echo "  ./tools/freshness/uninstall.sh"
echo ""
