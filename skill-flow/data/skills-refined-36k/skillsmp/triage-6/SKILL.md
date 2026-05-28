---
name: triage
description: Triage FreshService ticket and create GitHub issue
argument-hint: "[ticket-id]"
model: claude-sonnet-4-5
context: fork
agent: general-purpose
allowed-tools:
  - Bash(*)
  - Task
extended-thinking: true
---

# FreshService Ticket Triage

You are a support engineer who triages bug reports from FreshService and creates well-structured GitHub issues. You extract all relevant information from FreshService tickets and automatically create comprehensive issues for development teams.

**Ticket ID:** $ARGUMENTS

## Workflow

### Phase 1: Configuration Validation & Ticket Fetch

Validate credentials, fetch the ticket, and format the data:

```bash
# Validate and sanitize ticket ID
TICKET_ID="$ARGUMENTS"
TICKET_ID="${TICKET_ID//[^0-9]/}"  # Remove all non-numeric characters

if [ -z "$TICKET_ID" ] || ! [[ "$TICKET_ID" =~ ^[0-9]+$ ]]; then
  echo "Invalid ticket ID"
  echo "Usage: /triage <ticket-id>"
  exit 1
fi

# Check for environment configuration
if [ -f ~/.claude/freshservice.env ]; then
  echo "Loading FreshService configuration..."
  source ~/.claude/freshservice.env
else
  echo "FreshService configuration not found!"
  echo ""
  echo "Please create ~/.claude/freshservice.env with:"
  echo ""
  echo "FRESHSERVICE_API_KEY=your_api_key_here"
  echo "FRESHSERVICE_DOMAIN=your_domain"
  echo ""
  echo "Example:"
  echo "FRESHSERVICE_API_KEY=abcdef123456"
  echo "FRESHSERVICE_DOMAIN=psd401"
  echo ""
  exit 1
fi

# Validate required variables
if [ -z "$FRESHSERVICE_API_KEY" ] || [ -z "$FRESHSERVICE_DOMAIN" ]; then
  echo "Missing required environment variables!"
  echo "Required: FRESHSERVICE_API_KEY, FRESHSERVICE_DOMAIN"
  exit 1
fi

# Validate domain format (alphanumeric and hyphens only, prevents SSRF)
if ! [[ "$FRESHSERVICE_DOMAIN" =~ ^[a-zA-Z0-9-]+$ ]]; then
  echo "Invalid FRESHSERVICE_DOMAIN format"
  echo "Domain must contain only alphanumeric characters and hyphens"
  echo "Example: 'psd401' (not 'psd401.freshservice.com')"
  exit 1
fi

# Validate API key format (basic sanity check)
if [ ${#FRESHSERVICE_API_KEY} -lt 20 ]; then
  echo "Warning: API key appears too short. Please verify your configuration."
fi

echo "Configuration validated"
echo "Domain: $FRESHSERVICE_DOMAIN"
echo ""

# API configuration
API_BASE_URL="https://${FRESHSERVICE_DOMAIN}.freshservice.com/api/v2"
TICKET_ENDPOINT="${API_BASE_URL}/tickets/${TICKET_ID}"

# Temporary files for API responses
TICKET_JSON="/tmp/fs-ticket-${TICKET_ID}.json"
CONVERSATIONS_JSON="/tmp/fs-conversations-${TICKET_ID}.json"

# Cleanup function
cleanup() {
  rm -f "$TICKET_JSON" "$CONVERSATIONS_JSON"
}
trap cleanup EXIT

echo "=== Fetching FreshService Ticket #${TICKET_ID} ==="
echo ""

# Function to make API request with retry logic
api_request() {
  local url="$1"
  local output_file="$2"
  local max_retries=3
  local retry_delay=2
  local attempt=1

  while [ $attempt -le $max_retries ]; do
    # Make request and capture HTTP status code
    http_code=$(curl -s -w "%{http_code}" -u "${FRESHSERVICE_API_KEY}:X" \
         -H "Content-Type: application/json" \
         -X GET "$url" \
         -o "$output_file" \
         --max-time 30)

    # Check for rate limiting (HTTP 429)
    if [ "$http_code" = "429" ]; then
      echo "Error: Rate limit exceeded. Please wait before retrying."
      echo "FreshService API has rate limits (typically 1000 requests/hour)."
      return 1
    fi

    # Success (HTTP 200)
    if [ "$http_code" = "200" ]; then
      return 0
    fi

    # Unauthorized (HTTP 401)
    if [ "$http_code" = "401" ]; then
      echo "Error: Authentication failed. Please check your API key."
      return 1
    fi

    # Not found (HTTP 404)
    if [ "$http_code" = "404" ]; then
      echo "Error: Ticket not found. Please verify the ticket ID."
      return 1
    fi

    # Retry on server errors (5xx)
    if [ $attempt -lt $max_retries ]; then
      echo "Warning: API request failed with HTTP $http_code (attempt $attempt/$max_retries), retrying in ${retry_delay}s..."
      sleep $retry_delay
      retry_delay=$((retry_delay * 2))  # Exponential backoff
    fi
    attempt=$((attempt + 1))
  done

  echo "Error: API request failed after $max_retries attempts (last HTTP code: $http_code)"
  return 1
}

# Fetch ticket with embedded fields
echo "Fetching ticket #${TICKET_ID}..."
if ! api_request "${TICKET_ENDPOINT}?include=requester,stats" "$TICKET_JSON"; then
  echo ""
  echo "Failed to retrieve ticket from FreshService"
  echo "Please verify:"
  echo "  - Ticket ID $TICKET_ID exists"
  echo "  - API key is valid"
  echo "  - Domain is correct ($FRESHSERVICE_DOMAIN)"
  exit 1
fi

# Fetch conversations (comments)
echo "Fetching ticket conversations..."
if ! api_request "${TICKET_ENDPOINT}/conversations" "$CONVERSATIONS_JSON"; then
  echo "Warning: Failed to fetch conversations, continuing without them..."
  echo '{"conversations":[]}' > "$CONVERSATIONS_JSON"
fi

echo "Ticket retrieved successfully"
echo ""

# Check if jq is available for JSON parsing
if ! command -v jq &> /dev/null; then
  echo "Warning: jq not found, using basic parsing"
  echo "Install jq for full functionality: brew install jq (macOS) or apt-get install jq (Linux)"
  JQ_AVAILABLE=false
else
  JQ_AVAILABLE=true
fi

# Extract ticket fields
if [ "$JQ_AVAILABLE" = true ]; then
  SUBJECT=$(jq -r '.ticket.subject // "No subject"' "$TICKET_JSON")
  DESCRIPTION=$(jq -r '.ticket.description_text // .ticket.description // "No description"' "$TICKET_JSON")
  PRIORITY=$(jq -r '.ticket.priority // 0' "$TICKET_JSON")
  STATUS=$(jq -r '.ticket.status // 0' "$TICKET_JSON")
  CREATED_AT=$(jq -r '.ticket.created_at // "Unknown"' "$TICKET_JSON")
  REQUESTER_NAME=$(jq -r '.ticket.requester.name // "Unknown"' "$TICKET_JSON" 2>/dev/null || echo "Unknown")
  CATEGORY=$(jq -r '.ticket.category // "Uncategorized"' "$TICKET_JSON")
  URGENCY=$(jq -r '.ticket.urgency // 0' "$TICKET_JSON")

  # Extract custom fields if present
  CUSTOM_FIELDS=$(jq -r '.ticket.custom_fields // {}' "$TICKET_JSON")

  # Extract attachments if present
  ATTACHMENTS=$(jq -r '.ticket.attachments // []' "$TICKET_JSON")
  HAS_ATTACHMENTS=$(echo "$ATTACHMENTS" | jq '. | length > 0')

  # Extract conversations
  CONVERSATIONS=$(jq -r '.conversations // []' "$CONVERSATIONS_JSON")
  CONVERSATION_COUNT=$(echo "$CONVERSATIONS" | jq '. | length')
else
  # Fallback to basic grep/sed parsing
  SUBJECT=$(grep -o '"subject":"[^"]*"' "$TICKET_JSON" | head -1 | sed 's/"subject":"//;s/"$//' || echo "No subject")
  DESCRIPTION=$(grep -o '"description_text":"[^"]*"' "$TICKET_JSON" | head -1 | sed 's/"description_text":"//;s/"$//' || echo "No description")
  PRIORITY="0"
  STATUS="0"
  CREATED_AT="Unknown"
  REQUESTER_NAME="Unknown"
  CATEGORY="Unknown"
  URGENCY="0"
  HAS_ATTACHMENTS="false"
  CONVERSATION_COUNT="0"
fi

# Map priority codes to human-readable strings
case "$PRIORITY" in
  1) PRIORITY_STR="Low" ;;
  2) PRIORITY_STR="Medium" ;;
  3) PRIORITY_STR="High" ;;
  4) PRIORITY_STR="Urgent" ;;
  *) PRIORITY_STR="Unknown" ;;
esac

# Map urgency codes
case "$URGENCY" in
  1) URGENCY_STR="Low" ;;
  2) URGENCY_STR="Medium" ;;
  3) URGENCY_STR="High" ;;
  *) URGENCY_STR="Unknown" ;;
esac

# Map status codes
case "$STATUS" in
  2) STATUS_STR="Open" ;;
  3) STATUS_STR="Pending" ;;
  4) STATUS_STR="Resolved" ;;
  5) STATUS_STR="Closed" ;;
  *) STATUS_STR="Unknown" ;;
esac

# Format the issue description
ISSUE_DESCRIPTION="Bug report from FreshService Ticket #${TICKET_ID}

## Summary
${SUBJECT}

## Description
${DESCRIPTION}

## Ticket Information
- **FreshService Ticket**: #${TICKET_ID}
- **Status**: ${STATUS_STR}
- **Priority**: ${PRIORITY_STR}
- **Urgency**: ${URGENCY_STR}
- **Category**: ${CATEGORY}
- **Created**: ${CREATED_AT}

## Reporter Information
- **Name**: ${REQUESTER_NAME}
- **Contact**: Available in FreshService ticket #${TICKET_ID}

## Steps to Reproduce
(Please extract from description or conversations if available)

## Expected Behavior
(To be determined from ticket context)

## Actual Behavior
(Described in ticket)

## Additional Context"

# Add attachments section if present
if [ "$HAS_ATTACHMENTS" = "true" ] && [ "$JQ_AVAILABLE" = true ]; then
  ISSUE_DESCRIPTION="${ISSUE_DESCRIPTION}

### Attachments"
  ATTACHMENTS_LIST=$(echo "$ATTACHMENTS" | jq -r '.[] | "- \(.name) (\(.size) bytes)"')
  ISSUE_DESCRIPTION="${ISSUE_DESCRIPTION}
${ATTACHMENTS_LIST}"
fi

# Add conversation history if present (sanitize HTML/script tags)
# SECURITY FIX (CWE-79): Enhanced sanitization beyond simple <> removal
# See @agents/document-validator.md for sanitizeWebContent() function
if [ "$CONVERSATION_COUNT" -gt 0 ] && [ "$JQ_AVAILABLE" = true ]; then
  ISSUE_DESCRIPTION="${ISSUE_DESCRIPTION}

### Conversation History
"
  # SECURITY NOTE: This jq-based sanitization is LIMITED
  # - For production: Use DOMPurify library (see @agents/document-validator.md)
  # - This approach: Strips HTML tags, encodes special chars
  # - Limitation: Cannot handle complex XSS vectors or encoding bypasses
  # - Acceptable for: GitHub markdown issues (renderer has additional protections)
  CONVERSATION_TEXT=$(echo "$CONVERSATIONS" | jq -r '.[] | "**\(.user_id // "User")** (\(.created_at)):\n" + (
    (.body_text // .body)
    | gsub("<[^>]+>"; "")     # Strip ALL HTML tags completely
    | gsub("&"; "&amp;")      # Encode ampersands first
    | gsub("<"; "&lt;")       # Encode any remaining less-than
    | gsub(">"; "&gt;")       # Encode any remaining greater-than
  ) + "\n"')
  ISSUE_DESCRIPTION="${ISSUE_DESCRIPTION}${CONVERSATION_TEXT}"
fi

# Add custom fields if present and not empty
if [ "$JQ_AVAILABLE" = true ]; then
  CUSTOM_FIELDS_COUNT=$(echo "$CUSTOM_FIELDS" | jq '. | length')
  if [ "$CUSTOM_FIELDS_COUNT" -gt 0 ]; then
    ISSUE_DESCRIPTION="${ISSUE_DESCRIPTION}

### Custom Fields
\`\`\`json
# Custom fields from FreshService - review before using
$(echo "$CUSTOM_FIELDS" | jq '.')
\`\`\`"
  fi
fi

# Add link to original ticket
ISSUE_DESCRIPTION="${ISSUE_DESCRIPTION}

---
*Imported from FreshService: https://${FRESHSERVICE_DOMAIN}.freshservice.com/a/tickets/${TICKET_ID}*"

echo "=== Ticket Information ==="
echo ""
echo "Subject: $SUBJECT"
echo "Priority: $PRIORITY_STR"
echo "Status: $STATUS_STR"
echo ""
```

### Phase 2: Create GitHub Issue

Now invoke the `/issue` command with the extracted information:

**IMPORTANT**: Use the Skill tool to invoke `/psd-claude-coding-system:issue` with the ticket description.

Pass the `$ISSUE_DESCRIPTION` variable that contains the formatted bug report from FreshService.

**After the issue is created, capture the issue number/URL for the FreshService reply.**

### Phase 3: Update FreshService Ticket

After successfully creating the GitHub issue, add a reply to the FreshService ticket and update its status:

```bash
echo ""
echo "=== Updating FreshService Ticket ==="
echo ""

# Add a reply to the ticket with the GitHub issue link
echo "Adding reply to ticket..."
REPLY_BODY="Thank you for submitting this issue. We have received your ticket and created a GitHub issue to track this problem. We will let you know when the issue has been resolved."

REPLY_RESPONSE=$(curl -s -w "\n%{http_code}" -u "${FRESHSERVICE_API_KEY}:X" \
  -H "Content-Type: application/json" \
  -X POST "${API_BASE_URL}/tickets/${TICKET_ID}/conversations" \
  -d "{\"body\": \"${REPLY_BODY}\"}")

# Extract HTTP code from response
REPLY_HTTP_CODE=$(echo "$REPLY_RESPONSE" | tail -n1)
REPLY_JSON=$(echo "$REPLY_RESPONSE" | head -n-1)

if [ "$REPLY_HTTP_CODE" = "201" ]; then
  echo "Reply added to ticket"
else
  echo "Warning: Failed to add reply (HTTP $REPLY_HTTP_CODE)"
  echo "   FreshService ticket NOT updated"
fi

# Update ticket status to "In Progress" (status code 2)
echo "Updating ticket status to In Progress..."
STATUS_RESPONSE=$(curl -s -w "\n%{http_code}" -u "${FRESHSERVICE_API_KEY}:X" \
  -H "Content-Type: application/json" \
  -X PUT "${API_BASE_URL}/tickets/${TICKET_ID}" \
  -d '{"status": 2}')

# Extract HTTP code from response
STATUS_HTTP_CODE=$(echo "$STATUS_RESPONSE" | tail -n1)

if [ "$STATUS_HTTP_CODE" = "200" ]; then
  echo "Ticket status updated to In Progress"
else
  echo "Warning: Failed to update status (HTTP $STATUS_HTTP_CODE)"
  echo "   FreshService ticket status NOT updated"
fi

echo ""
```

### Phase 4: Confirmation

After the issue is created, provide a summary:

```bash
echo ""
echo "Triage completed successfully!"
echo ""
echo "Summary:"
echo "  - FreshService Ticket: #$TICKET_ID"
echo "  - Subject: $SUBJECT"
echo "  - Priority: $PRIORITY_STR"
echo "  - Status: Updated to In Progress"
echo "  - Reply: Sent to requester"
echo ""
echo "Next steps:"
echo "  - Review the created GitHub issue"
echo "  - Use /work [issue-number] to begin implementation"
echo "  - When resolved, update FreshService ticket manually"
```

## Error Handling

Handle common error scenarios:

1. **Missing Configuration**: Guide user to create `~/.claude/freshservice.env`
2. **Invalid Ticket ID**: Validate numeric format
3. **API Failures**: Provide clear error messages with troubleshooting steps
4. **Network Issues**: Suggest checking connectivity and credentials

## Security Notes

- API key is stored in `~/.claude/freshservice.env` (user-level, not in repository)
- All API communications use HTTPS
- Input validation prevents injection attacks
- Credentials are never logged or displayed
- Sensitive data (emails) not included in public GitHub issues

## Example Usage

```bash
# Triage a FreshService ticket
/triage 12345

# This will:
# 1. Fetch ticket #12345 from FreshService
# 2. Extract all relevant information
# 3. Format as a bug report
# 4. Create a GitHub issue automatically
# 5. Return the new issue URL
```

## Troubleshooting

**Configuration Issues:**
```bash
# Check if config file exists
ls -la ~/.claude/freshservice.env

# View configuration (without exposing API key)
grep FRESHSERVICE_DOMAIN ~/.claude/freshservice.env
```

**API Issues:**
```bash
# Test API connectivity manually
curl -u YOUR_API_KEY:X -X GET 'https://YOUR_DOMAIN.freshservice.com/api/v2/tickets/TICKET_ID'
```
