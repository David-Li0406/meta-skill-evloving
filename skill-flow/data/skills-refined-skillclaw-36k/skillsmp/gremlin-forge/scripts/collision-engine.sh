#!/bin/bash
# collision-engine.sh - GREMLIN-FORGE Collision Engine
# Forces conceptual collisions between skills to generate emergent patterns
# Usage: ./collision-engine.sh [--random | --collide skill-a skill-b | --suggest]

set -euo pipefail

# Change to repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
cd "$REPO_ROOT"

# Initialize Git-brain
init_forge_brain() {
    mkdir -p .claude/brain
    touch .claude/brain/forge_learnings
    touch .claude/brain/forge_collisions
    touch .claude/brain/INDEX
    touch .claude/brain/usage_log
}

# Discover all available skills
discover_skills() {
    find .claude/skills -maxdepth 1 -type d | \
        tail -n +2 | \
        xargs -I {} basename {} | \
        sort
}

# Get skill description from SKILL.md
get_skill_description() {
    local skill="$1"
    local skill_md=".claude/skills/$skill/SKILL.md"
    
    if [ ! -f "$skill_md" ]; then
        echo "No description available"
        return
    fi
    
    # Try to get from frontmatter
    local desc=$(grep "^description:" "$skill_md" 2>/dev/null | \
        cut -d':' -f2- | \
        sed 's/^ *//' | \
        tr -d '"' | \
        head -1)
    
    if [ -n "$desc" ]; then
        echo "$desc"
    else
        # Fallback: get first paragraph after # heading
        grep -A 3 "^# " "$skill_md" | tail -3 | head -1
    fi
}

# Extract key patterns from a skill
extract_patterns() {
    local skill="$1"
    local skill_md=".claude/skills/$skill/SKILL.md"
    
    if [ ! -f "$skill_md" ]; then
        echo "⚡ Skill file not found: $skill_md" >&2
        return 1
    fi
    
    # Get tier
    local tier=$(grep "^tier:" "$skill_md" 2>/dev/null | \
        cut -d':' -f2 | \
        tr -d ' ' | \
        head -1)
    [ -z "$tier" ] && tier="unknown"
    
    # Get composition flag
    local composition=$(grep "^composition:" "$skill_md" 2>/dev/null | \
        cut -d':' -f2 | \
        tr -d ' ' | \
        head -1)
    [ -z "$composition" ] && composition="false"
    
    # Extract section headers (key concepts)
    local concepts=$(grep "^## " "$skill_md" | \
        sed 's/^## //' | \
        grep -v "^#" | \
        head -3 | \
        tr '\n' '; ')
    
    echo "tier=$tier; composition=$composition; concepts=$concepts"
}

# Random collision: pick 2 random skills
random_collision() {
    local skills=($(discover_skills))
    local count=${#skills[@]}
    
    if [ "$count" -lt 2 ]; then
        echo "⚡ Not enough skills for collision (need at least 2)" >&2
        return 1
    fi
    
    local idx1=$((RANDOM % count))
    local idx2=$((RANDOM % count))
    
    # Ensure different skills
    local retries=0
    while [ $idx2 -eq $idx1 ] && [ $retries -lt 10 ]; do
        idx2=$((RANDOM % count))
        retries=$((retries + 1))
    done
    
    if [ $idx2 -eq $idx1 ]; then
        echo "⚡ Failed to pick different skills" >&2
        return 1
    fi
    
    echo "${skills[$idx1]}" "${skills[$idx2]}"
}

# Targeted collision: user specifies
targeted_collision() {
    local skill_a="$1"
    local skill_b="$2"
    
    if [ ! -d ".claude/skills/$skill_a" ]; then
        echo "⚡ Skill '$skill_a' not found. Available:" >&2
        discover_skills | sed 's/^/  - /' >&2
        return 1
    fi
    
    if [ ! -d ".claude/skills/$skill_b" ]; then
        echo "⚡ Skill '$skill_b' not found. Available:" >&2
        discover_skills | sed 's/^/  - /' >&2
        return 1
    fi
    
    echo "$skill_a" "$skill_b"
}

# Record collision attempt
record_collision() {
    local skill_a="$1"
    local skill_b="$2"
    local timestamp=$(date -Iseconds)
    
    init_forge_brain
    
    echo "${skill_a}×${skill_b}|${timestamp}|attempted" >> .claude/brain/forge_collisions
}

# Force collision and display emergent pattern prompt
force_collision() {
    local skill_a="$1"
    local skill_b="$2"
    
    echo ""
    echo "🍆👾⚡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⚡👾🍆"
    echo "       GREMLIN-FORGE COLLISION INITIATED       "
    echo "🍆👾⚡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⚡👾🍆"
    echo ""
    echo "COLLIDING:"
    echo "  [A] $skill_a"
    echo "  [B] $skill_b"
    echo ""
    
    # Extract patterns
    echo "📊 Analyzing patterns..."
    local patterns_a=$(extract_patterns "$skill_a")
    local patterns_b=$(extract_patterns "$skill_b")
    
    echo "  A: $patterns_a"
    echo "  B: $patterns_b"
    echo ""
    
    # Get descriptions
    local desc_a=$(get_skill_description "$skill_a")
    local desc_b=$(get_skill_description "$skill_b")
    
    # Generate collision prompt
    cat <<EOF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 COLLISION ZONE 🔥
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUESTION: What if we treated [$skill_a] like [$skill_b]?

Skill A Essence:
  $desc_a

Skill B Essence:
  $desc_b

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EMERGENT QUESTIONS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. What properties from B could enhance A's core function?
2. What patterns from A could reframe B's approach?
3. What NEW capability emerges that neither has alone?
4. Where does the metaphor break?
   (That's where innovation lives!)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🍆👾 THINK LIKE A GREMLIN 👾🍆
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Edge cases ARE main cases
• Jank that works > elegant that doesn't
• Trauma-informed chaos is the way
• If it's technically correct, it's CORRECT
• Maximum jank = Maximum insight

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SUGGESTED NEW SKILL NAMES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EOF
    
    # Generate some name suggestions
    local base_a=$(echo "$skill_a" | cut -d'-' -f1-2)
    local base_b=$(echo "$skill_b" | cut -d'-' -f1-2)
    
    echo "  - ${base_a}-${base_b}"
    echo "  - ${base_b}-${base_a}"
    echo "  - $(echo "$skill_a" | cut -d'-' -f1)-$(echo "$skill_b" | cut -d'-' -f1)"
    echo "  - meta-$(echo "$skill_a" | cut -d'-' -f2 2>/dev/null || echo "$skill_a")"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Record collision
    record_collision "$skill_a" "$skill_b"
    
    # Record usage
    echo "$(date -Iseconds)|gremlin-forge|collision:$skill_a×$skill_b" >> .claude/brain/usage_log
    
    echo "✓ Collision recorded in Git-brain"
    echo ""
    echo "💡 Next steps:"
    echo "  1. Ponder the emergent pattern"
    echo "  2. Use gremlin-jank-builder-v2 to generate the new skill"
    echo "  3. Or use: ./pattern-extractor.sh to analyze further"
    echo ""
}

# Suggest next collisions based on learnings
suggest_next_collisions() {
    echo ""
    echo "🎯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🎯"
    echo "        COLLISION SUGGESTIONS"
    echo "🎯━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🎯"
    echo ""
    
    # Skills that haven't been collided yet
    local all_skills=($(discover_skills))
    local collided=""
    
    if [ -f .claude/brain/forge_collisions ]; then
        collided=$(cut -d'|' -f1 .claude/brain/forge_collisions)
    fi
    
    local suggestions=0
    local max_suggestions=5
    
    echo "💡 Untested Collisions:" 
    echo ""
    
    # Suggest interesting combinations
    for skill_a in "${all_skills[@]}"; do
        if [ $suggestions -ge $max_suggestions ]; then
            break
        fi
        
        for skill_b in "${all_skills[@]}"; do
            if [ $suggestions -ge $max_suggestions ]; then
                break
            fi
            
            if [ "$skill_a" != "$skill_b" ]; then
                # Check if this collision was tried
                if [ -z "$collided" ] || ! echo "$collided" | grep -q "${skill_a}×${skill_b}\|${skill_b}×${skill_a}"; then
                    echo "  ⚡ $skill_a × $skill_b"
                    echo "     A: $(get_skill_description "$skill_a" | head -c 60)..."
                    echo "     B: $(get_skill_description "$skill_b" | head -c 60)..."
                    echo ""
                    suggestions=$((suggestions + 1))
                fi
            fi
        done
    done
    
    if [ $suggestions -eq 0 ]; then
        echo "  🍆👾 All basic collisions attempted! Time for advanced chaos:"
        echo "  - Try 3-way collisions"
        echo "  - Collide generated skills with originals"
        echo "  - Collide a skill with itself (meta-recursion)"
        echo ""
    fi
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Run: ./collision-engine.sh --collide skill-a skill-b"
    echo ""
}

# Get forge statistics
forge_stats() {
    init_forge_brain
    
    echo ""
    echo "📊━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━📊"
    echo "        GREMLIN-FORGE STATISTICS"
    echo "📊━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━📊"
    echo ""
    
    local total_collisions=$(wc -l < .claude/brain/forge_collisions 2>/dev/null || echo 0)
    local total_learnings=$(wc -l < .claude/brain/forge_learnings 2>/dev/null || echo 0)
    local total_skills=$(discover_skills | wc -l)
    
    echo "Total Skills Available:  $total_skills"
    echo "Collisions Attempted:    $total_collisions"
    echo "Learnings Stored:        $total_learnings"
    
    if [ "$total_collisions" -gt 0 ]; then
        echo "Success Rate:            $((total_learnings * 100 / total_collisions))%"
    fi
    
    echo ""
    
    if [ "$total_learnings" -gt 0 ]; then
        echo "Recent Learnings:"
        tail -3 .claude/brain/forge_learnings | while read hash; do
            if [ -n "$hash" ]; then
                # More robust JSON parsing - handles multiline and edge cases
                git cat-file -p "$hash" 2>/dev/null | grep '"collision"' | \
                    sed 's/.*"collision":[[:space:]]*"\([^"]*\)".*/  🔥 \1/' || \
                    echo "  🔥 (parsing error - hash: $hash)"
            fi
        done
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Main entry point
main() {
    local command="${1:-}"
    
    init_forge_brain
    
    case "$command" in
        --random)
            echo "🎲 Random collision mode..."
            local collision=$(random_collision)
            if [ $? -eq 0 ]; then
                local skill_a=$(echo "$collision" | awk '{print $1}')
                local skill_b=$(echo "$collision" | awk '{print $2}')
                force_collision "$skill_a" "$skill_b"
            fi
            ;;
        --collide)
            if [ $# -lt 3 ]; then
                echo "Usage: $0 --collide skill-a skill-b" >&2
                exit 1
            fi
            local skill_a="$2"
            local skill_b="$3"
            local collision=$(targeted_collision "$skill_a" "$skill_b")
            if [ $? -eq 0 ]; then
                force_collision "$skill_a" "$skill_b"
            fi
            ;;
        --suggest)
            suggest_next_collisions
            ;;
        --stats)
            forge_stats
            ;;
        --help|*)
            cat <<EOF
🍆👾⚡ GREMLIN-FORGE Collision Engine ⚡👾🍆

Usage: $0 [OPTIONS]

OPTIONS:
  --random              Random collision (let chaos decide)
  --collide A B         Targeted collision (specific skills)
  --suggest             Suggest next untested collisions
  --stats               Show forge statistics
  --help                Show this help

EXAMPLES:
  $0 --random
  $0 --collide reasoning-patterns-v2 synthesis-engine
  $0 --suggest

🍆👾 MAXIMUM JANK. MAXIMUM INSIGHT. 👾🍆
EOF
            if [ "$command" != "--help" ]; then
                exit 1
            fi
            ;;
    esac
}

main "$@"
