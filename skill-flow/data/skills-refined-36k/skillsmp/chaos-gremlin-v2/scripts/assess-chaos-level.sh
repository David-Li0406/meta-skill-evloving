#!/bin/bash
# Assess appropriate chaos level based on context
# Usage: ./assess-chaos-level.sh --env production --expertise senior --pattern high --problem recursion --stakes significant

set -e

# Default values
environment="development"
expertise="intermediate"
pattern_potential="medium"
problem_type=""
stakes="low"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --env|--environment) environment="$2"; shift 2;;
        --expertise|--exp) expertise="$2"; shift 2;;
        --pattern|--potential) pattern_potential="$2"; shift 2;;
        --problem|--type) problem_type="$2"; shift 2;;
        --stakes) stakes="$2"; shift 2;;
        --help) 
            echo "Usage: assess-chaos-level.sh [options]"
            echo "Options:"
            echo "  --env <production|staging|development|educational|experimental|security>"
            echo "  --expertise <beginner|intermediate|senior|expert>"
            echo "  --pattern <low|medium|high|very_high>"
            echo "  --problem <problem_type>"
            echo "  --stakes <catastrophic|critical|significant|low|none>"
            exit 0
            ;;
        *) shift;;
    esac
done

# Base level
level=2

# Environment modifier
case "$environment" in
    production) level=$((level - 1));;
    staging) level=$((level + 0));;
    development) level=$((level + 1));;
    educational) level=$((level + 0));;
    experimental) level=$((level + 2));;
    security) level=1; echo "⚠️ Security context: Chaos hard-limited to Level 1" >&2;;
esac

# Expertise modifier
case "$expertise" in
    beginner) level=$((level - 1));;
    intermediate) level=$((level + 0));;
    senior) level=$((level + 1));;
    expert) level=$((level + 2));;
esac

# Pattern potential modifier
case "$pattern_potential" in
    low) level=$((level - 1));;
    medium) level=$((level + 0));;
    high) level=$((level + 1));;
    very_high) level=$((level + 2));;
esac

# Historical success check (if problem_type provided and database exists)
if [ -n "$problem_type" ] && [ -f .claude/brain/chaos_discoveries ]; then
    success_count=$(grep "$problem_type.*|true|" .claude/brain/chaos_discoveries 2>/dev/null | wc -l || echo "0")
    total_count=$(grep "$problem_type" .claude/brain/chaos_discoveries 2>/dev/null | wc -l || echo "0")
    
    if [ "$total_count" -gt 0 ]; then
        success_rate=$((success_count * 100 / total_count))
        
        if [ "$success_rate" -gt 70 ]; then
            level=$((level + 1))
            echo "📊 Historical: Chaos works well ($success_rate%) for $problem_type" >&2
        elif [ "$success_rate" -lt 40 ]; then
            level=$((level - 1))
            echo "📊 Historical: Conventional preferred ($success_rate%) for $problem_type" >&2
        else
            echo "📊 Historical: Mixed results ($success_rate%) for $problem_type" >&2
        fi
    else
        echo "📊 No historical data for $problem_type" >&2
    fi
fi

# Stakes modifier
case "$stakes" in
    catastrophic) level=$((level - 3));;
    critical) level=$((level - 2));;
    significant) level=$((level - 1));;
    low) level=$((level + 0));;
    none) level=$((level + 1));;
esac

# Apply hard caps
if [ "$environment" = "security" ]; then
    level=1
elif [ "$environment" = "production" ]; then
    [ $level -gt 2 ] && level=2
elif [ "$environment" = "educational" ]; then
    [ $level -gt 3 ] && level=3
fi

# Clamp to valid range [1, 4]
[ $level -lt 1 ] && level=1
[ $level -gt 4 ] && level=4

# Output recommended level
echo "$level"

# Optional: Output reasoning if verbose
if [ -n "$VERBOSE" ]; then
    echo "" >&2
    echo "Context Assessment:" >&2
    echo "  Environment: $environment" >&2
    echo "  Expertise: $expertise" >&2
    echo "  Pattern Potential: $pattern_potential" >&2
    echo "  Problem Type: ${problem_type:-N/A}" >&2
    echo "  Stakes: $stakes" >&2
    echo "" >&2
    echo "Recommended Chaos Level: $level" >&2
fi
