#!/bin/bash
# Record successful chaos discovery to Git-brain
# Usage: ./record-discovery.sh --problem-type <type> --chaos-level <level> --generators <G1,G2,...> --success <true|false>

set -e

# Initialize Git-brain if needed
init_git_brain() {
    mkdir -p .claude/brain
    [ ! -f .claude/brain/INDEX ] && touch .claude/brain/INDEX
    [ ! -f .claude/brain/chaos_discoveries ] && touch .claude/brain/chaos_discoveries
    [ ! -f .claude/brain/generator_matches ] && touch .claude/brain/generator_matches
    [ ! -f .claude/brain/emergence_events ] && touch .claude/brain/emergence_events
    [ ! -f .claude/brain/success_rates ] && touch .claude/brain/success_rates
    [ ! -f .claude/brain/trauma_log ] && touch .claude/brain/trauma_log
}

# Parse arguments
problem_type=""
chaos_level=""
solution_code=""
generators=""
success="true"
context=""
severity="LOW"
failure_mode=""
dokkado_phase=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --problem-type|--problem|--type) problem_type="$2"; shift 2;;
        --chaos-level|--level) chaos_level="$2"; shift 2;;
        --solution) solution_code="$2"; shift 2;;
        --generators|--gen) generators="$2"; shift 2;;
        --success) success="$2"; shift 2;;
        --context) context="$2"; shift 2;;
        --severity) severity="$2"; shift 2;;
        --failure-mode|--failure) failure_mode="$2"; shift 2;;
        --dokkado-phase|--dokkado) dokkado_phase="$2"; shift 2;;
        --help)
            echo "Usage: record-discovery.sh [options]"
            echo "Required:"
            echo "  --problem-type <type>        Problem category"
            echo "  --chaos-level <1-4>          Chaos level used"
            echo "  --generators <G1,G2,...>     Generator matches"
            echo "Optional:"
            echo "  --solution <code>            Solution code to store"
            echo "  --success <true|false>       Whether chaos succeeded (default: true)"
            echo "  --context <context>          Additional context"
            echo "  --severity <LOW|MEDIUM|HIGH|CRITICAL>  Failure severity"
            echo "  --failure-mode <mode>        How it failed (for failures)"
            echo "  --dokkado-phase <phase>      Dokkado phase if applicable"
            exit 0
            ;;
        *) shift;;
    esac
done

# Validate required arguments
if [ -z "$problem_type" ] || [ -z "$chaos_level" ]; then
    echo "Error: --problem-type and --chaos-level are required" >&2
    echo "Run with --help for usage" >&2
    exit 1
fi

# Initialize Git-brain
init_git_brain

# Generate problem hash
problem_hash=$(echo "$problem_type" | md5sum | cut -d' ' -f1 | cut -c1-6)

# Store solution in Git if provided
solution_hash="NONE"
if [ -n "$solution_code" ]; then
    solution_hash=$(git hash-object -w --stdin <<< "$solution_code" 2>/dev/null || echo "FAILED")
    if [ "$solution_hash" != "FAILED" ]; then
        echo "π.3.4.2|chaos-discovery|${problem_type}|${solution_hash}" >> .claude/brain/INDEX
    fi
fi

# Record in chaos_discoveries
timestamp=$(date -Iseconds 2>/dev/null || date +"%Y-%m-%dT%H:%M:%S")
echo "${problem_hash}|${chaos_level}|${solution_hash}|${success}|${generators}|${timestamp}|${problem_type}" \
    >> .claude/brain/chaos_discoveries

# If success, record generator matches
if [ "$success" = "true" ] && [ -n "$generators" ]; then
    generator_count=$(echo "$generators" | tr ',' '\n' | grep -c 'G' || echo "0")
    
    if [ $generator_count -ge 6 ]; then
        significance="VERY_HIGH"
    elif [ $generator_count -ge 4 ]; then
        significance="HIGH"
    elif [ $generator_count -ge 3 ]; then
        significance="MEDIUM"
    else
        significance="LOW"
    fi
    
    pattern_id="${problem_type}_${problem_hash}"
    echo "${pattern_id}|${generators}|${generator_count}|${significance}|${timestamp}|${problem_type}" \
        >> .claude/brain/generator_matches
    
    # Check for emergence (4+ generators)
    if [ $generator_count -ge 4 ]; then
        description="Chaos discovery in ${problem_type} matched ${generator_count}/7 generators"
        [ -n "$dokkado_phase" ] && description="${description} (Dokkado ${dokkado_phase})"
        
        echo "${timestamp}|EMERGENCE|${generator_count}|${pattern_id}|${generators}|${context}|${description}" \
            >> .claude/brain/emergence_events
        
        echo "🔥 EMERGENCE EVENT recorded: ${generator_count}/7 generators matched"
    fi
fi

# If critical failure, add to trauma log
if [ "$success" = "false" ] && [ "$severity" = "CRITICAL" ]; then
    echo "${problem_type}|${chaos_level}|${failure_mode}|${severity}|${timestamp}|Recorded automatically" \
        >> .claude/brain/trauma_log
    
    echo "⚠️ CRITICAL FAILURE recorded in trauma log"
    echo "   Future chaos for ${problem_type} at level ${chaos_level} will be flagged"
fi

# Output confirmation
echo "✓ Discovery recorded:"
echo "  Problem: ${problem_type}"
echo "  Level: ${chaos_level}"
echo "  Success: ${success}"
if [ -n "$generators" ]; then
    echo "  Generators: ${generators}"
fi
if [ "$solution_hash" != "NONE" ] && [ "$solution_hash" != "FAILED" ]; then
    echo "  Solution: ${solution_hash}"
fi

# Update success rates (simplified aggregation)
update_success_rates() {
    # This would be more complex in production - for now just touch the file to indicate update needed
    touch .claude/brain/success_rates.needs_update
}

update_success_rates

echo ""
echo "Use 'git cat-file -p ${solution_hash}' to retrieve solution" 2>/dev/null || true
