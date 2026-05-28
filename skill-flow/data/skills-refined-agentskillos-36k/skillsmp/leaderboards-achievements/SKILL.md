---
name: Leaderboards & Achievements
description: Ranking systems, achievements, and competitive tracking
---

# Leaderboards & Achievements Skill

## Database Schema

### Leaderboards
```sql
CREATE TABLE leaderboards (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  type TEXT NOT NULL, -- daily, weekly, monthly, alltime
  game_type TEXT, -- null for global
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE leaderboard_entries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  leaderboard_id UUID REFERENCES leaderboards,
  user_id UUID REFERENCES auth.users,
  score INTEGER NOT NULL,
  rank INTEGER,
  period_start DATE,
  period_end DATE,
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(leaderboard_id, user_id, period_start)
);

CREATE INDEX idx_leaderboard_score ON leaderboard_entries(leaderboard_id, score DESC);
CREATE INDEX idx_leaderboard_user ON leaderboard_entries(user_id);
```

### Achievements
```sql
CREATE TABLE achievements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  description TEXT,
  icon TEXT,
  category TEXT, -- training, social, mastery, special
  rarity TEXT, -- common, rare, epic, legendary
  xp_reward INTEGER DEFAULT 0,
  diamond_reward INTEGER DEFAULT 0,
  requirement_type TEXT, -- games_played, accuracy, streak, etc.
  requirement_value INTEGER,
  hidden BOOLEAN DEFAULT false
);

CREATE TABLE user_achievements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users,
  achievement_id UUID REFERENCES achievements,
  unlocked_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, achievement_id)
);

CREATE INDEX idx_user_achievements ON user_achievements(user_id);
```

## Leaderboard Functions

### Update Score
```sql
CREATE OR REPLACE FUNCTION update_leaderboard_score(
  p_user_id UUID,
  p_leaderboard_name TEXT,
  p_score INTEGER
) RETURNS void AS $$
DECLARE
  v_leaderboard_id UUID;
  v_period_start DATE;
BEGIN
  -- Get leaderboard
  SELECT id INTO v_leaderboard_id 
  FROM leaderboards WHERE name = p_leaderboard_name;
  
  -- Determine period
  v_period_start := DATE_TRUNC('week', NOW())::DATE;
  
  -- Upsert entry
  INSERT INTO leaderboard_entries (leaderboard_id, user_id, score, period_start)
  VALUES (v_leaderboard_id, p_user_id, p_score, v_period_start)
  ON CONFLICT (leaderboard_id, user_id, period_start)
  DO UPDATE SET score = GREATEST(leaderboard_entries.score, p_score);
END;
$$ LANGUAGE plpgsql;
```

### Get Leaderboard
```javascript
async function getLeaderboard(name, limit = 100) {
  const { data } = await supabase
    .from('leaderboard_entries')
    .select(`
      score,
      rank,
      user:user_id (
        id,
        username,
        avatar_url
      )
    `)
    .eq('leaderboard_id', leaderboardId)
    .order('score', { ascending: false })
    .limit(limit);
  
  return data;
}
```

## Achievement System

### Check & Unlock
```javascript
async function checkAchievements(userId, event) {
  // Get all unearned achievements
  const { data: unearned } = await supabase
    .from('achievements')
    .select('*')
    .not('id', 'in', 
      supabase
        .from('user_achievements')
        .select('achievement_id')
        .eq('user_id', userId)
    );
  
  for (const achievement of unearned) {
    const met = await checkRequirement(userId, achievement, event);
    if (met) {
      await unlockAchievement(userId, achievement);
    }
  }
}

async function unlockAchievement(userId, achievement) {
  // Record achievement
  await supabase
    .from('user_achievements')
    .insert({ user_id: userId, achievement_id: achievement.id });
  
  // Award rewards
  if (achievement.xp_reward) {
    await supabase.rpc('add_xp', { user_id: userId, amount: achievement.xp_reward });
  }
  if (achievement.diamond_reward) {
    await supabase.rpc('add_diamonds', { user_id: userId, amount: achievement.diamond_reward });
  }
  
  // Send notification
  await sendAchievementNotification(userId, achievement);
}
```

## React Components

### Leaderboard Display
```jsx
function Leaderboard({ entries, currentUserId }) {
  return (
    <div className="leaderboard">
      {entries.map((entry, index) => (
        <div 
          key={entry.user.id}
          className={`entry ${entry.user.id === currentUserId ? 'current-user' : ''}`}
        >
          <span className="rank">{index + 1}</span>
          <img src={entry.user.avatar_url} className="avatar" />
          <span className="username">{entry.user.username}</span>
          <span className="score">{entry.score.toLocaleString()}</span>
        </div>
      ))}
    </div>
  );
}
```

### Achievement Toast
```jsx
function AchievementUnlocked({ achievement }) {
  return (
    <motion.div 
      className="achievement-toast"
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
    >
      <img src={achievement.icon} />
      <div>
        <h4>Achievement Unlocked!</h4>
        <p>{achievement.name}</p>
      </div>
    </motion.div>
  );
}
```
