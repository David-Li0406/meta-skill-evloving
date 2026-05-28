#!/usr/bin/env bash
# Example Setup Script
# Shows how to set up dual-channel watchexec notifications for your project

set -euo pipefail

# ============================================================================
# STEP 1: Install Dependencies
# ============================================================================

echo "📦 Installing dependencies..."

# Ensure watchexec is installed
if ! command -v watchexec >/dev/null 2>&1; then
    echo "Installing watchexec..."
    # macOS
    if [[ "$(uname)" == "Darwin" ]]; then
        brew install watchexec
    # Linux
    else
        cargo install watchexec-cli
    fi
fi

# Ensure jq is installed (for parsing watchexec JSON)
if ! command -v jq >/dev/null 2>&1; then
    echo "Installing jq..."
    if [[ "$(uname)" == "Darwin" ]]; then
        brew install jq
    else
        sudo apt-get install -y jq || sudo yum install -y jq
    fi
fi

# ============================================================================
# STEP 2: Set Up Credentials
# ============================================================================

echo ""
echo "🔑 Setting up credentials..."
echo ""
echo "Choose credential management method:"
echo "  1) Environment variables (simple)"
echo "  2) Doppler (recommended for production)"
echo "  3) macOS Keychain"
read -p "Enter choice [1-3]: " CRED_METHOD

case "$CRED_METHOD" in
    1)
        echo ""
        echo "Add these to your shell profile (~/.bashrc, ~/.zshrc):"
        echo ""
        echo "export TELEGRAM_BOT_TOKEN='your_bot_token_here'"
        echo "export TELEGRAM_CHAT_ID='your_chat_id_here'"
        echo "export PUSHOVER_APP_TOKEN='your_app_token_here'"
        echo "export PUSHOVER_USER_KEY='your_user_key_here'"
        echo "export PUSHOVER_DEVICE='device_name'"
        ;;
    2)
        echo ""
        echo "Install Doppler CLI:"
        echo "  brew install dopplerhq/cli/doppler"
        echo ""
        echo "Then configure secrets:"
        echo "  doppler secrets set TELEGRAM_BOT_TOKEN"
        echo "  doppler secrets set TELEGRAM_CHAT_ID"
        echo "  doppler secrets set PUSHOVER_APP_TOKEN"
        echo "  doppler secrets set PUSHOVER_USER_KEY"
        echo ""
        echo "Run your script with:"
        echo "  doppler run -- watchexec --restart -- ./bot-wrapper.sh"
        ;;
    3)
        echo ""
        echo "Store in macOS Keychain:"
        echo "  security add-generic-password -s 'telegram-bot-token' -a '$USER' -w 'your_token'"
        echo "  security add-generic-password -s 'telegram-chat-id' -a '$USER' -w 'your_chat_id'"
        echo "  security add-generic-password -s 'pushover-app-token' -a '$USER' -w 'your_token'"
        echo "  security add-generic-password -s 'pushover-user-key' -a '$USER' -w 'your_key'"
        echo ""
        echo "Then load in scripts:"
        echo "  export TELEGRAM_BOT_TOKEN=\$(security find-generic-password -s 'telegram-bot-token' -a '$USER' -w)"
        ;;
esac

# ============================================================================
# STEP 3: Copy Example Scripts
# ============================================================================

echo ""
echo "📋 Copy example scripts to your project:"
echo ""
echo "  cp notify-restart.sh /path/to/your/project/"
echo "  cp bot-wrapper.sh /path/to/your/project/"
echo "  chmod +x /path/to/your/project/*.sh"
echo ""

# ============================================================================
# STEP 4: Configure Paths
# ============================================================================

echo "📝 Edit bot-wrapper.sh to configure:"
echo ""
echo "  MAIN_SCRIPT='./your-script.py'  # Your main process"
echo "  WATCH_DIRS=('./src' './lib')     # Directories to watch"
echo "  BOT_LOG='./logs/app.log'         # Your log file"
echo ""

# ============================================================================
# STEP 5: Run with watchexec
# ============================================================================

echo "▶️  Run your process with watchexec:"
echo ""
echo "  watchexec --restart --watch ./src --exts py -- ./bot-wrapper.sh"
echo ""
echo "Or run the wrapper directly (for testing):"
echo ""
echo "  ./bot-wrapper.sh"
echo ""

# ============================================================================
# STEP 6: Test Notifications
# ============================================================================

echo "🧪 Test notifications manually:"
echo ""
echo "  ./notify-restart.sh startup 0"
echo "  ./notify-restart.sh code_change 0"
echo "  ./notify-restart.sh crash 1"
echo ""

# ============================================================================
# STEP 7: systemd Service (Optional, Linux only)
# ============================================================================

if [[ "$(uname)" == "Linux" ]]; then
    echo "🔧 Create systemd service (optional):"
    echo ""
    echo "File: /etc/systemd/system/myapp-watchexec.service"
    echo ""
    cat <<'SYSTEMD_EOF'
[Unit]
Description=My App with watchexec monitoring
After=network.target

[Service]
Type=simple
User=myuser
WorkingDirectory=/path/to/project
Environment="TELEGRAM_BOT_TOKEN=your_token"
Environment="TELEGRAM_CHAT_ID=your_chat_id"
Environment="PUSHOVER_APP_TOKEN=your_token"
Environment="PUSHOVER_USER_KEY=your_key"
ExecStart=/usr/local/bin/watchexec --restart --watch ./src --exts py -- ./bot-wrapper.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SYSTEMD_EOF
    echo ""
    echo "Enable and start:"
    echo "  sudo systemctl enable myapp-watchexec"
    echo "  sudo systemctl start myapp-watchexec"
    echo ""
fi

# ============================================================================
# DONE
# ============================================================================

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Configure credentials"
echo "  2. Copy and customize scripts"
echo "  3. Test notifications manually"
echo "  4. Run with watchexec"
echo ""
