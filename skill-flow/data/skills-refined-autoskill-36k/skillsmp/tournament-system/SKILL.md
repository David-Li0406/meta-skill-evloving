---
name: Tournament System
description: Multi-table tournaments, sit-n-gos, and satellite structures
---

# Tournament System Skill

## Overview
Build MTT and SNG tournament infrastructure with blind structures, payouts, and table balancing.

## Tournament Types
| Type | Players | Tables | Duration |
|------|---------|--------|----------|
| Sit & Go | 6-10 | 1 | 30-60 min |
| Turbo SNG | 6-10 | 1 | 15-30 min |
| MTT | 50-10000 | Dynamic | 2-8 hours |
| Satellite | Variable | Variable | 1-3 hours |
| Freeroll | Unlimited | Dynamic | 2-4 hours |

## Database Schema
```sql
CREATE TABLE tournaments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  type TEXT, -- 'MTT', 'SNG', 'SATELLITE'
  buy_in DECIMAL,
  entry_fee DECIMAL,
  starting_stack INTEGER DEFAULT 10000,
  prize_pool DECIMAL,
  guaranteed DECIMAL,
  max_players INTEGER,
  min_players INTEGER DEFAULT 2,
  current_players INTEGER DEFAULT 0,
  status TEXT DEFAULT 'registering', -- 'registering', 'running', 'final_table', 'completed'
  blind_structure_id UUID,
  starts_at TIMESTAMPTZ,
  late_reg_until TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE tournament_registrations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tournament_id UUID REFERENCES tournaments(id),
  user_id UUID REFERENCES auth.users(id),
  registered_at TIMESTAMPTZ DEFAULT NOW(),
  current_stack INTEGER,
  table_id UUID,
  seat_number INTEGER,
  finish_position INTEGER,
  prize_won DECIMAL,
  UNIQUE(tournament_id, user_id)
);

CREATE TABLE blind_structures (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT,
  levels JSONB -- [{level: 1, small: 25, big: 50, ante: 0, duration: 10}, ...]
);

CREATE TABLE tournament_tables (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tournament_id UUID REFERENCES tournaments(id),
  table_number INTEGER,
  status TEXT DEFAULT 'active',
  players JSONB -- Current seating
);
```

## Blind Structure
```javascript
const STANDARD_STRUCTURE = [
  { level: 1, small: 25, big: 50, ante: 0, duration: 10 },
  { level: 2, small: 50, big: 100, ante: 0, duration: 10 },
  { level: 3, small: 75, big: 150, ante: 0, duration: 10 },
  { level: 4, small: 100, big: 200, ante: 25, duration: 10 },
  { level: 5, small: 150, big: 300, ante: 50, duration: 10 },
  // ...
];
```

## Prize Pool Distribution
```javascript
function calculatePayouts(prizePool, playerCount) {
  // Standard structure
  const payoutStructure = {
    10: [0.50, 0.30, 0.20],
    20: [0.40, 0.25, 0.15, 0.10, 0.10],
    50: [0.30, 0.20, 0.12, 0.08, 0.06, 0.05, 0.05, 0.05, 0.05, 0.04]
  };
  
  const structure = payoutStructure[Math.min(playerCount, 50)];
  return structure.map(pct => prizePool * pct);
}
```

## Table Balancing
```javascript
async function balanceTables(tournamentId) {
  const tables = await getTournamentTables(tournamentId);
  
  // Find imbalance
  const playerCounts = tables.map(t => t.players.length);
  const minCount = Math.min(...playerCounts);
  const maxCount = Math.max(...playerCounts);
  
  if (maxCount - minCount > 1) {
    // Move player from largest to smallest table
    const largeTable = tables.find(t => t.players.length === maxCount);
    const smallTable = tables.find(t => t.players.length === minCount);
    
    const movedPlayer = largeTable.players.pop();
    smallTable.players.push(movedPlayer);
    
    // Update database
    await updateTableSeating(largeTable);
    await updateTableSeating(smallTable);
    
    // Notify players
    broadcastTableMove(movedPlayer, smallTable.id);
  }
}
```

## Final Table
```javascript
async function createFinalTable(tournamentId) {
  const remainingPlayers = await getRemainingPlayers(tournamentId);
  
  if (remainingPlayers.length <= 9) {
    // Consolidate to single table
    const finalTable = await supabase.from('tournament_tables').insert({
      tournament_id: tournamentId,
      table_number: 0,
      status: 'final_table',
      players: remainingPlayers
    });
    
    await updateTournamentStatus(tournamentId, 'final_table');
    broadcastFinalTable(tournamentId, remainingPlayers);
  }
}
```

## Components
- `TournamentLobby.jsx` - Browse tournaments
- `TournamentDetail.jsx` - Info + registration
- `BlindClock.jsx` - Timer display
- `PayoutStructure.jsx` - Prize breakdown
- `TournamentTable.jsx` - Active play
- `FinishModal.jsx` - Bust out / cash display
