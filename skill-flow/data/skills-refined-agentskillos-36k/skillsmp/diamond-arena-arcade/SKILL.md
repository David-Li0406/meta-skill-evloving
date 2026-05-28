---
name: Diamond Arena & Arcade
description: Build the Diamond Arena competitive system and Arcade games
---

# Diamond Arena & Arcade Skill

## Overview
The Diamond Arena (Orb #3) is the competitive layer where players use Diamonds to compete for prizes.

## Diamond Arena Structure

### Arena Types
| Type | Entry | Prize Pool | Players |
|------|-------|------------|---------|
| Free Roll | 0 💎 | 100 💎 | 50 |
| Bronze | 50 💎 | 2,500 💎 | 50 |
| Silver | 100 💎 | 5,000 💎 | 50 |
| Gold | 250 💎 | 12,500 💎 | 50 |
| Diamond | 500 💎 | 25,000 💎 | 50 |
| Platinum | 1,000 💎 | 50,000 💎 | 50 |

### Arena Flow
```javascript
// 1. Enter arena
async function enterArena(userId, arenaId, entryFee) {
  // Check balance
  const canAfford = await supabase.rpc('spend_diamonds', {
    p_user_id: userId,
    p_amount: entryFee,
    p_purpose: `arena_entry:${arenaId}`
  });
  
  if (!canAfford) throw new Error('Insufficient diamonds');
  
  // Register player
  await supabase.from('arena_participants').insert({
    arena_id: arenaId,
    user_id: userId,
    entered_at: new Date()
  });
}

// 2. Complete challenge
async function completeChallenge(userId, arenaId, score) {
  await supabase.from('arena_participants')
    .update({ score, completed_at: new Date() })
    .eq('user_id', userId)
    .eq('arena_id', arenaId);
}

// 3. Distribute prizes
async function distributeArenaRewards(arenaId) {
  const { data: participants } = await supabase
    .from('arena_participants')
    .select('user_id, score')
    .eq('arena_id', arenaId)
    .order('score', { ascending: false });
  
  const payouts = calculatePayouts(participants);
  
  for (const { userId, amount } of payouts) {
    await supabase.rpc('award_diamonds', {
      p_user_id: userId,
      p_amount: amount,
      p_source: `arena_win:${arenaId}`
    });
  }
}
```

## Diamond Arcade Games

### Available Games
| Game | Type | Diamonds to Play |
|------|------|------------------|
| GTO Speed Quiz | Trivia | 10 💎 |
| Hand Ranking Rush | Memory | 10 💎 |
| Range Builder | Puzzle | 15 💎 |
| Pot Odds Challenge | Math | 10 💎 |
| Position Master | Quiz | 10 💎 |
| All-In EV Calculator | Math | 20 💎 |

### Game Structure
```javascript
const ARCADE_GAME = {
  id: 'gto_speed_quiz',
  name: 'GTO Speed Quiz',
  description: 'Answer GTO questions before time runs out',
  entry_cost: 10,
  max_prize: 100,
  duration_seconds: 60,
  questions_count: 10
};
```

### Arcade Session Flow
```javascript
async function startArcadeGame(userId, gameId) {
  const game = ARCADE_GAMES[gameId];
  
  // Charge entry
  await supabase.rpc('spend_diamonds', {
    p_user_id: userId,
    p_amount: game.entry_cost,
    p_purpose: `arcade:${gameId}`
  });
  
  // Create session
  const { data: session } = await supabase
    .from('arcade_sessions')
    .insert({
      user_id: userId,
      game_id: gameId,
      started_at: new Date(),
      expires_at: new Date(Date.now() + game.duration_seconds * 1000)
    })
    .select()
    .single();
  
  return session;
}

async function completeArcadeGame(sessionId, score) {
  const prize = calculateArcadePrize(score);
  
  await supabase.from('arcade_sessions')
    .update({ score, prize_won: prize, completed_at: new Date() })
    .eq('id', sessionId);
  
  if (prize > 0) {
    await supabase.rpc('award_diamonds', {
      p_user_id: session.user_id,
      p_amount: prize,
      p_source: `arcade_win:${session.game_id}`
    });
  }
}
```

## Trivia System

### Trivia Categories
- Poker History
- Famous Hands
- GTO Theory
- Player Profiles
- Tournament Facts
- Rule Knowledge

### Question Format
```javascript
const TRIVIA_QUESTION = {
  id: 'q123',
  category: 'famous_hands',
  difficulty: 'medium',  // easy, medium, hard
  question: 'In the 2003 WSOP Main Event, what hand did Chris Moneymaker have when he won?',
  options: ['5-4 suited', 'A-K suited', 'Pocket Aces', '7-2 offsuit'],
  correct_answer: 0,
  xp_reward: 10,
  diamond_reward: 5  // Only in Diamond mode
};
```

### Daily Trivia Challenge
```javascript
async function getDailyTrivia(userId) {
  const today = new Date().toISOString().split('T')[0];
  
  // Check if already played
  const { data: existing } = await supabase
    .from('daily_trivia_plays')
    .select('*')
    .eq('user_id', userId)
    .eq('date', today)
    .single();
  
  if (existing) return { alreadyPlayed: true, score: existing.score };
  
  // Get today's questions
  const { data: questions } = await supabase
    .from('trivia_questions')
    .select('*')
    .eq('daily_date', today)
    .order('order');
  
  return { questions, alreadyPlayed: false };
}
```

## Database Tables

### arenas
```sql
CREATE TABLE arenas (
  id UUID PRIMARY KEY,
  name TEXT,
  type TEXT,  -- 'daily', 'weekly', 'special'
  entry_fee INTEGER,
  prize_pool INTEGER,
  max_players INTEGER,
  starts_at TIMESTAMPTZ,
  ends_at TIMESTAMPTZ,
  status TEXT  -- 'upcoming', 'active', 'completed'
);
```

### arcade_sessions
```sql
CREATE TABLE arcade_sessions (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES auth.users(id),
  game_id TEXT,
  score INTEGER,
  prize_won INTEGER DEFAULT 0,
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ
);
```

### trivia_questions
```sql
CREATE TABLE trivia_questions (
  id UUID PRIMARY KEY,
  category TEXT,
  difficulty TEXT,
  question TEXT,
  options JSONB,
  correct_index INTEGER,
  daily_date DATE,
  created_at TIMESTAMPTZ
);
```

## UI Components
- `ArenaLobby.jsx` - List of active/upcoming arenas
- `ArcadeGrid.jsx` - Game selection grid
- `TriviaGame.jsx` - Question/answer interface
- `LeaderboardDisplay.jsx` - Rankings with prizes
