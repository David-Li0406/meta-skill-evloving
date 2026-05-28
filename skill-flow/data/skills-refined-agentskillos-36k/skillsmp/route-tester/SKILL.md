---
name: route-tester
description: Test authenticated API routes in ActionPhase using JWT Bearer token authentication. Use when testing API endpoints, validating route functionality, debugging authentication issues, or verifying request/response data. Includes patterns for using backend/scripts/api-test.sh and curl with proper authorization headers.
---

# ActionPhase Route Tester Skill

## Purpose

This skill provides patterns for testing authenticated routes in ActionPhase using JWT Bearer token authentication with the Go backend.

## When to Use This Skill

- Testing new API endpoints
- Validating route functionality after changes
- Debugging authentication issues
- Testing POST/PUT/DELETE operations
- Verifying request/response data
- End-to-end API testing
- Integration testing before E2E tests

## ActionPhase Authentication Overview

ActionPhase uses:
- **JWT Bearer tokens** (Authorization header)
- **Token lifetime**: 15 minutes (access token)
- **Refresh tokens**: 7 days (stored in database sessions)
- **Token storage**: Frontend stores in memory + localStorage
- **Backend**: Go with Chi router + JWT middleware

**See**: `/docs/adrs/003-authentication-strategy.md` for complete details

---

## Testing Methods

### Method 1: api-test.sh (RECOMMENDED)

The `api-test.sh` script handles authentication and provides convenient commands for testing.

**Location**: `backend/scripts/api-test.sh`

#### Quick Start

```bash
# 1. Login and save token
./backend/scripts/api-test.sh login-player

# 2. Test endpoints
./backend/scripts/api-test.sh games
./backend/scripts/api-test.sh game 164
./backend/scripts/api-test.sh characters 164
```

#### Available Commands

**Authentication**:
```bash
./api-test.sh login [username]     # Login as any user (default: TestPlayer1)
./api-test.sh login-gm              # Login as TestGM
./api-test.sh login-player          # Login as TestPlayer1
./api-test.sh test-token            # Verify current token is valid
```

**API Endpoints**:
```bash
./api-test.sh health                # Check backend health
./api-test.sh status                # Complete status check
./api-test.sh games                 # List all games
./api-test.sh game [id]             # Get game details (default: 164)
./api-test.sh characters [game_id]  # Get characters (default: 164)
./api-test.sh posts [game_id]       # Get posts (default: 164)
./api-test.sh comments <post_id>    # Get comments for post
```

**Create Operations**:
```bash
./api-test.sh create-post [game_id] [character_id] [content]
./api-test.sh create-comment <post_id> [character_id] [content]
```

**Feature Testing**:
```bash
./api-test.sh test-mentions         # End-to-end mention testing
```

#### What the Script Does

1. Logs in via `/api/v1/auth/login` with test credentials
2. Extracts JWT token from response
3. Saves token to `/tmp/api-token.txt`
4. Uses token in `Authorization: Bearer <token>` header for all requests
5. Parses responses with `jq` for readability

#### Script Output

The script outputs:
- Colored status indicators (✅/❌)
- JSON responses formatted with jq
- Error messages if requests fail
- Token validation results

---

### Method 2: Manual curl with Token

Use the token saved by api-test.sh for manual testing:

```bash
# Get the token
TOKEN=$(cat /tmp/api-token.txt)

# Use in curl requests
curl -s -H "Authorization: Bearer $TOKEN" \
  http://localhost:3000/api/v1/games | jq '.'
```

#### Manual curl Patterns

**GET Request**:
```bash
curl -s -H "Authorization: Bearer $(cat /tmp/api-token.txt)" \
  "http://localhost:3000/api/v1/games/164" | jq '.'
```

**POST Request**:
```bash
curl -s -X POST \
  -H "Authorization: Bearer $(cat /tmp/api-token.txt)" \
  -H "Content-Type: application/json" \
  -d '{"title": "New Game", "description": "Test game"}' \
  "http://localhost:3000/api/v1/games" | jq '.'
```

**PUT Request**:
```bash
curl -s -X PUT \
  -H "Authorization: Bearer $(cat /tmp/api-token.txt)" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title"}' \
  "http://localhost:3000/api/v1/games/164" | jq '.'
```

**DELETE Request**:
```bash
curl -s -X DELETE \
  -H "Authorization: Bearer $(cat /tmp/api-token.txt)" \
  "http://localhost:3000/api/v1/games/164" | jq '.'
```

---

## Common Testing Patterns

### Test New API Endpoint

```bash
# 1. Login first
./backend/scripts/api-test.sh login-player

# 2. Test the endpoint
curl -s -H "Authorization: Bearer $(cat /tmp/api-token.txt)" \
  "http://localhost:3000/api/v1/your-new-endpoint" | jq '.'

# 3. Verify response structure
# 4. Check database changes if applicable
```

### Test Character Creation Flow

```bash
# 1. Login as player
./backend/scripts/api-test.sh login-player

# 2. Create character
curl -s -X POST \
  -H "Authorization: Bearer $(cat /tmp/api-token.txt)" \
  -H "Content-Type: application/json" \
  -d '{
    "game_id": 164,
    "name": "Test Character",
    "character_sheet": {"class": "Warrior", "level": 1}
  }' \
  "http://localhost:3000/api/v1/characters" | jq '.'

# 3. Verify in database
# 4. Login as GM and test approval workflow
./backend/scripts/api-test.sh login-gm
```

### Test Phase Transition

```bash
# Login as GM
./backend/scripts/api-test.sh login-gm

# Advance phase
curl -s -X POST \
  -H "Authorization: Bearer $(cat /tmp/api-token.txt)" \
  -H "Content-Type: application/json" \
  -d '{"game_id": 164}' \
  "http://localhost:3000/api/v1/phases/advance" | jq '.'

# Verify phase changed
./backend/scripts/api-test.sh game 164 | jq '.current_phase'
```

### Test Private Messages

```bash
# Login as Player 1
./backend/scripts/api-test.sh login TestPlayer1

# Send message to Player 2
curl -s -X POST \
  -H "Authorization: Bearer $(cat /tmp/api-token.txt)" \
  -H "Content-Type: application/json" \
  -d '{
    "recipient_character_id": 1320,
    "content": "Test private message"
  }' \
  "http://localhost:3000/api/v1/games/164/messages/private" | jq '.'

# Login as Player 2 and check messages
./backend/scripts/api-test.sh login TestPlayer2
./backend/scripts/api-test.sh posts 164
```

### Test with Query Parameters

```bash
curl -s -H "Authorization: Bearer $(cat /tmp/api-token.txt)" \
  "http://localhost:3000/api/v1/games/164/posts?limit=10&offset=0" | jq '.'
```

---

## Test Credentials

**Available Test Users**:

| Username | Password | Role |
|----------|----------|------|
| TestGM | testpassword123 | Game Master |
| TestPlayer1 | testpassword123 | Player |
| TestPlayer2 | testpassword123 | Player |
| TestPlayer3 | testpassword123 | Player |

**Test Game**: Game ID `164` (use this for testing)

**See**: `.claude/context/TEST_DATA.md` for complete test fixture documentation

---

## API Structure

### Base URL

```
http://localhost:3000/api/v1
```

### Route Structure

All routes follow REST conventions:

```
/api/v1/{resource}
/api/v1/{resource}/{id}
/api/v1/{resource}/{id}/{sub-resource}
```

**Examples**:
- `/api/v1/games` - List games
- `/api/v1/games/164` - Get game 164
- `/api/v1/games/164/characters` - List characters in game 164
- `/api/v1/games/164/posts` - List posts in game 164

### Authentication Endpoints

```
POST /api/v1/auth/login          # Login (returns JWT)
POST /api/v1/auth/logout         # Logout
GET  /api/v1/auth/me             # Get current user
POST /api/v1/auth/refresh        # Refresh access token
```

### Main Resource Endpoints

**Games**:
```
GET    /api/v1/games              # List games
POST   /api/v1/games              # Create game (GM only)
GET    /api/v1/games/{id}         # Get game details
PUT    /api/v1/games/{id}         # Update game (GM only)
DELETE /api/v1/games/{id}         # Delete game (GM only)
```

**Characters**:
```
GET    /api/v1/games/{game_id}/characters              # List characters
POST   /api/v1/characters                              # Create character
GET    /api/v1/characters/{id}                         # Get character
PUT    /api/v1/characters/{id}                         # Update character
POST   /api/v1/characters/{id}/approve                 # Approve (GM only)
POST   /api/v1/characters/{id}/reject                  # Reject (GM only)
```

**Messaging**:
```
GET    /api/v1/games/{game_id}/posts                   # Common room posts
POST   /api/v1/games/{game_id}/posts                   # Create post
GET    /api/v1/games/{game_id}/posts/{id}/comments    # Get comments
POST   /api/v1/games/{game_id}/posts/{id}/comments    # Create comment
GET    /api/v1/games/{game_id}/messages/private       # Private messages
POST   /api/v1/games/{game_id}/messages/private       # Send private message
```

**Phases**:
```
POST   /api/v1/phases/advance                          # Advance phase (GM only)
GET    /api/v1/games/{game_id}/phases/current         # Get current phase
```

**See**: `.claude/reference/API_DOCUMENTATION.md` for complete API reference

---

## Testing Checklist

Before testing a route:

- [ ] Backend server is running (`just dev`)
- [ ] Database is migrated (`just migrate`)
- [ ] Test fixtures are loaded (if needed)
- [ ] You have a valid token (`./api-test.sh login-player`)
- [ ] You know the full route path
- [ ] You know the HTTP method (GET/POST/PUT/DELETE)
- [ ] You have the request body prepared (if POST/PUT)
- [ ] You know the expected response structure
- [ ] You can verify changes (database, logs, etc.)

---

## Verifying Database Changes

After testing routes that modify data:

```bash
# Connect to PostgreSQL
PGPASSWORD=example psql -h localhost -U postgres -d actionphase

# Check specific tables
actionphase=# SELECT * FROM games WHERE id = 164;
actionphase=# SELECT * FROM characters WHERE game_id = 164;
actionphase=# SELECT * FROM posts WHERE game_id = 164 ORDER BY created_at DESC LIMIT 5;
actionphase=# SELECT * FROM sessions WHERE username = 'TestPlayer1';

# Or use justfile command
just psql
```

**Quick queries**:
```sql
-- Latest posts
SELECT id, character_id, content, created_at
FROM posts
WHERE game_id = 164
ORDER BY created_at DESC
LIMIT 10;

-- Character mentions
SELECT p.id, p.content, p.mentioned_character_ids
FROM posts p
WHERE game_id = 164
  AND mentioned_character_ids IS NOT NULL
ORDER BY created_at DESC;

-- Current phase
SELECT id, title, current_phase, phase_number
FROM games
WHERE id = 164;
```

---

## Debugging Failed Tests

### 401 Unauthorized

**Possible causes**:
1. No token provided
2. Token expired (15 minute lifetime)
3. Invalid token format
4. JWT secret mismatch

**Solutions**:
```bash
# Check if backend is running
curl http://localhost:3000/health

# Get a fresh token
./backend/scripts/api-test.sh login-player

# Verify token works
./backend/scripts/api-test.sh test-token

# Check token format (should start with "eyJ")
cat /tmp/api-token.txt
```

### 403 Forbidden

**Possible causes**:
1. User lacks required permissions
2. Not the GM for GM-only routes
3. Not the owner of the resource
4. Character not approved yet

**Solutions**:
```bash
# For GM-only routes, login as GM
./backend/scripts/api-test.sh login-gm

# Check user info
./backend/scripts/api-test.sh test-token

# Verify ownership in database
just psql
```

### 404 Not Found

**Possible causes**:
1. Incorrect URL
2. Resource doesn't exist
3. Route not implemented yet
4. Typo in endpoint path

**Solutions**:
```bash
# Check route exists in backend/pkg/http/root.go
grep -r "your-route" backend/pkg/http/

# Verify resource exists
just psql
# Then: SELECT * FROM games WHERE id = 164;

# Check server logs
# (server should print route registrations on startup)
```

### 500 Internal Server Error

**Possible causes**:
1. Database connection issue
2. Missing required fields
3. Validation error
4. Application panic/error

**Solutions**:
```bash
# Check server logs in terminal
# Backend prints detailed error logs with correlation IDs

# Check database is running
docker ps | grep postgres

# Verify request body structure
# Compare with models in backend/pkg/core/models.go

# Check correlation ID in error response
# Search logs for that correlation ID
```

---

## Testing Workflow

### 1. Unit Tests → 2. API Tests → 3. Manual Tests → 4. E2E Tests

**This skill covers steps 2 and 3.**

#### Step-by-Step Testing Flow

1. **Write/modify backend code**
2. **Run unit tests**: `just test-mocks`
3. **Start backend**: `just dev`
4. **Test API with curl/api-test.sh** ← **This skill**
5. **Verify in database**: `just psql`
6. **Test in UI manually**
7. **Write E2E tests**: Only after API works

**See**: `.claude/context/TESTING.md` for complete testing strategy

---

## Integration with Other Tools

### Use with Test Fixtures

```bash
# Load test fixtures
./backend/pkg/db/test_fixtures/apply_e2e.sh

# Now test with known data
./backend/scripts/api-test.sh game 164
./backend/scripts/api-test.sh characters 164
```

### Use Before E2E Tests

```bash
# 1. Test API endpoint works
./backend/scripts/api-test.sh create-post 164 1319 "Test content"

# 2. Verify response structure is correct

# 3. NOW write Playwright test
# The API endpoint is confirmed working
```

### Use with justfile Commands

```bash
# justfile integrates api-test.sh
just api-login          # Login as player
just api-login-gm       # Login as GM
just api-games          # List games
just api-game 164       # Get game 164
```

---

## Environment Variables

```bash
# Override API base URL
API_BASE_URL=http://localhost:3000 ./backend/scripts/api-test.sh games

# Use different port
API_BASE_URL=http://localhost:8080 ./backend/scripts/api-test.sh health
```

---

## Common Scenarios

### Scenario 1: Testing a New POST Endpoint

```bash
# 1. Start backend
just dev

# 2. Login
./backend/scripts/api-test.sh login-player

# 3. Test endpoint
curl -s -X POST \
  -H "Authorization: Bearer $(cat /tmp/api-token.txt)" \
  -H "Content-Type: application/json" \
  -d '{"field": "value"}' \
  "http://localhost:3000/api/v1/your-endpoint" | jq '.'

# 4. Verify in database
just psql
# Then: SELECT * FROM your_table ORDER BY created_at DESC LIMIT 1;

# 5. Test error cases
curl -s -X POST \
  -H "Authorization: Bearer $(cat /tmp/api-token.txt)" \
  -H "Content-Type: application/json" \
  -d '{"invalid": "data"}' \
  "http://localhost:3000/api/v1/your-endpoint" | jq '.'

# Should return 400 with validation error
```

### Scenario 2: Testing Permission-Based Access

```bash
# Test as Player (should fail)
./backend/scripts/api-test.sh login-player
curl -s -X POST \
  -H "Authorization: Bearer $(cat /tmp/api-token.txt)" \
  "http://localhost:3000/api/v1/phases/advance" | jq '.'
# Should return 403

# Test as GM (should succeed)
./backend/scripts/api-test.sh login-gm
curl -s -X POST \
  -H "Authorization: Bearer $(cat /tmp/api-token.txt)" \
  "http://localhost:3000/api/v1/phases/advance" | jq '.'
# Should return 200
```

### Scenario 3: End-to-End Feature Test

```bash
# Complete workflow test
echo "=== Testing Character Creation & Approval ==="

# 1. Player creates character
./backend/scripts/api-test.sh login-player
CHAR=$(curl -s -X POST \
  -H "Authorization: Bearer $(cat /tmp/api-token.txt)" \
  -H "Content-Type: application/json" \
  -d '{
    "game_id": 164,
    "name": "Test Character",
    "character_sheet": {"class": "Mage"}
  }' \
  "http://localhost:3000/api/v1/characters")

CHAR_ID=$(echo "$CHAR" | jq -r '.id')
echo "Created character: $CHAR_ID"

# 2. GM approves character
./backend/scripts/api-test.sh login-gm
curl -s -X POST \
  -H "Authorization: Bearer $(cat /tmp/api-token.txt)" \
  "http://localhost:3000/api/v1/characters/$CHAR_ID/approve" | jq '.'

# 3. Verify character is approved
curl -s -H "Authorization: Bearer $(cat /tmp/api-token.txt)" \
  "http://localhost:3000/api/v1/characters/$CHAR_ID" | jq '.status'
# Should return "approved"

echo "✅ Character workflow complete"
```

---

## Key Files

- **Testing script**: `backend/scripts/api-test.sh`
- **API routes**: `backend/pkg/http/root.go`
- **Handler implementations**: `backend/pkg/*/api.go`
- **Test fixtures**: `backend/pkg/db/test_fixtures/*.sql`
- **justfile**: Development commands that wrap api-test.sh

---

## Related Skills & Context

- **backend-dev-guidelines** - Patterns for implementing API endpoints
- **database-operations** - Database schema and query patterns
- **authentication** - JWT authentication details
- **test-fixtures** - Test data setup and usage

**Context Files**:
- `.claude/context/TESTING.md` - Testing strategy
- `.claude/context/TEST_DATA.md` - Test fixtures reference
- `.claude/context/ARCHITECTURE.md` - Request flow
- `.claude/reference/API_DOCUMENTATION.md` - Complete API reference

---

**Skill Status**: COMPLETE ✅
**Authentication**: JWT Bearer tokens ✅
**Testing Script**: `backend/scripts/api-test.sh` ✅
**Integration**: Works with test fixtures, justfile, E2E tests ✅
