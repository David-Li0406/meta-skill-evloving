# Cost Monitoring and Budget Management

Track Claude Code API usage, set budgets, and manage costs across sessions and projects.

## The /cost Command

### Basic Usage

```
> /cost
```

Displays:
- **Input tokens**: Tokens Claude has read this session
- **Output tokens**: Tokens Claude has generated
- **Total tokens**: Combined usage
- **Estimated cost**: Dollar amount for session
- **Context usage**: Percentage of context window used

### Example Output

```
Session Cost:
  Input tokens:  45,234
  Output tokens: 12,891
  Total tokens:  58,125
  Estimated cost: $0.47
  Context usage: 34%
```

### Interpreting Results

| Metric | Good | Warning | Action |
|--------|------|---------|--------|
| Context usage | <50% | 70%+ | /compact at 70% |
| Token ratio | Input > Output | Output >> Input | Responses too verbose |
| Cost trend | Steady | Spiking | Review recent operations |

## When to Check /cost

### Regular Checkpoints

| Trigger | Why Check |
|---------|-----------|
| After reading multiple files | High input cost |
| After verbose operations | Unexpected cost |
| Every 15-20 turns | Stay informed |
| Before major tasks | Budget for work |
| After /compact | Verify reduction |
| Before deciding /compact vs /clear | Inform decision |

### Warning Signs

Check immediately when:
- Responses become noticeably slower
- Claude asks to re-read files it should know
- You've been working for 30+ minutes
- Running verbose commands (npm, test suites)

## Understanding Cost Drivers

### High-Cost Activities

| Activity | Cost Impact | Mitigation |
|----------|-------------|------------|
| Reading large files | $$$ | Read specific sections |
| Directory glob (@src/) | $$$$ | Use grep first |
| Test suite output | $$$ | Request summary |
| npm install output | $$ | Suppress unless errors |
| Long conversations | Cumulative | /compact regularly |
| Opus usage | $$$$$ | Use only when needed |

### Low-Cost Activities

| Activity | Cost Impact | Notes |
|----------|-------------|-------|
| Simple prompts | $ | Few tokens |
| Grep searches | $ | Returns paths only |
| Single file edits | $ | Minimal context |
| Clear commands | $ | Resets context |
| Haiku model | $ | Cheap for exploration |

### Cost Accumulation Pattern

```
Turn 1:   $0.02 (hello, read one file)
Turn 5:   $0.15 (several exchanges)
Turn 10:  $0.35 (more context)
Turn 15:  $0.60 (approaching /compact time)
Turn 20:  $0.95 (should have compacted)
/compact
Turn 21:  $0.45 (context reduced)
Turn 25:  $0.65 (growing again)
```

## Session Tracking

### Tracking Across Sessions

```
> /cost
[Note: Session A - $0.85]

> /resume session-b
> /cost
[Note: Session B - $0.42]
```

### Session Naming for Cost Awareness

```
> /rename feature-auth-v1
```

Named sessions help you:
- Identify expensive sessions
- Compare session costs
- Allocate to projects/features

### Multi-Session Budget

For large features, track across sessions:

| Session | Cost | Phase |
|---------|------|-------|
| auth-planning | $0.25 | Design |
| auth-backend | $0.85 | Implementation |
| auth-frontend | $0.72 | Implementation |
| auth-testing | $0.48 | Testing |
| **Total** | **$2.30** | Feature complete |

## Budget Management Strategies

### Setting Mental Limits

Before starting, decide:
- **Session budget**: "I'll /compact at $0.50"
- **Feature budget**: "This feature should cost <$5"
- **Daily budget**: "Target <$20/day"

### Budget Checkpoints

```
$0.20 - Review: Am I on track?
$0.40 - Consider: /compact soon?
$0.60 - Action: /compact now
$0.80 - Evaluate: /clear and restart?
```

### Cost-Per-Task Estimation

| Task Type | Typical Cost |
|-----------|--------------|
| Quick fix | $0.05-0.15 |
| Small feature | $0.20-0.50 |
| Medium feature | $0.50-1.50 |
| Large feature | $2.00-5.00 |
| Architecture session (Opus) | $3.00-10.00 |

## Cost Reduction Actions

### Immediate Actions

| If Cost Is... | Do This |
|---------------|---------|
| Growing fast | Check what's consuming |
| Unexpectedly high | Review recent operations |
| Approaching limit | /compact immediately |
| Way over budget | /clear and restart efficiently |

### Prevention Actions

| Strategy | Implementation |
|----------|---------------|
| Use Haiku for exploration | Set model in skill/prompt |
| Grep before reading | Search first, then target |
| Batch operations | Combine related tasks |
| Compact proactively | At 70%, not 95% |
| Limit verbosity | Request summaries |

## Project-Level Tracking

### Feature Cost Tracking

Create a simple tracking file:

```markdown
# API Cost Tracking

## 2024-01

### Week 1
- User auth feature: $2.30
- Bug fixes: $0.85
- Code review: $0.45
**Weekly total**: $3.60

### Week 2
- Payment integration: $4.20
- Testing: $1.15
**Weekly total**: $5.35
```

### Per-Story Tracking

If using project management:

```markdown
## STORY-123: Add User Search

| Session | Model | Cost | Notes |
|---------|-------|------|-------|
| search-design | Opus | $1.20 | Architecture |
| search-impl-1 | Sonnet | $0.85 | Backend |
| search-impl-2 | Sonnet | $0.62 | Frontend |
| search-test | Haiku | $0.35 | E2E tests |
| **Total** | | **$3.02** | |
```

## Alerting Yourself

### Context Warnings

Claude shows warnings as context fills:
- Watch for slower responses
- Notice when asked to re-read files
- Check /cost when warning signs appear

### Custom Checkpoints

Build cost checking into workflow:

```
> [Start of session]
> /cost
> [Note baseline]

> [After major work]
> /cost
> [Compare to checkpoint]
```

## Cost Optimization Workflow

### Pre-Session

1. Review task scope
2. Estimate cost budget
3. Plan /compact points
4. Choose appropriate model

### During Session

1. Check /cost every 15-20 turns
2. /compact at 70% context
3. Batch related operations
4. Use efficient prompting

### Post-Session

1. Final /cost check
2. Log cost if tracking
3. Note lessons for future

## Team Cost Management

### Shared Best Practices

- Document model selection guidelines
- Share efficient prompting patterns
- Establish session naming conventions
- Review high-cost sessions together

### Cost Review Questions

When reviewing expensive sessions:
- Was the model appropriate?
- Could we have used grep more?
- Were there unnecessary file reads?
- Did we compact early enough?

## Cost Tracking Checklist

Daily:
- [ ] Check /cost periodically
- [ ] /compact at 70%
- [ ] Note any unexpected costs

Weekly:
- [ ] Review total spend
- [ ] Identify expensive sessions
- [ ] Adjust strategies if needed

Monthly:
- [ ] Analyze cost trends
- [ ] Update team guidelines
- [ ] Set next month budget

## Quick Reference

### Healthy Session Pattern

```
Start:     $0.00, 0% context
Work:      $0.30, 45% context (comfortable)
Compact:   $0.45, 70% context (trigger /compact)
Continue:  $0.25, 25% context (after compact)
Complete:  $0.55, 55% context (within budget)
```

### Cost Red Flags

| Signal | Problem | Action |
|--------|---------|--------|
| $0.50+ in 10 turns | Reading too much | Be selective |
| 80%+ context | Context bloat | /compact now |
| Opus for everything | Over-spending | Use Sonnet |
| Many file reads | Inefficient exploration | Grep first |
| Same files re-read | Lost context | /compact sooner |
