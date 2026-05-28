# Account Directory Structure

## Overview

Each account has its own directory under `mem/accounts/{account_id}/`.

## Files

### state.md

Current account status in markdown format:

```markdown
# {Account Name} (Account {ID})

## Status
- **Stage**: Quote Pitched
- **Insurance Types**: General Liability, Workers Comp

## Contacts
- **Primary Email**: owner@company.com
- **Primary Phone**: (555) 123-4567

## Next Steps
- Follow up on quote decision
- Send additional carrier options

## Pending Actions
- Waiting for loss runs from client
- COI requested

## Last Contact
- **Date**: 2025-01-15
- **Type**: email
```

### history.md

Linked history entries (newest first):

```markdown
# Change History

## 2025-01-15T14:30:00Z

Stage updated after quote presentation call.

- **Stage**: Application Received → Quote Pitched
- **Evidence**: [call_150734](sources/calls/call_150734/raw.txt)

---
```

### sources/

Contains all communications organized by type:

- `emails/email_{id}/` - Email communications
- `calls/call_{id}/` - Phone call transcripts
- `sms/sms_{id}/` - Text messages

Each source folder contains:
- `raw.txt` - Original content
- `summary.md` - AI-generated summary
