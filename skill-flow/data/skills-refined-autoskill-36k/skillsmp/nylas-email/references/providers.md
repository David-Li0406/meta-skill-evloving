# Provider-Specific Notes

## Google
- Uses "labels" (mapped to folders API)
- Supports `text_color` and `background_color` for labels
- One-click unsubscribe required for bulk senders (5000+/day)
- Scopes: `gmail.readonly`, `gmail.send`, `contacts.readonly`

## Microsoft
- Supports nested folders with `parent_id`
- Some Exchange servers ignore From headers
- May need quarantine check for EAS devices
- Scopes: `Mail.Read`, `Mail.ReadWrite`, `Mail.Send`, `Contacts.Read`

## IMAP
- 90-day rolling window for message storage
- Folder names may differ from provider UI
- Hierarchy reflected in folder name (e.g., `INBOX\Accounting\Taxes`)
- Folders may take up to 10 minutes to appear after auth

## iCloud/Yahoo
- Email data up to 90 days old
- Yahoo/AOL webhooks may have 5-minute delay
- Don't support unsubscribe headers
