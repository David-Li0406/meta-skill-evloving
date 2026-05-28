---
name: Discord Integration
description: Send messages and manage the Discord channel for this session
---

# Discord Integration Skills

Communicate directly with users in the Discord channel tied to this session.

## Commands

### `update-channel.sh` — Rename Channel

```bash
update-channel.sh "channel-name" "Description of current task"
```

- **channel-name**: kebab-case, max 5 words (e.g., `fix-auth-bug`)
- **description**: Brief summary of what you're working on

---

### `send-to-discord.sh` — Send Message

#### Plain Message
```bash
send-to-discord.sh "Your message here"
```

#### Rich Embed (for status updates)
```bash
send-to-discord.sh --title "Title" --description "Details" --color "green"
```

**Required:** Either plain message content, OR both `--title` AND `--description` for embeds.

**Valid colors:** `green`, `red`, `yellow`, `blue`, `orange`, `purple`

#### Sending Files
```bash
send-to-discord.sh --file "path/to/image.png" "Here is the image."
```

---

## Quick Reference

| Situation         | Command |
|-------------------|---------|
| Start/switch task | `update-channel.sh "task-name" "description"` |
| Task done         | `send-to-discord.sh --title "✅ Done" --description "..." --color "green"` |
| Need user input   | `send-to-discord.sh "Hey @username, I need..."` |
| Error occurred    | `send-to-discord.sh --title "⚠️ Error" --description "..." --color "red"` |
