# Test Fixtures

Complete guide to test data management in ActionPhase.

## Overview

ActionPhase uses a sophisticated fixture system to support **parallel test execution** with **isolated test data** for each worker.

---

## Fixture Types

### 1. Common Fixtures

**Purpose**: Shared base data needed by all tests

**Location**: `backend/pkg/db/test_fixtures/common/*.sql`

**Includes**:
- Base users (TestGM, TestPlayer1-5, TestAudience)
- System configuration data
- Reference data (e.g., game templates)

**Applied by**: `apply_common.sh`

### 2. E2E Worker Fixtures

**Purpose**: Worker-specific test data with ID offsets for parallel execution

**Location**: `backend/pkg/db/test_fixtures/e2e/*.sql`

**Includes**:
- Test games (164-168, 200-210, 300-310, etc.)
- Game participants, phases, characters
- Posts, messages, action submissions
- **Worker-specific variants** with ID offsets

**Applied by**: `apply_e2e_worker.sh <worker_index>`

---

## Test Users

### Base Test Users (Worker 0)

**All passwords**: `testpassword123`
**⚠️ Important**: Usernames are **case-sensitive** (use PascalCase!)

| User | Email | Username | Role |
|------|-------|----------|------|
| GM | `test_gm@example.com` | `TestGM` | Game Master |
| Player 1 | `test_player1@example.com` | `TestPlayer1` | Player |
| Player 2 | `test_player2@example.com` | `TestPlayer2` | Player |
| Player 3 | `test_player3@example.com` | `TestPlayer3` | Player |
| Player 4 | `test_player4@example.com` | `TestPlayer4` | Player |
| Player 5 | `test_player5@example.com` | `TestPlayer5` | Player |
| Audience | `test_audience@example.com` | `TestAudience` | Audience |

### Worker-Specific Users (Workers 1-5)

For parallel execution, workers 1-5 get user variants:

| Worker | GM Email | Player 1 Email | Username |
|--------|----------|----------------|----------|
| Worker 1 | `test_gm_1@example.com` | `test_player1_1@example.com` | `TestGM_1`, `TestPlayer1_1` |
| Worker 2 | `test_gm_2@example.com` | `test_player1_2@example.com` | `TestGM_2`, `TestPlayer1_2` |
| Worker 3 | `test_gm_3@example.com` | `test_player1_3@example.com` | `TestGM_3`, `TestPlayer1_3` |
| Worker 4 | `test_gm_4@example.com` | `test_player1_4@example.com` | `TestGM_4`, `TestPlayer1_4` |
| Worker 5 | `test_gm_5@example.com` | `test_player1_5@example.com` | `TestGM_5`, `TestPlayer1_5` |

**Password**: Same for all workers: `testpassword123`

---

## Test Games

### Base Game IDs (Worker 0)

Games organized by testing purpose:

| ID Range | Purpose | Example Games |
|----------|---------|---------------|
| 164-168 | Common Room testing | Game 164: "Shadows Over Innsmouth" (common room phase) |
| 200-210 | Action/Phase testing | Game 200: "The Heist" (action submission testing) |
| 300-310 | Character management | Game 300: "Character workflows" |
| 335-345 | Game lifecycle | Game 335: "Complete lifecycle" |
| 400-410 | Messaging | Game 400: "Private messages" |
| 600-610 | Character workflows | Game 600: "Character approval" |

### Worker Game ID Offsets

To support parallel execution, each worker gets **isolated games** with offset IDs:

**Formula**: `Worker Game ID = Base ID + (Worker Index × 10,000)`

| Worker | Game 164 | Game 200 | Game 300 |
|--------|----------|----------|----------|
| Worker 0 | 164 | 200 | 300 |
| Worker 1 | 10164 | 10200 | 10300 |
| Worker 2 | 20164 | 20200 | 20300 |
| Worker 3 | 30164 | 30200 | 30300 |
| Worker 4 | 40164 | 40200 | 40300 |
| Worker 5 | 50164 | 50200 | 50300 |

**Why offsets?**: Each worker operates on independent data, preventing test interference.

---

## Worker Fixture System

### How It Works

When E2E tests run, `global-setup.ts` automatically loads fixtures for all 6 workers:

```typescript
// frontend/e2e/global-setup.ts
async function globalSetup() {
  // 1. Apply common fixtures (shared by all workers)
  execSync('env DB_NAME=actionphase ./backend/pkg/db/test_fixtures/apply_common.sh');

  // 2. Apply worker-specific fixtures for 6 parallel workers
  for (let workerIndex = 0; workerIndex <= 5; workerIndex++) {
    execSync(`env DB_NAME=actionphase ./backend/pkg/db/test_fixtures/apply_e2e_worker.sh ${workerIndex}`);
  }
}
```

### Worker Fixture Script Details

**Script**: `backend/pkg/db/test_fixtures/apply_e2e_worker.sh`

**What it does**:
1. Takes a worker index (0-5) as argument
2. Reads base E2E fixture SQL files
3. **Replaces user references** with worker-specific variants
4. **Offsets game IDs** using Python script for reliable arithmetic
5. Applies modified SQL to database

### User Replacement Logic

**Worker 0**: Uses original users
```sql
-- Original SQL
INSERT INTO game_participants (game_id, user_id, role)
VALUES (164, (SELECT id FROM users WHERE email = 'test_gm@example.com'), 'gm');
```

**Worker 1+**: Replaces users with suffixed variants
```sql
-- Worker 1 SQL (after replacement)
INSERT INTO game_participants (game_id, user_id, role)
VALUES (10164, (SELECT id FROM users WHERE email = 'test_gm_1@example.com'), 'gm');
```

**Replacement patterns**:
- `'TestGM'` → `'TestGM_1'` (for Worker 1)
- `test_gm@` → `test_gm_1@`
- `'TestPlayer1'` → `'TestPlayer1_1'`
- `test_player1@` → `test_player1_1@`

### Game ID Offset Logic

**Uses Python for reliable arithmetic** (regex replacements with math):

```python
# 1. Offset game IDs in INSERT INTO games statements
# Only match 1-3 digit IDs (original range) to avoid double-offsetting
content = re.sub(
    r'(INSERT INTO games \([^)]*\bid\b[^)]*\)\s+VALUES\s*\(\s*)(\d{1,3})(\s*,)',
    lambda m: m.group(1) + offset_id(m.group(2)) + m.group(3),
    content
)

# 2. Offset game_id in related tables (game_participants, game_phases, etc.)
content = re.sub(
    r'(INSERT INTO (?!games\b)\w+\s*\([^)]*\bgame_id\b[^)]*\)\s+VALUES\s*\(\s*)(\d{1,3})(\s*,)',
    lambda m: m.group(1) + offset_id(m.group(2)) + m.group(3),
    content
)

# 3. Offset game_id variable assignments: game_id := 164;
content = re.sub(
    r'\b(game_?\w*_id(?:\s+(?:INT|INTEGER))?)\s*:=\s*(\d{1,3});',
    lambda m: f'{m.group(1)} := {offset_id(m.group(2))};',
    content
)

# 4. Offset DELETE statements: DELETE FROM games WHERE id IN (164, 200);
content = re.sub(
    r'(DELETE FROM games WHERE id IN \()([\d,\s]+)(\))',
    lambda m: m.group(1) + ','.join(offset_id(id) for id in m.group(2).split(',')) + m.group(3),
    content
)
```

**Offset function**:
```python
def offset_id(id_str):
    return str(int(id_str) + offset)  # offset = worker_index * 10000
```

### Special Handling

**Title-based DELETE statements removed**:
```sql
-- This type of DELETE can't be offset (removed by script)
DELETE FROM games WHERE title IN ('Game Title 1', 'Game Title 2');
```

**ID-based DELETE statements preserved** (offsettable):
```sql
-- This type of DELETE can be offset (preserved and modified)
DELETE FROM games WHERE id IN (164, 200, 300);
-- Becomes (Worker 1): DELETE FROM games WHERE id IN (10164, 10200, 10300);
```

---

## Fixture Commands

### Load All E2E Fixtures (Automatic)

```bash
# Happens automatically before E2E tests via global-setup.ts
just e2e
```

### Manual Fixture Loading

```bash
# Load fixtures for all 6 workers
just load-e2e

# Load common fixtures only
./backend/pkg/db/test_fixtures/apply_common.sh

# Load fixtures for specific worker
DB_NAME=actionphase ./backend/pkg/db/test_fixtures/apply_e2e_worker.sh 0  # Worker 0
DB_NAME=actionphase ./backend/pkg/db/test_fixtures/apply_e2e_worker.sh 1  # Worker 1
```

### Verify Fixtures Loaded

```bash
# Check users exist
PGPASSWORD=example psql -h localhost -U postgres -d actionphase \
  -c "SELECT username FROM users WHERE username LIKE 'Test%' ORDER BY username;"

# Check games exist for Worker 0
PGPASSWORD=example psql -h localhost -U postgres -d actionphase \
  -c "SELECT id, title FROM games WHERE id BETWEEN 164 AND 610 ORDER BY id;"

# Check games exist for Worker 1
PGPASSWORD=example psql -h localhost -U postgres -d actionphase \
  -c "SELECT id, title FROM games WHERE id BETWEEN 10164 AND 10610 ORDER BY id;"
```

---

## Using Fixtures in Tests

### Backend Tests

```go
func TestGameService(t *testing.T) {
    // Use testDB helper
    testDB := setupTestDB(t)
    defer testDB.Cleanup()

    // Create test data
    user := testDB.CreateTestUser(t, "testuser", "test@example.com")
    game := testDB.CreateTestGame(t, user.ID, "Test Game")

    // Run test
    result, err := gameService.GetGame(ctx, game.ID)
    require.NoError(t, err)
    assert.Equal(t, "Test Game", result.Title)
}
```

### Frontend Component Tests

```typescript
// Mock API responses in component tests
import { http, HttpResponse } from 'msw';
import { server } from '@/test-utils/msw-server';

test('renders game list', async () => {
  // Mock API with test data
  server.use(
    http.get('/api/v1/games', () => {
      return HttpResponse.json([
        { id: 164, title: 'Shadows Over Innsmouth' },
        { id: 200, title: 'The Heist' },
      ]);
    })
  );

  // Render and verify
  render(<GameList />);
  await screen.findByText('Shadows Over Innsmouth');
  await screen.findByText('The Heist');
});
```

### E2E Tests (Playwright)

```typescript
import { test, expect } from '@playwright/test';
import { loginAsPlayer } from '../helpers/auth';

test('can view game details', async ({ page }) => {
  // Login as test user
  await loginAsPlayer(page, 'TestPlayer1');

  // Navigate to test game (Worker 0)
  await page.goto('/games/164');

  // Verify fixture data
  await expect(page.getByText('Shadows Over Innsmouth')).toBeVisible();
});
```

---

## Key Test Games

### Game 164: "Shadows Over Innsmouth"

**State**: `in_progress`
**Current Phase**: Common Room
**Purpose**: Testing common room posts, mentions, notifications

**Participants**:
- GM: TestGM
- Players: TestPlayer1, TestPlayer2, TestPlayer3

**Test scenarios**:
- Posting messages
- @mentions and autocomplete
- Notifications
- Read/unread state

### Game 200: "The Heist at Goldstone Bank"

**State**: `in_progress`
**Current Phase**: Action Phase
**Purpose**: Testing action submissions

**Participants**:
- GM: TestGM
- Players: TestPlayer1, TestPlayer2

**Test scenarios**:
- Submitting actions
- Editing actions before deadline
- Phase advancement
- GM viewing all actions

### Game 300: "Character Creation Game"

**State**: `character_creation`
**Purpose**: Testing character approval workflow

**Participants**:
- GM: TestGM
- Players: TestPlayer1, TestPlayer2, TestPlayer3

**Test scenarios**:
- Creating characters
- GM approval/rejection
- Character status transitions
- Multiple characters per player

### Game 335: "Complete Lifecycle"

**State**: `setup`
**Purpose**: Testing full game lifecycle transitions

**Test scenarios**:
- State transitions: setup → recruitment → character_creation → in_progress → completed
- Phase creation and advancement
- Game completion and archival

### Game 600: "Character Workflows"

**State**: `in_progress`
**Purpose**: Testing character death and replacement

**Participants**:
- GM: TestGM
- Players: TestPlayer1 (has active + dead characters)

**Test scenarios**:
- Character death
- Creating replacement character
- Approval of replacement
- Multiple character states

---

## Fixture Best Practices

### DO:

✅ **Use predictable IDs** in E2E tests:
```typescript
await page.goto('/games/164');  // Game 164 always exists
```

✅ **Create fresh data** in unit/integration tests:
```go
user := testDB.CreateTestUser(t, "testuser", "test@example.com")
```

✅ **Clean up after tests**:
```go
defer testDB.CleanupTables(t, "users", "games", "game_participants")
```

✅ **Use fixture helper functions**:
```typescript
await loginAsPlayer(page, 'TestPlayer1');  // Uses fixture user
```

### DON'T:

❌ **Hardcode non-fixture IDs**:
```typescript
await page.goto('/games/999');  // ❌ May not exist
```

❌ **Modify shared fixture data** in tests:
```go
// ❌ Don't update fixture users
db.Exec("UPDATE users SET username = 'Modified' WHERE email = 'test_gm@example.com'")
```

❌ **Rely on fixture data in unit tests**:
```go
// ❌ Don't query fixture data in unit tests
user := db.QueryRow("SELECT * FROM users WHERE username = 'TestGM'")
```

❌ **Skip fixture reset** when debugging:
```bash
# ❌ Don't skip fixture reload
# Fixtures automatically reset before E2E tests
```

---

## Debugging Fixture Issues

### Fixtures Not Loading

```bash
# Check if database exists
PGPASSWORD=example psql -h localhost -U postgres -l | grep actionphase

# Reload fixtures manually
just load-e2e

# Check for SQL errors in output
# Look for "ERROR:" or "FATAL:" messages
```

### User Not Found Errors

```bash
# Verify users exist
PGPASSWORD=example psql -h localhost -U postgres -d actionphase \
  -c "SELECT id, username, email FROM users WHERE username LIKE 'Test%';"

# Common issue: Case-sensitive username
# ❌ 'testgm' → ✅ 'TestGM'
```

### Game ID Not Found

```bash
# Check which worker you're using
# Playwright assigns workers automatically

# Worker 0 games: 164, 200, 300, etc.
# Worker 1 games: 10164, 10200, 10300, etc.

# Check if game exists for your worker
PGPASSWORD=example psql -h localhost -U postgres -d actionphase \
  -c "SELECT id, title, state FROM games WHERE id IN (164, 10164, 20164);"
```

### Fixture Data Conflicts

```bash
# Clear all test data and reload
just db-restart  # Restarts database
just migrate     # Apply migrations
just load-e2e    # Reload fixtures
```

---

## Fixture File Structure

```
backend/pkg/db/test_fixtures/
├── apply_common.sh              # Applies common fixtures
├── apply_e2e.sh                 # Applies E2E fixtures (legacy, use worker version)
├── apply_e2e_worker.sh          # Applies worker-specific E2E fixtures
├── common/
│   ├── 01_users.sql            # Base test users
│   ├── 02_system_data.sql      # System configuration
│   └── 03_reference_data.sql   # Reference data
└── e2e/
    ├── 01_games_common_room.sql      # Games 164-168
    ├── 02_games_action_phase.sql     # Games 200-210
    ├── 03_games_characters.sql       # Games 300-310
    ├── 04_games_lifecycle.sql        # Games 335-345
    ├── 05_games_messaging.sql        # Games 400-410
    └── 06_games_workflows.sql        # Games 600-610
```

---

## Performance Considerations

### Parallel Execution

- **6 workers** run E2E tests concurrently
- Each worker has **isolated data** (no conflicts)
- Total fixture load time: ~5-10 seconds
- Tests can run **without waiting** for other workers

### Fixture Size

E2E fixtures are **intentionally minimal**:
- **Predictable IDs** (easy debugging)
- **Minimal content** (fast loading)
- **State-specific scenarios** (targeted testing)

### Cleanup Strategy

- Fixtures **reset before each test run** (global-setup.ts)
- No need to clean up individual test data
- Database state is **consistent** at test start

---

**Back to**: [SKILL.md](../SKILL.md)
