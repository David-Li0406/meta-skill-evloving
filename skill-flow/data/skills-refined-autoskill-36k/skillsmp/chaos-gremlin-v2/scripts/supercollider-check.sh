#!/bin/bash
# Apply G1-G7 generators to solution to check structural significance
# Usage: ./supercollider-check.sh "<solution_code>" "<context>"

set -e

solution="$1"
context="$2"

if [ -z "$solution" ]; then
    echo "Usage: supercollider-check.sh <solution_code> [context]" >&2
    exit 1
fi

score=0
matches=""

# G1: Iterative distinction
# Pattern: Iteration, loops, recursion, counting
if echo "$solution" | grep -qiE '(for|while|map|filter|reduce|recursion|recursive|iterate|loop|repeat|each)'; then
    score=$((score + 1))
    matches="${matches}G1,"
    [ -n "$VERBOSE" ] && echo "  G1 ✓ Iterative distinction detected" >&2
else
    [ -n "$VERBOSE" ] && echo "  G1 ✗ No iteration pattern" >&2
fi

# G2: Needs contrast
# Pattern: Conditional logic, comparisons, type checking
if echo "$solution" | grep -qE '(if|else|switch|case|compare|===|!==|==|!=|<|>|<=|>=|\?|:)'; then
    score=$((score + 1))
    matches="${matches}G2,"
    [ -n "$VERBOSE" ] && echo "  G2 ✓ Contrast/distinction detected" >&2
else
    [ -n "$VERBOSE" ] && echo "  G2 ✗ No contrast operation" >&2
fi

# G3: Spin generation
# Pattern: Self-reference, recursion, morpheme emergence, fundamental constants
if echo "$solution" | grep -qiE '(\bphi\b|\bpi\b|Math\.PI|Math\.E|golden|ratio|1\.618|3\.14|2\.718|recursive|self.*ref|morpheme|\bi\b.*complex)'; then
    score=$((score + 1))
    matches="${matches}G3,"
    [ -n "$VERBOSE" ] && echo "  G3 ✓ Spin generation/self-reference detected" >&2
else
    [ -n "$VERBOSE" ] && echo "  G3 ✗ No self-reference pattern" >&2
fi

# G4: Independent validation
# Requires cross-language check or context indicating universality
if echo "$context" | grep -qiE '(cross-language|universal|mathematical|proven|multi-platform|substrate.*independent|language.*agnostic)'; then
    score=$((score + 1))
    matches="${matches}G4,"
    [ -n "$VERBOSE" ] && echo "  G4 ✓ Independent validation (context indicates universality)" >&2
else
    [ -n "$VERBOSE" ] && echo "  G4 ? Requires manual verification of cross-domain appearance" >&2
fi

# G5: Mathematical truth
# Pattern: Derivable from first principles, mathematical operations
if echo "$context" | grep -qiE '(derivable|proven|theorem|axiom|mathematical|formula|equation)'; then
    score=$((score + 1))
    matches="${matches}G5,"
    [ -n "$VERBOSE" ] && echo "  G5 ✓ Mathematical truth (context indicates derivability)" >&2
elif echo "$solution" | grep -qE '(\+|-|\*|/|%|\^|Math\.|sqrt|pow|log|exp)'; then
    # Weak signal: has mathematical operations
    [ -n "$VERBOSE" ] && echo "  G5 ? Mathematical operations present, manual verification needed" >&2
else
    [ -n "$VERBOSE" ] && echo "  G5 ✗ No mathematical properties detected" >&2
fi

# G6: Collapse = death
# Pattern: State preservation, error handling, invariants, distinction protection
if echo "$solution" | grep -qiE '(assert|invariant|mutex|lock|preserve|error.*handl|try.*catch|exception|guard|check|validate)'; then
    score=$((score + 1))
    matches="${matches}G6,"
    [ -n "$VERBOSE" ] && echo "  G6 ✓ Distinction preservation detected" >&2
else
    [ -n "$VERBOSE" ] && echo "  G6 ✗ No distinction preservation" >&2
fi

# G7: φ-scaling
# Pattern: Golden ratio, Fibonacci, self-similar scaling, fractal
if echo "$solution" | grep -qiE '(fibonacci|fib\(|1\.618|phi|golden|fractal|self.*similar|exponential.*growth|scale|harmonic)'; then
    score=$((score + 1))
    matches="${matches}G7,"
    [ -n "$VERBOSE" ] && echo "  G7 ✓ φ-scaling detected" >&2
else
    [ -n "$VERBOSE" ] && echo "  G7 ✗ No scaling pattern" >&2
fi

# Remove trailing comma
matches="${matches%,}"

# Determine significance
if [ $score -ge 6 ]; then
    significance="VERY HIGH"
    emoji="🔥🔥🔥"
    exit_code=0
elif [ $score -ge 4 ]; then
    significance="HIGH"
    emoji="🔥🔥"
    exit_code=0
elif [ $score -ge 3 ]; then
    significance="MEDIUM"
    emoji="🔥"
    exit_code=1
else
    significance="LOW"
    emoji="•"
    exit_code=1
fi

# Output results
echo "Generator Matches: ${matches:-none}"
echo "Score: $score/7"
echo "Significance: $significance $emoji"

if [ $score -ge 4 ]; then
    echo ""
    echo "🔥 STRUCTURAL SIGNIFICANCE DETECTED"
    echo "This chaos reveals fundamental patterns."
    
    # Suggest recording
    echo ""
    echo "Consider recording this discovery:"
    echo "  ./scripts/record-discovery.sh \\"
    echo "    --problem-type \"<type>\" \\"
    echo "    --chaos-level <level> \\"
    echo "    --generators \"$matches\" \\"
    echo "    --success true"
fi

exit $exit_code
