# ADR 005: Ethical Gamification Strategy

## Status
Accepted

## Context
Gamification is a powerful tool for retention, but in the context of ADHD and mental health apps, it carries risks:
1.  **Predatory Mechanisms**: Loot boxes, infinite scrolls, and "shame" mechanics (e.g., losing a streak due to illness) can be harmful.
2.  **Dopamine Burnout**: Over-stimulating users can lead to quick engagement followed by abandonment.
3.  **Rejection Sensitivity**: ADHD users often suffer from Rejection Sensitive Dysphoria (RSD). Punishing them for missing a day can cause them to quit the app entirely to avoid the negative feeling.

## Decision
We will adopt a **"White Hat" / Supportive Gamification** strategy:

1.  **Permanent Progress**:
    - "Experience Points" (XP) or "Brain Health Score" only goes UP, never down.
    - Missing a day pauses progress, it does not reset it (or resets only the 'streak' count, not the cumulative level).

2.  **The "Frozen Streak" Protocol**:
    - Users are given "Grace Days" (Freeze Streaks).
    - If a user misses a log, the app automatically applies a Grace Day if available, framing it as "We've got your back" rather than "You failed."

3.  **Celebration, Not Addiction**:
    - Use `MilestoneSuccessScreen` for meaningful intervals (7, 30, 100 days).
    - Avoid "daily login bonuses" that provide no real value other than clicking a button.
    - Rewards are aesthetic (Icons, Themes) rather than functional advantages.

## Consequences
### Positive
- **Trust**: builds a relationship of support rather than judgment.
- **Retention**: Reduces churn caused by broken streaks/demotivation.
- **Mental Health**: Aligns with the app's therapeutic goals.

### Negative
- **Lower Short-Term Obsession**: Might have slightly lower immediate DAU (Daily Active Users) obsession compared to "predatory" apps, but higher LTV (Lifetime Value).

## Implementation Details
- **Visuals**: `Confetti`, `TrophyRoom`, `ParticlesBackground`.
- **Logic**: `StreakService` calculates streaks locally. `GracePeriod` logic handles missed days.
