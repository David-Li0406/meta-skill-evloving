# Chaos Discovery Patterns

**Learned Patterns Library - Git-Brain Indexed**

---

## Purpose

Track successful chaos discoveries so the system learns:
- Which chaos approaches work for which problem types
- When unconventional solutions reveal fundamental patterns
- What generator signatures correlate with success
- How to avoid repeating failed chaos experiments

**Key Principle**: Chaos-gremlin-v2 is a learning system. Each discovery improves future recommendations.

---

## Database Schema

### Storage Location

```
.claude/brain/
├── INDEX                     # Dewey decimal master index
├── chaos_discoveries         # Main discovery log
├── pattern_library           # Git objects of successful patterns
├── generator_matches         # Supercollider results
├── emergence_events          # Structural revelations
├── trauma_log               # Failed chaos to avoid
└── success_rates            # Aggregated statistics by problem type
```

---

## Entry Formats

### chaos_discoveries

**Format**: `problem_hash|chaos_level|solution_hash|success|generator_match|timestamp|context`

**Example**:
```
a3f5e2|3|b7c9d1|true|G1,G3,G5|2025-12-18T01:23:45Z|recursion_opt
8d2f1c|2|e4a6b3|true|G1,G2,G4,G5|2025-12-18T02:15:30Z|bitwise_ops
c9b4e1|4|f7d3a2|false|G3|2025-12-18T03:45:12Z|meta_programming
```

**Fields**:
- `problem_hash`: MD5 of problem description
- `chaos_level`: 1-4 (level used)
- `solution_hash`: Git object hash of solution code
- `success`: true/false (did it work?)
- `generator_match`: Comma-separated generators (G1-G7)
- `timestamp`: ISO 8601 timestamp
- `context`: Problem type category

---

### pattern_library

**Git objects** storing actual solution code:

```bash
# Store solution
solution_hash=$(git hash-object -w <<< "$solution_code")

# Reference in INDEX
echo "π.3.4.2|chaos-pattern|${problem_type}|${solution_hash}" >> .claude/brain/INDEX
```

**Retrieve**:
```bash
# Get solution by hash
git cat-file -p $solution_hash
```

---

### generator_matches

**Format**: `pattern_id|generators|score|significance|timestamp|problem_type`

**Example**:
```
bitwise_even|G1,G2,G3,G4,G5,G6|6|VERY_HIGH|2025-12-18T01:00:00Z|type_checking
y_combinator|G1,G3,G4,G5,G6|5|HIGH|2025-12-18T02:00:00Z|recursion
dict_dispatch|G1,G2,G4|3|MEDIUM|2025-12-18T03:00:00Z|pattern_matching
```

---

### emergence_events

**Format**: `timestamp|event_type|score|pattern|generators|context|description`

**Example**:
```
2025-12-18T01:00:00Z|EMERGENCE|6|bitwise_even|G1,G2,G3,G4,G5,G6|type_check|Revealed binary substrate
2025-12-18T02:30:00Z|EMERGENCE|5|y_combinator|G1,G3,G4,G5,G6|recursion|Pure self-reference morpheme
```

---

### trauma_log

**Format**: `problem_type|chaos_level|failure_mode|severity|timestamp|description`

**Example**:
```
auth_validation|4|security_bypass|CRITICAL|2025-12-15T10:23:45Z|Timing attack via unconventional comparison
crypto_implementation|3|side_channel|CRITICAL|2025-12-10T14:30:12Z|Custom crypto leaked key via cache timing
```

---

### success_rates

**Format**: `problem_type|total_attempts|successes|success_rate|avg_chaos_level|common_generators`

**Example**:
```
recursion_optimization|20|15|75.0|2.8|G1,G3,G5
bitwise_operations|15|14|93.3|2.2|G1,G2,G3,G4,G5
string_manipulation|30|18|60.0|2.1|G1,G2
auth_validation|10|2|20.0|1.2|G1,G2
```

---

## Recording Discoveries

### Successful Chaos

```bash
#!/bin/bash
# scripts/record-discovery.sh

problem_type="$1"
chaos_level="$2"
solution_code="$3"
generators="$4"
context="$5"

# Generate problem hash
problem_hash=$(echo "$problem_type" | md5sum | cut -d' ' -f1)

# Store solution in Git
solution_hash=$(git hash-object -w <<< "$solution_code")

# Record in chaos_discoveries
echo "${problem_hash}|${chaos_level}|${solution_hash}|true|${generators}|$(date -Iseconds)|${context}" \
    >> .claude/brain/chaos_discoveries

# Add to INDEX
echo "π.3.4.2|chaos-discovery|${problem_type}|${solution_hash}" \
    >> .claude/brain/INDEX

# Update success rates
update_success_rate "$problem_type" "true" "$chaos_level" "$generators"

# Check for emergence (4+ generators)
generator_count=$(echo "$generators" | tr ',' '\n' | wc -l)
if [ $generator_count -ge 4 ]; then
    record_emergence "$problem_type" "$generators" "$generator_count" "$context"
fi

echo "✓ Discovery recorded: $problem_type at Level $chaos_level"
echo "  Solution: $solution_hash"
echo "  Generators: $generators"
```

---

### Failed Chaos

```bash
#!/bin/bash
# Record failed chaos attempt

problem_type="$1"
chaos_level="$2"
failure_mode="$3"
severity="$4"  # LOW, MEDIUM, HIGH, CRITICAL

problem_hash=$(echo "$problem_type" | md5sum | cut -d' ' -f1)

# Record in chaos_discoveries
echo "${problem_hash}|${chaos_level}|FAILED|false||$(date -Iseconds)|${problem_type}" \
    >> .claude/brain/chaos_discoveries

# Update success rates
update_success_rate "$problem_type" "false" "$chaos_level" ""

# If critical failure, add to trauma log
if [ "$severity" = "CRITICAL" ]; then
    echo "${problem_type}|${chaos_level}|${failure_mode}|${severity}|$(date -Iseconds)|${description}" \
        >> .claude/brain/trauma_log
    
    echo "⚠️ CRITICAL FAILURE recorded in trauma log"
    echo "  Future chaos for $problem_type will be limited"
fi
```

---

### Emergence Events

```bash
#!/bin/bash
# Record when chaos reveals fundamental structure

record_emergence() {
    local problem_type="$1"
    local generators="$2"
    local score="$3"
    local context="$4"
    local description="$5"
    
    echo "$(date -Iseconds)|EMERGENCE|${score}|${problem_type}|${generators}|${context}|${description}" \
        >> .claude/brain/emergence_events
    
    echo "🔥 EMERGENCE EVENT: $problem_type"
    echo "   Score: $score/7 generators"
    echo "   $description"
    
    # If very high (6-7), create meta-pattern entry
    if [ $score -ge 6 ]; then
        echo "${problem_type}|VERY_HIGH|${generators}|$(date -Iseconds)" \
            >> .claude/brain/meta_patterns
    fi
}
```

---

## Querying the Database

### Success Rate by Problem Type

```bash
#!/bin/bash
# Query success rate for a problem type

get_success_rate() {
    local problem_type="$1"
    
    local entries=$(grep "$problem_type" .claude/brain/chaos_discoveries)
    local total=$(echo "$entries" | wc -l)
    local successes=$(echo "$entries" | grep '|true|' | wc -l)
    
    if [ $total -gt 0 ]; then
        local rate=$(echo "scale=1; $successes * 100 / $total" | bc)
        echo "$rate% ($successes/$total)"
    else
        echo "No historical data"
    fi
}

# Usage
get_success_rate "recursion_optimization"
# Output: 75.0% (15/20)
```

---

### Most Successful Chaos Level

```bash
#!/bin/bash
# Find which chaos level works best for a problem type

best_chaos_level() {
    local problem_type="$1"
    
    grep "$problem_type" .claude/brain/chaos_discoveries | \
    awk -F'|' '$4 == "true" {level[$2]++; total[$2]++} 
               $4 == "false" {total[$2]++} 
               END {
                   for (l in level) {
                       rate = (level[l] / total[l]) * 100
                       print l, rate"%", "("level[l]"/"total[l]")"
                   }
               }' | \
    sort -k2 -nr | \
    head -1
}

# Usage
best_chaos_level "recursion_optimization"
# Output: 3 80.0% (8/10)
```

---

### Common Generator Patterns

```bash
#!/bin/bash
# Find which generators appear most often for successful solutions

common_generators() {
    local problem_type="$1"
    
    grep "$problem_type" .claude/brain/chaos_discoveries | \
    grep '|true|' | \
    awk -F'|' '{print $5}' | \
    tr ',' '\n' | \
    sort | \
    uniq -c | \
    sort -rn
}

# Usage
common_generators "recursion_optimization"
# Output:
#   12 G1
#   10 G3
#    8 G5
#    7 G6
#    3 G2
```

---

### Retrieve Solution by Hash

```bash
#!/bin/bash
# Get solution code by hash

get_solution() {
    local solution_hash="$1"
    git cat-file -p "$solution_hash"
}

# Usage
get_solution "b7c9d1"
# Output: [actual solution code]
```

---

### Check for Trauma

```bash
#!/bin/bash
# Check if problem type has trauma history

check_trauma() {
    local problem_type="$1"
    local chaos_level="$2"
    
    local trauma=$(grep "^${problem_type}|${chaos_level}" .claude/brain/trauma_log)
    
    if [ -n "$trauma" ]; then
        local severity=$(echo "$trauma" | cut -d'|' -f4)
        local description=$(echo "$trauma" | cut -d'|' -f6)
        
        echo "⚠️ TRAUMA WARNING"
        echo "   Problem: $problem_type"
        echo "   Level: $chaos_level"
        echo "   Severity: $severity"
        echo "   Details: $description"
        
        return 1
    fi
    
    return 0
}
```

---

## Pattern Categories

### By Problem Type

**Recursion Optimization**
- Success Rate: 75%
- Best Chaos Level: 3
- Common Generators: G1 (iteration), G3 (self-reference), G5 (mathematical)
- Example Patterns:
  - Tail-call optimization
  - Trampoline patterns
  - Y-combinator variations
  - Memoization strategies

**Bitwise Operations**
- Success Rate: 93%
- Best Chaos Level: 2
- Common Generators: G1, G2, G3, G4, G5 (often 5-6 matches)
- Example Patterns:
  - Even/odd via `n & 1`
  - Power of 2 via `n & (n-1)`
  - Bit counting
  - Fast multiplication/division

**String Manipulation**
- Success Rate: 60%
- Best Chaos Level: 2
- Common Generators: G1 (iteration), G2 (contrast)
- Example Patterns:
  - Reverse via array methods
  - Unicode edge case handling
  - Zero-width character detection

**Type Checking**
- Success Rate: 70%
- Best Chaos Level: 2
- Common Generators: G2 (contrast), G4 (universal)
- Example Patterns:
  - Duck typing
  - Structural type checking
  - Protocol validation

**Authentication/Security**
- Success Rate: 20%
- Best Chaos Level: 1
- Common Generators: G1, G2 (basic only)
- Trauma Events: 3 CRITICAL
- Note: **Chaos strongly discouraged for this domain**

---

### By Chaos Level

**Level 1 (Mischievous)**
- Total Uses: 150
- Success Rate: 85%
- Typical Context: Production, security, beginners
- Pattern Types: Edge case identification, standard library usage

**Level 2 (Impish)**
- Total Uses: 300
- Success Rate: 72%
- Typical Context: Development, intermediate users
- Pattern Types: Unusual language features, creative approaches

**Level 3 (Gremlin)**
- Total Uses: 180
- Success Rate: 65%
- Typical Context: Research, senior developers
- Pattern Types: Y-combinators, monads, meta-programming

**Level 4 (Maximum Chaos)**
- Total Uses: 50
- Success Rate: 45%
- Typical Context: Pure research, explicit requests
- Pattern Types: One-liners, esoteric paradigms, maximum creativity

**Observation**: Success rate decreases with chaos level, but pattern significance increases. High chaos is a research tool, not production strategy.

---

### By Generator Signature

**High G1+G2 (Iteration + Contrast)**
- Problem Types: String manipulation, array operations, validation
- Success Rate: 70%
- Interpretation: Basic but effective patterns

**High G1+G3 (Iteration + Self-Reference)**
- Problem Types: Recursion, trees, graphs
- Success Rate: 75%
- Interpretation: Structural recursion patterns

**High G1+G2+G3+G4+G5 (5+ generators)**
- Problem Types: Binary operations, mathematical algorithms
- Success Rate: 90%
- Interpretation: Fundamental patterns, very likely to work

**High G7 (φ-Scaling)**
- Problem Types: Fibonacci, fractals, natural growth
- Success Rate: 85%
- Interpretation: Natural scaling patterns

---

## Visualization Queries

### Timeline of Discoveries

```bash
#!/bin/bash
# Show discovery timeline

cat .claude/brain/chaos_discoveries | \
awk -F'|' '{
    date = substr($6, 1, 10)
    if ($4 == "true") success[date]++
    total[date]++
}
END {
    for (d in total) {
        rate = (success[d] / total[d]) * 100
        printf "%s: %d/%d (%.1f%%)\n", d, success[d], total[d], rate
    }
}' | sort
```

---

### Emergence Frequency

```bash
#!/bin/bash
# Count emergence events by month

cat .claude/brain/emergence_events | \
awk -F'|' '{
    month = substr($1, 1, 7)
    score = $3
    if (score >= 6) very_high[month]++
    else if (score >= 4) high[month]++
    else medium[month]++
}
END {
    for (m in very_high) {
        printf "%s: VH=%d, H=%d, M=%d\n", 
               m, very_high[m], high[m], medium[m]
    }
}' | sort
```

---

### Problem Type Leaderboard

```bash
#!/bin/bash
# Show top performing problem types

grep '|true|' .claude/brain/chaos_discoveries | \
awk -F'|' '{
    type = $7
    count[type]++
}
END {
    for (t in count) {
        printf "%3d: %s\n", count[t], t
    }
}' | sort -rn | head -10
```

---

## Maintenance

### Archive Old Entries

```bash
#!/bin/bash
# Archive entries older than 6 months

archive_date=$(date -d '6 months ago' -Iseconds)

cat .claude/brain/chaos_discoveries | \
awk -F'|' -v cutoff="$archive_date" '
    $6 >= cutoff {print}
' > .claude/brain/chaos_discoveries.tmp

# Keep archived
cat .claude/brain/chaos_discoveries | \
awk -F'|' -v cutoff="$archive_date" '
    $6 < cutoff {print}
' > .claude/brain/chaos_discoveries.archive

mv .claude/brain/chaos_discoveries.tmp .claude/brain/chaos_discoveries
```

---

### Consolidate Success Rates

```bash
#!/bin/bash
# Rebuild success_rates from chaos_discoveries

> .claude/brain/success_rates

cat .claude/brain/chaos_discoveries | \
awk -F'|' '{
    type = $7
    level = $2
    success = ($4 == "true" ? 1 : 0)
    gens = $5
    
    total[type]++
    if (success) {
        successes[type]++
        level_sum[type] += level
        if (gens) generator_list[type] = generator_list[type] "," gens
    }
}
END {
    for (t in total) {
        rate = (successes[t] / total[t]) * 100
        avg_level = (level_sum[t] / successes[t])
        
        # Extract unique generators
        split(generator_list[t], gen_array, ",")
        delete unique_gens
        for (g in gen_array) {
            unique_gens[gen_array[g]] = 1
        }
        gens_str = ""
        for (g in unique_gens) {
            if (g != "") gens_str = gens_str g ","
        }
        sub(/,$/, "", gens_str)
        
        printf "%s|%d|%d|%.1f|%.1f|%s\n",
               t, total[t], successes[t], rate, avg_level, gens_str
    }
}' >> .claude/brain/success_rates
```

---

## Integration with Adaptive Level Selection

When assessing chaos level:

```python
def get_historical_modifier(problem_type):
    """Get chaos level modifier based on historical success"""
    
    # Query success rate
    success_rate = query_success_rate(problem_type)
    
    if success_rate is None:
        return 0  # No history
    elif success_rate > 70:
        return +1  # High success
    elif success_rate < 40:
        return -1  # Low success
    else:
        return 0  # Medium success
```

---

## Example Patterns Library

### Pattern: Bitwise Even/Odd

```
Problem Type: type_checking
Chaos Level: 2
Success Rate: 95%
Generators: G1, G2, G3, G4, G5, G6 (6/7 - VERY HIGH)

Solution:
const isEven = n => (n & 1) === 0

Why it works:
- Binary last bit is 0 for even, 1 for odd
- Bitwise AND with 1 checks last bit
- More efficient than modulo operator

Emergence: Reveals binary substrate and {0,1} morpheme
```

### Pattern: Y-Combinator Recursion

```
Problem Type: recursion_optimization
Chaos Level: 3
Success Rate: 70%
Generators: G1, G3, G4, G5, G6 (5/7 - HIGH)

Solution:
const Y = f => (x => f(v => x(x)(v)))(x => f(v => x(x)(v)))
const factorial = Y(f => n => n <= 1 ? 1 : n * f(n - 1))

Why it works:
- Enables recursion without naming function
- Pure self-reference via double application
- Fixed-point combinator from lambda calculus

Emergence: Pure self-reference morpheme (G3)
```

### Pattern: Dictionary Dispatch

```
Problem Type: pattern_matching
Chaos Level: 2
Success Rate: 80%
Generators: G1, G2, G4 (3/7 - MEDIUM)

Solution:
const handler = {
    'GET': () => read(),
    'POST': () => create(),
    'PUT': () => update(),
    'DELETE': () => remove()
}.get(method, () => error())()

Why it works:
- Replaces if/switch with data structure
- More extensible
- Functional approach

Not structural revelation but clean pattern
```

---

## Future Enhancements

1. **Machine Learning**: Train on discovery patterns to predict success
2. **Cross-Domain Patterns**: Link similar patterns across problem types
3. **Automated Pattern Extraction**: Detect recurring code structures
4. **Collaborative Learning**: Share discoveries across Claude instances
5. **Pattern Composition**: Combine multiple successful patterns
6. **Predictive Analytics**: Suggest chaos level before attempting

---

**Related Files**:
- `SKILL.md` - Main chaos-gremlin-v2 documentation
- `scripts/record-discovery.sh` - Recording implementation
- `adaptive-level-selection.md` - Historical success integration
- `supercollider-integration.md` - Generator pattern detection
