# Context Pressure Indicators

Recognize when context is becoming a problem and how to monitor usage effectively.

## Visual Indicators

### Token Counter (UI)

The Claude Code UI displays context usage in the header area:

| Display | Meaning | Action |
|---------|---------|--------|
| Green/Low | Under 50% | Continue normally |
| Yellow/Medium | 50-70% | Plan for compaction |
| Orange/High | 70-85% | Compact soon |
| Red/Critical | 85%+ | Compact immediately |

### Progress Bar Interpretation

```
[███████░░░░░░░░░░░░░] 35% - Healthy
[████████████░░░░░░░░] 60% - Watch it
[███████████████░░░░░] 75% - Compact soon
[█████████████████░░░] 85% - Compact now
[███████████████████░] 95% - Emergency compact
```

## Behavioral Indicators

### Response Quality Degradation

| Symptom | What's Happening | Severity |
|---------|------------------|----------|
| Slower responses | Processing large context | Medium |
| Shorter responses | Conserving output space | Medium |
| Incomplete answers | Hitting practical limits | High |
| Repetitive responses | Limited working memory | High |
| Generic answers | Lost specific context | High |

### Memory Loss Signs

**Early Signs:**
- Asks to re-read files recently read
- Forgets variable names discussed earlier
- Misses constraints mentioned earlier
- Needs reminders about decisions made

**Late Signs:**
- Contradicts earlier statements
- Proposes already-rejected approaches
- Confuses different files or functions
- Loses track of the overall goal

### Tool Behavior Changes

| Observation | Indicates |
|-------------|-----------|
| Truncated tool outputs | Context conservation |
| Summarized instead of raw | Automatic compression |
| Fewer suggestions | Reduced processing capacity |
| Simpler code suggestions | Less context for complex solutions |

## Performance Indicators

### Response Time

| Response Time | Context Status |
|---------------|----------------|
| 2-5 seconds | Healthy |
| 5-10 seconds | Elevated usage |
| 10-20 seconds | High pressure |
| 20+ seconds | Critical |

**Note:** Response time also depends on task complexity and model load.

### Turn Quality

Monitor across turns:

| Turn Pattern | Indicates |
|--------------|-----------|
| Consistent quality | Good context management |
| Declining quality | Context pressure building |
| Sudden drop | Possible truncation |
| Recovery after compact | Successful optimization |

## Monitoring Commands

### /cost Command

```
> /cost
```

Output includes:
- **Total input tokens** - Everything sent to Claude
- **Total output tokens** - Claude's responses
- **Current context size** - Active window usage
- **Estimated cost** - Running cost

### Interpreting /cost Output

```
Session cost:
  Input tokens: 45,000
  Output tokens: 12,000
  Current context: 57,000 tokens (28.5% of 200K)
  Estimated cost: $0.45
```

**Key metric:** Current context percentage

### When to Run /cost

| Trigger | Why Check |
|---------|-----------|
| After reading large files | Assess impact |
| Every 10-15 exchanges | Regular monitoring |
| Before complex operations | Verify headroom |
| After seeing slowness | Diagnose cause |
| Before deciding to compact | Confirm need |

## Context Consumption Rates

### By Activity Type

| Activity | Token Consumption | Notes |
|----------|-------------------|-------|
| Reading small file | 500-1,500 | Typical source file |
| Reading large file | 3,000-15,000 | Large or verbose files |
| Your message | 50-200 | Depends on length |
| Claude's response | 200-2,000 | Varies by complexity |
| Bash output | 100-5,000 | Can be very verbose |
| Search results | 500-3,000 | Multiple matches |
| Error messages | 200-1,000 | Stack traces are large |

### Consumption Patterns

**Slow Context Growth:**
- Short messages
- Targeted questions
- Focused file reads
- Summarized outputs

**Fast Context Growth:**
- Large file reads
- Verbose bash commands
- Multiple tool calls
- Long explanations

### Rate Calculation

Rough formula:
```
Tokens per turn = Your message + Claude's response + Tool outputs

At 500 tokens/turn: 200K window = ~400 turns
At 2,000 tokens/turn: 200K window = ~100 turns
At 5,000 tokens/turn: 200K window = ~40 turns
```

## Warning Thresholds

### Custom Monitoring

Track these thresholds:

| Level | Threshold | Action |
|-------|-----------|--------|
| Green | Under 50K tokens (25%) | Continue |
| Yellow | 50-100K tokens (25-50%) | Be mindful |
| Orange | 100-140K tokens (50-70%) | Plan compaction |
| Red | 140-170K tokens (70-85%) | Compact now |
| Critical | 170K+ tokens (85%+) | Immediate action |

### Early Warning System

Create mental checkpoints:

```
At start: "Fresh context, full capacity"
After exploration: "Check usage - did reading inflate context?"
After implementation: "Check usage - time to compact?"
Before new phase: "Assess and compact if needed"
```

## Diagnosing Context Issues

### Decision Tree

```
Problem: Claude seems confused or slow

1. Check /cost
   - Under 50%? Probably not context issue
   - Over 70%? Likely context pressure

2. If over 70%:
   - Still on same task? /compact
   - Changed topics? /clear

3. If under 50% but still issues:
   - Check conversation clarity
   - Restate context explicitly
   - Consider pollution from mixed topics
```

### Root Cause Analysis

| Symptom | Possible Cause | Check |
|---------|----------------|-------|
| Slow responses | High context | /cost |
| Forgetting context | Context truncation | /cost, restate |
| Wrong suggestions | Context pollution | Review history |
| Repetitive answers | Lost conversation flow | /compact or /clear |
| Generic responses | Overwhelmed context | /compact |

## Context Pollution

### What Is Pollution?

Irrelevant information in context that:
- Displaces relevant information
- Confuses the model
- Wastes token budget
- Reduces response quality

### Pollution Sources

| Source | Impact | Prevention |
|--------|--------|------------|
| Off-topic discussions | Confuses focus | Stay on topic |
| Failed experiments | Misleading history | Clear after failures |
| Verbose outputs | Wastes space | Ask for summaries |
| Irrelevant file reads | Displaces useful context | Read selectively |
| Old debugging context | Outdated information | Compact after fixes |

### Detecting Pollution

Signs of polluted context:
- Claude references irrelevant earlier discussion
- Suggestions include discarded approaches
- Confusion about current state
- Mix of old and new information

### Cleaning Polluted Context

**Light pollution:** `/compact` - Summarize away irrelevant details

**Heavy pollution:** `/clear` - Start fresh with clean context

## Monitoring Best Practices

### Regular Check Rhythm

```
Every 5-10 turns: Quick mental assessment
  - Am I getting good responses?
  - Does Claude remember context?

Every 15-20 turns: /cost check
  - Where am I in the budget?
  - Should I compact soon?

After major activity: Explicit check
  - Reading many files
  - Running verbose commands
  - Long implementation sessions
```

### Pre-Emptive Monitoring

Before activities that consume context:
1. Check current usage with /cost
2. Estimate activity consumption
3. Decide: proceed, compact first, or delegate

### Post-Activity Assessment

After heavy context usage:
1. Check /cost again
2. If over 70%, compact now
3. If 50-70%, plan compaction point
4. Note what consumed most context

## Summary: Key Indicators

### Must-Watch Indicators

1. **Token percentage** - Primary metric via /cost
2. **Response speed** - Early warning sign
3. **Claude's memory** - Is context being retained?
4. **Response quality** - Degradation signals pressure

### Action Triggers

| Indicator | Threshold | Action |
|-----------|-----------|--------|
| Token usage | >70% | Compact |
| Token usage | >85% | Immediate compact |
| Response time | >15s sustained | Check /cost |
| Memory loss | Repeated questions | Restate or compact |
| Quality drop | Generic responses | Compact or clear |
