# EVE SSO Authentication Flow

Complete guide for implementing EVE Online Single Sign-On.

## Registration

1. Go to https://developers.eveonline.com/applications
2. Create new application
3. Set callback URL (e.g., `http://localhost:8000/callback`)
4. Select required scopes
5. Save Client ID and Secret Key

## Common Scopes

| Scope | Purpose |
|-------|---------|
| `esi-location.read_location.v1` | Character current system |
| `esi-location.read_online.v1` | Online/offline status |
| `esi-ui.write_waypoint.v1` | Set autopilot waypoints |
| `esi-assets.read_assets.v1` | Character assets |
| `esi-skills.read_skills.v1` | Character skills |
| `esi-characters.read_standings.v1` | NPC standings |
| `esi-corporations.read_corporation_membership.v1` | Corp info |

## OAuth2 Flow

### Step 1: Authorization URL

```python
import secrets
import urllib.parse

CLIENT_ID = "your_client_id"
CALLBACK_URL = "http://localhost:8000/callback"
SCOPES = ["esi-location.read_location.v1", "esi-ui.write_waypoint.v1"]

state = secrets.token_urlsafe(32)  # Store this for verification

params = {
    "response_type": "code",
    "redirect_uri": CALLBACK_URL,
    "client_id": CLIENT_ID,
    "scope": " ".join(SCOPES),
    "state": state
}

auth_url = f"https://login.eveonline.com/v2/oauth/authorize?{urllib.parse.urlencode(params)}"
# Redirect user to auth_url
```

### Step 2: Handle Callback

User returns with `?code=AUTHORIZATION_CODE&state=STATE`

```python
# Verify state matches what we sent
if request.args["state"] != stored_state:
    raise SecurityError("State mismatch")

auth_code = request.args["code"]
```

### Step 3: Exchange Code for Tokens

```python
import base64
import httpx

CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_secret"

credentials = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

async with httpx.AsyncClient() as client:
    response = await client.post(
        "https://login.eveonline.com/v2/oauth/token",
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={
            "grant_type": "authorization_code",
            "code": auth_code
        }
    )
    
    tokens = response.json()
    # {
    #   "access_token": "...",
    #   "token_type": "Bearer",
    #   "expires_in": 1199,
    #   "refresh_token": "..."
    # }
```

### Step 4: Decode JWT for Character Info

```python
import jwt

# Access token is a JWT - decode without verification to get character info
# (CCP signs it, we just need the payload)
token_data = jwt.decode(
    tokens["access_token"],
    options={"verify_signature": False}
)

character_id = token_data["sub"].split(":")[2]  # "CHARACTER:EVE:123456" → "123456"
character_name = token_data["name"]
```

### Step 5: Use Access Token

```python
async with httpx.AsyncClient() as client:
    response = await client.get(
        f"https://esi.evetech.net/latest/characters/{character_id}/location/",
        headers={
            "Authorization": f"Bearer {tokens['access_token']}",
            "User-Agent": "MyApp/1.0 (contact@example.com)"
        }
    )
    
    location = response.json()
    # {"solar_system_id": 30000142, "station_id": 60003760}
```

### Step 6: Refresh Token

Access tokens expire after ~20 minutes. Use refresh token:

```python
async with httpx.AsyncClient() as client:
    response = await client.post(
        "https://login.eveonline.com/v2/oauth/token",
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data={
            "grant_type": "refresh_token",
            "refresh_token": tokens["refresh_token"]
        }
    )
    
    new_tokens = response.json()
    # Store new access_token and refresh_token
```

## FastAPI Integration Example

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
import secrets

app = FastAPI()
sessions = {}  # Use Redis in production

@app.get("/login")
async def login():
    state = secrets.token_urlsafe(32)
    sessions[state] = {"status": "pending"}
    
    params = urllib.parse.urlencode({
        "response_type": "code",
        "redirect_uri": CALLBACK_URL,
        "client_id": CLIENT_ID,
        "scope": " ".join(SCOPES),
        "state": state
    })
    
    return RedirectResponse(
        f"https://login.eveonline.com/v2/oauth/authorize?{params}"
    )

@app.get("/callback")
async def callback(code: str, state: str):
    if state not in sessions:
        raise HTTPException(400, "Invalid state")
    
    # Exchange code for tokens...
    tokens = await exchange_code(code)
    
    # Store tokens in session
    sessions[state] = {
        "status": "authenticated",
        "tokens": tokens,
        "character_id": extract_character_id(tokens["access_token"])
    }
    
    return {"message": "Authenticated successfully"}
```

## Security Notes

1. **Never expose Client Secret** in frontend code
2. **Always verify state parameter** to prevent CSRF
3. **Store refresh tokens securely** (encrypted at rest)
4. **Implement token rotation** - refresh tokens change on use
5. **Handle revocation** - users can revoke access anytime
