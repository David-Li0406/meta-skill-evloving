# ADR 0022: Evidence-Based Gamification (XP System)

**Date:** 2026-01-20  
**Status:** Accepted  
**Deciders:** Development Team

## Context

The app aims to improve adherence for supplement stacks. Since ADHD users often struggle with long-term habit formation, a gamification layer was needed to provide immediate dopamine rewards for small wins (intake).

## Decision

Implement an **Experience Point (XP) System** directly tied to supplement intake and daily reflections.

Rules:
1. **Intake Reward**: 10 XP per supplement marked "Taken".
2. **Reflection Reward**: 25 XP for completing a nightly reflection.
3. **Streak Multiplier**: (Proposed) Bonus XP for consistency streaks.
4. **Persistence**: XP is stored in the `User` entity and synced to Firestore/LocalStorage.

## Rationale
- **Immediate Feedback**: ADHD minds crave immediate positive feedback. XP gain at the moment of intake provides this "micro-reward".
- **Visual Progress**: Leveling up acts as a long-term indicator of consistency that is more satisfying than just a calendar streak.
- **Social Integration**: XP provides a baseline metric for the "Focus Buddies" feature to compare progress.

## Consequences

**Positive:**
- Significant boost in daily engagement metrics.
- Gamified foundation for future features like badges, trophy room, and level-locked content.
- Low technical overhead (simple numeric increments).

**Negative:**
- Risk of "junk engagement" if users log fake intake to gain XP.
- Need for careful balance to ensure levels don't become unattainable and discouraging.

## Alternatives Considered

| Option | Rejected Because |
|--------|------------------|
| Badge-only System | Milestones are too far apart; lacks the "daily dopamine" hit of XP. |
| Monetary/Real Rewards | Legal and financial complexity; high risk of cheating. |
| Leaderboards (Global) | Can be discouraging for users struggling with severe symptoms; peer-to-peer "Buddies" is safer. |
