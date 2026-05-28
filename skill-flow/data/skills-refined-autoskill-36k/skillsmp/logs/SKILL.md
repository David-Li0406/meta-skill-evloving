---
name: logs
description: View call logs for the Vocal Bridge voice agent. Can list recent calls or show details of a specific session including transcript.
allowed-tools: Bash
---

View call logs for the voice agent.

First ensure CLI is installed:

```bash
pip install --upgrade vocal-bridge
```

## List Recent Logs

If $ARGUMENTS is empty or contains options, list recent logs:

```bash
vb logs $ARGUMENTS
```

Common options:
- `-n 50` - Show 50 logs (default 20)
- `--status completed` - Filter by status (completed/failed/abandoned/in_progress)
- `--json` - Output as JSON

## View Session Details

If $ARGUMENTS contains a UUID (session ID), show details:

```bash
vb logs <session_id>
```

This shows:
- Session ID and status
- Start/end time and duration
- Message count
- Caller phone and direction
- Full transcript
- Error message (if failed)
- Recording availability (if available, use `/vocal-bridge:download <session_id>` to download)

Use `--json` flag for machine-readable output.
