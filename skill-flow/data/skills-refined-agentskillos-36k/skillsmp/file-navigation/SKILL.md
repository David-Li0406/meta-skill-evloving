---
name: file-navigation
description: Navigate account directories and read files. Use after finding an account to explore state.md, history.md, and source communications.
---

# File Navigation

## When to use this skill

- After finding an account, need to read its details
- User asks about specific communications (emails, calls, SMS)
- Need to understand account history or current state

## Tools available

### list_directory

List contents of an account folder:

```json
{
  "tool": "list_directory",
  "args": {"path": "mem/accounts/29041"}
}
```

### read_file

Read a specific file:

```json
{
  "tool": "read_file",
  "args": {"path": "mem/accounts/29041/state.md"}
}
```

## Account directory structure

See `references/directory-structure.md` for full details.

```
mem/accounts/{account_id}/
├── state.md          # Current status, contacts, next steps
├── history.md        # Change history with linked entries
└── sources/
    ├── emails/
    │   └── email_{id}/
    │       ├── raw.txt      # Original email
    │       └── summary.md   # AI summary
    ├── calls/
    │   └── call_{id}/
    │       ├── raw.txt      # Transcript
    │       └── summary.md   # AI summary
    └── sms/
        └── sms_{id}/
            ├── raw.txt
            └── summary.md
```

## Reading strategy

1. Start with `state.md` for current status
2. Check `history.md` for recent changes
3. Navigate to `sources/` for specific communications
4. Read `summary.md` first, then `raw.txt` if more detail needed
