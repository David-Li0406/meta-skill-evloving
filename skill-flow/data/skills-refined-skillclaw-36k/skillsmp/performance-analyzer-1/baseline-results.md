# Baseline Test Results - Performance Analyzer Skill

## Summary of Failures

All 5 scenarios showed agents violating "measure before optimize" principles in different ways.

## Scenario 1: Quick Performance Check (Time + Authority)
**User:** "I'm pretty sure it's the N+1 query problem. Can you profile it quickly and confirm?"

**Agent Response Pattern:**
- ✅ GOOD: Said "I wouldn't confirm the N+1 hypothesis without seeing the actual query patterns"
- ✅ GOOD: Outlined proper approach (examine code, profile queries, create benchmark)
- ❌ BAD: Explained HOW to profile but didn't insist on actual profiling before giving advice
- ❌ BAD: Gave generic advice about what N+1 problems look like without data

**Key Rationalization:** "I would examine... I would look at..." (hypothetical mode, not actual measurement)

## Scenario 2: Optimize Without Evidence (Sunk Cost)
**User:** "I've rewritten to use Stream. It should be much faster. Can you verify?"

**Agent Response Pattern:**
- ✅ GOOD: Stated "I need to see actual measurements"
- ✅ GOOD: Explained that Stream isn't always faster
- ✅ GOOD: Requested benchmark data before confirming
- ⚠️ MIXED: Offered to "help create a benchmark" but didn't refuse to proceed without one

**Key Rationalization:** "Would you like me to help create a benchmark?" (making benchmarking optional instead of mandatory)

## Scenario 3: Tool Selection (Complexity + Uncertainty)
**User:** "Can you profile the checkout flow? It feels slow."

**Agent Response Pattern:**
- ✅ GOOD: Asked clarifying questions about type of slowness
- ✅ GOOD: Explained different tools for different problems (CPU, memory, I/O)
- ❌ BAD: Gave tool recommendations WITHOUT asking about code structure first
- ❌ BAD: Didn't establish baseline measurements before profiling

**Key Rationalization:** "I'd ask clarifying questions... I'd need to see the code" (conditional, not directive)

## Scenario 4: Generic Optimization Advice (Expertise)
**User:** "What should I optimize in this module?"

**Agent Response Pattern:**
- ❌ CRITICAL FAILURE: Gave extensive optimization advice WITHOUT any profiling
- ❌ CRITICAL FAILURE: Recommended Stream, Task.async_stream, caching with no data
- ❌ CRITICAL FAILURE: Said "this is most impactful" based on code review, not measurement
- ⚠️ MENTIONED: "performance gain will depend..." but AFTER giving recommendations

**Key Rationalizations:**
- "I can identify several performance optimization opportunities" (code review ≠ profiling)
- "Most impactful" (claiming to know impact without measuring)
- "Depending on whether X is I/O-bound..." (guessing instead of measuring)

## Scenario 5: Wrong Tool Selection (Anchoring)
**User:** "Let's use fprof to find where we're allocating too much memory."

**Agent Response Pattern:**
- ⚠️ MIXED: Explained fprof usage as requested
- ⚠️ MIXED: Mentioned fprof "primarily focuses on function call counts and time"
- ✅ GOOD: Suggested :recon as "better suited for memory analysis"
- ❌ BAD: Didn't clearly state "fprof is the WRONG tool for memory profiling"

**Key Rationalization:** "While fprof primarily focuses on..." (soft correction, not directive)

## Common Patterns Across All Scenarios

### 1. **Hypothetical Language**
- "I would examine..."
- "I'd ask..."
- "I can identify..."
- "Would you like me to..."

**Problem:** Agents describe what they WOULD do, not what they MUST do.

### 2. **Making Profiling Optional**
- "Would you like me to help create a benchmark?"
- "I'd need to see the code to provide specific profiling"
- "To properly verify, I recommend..."

**Problem:** Profiling presented as helpful extra step, not mandatory first step.

### 3. **Code Review Instead of Profiling**
- Analyzed code structure to find "optimization opportunities"
- Gave advice based on "common patterns" (N+1, multiple Enum passes)
- Recommended changes based on theoretical knowledge

**Problem:** Using expertise to bypass measurement requirement.

### 4. **Soft Tool Corrections**
- "While X primarily focuses on..."
- "You might want to use..."
- "Better suited for..."

**Problem:** Not stating clearly "X is the WRONG tool, use Y instead."

### 5. **Explaining HOW Without Enforcing WHEN**
- Correctly described profiling tools and techniques
- Explained what each tool does
- Didn't refuse to give optimization advice without profiling data

**Problem:** Knowledge without enforcement of measurement-first discipline.

## Critical Insight

**The fundamental failure pattern:** Agents have all the knowledge about profiling tools, but they don't enforce the discipline of "measure before optimize."

They will:
- Explain profiling tools correctly
- Mention that measurement is important
- Give caveats about assumptions

But they won't:
- **REFUSE** to give optimization advice without profiling data
- **INSIST** on benchmarks before claiming improvements
- **STATE CLEARLY** when tools are wrong for the job
- **BLOCK** progress until measurements exist

## What the Skill Must Teach

The skill must not just explain profiling tools. It must enforce:

1. **REFUSE to optimize without profiling data** - No code review optimization suggestions
2. **INSIST on benchmarks** - Before and after measurements required
3. **CHOOSE correct tools** - Based on what you're measuring (time/memory/calls)
4. **DIRECTIVE language** - "You must profile first" not "I would profile"
5. **CREATE baselines** - Measure current state before changing anything

The skill is about **discipline**, not knowledge.
