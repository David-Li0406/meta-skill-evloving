---
name: wacli
description: Use this skill to send WhatsApp messages to others or to search/sync WhatsApp history via the wacli CLI, specifically for non-user chats.
---

# wacli

Use `wacli` only when the user explicitly asks you to message someone else on WhatsApp or when they request to sync/search WhatsApp history. Do NOT use `wacli` for normal user chats; it is designed for messaging other people.

## Safety
- Require explicit recipient and message text.
- Confirm recipient and message before sending.
- If anything is ambiguous, ask a clarifying question.

## Auth + Sync
- `wacli auth` (QR login + initial sync)
- `wacli sync --follow` (continuous sync)
- `wacli doctor`

## Find Chats + Messages
- `wacli chats list --limit 20 --query "name or number"`
- `wacli messages search "query" --limit 20 --chat <jid>`
- `wacli messages search "invoice" --after <start_date> --before <end_date>`

## History Backfill
- `wacli history backfill --chat <jid> --requests 2 --count 50`

## Send Messages
- Text: `wacli send text --to "<recipient_number>" --message "<your_message>"`
- Group: `wacli send text --to "<group_id>" --message "<your_message>"`
- File: `wacli send file --to "<recipient_number>" --file <file_path> --caption "<caption>"`

## Notes
- Store directory: `~/.wacli` (override with `--store`).
- Use `--json` for machine-readable output when parsing.
- Backfill requires your phone to be online; results are best-effort.
- WhatsApp CLI is not needed for routine user chats; it’s for messaging other people.
- JIDs: direct chats look like `<number>@s.whatsapp.net`; groups look like `<id>@g.us` (use `wacli chats list` to find).