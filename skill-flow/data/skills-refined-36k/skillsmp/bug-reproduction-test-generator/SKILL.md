---
name: bug-reproduction-test-generator
description: Generates failing tests that reproduce reported bugs in FanHub. Use when a bug report comes in and you need to create a test that demonstrates the issue before fixing it. Follows FanHub's testing patterns and data integrity rules.
---

# Bug Reproduction Test Generator

This skill helps you write failing tests that reproduce reported bugs in the FanHub application. Following test-driven debugging principles, creating a failing test first ensures the bug is properly understood and the fix can be verified.

## When to Use This Skill

Use this skill when:
- A bug report comes in from users or QA
- You need to reproduce an issue before fixing it
- You want to prevent regression by capturing the bug in a test
- You're debugging data integrity issues or unexpected behavior

## FanHub Testing Patterns

### Test Structure
All FanHub tests follow this pattern:

```javascript
describe('[Feature] - Bug: [Brief Description]', () => {
  beforeEach(() => {
    // Set up test database state
  });

  it('should [expected behavior] - Bug #[issue-number]', async () => {
    // Arrange: Set up the specific conditions that trigger the bug
    // Act: Perform the action that causes the issue
    // Assert: Verify the bug occurs (test should FAIL initially)
  });
});
```

### Common Bug Categories

#### 1. Data Integrity Issues
**Symptoms**: Duplicate records, orphaned foreign keys, constraint violations

**Test Pattern**:
```javascript
describe('Characters API - Bug: Duplicate character records', () => {
  it('should return only unique characters per show - Bug #142', async () => {
    // Arrange: Seed database with duplicate character
    await db.characters.insert({
      name: 'Jesse Pinkman',
      show_id: 1,
      actor_name: 'Aaron Paul'
    });
    await db.characters.insert({
      name: 'Jesse Pinkman', // Duplicate!
      show_id: 1,
      actor_name: 'Aaron Paul'
    });

    // Act: Query for characters
    const response = await request(app).get('/api/shows/1/characters');
    
    // Assert: Should only return one Jesse Pinkman
    const jessePinkman = response.body.filter(c => c.name === 'Jesse Pinkman');
    expect(jessePinkman).toHaveLength(1); // FAILS - returns 2!
  });
});
```

#### 2. Null Reference Errors
**Symptoms**: "Cannot read property of null", crashes when data is missing

**Test Pattern**:
```javascript
describe('Quotes API - Bug: Crash with deleted character', () => {
  it('should handle quotes for deleted characters gracefully - Bug #156', async () => {
    // Arrange: Create quote, then delete character
    const character = await db.characters.insert({ name: 'Test', show_id: 1 });
    await db.quotes.insert({
      quote_text: 'Test quote',
      character_id: character.id,
      show_id: 1
    });
    await db.characters.delete(character.id);

    // Act: Try to get quote
    const response = await request(app).get(`/api/quotes/${quote.id}`);
    
    // Assert: Should return 200 with null character, not crash
    expect(response.status).toBe(200); // FAILS - returns 500!
  });
});
```

#### 3. Incorrect Query Results
**Symptoms**: API returns wrong data, missing records, or unexpected filtering

**Test Pattern**:
```javascript
describe('Episodes API - Bug: Season filter not working', () => {
  it('should return only episodes from specified season - Bug #178', async () => {
    // Arrange: Create episodes across seasons
    await db.episodes.insert([
      { title: 'S1E1', season_number: 1, episode_number: 1, show_id: 1 },
      { title: 'S2E1', season_number: 2, episode_number: 1, show_id: 1 }
    ]);

    // Act: Request only season 1
    const response = await request(app).get('/api/episodes?season=1');
    
    // Assert: Should only return season 1 episodes
    expect(response.body.every(ep => ep.season_number === 1)).toBe(true);
    // FAILS - returns episodes from all seasons!
  });
});
```

#### 4. Business Logic Errors
**Symptoms**: Data doesn't follow business rules, invalid states allowed

**Test Pattern**:
```javascript
describe('Characters API - Bug: Allows invalid status values', () => {
  it('should reject character with invalid status - Bug #189', async () => {
    // Arrange: Attempt to create character with invalid status
    const invalidCharacter = {
      name: 'New Character',
      show_id: 1,
      status: 'retired' // Invalid! Should be 'alive', 'deceased', or 'unknown'
    };

    // Act: Try to create character
    const response = await request(app)
      .post('/api/characters')
      .send(invalidCharacter);
    
    // Assert: Should return 400 Bad Request
    expect(response.status).toBe(400); // FAILS - returns 201!
    expect(response.body.error).toContain('Invalid status');
  });
});
```

## FanHub Schema Constraints

When writing bug reproduction tests, keep these schema rules in mind:

### Characters
- `name` (required): String
- `show_id` (required): Integer, must reference existing show
- `actor_name` (optional): String
- `status` (optional): Must be 'alive', 'deceased', or 'unknown'
- `bio` (optional): Text
- `is_main_character` (optional): Boolean

### Episodes
- `title` (required): String
- `show_id` (required): Integer, must reference existing show
- `season_id` (required): Integer, must reference existing season
- `episode_number` (required): Integer
- `season_number + episode_number` must be unique per show

### Quotes
- `quote_text` (required): String
- `show_id` (required): Integer, must reference existing show
- `character_id` (optional): Integer, must reference existing character if provided
- `episode_id` (optional): Integer, must reference existing episode if provided

## Effective Bug Reproduction Tips

1. **Isolate the issue**: Create minimal test data that triggers the bug
2. **Document expected vs. actual**: Comment what SHOULD happen vs. what DOES happen
3. **Include bug report context**: Reference the issue number and user report
4. **Test should FAIL initially**: Confirm the bug exists before fixing
5. **Verify the fix**: After fixing, test should PASS

## Example: Complete Bug Reproduction Flow

```javascript
/**
 * Bug Report #142: User reports seeing duplicate "Jesse Pinkman" entries
 * when viewing Breaking Bad characters. Investigation shows database
 * has two records with the same name.
 * 
 * Expected: One Jesse Pinkman record per show
 * Actual: Multiple records with identical names allowed
 */

describe('Characters API - Bug: Duplicate character names in same show', () => {
  let breakingBadId;

  beforeEach(async () => {
    // Set up Breaking Bad show
    const show = await db.shows.insert({
      title: 'Breaking Bad',
      start_year: 2008
    });
    breakingBadId = show.id;
  });

  it('should prevent duplicate character names within same show - Bug #142', async () => {
    // Arrange: Create first Jesse Pinkman
    const first = await request(app)
      .post('/api/characters')
      .send({
        name: 'Jesse Pinkman',
        show_id: breakingBadId,
        actor_name: 'Aaron Paul'
      });
    expect(first.status).toBe(201);

    // Act: Attempt to create duplicate
    const duplicate = await request(app)
      .post('/api/characters')
      .send({
        name: 'Jesse Pinkman', // Same name!
        show_id: breakingBadId,
        actor_name: 'Aaron Paul'
      });
    
    // Assert: Should reject duplicate
    expect(duplicate.status).toBe(400); // FAILS - returns 201!
    expect(duplicate.body.error).toContain('Character already exists');

    // Verify only one Jesse exists
    const characters = await db.characters.findByShow(breakingBadId);
    const jesseRecords = characters.filter(c => c.name === 'Jesse Pinkman');
    expect(jesseRecords).toHaveLength(1); // FAILS - length is 2!
  });
});
```

## When NOT to Use This Skill

Don't use this skill for:
- Writing regular feature tests (use standard test generation patterns)
- Testing happy paths (this is for reproducing FAILURES)
- Performance testing or load testing
- Integration tests that aren't bug-specific

For those scenarios, use the appropriate test generation prompts or patterns instead.
- Creating database seed data
- Writing API endpoint handlers
- Generating test fixtures
- Validating API request/response bodies
- Implementing data import/export functionality
