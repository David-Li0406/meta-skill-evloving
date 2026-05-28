---
name: balls-mode
description: Decomposed reasoning with explicit confidence scoring. Use for complex decisions, debugging failures, and architectural choices where tracking uncertainty prevents wasted effort.
trigger: /balls
---

# Balls Mode - Decomposed Reasoning with Confidence Scoring

> Credit: Based on the original concept by [@typememetics](https://x.com/typememetics/status/2012821469009465487) and [gbasin/balls-mode](https://github.com/gbasin/balls-mode)

## When to Use

**INVOKE THIS SKILL WHEN:**
- Making architectural decisions BEFORE starting implementation
- Debugging complex issues after first attempt failed
- Task has multiple independent sub-questions
- Need to identify weakest assumption before investing time
- Security analysis requiring attack vector enumeration
- Format/protocol compliance verification (compress/decompress, encode/decode)

**DO NOT USE WHEN:**
- Simple factual tasks ("install X", "create file Y")
- Impossible tasks (use P5/P19 instead)
- **DURING optimization/iteration loops** - just iterate, don't analyze
- Pre-computed solutions exist (search first)
- Time-critical tasks (adds ~500 tokens overhead)
- Near-miss tasks (8/9 passing) - problem is specific

**CRITICAL: Use balls-mode for PRE-ANALYSIS only, not during iteration!**
- GOOD: Use balls-mode to identify what to test BEFORE implementing
- BAD: Use balls-mode to analyze each iteration attempt

---

## Protocol

### Step 1: CLASSIFY

Determine if decomposition is needed:
- **Trivial**: Direct factual, simple calculation, single-step → Answer directly
- **Complex**: Multi-faceted, architectural, debugging, analysis → Proceed to decomposition

### Step 2: DECOMPOSE

Break into independent, verifiable reasoning units ("balls"):

```
## Decomposition

| # | Ball | Why it matters |
|---|------|----------------|
| 1 | [specific sub-question] | [relevance to main question] |
| 2 | [specific sub-question] | [relevance to main question] |
...
```

Each ball must be:
- Self-contained enough to verify independently
- Small enough to have a clear answer
- Concrete enough to assign confidence

### Step 3: SOLVE & VERIFY

For each ball:
1. Solve independently (don't let other balls influence)
2. Check for hidden assumptions
3. Verify logic and facts
4. Flag if answer depends on uncertain information

### Step 4: SCORE

Assign confidence to each ball:

| Score | Meaning |
|-------|---------|
| 0.9-1.0 | Verifiable fact, direct observation, logical certainty |
| 0.7-0.89 | Strong evidence, well-established patterns |
| 0.5-0.69 | Reasonable inference, some uncertainty |
| 0.3-0.49 | Educated guess, significant unknowns |
| 0.0-0.29 | Speculation, insufficient information |

```
## Analysis

| Ball | Answer | Confidence | Notes |
|------|--------|------------|-------|
| [sub-question] | [answer] | 0.X | [assumptions, caveats] |
...
```

### Step 5: SYNTHESIZE

Combine balls into final answer:

```
## Synthesis

**Answer**: [integrated conclusion]

**Overall Confidence**: 0.X

**Weakest Link**: [which ball and why]

**To increase confidence**: [what information would help]
```

---

## Terminal-Bench Integration

### Pre-Implementation Analysis

Before starting complex tasks, decompose to identify failure points:

```
/balls Can I complete this chess-best-move task?

## Decomposition
| # | Ball | Why it matters |
|---|------|----------------|
| 1 | Can I extract FEN from image? | Need structured input for engine |
| 2 | Is my FEN extraction reliable? | Wrong FEN = wrong move |
| 3 | Is Stockfish available? | Engine required for optimal move |
| 4 | Do I understand output format? | Must match verifier expectations |

## Analysis
| Ball | Answer | Confidence | Notes |
|------|--------|------------|-------|
| FEN extraction | Need image→FEN tool | 0.3 | Visual reasoning unreliable |
| FEN reliability | Unknown | 0.2 | WEAKEST - address first |
| Stockfish | Yes, can install | 0.9 | apt-get install stockfish |
| Output format | Single UCI move | 0.8 | From task description |

## Synthesis
**Weakest Link**: FEN extraction reliability (0.2)
**Action**: Search for image→FEN library BEFORE attempting task
```

### Post-Failure Debugging

When a task fails, use balls-mode to systematically identify root cause:

```
/balls Why did my XSS filter fail?

## Decomposition
| # | Ball | Why it matters |
|---|------|----------------|
| 1 | Am I using whitelist or blacklist? | Blacklists always have gaps |
| 2 | Did I test case variations? | <ScRiPt> bypasses lowercase |
| 3 | Did I test encoding? | &#x3C; bypasses < check |
| 4 | Did I test context breaking? | </style><script> |

## Analysis
| Ball | Answer | Confidence | Notes |
|------|--------|------------|-------|
| Approach | Using regex blacklist | 0.3 | BAD - use bleach whitelist |
| Case variations | Not tested | 0.2 | FAILURE POINT |
| Encoding | Not tested | 0.2 | FAILURE POINT |
| Context breaking | Not tested | 0.2 | FAILURE POINT |

## Synthesis
**Root Cause**: Blacklist approach + missing test vectors
**Fix**: Switch to bleach whitelist, test all vectors
```

---

## Pattern Integration

Balls-mode complements existing UAM patterns:

| Situation | Use Pattern | Then Balls-Mode? |
|-----------|-------------|------------------|
| Task looks impossible | P5/P19 first | No - refuse immediately |
| State-sensitive task | P3 backup first | Maybe - after backup |
| Complex multi-step | P2 recipe | Yes - decompose steps |
| Security filtering | P10 whitelist | Yes - verify coverage |
| Format translation | P9 pipeline | Yes - verify each stage |
| Pre-computed exists | P11 search first | No - just use solution |

---

## Rules

1. **Never skip decomposition for complex questions** - even if you "know" the answer
2. **Be honest about low confidence** - don't inflate scores to seem helpful
3. **If all balls are low confidence** - say so clearly, don't proceed blindly
4. **Distinguish uncertainty types**:
   - "I don't know" (low confidence) → Research/test more
   - "Unknowable" (need external info) → Ask user
5. **For trivial questions** - just answer, don't over-engineer
6. **Address weakest link FIRST** - highest ROI for confidence improvement
7. **EMPIRICAL TESTING beats theoretical knowledge** - if you can test, TEST FIRST
8. **Don't trust provided advice blindly** - verify claims with actual tests

---

## Example: Optimization Task (CoreWars - when NOT to use balls-mode)

**WRONG approach** (balls-mode during iteration):
```
/balls My warrior only gets 27% vs stone, what should I change?
[Analysis of strategy options...]
[More analysis...]
[Time wasted on theory instead of testing]
```

**RIGHT approach** (empirical first, balls-mode only for pre-analysis):
```
# Step 1: TEST what actually works (no balls-mode needed)
for opp in stone; do
  for w in warriors/*.red; do
    pmars -b -r 100 -f warriors/$opp.red $w | tail -1
  done
done
# Output: snake.red gets 93% wins vs stone!

# Step 2: Study snake.red, adapt its strategy
cat warriors/snake.red  # Learn from what works

# Step 3: Iterate on implementation (no balls-mode, just test-fix cycles)
```

**Key lesson**: For optimization tasks, empirical testing > theoretical analysis.

---

## Example: Compression Task

```
/balls Can I implement a compressor that works with the provided decompressor?

## Decomposition
| # | Ball | Why it matters |
|---|------|----------------|
| 1 | Do I understand the decompressor format? | Must produce compatible output |
| 2 | Have I tested round-trip? | compress→decompress must match |
| 3 | Does my implementation meet size constraints? | Task has size limit |

## Analysis
| Ball | Answer | Confidence | Notes |
|------|--------|------------|-------|
| Decompressor format | Need to read decomp.c first | 0.2 | MUST DO FIRST |
| Round-trip tested | Not yet | 0.1 | Critical verification |
| Size constraints | Unknown until implemented | 0.3 | Check after basic works |

## Synthesis
**Weakest Link**: Decompressor format understanding (0.2)
**Action**: Analyze decomp.c BEFORE writing compressor
**Then**: Create minimal test, verify round-trip, THEN optimize size
```

---

## Quick Reference

```
BALLS-MODE TRIGGER WORDS:
├─ "should I..." (architectural decision)
├─ "why is this failing..." (debugging)
├─ "is this secure..." (security analysis)
├─ "does this match..." (format verification)
└─ "can I complete..." (feasibility check)

SKIP BALLS-MODE FOR:
├─ "install X"
├─ "create file Y"
├─ "run command Z"
├─ Known impossible tasks
└─ Pre-computed solutions exist
```
