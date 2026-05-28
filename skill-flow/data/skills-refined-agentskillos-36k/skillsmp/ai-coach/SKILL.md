---
name: ai-coach
description: Manage the AI coaching system for NutriProfile. Use this skill when working with personalized nutrition advice, daily tips, motivational messages, challenges, or the coaching features. Handles user context, streak management, and gamification integration.
allowed-tools: Read,Write,Edit,Grep,Glob,Bash
---

# NutriProfile AI Coach Skill

You are an AI coaching expert for the NutriProfile application. This skill helps you work with the personalized coaching system that provides nutrition advice, motivation, and challenges.

## Context

NutriProfile's AI Coach uses Mistral and Llama models to generate personalized advice based on:
- User's nutritional profile (BMR, TDEE, goals)
- Recent meal history (7 days)
- Activity and weight tracking
- Current streaks and achievements
- Progress toward goals

## Architecture

### Backend Files
- `backend/app/agents/coach.py` - Coaching agent implementation
- `backend/app/api/v1/coaching.py` - Coaching API endpoints
- `backend/app/models/gamification.py` - Achievement, Streak, UserStats models
- `backend/app/services/gamification.py` - Gamification logic

### Frontend Files
- `frontend/src/components/dashboard/CoachingCard.tsx` - Daily coaching widget
- `frontend/src/components/dashboard/AchievementBadge.tsx` - Badge display
- `frontend/src/components/dashboard/StreakCounter.tsx` - Streak visualization

## Data Models

### UserStats Model
```python
class UserStats(Base):
    id: int
    user_id: int
    xp: int  # Experience points
    level: int  # 1-50
    total_meals_logged: int
    total_recipes_generated: int
    total_activities_logged: int
    created_at: datetime
    updated_at: datetime
```

### Achievement Model
```python
class Achievement(Base):
    id: int
    user_id: int
    achievement_type: str  # 20+ badge types
    unlocked_at: datetime
```

### Streak Model
```python
class Streak(Base):
    id: int
    user_id: int
    streak_type: str  # meal_logging, activity, water_intake
    current_count: int
    longest_count: int
    last_activity_date: date
```

## Achievement Types (20+ Badges)

### Meal Logging
- `first_meal` - Log first meal
- `meal_streak_7` - 7-day meal logging streak
- `meal_streak_30` - 30-day meal logging streak
- `variety_champion` - Log 20 different foods

### Activity
- `first_workout` - Log first activity
- `activity_streak_7` - 7-day activity streak
- `calorie_burner` - Burn 10,000 calories total

### Nutrition Goals
- `protein_master` - Hit protein target 7 days
- `balanced_week` - Stay within macros for 7 days
- `hydration_hero` - Meet water goal 14 days

### Recipes
- `chef_beginner` - Generate first recipe
- `chef_expert` - Generate 50 recipes

### Engagement
- `early_adopter` - Join in first month
- `loyal_user` - Active for 90 days

## Coach Agent Flow

```python
async def generate_advice(self, user_id: int) -> CoachingResponse:
    # 1. Load user context
    profile = await self.get_user_profile(user_id)
    meals = await self.get_recent_meals(user_id, days=7)
    stats = await self.get_user_stats(user_id)
    streaks = await self.get_streaks(user_id)

    # 2. Build context prompt
    context = self._build_coaching_context(profile, meals, stats, streaks)

    # 3. Generate advice with Mistral/Llama
    advice = await self.query_model(context)

    # 4. Add personalized tips
    tips = self._generate_tips(profile, meals)

    return CoachingResponse(
        daily_tip=advice.daily_tip,
        suggestions=advice.suggestions,
        motivation_level=self._calculate_motivation(stats),
        challenges=self._generate_challenges(profile),
        confidence=advice.confidence
    )
```

## API Endpoints

### Daily Coaching
```
GET /api/v1/coaching/daily

Response:
{
  "daily_tip": "Vous avez bien progressé cette semaine !",
  "suggestions": [
    "Ajoutez plus de légumes verts",
    "Pensez à vous hydrater"
  ],
  "motivation_level": "high",
  "challenges": [
    {
      "type": "protein",
      "target": 120,
      "current": 85,
      "reward_xp": 50
    }
  ],
  "confidence": 0.82
}
```

### Other Endpoints
- `GET /api/v1/coaching/stats` - User statistics
- `GET /api/v1/coaching/achievements` - Unlocked badges
- `GET /api/v1/coaching/streaks` - Current streaks
- `POST /api/v1/coaching/complete-challenge` - Mark challenge done

## Freemium Limits

| Tier | Coach Messages/Day |
|------|-------------------|
| Free | 1 |
| Premium | 5 |
| Pro | Unlimited |

## XP and Leveling System

### XP Sources
- Log meal: +10 XP
- Hit daily target: +25 XP
- Complete challenge: +50 XP
- Unlock achievement: +100 XP
- 7-day streak: +200 XP

### Level Thresholds
```python
def calculate_level(xp: int) -> int:
    # Levels 1-50, exponential scaling
    # Level 1: 0 XP
    # Level 10: 1,000 XP
    # Level 25: 10,000 XP
    # Level 50: 100,000 XP
    return min(50, int(1 + (xp / 100) ** 0.6))
```

## Frontend Integration

### Coaching Widget
```typescript
const { data: coaching } = useQuery({
  queryKey: ['coaching', 'daily'],
  queryFn: () => coachingApi.getDaily(),
  staleTime: 1000 * 60 * 60  // 1 hour cache
})
```

### i18n Namespace
Use `dashboard` namespace:
- `dashboard.coaching.title` - Widget title
- `dashboard.coaching.tip` - Daily tip label
- `dashboard.coaching.suggestions` - Suggestions section
- `dashboard.coaching.challenge` - Challenge label

## Best Practices

1. **Personalize advice** - Use user's specific data, not generic tips
2. **Stay positive** - Focus on progress, not failures
3. **Be actionable** - Give specific, doable suggestions
4. **Track engagement** - Monitor which tips users act on
5. **Fallback gracefully** - Have pre-defined tips if AI unavailable

## Example Tasks

### Add New Achievement Type
1. Add to `ACHIEVEMENT_TYPES` enum in gamification model
2. Implement unlock logic in gamification service
3. Create badge icon in frontend assets
4. Add translations for badge name/description
5. Test unlock conditions

### Improve Coach Advice Quality
1. Review prompts in `coach.py`
2. Add more context (weight trends, activity patterns)
3. Test with various user profiles
4. Collect user feedback on advice quality

### Add New Challenge Type
1. Define challenge in coaching model
2. Add validation logic
3. Set XP reward amount
4. Update frontend challenge display
5. Add i18n translations
