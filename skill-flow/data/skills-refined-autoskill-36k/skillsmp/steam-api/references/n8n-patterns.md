# n8n Integration Patterns

## HTTP Request Node Config

### Base Setup
```json
{
  "url": "https://api.steampowered.com/{interface}/{method}/{version}/",
  "authentication": "genericCredentialType",
  "genericAuthType": "httpQueryAuth"
}
```

### Query Parameters
```json
{
  "sendQuery": true,
  "queryParameters": {
    "parameters": [
      { "name": "steamid", "value": "={{ $json.steamid }}" },
      { "name": "format", "value": "json" }
    ]
  }
}
```

## Credential Setup

Use **HTTP Query Auth** credential:
- Name: `key`
- Value: `<YOUR_STEAM_API_KEY>`

## Common Patterns

### 1. Chain Player Info → Games
```
GetPlayerSummaries → GetOwnedGames

Expression: steamid = {{ $json.response.players[0].steamid }}
```

### 2. Loop Through Friends
```
GetFriendList → SplitInBatches → GetPlayerSummaries

Batch steamids (max 100): {{ $json.map(f => f.steamid).join(',') }}
```

### 3. Multi-Game Stats
```
GetOwnedGames → SplitInBatches → GetPlayerAchievements

Expression: appid = {{ $json.appid }}
```

## Expression Snippets

```javascript
// Extract first player steamid
{{ $json.response.players[0].steamid }}

// Join array of steamids
{{ $json.friendslist.friends.map(f => f.steamid).join(',') }}

// Filter games with playtime
{{ $json.response.games.filter(g => g.playtime_forever > 0) }}

// Format playtime (min → hours)
{{ Math.round($json.playtime_forever / 60) }} hours

// Build game image URL
http://media.steampowered.com/steamcommunity/public/images/apps/{{ $json.appid }}/{{ $json.img_icon_url }}.jpg

// Persona state to text
{{ ['Offline','Online','Busy','Away','Snooze','Trading','Playing'][$json.personastate] }}
```

## Error Handling

Add IF node after HTTP Request:
```javascript
// Check for valid response
{{ $json.response !== undefined }}

// Check for public profile
{{ $json.response.players[0].communityvisibilitystate === 3 }}
```
