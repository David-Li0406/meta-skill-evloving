# Playtesting Methods

## Session Types

### 1. First-Time User Experience (FTUE) Test

**Purpose:** Understand how new players learn and perceive the game.

**Setup:**
- Fresh install/cleared data
- No instructions given
- Silent observation (no hints!)

**What to Watch:**
```
□ Where do they click first?
□ What do they try to interact with?
□ Where do they get stuck?
□ What makes them smile/frown?
□ How long until first "aha!" moment?
□ Do they understand the core goal?
```

**Key Questions After:**
- "What do you think this game is about?"
- "What were you trying to do?"
- "What confused you?"
- "What would you try next?"

### 2. Think-Aloud Protocol

**Purpose:** Understand player thought process in real-time.

**Instructions to Player:**
> "Please say everything you're thinking out loud as you play. 
> Tell me what you're looking at, what you're trying to do, 
> and any reactions you have."

**Observer Notes Template:**
```
Timestamp | Action | Verbalization | Emotion | Notes
----------|--------|---------------|---------|------
0:00      | Click  | "What's this?" | Curious | Exploring UI
0:15      | Hover  | "Oh, coins!"   | Happy   | Found resource
0:30      | Stuck  | "Hmm..."       | Confused| Needs hint?
```

### 3. A/B Comparison Test

**Purpose:** Compare two design approaches.

**Structure:**
```
Group A (50%): Version with Feature X
Group B (50%): Version without Feature X

Measure:
- Task completion rate
- Time to complete
- Error rate
- Satisfaction rating
```

**Analysis:**
```javascript
// Statistical significance check
const isSignificant = (groupA, groupB, metric) => {
  // Use t-test or chi-squared depending on metric type
  const pValue = calculatePValue(groupA[metric], groupB[metric]);
  return pValue < 0.05;
};
```

### 4. Heuristic Evaluation

**Purpose:** Expert review against game design principles.

**Nielsen's 10 Usability Heuristics (Game Adapted):**

| # | Heuristic | Game Application | Score (1-5) |
|---|-----------|------------------|-------------|
| 1 | Visibility of system status | Is score/progress always visible? | |
| 2 | Match real world | Do metaphors make sense? | |
| 3 | User control | Can player undo/pause? | |
| 4 | Consistency | Same action = same result? | |
| 5 | Error prevention | Hard to make mistakes? | |
| 6 | Recognition over recall | Is info visible vs memorized? | |
| 7 | Flexibility | Multiple ways to succeed? | |
| 8 | Aesthetic design | Clean, not cluttered? | |
| 9 | Error recovery | Easy to recover from mistakes? | |
| 10 | Help & documentation | Tutorial/hints available? | |

### 5. Longitudinal Play Test

**Purpose:** Test retention and long-term engagement.

**Structure:**
```
Day 1: Initial session (45 min)
Day 2: Return session (30 min)  
Day 7: Weekly check-in (30 min)
Day 30: Monthly review (30 min)

Track:
- Voluntary return rate
- Skill progression
- Feature discovery over time
- Boredom/frustration points
- What keeps them coming back
```

## Feedback Collection

### In-Session Observation Sheet

```markdown
## Playtest Observation - [Date] - [Tester ID]

### Player Info
- Experience level: Casual / Regular / Hardcore
- Similar games played: _______________
- Platform preference: Mobile / Desktop / Both

### Timestamps
- Session start: ___
- First interaction: ___
- First confusion: ___
- First success: ___
- First frustration: ___
- Session end: ___

### Observations

| Time | Event | Emotion | Notes |
|------|-------|---------|-------|
|      |       |         |       |

### Critical Moments
1. ________________________________
2. ________________________________
3. ________________________________

### Quotes (verbatim)
- "_________________________________"
- "_________________________________"
```

### Post-Session Survey

```markdown
## Player Feedback Survey

1. Overall, how fun was this game? (1-10)
   [ ] 1  [ ] 2  [ ] 3  [ ] 4  [ ] 5  [ ] 6  [ ] 7  [ ] 8  [ ] 9  [ ] 10

2. How likely would you play again? (1-10)
   [ ] 1  [ ] 2  [ ] 3  [ ] 4  [ ] 5  [ ] 6  [ ] 7  [ ] 8  [ ] 9  [ ] 10

3. What was the MOST fun part?
   _______________________________________________

4. What was the LEAST fun part?
   _______________________________________________

5. What confused you?
   _______________________________________________

6. What would you change?
   _______________________________________________

7. Describe this game in 3 words:
   __________, __________, __________

8. Who would enjoy this game?
   _______________________________________________
```

### Emotion Mapping

Track emotional journey through gameplay:

```
Excitement
    ^
  5 |        *
  4 |    *       *
  3 | *             *
  2 |                  *
  1 |________________________>
    Start  Mid  Win  Loss  End
    
* = Emotional state at each moment
Target: Peaks at wins, quick recovery from losses
```

## Analyzing Results

### Affinity Mapping

```
1. Collect all feedback points on sticky notes
2. Group similar items together
3. Label each group with theme
4. Prioritize by frequency + severity

Example Groups:
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   CONFUSION     │ │   DELIGHT       │ │   FRUSTRATION   │
├─────────────────┤ ├─────────────────┤ ├─────────────────┤
│ "What's this?"  │ │ "Love the coins"│ │ "Lost unfairly" │
│ "How do I bet?" │ │ "Pretty visuals"│ │ "Too slow"      │
│ "Where am I?"   │ │ "Fun sounds"    │ │ "Confusing menu"│
└─────────────────┘ └─────────────────┘ └─────────────────┘
     7 mentions         5 mentions          4 mentions
     PRIORITY: P1       Keep doing!         PRIORITY: P2
```

### Issue Prioritization Matrix

```
                    FREQUENCY
                 Low         High
              ┌─────────┬─────────┐
        High  │   P2    │   P0    │  ← Fix immediately
   SEVERITY   ├─────────┼─────────┤
        Low   │   P4    │   P1    │  ← Fix soon
              └─────────┴─────────┘
```

### Playtest Report Template

```markdown
# Playtest Report - Build [version] - [Date]

## Executive Summary
- Testers: [N] participants
- Fun rating: [X]/10 average
- Key finding: [One sentence]

## What's Working
1. [Feature] - [Evidence]
2. [Feature] - [Evidence]

## What Needs Work
1. [Issue] - [Frequency] - [Suggested fix]
2. [Issue] - [Frequency] - [Suggested fix]

## Critical Bugs Found
1. [Bug description] - [Steps to reproduce]

## Recommendations
- [ ] Immediate: [Action]
- [ ] Next sprint: [Action]
- [ ] Backlog: [Action]

## Raw Data
[Link to observation notes, recordings, surveys]
```

## Remote Playtesting

### Tools
- **Screen sharing:** Discord, Zoom, Google Meet
- **Recording:** OBS, Loom
- **Surveys:** Google Forms, Typeform
- **Analytics:** Mixpanel, Amplitude, PostHog

### Remote Session Tips
```
DO:
✓ Test tech setup before session
✓ Have backup communication channel
✓ Ask player to share audio (reactions)
✓ Record with permission
✓ Send survey link immediately after

DON'T:
✗ Interrupt during play
✗ Lead the witness ("Did you like X?")
✗ Sessions longer than 60 min
✗ Test too many things at once
```
