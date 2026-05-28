---
name: Training & Memory Games
description: Build GTO training games and memory-based learning systems
---

# Training & Memory Games Skill

## Overview
The Training Hub (Orb #4) and Memory Matrix (Orb #5) provide structured GTO learning through interactive games.

## Training Hub Structure

### Game Categories
| Category | Description |
|----------|-------------|
| GTO Fundamentals | Core GTO concepts |
| Preflop Mastery | Opening/3-bet ranges |
| Postflop Play | Flop/turn/river decisions |
| MTT Strategy | Tournament-specific |
| Cash Game | Ring game focus |
| PLO Training | Pot-Limit Omaha |

### Training Game Types
1. **Scenario Trainer** - Make decisions on solved spots
2. **Range Quiz** - Identify correct opening ranges
3. **EV Calculator** - Calculate pot odds/equity
4. **Hand Reader** - Narrow opponent ranges
5. **Bet Sizing** - Choose optimal sizing

## Training Game Flow

### 1. Load Scenario
```javascript
async function loadTrainingScenario(gameId, level) {
  const { data: scenario } = await supabase
    .from('solved_spots_gold')
    .select('*')
    .eq('game_type', gameId)
    .eq('difficulty', level)
    .limit(1)
    .single();
  
  return {
    board: scenario.board_cards,
    heroHand: pickRandomHand(),
    strategy: scenario.strategy_matrix,
    metrics: scenario.macro_metrics
  };
}
```

### 2. Present Decision
```jsx
<TrainingDecision
  scenario={scenario}
  options={['Fold', 'Check', 'Call', 'Raise 50%', 'Raise 75%', 'All-In']}
  onDecision={handleDecision}
  timeLimit={30}
/>
```

### 3. Evaluate & Score
```javascript
function evaluateDecision(userAction, correctStrategy) {
  const gtoAction = correctStrategy.best_action;
  const userEV = correctStrategy.actions[userAction]?.ev || 0;
  const evLoss = correctStrategy.max_ev - userEV;
  
  return {
    isCorrect: evLoss < 0.1,  // Within 0.1bb of optimal
    evLoss,
    gtoAction,
    explanation: generateExplanation(correctStrategy)
  };
}
```

### 4. Update Progress
```javascript
async function updateProgress(userId, gameId, result) {
  // Award XP
  const xpAmount = result.isCorrect ? 20 : 5;
  await supabase.rpc('award_xp', {
    p_user_id: userId,
    p_amount: xpAmount,
    p_source: `training:${gameId}`
  });
  
  // Update mastery
  await supabase.from('user_mastery')
    .upsert({
      user_id: userId,
      game_id: gameId,
      correct_count: supabase.sql`correct_count + ${result.isCorrect ? 1 : 0}`,
      total_count: supabase.sql`total_count + 1`,
      last_played: new Date()
    });
}
```

## Memory Matrix Games

### Game Types
| Game | Description | Grid Size |
|------|-------------|-----------|
| Range Recall | Memorize opening range | 13x13 |
| Position Memory | Remember position ranges | 6 positions |
| Bet Size Sequence | Remember sizing patterns | 4-8 items |
| Board Texture | Match boards to ranges | 3x3 |

### Memory Game Flow
```javascript
// 1. Show pattern
async function startMemoryGame(gameId) {
  const { data: chart } = await supabase
    .from('memory_charts_gold')
    .select('chart_grid')
    .eq('id', gameId)
    .single();
  
  return {
    phase: 'study',
    duration: 10000,  // 10 seconds to memorize
    chart: chart.chart_grid
  };
}

// 2. Quiz phase
function generateQuiz(chart, questionCount = 10) {
  const hands = Object.keys(chart);
  const questions = [];
  
  for (let i = 0; i < questionCount; i++) {
    const hand = hands[Math.floor(Math.random() * hands.length)];
    questions.push({
      hand,
      correctAction: chart[hand].action,
      options: ['Fold', 'Call', 'Raise']
    });
  }
  
  return questions;
}

// 3. Score
function scoreMemoryGame(answers, chart) {
  let correct = 0;
  for (const answer of answers) {
    if (chart[answer.hand].action === answer.userAction) {
      correct++;
    }
  }
  return { correct, total: answers.length, percentage: (correct / answers.length) * 100 };
}
```

## Progress & Mastery

### Mastery Levels
```javascript
const MASTERY_LEVELS = {
  0: { name: 'Unstarted', minAccuracy: 0 },
  1: { name: 'Beginner', minAccuracy: 40 },
  2: { name: 'Learning', minAccuracy: 60 },
  3: { name: 'Proficient', minAccuracy: 75 },
  4: { name: 'Advanced', minAccuracy: 85 },
  5: { name: 'Mastered', minAccuracy: 95 }
};
```

### Progress Tracking
```sql
CREATE TABLE user_mastery (
  user_id UUID REFERENCES auth.users(id),
  game_id TEXT,
  level INTEGER DEFAULT 0,
  correct_count INTEGER DEFAULT 0,
  total_count INTEGER DEFAULT 0,
  streak_current INTEGER DEFAULT 0,
  streak_best INTEGER DEFAULT 0,
  last_played TIMESTAMPTZ,
  PRIMARY KEY (user_id, game_id)
);
```

## Daily Challenge

### Structure
- 5 questions from different categories
- Time limit: 2 minutes total
- Rewards: 50 XP + 10 💎 for completion
- Bonus: 2x rewards for perfect score

### Implementation
```javascript
async function getDailyChallenge(userId) {
  const today = new Date().toISOString().split('T')[0];
  
  // Check if completed
  const { data: existing } = await supabase
    .from('daily_challenges')
    .select('*')
    .eq('user_id', userId)
    .eq('date', today)
    .single();
  
  if (existing) return { completed: true, score: existing.score };
  
  // Generate challenge
  const questions = await generateDailyQuestions();
  return { completed: false, questions };
}
```

## UI Components
- `TrainingHub.jsx` - Category selection
- `GameCard.jsx` - Individual game entry
- `ScenarioTrainer.jsx` - Decision interface
- `MemoryGrid.jsx` - 13x13 range grid
- `ProgressRing.jsx` - Mastery visualization
- `DailyChallenge.jsx` - Daily game wrapper
