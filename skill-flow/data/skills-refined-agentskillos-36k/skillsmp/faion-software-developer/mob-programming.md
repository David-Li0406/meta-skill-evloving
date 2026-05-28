---
id: mob-programming
name: "Mob Programming"
domain: DEV
skill: faion-software-developer
category: "development-practices"
---

# Mob Programming

## Overview

Mob programming is a software development approach where the whole team works on the same thing, at the same time, in the same space, and on the same computer. It's "all the brilliant people working on the same thing, at the same time, in the same place, on the same computer."

## When to Use

- Complex features requiring multiple perspectives
- Critical system changes
- Team learning/upskilling
- Onboarding new team members
- Breaking down silos
- When team alignment is crucial
- Solving "impossible" bugs

## When to Skip

- Simple, well-understood tasks
- Parallel independent work needed
- Individual deep work required
- Very large teams (8+)

## Key Roles

### Driver

```markdown
## Responsibilities
- Only person at keyboard
- Types what navigators describe
- Asks clarifying questions
- Does NOT make independent decisions
- Rotates every 5-15 minutes

## Rule
"For an idea to go from your head to the computer,
it must go through someone else's hands."
```

### Navigator(s)

```markdown
## Responsibilities
- Think at higher level than typing
- Direct the driver verbally
- Discuss approach among navigators
- Keep track of the goal
- One navigator speaks at a time

## Types of Navigation
- Directing: Tell driver what to type
- Suggesting: Propose approaches
- Discussing: Debate among navigators
```

### Facilitator (Optional)

```markdown
## Responsibilities
- Manages rotation timer
- Ensures everyone participates
- Keeps mob focused on goal
- Handles interruptions
- Manages breaks

## When Needed
- Large mobs (5+)
- New to mobbing teams
- When conflicts arise
```

## Mob Setup

### Physical Space

```markdown
## Requirements
- Large screen/projector (55"+ or projector)
- Wireless keyboard/mouse
- Seating for all in semicircle
- Whiteboard for diagrams
- Timer visible to all

## Arrangement
        [Screen]
    O O O O O O  ← Navigators
        [Driver]
```

### Remote Mob

```markdown
## Tools
- Video: Zoom, Meet (cameras ON)
- Driving: VS Code Live Share, Tuple
- Timer: Mobti.me, mob.sh
- Whiteboard: Miro, FigJam

## Tips
- Good microphones essential
- One person shares screen
- Use hand-raise for speaking
- More frequent breaks
```

### Timer Setup

```bash
# mob CLI tool (recommended for remote)
# https://mob.sh

# Start as driver (creates WIP branch)
mob start

# Pass to next person (pushes WIP)
mob next

# When done (squashes to clean commit)
mob done

# Rotate every 5-10 minutes
```

## Best Practices

### Rotation Patterns

```markdown
## Fixed Timer
- Rotate every 5-10 minutes
- Timer visible to all
- No exceptions (builds habit)
- Good for beginners

## Natural Transitions
- After completing a small task
- When stuck
- After a test passes (with TDD)
- Good for experienced mobs

## Micro-rotation
- Very short (2-4 minutes)
- Forces concise communication
- Keeps everyone engaged
- Good for learning
```

### Communication Protocols

```markdown
## "Yes, and..." Rule
- Build on others' ideas
- Don't dismiss suggestions
- Try before critiquing

## Intention-Based Navigation
# Bad: "Type 'public class User'"
# Good: "Create a User class that stores name and email"

## Levels of Navigation
1. Intent: "We need to validate the input"
2. Location: "In the validate method"
3. Details: "Check if email contains @"
4. Dictation: "Type 'if not @ in email'" (avoid)
```

### Handling Disagreements

```markdown
## Quick Resolution
1. Time-box discussion (2 min)
2. Try one approach
3. Learn from result
4. Can always refactor

## "Let's try it" Culture
- Experiments over debates
- Code is cheap to change
- Retrospect on decisions

## Parking Lot
- Note off-topic items
- Discuss after mob session
- Don't derail the mob
```

### Daily Mob Schedule

```markdown
## Recommended Structure
09:00-09:15  Daily standup
09:15-10:30  Mob session 1
10:30-10:45  Break
10:45-12:00  Mob session 2
12:00-13:00  Lunch
13:00-14:15  Mob session 3
14:15-14:30  Break
14:30-15:45  Mob session 4 OR solo work
15:45-16:00  Retrospective

## Breaks Are Essential
- Every 75-90 minutes
- Real breaks (away from screen)
- Individual check-ins during breaks
```

## Mob Programming Patterns

### TDD Mob

```markdown
## Flow
1. Navigator describes test intent
2. Driver writes failing test
3. Rotate
4. New navigator describes implementation
5. Driver makes test pass
6. Rotate
7. Refactor together
8. Repeat

## Benefits
- TDD discipline enforced
- Tests are clear (explained to group)
- Design emerges collaboratively
```

### Learning Mob

```markdown
## Purpose
- Team learns new technology
- Expert shares knowledge
- No pressure for output

## Setup
- Expert explains concepts
- Everyone tries hands-on
- Questions encouraged
- Slower rotation (15-20 min)
- Focus on understanding, not speed
```

### Bug Hunt Mob

```markdown
## When
- Critical production bug
- Bug no one can solve alone
- Cross-system issues

## Approach
1. Reproduce bug together
2. Hypothesize causes
3. Test hypotheses systematically
4. Fix collaboratively
5. Add regression test
6. Document root cause
```

### Randori Mob

```markdown
## Structure
- One exercise (kata)
- Each person adds one line/change
- Rotate after each change
- No big jumps

## Rules
- Must make test pass
- If can't, ask for help
- Learn from each other
- Time-boxed (1-2 hours)
```

## Common Challenges

### "It's Inefficient"

```markdown
## Perception
- Multiple people on one task = waste

## Reality
- Less rework (bugs caught early)
- No code review delay
- No knowledge silos
- Faster onboarding
- Higher quality code

## Metrics to Track
- Cycle time (idea to production)
- Bug escape rate
- Team satisfaction
- Knowledge distribution
```

### Introverts/Quiet People

```markdown
## Signs
- Not speaking up
- Looking disengaged
- Only driving, not navigating

## Solutions
- Round-robin navigation
- Written chat alongside verbal
- Smaller mob (3-4 people)
- Regular check-ins during breaks
- Value their input explicitly
```

### Dominant Personalities

```markdown
## Signs
- One person always talking
- Others' ideas dismissed
- Steering all decisions

## Solutions
- Facilitator manages turns
- Round-robin for ideas
- "Yes, and..." rule
- Retrospective feedback
```

### Remote Mob Challenges

```markdown
## Latency
- Use low-latency tools (Tuple)
- Smaller mob for remote (3-4)
- Clear handoff protocols

## Engagement
- Cameras on
- Active facilitation
- Shorter sessions (60-90 min)
- More frequent breaks
```

## Measuring Success

```markdown
## Quantitative Metrics
- Cycle time improvement
- Bug escape rate
- Code review time (should drop)
- Deployment frequency

## Qualitative Metrics
- Team happiness surveys
- Knowledge sharing (can anyone work on any part?)
- Onboarding speed
- Code consistency
```

## Mob vs Pair Programming

| Aspect | Pair | Mob |
|--------|------|-----|
| Size | 2 people | 3-8 people |
| Overhead | Low | Medium |
| Knowledge sharing | Good | Excellent |
| Energy | Sustainable | Can be intense |
| Best for | Daily work | Complex/critical work |
| Requires | Pairing setup | Larger space/screen |

## Starting with Mob Programming

```markdown
## Week 1: Trial
- Try 2-3 mob sessions (2 hours each)
- Focus on learning, not output
- Use facilitation
- Retrospect after each session

## Week 2-4: Practice
- Regular mob time (e.g., mornings)
- Mix with solo/pair work
- Adjust rotation timing
- Refine communication

## Month 2+: Optimization
- Team finds natural rhythm
- Reduce facilitation need
- Apply to appropriate work
- Measure and adjust
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Tourist mob | People not engaged | Active facilitation, round-robin |
| Expert dominance | One person controls | Strong-style navigation |
| No rotation | Driver fatigue | Strict timer |
| Everything is mobbed | Efficiency loss | Choose appropriate tasks |
| No breaks | Burnout | Mandatory breaks every 90 min |
| No retrospective | Problems persist | Regular feedback sessions |

## References

- [Mob Programming - Woody Zuill](https://www.agilealliance.org/resources/experience-reports/mob-programming-agile2014/)
- [Mob Programming Guidebook](https://mobprogrammingguidebook.com/)
- [mob.sh - CLI Tool](https://mob.sh/)
- [Mobti.me - Online Timer](https://mobti.me/)
- [Remote Mob Programming](https://www.remotemobprogramming.org/)
