# Agent Observability Auto-Start Configuration

## Overview
The agent observability services (server and client) have been configured to automatically start when your Mac boots up using macOS launchd.

## Services Configuration

### LaunchAgent Files
Two launchd plist files have been created in `~/Library/LaunchAgents/`:

1. **Server**: `com.pai.observability-server.plist`
   - Runs on: http://localhost:4000
   - Working directory: `~/.claude/skills/agent-observability/apps/server`
   - Logs: `~/.claude/skills/agent-observability/logs/server-*.log`

2. **Client**: `com.pai.observability-client.plist`
   - Runs on: http://localhost:5172 (or http://localhost:3000 depending on config)
   - Working directory: `~/.claude/skills/agent-observability/apps/client`
   - Logs: `~/.claude/skills/agent-observability/logs/client-*.log`

### Configuration Details
- **RunAtLoad**: `true` - Services start automatically on login
- **KeepAlive**: `true` - Services automatically restart if they crash
- **Environment**: PATH configured to include bun binary location

## Manual Service Management

### Start Services
```bash
~/.claude/skills/agent-observability/start-services.sh
```

### Stop Services
```bash
~/.claude/skills/agent-observability/stop-services.sh
```

### Check Service Status
```bash
# Check if services are running
ps aux | grep -E "(bun run dev)" | grep -v grep

# Check server
curl http://localhost:4000

# Check client
curl http://localhost:5172
```

### View Logs
```bash
# Real-time server logs
tail -f ~/.claude/skills/agent-observability/logs/server-stdout.log

# Real-time client logs
tail -f ~/.claude/skills/agent-observability/logs/client-stdout.log

# Error logs
tail -f ~/.claude/skills/agent-observability/logs/server-stderr.log
tail -f ~/.claude/skills/agent-observability/logs/client-stderr.log
```

## LaunchAgent Management

### Verify Configuration
```bash
# Check plist syntax
plutil -lint ~/Library/LaunchAgents/com.pai.observability-server.plist
plutil -lint ~/Library/LaunchAgents/com.pai.observability-client.plist

# List loaded services
launchctl list | grep com.pai
```

### Manual Load/Unload (if needed)
```bash
# Load services
launchctl load ~/Library/LaunchAgents/com.pai.observability-server.plist
launchctl load ~/Library/LaunchAgents/com.pai.observability-client.plist

# Unload services
launchctl unload ~/Library/LaunchAgents/com.pai.observability-server.plist
launchctl unload ~/Library/LaunchAgents/com.pai.observability-client.plist
```

### Disable Auto-Start
If you want to prevent services from starting automatically:
```bash
# Remove or rename the plist files
mv ~/Library/LaunchAgents/com.pai.observability-server.plist ~/Library/LaunchAgents/com.pai.observability-server.plist.disabled
mv ~/Library/LaunchAgents/com.pai.observability-client.plist ~/Library/LaunchAgents/com.pai.observability-client.plist.disabled
```

### Re-enable Auto-Start
```bash
# Restore the plist files
mv ~/Library/LaunchAgents/com.pai.observability-server.plist.disabled ~/Library/LaunchAgents/com.pai.observability-server.plist
mv ~/Library/LaunchAgents/com.pai.observability-client.plist.disabled ~/Library/LaunchAgents/com.pai.observability-client.plist
```

## Troubleshooting

### Services Not Starting on Boot
1. Check plist files exist and are valid:
   ```bash
   ls -la ~/Library/LaunchAgents/com.pai.observability-*.plist
   plutil -lint ~/Library/LaunchAgents/com.pai.observability-*.plist
   ```

2. Check logs for errors:
   ```bash
   tail -100 ~/.claude/skills/agent-observability/logs/server-stderr.log
   tail -100 ~/.claude/skills/agent-observability/logs/client-stderr.log
   ```

3. Verify bun is installed and accessible:
   ```bash
   which bun
   bun --version
   ```

### Services Keep Crashing
- Check error logs: `tail -f ~/.claude/skills/agent-observability/logs/*-stderr.log`
- Verify dependencies: `cd apps/server && bun install && cd ../client && bun install`
- Check port conflicts: `lsof -i :4000` and `lsof -i :5172`

### High CPU/Memory Usage
- KeepAlive is enabled, which means services restart automatically
- If you notice issues, you can temporarily disable auto-start and investigate
- Consider using the stop-services.sh script when not actively using observability

## Testing the Configuration

### Verify Auto-Start After Setup
The services are currently running manually. To test the auto-start configuration:

1. **Option 1: Reboot** (Full test)
   ```bash
   sudo reboot
   # After reboot, check: ps aux | grep "bun run dev"
   ```

2. **Option 2: Simulate user login** (Quick test)
   ```bash
   # Stop current services
   ~/.claude/skills/agent-observability/stop-services.sh

   # Load the LaunchAgents (simulates login)
   launchctl load ~/Library/LaunchAgents/com.pai.observability-server.plist
   launchctl load ~/Library/LaunchAgents/com.pai.observability-client.plist

   # Check if they started
   sleep 5
   curl http://localhost:4000
   curl http://localhost:5172
   ```

## Current Status

✅ **Plist files created and validated**
✅ **Services currently running manually**
✅ **Helper scripts created** (start-services.sh, stop-services.sh)
✅ **Logs directory configured**
⏳ **Auto-start will be active after next reboot**

The services are configured and will start automatically on the next system boot or user login.
