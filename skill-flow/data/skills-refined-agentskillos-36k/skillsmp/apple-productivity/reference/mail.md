# Mail Reference

## Command: mail-unread

Get unread mail. **REQUIRES Mail.app RUNNING**.

```bash
mail-unread              # Last 24 hours (default)
mail-unread 6            # Last 6 hours
mail-unread -d 3         # Last 3 days
mail-unread -l 5         # Limit to 5 messages
mail-unread -j           # JSON output
```

## Error Handling

**Exit code 1** = Mail.app not running.

Response: Tell user to open Mail.app, then retry.

```
Error: Mail.app not running
Please open Mail.app before running this command
```

## Examples

**"Any unread emails?"**
```bash
mail-unread
```

**"Any unread emails from Marie?"**
```bash
mail-unread -l 20
```
Then filter output for "Marie" in sender field.

**"Check emails from the last week"**
```bash
mail-unread -d 7
```
