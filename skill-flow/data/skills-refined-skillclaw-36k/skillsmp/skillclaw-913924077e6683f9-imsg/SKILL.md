---
name: imsg
description: Use this skill when you want to read and send iMessage/SMS messages from the command line on macOS.
---

# Skill body

## Requirements
- Messages.app signed in
- Full Disk Access for your terminal
- Automation permission to control Messages.app (for sending)

## Common commands
- **List chats**: 
  ```bash
  imsg chats --limit 10 --json
  ```
- **View chat history**: 
  ```bash
  imsg history --chat-id 1 --limit 20 --attachments --json
  ```
- **Watch a chat**: 
  ```bash
  imsg watch --chat-id 1 --attachments
  ```
- **Send a message**: 
  ```bash
  imsg send --to "+14155551212" --text "hi" --file /path/pic.jpg
  ```

## Notes
- Use `--service imessage|sms|auto` to control delivery.
- Always confirm the recipient and message before sending.