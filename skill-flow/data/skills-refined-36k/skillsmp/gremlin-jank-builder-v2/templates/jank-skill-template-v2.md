---
name: skill-name
description: Use this skill when [specific trigger context]. [What it does in one sentence]. [Why it's distinct from alternatives].
tier: π              # φ (seed), π (structure), e (current), i (deep)
version: 1.0         # Track evolution
dependencies: []     # List required skills, empty if none
morpheme: π          # Memory architecture tier
composition: false   # true if this orchestrates other skills
---

# Skill Name

Brief tagline or one-sentence identity.

## Core Identity

[What this skill fundamentally does]
[Core philosophy or approach]
[What makes it distinct]

**Philosophy**: [Optional one-liner about approach]

**Tier**: [φ/π/e/i] - [Brief explanation of why this tier]

## When to Use

Invoke this skill when:
- [Specific scenario 1]
- [Specific scenario 2]
- [Specific scenario 3]

Do NOT use this skill for:
- [Common confusion point]
- [Better alternative skill for that use case]

## How It Works

### Phase 1: [First Step Name]

[Instructions for first phase]

**If using bash**:
```bash
#!/bin/bash
# Example command or pattern
command --flag argument
```

**If error-prone, add adaptive healer loop (V2)**:
```bash
adaptive_attempt() {
    local operation="$1"
    local max_attempts=3
    local attempt=1
    local strategy="standard"
    
    # Check for learned strategies (V2 feature)
    if [ -f ".claude/brain/error_patterns" ]; then
        local pattern=$(echo "$operation" | git hash-object --stdin)
        strategy=$(grep "^${pattern}|" .claude/brain/error_patterns | \
                   tail -1 | cut -d'|' -f2)
        [ -n "$strategy" ] && echo "💡 Using learned strategy: ${strategy}" >&2
    fi
    
    while [ $attempt -le $max_attempts ]; do
        if eval "$operation" 2>&1 | tee /tmp/attempt_${attempt}.log; then
            echo "✓ Success on attempt $attempt!" >&2
            # Record success for future learning
            [ -n "$pattern" ] && echo "${pattern}|${strategy}|${attempt}|$(date +%s)" >> .claude/brain/error_patterns
            return 0
        fi
        
        # Categorize error and adapt
        local error_type=$(grep -i "error\|failed\|denied" /tmp/attempt_${attempt}.log | head -1)
        case "$error_type" in
            *"permission"*) strategy="chmod_fix"; chmod +x script.sh 2>/dev/null ;;
            *"not found"*)  strategy="fallback_path"; export PATH="$PATH:/usr/local/bin" ;;
            *"locked"*)     strategy="force_unlock"; rm -f *.lock 2>/dev/null ;;
            *)              strategy="retry_backoff" ;;
        esac
        
        echo "⚡ Attempt $attempt/$max_attempts: ${strategy}. Trying again..." >&2
        attempt=$((attempt + 1))
        sleep $((2 ** (attempt - 2)))
    done
    
    echo "💚 Couldn't complete after $max_attempts tries." >&2
    echo "   Last error: $(tail -1 /tmp/attempt_${max_attempts}.log)" >&2
    echo "   You might want to check: [specific suggestions based on error_type]" >&2
    return 1
}
```

### Phase 2: [Second Step Name]

[Instructions for second phase]

### Phase 3: [Third Step Name]

[Instructions for third phase]

## Git-Brain Integration (Optional)

**If this skill needs persistence**, use Git-brain storage with V2 morpheme-aware indexing:

### Initialize Brain Storage

```bash
mkdir -p .claude/brain/skills
touch .claude/brain/INDEX
```

### Store Data with Morpheme

```bash
# V2: Store with tier-aware morpheme
store_data_v2() {
    local key="$1"
    local value="$2"
    local tier="${3:-π}"  # Default to π-tier
    
    # Hash and store
    local hash=$(echo "$value" | git hash-object -w --stdin)
    echo "$hash" > ".claude/brain/${key}"
    
    # Index with morpheme
    echo "${tier}.skill.${key}|${hash}|$(date -Iseconds)" >> .claude/brain/INDEX
    
    echo "✓ Stored ${key} (tier: ${tier})" >&2
}

# Usage
store_data_v2 "mykey" "my data" "π"
```

### Retrieve Data

```bash
# Retrieve by key
retrieve_data() {
    local key="$1"
    if [ -f ".claude/brain/${key}" ]; then
        local hash=$(cat ".claude/brain/${key}")
        git cat-file -p "$hash"
    else
        echo "💚 Key '${key}' not found. Want to create it?" >&2
        return 1
    fi
}

# Usage
DATA=$(retrieve_data "mykey")
```

### Register in Index with Dewey ID

```bash
# V2: Register with morpheme-aware Dewey
register_skill_v2() {
    local skill_name="$1"
    local category="$2"  # 0-9
    local tier="$3"       # φ/π/e/i
    
    # Assign morpheme
    case "$tier" in
        φ) morpheme="φ" ;;
        π) morpheme="π" ;;
        e) morpheme="e" ;;
        i) morpheme="i" ;;
        *) morpheme="" ;;
    esac
    
    # Generate Dewey ID
    local domain=$(($(date +%s) % 10))
    local next=$(grep "^${morpheme}\.${category}\.${domain}\." .claude/brain/INDEX | \
                 wc -l)
    local dewey_id="${morpheme}.${category}.${domain}.$((next + 1))"
    
    echo "${dewey_id}|${skill_name}|tier:${tier}|$(date -Iseconds)" >> .claude/brain/INDEX
    echo "✓ Registered ${skill_name} as ${dewey_id}" >&2
}

# Usage
register_skill_v2 "my-skill" 3 "π"  # Methodology, π-tier
```

**Dewey Categories**:
- 0.x = System/Index
- 1.x = Entities
- 2.x = Theory
- 3.x = Methodology
- 4.x = History
- 5.x = Connections
- 6.x = Research
- 7.x = Applications
- 8.x = Memory
- 9.x = References

## Error Handling

### Trauma-Informed Patterns (V2 Enhanced)

**Don't**:
```bash
echo "ERROR: Operation failed" >&2
echo "FATAL: Invalid input" >&2
echo "CRITICAL: Permission denied" >&2
```

**Do (V2 with learning)**:
```bash
echo "⚡ Operation hit a snag. Let me try a different approach..." >&2
echo "💚 That input isn't quite right. Here's an example: [...]" >&2
echo "🔒 Permission issue detected. Applying learned fix: chmod +x" >&2
```

### Common Error Scenarios with Adaptive Responses

| Error | First Response | Learned Response (V2) | Auto-Fix |
|-------|---------------|---------------------|----------|
| File not found | "💚 Can't find that file..." | "💡 Checked common paths, not there" | Try ~/.local/, /opt/ |
| Permission denied | "🔒 Permission issue..." | "💡 This usually needs +x" | Auto-chmod |
| Command not found | "⚡ Missing tool..." | "💡 Installing via fallback" | Try apt/brew/manual |
| Lock file exists | "🔓 Found a stale lock..." | "💡 This lock is safe to remove" | Auto-rm |
| Network timeout | "⏳ Network hiccup..." | "💡 Using offline cache" | Switch to local |

### Adaptive Retry Pattern (V2)

```bash
retry_with_learning() {
    local operation="$1"
    local max_attempts=3
    
    for attempt in $(seq 1 $max_attempts); do
        # Try operation
        if eval "$operation" 2>&1 | tee /tmp/retry_${attempt}.log; then
            # Success - record it
            echo "✓ Success on attempt $attempt!" >&2
            record_success_pattern "$operation" "$attempt"
            return 0
        fi
        
        # Failure - learn from it
        local error=$(tail -1 /tmp/retry_${attempt}.log)
        apply_learned_fix "$error"
        
        echo "⚡ Attempt $attempt/$max_attempts didn't work. Adapting..." >&2
        sleep $((2 ** (attempt - 1)))
    done
    
    echo "💚 Couldn't complete. Here's what we learned:" >&2
    summarize_attempts /tmp/retry_*.log
    return 1
}
```

## Jank Heuristics (V2 with Learning)

**Known quirks and workarounds** (V2 records these for future use):

### Quirk 1: [Description]

**When it happens**: [Conditions]

**Why it happens**: [Root cause]

**Workaround**:
```bash
# V2: Record quirk for future reference
if [condition]; then
    echo "⚡ Known quirk: [description]. Applying workaround..." >&2
    weird_hack
    # Record that this quirk was encountered
    echo "quirk_1|$(date -Iseconds)|${SKILL_NAME}" >> .claude/brain/quirk_log
fi
```

**Status**: ✓ Intentional jank (works reliably) | ⚠ Known issue (fix if time) | 🔥 Will bite you (beware)

**Learning**: [After 10 encounters, what pattern emerged?]

## Composition (V2 Feature)

**If this skill orchestrates other skills**:

```markdown
### Dependency Management

This skill coordinates:
- `skill-a`: [What it provides]
- `skill-b`: [What it provides]
- `skill-c`: [What it provides]

### Orchestration Pattern

```bash
# V2: Sequential composition with shared context
orchestrate_skills() {
    local context_key="composition_$(date +%s)"
    
    # Store initial context
    store_data_v2 "${context_key}_input" "$1" "e"
    
    # Run skill A
    echo "🔄 Running skill-a..." >&2
    result_a=$(run_skill "skill-a" "$(retrieve_data "${context_key}_input")")
    store_data_v2 "${context_key}_a" "$result_a" "e"
    
    # Run skill B with A's output
    echo "🔄 Running skill-b..." >&2
    result_b=$(run_skill "skill-b" "$result_a")
    store_data_v2 "${context_key}_b" "$result_b" "e"
    
    # Run skill C with B's output
    echo "🔄 Running skill-c..." >&2
    result_c=$(run_skill "skill-c" "$result_b")
    
    # Cleanup temp context
    rm -f .claude/brain/${context_key}_*
    
    echo "$result_c"
}
```

### Fallback Handling

If a composed skill isn't available:

```bash
# V2: Graceful degradation
run_skill_with_fallback() {
    local skill="$1"
    local input="$2"
    
    if skill_exists "$skill"; then
        run_skill "$skill" "$input"
    else
        echo "⚡ ${skill} not available, using fallback..." >&2
        fallback_implementation "$input"
    fi
}
```

## Examples

### Example 1: [Simple Use Case]

**Scenario**: [What the user wants to do]

**Input**: 
```
[What the user provides]
```

**Process**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Output**:
```
[What gets generated or returned]
```

**V2 Learning**: [If this example was generated from learned patterns, note that]

### Example 2: [Complex Use Case]

**Scenario**: [What the user wants to do]

**Input**:
```
[What the user provides]
```

**Process**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Output**:
```
[What gets generated or returned]
```

### Example 3: [Edge Case with Adaptation]

**Scenario**: [Unusual or tricky situation]

**Initial Approach**: [What was tried first]

**Adaptation**: [How V2 learned and adjusted]

**Final Solution**:
```bash
# V2: Adaptive solution based on learned patterns
if [edge_condition]; then
    echo "💡 Seen this edge case before, using learned approach..." >&2
    apply_learned_solution "$edge_condition"
fi
```

## Integration with Other Skills

**Coordinates with**:
- `skill-a` — [How they work together]
- `skill-b` — [Complementary usage]

**Distinct from**:
- `skill-c` — [Key difference: when to use this instead]
- `skill-d` — [Key difference: when to use that instead]

**Depends on** (V2 explicit):
- `skill-e` — [Required, skill won't work without it]
- `skill-f` (optional) — [Enhances functionality if available]

**Composes with** (V2):
- `skill-g + skill-h` → meta-skill pattern
- `skill-i` as pre-processor

## Autopoietic Hooks (V2 Feature)

**If this skill can improve itself**:

### Usage Tracking

```bash
# V2: Record each invocation
record_usage() {
    local context="$1"
    echo "$(date -Iseconds)|${SKILL_NAME}|${context}" >> .claude/brain/usage_log
}

# Call at skill invocation
record_usage "user_requested_X"
```

### Pattern Detection

```bash
# V2: Flag if novel patterns emerge during execution
detect_emergence() {
    local pattern="$1"
    if ! grep -q "$pattern" .claude/brain/known_patterns 2>/dev/null; then
        echo "🔥 EMERGENCE: Novel pattern detected: ${pattern}" >&2
        echo "${pattern}|${SKILL_NAME}|$(date -Iseconds)" >> .claude/brain/novel_patterns
        return 0
    fi
    return 1
}

# Call when unexpected patterns occur
detect_emergence "new_error_handling_approach"
```

### Self-Improvement Trigger

```bash
# V2: Suggest when skill should evolve
check_evolution_readiness() {
    local usage_count=$(grep "|${SKILL_NAME}|" .claude/brain/usage_log | wc -l)
    local novel_patterns=$(grep "|${SKILL_NAME}|" .claude/brain/novel_patterns | wc -l)
    
    if [ "$usage_count" -gt 50 ] && [ "$novel_patterns" -gt 3 ]; then
        echo "🎯 ${SKILL_NAME} is ready for v2 evolution!" >&2
        echo "   Usage: $usage_count, Novel patterns: $novel_patterns" >&2
        return 0
    fi
    return 1
}

# Call periodically
check_evolution_readiness
```

## Progressive Disclosure (V2 Optimized)

**Main SKILL.md should be <[tier-specific-limit] lines**.

Tier limits:
- φ-tier: <100 lines
- π-tier: <200 lines
- e-tier: <300 lines
- i-tier: <400 lines (orchestrator only)

### Supporting Documentation

- `references/deep-dive.md` — Detailed explanations and theory
- `references/examples.md` — Extended examples and use cases
- `patterns/common-operations.md` — Reusable code patterns
- `scripts/helper.sh` — Bash utilities (if complex logic)

**V2 Auto-Cross-Linking**:
This skill references: [Auto-generated based on `@skill-name` mentions]

**Loading hint for Claude**:
```markdown
For implementation details, see:
- `references/deep-dive.md`
- `patterns/common-operations.md`
```

## Testing / Validation (V2 with Learning)

**If skill generates files or code**, include validation:

### Automated Testing

```bash
# V2: Test with result recording
test_skill_functionality() {
    local test_name="$1"
    local input="$2"
    local expected="$3"
    
    echo "Testing: $test_name..." >&2
    local result=$(skill_function "$input")
    
    if [ "$result" = "$expected" ]; then
        echo "✓ Test passed: $test_name" >&2
        echo "pass|$test_name|$(date -Iseconds)" >> .claude/brain/test_log
        return 0
    else
        echo "⚡ Test failed: $test_name" >&2
        echo "   Expected: $expected" >&2
        echo "   Got: $result" >&2
        echo "fail|$test_name|$(date -Iseconds)" >> .claude/brain/test_log
        return 1
    fi
}

# Run test suite
test_skill_functionality "test_1" "input1" "output1"
test_skill_functionality "test_2" "input2" "output2"
```

### Validation Checklist

Before considering output complete:
- [ ] [Validation criterion 1]
- [ ] [Validation criterion 2]
- [ ] [Validation criterion 3]
- [ ] [V2: Usage recorded]
- [ ] [V2: Patterns checked for novelty]

## Maintenance Notes

**For future updates**:

### Known Limitations

- [Limitation 1]: [Why it exists, when to fix]
- [Limitation 2]: [Why it exists, when to fix]

### Future Improvements (V2 Tracked)

- [ ] [Enhancement 1] — Priority: [High/Med/Low]
- [ ] [Enhancement 2] — Triggered when: [Condition]
- [ ] [Enhancement 3] — Depends on: [Other skill/feature]

### Dependencies

**Required**:
- bash (4.0+)
- git (2.0+)
- [other requirements]

**Optional (V2 Enhanced)**:
- jq (for JSON parsing, falls back to python/grep)
- [other optional tools with fallbacks]

### Evolution History (V2)

**V1.0** — Initial creation  
**V2.0** — [Date] - [Major changes]  
**V3.0** — [Planned] - [Anticipated improvements]

## Red Flags

**You're using this skill wrong if**:
- [Misuse pattern 1]
- [Misuse pattern 2]
- [Misuse pattern 3]

**You're using this skill right if**:
- [Correct usage pattern 1]
- [Correct usage pattern 2]
- [Correct usage pattern 3]

## Meta-Notes

[Any additional context about the skill]
[Design decisions or philosophy]
[Relation to other patterns in the ecosystem]

**V2 Enhancements Applied**:
- ✓ Adaptive error handling with learning
- ✓ Morpheme-aware Git-brain integration
- ✓ Usage tracking for autopoietic evolution
- ✓ Pattern emergence detection
- ✓ [Tier]-specific optimizations
- ✓ Composition support (if applicable)

---

**Template version**: 2.0  
**Generated by**: gremlin-jank-builder-v2  
**Last updated**: [Date]  
**Tier**: [φ/π/e/i]
