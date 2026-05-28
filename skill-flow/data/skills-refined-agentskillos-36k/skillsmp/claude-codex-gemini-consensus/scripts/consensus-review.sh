#!/usr/bin/env bash
# consensus-review.sh - Submit code/plan to Codex and Gemini for critical review
# Usage: ./consensus-review.sh <plan|code> <file_or_text>

set -euo pipefail

MODE="${1:-}"
INPUT="${2:-}"

if [[ -z "$MODE" ]] || [[ -z "$INPUT" ]]; then
    echo "Usage: $0 <plan|code> <file_path_or_text>"
    echo ""
    echo "Examples:"
    echo "  $0 plan implementation_plan.md"
    echo "  $0 code src/analysis.py"
    echo "  $0 plan 'Build a REST API for patient data'"
    exit 1
fi

# Determine if input is a file or text
if [[ -f "$INPUT" ]]; then
    CONTENT=$(cat "$INPUT")
    echo "📄 Reading from file: $INPUT"
else
    CONTENT="$INPUT"
    echo "📝 Using provided text"
fi

# Build the review prompt based on mode
if [[ "$MODE" == "plan" ]]; then
    PROMPT="Review this implementation plan critically for a clinical research application.

REQUIRED CHECKS:
1. Logical correctness and completeness
2. Edge cases and error conditions  
3. Security vulnerabilities
4. Performance implications
5. Maintainability and readability
6. Compliance with medical/research standards

BE CRITICAL. ARGUE AGAINST WEAK POINTS. DO NOT APPROVE BLINDLY.

Plan:
$CONTENT"

elif [[ "$MODE" == "code" ]]; then
    PROMPT="Critically review this code for a clinical research application.

REQUIRED CHECKS:
1. Correctness: Does it do what it claims?
2. Edge cases: Are all inputs handled?
3. Error handling: Are failures graceful?
4. Security: Any vulnerabilities?
5. Performance: Any bottlenecks?
6. Documentation: Is intent clear?
7. Tests: What tests are needed?

BE HARSH. FIND PROBLEMS. DO NOT APPROVE BLINDLY.

Code:
$CONTENT"

else
    echo "❌ Unknown mode: $MODE (use 'plan' or 'code')"
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "🤖 CODEX REVIEW"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Check if codex is available
if command -v codex &> /dev/null; then
    codex exec --dangerously-bypass-approvals-and-sandbox \
        --model gpt-5.2-codex \
        --skip-git-repo-check \
        "$PROMPT" 2>&1 || echo "⚠️  Codex review failed or not authenticated"
else
    echo "⚠️  Codex CLI not installed. Install with: npm i -g @openai/codex"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "🌟 GEMINI REVIEW"  
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Check if gemini is available
if command -v gemini &> /dev/null; then
    gemini --yolo \
        --model gemini-3-pro-preview \
        -p "$PROMPT" 2>&1 || echo "⚠️  Gemini review failed or not authenticated"
else
    echo "⚠️  Gemini CLI not installed. Install with: npm i -g @google/gemini-cli"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ REVIEWS COMPLETE - Synthesize feedback and reach consensus"
echo "═══════════════════════════════════════════════════════════════"
