# Authentication

The auth service path must be discovered dynamically - it is NOT always at `/auth`.

## Required Environment Variables

```
RESTSPACE_URL       - Server URL (optional, defaults to http://localhost:3100)
RESTSPACE_EMAIL     - Login email address
RESTSPACE_PASSWORD  - Login password
```

## Step 1: Find the Auth Service

```bash
# Use $RESTSPACE_URL directly (defaults to http://localhost:3100 if not set)

# Find auth service path
AUTH_PATH=$(curl -s "$RESTSPACE_URL/.well-known/restspace/services" | \
  jq -r 'to_entries | map(select(.value.source | contains("auth.rsm"))) | .[0].key // empty')

if [ -z "$AUTH_PATH" ]; then
  echo "No auth service found on this server"
  exit 1
fi

echo "Auth service at: $AUTH_PATH"
```

## Step 2: Login

```bash
# Login and store session cookie (credentials from env vars, never echoed)
curl -s -c cookies.txt -X POST "$RESTSPACE_URL$AUTH_PATH/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"$RESTSPACE_EMAIL\", \"password\": \"$RESTSPACE_PASSWORD\"}"
```

**Response (200 OK):**
```json
{
  "email": "user@example.com",
  "name": "User Name",
  "roles": "U",
  "exp": 1234567890
}
```

## Check Current User

```bash
curl -s -b cookies.txt "$RESTSPACE_URL$AUTH_PATH/user"
```

**Response (200 OK):**
```json
{
  "email": "user@example.com",
  "name": "User Name",
  "roles": "U",
  "sessionRemaining": 1800
}
```

## Logout

```bash
curl -s -b cookies.txt -X POST "$RESTSPACE_URL$AUTH_PATH/logout"
```

## Smart Login (Only if Needed)

Check if already authenticated before re-logging in:

```bash
# Only login if not already authenticated
curl -s -b cookies.txt "$RESTSPACE_URL$AUTH_PATH/user" | jq -e '.email' > /dev/null 2>&1 || \
  curl -s -c cookies.txt -X POST "$RESTSPACE_URL$AUTH_PATH/login" \
    -H "Content-Type: application/json" \
    -d "{\"email\": \"$RESTSPACE_EMAIL\", \"password\": \"$RESTSPACE_PASSWORD\"}"
```

## Complete Auth Flow

```bash
# Use $RESTSPACE_URL directly (defaults to http://localhost:3100 if not set)

# 1. Discover auth service
AUTH_PATH=$(curl -s "$RESTSPACE_URL/.well-known/restspace/services" | \
  jq -r 'to_entries | map(select(.value.source | contains("auth.rsm"))) | .[0].key // empty')

# 2. Login if needed
if [ -n "$AUTH_PATH" ]; then
  curl -s -b cookies.txt "$RESTSPACE_URL$AUTH_PATH/user" | jq -e '.email' > /dev/null 2>&1 || \
    curl -s -c cookies.txt -X POST "$RESTSPACE_URL$AUTH_PATH/login" \
      -H "Content-Type: application/json" \
      -d "{\"email\": \"$RESTSPACE_EMAIL\", \"password\": \"$RESTSPACE_PASSWORD\"}"
fi
```

## Security Notes

- Never echo `$RESTSPACE_EMAIL` or `$RESTSPACE_PASSWORD` values
- Use `-s` flag to suppress curl progress output
- Cookie file should be in a secure, non-committed location
- Sessions expire after configurable timeout (default 30 minutes)
- Sessions auto-refresh at 50% expiry on activity
