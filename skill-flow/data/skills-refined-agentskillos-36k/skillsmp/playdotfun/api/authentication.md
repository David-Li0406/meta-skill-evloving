---
name: api-authentication
description: HMAC-SHA256 Authentication for Play.fun API
metadata:
  tags: playfun, authentication, api, hmac, security
---

## Overview

Play.fun uses HMAC-SHA256 authentication for secure, stateless API requests. This ensures that only authorized users can access protected endpoints.

## Getting Credentials

1. Sign up at [https://play.fun](https://play.fun)
2. Navigate to **Dashboard > Settings > API Keys** (or Creator Dashboard > Creator Credentials)
3. Your **API Key** is your user ID
4. Generate or view your **Secret Key**

## Endpoints Requiring Authentication

| Endpoint                        | Method | Description                   |
| ------------------------------- | ------ | ----------------------------- |
| `/games/me`                     | GET    | Get your registered games     |
| `/games`                        | POST   | Register a new game           |
| `/games/update/:gameId`         | POST   | Update a game (must be owner) |
| `/games/update/token-splits`    | POST   | Update reward distribution    |
| `/play/dev/points`              | GET    | Get player points             |
| `/play/dev/leaderboard/:gameId` | GET    | Get game leaderboard          |
| `/play/dev/batch-save-points`   | POST   | Save player points            |

## HMAC Signature Generation

### Signature Format

Signatures are generated from these components:

- HTTP method (lowercase)
- Endpoint path (lowercase)
- Unix timestamp (seconds)

```typescript
import crypto from 'crypto';

function generateSignature(
  secretKey: string,
  method: string,
  path: string,
  timestamp: number,
): string {
  const dataToSign = [method.toLowerCase(), path.toLowerCase(), timestamp].join('\n');

  return crypto.createHmac('sha256', secretKey).update(dataToSign).digest('hex');
}
```

### Authorization Header

```
Authorization: HMAC-SHA256 apiKey=<your-api-key>, signature=<signature>, timestamp=<unix-timestamp>
```

## Example Request

```typescript
const timestamp = Math.floor(Date.now() / 1000);
const signature = generateSignature(secretKey, 'GET', '/games/me', timestamp);

const response = await fetch('https://api.opengameprotocol.com/games/me', {
  headers: {
    Authorization: `HMAC-SHA256 apiKey=${apiKey}, signature=${signature}, timestamp=${timestamp}`,
    'Content-Type': 'application/json',
  },
});
```

## Using the Signature Helper Endpoint

Play.fun provides a helper endpoint to generate signatures:

### POST /user/hmac-signature

```typescript
const response = await fetch('https://api.play.fun/user/hmac-signature', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    method: 'GET',
    path: '/games/me',
    apiKey: 'YOUR_API_KEY',
    apiSecret: 'YOUR_API_SECRET',
  }),
});

const { data } = await response.json();
// data.signature contains the HMAC signature
```

### Python Example

```python
import requests

response = requests.post(
    'https://api.play.fun/user/hmac-signature',
    json={
        'method': 'GET',
        'path': '/games/me',
        'apiKey': 'YOUR_API_KEY',
        'apiSecret': 'YOUR_API_SECRET',
    }
)

signature = response.json()['data']['signature']
```

### cURL Example

```bash
curl -X POST \
  https://api.play.fun/user/hmac-signature \
  -H 'Content-Type: application/json' \
  -d '{
    "method": "GET",
    "path": "/games/me",
    "apiKey": "YOUR_API_KEY",
    "apiSecret": "YOUR_API_SECRET"
  }'
```

## MCP Server Authentication

When using the Play.fun MCP server, pass credentials as headers:

```
x-api-key: your-api-key
x-secret-key: your-secret-key
x-base-url: https://api.opengameprotocol.com (optional)
```

## Security Best Practices

1. **Never expose your Secret Key** in client-side code or version control
2. **Use environment variables** to store credentials
3. **Rotate secrets periodically** using the `reset_api_secret` tool or API
4. **Timestamp validation**: Signatures expire after 5 minutes
5. **Server-side only**: Generate signatures on your server, never in the browser
