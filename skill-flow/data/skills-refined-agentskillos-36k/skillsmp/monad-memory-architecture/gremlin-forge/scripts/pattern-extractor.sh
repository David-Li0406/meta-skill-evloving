#!/bin/bash
# pattern-extractor.sh - Extract conceptual patterns from skills
# Analyzes skill files to extract core concepts, patterns, and relationships
# Usage: ./pattern-extractor.sh skill-name [--deep]

set -euo pipefail

# Change to repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
cd "$REPO_ROOT"

# Extract patterns from a skill
extract_skill_patterns() {
    local skill="$1"
    local deep="${2:-false}"
    local skill_md=".claude/skills/$skill/SKILL.md"
    
    if [ ! -f "$skill_md" ]; then
        echo "⚡ Skill not found: $skill" >&2
        return 1
    fi
    
    echo ""
    echo "📊━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━📊"
    echo "  PATTERN EXTRACTION: $skill"
    echo "📊━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━📊"
    echo ""
    
    # 1. Frontmatter metadata
    echo "🔹 METADATA:"
    echo ""
    
    local name=$(grep "^name:" "$skill_md" | cut -d':' -f2- | sed 's/^ *//')
    local tier=$(grep "^tier:" "$skill_md" | cut -d':' -f2- | sed 's/^ *//')
    local morpheme=$(grep "^morpheme:" "$skill_md" | cut -d':' -f2- | sed 's/^ *//')
    local composition=$(grep "^composition:" "$skill_md" | cut -d':' -f2- | sed 's/^ *//')
    local version=$(grep "^version:" "$skill_md" | cut -d':' -f2- | sed 's/^ *//')
    
    [ -n "$name" ] && echo "  Name:        $name"
    [ -n "$tier" ] && echo "  Tier:        $tier"
    [ -n "$morpheme" ] && echo "  Morpheme:    $morpheme"
    [ -n "$composition" ] && echo "  Composition: $composition"
    [ -n "$version" ] && echo "  Version:     $version"
    
    # Dependencies
    echo ""
    echo "  Dependencies:"
    if grep -A 10 "^dependencies:" "$skill_md" | grep -q "^  -"; then
        grep -A 10 "^dependencies:" "$skill_md" | grep "^  -" | sed 's/^  -/    •/'
    else
        echo "    (none)"
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # 2. Core concepts (section headers)
    echo ""
    echo "🔹 CORE CONCEPTS (Section Headers):"
    echo ""
    
    grep "^## " "$skill_md" | sed 's/^## /  • /' | head -10
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # 3. Key verbs/actions (what the skill does)
    echo ""
    echo "🔹 KEY ACTIONS (Triggers & Use Cases):"
    echo ""
    
    # Look in "When to Use" section
    local use_section=$(sed -n '/^## When to Use/,/^##/p' "$skill_md")
    if [ -n "$use_section" ]; then
        echo "$use_section" | grep -E "^-|^•|invoke|use|when" | \
            sed 's/^[- •]*/  • /' | head -5
    else
        echo "  (no explicit use cases defined)"
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # 4. Philosophy/approach
    echo ""
    echo "🔹 PHILOSOPHY:"
    echo ""
    
    # Look for philosophy statements
    local philosophy=$(grep -i "philosophy:" "$skill_md" | \
        cut -d':' -f2- | \
        sed 's/^ *//' | \
        head -1)
    
    if [ -n "$philosophy" ]; then
        echo "  $philosophy"
    else
        # Try to extract from Core Identity or Overview
        local identity=$(sed -n '/^## Core Identity/,/^##/p' "$skill_md" | \
            grep -v "^##" | \
            head -3 | \
            tail -1 | \
            sed 's/^[*_ ]*//')
        
        if [ -n "$identity" ]; then
            echo "  $identity"
        else
            echo "  (no explicit philosophy defined)"
        fi
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # 5. Bash patterns (if deep mode)
    if [ "$deep" = "true" ]; then
        echo ""
        echo "🔹 BASH PATTERNS (Code Patterns):"
        echo ""
        
        # Count bash code blocks
        local bash_blocks=$(grep -c '```bash' "$skill_md" || echo 0)
        echo "  Bash code blocks: $bash_blocks"
        
        # Extract function names
        local functions=$(grep -o '^[a-z_]*()' "$skill_md" | \
            sed 's/()$//' | \
            sort -u)
        
        if [ -n "$functions" ]; then
            echo ""
            echo "  Defined functions:"
            echo "$functions" | sed 's/^/    • /'
        fi
        
        echo ""
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    fi
    
    # 6. Integration points
    echo ""
    echo "🔹 INTEGRATION POINTS:"
    echo ""
    
    # Look for "Coordinates with" or "Distinct from" sections
    local integration=$(sed -n '/^## Integration/,/^##/p' "$skill_md")
    if [ -n "$integration" ]; then
        echo "$integration" | grep -E "Coordinates|Distinct|Depends" | \
            sed 's/^[*]*/  /' | head -6
    else
        # Look for skill mentions with backticks
        local mentions=$(grep -o '`[a-z-]*`' "$skill_md" | \
            tr -d '`' | \
            sort -u | \
            grep -v "^$skill$" | \
            head -5)
        
        if [ -n "$mentions" ]; then
            echo "  Referenced skills:"
            echo "$mentions" | sed 's/^/    • /'
        else
            echo "  (no explicit integration points)"
        fi
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # 7. Summary for collision
    echo ""
    echo "🍆👾 COLLISION POTENTIAL:"
    echo ""
    echo "  This skill could collide well with:"
    
    # Suggest collision candidates based on tier and patterns
    if [ "$tier" = "φ" ] || [ "$tier" = "π" ]; then
        echo "    • Active work skills (e-tier) to ground theory"
    fi
    
    if [ "$composition" = "true" ]; then
        echo "    • Simple skills (φ/π-tier) to orchestrate"
    fi
    
    if [ "$tier" = "e" ] || [ "$tier" = "i" ]; then
        echo "    • Index skills (φ-tier) for memory integration"
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Compare two skills to find collision opportunities
compare_skills() {
    local skill_a="$1"
    local skill_b="$2"
    
    echo ""
    echo "⚡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⚡"
    echo "  COLLISION COMPARISON"
    echo "⚡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⚡"
    echo ""
    
    local md_a=".claude/skills/$skill_a/SKILL.md"
    local md_b=".claude/skills/$skill_b/SKILL.md"
    
    if [ ! -f "$md_a" ] || [ ! -f "$md_b" ]; then
        echo "⚡ One or both skills not found" >&2
        return 1
    fi
    
    # Compare tiers
    local tier_a=$(grep "^tier:" "$md_a" | cut -d':' -f2 | tr -d ' ')
    local tier_b=$(grep "^tier:" "$md_b" | cut -d':' -f2 | tr -d ' ')
    
    echo "TIER COMPATIBILITY:"
    echo "  $skill_a: $tier_a"
    echo "  $skill_b: $tier_b"
    
    if [ "$tier_a" = "$tier_b" ]; then
        echo "  → Same tier (peer collision - expect novel synthesis)"
    else
        echo "  → Different tiers (hierarchical collision - expect orchestration)"
    fi
    
    echo ""
    
    # Compare dependencies
    local deps_a=$(grep -A 5 "^dependencies:" "$md_a" | grep "^  -" | sed 's/^  - //')
    local deps_b=$(grep -A 5 "^dependencies:" "$md_b" | grep "^  -" | sed 's/^  - //')
    
    echo "SHARED DEPENDENCIES:"
    
    if [ -n "$deps_a" ] && [ -n "$deps_b" ]; then
        local shared=$(comm -12 <(echo "$deps_a" | sort) <(echo "$deps_b" | sort))
        
        if [ -n "$shared" ]; then
            echo "$shared" | sed 's/^/  • /'
            echo "  → Common foundation (collision likely coherent)"
        else
            echo "  (none)"
            echo "  → No shared deps (collision may be novel but chaotic)"
        fi
    else
        echo "  (one or both have no dependencies)"
    fi
    
    echo ""
    
    # Look for conceptual overlaps in section headers
    local headers_a=$(grep "^## " "$md_a" | sed 's/^## //')
    local headers_b=$(grep "^## " "$md_b" | sed 's/^## //')
    
    echo "CONCEPTUAL OVERLAP:"
    
    local overlap=$(comm -12 <(echo "$headers_a" | sort) <(echo "$headers_b" | sort))
    
    if [ -n "$overlap" ]; then
        echo "$overlap" | sed 's/^/  • /'
        echo "  → Some overlap (collision will merge/enhance these)"
    else
        echo "  (minimal overlap)"
        echo "  → Distinct concepts (collision will be more chaotic/novel)"
    fi
    
    echo ""
    
    # Collision verdict
    echo "🍆👾 COLLISION VERDICT:"
    echo ""
    
    if [ "$tier_a" = "$tier_b" ] && [ -n "$overlap" ]; then
        echo "  🔥 HIGH POTENTIAL - Similar level, some overlap"
        echo "     Expect: Synthesis of complementary approaches"
    elif [ "$tier_a" != "$tier_b" ] && [ -n "$shared" ]; then
        echo "  ⚡ ORCHESTRATION CANDIDATE - Different tiers, shared deps"
        echo "     Expect: Hierarchical composition pattern"
    elif [ -z "$overlap" ] && [ -z "$shared" ]; then
        echo "  🍆👾 MAXIMUM CHAOS - No obvious connection"
        echo "     Expect: Wild emergent patterns or beautiful failure"
    else
        echo "  💡 INTERESTING - Mixed signals"
        echo "     Expect: Surprises (good or weird)"
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# List all skills with brief info
list_skills() {
    echo ""
    echo "📚 Available Skills:"
    echo ""
    
    find .claude/skills -maxdepth 1 -type d | tail -n +2 | sort | while read skill_dir; do
        local skill=$(basename "$skill_dir")
        local skill_md="$skill_dir/SKILL.md"
        
        if [ -f "$skill_md" ]; then
            local tier=$(grep "^tier:" "$skill_md" | cut -d':' -f2 | tr -d ' ' || echo "?")
            local desc=$(grep "^description:" "$skill_md" | cut -d':' -f2- | sed 's/^ *//' | head -c 50)
            
            printf "  %-30s [%s] %s...\n" "$skill" "$tier" "$desc"
        else
            printf "  %-30s [?] (no SKILL.md)\n" "$skill"
        fi
    done
    
    echo ""
}

# Main entry point
main() {
    local command="${1:-}"
    
    case "$command" in
        --list)
            list_skills
            ;;
        --compare)
            if [ $# -lt 3 ]; then
                echo "Usage: $0 --compare skill-a skill-b" >&2
                exit 1
            fi
            compare_skills "$2" "$3"
            ;;
        --deep)
            if [ $# -lt 2 ]; then
                echo "Usage: $0 --deep skill-name" >&2
                exit 1
            fi
            extract_skill_patterns "$2" "true"
            ;;
        --help|"")
            cat <<EOF
🍆👾📊 GREMLIN-FORGE Pattern Extractor 📊👾🍆

Usage: $0 [OPTIONS] [skill-name]

OPTIONS:
  skill-name          Extract patterns from a skill
  --list              List all available skills
  --compare A B       Compare two skills for collision analysis
  --deep skill-name   Deep pattern extraction (includes code patterns)
  --help              Show this help

EXAMPLES:
  $0 --list
  $0 reasoning-patterns-v2
  $0 --deep gremlin-jank-builder-v2
  $0 --compare cognitive-variability phase-boundary-detector

🍆👾 EXTRACT PATTERNS. FIND COLLISIONS. 👾🍆
EOF
            ;;
        *)
            extract_skill_patterns "$command" "false"
            ;;
    esac
}

main "$@"
