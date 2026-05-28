---
name: tv-show-data-validator
description: Validates TV show data against FanHub's domain rules. Use when working with show, character, episode, or quote data to ensure data integrity and business rule compliance.
level: 2
---

# TV Show Data Validator

This skill helps validate TV show data against FanHub's domain rules and business logic. It ensures data integrity across the shows, characters, episodes, and quotes that make up the FanHub application.

## When to Use This Skill

Use this skill when:
- Creating or updating TV show data
- Validating data imports or migrations
- Writing tests that need valid test data
- Reviewing data integrity issues
- Building features that work with the TV show domain model

## FanHub Data Model

### Entity Relationships

```
Shows (1) ─────────────────────────> (N) Seasons
  │                                        │
  │                                        v
  │─────────────────────────────────> (N) Episodes
  │                                        │
  │                                        │
  └─────> (N) Characters <────────────────┘
                │                    (many-to-many)
                │
                v
          (N) Quotes ─────────────> Episodes
```

### Core Entities

#### Shows
- **Required fields**: `title`, `start_year`
- **Optional fields**: `end_year`, `genre`, `description`, `network`, `status`
- **Constraints**:
  - `title` must be unique
  - `start_year` must be between 1950 and current year
  - `end_year` must be >= `start_year` (if provided)
  - `status` must be: 'running', 'ended', 'cancelled', or 'upcoming'

#### Characters
- **Required fields**: `name`, `show_id`
- **Optional fields**: `actor_name`, `status`, `bio`, `is_main_character`
- **Constraints**:
  - `name` + `show_id` must be unique (no duplicate characters per show)
  - `status` must be: 'alive', 'deceased', or 'unknown'
  - `bio` should not exceed 2000 characters
  - `show_id` must reference an existing show

#### Episodes
- **Required fields**: `title`, `show_id`, `season_number`, `episode_number`
- **Optional fields**: `air_date`, `synopsis`, `runtime_minutes`, `director`, `writer`
- **Constraints**:
  - `show_id` + `season_number` + `episode_number` must be unique
  - `season_number` must be >= 1
  - `episode_number` must be >= 1
  - `runtime_minutes` should be between 1 and 300
  - `air_date` should not be in the future (unless show status is 'upcoming')

#### Quotes
- **Required fields**: `quote_text`, `show_id`
- **Optional fields**: `character_id`, `episode_id`, `speaker_context`
- **Constraints**:
  - `character_id` must reference an existing character (if provided)
  - `episode_id` must reference an existing episode (if provided)
  - `quote_text` should not exceed 1000 characters
  - If `character_id` is provided, character must belong to the same show

## Validation Rules

### Cross-Entity Validation

1. **Character-Show Consistency**
   ```
   INVALID: Character references show_id=5, but that show doesn't exist
   VALID: Character's show_id matches an existing show
   ```

2. **Quote-Character Consistency**
   ```
   INVALID: Quote has show_id=1 but character_id references character from show_id=2
   VALID: Quote's character belongs to the same show as the quote
   ```

3. **Episode-Season Consistency**
   ```
   INVALID: Episode references season_number=3 but show only has 2 seasons
   VALID: Episode's season exists for that show
   ```

4. **No Duplicate Characters Per Show**
   ```
   INVALID: Two characters named "Walter White" in Breaking Bad
   VALID: "Walter White" in Breaking Bad and "Walter White" in a different show
   ```

### Data Quality Rules

1. **Related Characters**
   - Related characters should never include duplicates from the same show
   - A character cannot be related to themselves
   - Related character relationships should be bidirectional

2. **Episode Ordering**
   - Episodes within a season should have sequential episode numbers
   - No gaps in episode numbering (1, 2, 3... not 1, 3, 5)
   - Season numbers should be sequential (1, 2, 3... not 1, 3)

3. **Quote Attribution**
   - Quotes with `character_id` should have proper attribution
   - Quotes without `character_id` should have `speaker_context` for context
   - Famous quotes should be verified for accuracy

## Validation Examples

### Valid Data

```json
{
  "show": {
    "title": "Breaking Bad",
    "start_year": 2008,
    "end_year": 2013,
    "status": "ended",
    "genre": "Drama"
  },
  "character": {
    "name": "Walter White",
    "show_id": 1,
    "actor_name": "Bryan Cranston",
    "status": "deceased",
    "is_main_character": true
  },
  "episode": {
    "title": "Pilot",
    "show_id": 1,
    "season_number": 1,
    "episode_number": 1,
    "air_date": "2008-01-20",
    "runtime_minutes": 58
  },
  "quote": {
    "quote_text": "I am the one who knocks!",
    "show_id": 1,
    "character_id": 1,
    "episode_id": 35
  }
}
```

### Invalid Data (with explanations)

```json
{
  "character": {
    "name": "Jesse Pinkman",
    "show_id": 1,
    "status": "retired"  // ❌ Invalid status - must be alive/deceased/unknown
  },
  "episode": {
    "title": "Future Episode",
    "show_id": 1,
    "season_number": 1,
    "episode_number": 1,
    "air_date": "2099-01-01"  // ❌ Future date for ended show
  },
  "quote": {
    "quote_text": "Famous quote",
    "show_id": 1,
    "character_id": 999  // ❌ References non-existent character
  }
}
```

## Common Validation Scenarios

### Scenario 1: Importing Show Data

When importing TV show data from external sources:

1. Validate show exists or create it first
2. Create seasons in order
3. Create episodes with valid season references
4. Create characters with valid show references
5. Create quotes with valid character AND episode references

### Scenario 2: Character Detail Feature

When building character detail pages:

1. Verify character exists and belongs to valid show
2. Related characters should not include duplicates
3. Related characters must belong to the same show
4. All linked quotes must reference valid episodes
5. Episode appearances should be in chronological order

### Scenario 3: Episode Detail Feature

When building episode detail pages:

1. Verify episode exists with valid show/season
2. Character appearances must all belong to the episode's show
3. Quotes must reference this specific episode
4. Previous/next episode links must be valid

## Integration with Other Skills

This skill works alongside:
- **bug-reproduction-test-generator**: Provides schema knowledge for writing valid test data
- **feature-requirements**: Ensures features respect data model constraints
- **effort-estimator**: Understanding data complexity informs effort estimates

## When NOT to Use This Skill

Don't use this skill for:
- General code style or formatting questions
- Non-FanHub domain data validation
- Authentication or authorization logic
- Performance optimization
