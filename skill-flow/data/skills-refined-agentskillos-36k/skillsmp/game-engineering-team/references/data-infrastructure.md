# Data & Infrastructure Reference

## Drizzle Schema Design

```typescript
import { sqliteTable, text, integer, real } from 'drizzle-orm/sqlite-core';

export const users = sqliteTable('users', {
  id: text('id').primaryKey(),
  email: text('email').notNull().unique(),
  createdAt: integer('created_at', { mode: 'timestamp' }).notNull(),
});

export const seasons = sqliteTable('seasons', {
  id: text('id').primaryKey(),
  userId: text('user_id').notNull().references(() => users.id),
  seasonNumber: integer('season_number').notNull(),
  currentDay: integer('current_day').notNull().default(1),
  phase: text('phase', { enum: ['planting', 'growth', 'harvest'] }).notNull(),
  jackpotContribution: real('jackpot_contribution').default(0),
  startedAt: integer('started_at', { mode: 'timestamp' }).notNull(),
});

export const dailyTriggers = sqliteTable('daily_triggers', {
  id: text('id').primaryKey(),
  seasonId: text('season_id').notNull().references(() => seasons.id),
  dayNumber: integer('day_number').notNull(),
  triggerType: text('trigger_type').notNull(),
  earnedAt: integer('earned_at', { mode: 'timestamp' }).notNull(),
});

export const simulins = sqliteTable('simulins', {
  id: text('id').primaryKey(),
  userId: text('user_id').notNull().references(() => users.id),
  name: text('name').notNull(),
  stage: text('stage', { enum: ['sproutling', 'cultivar', 'bloomform', 'legendary'] }).notNull(),
  path: text('path', { enum: ['tender', 'watcher', 'lucky'] }),
  bondLevel: integer('bond_level').notNull().default(1),
  bondXP: integer('bond_xp').notNull().default(0),
});
```

## Telemetry System

```typescript
class Telemetry {
  private queue: GameEvent[] = [];
  
  track(type: string, properties: Record<string, any>): void {
    this.queue.push({
      type,
      timestamp: new Date(),
      sessionId: this.getSessionId(),
      properties,
    });
    
    if (this.queue.length >= 10) this.flush();
  }
  
  private async flush(): Promise<void> {
    const batch = this.queue.splice(0, 10);
    await fetch('/api/telemetry', {
      method: 'POST',
      body: JSON.stringify({ events: batch }),
    });
  }
}

// Standard events
telemetry.track('day_started', { dayNumber: 5 });
telemetry.track('bet_placed', { potId: 'water', betType: 'raise' });
telemetry.track('trigger_earned', { triggerType: 'perfect_read' });
```

## Security Patterns

```typescript
// Input validation
const PlaceBetSchema = z.object({
  potId: z.enum(['water', 'sun', 'pest', 'growth']),
  betType: z.enum(['fold', 'call', 'raise', 'all-in']),
  amount: z.number().int().min(0).max(10000),
});

// Rate limiting
class RateLimiter {
  private requests = new Map<string, number[]>();
  
  isAllowed(key: string, windowMs = 60000, maxRequests = 100): boolean {
    const now = Date.now();
    const timestamps = (this.requests.get(key) || []).filter(t => t > now - windowMs);
    
    if (timestamps.length >= maxRequests) return false;
    
    timestamps.push(now);
    this.requests.set(key, timestamps);
    return true;
  }
}

// Server-authoritative validation
class GameStateValidator {
  validateDayAdvance(current: GameState, proposed: GameState): boolean {
    const expected = this.calculateExpectedState(current);
    return proposed.coins <= expected.maxPossibleCoins;
  }
}
```

## Logging Standards

```typescript
interface LogEntry {
  level: 'debug' | 'info' | 'warn' | 'error';
  message: string;
  timestamp: Date;
  context?: Record<string, any>;
  error?: Error;
}

class Logger {
  info(message: string, context?: Record<string, any>): void {
    this.log({ level: 'info', message, timestamp: new Date(), context });
  }
  
  error(message: string, error: Error, context?: Record<string, any>): void {
    this.log({ level: 'error', message, timestamp: new Date(), context, error });
  }
  
  private log(entry: LogEntry): void {
    // Send to logging service
    console.log(JSON.stringify(entry));
  }
}
```

---

*Data & Infrastructure Reference - Game Engineering Team*
