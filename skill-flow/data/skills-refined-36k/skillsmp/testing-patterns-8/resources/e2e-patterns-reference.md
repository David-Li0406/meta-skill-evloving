# E2E Testing Patterns - Complete Reference

**Read this BEFORE writing any E2E test in ActionPhase**

---

## Core Principles

### 1. E2E Tests Are LAST
```
✅ Unit Tests Pass
   ↓
✅ API Works (curl)
   ↓
✅ Component Tests Pass
   ↓
✅ System Running
   ↓
THEN → Write E2E Test
```

### 2. One Concern Per Test
```typescript
// ❌ WRONG: Testing too much
test('messaging works', async ({ page }) => {
  // Creates conversation + sends message + receives + replies + deletes ❌
});

// ✅ CORRECT: One concern
test('user can delete own message', async ({ page }) => {
  // Only tests deletion ✅
});
```

### 3. Use Helpers and Page Objects
```typescript
// ❌ WRONG: Raw Playwright everywhere
test('...', async ({ page }) => {
  await page.goto('/login');
  await page.fill('input[name="username"]', 'TestPlayer1');
  await page.fill('input[name="password"]', 'testpassword123');
  // ... lots of boilerplate
});

// ✅ CORRECT: Use auth helpers
import { loginAs } from '../fixtures/auth-helpers';

test('...', async ({ page }) => {
  await loginAs(page, 'PLAYER_1'); // Clean and reusable
});
```

---

## Project Structure

```
e2e/
├── fixtures/
│   ├── auth-helpers.ts       # Authentication helpers (loginAs, logout, etc.)
│   ├── game-helpers.ts       # Game fixture helpers (getFixtureGameId, etc.)
│   └── test-users.ts         # Test user constants
├── pages/
│   ├── MessagingPage.ts      # Page Object for messaging
│   └── ... (other page objects)
├── utils/
│   ├── assertions.ts         # assertTextVisible, assertUrl, etc.
│   ├── navigation.ts         # navigateToGame, navigateToGameAndTab
│   └── waits.ts              # waitForVisible, waitForModal
└── [feature]/
    └── feature.spec.ts       # Test specs organized by feature
```

---

## Authentication Patterns

### Using Auth Helpers

```typescript
import { loginAs, logout } from '../fixtures/auth-helpers';

test('feature test', async ({ page }) => {
  // Login as a test user
  await loginAs(page, 'PLAYER_1');  // Uses TestPlayer1

  // Your test logic here

  // Logout if needed
  await logout(page);
});
```

### Available Test Users

```typescript
import { loginAs } from '../fixtures/auth-helpers';

// Available user keys:
'GM'         // TestGM (Game Master)
'PLAYER_1'   // TestPlayer1
'PLAYER_2'   // TestPlayer2
'PLAYER_3'   // TestPlayer3
'PLAYER_4'   // TestPlayer4
'PLAYER_5'   // TestPlayer5
'AUDIENCE'   // TestAudience
```

**All passwords**: `testpassword123`

**Important**: Usernames are case-sensitive PascalCase (`TestGM`, not `testgm`)

### Multi-User Tests

```typescript
test('multi-user scenario', async ({ browser }) => {
  // Create separate contexts for each user
  const player1Context = await browser.newContext();
  const player2Context = await browser.newContext();
  const player1Page = await player1Context.newPage();
  const player2Page = await player2Context.newPage();

  try {
    // Player 1 actions
    await loginAs(player1Page, 'PLAYER_1');
    // ... Player 1 does something ...

    // Player 2 actions
    await loginAs(player2Page, 'PLAYER_2');
    // ... Player 2 sees the change ...

  } finally {
    // ALWAYS clean up contexts
    await player1Context.close();
    await player2Context.close();
  }
});
```

---

## Game Fixtures

### Using Game Helpers

```typescript
import { getFixtureGameId, FIXTURE_GAMES } from '../fixtures/game-helpers';

test('feature test', async ({ page }) => {
  await loginAs(page, 'PLAYER_1');

  // Get game ID by fixture name (safer than hardcoded IDs)
  const gameId = await getFixtureGameId(page, 'E2E_MESSAGES');

  // Navigate to the game
  await navigateToGame(page, gameId);
});
```

### Common Fixture Games

```typescript
// Messaging tests
FIXTURE_GAMES.E2E_MESSAGES        // Private messaging fixture
FIXTURE_GAMES.E2E_PM             // Alias for E2E_MESSAGES

// Common room tests
FIXTURE_GAMES.COMMON_ROOM_POSTS  // Game #164
FIXTURE_GAMES.COMMON_ROOM_MENTIONS
FIXTURE_GAMES.COMMON_ROOM_NOTIFICATIONS

// Character tests
FIXTURE_GAMES.E2E_CHARACTER_CREATION
FIXTURE_GAMES.CHARACTER_AVATARS

// Action/Phase tests
FIXTURE_GAMES.E2E_ACTION
FIXTURE_GAMES.E2E_ACTION_RESULTS
FIXTURE_GAMES.E2E_LIFECYCLE
```

**See**: `e2e/fixtures/game-helpers.ts` for complete list

---

## Page Object Model (POM)

### Using Page Objects

```typescript
import { MessagingPage } from '../pages/MessagingPage';

test('send message', async ({ page }) => {
  await loginAs(page, 'PLAYER_1');
  const gameId = await getFixtureGameId(page, 'E2E_MESSAGES');

  // Create page object
  const messaging = new MessagingPage(page);

  // Use page object methods
  await messaging.goto(gameId);
  await messaging.openConversation('Test Conversation');
  await messaging.sendMessage('Hello!');
  await messaging.verifyMessageExists('Hello!');
});
```

### Creating Page Objects

```typescript
export class FeaturePage {
  constructor(private page: Page) {}

  // Locators (getters for reusability)
  get submitButton(): Locator {
    return this.page.getByRole('button', { name: 'Submit' });
  }

  // Actions (methods that interact with the page)
  async goto(gameId: number) {
    await navigateToGameAndTab(this.page, gameId, 'Feature');
  }

  async submitForm(data: string) {
    await this.page.fill('input[name="field"]', data);
    await this.submitButton.click();
  }

  // Assertions (methods that verify state)
  async verifySuccess(message: string) {
    await expect(this.page.getByText(message)).toBeVisible();
  }
}
```

---

## Navigation Patterns

### Helper Functions

```typescript
import { navigateToGame, navigateToGameAndTab } from '../utils/navigation';

// Navigate to game's default tab
await navigateToGame(page, gameId);

// Navigate to specific tab
await navigateToGameAndTab(page, gameId, 'Messages');
await navigateToGameAndTab(page, gameId, 'Common Room');
await navigateToGameAndTab(page, gameId, 'Actions');
```

---

## Waiting and Assertions

### Smart Waits

```typescript
import { waitForVisible, waitForModal } from '../utils/waits';

// Wait for element to be visible
await waitForVisible(page.getByText('Success'));

// Wait for modal to appear
await waitForModal(page, 'Confirm Delete');
```

### Assertion Helpers

```typescript
import { assertTextVisible, assertUrl, assertElementExists } from '../utils/assertions';

// Assert text is visible
await assertTextVisible(page, 'Welcome!');

// Assert URL matches pattern
await assertUrl(page, '/games/\\d+');

// Assert element exists
await assertElementExists(page, 'button[type="submit"]');
```

### ❌ Anti-Pattern: Arbitrary Timeouts

```typescript
// ❌ WRONG: Flaky
await page.waitForTimeout(3000);  // Will break randomly

// ✅ CORRECT: Wait for specific condition
await page.waitForSelector('[data-testid="message"]');
await page.waitForURL(/\/games\/\d+$/);
await page.waitForLoadState('networkidle');
```

---

## Test Data Patterns

### Using data-testid

```typescript
// In component (MessageThread.tsx):
<div className="message" data-testid="message">
  <span data-testid="message-sender">{sender}</span>
  {/* ... */}
</div>

// In E2E test:
const messages = page.locator('[data-testid="message"]');
const sender = page.locator('[data-testid="message-sender"]');
```

### Dynamic Test Data

```typescript
// Use timestamps to avoid conflicts
const conversationTitle = `Test Conversation ${Date.now()}`;
const messageContent = `Test message at ${Date.now()}`;
```

---

## Real-World Example

### Private Messages Delete Test (Refactored)

```typescript
import { test, expect } from '@playwright/test';
import { loginAs } from '../fixtures/auth-helpers';
import { getFixtureGameId } from '../fixtures/game-helpers';
import { MessagingPage } from '../pages/MessagingPage';

test.describe('Private Message Deletion', () => {
  test('allows user to delete own message', async ({ page }) => {
    // 1. Login
    await loginAs(page, 'PLAYER_1');

    // 2. Get game ID
    const gameId = await getFixtureGameId(page, 'E2E_PM_DELETE');

    // 3. Navigate to messaging
    const messaging = new MessagingPage(page);
    await messaging.goto(gameId);

    // 4. Open test conversation
    await messaging.openConversation('Private Message Delete Test');

    // 5. Verify message exists
    await messaging.verifyMessageExists('Message from Player 1');

    // 6. Delete message
    await messaging.deleteMessage('Message from Player 1');

    // 7. Confirm deletion
    await expect(page.getByText('Delete Message?')).toBeVisible();
    await page.click('button:has-text("Delete")');

    // 8. Verify deleted
    await expect(page.getByText('[Message deleted]')).toBeVisible();
    await expect(page.getByText('Message from Player 1')).not.toBeVisible();
  });

  test('cannot delete other users messages', async ({ page }) => {
    await loginAs(page, 'PLAYER_1');
    const gameId = await getFixtureGameId(page, 'E2E_PM_DELETE');

    const messaging = new MessagingPage(page);
    await messaging.goto(gameId);
    await messaging.openConversation('Private Message Delete Test');

    // Hover over other user's message
    const otherMessage = page.locator('[data-testid="message"]')
      .filter({ hasText: 'Message from Player 2' });
    await otherMessage.hover();

    // Delete button should NOT appear
    await expect(otherMessage.locator('button[title="Delete message"]'))
      .not.toBeVisible();
  });
});
```

---

## Checklist for New E2E Test

Before writing an E2E test, verify:

- [ ] ✅ Backend unit test passes
- [ ] ✅ API endpoint works (curl)
- [ ] ✅ Frontend component test passes
- [ ] ✅ Backend and frontend servers running
- [ ] Created dedicated E2E fixture (if needed)
- [ ] Added fixture to `FIXTURE_GAMES` (if new)
- [ ] Using auth helpers (`loginAs`, not raw login)
- [ ] Using game helpers (`getFixtureGameId`, not hardcoded IDs)
- [ ] Using page objects (if messaging/complex UI)
- [ ] Using assertion helpers (`assertTextVisible`, etc.)
- [ ] Using data-testid for critical elements
- [ ] NO arbitrary `waitForTimeout` calls
- [ ] Test has ONE clear concern
- [ ] Multi-user tests clean up contexts
- [ ] Test uses dynamic data (timestamps) if creating records

---

## Common Pitfalls

### 1. Login Form Timing

```typescript
// ❌ WRONG: Filling before page loads
await page.goto('/login');
await page.fill('input[type="email"]', '...');  // May fail

// ✅ CORRECT: Use auth helper (handles timing)
await loginAs(page, 'PLAYER_1');
```

### 2. Hardcoded Game IDs

```typescript
// ❌ WRONG: Brittle
await page.goto('/games/9999');  // May not exist

// ✅ CORRECT: Use fixture helper
const gameId = await getFixtureGameId(page, 'E2E_MESSAGES');
await navigateToGame(page, gameId);
```

### 3. Not Waiting for Network

```typescript
// ❌ WRONG: Race condition
await page.click('button:has-text("Submit")');
await expect(page.getByText('Success')).toBeVisible();  // May fail

// ✅ CORRECT: Wait for network
await page.click('button:has-text("Submit")');
await page.waitForLoadState('networkidle');
await expect(page.getByText('Success')).toBeVisible();
```

### 4. Fixture Loading in Tests

```typescript
// ❌ WRONG: Loading fixtures in beforeEach
test.beforeEach(async () => {
  await execAsync('DB_NAME=actionphase ./backend/pkg/db/test_fixtures/apply_e2e.sh');
});

// ✅ CORRECT: Fixtures loaded by global setup
// Just use the data, don't reload
test.beforeEach(async ({ page }) => {
  await page.goto('/login');
});
```

---

## References

**Auth Helpers**: `e2e/fixtures/auth-helpers.ts`
**Game Helpers**: `e2e/fixtures/game-helpers.ts`
**Test Users**: `e2e/fixtures/test-users.ts`
**Page Objects**: `e2e/pages/`
**Utils**: `e2e/utils/`

**Examples**:
- `e2e/auth/login.spec.ts` - Authentication patterns
- `e2e/messaging/private-messages-flow.spec.ts` - Messaging patterns
- `e2e/messaging/character-mentions.spec.ts` - Page object usage
