# Troubleshooting

Common issues and solutions for claude-bell.

## Quick Diagnostics

Always start with:

```bash
cb doctor
```

This checks configuration, aliases, and system status.

## Common Issues

### Notifications Not Appearing

**Symptoms:** Command runs without error but no notification appears.

**Solutions:**

1. Check notification permissions:
   - Open System Preferences > Notifications
   - Find your terminal app (Terminal, iTerm2, etc.)
   - Ensure "Allow Notifications" is enabled
   - Set alert style to "Alerts" for interactive notifications

2. Check Do Not Disturb:
   - Click the notification icon in menu bar
   - Ensure DND is not enabled

3. Verify with simple test:
   ```bash
   cb -t "Test" -m "Hello"
   ```

### Interactive Notifications Dismiss Immediately

**Symptoms:** Notification with buttons disappears before you can click.

**Solutions:**

1. Change alert style:
   - System Preferences > Notifications > [Terminal App]
   - Set to "Alerts" instead of "Banners"

2. Use `--persistent` flag:
   ```bash
   cb -t "Confirm" -a "Yes,No" --persistent
   ```

### Sound Not Playing

**Symptoms:** Notification appears but no sound.

**Solutions:**

1. Check system volume is not muted

2. Verify sound exists:
   ```bash
   # For system sounds
   ls /System/Library/Sounds/

   # For aliases
   cb sound doctor
   ```

3. Test with known system sound:
   ```bash
   cb -t "Test" --sound Glass
   ```

4. Check sound alias:
   ```bash
   cb sound list
   ```

### Template Not Found

**Symptoms:** Error "Template not found: name"

**Solutions:**

1. List available templates:
   ```bash
   cb template list
   ```

2. Validate templates:
   ```bash
   cb template validate --all
   ```

3. Check template file exists:
   ```bash
   ls ~/.config/claude-bell/templates/
   ```

### Alias Not Found

**Symptoms:** Error "Alias not found: @name"

**Solutions:**

1. List aliases:
   ```bash
   cb sound list  # For sound aliases
   cb icon list   # For icon aliases
   ```

2. Check alias health:
   ```bash
   cb sound doctor
   cb icon doctor
   ```

3. Prune invalid aliases:
   ```bash
   cb sound prune aliases
   cb icon prune aliases
   ```

### Configuration Errors

**Symptoms:** Error parsing or validating configuration.

**Solutions:**

1. Validate configuration:
   ```bash
   cb config validate
   ```

2. View current configuration:
   ```bash
   cb config show --pretty
   ```

3. Reset to defaults:
   ```bash
   cb config reset
   ```

4. Check JSON syntax manually:
   ```bash
   cat ~/.config/claude-bell/config.json | python -m json.tool
   ```

### Timeout Not Working

**Symptoms:** Notification doesn't auto-dismiss after timeout.

**Solutions:**

1. Verify timeout format:
   ```bash
   # Correct formats
   --timeout 30s   # 30 seconds
   --timeout 5m    # 5 minutes
   --timeout 1h    # 1 hour

   # Incorrect formats
   --timeout 30    # Missing unit
   --timeout 5min  # Wrong unit
   ```

2. Provide default value:
   ```bash
   cb -t "Test" -a "Yes,No" --timeout 30s --default "No"
   ```

## Exit Code Reference

| Code | Meaning | Typical Cause |
|------|---------|---------------|
| 0 | Success | User clicked action or replied |
| 1 | Timeout | User didn't respond in time |
| 2 | Dismissed | User dismissed notification |
| 3 | User error | Invalid arguments, missing template |
| 4 | System error | Permission denied, notification service unavailable |
| 5 | App error | Bug in claude-bell |

### Checking Exit Codes

```bash
cb -t "Test" -a "Yes,No"
echo "Exit code: $?"
```

## Debug Mode

Enable verbose logging:

```bash
# Debug level
cb -t "Test" --log-level debug

# Trace level (most verbose)
cb -t "Test" --log-level trace
```

## Log Locations

Logs can be directed to different targets:

```bash
# Log to stderr
cb -t "Test" --json logs 2>debug.log

# JSON output includes more details
cb -t "Test" --json stdout --pretty
```

## File Locations

| File | Location |
|------|----------|
| Configuration | `~/.config/claude-bell/config.json` |
| Templates | `~/.config/claude-bell/templates/templates.json` |
| Sound aliases | `~/.config/claude-bell/sounds/aliases.json` |
| Cached sounds | `~/.config/claude-bell/sounds/files/` |
| Icon aliases | `~/.config/claude-bell/icons/aliases.json` |

## Resetting Everything

If all else fails, reset to clean state:

```bash
# Backup current config
cp -r ~/.config/claude-bell ~/.config/claude-bell.backup

# Remove configuration
rm -rf ~/.config/claude-bell

# Run setup again
cb setup
```

## Reporting Bugs

If you encounter exit code 5 (App error), please report:

1. Command that caused the error
2. Output of `cb doctor`
3. macOS version
4. Architecture (Intel or Apple Silicon)
5. Any error messages

Include debug output:
```bash
cb [your command] --log-level trace 2>&1 | tee bug-report.txt
```
