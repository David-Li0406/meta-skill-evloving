---
name: Poker Room Engine
description: Build the real-time multiplayer poker room system
---

# Poker Room Engine Skill

## Overview
Build real-time multiplayer poker rooms with proper game state management, WebSocket communication, and GTO integration.

## Architecture

### Components
```
┌─────────────────────────────────────────────────────────┐
│                    Poker Room Engine                     │
├─────────────────────────────────────────────────────────┤
│  Frontend (React)                                        │
│  ├── PokerTable.jsx (UI rendering)                      │
│  ├── GameLoop.js (State machine)                        │
│  └── WebSocketManager.js (Real-time sync)               │
├─────────────────────────────────────────────────────────┤
│  Backend (Supabase)                                      │
│  ├── game_tables (Active games)                         │
│  ├── game_sessions (Hand history)                       │
│  ├── player_wallets (Chip balances)                     │
│  └── Realtime subscriptions                             │
├─────────────────────────────────────────────────────────┤
│  AI (Horse Fleet)                                        │
│  ├── horse_personality (Decision traits)                │
│  ├── get_horse_action() (GTO + bias)                    │
│  └── horse_poker_decisions (History)                    │
└─────────────────────────────────────────────────────────┘
```

## Game State Machine

### States
```javascript
const GAME_STATES = {
  WAITING: 'waiting',      // Waiting for players
  DEALING: 'dealing',      // Cards being dealt
  PREFLOP: 'preflop',      // Preflop betting
  FLOP: 'flop',            // Flop betting
  TURN: 'turn',            // Turn betting
  RIVER: 'river',          // River betting
  SHOWDOWN: 'showdown',    // Cards revealed
  PAYOUT: 'payout'         // Chips distributed
};
```

### Transitions
```javascript
function nextState(currentState, action) {
  switch(currentState) {
    case 'DEALING': return 'PREFLOP';
    case 'PREFLOP': return action === 'ALL_IN' ? 'SHOWDOWN' : 'FLOP';
    case 'FLOP': return 'TURN';
    case 'TURN': return 'RIVER';
    case 'RIVER': return 'SHOWDOWN';
    case 'SHOWDOWN': return 'PAYOUT';
    case 'PAYOUT': return 'DEALING';
  }
}
```

## Real-time Sync (Supabase Realtime)

### Subscribe to Table
```javascript
const channel = supabase.channel(`table:${tableId}`)
  .on('broadcast', { event: 'action' }, (payload) => {
    handleAction(payload);
  })
  .on('broadcast', { event: 'state_update' }, (payload) => {
    updateGameState(payload);
  })
  .subscribe();
```

### Broadcast Action
```javascript
await channel.send({
  type: 'broadcast',
  event: 'action',
  payload: {
    playerId,
    action: 'raise',
    amount: 100
  }
});
```

## Database Schema

### game_tables
```sql
CREATE TABLE game_tables (
  id UUID PRIMARY KEY,
  name TEXT,
  game_type TEXT,        -- 'NLH', 'PLO'
  stakes TEXT,           -- '1/2', '2/5'
  max_players INTEGER,
  current_players INTEGER,
  state TEXT,            -- Game state
  pot DECIMAL,
  community_cards TEXT[],
  current_turn UUID,     -- Active player
  dealer_position INTEGER
);
```

### game_sessions
```sql
CREATE TABLE game_sessions (
  id UUID PRIMARY KEY,
  table_id UUID REFERENCES game_tables(id),
  hand_number INTEGER,
  players JSONB,         -- Seat map with stacks
  actions JSONB[],       -- Action history
  board TEXT[],
  winners JSONB,
  created_at TIMESTAMPTZ
);
```

## Action Processing

### Validate Action
```javascript
function validateAction(gameState, playerId, action, amount) {
  if (gameState.currentTurn !== playerId) return false;
  if (action === 'raise' && amount < gameState.minRaise) return false;
  if (action === 'call' && amount !== gameState.amountToCall) return false;
  return true;
}
```

### Process Action
```javascript
async function processAction(tableId, playerId, action, amount) {
  // 1. Validate
  if (!validateAction(gameState, playerId, action, amount)) {
    throw new Error('Invalid action');
  }
  
  // 2. Update pot
  gameState.pot += amount;
  
  // 3. Update player stack
  gameState.players[playerId].stack -= amount;
  
  // 4. Record action
  gameState.actions.push({ playerId, action, amount, timestamp: Date.now() });
  
  // 5. Determine next player or state transition
  advanceGame(gameState);
  
  // 6. Broadcast update
  await broadcastState(tableId, gameState);
}
```

## Horse AI Integration

### Fill Seat with Horse
```javascript
async function seatHorse(tableId, seatNumber) {
  // Get random available horse
  const { data: horse } = await supabase
    .from('content_authors')
    .select('id, name, avatar_url')
    .eq('is_active', true)
    .limit(1)
    .single();
    
  // Seat the horse
  await supabase.from('game_table_seats').insert({
    table_id: tableId,
    seat_number: seatNumber,
    player_type: 'horse',
    horse_id: horse.id,
    stack: 1000  // Buy-in amount
  });
}
```

### Horse Decision
```javascript
async function getHorseDecision(horseId, gameState, heroHand) {
  // Get GTO solution
  const solution = await getGTOSolution(gameState);
  const strategy = solution.strategy_matrix[heroHand];
  
  // Apply horse personality
  const { data: action } = await supabase.rpc('get_horse_action', {
    p_author_id: horseId,
    p_strategy_actions: strategy.actions
  });
  
  return action;
}
```

## Best Practices
1. Use optimistic UI updates with server reconciliation
2. Implement action timeouts (30s default)
3. Log all actions for replay/audit
4. Handle disconnections gracefully (auto-fold after timeout)
5. Use transactions for chip movements
