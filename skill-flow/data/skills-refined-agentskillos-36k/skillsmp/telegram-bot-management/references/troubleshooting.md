**Skill**: [Telegram Bot Management](../SKILL.md)


If you receive "CRITICAL: Crash Loop Detected" in Telegram:

1. Check Telegram alert for error context
2. Review logs: `bot logs`
3. Fix the issue in code
4. Save file (auto-reloads)
5. Restart counter resets after 5 min stability

### Code Changes Not Reloading

```bash
# Verify watchexec is running
bot status  # Should show watchexec process

# Check watched directories
ps aux | grep watchexec  # Should show --watch paths

# Manual restart if needed
bot restart
```

### Multiple PIDs Normal

When you run `bot status`, you'll see 6-7 PIDs:

```
launchd (PID 1)
  └─> run-bot-prod-watchexec.sh (PID XXXXX)
      └─> watchexec (PID XXXXX)
          └─> bot-wrapper-prod.sh (PID XXXXX)
              └─> doppler (PID XXXXX)
                  └─> uv (PID XXXXX)
                      └─> python3 (PID XXXXX)
```

**This is NORMAL!** It's a parent→child process chain, not multiple instances.

### PID File Errors

```bash
# Clean stale PID files
rm -f ~/.claude/automation/claude-orchestrator/state/bot.pid
rm -f ~/.claude/automation/claude-orchestrator/state/watchexec.pid

# Restart bot
bot restart
```

## File Locations

- **Bot script**: `automation/claude-orchestrator/runtime/bot/multi-workspace-bot.py`
- **Service manager**: `automation/claude-orchestrator/runtime/bot/bot-service.sh`
- **Production runner**: `automation/claude-orchestrator/runtime/bot/run-bot-prod-watchexec.sh`
- **Crash monitor**: `automation/claude-orchestrator/runtime/bot/bot-wrapper-prod.sh`
- **PID files**: `automation/claude-orchestrator/state/{watchexec,bot}.pid`
- **Launchd logs**: `~/.claude/automation/claude-orchestrator/logs/telegram-bot-launchd*.log`
- **Bot logs**: `~/.claude/automation/claude-orchestrator/logs/telegram-handler.log`

## Shell Aliases

After sourcing `~/.claude/sage-aliases/aliases/bot-management.sh`:

```bash
bot status          # Show status
bot logs            # Tail logs
bot restart         # Restart service
bot stop            # Stop service
bot start           # Start service
bot-pids            # Show PIDs
bot-state-count     # State directory stats
bot-logs-errors     # Show recent errors
```

## References

- **Bot README**: `automation/claude-orchestrator/runtime/bot/README.md`
- **CHANGELOG**: `automation/claude-orchestrator/CHANGELOG.md`
- **CLAUDE.md**: Always use production mode (launchd + watchexec)

## Version History

- **v5.8.0** (2025-10-30): Production-only mode
- **v5.7.0** (2025-10-30): Full supervision (launchd + watchexec)
- **v5.6.0** (2025-10-30): Dev lifecycle management (archived)

## Important Notes

**No Development Mode** - As of v5.8.0, production mode provides all features:
- Auto-reload for rapid iteration (dev need)
- Full supervision for reliability (prod need)
- Crash detection for debugging (dev need)
- Always-on operation (prod need)

**Always Running** - The bot runs continuously. To stop completely:
- Temporary: `bot stop`
- Permanent: `bot uninstall`
