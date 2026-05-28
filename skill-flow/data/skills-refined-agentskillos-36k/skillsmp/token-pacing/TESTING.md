# Testing & Evaluation

## Testing Summary

| Model | Tested | Result |
|-------|--------|--------|
| Claude Sonnet | Yes | Excellent parsing of natural dates, accurate calculations |
| Claude Haiku | Yes | Works well for simple queries; may need explicit date formats |
| Claude Opus | Yes | Handles complex date expressions and edge cases reliably |

## Evaluation Scenarios

### Scenario 1: The "Spender" (Over Budget)

**Context:** User is at 80% usage with 4 days left.
**Query:** "I'm at 80%, reset is in 4 days. Am I okay?"

**Expected Behavior:**
- [ ] Calculates very low daily allowance (~5% per day)
- [ ] Status reports "Over Budget"
- [ ] Recommendation warns user to limit usage
- [ ] Buffer shows negative value

**Failure Indicators:**
- Status incorrectly shows "On Track"
- Daily target calculation is wrong
- Missing urgency in recommendation

---

### Scenario 2: The "Saver" (Under Budget)

**Context:** User is at 10% usage with 1 day left.
**Query:** "10% used, reset tomorrow morning."

**Expected Behavior:**
- [ ] Calculates high daily allowance (~90% per day)
- [ ] Status reports "Under Budget"
- [ ] Recommendation encourages heavier usage
- [ ] Buffer shows large positive value

**Failure Indicators:**
- Fails to recognize urgency of unused tokens
- Doesn't suggest increasing usage

---

### Scenario 3: The "Balanced" (On Track)

**Context:** User is at 50% usage with 3.5 days remaining (half the week).
**Query:** "I'm at 50% with half the week left."

**Expected Behavior:**
- [ ] Status reports "On Track"
- [ ] Buffer is near zero (within ±3%)
- [ ] Recommendation confirms good pacing

**Failure Indicators:**
- Incorrectly flags as Over/Under Budget
- Buffer calculation is off

---

### Scenario 4: Edge Case — Less Than 1 Day Remaining

**Context:** User is at 85% with 6 hours left.
**Query:** "85% used, reset in 6 hours."

**Expected Behavior:**
- [ ] Switches to hourly targets (not daily)
- [ ] Calculates ~2.5%/hour remaining
- [ ] Provides appropriate urgency

**Failure Indicators:**
- Still shows daily target
- Calculation errors with fractional days

---

## Validation Commands

Test the skill by asking these queries directly:

```
# Under Budget scenario
"I've used 31% and my reset is Wednesday 9am. How am I pacing?"

# Over Budget scenario
"80% used, 2 days until reset. Am I in trouble?"

# On Track scenario
"50% through my tokens, 3.5 days left. Status?"

# Edge case
"I have 15% left and reset is in 4 hours. What should I do?"
```

## Known Edge Cases

| Edge Case | Expected Handling |
|-----------|-------------------|
| Reset time in the past | Ask user to clarify the next reset date |
| Usage > 100% | Report as "Exhausted" with 0% remaining |
| Negative days remaining | Treat as reset already occurred |
| Ambiguous date ("next Wednesday") | Parse as the upcoming occurrence |
