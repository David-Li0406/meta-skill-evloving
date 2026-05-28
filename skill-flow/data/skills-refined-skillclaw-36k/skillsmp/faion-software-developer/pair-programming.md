---
id: pair-programming
name: "Pair Programming"
domain: DEV
skill: faion-software-developer
category: "development-practices"
---

# Pair Programming

## Overview

Pair programming is a software development technique where two programmers work together at one workstation. One (the "driver") writes code while the other (the "navigator") reviews each line as it's typed, thinks strategically about direction, and catches errors. The pair switches roles frequently.

## When to Use

- Complex or unfamiliar code areas
- Knowledge transfer (onboarding, cross-training)
- Critical business logic
- Debugging difficult issues
- Learning new technologies
- When code quality is paramount

## When to Skip

- Simple, routine tasks
- Reading documentation/research
- Administrative tasks
- When deep individual focus is needed
- Very tight deadlines (sometimes pairing is faster though)

## Key Roles

### Driver

```markdown
## Responsibilities
- Writes the code
- Focuses on tactical, line-by-line implementation
- Thinks about syntax and immediate logic
- Verbalizes thought process

## Tips
- Think out loud
- Don't get defensive about suggestions
- Switch roles when stuck or tired
- Ask navigator for input
```

### Navigator

```markdown
## Responsibilities
- Reviews code in real-time
- Thinks strategically (architecture, design)
- Spots bugs, typos, edge cases
- Keeps track of next steps
- Suggests improvements

## Tips
- Don't dictate (guide, don't drive)
- Take notes for later
- Think about tests, edge cases
- Consider the bigger picture
```

## Pairing Styles

### Driver-Navigator (Classic)

```markdown
## Flow
1. Driver codes, navigator reviews
2. Switch every 15-30 minutes
3. Navigator spots issues, suggests directions
4. Driver implements

## Best For
- Most situations
- Knowledge transfer
- Complex features
```

### Ping-Pong (with TDD)

```markdown
## Flow
1. Person A writes a failing test
2. Person B makes it pass
3. Person B writes next failing test
4. Person A makes it pass
5. Repeat

## Best For
- TDD practice
- Keeping both engaged
- Learning testing
```

### Strong-Style Pairing

```markdown
## Rule
"For an idea to go from your head to the computer,
it MUST go through someone else's hands."

## Flow
- Navigator dictates
- Driver types
- Driver must understand before typing
- No silent coding

## Best For
- Teaching/mentoring
- Complex explanations
- When one person knows the solution
```

### Tour Guide Pairing

```markdown
## Flow
- Expert "guides" newcomer through codebase
- Newcomer drives
- Expert explains architecture, history, gotchas

## Best For
- Onboarding new team members
- Codebase exploration
- Knowledge documentation
```

## Best Practices

### Environment Setup

```markdown
## Physical (Same Room)
- Large monitor (27"+) or two monitors
- Two keyboards (switch easily)
- Comfortable seating for two
- Whiteboard nearby

## Remote Setup
- Screen sharing tool (VS Code Live Share, Tuple, Pop)
- High-quality audio (headset)
- Camera on (builds rapport)
- Low-latency connection
```

### Time Management

```markdown
## Session Structure
- Start: Agree on goal (10 min max)
- Work: 25-minute focused blocks (Pomodoro)
- Break: 5 minutes every 25 min
- Switch: Change roles at break or when natural
- End: Reflect on what was learned

## Daily Pairing Time
- 4-6 hours max per day
- Leave time for solo tasks
- Don't pair all day every day
```

### Communication

```python
# Good communication examples

# Driver thinking aloud:
"I'm creating a validator class here because
we might need to add more rules later..."

# Navigator suggesting:
"What if we extract that into a helper?
It might make testing easier."

# Switching signal:
"I'm losing focus, want to switch?"

# Disagreement:
"Let's try your approach for 10 minutes,
then we can compare."
```

### Remote Pairing Tools

```markdown
## Code Sharing
| Tool | Best For |
|------|----------|
| VS Code Live Share | Full IDE sharing, free |
| Tuple | Low latency, macOS only, paid |
| Pop | Multi-cursor, free tier |
| CodeTogether | Cross-IDE, enterprise |

## Communication
- Slack/Discord for text
- Zoom/Meet for video
- Miro for whiteboarding

## VS Code Live Share Setup
1. Install Live Share extension
2. Click "Share" in status bar
3. Send link to pair
4. Both can edit simultaneously
```

### Pairing Patterns by Skill Level

```markdown
## Expert + Expert
- High productivity
- Watch for "keyboard hogging"
- Take breaks to avoid fatigue
- Great for complex problems

## Expert + Novice
- Use Tour Guide or Strong-Style
- Expert navigates more often
- Be patient, explain why
- Novice learns fast

## Novice + Novice
- Longer sessions needed
- Focus on learning, not speed
- Celebrate small wins
- Get expert review after
```

## Common Challenges

### "It's Slower"

```markdown
## Reality Check
- Initial slowdown: Yes, 15-20%
- Long-term: Fewer bugs, less rework
- Studies show net positive productivity
- Knowledge shared = no single point of failure

## Mitigation
- Don't pair on trivial tasks
- Measure quality, not just speed
- Track bug rates before/after
```

### Personality Conflicts

```markdown
## Solutions
- Rotate pairs regularly
- Set ground rules upfront
- Use structured techniques (Ping-Pong)
- Take breaks when tension rises
- Retrospect on pairing experience

## Ground Rules Example
1. No judgmental comments
2. Suggest, don't demand
3. Switch roles every 25 min
4. It's OK to disagree
5. Take breaks when needed
```

### Remote Fatigue

```markdown
## Signs
- Zoning out
- One-word responses
- Multitasking
- Camera off

## Solutions
- Shorter sessions (2 hours max)
- Camera on (accountability)
- Take real breaks (away from screen)
- Mix solo and pairing time
```

### Skill Imbalance

```markdown
## When Expert Dominates
- Navigator becomes passive
- Novice doesn't learn

## Fix: Strong-Style
- Novice drives
- Expert must verbalize
- Novice learns by doing

## When Novice Slows Down
- Use guided approach
- Focus on one concept
- Celebrate progress
```

## AI-Assisted Pairing

```markdown
## AI as Navigator
- Use Copilot/Claude while driving
- AI suggests, human decides
- Good for solo developers

## AI Limitations
- No strategic thinking
- Can suggest wrong patterns
- Doesn't understand context fully
- No social benefits of pairing

## Best Hybrid Approach
- Pair with human on design
- Use AI for implementation suggestions
- Human reviews AI code together
```

## Measuring Effectiveness

```markdown
## Metrics to Track
- Bug escape rate (bugs found in production)
- Code review turnaround (should decrease)
- Knowledge distribution (bus factor)
- Team satisfaction surveys
- Onboarding time for new members

## Success Indicators
- Fewer "only X knows this" situations
- Better code quality (measurable)
- Faster onboarding
- Higher team morale
```

## Anti-patterns

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Keyboard hog | One person always drives | Timer-based switching |
| Backseat driver | Navigator dictates every keystroke | Trust driver, suggest strategically |
| Disengaged observer | Navigator zones out | Active techniques (Ping-Pong) |
| Forced pairing | Pairing on everything | Choose tasks wisely |
| No breaks | Mental exhaustion | Pomodoro technique |
| Silent pairing | No communication | Think-aloud protocol |

## References

- [Pair Programming Illuminated - Laurie Williams](https://www.amazon.com/Pair-Programming-Illuminated-Laurie-Williams/dp/0201745763)
- [On Pair Programming - Martin Fowler](https://martinfowler.com/articles/on-pair-programming.html)
- [Strong-Style Pairing - Llewellyn Falco](https://llewellynfalco.blogspot.com/2014/06/llewellyns-strong-style-pairing.html)
- [Tuple - The Pairing Tool](https://tuple.app/)
