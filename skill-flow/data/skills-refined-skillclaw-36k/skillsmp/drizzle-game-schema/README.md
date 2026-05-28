# Drizzle Game Schema

Expert skill for designing database schemas optimized for games using Drizzle ORM.

## Expertise

This skill provides deep knowledge in:

- **Player Data Models**: Profiles, preferences, authentication
- **Inventory Systems**: Items, stacking, equipment slots
- **Game State Persistence**: Save systems, checkpoints, progress
- **Leaderboards**: Rankings, scores, time-based competitions
- **Achievement Systems**: Unlocks, progress tracking, rewards
- **Economy Tables**: Currency, transactions, balances
- **Session Management**: Play sessions, analytics, retention

## When to Use

Invoke this skill when you need to:

- Design database schemas for a new game feature
- Create migrations for game data
- Optimize queries for leaderboards or inventories
- Implement save/load systems
- Design multiplayer state synchronization
- Structure analytics and telemetry data

## Tech Stack

- **ORM**: Drizzle ORM
- **Database**: SQLite (local) / Turso (production)
- **TypeScript**: Full type safety

## Schema Patterns

### Player Profile

```typescript
export const player = sqliteTable("player", {
  id: text("id").primaryKey(),
  username: text("username").notNull().unique(),
  level: integer("level").notNull().default(1),
  experience: integer("experience").notNull().default(0),
  currency: integer("currency").notNull().default(0),
  createdAt: integer("created_at", { mode: "timestamp_ms" }).notNull(),
  lastLoginAt: integer("last_login_at", { mode: "timestamp_ms" }),
});
```

### Inventory System

```typescript
export const inventoryItem = sqliteTable("inventory_item", {
  id: text("id").primaryKey(),
  playerId: text("player_id").notNull().references(() => player.id),
  itemType: text("item_type").notNull(),
  quantity: integer("quantity").notNull().default(1),
  metadata: text("metadata", { mode: "json" }),
  acquiredAt: integer("acquired_at", { mode: "timestamp_ms" }).notNull(),
});
```

### Leaderboard

```typescript
export const leaderboardEntry = sqliteTable("leaderboard_entry", {
  id: text("id").primaryKey(),
  playerId: text("player_id").notNull().references(() => player.id),
  score: integer("score").notNull(),
  seasonId: text("season_id").notNull(),
  achievedAt: integer("achieved_at", { mode: "timestamp_ms" }).notNull(),
}, (table) => ({
  scoreIdx: index("score_idx").on(table.seasonId, table.score),
}));
```

## Best Practices

### Use Text IDs
```typescript
id: text("id").primaryKey()  // Use nanoid() or uuid
```

### Timestamp Pattern
```typescript
createdAt: integer("created_at", { mode: "timestamp_ms" }).notNull()
```

### JSON for Flexible Data
```typescript
metadata: text("metadata", { mode: "json" })
```

### Index Hot Queries
```typescript
(table) => ({
  playerIdx: index("player_idx").on(table.playerId),
})
```

## Integration

This skill works alongside:

- `zustand-game-patterns` - For client-side state that syncs with DB
- `game-systems-doc` - For documenting data models
- `testing-team` - For database testing strategies

## Usage in Claude Code

```
/drizzle-game-schema

"Design a schema for a farming game with crops and seasons..."
"Create an inventory system with item stacking..."
"How should I structure player achievements?"
```
