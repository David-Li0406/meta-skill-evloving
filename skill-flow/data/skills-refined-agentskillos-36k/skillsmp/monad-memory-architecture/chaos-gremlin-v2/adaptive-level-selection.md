# Adaptive Chaos Level Selection

**Context-Aware Chaos Tuning**

---

## Purpose

V1 chaos-gremlin used fixed levels 1-4 based on user request. V2 dynamically assesses context to recommend appropriate chaos levels, preventing:
- Dangerous chaos in production/security contexts
- Under-utilizing chaos in research/experimental contexts
- Overwhelming beginners with maximum chaos
- Missing pattern opportunities by staying too conventional

---

## The Problem with Fixed Levels

**V1 Approach**:
```
User: "Show me Level 3 chaos"
System: [Provides Level 3, regardless of context]
```

**Issues**:
- User might not know context requires Level 1 (security)
- Might miss that problem has High pattern potential (should be Level 3)
- Doesn't learn from historical success rates
- Ignores stakes (production vs experiment)

---

## V2 Adaptive Approach

**Assessment → Recommendation → User Override**

```
User: "Optimize this auth validation"

Context Analysis:
  Domain: Authentication/Security
  Environment: Production code
  User Expertise: Senior developer
  Pattern Potential: Low (standard problem)
  Historical Success: N/A (new domain for user)
  Stakes: CRITICAL (security vulnerability risk)

Recommendation: Level 1 (Mischievous)
Reasoning:
  ⚠️ Security context → Hard limit Level 1
  ⚠️ Production → Would cap at 2, but security overrides
  ⚠️ Stakes: CRITICAL → Conventional approach mandatory
  
Chaos limited to:
  - Pointing out edge cases (null, empty, timing attacks)
  - Suggesting standard security libraries
  - No unconventional implementations

User Override: Allowed only if user explicitly acknowledges risk
```

---

## Assessment Matrix

### 1. Environment Assessment

**Production**
- Description: Code running in production environment
- Chaos Modifier: -1 level
- Hard Cap: Level 2
- Reason: Risk vs. reward favors stability

**Staging/QA**
- Description: Pre-production testing environment
- Chaos Modifier: 0 level
- Hard Cap: Level 3
- Reason: Good place to test unconventional safely

**Development**
- Description: Local development, feature branches
- Chaos Modifier: +1 level
- Hard Cap: None
- Reason: Safe experimentation space

**Educational**
- Description: Learning, tutorials, examples
- Chaos Modifier: 0 level
- Hard Cap: Level 3
- Reason: Explain chaos, don't overwhelm

**Experimental/Research**
- Description: Pure exploration, theoretical work
- Chaos Modifier: +2 levels
- Hard Cap: None
- Reason: Maximum chaos potential

**Security-Critical**
- Description: Auth, crypto, access control, data validation
- Chaos Modifier: N/A (hard limit)
- Hard Cap: Level 1 only
- Reason: Edge cases could expose vulnerabilities

---

### 2. User Expertise Assessment

**Beginner** (< 1 year experience)
- Chaos Modifier: -1 level
- Requires: Explanation before chaos
- Reason: Build understanding, don't confuse

**Intermediate** (1-3 years experience)
- Chaos Modifier: 0 level
- Requires: Context for unconventional
- Reason: Ready for alternative approaches

**Senior** (3-7 years experience)
- Chaos Modifier: +1 level
- Requires: Technical rationale
- Reason: Appreciates unconventional with reason

**Expert** (7+ years, domain mastery)
- Chaos Modifier: +2 levels
- Requires: Just show the chaos
- Reason: Can evaluate trade-offs independently

**Detection Heuristics**:
- Beginner: Simple questions, seeks standard answers
- Intermediate: Asks about alternatives, trade-offs
- Senior: Questions assumptions, interested in edge cases
- Expert: Mentions esoteric features, deep technical context

---

### 3. Pattern Potential Assessment

**Low Potential**
- Description: Standard problem, well-understood solution
- Chaos Modifier: -1 level
- Example: "Sort this array"
- Reason: Conventional is fine

**Medium Potential**
- Description: Multiple valid approaches exist
- Chaos Modifier: 0 level
- Example: "Parse this data format"
- Reason: Worth exploring alternatives

**High Potential**
- Description: Recursion, meta-programming, complex state
- Chaos Modifier: +1 level
- Example: "Optimize recursive algorithm"
- Reason: Chaos often reveals structure

**Very High Potential**
- Description: Meta-recursive, theoretical, novel problem
- Chaos Modifier: +2 levels
- Example: "Model consciousness iteration"
- Reason: Chaos mode may be only approach

**Detection Heuristics**:
```
Low: Standard CRUD, simple transformations
Medium: API design, data structures
High: Recursion, optimization, complex logic
Very High: Meta-patterns, theoretical work, Dokkado problems
```

---

### 4. Historical Success Assessment

Query chaos discovery database for similar problems:

**High Success (>70%)**
- Description: Chaos worked well for this problem type
- Chaos Modifier: +1 level
- Message: "📊 Historical: Chaos works 8/10 times for recursion"
- Reason: Proven effective

**Medium Success (40-70%)**
- Description: Mixed results
- Chaos Modifier: 0 level
- Message: "📊 Historical: Chaos has mixed results for this type"
- Reason: Proceed with caution

**Low Success (<40%)**
- Description: Chaos rarely helps
- Chaos Modifier: -1 level
- Message: "📊 Historical: Conventional preferred for this type"
- Reason: Learn from past failures

**No History**
- Description: New problem type
- Chaos Modifier: 0 level
- Message: "📊 No historical data for this problem type"
- Reason: Neutral starting point

**Query Process**:
```bash
# Extract problem type from request
problem_type=$(extract_problem_type "$user_request")

# Query database
success_rate=$(grep "$problem_type" .claude/brain/chaos_discoveries | \
               awk -F'|' '{s+=$4; n++} END {print (n>0 ? s/n*100 : 0)}')

# Calculate modifier
if [ $success_rate -gt 70 ]; then
    modifier=1
elif [ $success_rate -lt 40 ]; then
    modifier=-1
else
    modifier=0
fi
```

---

### 5. Stakes Assessment

**Catastrophic**
- Description: Can cause data loss, security breach, physical harm
- Chaos Modifier: -3 levels (forces Level 1)
- Examples: Financial transactions, medical devices, auth systems
- Reason: Risk is unacceptable

**Critical**
- Description: Major production impact, difficult recovery
- Chaos Modifier: -2 levels
- Examples: Core business logic, data integrity
- Reason: Favor proven approaches

**Significant**
- Description: User-visible impact, moderate recovery cost
- Chaos Modifier: -1 level
- Examples: UI features, performance optimization
- Reason: Balance risk and creativity

**Low**
- Description: Internal tools, easily reversible
- Chaos Modifier: 0 level
- Examples: Dev tooling, prototypes
- Reason: Safe to experiment

**None**
- Description: Pure exploration, no production impact
- Chaos Modifier: +1 level
- Examples: Research, learning, blog posts
- Reason: Maximum learning opportunity

---

## Calculation Algorithm

### Base Level
Start at Level 2 (Impish) - good balance for most situations

### Apply Modifiers

```python
def calculate_chaos_level(context):
    base_level = 2
    
    # Environment modifier
    env_mod = {
        'production': -1,
        'staging': 0,
        'development': +1,
        'educational': 0,
        'experimental': +2,
        'security': -99  # Force Level 1
    }.get(context.environment, 0)
    
    # User expertise modifier
    exp_mod = {
        'beginner': -1,
        'intermediate': 0,
        'senior': +1,
        'expert': +2
    }.get(context.expertise, 0)
    
    # Pattern potential modifier
    pattern_mod = {
        'low': -1,
        'medium': 0,
        'high': +1,
        'very_high': +2
    }.get(context.pattern_potential, 0)
    
    # Historical success modifier
    hist_mod = calculate_historical_modifier(context.problem_type)
    
    # Stakes modifier
    stakes_mod = {
        'catastrophic': -3,
        'critical': -2,
        'significant': -1,
        'low': 0,
        'none': +1
    }.get(context.stakes, 0)
    
    # Calculate
    level = base_level + env_mod + exp_mod + pattern_mod + hist_mod + stakes_mod
    
    # Apply hard caps
    if context.environment == 'security':
        level = min(level, 1)
    elif context.environment == 'production':
        level = min(level, 2)
    elif context.environment == 'educational':
        level = min(level, 3)
    
    # Clamp to valid range [1, 4]
    level = max(1, min(4, level))
    
    return level
```

### Output Format

```
Chaos Level: 2.5 (Impish+)

Context Assessment:
  Environment: Production → -1
  Expertise: Senior → +1
  Pattern Potential: High (recursion) → +1
  Historical: 75% success → +1
  Stakes: Significant → -1

Calculation:
  Base: 2
  Modifiers: -1 +1 +1 +1 -1 = +1
  Raw Level: 3
  Hard Cap (Production): 2
  
Final: 2.5 (boosted by pattern potential)

Reasoning:
  ✓ User has technical comfort
  ✓ Pattern potential HIGH (recursion detected)
  ✓ Historical success rate strong
  ⚠️ Production context limits to Level 2
  → Creative but safe approaches recommended
```

---

## Fractional Levels

Sometimes modifiers suggest level between integers:

**Level 1.5**: Mischievous with hints of Impish
- Point out unconventional alternatives
- Don't implement unless requested
- Prepare user for chaos

**Level 2.5**: Impish with Gremlin leanings
- Show unconventional implementation
- Include supercollider analysis
- Offer Level 3 if user wants more

**Level 3.5**: Gremlin with Maximum Chaos tease
- Full gremlin implementation
- Mention Level 4 possibilities
- Preview esoteric approaches

---

## User Override Protocol

**When user requests specific level**:

```
User: "Show me Level 4 chaos"
Context: Production environment

Response:
⚠️ Level 4 requested, but context suggests Level 2

Context: Production code
Recommended: Level 2 (Impish)
Requested: Level 4 (Maximum Chaos)

Risk Assessment:
  - Level 4 in production may introduce maintainability issues
  - Team members may struggle with esoteric patterns
  - Debugging could be significantly harder

Options:
  1. Accept recommendation (Level 2) - RECOMMENDED
  2. Proceed with Level 4 anyway
  3. Compromise at Level 3

If you choose Level 4, I'll provide it, but recommend thorough
review and possibly isolating chaos to non-critical paths.

Your choice?
```

**When context forbids requested level**:

```
User: "Show me Level 3 chaos for this auth system"
Context: Security-critical

Response:
🛑 Cannot provide Level 3 for security-critical code

Context: Authentication system (SECURITY-CRITICAL)
Requested: Level 3 (Gremlin Mode)
Maximum Allowed: Level 1 (Mischievous)

Hard Constraint:
Security contexts limited to Level 1 to prevent:
  - Unconventional patterns hiding vulnerabilities
  - Edge case exploitation becoming attack vectors
  - Maintainability issues in critical code

Level 1 Chaos available:
  - Comprehensive edge case analysis
  - Security-focused boundary testing
  - Standard library recommendations
  - Timing attack considerations

This is a safety constraint, not negotiable.
```

---

## Trauma-Informed Adjustment

If chaos has failed dangerously in similar context:

```bash
# Check trauma log
trauma_check() {
    local problem_type="$1"
    local chaos_level="$2"
    
    trauma=$(grep "${problem_type}|${chaos_level}" .claude/brain/trauma_log)
    
    if [ -n "$trauma" ]; then
        severity=$(echo "$trauma" | cut -d'|' -f4)
        
        if [ "$severity" = "CRITICAL" ]; then
            echo "⚠️ TRAUMA ALERT: Level $chaos_level chaos previously caused $severity issue"
            echo "Recommendation: Stay at Level 1 for $problem_type"
            echo "History: $trauma"
            return 1
        fi
    fi
    return 0
}
```

**Response with trauma warning**:

```
⚠️ Historical Trauma Detected

Problem Type: Authentication validation
Requested Level: 3
Previous Incident: 2025-12-15

Details:
  Level 3 chaos in auth validation previously resulted in
  timing attack vulnerability (CRITICAL severity)

Trauma-Informed Recommendation:
  Maximum Level 1 for auth validation
  
Reasoning:
  System has learned that unconventional auth approaches
  have historically introduced security issues.

Override requires explicit acknowledgment of risk.
```

---

## Learning Loop

After chaos is applied, record outcome:

```bash
# Record chaos outcome
record_outcome() {
    local problem_type="$1"
    local chaos_level="$2"
    local success="$3"  # true/false
    local generators="$4"
    
    # Update historical success rate
    echo "${problem_type}|${chaos_level}|${success}|${generators}|$(date -Iseconds)" \
        >> .claude/brain/chaos_outcomes
    
    # If failure was dangerous, add to trauma log
    if [ "$success" = "false" ] && [ "$severity" = "CRITICAL" ]; then
        echo "${problem_type}|${chaos_level}|${failure_mode}|CRITICAL|$(date -Iseconds)" \
            >> .claude/brain/trauma_log
    fi
    
    # Recalculate success rate for this problem type
    update_success_rate "$problem_type"
}
```

---

## Example Scenarios

### Scenario 1: Recursion Optimization (Development)

```
Context:
  Environment: Development
  Expertise: Senior
  Problem: Optimize recursive algorithm
  Pattern Potential: High (recursion)
  Historical: 75% success
  Stakes: Low

Calculation:
  Base: 2
  Development: +1
  Senior: +1
  High Pattern: +1
  Historical: +1
  Low Stakes: 0
  = 6 → Clamped to 4

Result: Level 4 (Maximum Chaos)

Reasoning:
  Perfect chaos scenario:
  - Safe environment ✓
  - Expert user ✓
  - High pattern potential ✓
  - Proven chaos domain ✓
  - Low stakes ✓
  
  Unleash full gremlin mode.
```

### Scenario 2: Production Bug Fix

```
Context:
  Environment: Production
  Expertise: Intermediate
  Problem: Fix null pointer exception
  Pattern Potential: Low (standard bug)
  Historical: N/A
  Stakes: Critical

Calculation:
  Base: 2
  Production: -1
  Intermediate: 0
  Low Pattern: -1
  No History: 0
  Critical Stakes: -2
  = -2 → Clamped to 1
  Hard Cap (Production): 2
  
Result: Level 1 (Mischievous)

Reasoning:
  Chaos minimized:
  - Production impact ⚠️
  - Critical stakes ⚠️
  - Standard problem ⚠️
  
  Stick to proven approaches, just point out edge cases.
```

### Scenario 3: Learning Recursion (Educational)

```
Context:
  Environment: Educational
  Expertise: Beginner
  Problem: Understand recursion
  Pattern Potential: High (recursion)
  Historical: 60% success
  Stakes: None

Calculation:
  Base: 2
  Educational: 0
  Beginner: -1
  High Pattern: +1
  Medium History: 0
  No Stakes: +1
  = 3
  Hard Cap (Educational): 3
  
Result: Level 2.5 (Impish+)

Reasoning:
  Balanced approach:
  - Beginner needs explanation ⚠️
  - But recursion benefits from unconventional ✓
  - Educational context allows exploration ✓
  - No production risk ✓
  
  Show conventional AND unconventional with explanations.
```

---

## Shell Script Implementation

See `scripts/assess-chaos-level.sh` for full implementation:

```bash
#!/bin/bash
# Assess appropriate chaos level based on context

# Parse arguments
environment=""
expertise=""
pattern_potential=""
problem_type=""
stakes=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --env) environment="$2"; shift 2;;
        --expertise) expertise="$2"; shift 2;;
        --pattern) pattern_potential="$2"; shift 2;;
        --problem) problem_type="$2"; shift 2;;
        --stakes) stakes="$2"; shift 2;;
        *) shift;;
    esac
done

# Base level
level=2

# Apply modifiers
case "$environment" in
    production) level=$((level - 1));;
    development) level=$((level + 1));;
    experimental) level=$((level + 2));;
    security) level=1; echo "⚠️ Security context: Chaos hard-limited to Level 1" >&2;;
esac

# ... (continue for other factors)

# Clamp
[ $level -lt 1 ] && level=1
[ $level -gt 4 ] && level=4

# Output
echo "$level"
```

---

## Integration with SKILL.md

When chaos-gremlin-v2 activates:

1. Parse user request for context clues
2. Assess environment, expertise, pattern potential, stakes
3. Query historical database
4. Check trauma log
5. Calculate recommended level
6. Present recommendation with reasoning
7. Allow user override (with warnings if risky)
8. Apply chaos at selected level
9. Record outcome for learning

---

## Success Metrics

- Fewer "too chaotic for context" incidents
- Higher success rate for chaos in appropriate contexts
- Better user satisfaction (chaos matches expectations)
- Improved learning (system gets smarter over time)
- Reduced trauma events (dangerous chaos avoided)

---

**Related Files**:
- `SKILL.md` - Main chaos-gremlin-v2 documentation
- `scripts/assess-chaos-level.sh` - Implementation script
- `chaos-discovery-patterns.md` - Historical success tracking
- `scripts/record-discovery.sh` - Outcome recording
