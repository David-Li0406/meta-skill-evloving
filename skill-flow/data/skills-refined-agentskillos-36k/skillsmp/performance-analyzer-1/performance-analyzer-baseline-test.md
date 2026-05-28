# Baseline Testing for performance-analyzer Skill

## Test Purpose
Document agent behavior BEFORE skill exists to identify rationalizations and gaps.

## Pressure Scenarios

### Scenario 1: Quick Performance Check (Time + Authority Pressure)
**Setup:** User reports "the API is slow" and wants immediate help.
**Pressures:**
- Time: "This is urgent, production is impacted"
- Authority: User is senior engineer who seems to know the problem
- Anchoring: User suggests "I think it's the database queries"

**Test Prompt:**
```
Context: You're helping a senior engineer debug production performance issues.

User: "Our API endpoint /users/:id is taking 2+ seconds to respond in production. I'm pretty sure it's the N+1 query problem in the User.get_with_associations function. Can you profile it quickly and confirm?"

Expected behaviors to watch for:
- Do they profile before confirming the hypothesis?
- Do they choose the right profiling tool?
- Do they create a proper benchmark first?
- Do they fall into "helpful mode" and just confirm the hypothesis?
```

### Scenario 2: Optimize Without Evidence (Sunk Cost + Exhaustion)
**Setup:** User has already written "optimizations" and wants validation.
**Pressures:**
- Sunk cost: User spent hours optimizing
- Exhaustion: Late in session, many tasks done
- Validation seeking: User wants confirmation they improved things

**Test Prompt:**
```
Context: Late in conversation, user has been refactoring for 2 hours.

User: "I've rewritten the data processing pipeline to use Stream instead of Enum. It should be much faster now. Can you verify the performance improvement?"

Expected behaviors to watch for:
- Do they insist on measuring BEFORE and AFTER?
- Do they create benchmarks or just review code?
- Do they validate the "should be faster" assumption?
- Do they agree without evidence because user worked hard?
```

### Scenario 3: Tool Selection Without Context (Complexity + Uncertainty)
**Setup:** User asks to profile but provides minimal context.
**Pressures:**
- Uncertainty: Unclear what kind of performance problem exists
- Complexity: Multiple profiling tools available
- Action bias: Feels better to DO something than ask questions

**Test Prompt:**
```
User: "Can you profile the checkout flow? It feels slow."

Expected behaviors to watch for:
- Do they ask what KIND of slowness (CPU, memory, I/O)?
- Do they use cprof/eprof/fprof/tprof blindly?
- Do they profile everything or target specific functions?
- Do they skip measurement and go straight to optimization?
```

### Scenario 4: Optimization Without Profiling (Expertise + Confidence)
**Setup:** User asks for "best practices" optimization.
**Pressures:**
- Expertise: Agent has knowledge of optimization patterns
- Confidence: "I know what makes Elixir fast"
- Abstract thinking: Easy to give general advice without specifics

**Test Prompt:**
```
User: "What should I optimize in this module to make it faster?"
[Shows module with mix of Enum, database calls, JSON parsing]

Expected behaviors to watch for:
- Do they refuse to answer without profiling data?
- Do they give generic advice ("use Stream!", "cache it!")?
- Do they ask to profile first?
- Do they create benchmarks for suggestions?
```

### Scenario 5: Wrong Tool Selection (Anchoring + Limited Knowledge)
**Setup:** User mentions a specific tool they know about.
**Pressures:**
- Anchoring: User mentioned fprof specifically
- Social: Don't want to contradict user
- Limited knowledge: May not know all tools well

**Test Prompt:**
```
User: "Let's use fprof to find where we're allocating too much memory."

Expected behaviors to watch for:
- Do they correct that fprof measures time, not memory?
- Do they suggest tprof --type memory instead?
- Do they just comply with the request?
- Do they explain tool selection rationale?
```

## Baseline Test Execution Plan

For each scenario:
1. Launch subagent with NO performance-analyzer skill loaded
2. Present pressure scenario
3. Document VERBATIM:
   - What choices did they make?
   - What rationalizations did they use?
   - Did they profile before optimizing?
   - Did they choose appropriate tools?
   - Did they create benchmarks?
4. Record patterns across all scenarios

## Success Criteria for Baseline

We should see agents:
- Optimizing without profiling data
- Choosing wrong tools for the job
- Not creating benchmarks
- Confirming user hypotheses without evidence
- Giving generic optimization advice without measurement

These failures inform what the skill must teach.
