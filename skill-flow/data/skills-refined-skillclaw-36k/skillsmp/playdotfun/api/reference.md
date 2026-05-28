---
name: api-reference
description: Complete API Reference for Play.fun
metadata:
  tags: playfun, api, openapi, sdk, reference
---

## Base URL

- **Production**: `https://api.opengameprotocol.com`
- **Interactive Docs**: [https://api.play.fun/api-reference](https://api.play.fun/api-reference)

All authenticated endpoints require HMAC-SHA256 authentication (see [Authentication](../rules/api-authentication.md)).

## OpenAPI Specification

| Format      | URL                                     |
| ----------- | --------------------------------------- |
| Interactive | https://api.play.fun/api-reference      |
| JSON        | https://api.play.fun/api-reference-json |
| YAML        | https://api.play.fun/api-reference-yaml |

## Games

### GET /games

List all games with pagination and filtering.

**Query Parameters:**

| Parameter | Type   | Default                  | Description               |
| --------- | ------ | ------------------------ | ------------------------- |
| `limit`   | number | 50                       | Results per page (1-100)  |
| `cursor`  | string | -                        | Pagination cursor         |
| `query`   | string | -                        | Search by game name       |
| `sortBy`  | string | totalRewardsPoolValueUsd | Sort field                |
| `sort`    | string | desc                     | Sort direction (asc/desc) |

**sortBy Options:** `totalRewardsPoolValueUsd`, `totalRewardsAllocatedUsd`, `createdAt`, `estimatedDailyRewardsUsd`, `name`, `marketCap`, `playerCount`

### GET /games/:id

Get a specific game by UUID.

### POST /games

Register a new game. **Requires authentication.**

**Request Body:**

```json
{
  "name": "string",
  "description": "string",
  "gameUrl": "string",
  "platform": "web|ios|android|steam|itch",
  "gameCoinSymbol": "string?",
  "twitter": "string?",
  "discord": "string?",
  "telegram": "string?",
  "isHTMLGame": "boolean?",
  "iframable": "boolean?",
  "maxScorePerSession": "number?",
  "maxSessionsPerDay": "number?",
  "maxCumulativePointsPerDay": "number?"
}
```

### POST /games/update/:gameId

Update an existing game. **Requires authentication. Must be game owner.**

### GET /games/:id/leaderboard

Get the daily leaderboard for a game.

### GET /games/me

Get games owned by authenticated user. **Requires authentication.**

## Play (Points)

### POST /play/dev/batch-save-points

Save points for one or more players. **Requires authentication.**

**Request Body:**

```json
{
  "gameApiKey": "game-uuid",
  "points": [{ "playerId": "string", "points": "string" }]
}
```

### GET /play/dev/points/:gameId/:playerId

Get points for a specific player. **Requires authentication.**

### GET /play/dev/leaderboard/:gameId

Get the developer leaderboard for a game. **Requires authentication.**

## Token Launcher

### POST /token-launcher/launch

Launch a playcoin for a game. **Requires authentication.**

**Request Body:**

```json
{
  "gameId": "uuid",
  "emissionDays": 7,
  "buyAmount": "string?",
  "gameCoinSymbol": "string?"
}
```

| Field            | Type    | Description                    |
| ---------------- | ------- | ------------------------------ |
| `gameId`         | uuid    | Your game's UUID               |
| `emissionDays`   | 7 \| 30 | Reward distribution period     |
| `buyAmount`      | string? | Initial buy amount in lamports |
| `gameCoinSymbol` | string? | Token symbol (max 10 chars)    |

### GET /token-launcher/launch/:jobId

Check playcoin launch job status.

## Tokens

### GET /tokens

List all tokens with pagination.

### GET /tokens/:mint

Get token details by Solana mint address.

## User

### GET /user/me

Get current authenticated user profile. **Requires authentication.**

### GET /user/balance

Get user wallet balances. **Requires authentication.**

### POST /user/reset-secret

Reset API secret key. **Requires authentication.**

## Response Format

All responses follow this structure:

```json
{
  "data": { ... },
  "error": null
}
```

Error responses:

```json
{
  "data": null,
  "error": {
    "message": "Error description",
    "code": "ERROR_CODE"
  }
}
```
