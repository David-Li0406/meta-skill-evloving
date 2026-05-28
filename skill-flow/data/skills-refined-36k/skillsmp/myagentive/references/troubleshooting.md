# MyAgentive Troubleshooting Guide

## Configuration Issues

### Config file not found

**Symptom:** Error message about missing config or setup wizard runs unexpectedly.

**Solution:**
```bash
# Check if config exists
ls -la ~/.myagentive/config

# If missing, run MyAgentive to trigger setup wizard
bun run dev
# Or for binary:
myagentive
```

### View current configuration

```bash
cat ~/.myagentive/config
```

### Reset configuration

```bash
# Remove config to re-run setup wizard
rm ~/.myagentive/config

# Then start MyAgentive
bun run dev
```

### Invalid config format

**Symptom:** Variables not being read correctly.

**Check for:**
- No quotes around values: `KEY=value` not `KEY="value"`
- No trailing spaces
- Each variable on its own line
- No blank lines with spaces

---

## Telegram Issues

### Bot not responding

**Possible causes:**

1. **Invalid bot token:**
   ```bash
   # Check token format (should contain colon)
   grep TELEGRAM_BOT_TOKEN ~/.myagentive/config
   ```
   - Get new token from @BotFather if needed

2. **Wrong user ID:**
   ```bash
   # Check user ID is numeric (not @username)
   grep TELEGRAM_USER_ID ~/.myagentive/config
   ```
   - Get correct ID from @userinfobot

3. **Bot not started:**
   - Open Telegram chat with your bot
   - Send `/start` command

4. **Server not running:**
   ```bash
   # Check if MyAgentive is running
   ps aux | grep myagentive
   ```

### "User not authorised" error

**Cause:** Your Telegram user ID doesn't match config.

**Solution:**
1. Get your numeric user ID from @userinfobot
2. Update config:
   ```bash
   # Edit the config file
   nano ~/.myagentive/config
   # Change TELEGRAM_USER_ID to correct value
   ```
3. Restart MyAgentive

### Bot messages not appearing

**Possible causes:**

1. **Response timeout:**
   - Default is 60 minutes for long operations
   - Check `TELEGRAM_RESPONSE_TIMEOUT_MINUTES` in config

2. **Bot blocked:**
   - Unblock the bot in Telegram settings
   - Start a new chat with the bot

3. **Network issues:**
   - Check internet connectivity
   - Telegram servers may be temporarily unavailable

### Voice messages not transcribing

**Cause:** Missing Deepgram API key.

**Solution:**
1. Create account at https://deepgram.com ($200 free credit)
2. Get API key from Console > API Keys
3. Add to config:
   ```bash
   echo "DEEPGRAM_API_KEY=your_key" >> ~/.myagentive/config
   ```
4. Restart MyAgentive

---

## Claude Code Integration Issues

### "Claude Code not found" error

**Cause:** Claude CLI not installed or not in PATH.

**Solution:**
```bash
# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Login
claude login

# Verify installation
which claude
claude --version
```

**Paths searched by MyAgentive:**
- `/usr/local/bin/claude`
- `~/.local/bin/claude`
- `~/.claude/local/claude`
- nvm paths (if using nvm)

**Source:** `server/core/ai-client.ts` lines 144-161

### Claude responses failing

**Possible causes:**

1. **Not logged in to Claude:**
   ```bash
   claude login
   ```

2. **Subscription expired:**
   - Check Claude subscription status
   - Consider adding `ANTHROPIC_API_KEY` for pay-per-use

3. **Rate limits:**
   - Wait a few minutes and retry
   - Consider using a different model (`/model haiku`)

---

## Web Interface Issues

### Cannot access web interface

**Check server is running:**
```bash
curl http://localhost:3847/health
```

**Check correct port:**
```bash
grep PORT ~/.myagentive/config
# Default is 3847
```

**Try different browser or incognito mode** (cookie issues)

### Login not working

**Verify password:**
```bash
grep WEB_PASSWORD ~/.myagentive/config
```

**Reset password:**
1. Edit config: `nano ~/.myagentive/config`
2. Change `WEB_PASSWORD=newpassword`
3. Restart MyAgentive

### WebSocket connection failed

**Symptom:** Chat loads but messages don't appear.

**Solutions:**
1. Check browser console for errors
2. Ensure no firewall blocking WebSocket
3. Try refreshing the page
4. Clear browser cache

---

## Database Issues

### Database corruption

**Symptom:** Errors about database or messages not loading.

**Solution - Reset database:**
```bash
# Stop MyAgentive first
rm ~/.myagentive/data/myagentive.db

# Restart MyAgentive - database recreates automatically
bun run dev
```

**Note:** This deletes all chat history.

### Database locked

**Symptom:** "database is locked" error.

**Cause:** Multiple processes accessing database.

**Solution:**
```bash
# Find and kill MyAgentive processes
pkill -f myagentive

# Start fresh
bun run dev
```

### Messages not persisting

**Check database path:**
```bash
grep DATABASE_PATH ~/.myagentive/config
# Should be something like ./data/myagentive.db
```

**Verify database exists:**
```bash
ls -la ~/.myagentive/data/
```

---

## Media Issues

### Media files not found

**Check media path:**
```bash
grep MEDIA_PATH ~/.myagentive/config
ls -la ~/.myagentive/media/
```

**Structure should be:**
```
~/.myagentive/media/
├── audio/
├── voice/
├── videos/
├── photos/
└── documents/
```

### Files too large

**Telegram limit:** 50MB maximum file size.

**Solution:** Compress or split large files before sending.

### Media not downloading

**Check permissions:**
```bash
ls -la ~/.myagentive/media/
# Should be writable by your user
```

**Fix permissions:**
```bash
chmod -R u+rwX ~/.myagentive/media/
```

---

## API Key Issues

### Key not working

**Verify key is in config:**
```bash
grep KEY_NAME ~/.myagentive/config
```

**Check format:**
- No quotes: `KEY=value` not `KEY="value"`
- No trailing spaces or newlines
- Key on its own line

### Key not loading

**Config must be proper format:**
```
KEY_NAME=value
ANOTHER_KEY=another_value
```

**Restart required:** After adding keys, restart MyAgentive.

### Regenerating keys

Most services allow regenerating API keys:
1. Go to the service's developer console
2. Revoke/delete old key
3. Create new key
4. Update `~/.myagentive/config`
5. Restart MyAgentive

---

## Logs and Debugging

### View logs

**Development mode:**
```bash
# Logs appear in terminal
bun run dev
```

**Binary mode:**
```bash
# Use the control command
myagentivectl logs

# Or run in foreground
myagentive  # Ctrl+C to stop
```

### Check if running

```bash
ps aux | grep myagentive
```

### Debug mode

Run with verbose output:
```bash
DEBUG=* bun run dev
```

---

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `EADDRINUSE` | Port already in use | Kill existing process or change PORT in config |
| `ECONNREFUSED` | Server not running | Start MyAgentive |
| `SQLITE_BUSY` | Database locked | Kill duplicate processes |
| `Invalid bot token` | Wrong Telegram token | Get new token from @BotFather |
| `User not authorised` | Wrong user ID | Get ID from @userinfobot |
| `API key not found` | Missing key in config | Add key to ~/.myagentive/config |

---

## Getting Help

1. **Check this guide** for common issues
2. **Review architecture** in `references/architecture.md`
3. **Check API key setup** in `references/api-keys.md`
4. **GitHub Issues:** https://github.com/AgentiveAU/MyAgentive/issues
5. **Website:** https://MyAgentive.ai
