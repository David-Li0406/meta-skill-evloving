#!/bin/bash
# hive-node-setup.sh - Setup macmini as Hive worker node
# Run this ON macmini (the target VM)

set -e

echo "🔧 Hive Node Setup for $(hostname)"

# 1. Create systemd user directory
echo "📁 Creating systemd user config..."
mkdir -p ~/.config/systemd/user

# 2. Install protection slice
echo "🛡️ Installing claude.slice protection..."
cat > ~/.config/systemd/user/claude.slice << 'EOF'
[Slice]
Description=Claude Code Protection Slice
TasksMax=1
CPUQuota=80%
MemoryMax=8G
EOF

# Reload systemd
systemctl --user daemon-reload
echo "✓ systemd slice installed"

# 3. Verify claude is installed
echo "🔍 Checking Claude Code..."
if command -v claude &> /dev/null; then
    echo "✓ Claude Code: $(claude --version 2>/dev/null || echo 'installed')"
else
    echo "❌ Claude Code not found. Install with:"
    echo "   npm install -g @anthropic-ai/claude-code"
    exit 1
fi

# 4. Verify git
echo "🔍 Checking git..."
if command -v git &> /dev/null; then
    echo "✓ git: $(git --version)"
else
    echo "❌ git not found"
    exit 1
fi

# 5. Verify gh CLI
echo "🔍 Checking gh CLI..."
if command -v gh &> /dev/null; then
    echo "✓ gh: $(gh --version | head -1)"
else
    echo "⚠️ gh CLI not found (needed for PR creation)"
fi

# 6. Verify bd CLI
echo "🔍 Checking Beads..."
if command -v bd &> /dev/null; then
    echo "✓ bd: available"
else
    echo "⚠️ bd CLI not found (needed for status updates)"
fi

# 7. Clone/update affordabot repo
REPO_PATH="${HOME}/affordabot"
echo "📦 Setting up repo at $REPO_PATH..."
if [ -d "$REPO_PATH" ]; then
    cd "$REPO_PATH"
    git fetch origin
    echo "✓ Repo exists, fetched updates"
else
    git clone https://github.com/stars-end/affordabot.git "$REPO_PATH"
    echo "✓ Cloned repo"
fi

# 8. Summary
echo ""
echo "═══════════════════════════════════════"
echo "✅ Hive Node Setup Complete"
echo "═══════════════════════════════════════"
echo ""
echo "Protection:"
echo "  - systemd slice: TasksMax=1, CPU 80%, Mem 8G"
echo ""
echo "Next steps:"
echo "  1. Ensure SSH key access from orchestrator"
echo "  2. Test with: ssh macmini 'echo ok'"
echo "  3. Run dispatch from orchestrator"
echo ""
