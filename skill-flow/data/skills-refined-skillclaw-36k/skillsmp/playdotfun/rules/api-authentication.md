---
name: api-authentication
description: Best practices for authenticating with Play.fun APIs.
metadata:
  tags: playfun, authentication, api, server, sdk
---

## When to use authentication

The following endpoints and methods require authentication via an HMAC signature:

| Endpoint                       | Method | Description                                            |
| ------------------------------ | ------ | ------------------------------------------------------ |
| /games/me                      | GET    | Get the authenticated user's games                     |
| /games                         | POST   | Register a new game                                    |
| /games/update/token-splits     | POST   | Update the reward distribution for a game              |
| /games/update/{gameId}         | POST   | Update a game (Must also be creator/owner of the game) |
| /play/dev/points               | GET    | Get points for a specific player in a game             |
| /play/dev/leaderboard/{gameId} | GET    | Get the leaderboard for a specific game                |
| /play/dev/batch-save-points    | POST   | Save points for players in a game                      |

## How to generate an HMAC signature

HMAC signatures are generated using the following parameters:

- The HTTP method (GET or POST)
- The endpoint path
- The user's Play.fun API key
- The user's Play.fun API secret

The `/user/hmac-signature` endpoint can be used to generate an HMAC signature for any of the above endpoints.

### Examples

```ts
// Generate an HMAC signature for the /games/me endpoint

const response = await fetch(`https://api.play.fun/user/hmac-signature`, {
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
```

```python
# Generate an HMAC signature for the /games/me endpoint
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
```

```bash
# Generate an HMAC signature for the /games/me endpoint
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

#### HMAC Signature Endpoint Response

Status: 200 OK

```json
{
  "data": {
    "signature": "HMAC_SIGNATURE"
  }
}
```
