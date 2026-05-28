# Telegram Setup Guide for MyAgentive

## Prerequisites

- Telegram account
- Telegram app (mobile or desktop)

---

## Step 1: Create a Telegram Bot

### Using @BotFather

1. Open Telegram and search for `@BotFather`
2. Start a chat and send `/newbot`
3. Follow the prompts:
   - **Name:** Choose a display name (e.g., "My Personal Agent")
   - **Username:** Choose a unique username ending in `bot` (e.g., `my_agent_xyz_bot`)
4. BotFather will send you the bot token

### Bot Token Format

The token looks like:
```
7123456789:AAHxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

- Starts with numbers
- Contains a colon `:`
- Followed by alphanumeric characters

**Important:** Keep this token secret. Anyone with the token can control your bot.

### Configure Bot Settings (Optional)

While chatting with @BotFather:
- `/setdescription` - Set bot description
- `/setabouttext` - Set "About" text
- `/setuserpic` - Set bot profile picture
- `/setcommands` - Set command menu (MyAgentive does this automatically)

---

## Step 2: Get Your Telegram User ID

MyAgentive only responds to your user ID for security.

### Using @userinfobot

1. Open Telegram and search for `@userinfobot`
2. Start a chat and send any message
3. The bot replies with your user info including your **Id**

Example response:
```
Id: 123456789
First: John
Last: Doe
```

Your user ID is the numeric **Id** value (e.g., `123456789`).

### Alternative: @getidsbot

1. Search for `@getidsbot`
2. Send `/start`
3. It shows your user ID

**Important:** Use the numeric ID, not your @username.

---

## Step 3: Configure MyAgentive

### During Setup Wizard

When running MyAgentive for the first time:

1. **Bot Token prompt:**
   ```
   Telegram Bot Token:
   ```
   Paste your bot token from @BotFather

2. **User ID prompt:**
   ```
   Telegram User ID:
   ```
   Enter your numeric user ID from @userinfobot

### Manual Configuration

Edit `~/.myagentive/config`:
```
TELEGRAM_BOT_TOKEN=7123456789:AAHxxxxxxxxxxxxxxxxxxxxxxxxxxx
TELEGRAM_USER_ID=123456789
```

---

## Step 4: Start Using the Bot

1. Open Telegram and find your bot (search by username)
2. Start a chat: tap "Start" or send `/start`
3. Send a message to test

The bot should respond through MyAgentive.

---

## Activity Monitoring (Optional)

Send activity notifications to a Telegram group for logging.

### Setup Steps

1. **Create a Telegram group:**
   - Open Telegram > New Group
   - Name it (e.g., "MyAgentive Activity")
   - Add your bot as a member

2. **Get the group ID:**
   - Add `@getidsbot` to the group temporarily
   - The bot will show the group ID (negative number, starts with `-100`)
   - Remove @getidsbot from the group

3. **Configure MyAgentive:**
   ```bash
   echo "TELEGRAM_MONITORING_GROUP_ID=-100xxxxxxxxxx" >> ~/.myagentive/config
   ```

4. **Restart MyAgentive**

### What Gets Logged

- Session created/switched
- Messages sent and received (summaries)
- Errors and warnings
- System events

---

## Telegram Commands Reference

Once the bot is running:

| Command | Description |
|---------|-------------|
| `/start` | Start the bot / show welcome |
| `/help` | Show available commands |
| `/session <name>` | Switch to a named session |
| `/new [name]` | Create a new session |
| `/list` | List all sessions |
| `/status` | Show current session info |
| `/model <opus\|sonnet\|haiku>` | Change AI model |
| `/usage` | Show usage statistics |

### Examples

```
/session work
# Switches to "work" session (creates if doesn't exist)

/new project-x
# Creates new session named "project-x" and switches to it

/model haiku
# Changes to faster, cheaper Haiku model

/list
# Shows all your sessions
```

---

## Security Considerations

### User ID Restriction

MyAgentive only responds to the configured `TELEGRAM_USER_ID`. This means:
- Only you can interact with your bot
- Others who find your bot will be ignored
- You can share the bot link safely (others cannot use it)

### Bot Token Security

- Never share your bot token publicly
- Store only in `~/.myagentive/config`
- If compromised, regenerate via @BotFather: `/revoke` then `/newbot`

### Group Access (Optional)

To allow the bot in groups:
```
TELEGRAM_ALLOWED_GROUPS=-100xxx,-100yyy
```

By default, the bot only works in direct messages.

---

## Troubleshooting

### Bot not responding

1. **Verify token format:**
   ```bash
   grep TELEGRAM_BOT_TOKEN ~/.myagentive/config
   # Must contain a colon (:)
   ```

2. **Verify user ID:**
   ```bash
   grep TELEGRAM_USER_ID ~/.myagentive/config
   # Must be numeric (no @)
   ```

3. **Check MyAgentive is running:**
   ```bash
   ps aux | grep myagentive
   ```

4. **Send /start to the bot** in Telegram

### "User not authorised"

Your user ID doesn't match config. Get correct ID from @userinfobot and update config.

### Messages delayed

- Check internet connectivity
- MyAgentive may be processing a long task
- Default timeout is 60 minutes

### Cannot find the bot

Search by the exact username you set (e.g., `@my_agent_xyz_bot`).

---

## Updating Bot Token

If you need a new bot token:

1. Chat with @BotFather
2. Send `/mybots`
3. Select your bot
4. Choose "API Token" > "Revoke current token"
5. Copy the new token
6. Update `~/.myagentive/config`
7. Restart MyAgentive

---

## Multiple Bots

You can run multiple MyAgentive instances with different bots:

1. Create additional bots via @BotFather
2. Use different config directories:
   ```bash
   MYAGENTIVE_HOME=~/.myagentive-work myagentive
   MYAGENTIVE_HOME=~/.myagentive-personal myagentive
   ```

Each instance has its own config, database, and bot.
