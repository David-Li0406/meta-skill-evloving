---
name: spaced-repetition
description: Work with the spaced repetition learning algorithm and review system
allowed-tools: [Read, Edit, Write, Bash]
---

## Purpose
Understand and modify the spaced repetition algorithm, review scheduling, and learning progress tracking.

## Core Algorithm

### Location
- Algorithm: `src/lib/spaced-repetition.ts`
- Review service: `src/lib/services/review-service.ts`

### Current Implementation

**Spaced repetition intervals:**
```typescript
// From src/lib/spaced-repetition.ts
export const SPACED_REPETITION_INTERVALS = {
  NEW: 1,        // New cards: review in 1 day
  LEARNING: 3,   // Learning: review in 3 days
  MASTERED: 7,   // Mastered: review in 7 days
};

export type ReviewQuality = 'correct' | 'incorrect';

export function calculateNextReview(
  quality: ReviewQuality,
  currentInterval: number
): {
  nextInterval: number;
  newLevel: 'new' | 'learning' | 'mastered';
} {
  if (quality === 'incorrect') {
    // Reset to beginning
    return {
      nextInterval: SPACED_REPETITION_INTERVALS.NEW,
      newLevel: 'new',
    };
  }

  // Progress through levels
  if (currentInterval === SPACED_REPETITION_INTERVALS.NEW) {
    return {
      nextInterval: SPACED_REPETITION_INTERVALS.LEARNING,
      newLevel: 'learning',
    };
  }

  if (currentInterval === SPACED_REPETITION_INTERVALS.LEARNING) {
    return {
      nextInterval: SPACED_REPETITION_INTERVALS.MASTERED,
      newLevel: 'mastered',
    };
  }

  // Already mastered
  return {
    nextInterval: SPACED_REPETITION_INTERVALS.MASTERED,
    newLevel: 'mastered',
  };
}
```

### Database Schema

**Review tracking:**
```sql
-- Flashcard review state
CREATE TABLE flashcards (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  question TEXT NOT NULL,
  answer TEXT NOT NULL,
  category_id INTEGER NOT NULL,
  difficulty TEXT CHECK(difficulty IN ('easy', 'medium', 'hard')),
  next_review_date TEXT,  -- ISO date string
  review_interval INTEGER DEFAULT 1,  -- Days until next review
  times_reviewed INTEGER DEFAULT 0,
  times_correct INTEGER DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Review history
CREATE TABLE review_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  flashcard_id INTEGER NOT NULL,
  user_id INTEGER NOT NULL,
  quality TEXT CHECK(quality IN ('correct', 'incorrect')),
  review_mode TEXT CHECK(review_mode IN ('flashcard', 'quiz', 'recall')),
  reviewed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (flashcard_id) REFERENCES flashcards(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Struggling queue
CREATE TABLE struggling_queue (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  flashcard_id INTEGER NOT NULL UNIQUE,
  times_failed INTEGER DEFAULT 1,
  last_failed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (flashcard_id) REFERENCES flashcards(id)
);
```

### Review Logic

**Get due cards:**
```typescript
function getDueFlashcards(userId: number, categoryId?: number) {
  const db = getDb();

  let query = `
    SELECT f.*, c.name as category_name
    FROM flashcards f
    JOIN categories c ON f.category_id = c.id
    WHERE (
      f.next_review_date IS NULL
      OR f.next_review_date <= date('now')
    )
  `;

  if (categoryId) {
    query += ' AND f.category_id = ?';
    return db.prepare(query).all(categoryId);
  }

  return db.prepare(query).all();
}
```

**Submit review:**
```typescript
function submitReview(
  flashcardId: number,
  userId: number,
  quality: 'correct' | 'incorrect',
  reviewMode: 'flashcard' | 'quiz' | 'recall'
) {
  const db = getDb();

  // Get current card state
  const card = db.prepare('SELECT * FROM flashcards WHERE id = ?').get(flashcardId);

  // Calculate next review
  const { nextInterval, newLevel } = calculateNextReview(
    quality,
    card.review_interval
  );

  // Update card
  db.prepare(`
    UPDATE flashcards
    SET
      next_review_date = date('now', '+' || ? || ' days'),
      review_interval = ?,
      times_reviewed = times_reviewed + 1,
      times_correct = times_correct + CASE WHEN ? = 'correct' THEN 1 ELSE 0 END
    WHERE id = ?
  `).run(nextInterval, nextInterval, quality, flashcardId);

  // Record review history
  db.prepare(`
    INSERT INTO review_history (flashcard_id, user_id, quality, review_mode)
    VALUES (?, ?, ?, ?)
  `).run(flashcardId, userId, quality, reviewMode);

  // Handle struggling queue
  if (quality === 'incorrect') {
    // Add to or update struggling queue
    db.prepare(`
      INSERT INTO struggling_queue (flashcard_id, times_failed)
      VALUES (?, 1)
      ON CONFLICT(flashcard_id) DO UPDATE SET
        times_failed = times_failed + 1,
        last_failed_at = CURRENT_TIMESTAMP
    `).run(flashcardId);
  } else {
    // Remove from struggling queue if mastered
    if (newLevel === 'mastered') {
      db.prepare('DELETE FROM struggling_queue WHERE flashcard_id = ?').run(flashcardId);
    }
  }
}
```

## Common Modifications

### 1. Add More Intervals

Extend the algorithm to support more levels:
```typescript
export const INTERVALS = {
  NEW: 1,
  LEARNING_1: 3,
  LEARNING_2: 7,
  REVIEW_1: 14,
  REVIEW_2: 30,
  MASTERED: 90,
};

export function calculateNextReview(
  quality: ReviewQuality,
  currentInterval: number
): { nextInterval: number } {
  if (quality === 'incorrect') {
    return { nextInterval: INTERVALS.NEW };
  }

  // Progress through intervals
  const intervals = Object.values(INTERVALS);
  const currentIndex = intervals.indexOf(currentInterval);

  if (currentIndex < intervals.length - 1) {
    return { nextInterval: intervals[currentIndex + 1] };
  }

  return { nextInterval: INTERVALS.MASTERED };
}
```

### 2. Add Quality Ratings

Use 0-5 scale like Anki:
```typescript
export type ReviewQuality = 0 | 1 | 2 | 3 | 4 | 5;

export function calculateNextReview(quality: ReviewQuality, currentInterval: number) {
  if (quality < 3) {
    // Failed - reset
    return { nextInterval: 1 };
  }

  // Calculate ease factor (simplified)
  const easeFactor = 1.3 + (quality - 3) * 0.15; // 1.3, 1.45, 1.6

  // Increase interval based on quality
  const newInterval = Math.round(currentInterval * easeFactor);

  return { nextInterval: Math.min(newInterval, 365) }; // Cap at 1 year
}
```

### 3. Add Lapse Handling

Track lapses and adjust intervals:
```typescript
interface CardState {
  interval: number;
  lapses: number;
  ease: number;
}

export function calculateNextReview(
  quality: ReviewQuality,
  state: CardState
): CardState {
  if (quality === 'incorrect') {
    return {
      interval: 1,
      lapses: state.lapses + 1,
      ease: Math.max(1.3, state.ease - 0.2), // Reduce ease on lapse
    };
  }

  const newInterval = Math.round(state.interval * state.ease);

  return {
    interval: newInterval,
    lapses: state.lapses,
    ease: state.ease + 0.05, // Increase ease on success
  };
}
```

### 4. Add Difficulty Adjustment

Adjust intervals based on card difficulty:
```typescript
export function calculateNextReview(
  quality: ReviewQuality,
  currentInterval: number,
  difficulty: 'easy' | 'medium' | 'hard'
): { nextInterval: number } {
  const baseInterval = quality === 'correct'
    ? currentInterval * 2
    : 1;

  // Adjust for difficulty
  const multipliers = {
    easy: 1.5,
    medium: 1.0,
    hard: 0.75,
  };

  return {
    nextInterval: Math.round(baseInterval * multipliers[difficulty]),
  };
}
```

## Testing the Algorithm

### Test Script
```typescript
// tools/test-spaced-repetition.ts
import { calculateNextReview } from '@/lib/spaced-repetition';

console.log('=== Spaced Repetition Tests ===\n');

// Test progression on all correct
console.log('All correct answers:');
let interval = 1;
for (let i = 0; i < 5; i++) {
  const result = calculateNextReview('correct', interval);
  console.log(`  Review ${i + 1}: interval ${interval} -> ${result.nextInterval} days`);
  interval = result.nextInterval;
}

// Test failure
console.log('\nFailure on review 3:');
interval = 1;
for (let i = 0; i < 5; i++) {
  const quality = i === 2 ? 'incorrect' : 'correct';
  const result = calculateNextReview(quality, interval);
  console.log(`  Review ${i + 1} (${quality}): interval ${interval} -> ${result.nextInterval} days`);
  interval = result.nextInterval;
}
```

### Simulate Reviews
```typescript
// tools/simulate-reviews.ts
import { getDb } from '@/lib/db';

const db = getDb();

// Get a flashcard
const card = db.prepare('SELECT * FROM flashcards LIMIT 1').get();

console.log('Simulating 10 reviews...\n');

for (let i = 0; i < 10; i++) {
  const quality = Math.random() > 0.2 ? 'correct' : 'incorrect';

  // Submit review
  db.prepare(`
    INSERT INTO review_history (flashcard_id, user_id, quality, review_mode)
    VALUES (?, 1, ?, 'flashcard')
  `).run(card.id, quality);

  // Update card
  const { nextInterval } = calculateNextReview(quality, card.review_interval);

  db.prepare(`
    UPDATE flashcards
    SET review_interval = ?, next_review_date = date('now', '+' || ? || ' days')
    WHERE id = ?
  `).run(nextInterval, nextInterval, card.id);

  console.log(`Review ${i + 1}: ${quality} -> next in ${nextInterval} days`);

  card.review_interval = nextInterval;
}
```

## Analytics

### Review Statistics
```typescript
// Get review stats
const stats = db.prepare(`
  SELECT
    COUNT(*) as total_reviews,
    SUM(CASE WHEN quality = 'correct' THEN 1 ELSE 0 END) as correct,
    SUM(CASE WHEN quality = 'incorrect' THEN 1 ELSE 0 END) as incorrect,
    ROUND(
      100.0 * SUM(CASE WHEN quality = 'correct' THEN 1 ELSE 0 END) / COUNT(*),
      2
    ) as accuracy
  FROM review_history
  WHERE user_id = ?
`).get(userId);
```

### Struggling Cards
```typescript
// Get cards user struggles with
const struggling = db.prepare(`
  SELECT
    f.id,
    f.question,
    sq.times_failed,
    sq.last_failed_at
  FROM struggling_queue sq
  JOIN flashcards f ON sq.flashcard_id = f.id
  WHERE f.category_id IN (
    SELECT id FROM categories WHERE user_id = ?
  )
  ORDER BY sq.times_failed DESC
  LIMIT 10
`).all(userId);
```

## Best Practices
- ✅ Test algorithm changes thoroughly
- ✅ Keep intervals reasonable (1-365 days)
- ✅ Track review history for analytics
- ✅ Handle struggling cards specially
- ✅ Consider difficulty in scheduling
- ✅ Use transactions for review submissions
- ⚠️ Don't make intervals too short or long
- ⚠️ Don't forget to update next_review_date
- ⚠️ Don't skip recording review history
