#!/bin/bash
# Check safety constraints for chaos level in given context
# Usage: ./chaos-safe.sh --level <1-4> --env <environment> --problem <type>

set -e

# Parse arguments
chaos_level=""
environment="development"
problem_type=""
check_trauma="true"

while [[ $# -gt 0 ]]; do
    case $1 in
        --level|--chaos-level) chaos_level="$2"; shift 2;;
        --env|--environment) environment="$2"; shift 2;;
        --problem|--problem-type|--type) problem_type="$2"; shift 2;;
        --no-trauma-check) check_trauma="false"; shift;;
        --help)
            echo "Usage: chaos-safe.sh [options]"
            echo "Required:"
            echo "  --level <1-4>               Chaos level to check"
            echo "Optional:"
            echo "  --env <environment>         Environment context"
            echo "  --problem <type>            Problem type"
            echo "  --no-trauma-check           Skip trauma log check"
            exit 0
            ;;
        *) shift;;
    esac
done

# Validate
if [ -z "$chaos_level" ]; then
    echo "Error: --level is required" >&2
    exit 1
fi

# Check if level is valid
if [ "$chaos_level" -lt 1 ] || [ "$chaos_level" -gt 4 ]; then
    echo "❌ INVALID: Chaos level must be 1-4" >&2
    exit 1
fi

# Initialize safety check result
safe="true"
warnings=""
hard_limit=""

# Hard constraint: Security contexts must be Level 1
if [ "$environment" = "security" ]; then
    if [ "$chaos_level" -gt 1 ]; then
        safe="false"
        hard_limit="Security contexts require Level 1 maximum"
        echo "🛑 HARD CONSTRAINT VIOLATION" >&2
        echo "   Environment: security" >&2
        echo "   Requested: Level $chaos_level" >&2
        echo "   Maximum: Level 1" >&2
        echo "" >&2
        echo "   Reason: Edge cases in security code can become vulnerabilities" >&2
    fi
fi

# Hard constraint: Production contexts capped at Level 2
if [ "$environment" = "production" ]; then
    if [ "$chaos_level" -gt 2 ]; then
        safe="false"
        hard_limit="Production contexts require Level 2 maximum"
        echo "⚠️ HARD CONSTRAINT VIOLATION" >&2
        echo "   Environment: production" >&2
        echo "   Requested: Level $chaos_level" >&2
        echo "   Maximum: Level 2" >&2
        echo "" >&2
        echo "   Reason: High chaos in production risks maintainability" >&2
    fi
fi

# Hard constraint: Educational contexts capped at Level 3
if [ "$environment" = "educational" ]; then
    if [ "$chaos_level" -gt 3 ]; then
        warnings="${warnings}\n⚠️  Educational context: Level 4 may confuse learners"
    fi
fi

# Check trauma log if enabled and problem type provided
if [ "$check_trauma" = "true" ] && [ -n "$problem_type" ]; then
    if [ -f .claude/brain/trauma_log ]; then
        trauma=$(grep "^${problem_type}|${chaos_level}|" .claude/brain/trauma_log 2>/dev/null || true)
        
        if [ -n "$trauma" ]; then
            severity=$(echo "$trauma" | cut -d'|' -f4)
            failure_mode=$(echo "$trauma" | cut -d'|' -f3)
            
            if [ "$severity" = "CRITICAL" ]; then
                safe="false"
                echo "⚠️ TRAUMA WARNING: CRITICAL failure history" >&2
                echo "   Problem: $problem_type" >&2
                echo "   Level: $chaos_level" >&2
                echo "   Previous failure: $failure_mode" >&2
                echo "" >&2
                echo "   This combination has caused critical issues before." >&2
                echo "   Strongly recommend Level 1 or conventional approach." >&2
            else
                warnings="${warnings}\n⚠️  Trauma detected: ${severity} failure in ${problem_type} at Level ${chaos_level}"
            fi
        fi
    fi
fi

# Check for specific dangerous combinations
if [ "$problem_type" = "auth_validation" ] || [ "$problem_type" = "authentication" ]; then
    if [ "$chaos_level" -gt 1 ]; then
        warnings="${warnings}\n⚠️  Authentication code: Recommend Level 1 only"
    fi
fi

if [ "$problem_type" = "crypto" ] || [ "$problem_type" = "cryptography" ]; then
    if [ "$chaos_level" -gt 1 ]; then
        warnings="${warnings}\n⚠️  Cryptography: Strongly recommend conventional approaches"
    fi
fi

if [ "$problem_type" = "data_integrity" ] || [ "$problem_type" = "database" ]; then
    if [ "$chaos_level" -gt 2 ]; then
        warnings="${warnings}\n⚠️  Data operations: High chaos risks data loss"
    fi
fi

# Output result
if [ "$safe" = "true" ] && [ -z "$warnings" ]; then
    echo "✓ SAFE: Level $chaos_level approved for $environment environment"
    if [ -n "$problem_type" ]; then
        echo "  Problem type: $problem_type"
    fi
    exit 0
else
    if [ "$safe" = "false" ]; then
        echo "❌ UNSAFE: Level $chaos_level NOT approved" >&2
        if [ -n "$hard_limit" ]; then
            echo "  $hard_limit" >&2
        fi
        if [ -n "$warnings" ]; then
            echo -e "$warnings" >&2
        fi
        exit 1
    else
        echo "⚠️  WARNINGS for Level $chaos_level:" >&2
        echo -e "$warnings" >&2
        echo "" >&2
        echo "Proceed with caution. Consider lower chaos level." >&2
        exit 2  # Warning but not blocking
    fi
fi
