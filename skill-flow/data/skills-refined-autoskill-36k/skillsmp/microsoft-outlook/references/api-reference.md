# Microsoft Graph API Reference

API endpoints and types used by the microsoft-outlook skill.

## Base URL

```
https://graph.microsoft.com/v1.0
```

## Authentication

All requests require an OAuth 2.0 Bearer token:

```
Authorization: Bearer <access_token>
```

## Endpoints

### User Profile

**GET /me**

Returns the authenticated user's profile.

```bash
GET https://graph.microsoft.com/v1.0/me
```

Response:
```json
{
  "id": "string",
  "displayName": "string",
  "surname": "string",
  "givenName": "string",
  "userPrincipalName": "string",
  "mail": "string",
  "jobTitle": "string",
  "mobilePhone": "string",
  "officeLocation": "string",
  "preferredLanguage": "string"
}
```

### List Messages

**GET /me/messages**

Returns messages from the user's mailbox.

```bash
GET https://graph.microsoft.com/v1.0/me/messages?$top=10&$select=subject,receivedDateTime,from,isRead,id,hasAttachments
```

Query parameters:
- `$top` - Number of messages to return (default: 10)
- `$select` - Fields to include in response
- `$filter` - OData filter expression
- `$orderby` - Sort order (default: receivedDateTime DESC)
- `$skip` - Number of items to skip (pagination)

Response:
```json
{
  "@odata.context": "string",
  "@odata.nextLink": "string (optional)",
  "value": [
    {
      "id": "string",
      "createdDateTime": "datetime",
      "lastModifiedDateTime": "datetime",
      "receivedDateTime": "datetime",
      "sentDateTime": "datetime",
      "hasAttachments": "boolean",
      "subject": "string",
      "bodyPreview": "string",
      "importance": "low | normal | high",
      "isRead": "boolean",
      "isDraft": "boolean",
      "from": {
        "emailAddress": {
          "name": "string",
          "address": "string"
        }
      },
      "toRecipients": [...],
      "ccRecipients": [...],
      "body": {
        "contentType": "text | html",
        "content": "string"
      }
    }
  ]
}
```

### Get Message

**GET /me/messages/{id}**

Returns a specific message.

```bash
GET https://graph.microsoft.com/v1.0/me/messages/{message-id}
```

### Download Message (MIME)

**GET /me/messages/{id}/$value**

Returns the message in MIME format (`.eml` file).

```bash
GET https://graph.microsoft.com/v1.0/me/messages/{message-id}/$value
```

Response: Raw MIME content (binary)

## Types

### MicrosoftUser

```typescript
interface MicrosoftUser {
  id: string;
  displayName: string;
  surname: string;
  givenName: string;
  userPrincipalName: string;
  mail?: string;
  jobTitle?: string;
  mobilePhone?: string;
  officeLocation?: string;
  preferredLanguage?: string;
}
```

### Message

```typescript
interface Message {
  id: string;
  createdDateTime: string;
  lastModifiedDateTime: string;
  changeKey: string;
  categories: string[];
  receivedDateTime: string;
  sentDateTime: string;
  hasAttachments: boolean;
  internetMessageId: string;
  subject: string;
  bodyPreview: string;
  importance: "low" | "normal" | "high";
  parentFolderId: string;
  conversationId: string;
  isDeliveryReceiptRequested: boolean | null;
  isReadReceiptRequested: boolean;
  isRead: boolean;
  isDraft: boolean;
  webLink: string;
  inferenceClassification: "focused" | "other";
  body: {
    contentType: "text" | "html";
    content: string;
  };
  sender: Recipient;
  from: Recipient;
  toRecipients: Recipient[];
  ccRecipients: Recipient[];
  bccRecipients: Recipient[];
  replyTo: Recipient[];
  flag: {
    flagStatus: "notFlagged" | "complete" | "flagged";
  };
}
```

### Recipient

```typescript
interface Recipient {
  emailAddress: EmailAddress;
}

interface EmailAddress {
  name: string;
  address: string;
}
```

### MessageListResponse

```typescript
interface MessageListResponse {
  "@odata.context": string;
  "@odata.nextLink"?: string;
  value: Message[];
}
```

## OAuth Configuration

### Endpoints

- **Authorization**: `https://login.microsoftonline.com/common/oauth2/v2.0/authorize`
- **Token**: `https://login.microsoftonline.com/common/oauth2/v2.0/token`

### Scopes

```
User.Read Mail.Read offline_access
```

- `User.Read` - Read user profile
- `Mail.Read` - Read user's mail
- `offline_access` - Get refresh tokens

### PKCE Flow

The skill uses Authorization Code Flow with PKCE:

1. Generate code verifier (32 random bytes, base64url encoded)
2. Generate code challenge (SHA-256 hash of verifier, base64url encoded)
3. Include `code_challenge` and `code_challenge_method=S256` in authorization request
4. Include `code_verifier` in token exchange request

## Error Responses

Graph API errors return:

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "innerError": {
      "date": "datetime",
      "request-id": "string",
      "client-request-id": "string"
    }
  }
}
```

Common error codes:
- `InvalidAuthenticationToken` - Token expired or invalid
- `Authorization_RequestDenied` - Insufficient permissions
- `ResourceNotFound` - Message/resource not found
- `BadRequest` - Invalid request parameters

## Rate Limits

Microsoft Graph has throttling limits:
- Per-app: 2000 requests per second
- Per-user per-app: 10000 requests per 10 minutes

When throttled, responses include:
- HTTP 429 status
- `Retry-After` header with seconds to wait

## Additional Resources

- [Microsoft Graph API documentation](https://learn.microsoft.com/en-us/graph/api/overview)
- [Mail API reference](https://learn.microsoft.com/en-us/graph/api/resources/mail-api-overview)
- [Authentication overview](https://learn.microsoft.com/en-us/graph/auth/)
