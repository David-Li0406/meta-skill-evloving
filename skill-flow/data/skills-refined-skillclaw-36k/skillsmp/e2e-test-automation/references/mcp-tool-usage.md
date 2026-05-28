# MCP Tool Usage Reference

## Quick Reference

| MCP Server | Tools | Use Case |
|------------|-------|----------|
| telegram-mcp | send_message, get_messages, list_chats | Bot testing |
| gmail | search_emails, read_email | OTP verification |
| supabase | execute_sql, list_tables | Database state |
| chrome-devtools | navigate, screenshot, click | Portal testing |

---

## Telegram MCP Tools

### mcp__telegram-mcp__get_me

Get current authenticated user.

```
mcp__telegram-mcp__get_me
```

**Response:**
```json
{
  "id": 123456789,
  "first_name": "User",
  "username": "username"
}
```

### mcp__telegram-mcp__list_chats

List all chats for current user.

```
mcp__telegram-mcp__list_chats
```

**Response:** Array of chat objects with id, name, type.

### mcp__telegram-mcp__send_message

Send a message to a chat.

```
mcp__telegram-mcp__send_message
  chat_id="<chat_id>"
  text="Hello, world!"
```

**Parameters:**
- `chat_id` (required): Target chat ID
- `text` (required): Message text

### mcp__telegram-mcp__get_messages

Get recent messages from a chat.

```
mcp__telegram-mcp__get_messages
  chat_id="<chat_id>"
  limit=10
```

**Parameters:**
- `chat_id` (required): Target chat ID
- `limit` (optional): Number of messages (default 10)

### mcp__telegram-mcp__get_history

Get message history with more options.

```
mcp__telegram-mcp__get_history
  chat_id="<chat_id>"
  limit=50
```

---

## Gmail MCP Tools

### mcp__gmail__search_emails

Search for emails matching query.

```
mcp__gmail__search_emails
  query="from:noreply subject:Nikita code"
  max_results=5
```

**Parameters:**
- `query` (required): Gmail search query
- `max_results` (optional): Limit results

**Common Queries:**
- OTP emails: `from:noreply subject:Nikita code`
- Recent: `after:2025/12/21`
- Unread: `is:unread`

### mcp__gmail__read_email

Read a specific email by ID.

```
mcp__gmail__read_email
  id="<email_id>"
```

**Response:** Full email content including body.

### mcp__gmail__list_email_labels

List available email labels.

```
mcp__gmail__list_email_labels
```

---

## Supabase MCP Tools

### mcp__supabase__execute_sql

Execute SQL query against database.

```
mcp__supabase__execute_sql
  query="SELECT * FROM users LIMIT 5"
```

**Parameters:**
- `query` (required): SQL query string

**Important:**
- Use parameterized values for security
- Limit results to prevent large payloads
- Prefer SELECT for verification (avoid mutations)

### mcp__supabase__list_tables

List all tables in database.

```
mcp__supabase__list_tables
```

**Use for:** Discovering schema, verifying table existence.

### mcp__supabase__list_migrations

List applied migrations.

```
mcp__supabase__list_migrations
```

### mcp__supabase__get_logs

Get Supabase logs.

```
mcp__supabase__get_logs
```

---

## Chrome DevTools MCP Tools

### mcp__chrome-devtools__new_page

Create new browser page.

```
mcp__chrome-devtools__new_page
```

### mcp__chrome-devtools__navigate_page

Navigate to URL.

```
mcp__chrome-devtools__navigate_page
  url="https://example.com"
```

### mcp__chrome-devtools__take_screenshot

Capture current page.

```
mcp__chrome-devtools__take_screenshot
```

**Returns:** Base64 encoded image.

### mcp__chrome-devtools__click

Click an element.

```
mcp__chrome-devtools__click
  selector="button[type='submit']"
```

### mcp__chrome-devtools__fill

Fill a form field.

```
mcp__chrome-devtools__fill
  selector="input[name='email']"
  value="test@example.com"
```

### mcp__chrome-devtools__evaluate_script

Run JavaScript on page.

```
mcp__chrome-devtools__evaluate_script
  script="document.querySelector('h1')?.textContent"
```

### mcp__chrome-devtools__list_console_messages

Get browser console messages.

```
mcp__chrome-devtools__list_console_messages
```

### mcp__chrome-devtools__list_network_requests

Get network requests made by page.

```
mcp__chrome-devtools__list_network_requests
```

### mcp__chrome-devtools__resize_page

Change viewport size.

```
mcp__chrome-devtools__resize_page
  width=375
  height=812
```

### mcp__chrome-devtools__close_page

Close browser page.

```
mcp__chrome-devtools__close_page
```

---

## Tool Discovery

Use MCPSearch to find and load tools:

```
# Search by keyword
MCPSearch query="telegram message"

# Direct selection
MCPSearch query="select:mcp__telegram-mcp__send_message"
```

**Important:** MCP tools must be loaded via MCPSearch before first use.

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Tool not found | Not loaded | Use MCPSearch first |
| Authentication failed | Session expired | Re-authenticate MCP server |
| Rate limited | Too many requests | Wait and retry |
| Timeout | Slow response | Increase timeout, retry |

### Retry Pattern

```
1. First attempt
2. If failed: Wait 5s, retry
3. If failed again: Wait 15s, retry
4. If failed: Report as failure
```

---

## Best Practices

1. **Always load tools first** via MCPSearch
2. **Limit query results** to prevent context overflow
3. **Use specific selectors** for Chrome interactions
4. **Wait between operations** (especially Telegram)
5. **Handle errors gracefully** - log and continue
6. **Verify before mutating** - check state first
