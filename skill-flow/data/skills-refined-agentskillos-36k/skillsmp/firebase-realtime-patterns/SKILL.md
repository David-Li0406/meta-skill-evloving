---
name: firebase-realtime-patterns
description: Patterns for real-time multiplayer game state using Firebase Realtime Database or Supabase. Use when implementing room systems, game state sync, or handling concurrent player actions.
---

# Firebase Realtime Patterns for Mahjong

Patterns for implementing real-time multiplayer using Firebase Realtime Database (or Supabase).

## When to Use

- Setting up room creation/joining
- Syncing game state across clients
- Handling concurrent player actions (calls)
- Managing connection states
- Implementing security rules
- Debugging sync issues

## Database Structure

### Room Document

```javascript
// /rooms/{roomCode}
{
  roomCode: "ABC123",
  hostId: "player_uid_1",
  createdAt: timestamp,
  status: "waiting" | "playing" | "ended",

  players: {
    seat0: {
      id: "player_uid_1",
      name: "Player 1",
      connected: true,
      lastSeen: timestamp
    },
    seat1: { ... },
    seat2: { ... },
    seat3: { ... }
  },

  settings: {
    dealerSeat: 0  // Host selected
  },

  game: {
    // Only exists when status === "playing"
    // See Game State below
  }
}
```

### Game State

```javascript
// /rooms/{roomCode}/game
{
  phase: "setup" | "bonus_exposure" | "playing" | "calling" | "ended",

  goldTileType: "dots_5",
  exposedGold: "dots_5_0",  // Tile instance ID

  wall: ["tile_id_1", "tile_id_2", ...],  // Remaining tiles
  discardPile: ["tile_id_x", "tile_id_y", ...],

  currentPlayerSeat: 0,
  dealerSeat: 0,

  lastAction: {
    type: "discard",
    playerSeat: 0,
    tile: "bamboo_3_2",
    timestamp: timestamp
  },

  // Private hands stored separately (see below)

  exposedMelds: {
    seat0: [
      { type: "pung", tiles: ["dots_5_0", "dots_5_1", "dots_5_2"] }
    ],
    seat1: [],
    seat2: [],
    seat3: []
  },

  bonusTiles: {
    seat0: ["wind_east_0", "dragon_red_0"],
    seat1: [],
    seat2: [],
    seat3: []
  },

  // For calling phase
  pendingCalls: {
    seat0: null,  // Already discarded
    seat1: "pung",
    seat2: "pass",
    seat3: null   // Waiting for response
  },

  winner: null,  // Set when game ends
  scores: null   // Set when game ends
}
```

### Private Hands (Separate Path)

```javascript
// /rooms/{roomCode}/privateHands/{seatNumber}
// Only readable by the player in that seat
{
  concealedTiles: ["bamboo_1_0", "bamboo_2_1", "dots_5_3", ...]
}
```

## Room Management

### Create Room

```javascript
import { ref, set, push, serverTimestamp } from 'firebase/database';

async function createRoom(db, hostUser) {
  const roomCode = generateRoomCode();  // 6 char alphanumeric
  const roomRef = ref(db, `rooms/${roomCode}`);

  await set(roomRef, {
    roomCode,
    hostId: hostUser.uid,
    createdAt: serverTimestamp(),
    status: 'waiting',
    players: {
      seat0: {
        id: hostUser.uid,
        name: hostUser.displayName,
        connected: true,
        lastSeen: serverTimestamp()
      },
      seat1: null,
      seat2: null,
      seat3: null
    },
    settings: {
      dealerSeat: 0
    }
  });

  return roomCode;
}

function generateRoomCode() {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';  // Avoid confusing chars
  let code = '';
  for (let i = 0; i < 6; i++) {
    code += chars[Math.floor(Math.random() * chars.length)];
  }
  return code;
}
```

### Join Room

```javascript
import { ref, get, update, serverTimestamp } from 'firebase/database';

async function joinRoom(db, roomCode, user) {
  const roomRef = ref(db, `rooms/${roomCode}`);
  const snapshot = await get(roomRef);

  if (!snapshot.exists()) {
    throw new Error('Room not found');
  }

  const room = snapshot.val();

  if (room.status !== 'waiting') {
    throw new Error('Game already in progress');
  }

  // Find empty seat
  const players = room.players;
  let emptySeat = null;
  for (let i = 0; i < 4; i++) {
    if (!players[`seat${i}`]) {
      emptySeat = i;
      break;
    }
  }

  if (emptySeat === null) {
    throw new Error('Room is full');
  }

  // Join the seat
  await update(ref(db, `rooms/${roomCode}/players/seat${emptySeat}`), {
    id: user.uid,
    name: user.displayName,
    connected: true,
    lastSeen: serverTimestamp()
  });

  return emptySeat;
}
```

### Listen to Room Changes

```javascript
import { ref, onValue, off } from 'firebase/database';

function subscribeToRoom(db, roomCode, callback) {
  const roomRef = ref(db, `rooms/${roomCode}`);

  const unsubscribe = onValue(roomRef, (snapshot) => {
    if (snapshot.exists()) {
      callback(snapshot.val());
    }
  });

  return () => off(roomRef);
}
```

## Game State Management

### Start Game

```javascript
async function startGame(db, roomCode, dealerSeat) {
  // Generate and shuffle tiles
  const tiles = generateTileIds();
  const shuffled = shuffle(tiles);

  // Deal tiles (16 each, 17 to dealer)
  const hands = dealTiles(shuffled, dealerSeat);
  const remainingWall = shuffled.slice(65);  // 128 - 63 dealt

  // Flip gold tile
  const goldTile = remainingWall.shift();
  const goldTileType = getTileType(goldTile);

  // Initialize game state
  const gameState = {
    phase: 'bonus_exposure',
    goldTileType,
    exposedGold: goldTile,
    wall: remainingWall,
    discardPile: [],
    currentPlayerSeat: dealerSeat,
    dealerSeat,
    lastAction: null,
    exposedMelds: { seat0: [], seat1: [], seat2: [], seat3: [] },
    bonusTiles: { seat0: [], seat1: [], seat2: [], seat3: [] },
    bonusExposureComplete: { seat0: false, seat1: false, seat2: false, seat3: false },
    pendingCalls: null,
    winner: null,
    scores: null
  };

  // Use transaction to update atomically
  const updates = {
    [`rooms/${roomCode}/status`]: 'playing',
    [`rooms/${roomCode}/game`]: gameState,
    [`rooms/${roomCode}/privateHands/seat0`]: { concealedTiles: hands[0] },
    [`rooms/${roomCode}/privateHands/seat1`]: { concealedTiles: hands[1] },
    [`rooms/${roomCode}/privateHands/seat2`]: { concealedTiles: hands[2] },
    [`rooms/${roomCode}/privateHands/seat3`]: { concealedTiles: hands[3] }
  };

  await update(ref(db), updates);
}

function generateTileIds() {
  const tiles = [];

  // Suits
  ['dots', 'bamboo', 'characters'].forEach(suit => {
    for (let num = 1; num <= 9; num++) {
      for (let copy = 0; copy < 4; copy++) {
        tiles.push(`${suit}_${num}_${copy}`);
      }
    }
  });

  // Winds (4 copies each)
  ['east', 'south', 'west', 'north'].forEach(dir => {
    for (let copy = 0; copy < 4; copy++) {
      tiles.push(`wind_${dir}_${copy}`);
    }
  });

  // Red Dragons (4 copies)
  for (let copy = 0; copy < 4; copy++) {
    tiles.push(`dragon_red_${copy}`);
  }

  return tiles;  // 128 tiles
}

function getTileType(tileId) {
  // "dots_5_2" -> "dots_5"
  const parts = tileId.split('_');
  if (parts[0] === 'wind') {
    return `wind_${parts[1]}`;
  } else if (parts[0] === 'dragon') {
    return `dragon_${parts[1]}`;
  }
  return `${parts[0]}_${parts[1]}`;
}
```

### Player Actions

#### Discard Tile

```javascript
async function discardTile(db, roomCode, playerSeat, tileId) {
  const updates = {};

  // Get current hand
  const handRef = ref(db, `rooms/${roomCode}/privateHands/seat${playerSeat}`);
  const handSnap = await get(handRef);
  const hand = handSnap.val().concealedTiles;

  // Remove tile from hand
  const newHand = hand.filter(t => t !== tileId);

  // Update state
  updates[`rooms/${roomCode}/privateHands/seat${playerSeat}/concealedTiles`] = newHand;
  updates[`rooms/${roomCode}/game/discardPile`] = arrayUnion(tileId);
  updates[`rooms/${roomCode}/game/lastAction`] = {
    type: 'discard',
    playerSeat,
    tile: tileId,
    timestamp: serverTimestamp()
  };
  updates[`rooms/${roomCode}/game/phase`] = 'calling';
  updates[`rooms/${roomCode}/game/pendingCalls`] = {
    seat0: playerSeat === 0 ? 'discarder' : null,
    seat1: playerSeat === 1 ? 'discarder' : null,
    seat2: playerSeat === 2 ? 'discarder' : null,
    seat3: playerSeat === 3 ? 'discarder' : null
  };

  await update(ref(db), updates);
}
```

#### Submit Call

```javascript
async function submitCall(db, roomCode, playerSeat, callType) {
  // callType: 'win' | 'pung' | 'chow' | 'pass'

  await update(ref(db, `rooms/${roomCode}/game/pendingCalls/seat${playerSeat}`), callType);

  // Check if all players have responded
  const callsSnap = await get(ref(db, `rooms/${roomCode}/game/pendingCalls`));
  const calls = callsSnap.val();

  const allResponded = Object.values(calls).every(c => c !== null);

  if (allResponded) {
    await resolveCallS(db, roomCode, calls);
  }
}

async function resolveCalls(db, roomCode, calls) {
  const gameSnap = await get(ref(db, `rooms/${roomCode}/game`));
  const game = gameSnap.val();

  // Find discarder
  const discarderSeat = Object.entries(calls).find(([_, v]) => v === 'discarder')[0].replace('seat', '');

  // Priority: win > pung > chow
  const priority = { win: 3, pung: 2, chow: 1, pass: 0, discarder: -1 };

  let winner = null;
  let highestPriority = -1;

  for (const [seat, call] of Object.entries(calls)) {
    const seatNum = parseInt(seat.replace('seat', ''));
    const callPriority = priority[call] || 0;

    if (callPriority > highestPriority) {
      highestPriority = callPriority;
      winner = { seat: seatNum, call };
    } else if (callPriority === highestPriority && callPriority > 0) {
      // Tie-breaker: closest to discarder (counter-clockwise)
      const currentDistance = (seatNum - discarderSeat + 4) % 4;
      const winnerDistance = (winner.seat - discarderSeat + 4) % 4;
      if (currentDistance < winnerDistance) {
        winner = { seat: seatNum, call };
      }
    }
  }

  if (winner && winner.call !== 'pass') {
    await executeCall(db, roomCode, winner, game);
  } else {
    // Everyone passed, next player's turn
    const nextSeat = (parseInt(discarderSeat) + 3) % 4;  // Counter-clockwise
    await update(ref(db, `rooms/${roomCode}/game`), {
      phase: 'playing',
      currentPlayerSeat: nextSeat,
      pendingCalls: null
    });
  }
}
```

## Security Rules

```javascript
// Firebase Realtime Database Rules
{
  "rules": {
    "rooms": {
      "$roomCode": {
        // Anyone can read room metadata
        ".read": true,

        // Only host can write room settings
        "settings": {
          ".write": "data.parent().child('hostId').val() === auth.uid"
        },

        // Players can join empty seats
        "players": {
          "$seat": {
            ".write": "(!data.exists() && newData.child('id').val() === auth.uid) || data.child('id').val() === auth.uid"
          }
        },

        // Private hands only readable by owner
        "privateHands": {
          "$seat": {
            ".read": "root.child('rooms').child($roomCode).child('players').child($seat).child('id').val() === auth.uid",
            ".write": "root.child('rooms').child($roomCode).child('players').child($seat).child('id').val() === auth.uid || root.child('rooms').child($roomCode).child('hostId').val() === auth.uid"
          }
        },

        // Game state - validated writes
        "game": {
          ".read": true,
          ".write": "auth !== null && root.child('rooms').child($roomCode).child('players').hasChild('seat0') && root.child('rooms').child($roomCode).child('players').hasChild('seat1') && root.child('rooms').child($roomCode).child('players').hasChild('seat2') && root.child('rooms').child($roomCode).child('players').hasChild('seat3')"
        }
      }
    }
  }
}
```

## Connection Handling

### Presence System

```javascript
import { ref, onDisconnect, set, serverTimestamp, onValue } from 'firebase/database';

function setupPresence(db, roomCode, seatNumber, userId) {
  const presenceRef = ref(db, `rooms/${roomCode}/players/seat${seatNumber}/connected`);
  const lastSeenRef = ref(db, `rooms/${roomCode}/players/seat${seatNumber}/lastSeen`);

  // Set connected to true
  set(presenceRef, true);

  // On disconnect, set to false
  onDisconnect(presenceRef).set(false);
  onDisconnect(lastSeenRef).set(serverTimestamp());

  // Listen for connection state
  const connectedRef = ref(db, '.info/connected');
  onValue(connectedRef, (snap) => {
    if (snap.val() === true) {
      set(presenceRef, true);
      set(lastSeenRef, serverTimestamp());
    }
  });
}
```

### Reconnection

```javascript
async function rejoinRoom(db, roomCode, userId) {
  const roomSnap = await get(ref(db, `rooms/${roomCode}`));

  if (!roomSnap.exists()) {
    throw new Error('Room no longer exists');
  }

  const room = roomSnap.val();

  // Find player's seat
  let playerSeat = null;
  for (let i = 0; i < 4; i++) {
    if (room.players[`seat${i}`]?.id === userId) {
      playerSeat = i;
      break;
    }
  }

  if (playerSeat === null) {
    throw new Error('You are not in this room');
  }

  // Update connection status
  await update(ref(db, `rooms/${roomCode}/players/seat${playerSeat}`), {
    connected: true,
    lastSeen: serverTimestamp()
  });

  return {
    seat: playerSeat,
    room,
    game: room.game
  };
}
```

## Debugging Patterns

### Log State Changes

```javascript
function debugSubscribe(db, roomCode) {
  onValue(ref(db, `rooms/${roomCode}/game`), (snap) => {
    console.log('[GAME STATE]', JSON.stringify(snap.val(), null, 2));
  });

  onValue(ref(db, `rooms/${roomCode}/game/phase`), (snap) => {
    console.log('[PHASE CHANGE]', snap.val());
  });

  onValue(ref(db, `rooms/${roomCode}/game/pendingCalls`), (snap) => {
    console.log('[PENDING CALLS]', snap.val());
  });
}
```

### Validate State Consistency

```javascript
function validateGameState(game, privateHands) {
  const errors = [];

  // Check tile counts
  let totalTiles = 0;
  totalTiles += game.wall.length;
  totalTiles += game.discardPile.length;
  totalTiles += 1;  // Exposed gold

  for (let i = 0; i < 4; i++) {
    totalTiles += privateHands[`seat${i}`].concealedTiles.length;
    totalTiles += game.exposedMelds[`seat${i}`].reduce((sum, m) => sum + m.tiles.length, 0);
    totalTiles += game.bonusTiles[`seat${i}`].length;
  }

  if (totalTiles !== 128) {
    errors.push(`Tile count mismatch: ${totalTiles} (expected 128)`);
  }

  // Check for duplicate tiles
  const allTiles = [
    ...game.wall,
    ...game.discardPile,
    game.exposedGold,
    ...Object.values(privateHands).flatMap(h => h.concealedTiles),
    ...Object.values(game.exposedMelds).flatMap(melds => melds.flatMap(m => m.tiles)),
    ...Object.values(game.bonusTiles).flat()
  ];

  const seen = new Set();
  for (const tile of allTiles) {
    if (seen.has(tile)) {
      errors.push(`Duplicate tile: ${tile}`);
    }
    seen.add(tile);
  }

  return errors;
}
```

## Supabase Alternative

If using Supabase instead of Firebase:

```javascript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

// Subscribe to room changes
const subscription = supabase
  .channel(`room:${roomCode}`)
  .on('postgres_changes',
    { event: '*', schema: 'public', table: 'rooms', filter: `code=eq.${roomCode}` },
    (payload) => {
      console.log('Room changed:', payload);
    }
  )
  .subscribe();

// Real-time game state with Supabase Realtime
const gameSubscription = supabase
  .channel(`game:${roomCode}`)
  .on('broadcast', { event: 'game_update' }, (payload) => {
    updateGameState(payload.game);
  })
  .subscribe();

// Broadcast game update
await supabase.channel(`game:${roomCode}`).send({
  type: 'broadcast',
  event: 'game_update',
  payload: { game: newGameState }
});
```

## Usage

When implementing multiplayer features, reference this skill for:
1. Database structure patterns
2. Room management code
3. State sync logic
4. Security rules
5. Connection handling
