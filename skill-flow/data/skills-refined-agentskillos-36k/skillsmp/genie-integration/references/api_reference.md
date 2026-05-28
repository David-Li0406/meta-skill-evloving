# Databricks Genie SDK Reference

Quick reference for Databricks Genie API methods used in agent integration.

## WorkspaceClient.genie Methods

### start_conversation
Start a new conversation with a Genie space.

**Signature:**
```python
w.genie.start_conversation(
    space_id: str,
    content: str
) -> GenieStartConversationResponse
```

**Returns:**
- `conversation_id`: str - ID for this conversation
- `message_id`: str - ID for the initial message

**Example:**
```python
response = w.genie.start_conversation(
    space_id="01f09cdbacf01b5fa7ff7c237365502c",
    content="What products are trending?"
)
```

### create_message
Add a message to an existing conversation.

**Signature:**
```python
w.genie.create_message(
    space_id: str,
    conversation_id: str,
    content: str
) -> GenieCreateMessageResponse
```

**Returns:**
- `message_id`: str - ID for the new message

**Example:**
```python
response = w.genie.create_message(
    space_id="01f09cdbacf01b5fa7ff7c237365502c",
    conversation_id=conv_id,
    content="What about last month?"
)
```

### get_message
Retrieve message status and content.

**Signature:**
```python
w.genie.get_message(
    space_id: str,
    conversation_id: str,
    message_id: str
) -> GenieMessage
```

**Returns GenieMessage with:**
- `status`: str - "PENDING", "COMPLETED", "FAILED", "CANCELLED"
- `content`: str - Message text
- `attachments`: list - Query results, text, etc.

**Message Status Values:**
- `PENDING`: Still processing
- `COMPLETED`: Ready, attachments available
- `FAILED`: Query failed
- `CANCELLED`: User cancelled

**Example:**
```python
message = w.genie.get_message(
    space_id="01f09cdbacf01b5fa7ff7c237365502c",
    conversation_id=conv_id,
    message_id=msg_id
)

if message.status == "COMPLETED":
    # Extract results
    for attachment in message.attachments:
        if hasattr(attachment, 'text'):
            print(attachment.text.content)
```

## Message Attachments

### Text Attachment
Natural language summary from Genie.

```python
if hasattr(attachment, 'text') and attachment.text:
    summary = attachment.text.content
```

### Query Attachment
SQL query and results.

```python
if hasattr(attachment, 'query') and attachment.query:
    sql = attachment.query.query
    description = attachment.query.description
    # Note: Full results may not be in response
```

## Polling Pattern

Standard pattern for waiting on Genie responses:

```python
import time

def poll_for_completion(w, space_id, conversation_id, message_id, max_attempts=30):
    """Poll until message is complete or failed"""
    for attempt in range(max_attempts):
        message = w.genie.get_message(space_id, conversation_id, message_id)
        
        if message.status == "COMPLETED":
            return message
        elif message.status in ["FAILED", "CANCELLED"]:
            raise Exception(f"Message {message.status}")
        
        time.sleep(2)  # Wait 2 seconds between checks
    
    raise TimeoutError("Message did not complete in time")
```

## Error Handling

Common exceptions:

```python
from databricks.sdk.errors import DatabricksError

try:
    response = w.genie.start_conversation(space_id, content)
except DatabricksError as e:
    if "not found" in str(e).lower():
        # Space doesn't exist or no permission
        pass
    elif "permission" in str(e).lower():
        # Permission denied
        pass
```

## Rate Limits

- Genie API has rate limits per workspace
- Implement exponential backoff for polling
- Consider caching responses for repeated queries

## Best Practices

1. **Always poll with timeout** - Don't assume instant responses
2. **Handle all status values** - PENDING, COMPLETED, FAILED, CANCELLED
3. **Extract text summaries** - Prioritize natural language over raw SQL
4. **Cache responses** - Avoid repeated identical queries
5. **Manage conversations** - Reuse conversation_id for context
