---
name: imsg
description: Use this skill when you need to read and send iMessage/SMS messages on macOS via the command line.
---

# imsg

Use `imsg` to read and send Messages.app iMessage/SMS on macOS.

## Requirements
- Messages.app signed in
- Full Disk Access for your terminal
- Automation permission to control Messages.app (for sending)

## Common commands
- List chats: `imsg chats --limit 10 --json`
- History: `imsg history --chat-id <chat_id> --limit 20 --attachments --json`
- Watch: `imsg watch --chat-id <chat_id> --attachments`
- Send: `imsg send --to "<recipient_number>" --text "<message>" --file <file_path>`

## Notes
- Use `--service imessage|sms|auto` to control delivery.
- Confirm recipient and message before sending.