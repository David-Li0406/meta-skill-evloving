#!/bin/bash
# ==============================================================================
# lib/validation.sh - Deterministic Validation Checks
#
# Fast, local checks that don't require LLM.
# Catches structural issues early.
# ==============================================================================

check_spec_structure() {
    local file="$1"
    local content
    content=$(cat "$file")
    local issues=()
    local warnings=()

    # Required sections
    if ! echo "$content" | grep -qiE "^#.*problem|^##.*problem|problem.*statement"; then
        issues+=("Missing: Problem statement")
    else
        echo -e "  ${GREEN}✓${NC} Problem statement found"
    fi

    if ! echo "$content" | grep -qiE "success.*criter|acceptance.*criter|done.*when|definition.*done"; then
        issues+=("Missing: Success criteria")
    else
        echo -e "  ${GREEN}✓${NC} Success criteria found"
    fi

    if ! echo "$content" | grep -qiE "scope|boundar|in.scope|out.of.scope|non-goal"; then
        warnings+=("Consider adding: Scope boundaries")
    else
        echo -e "  ${GREEN}✓${NC} Scope defined"
    fi

    if ! echo "$content" | grep -qiE "test|verif|validat"; then
        warnings+=("Consider adding: Test/validation approach")
    else
        echo -e "  ${GREEN}✓${NC} Testing mentioned"
    fi

    # Check for vague words
    local vague_count
    vague_count=$(echo "$content" | grep -ciE "properly|efficiently|adequate|reasonable|good quality|as needed" 2>/dev/null) || vague_count=0
    if [[ $vague_count -gt 3 ]]; then
        warnings+=("Found $vague_count vague terms (properly, efficiently, etc.)")
    fi

    # Check minimum content
    local word_count
    word_count=$(wc -w < "$file" | tr -d ' ')
    if [[ $word_count -lt 100 ]]; then
        issues+=("Too short: $word_count words (minimum ~100)")
    fi

    # Report results
    if [[ ${#issues[@]} -gt 0 ]]; then
        echo -e "${RED}Critical issues:${NC}"
        for issue in "${issues[@]}"; do
            echo -e "  ${RED}❌${NC} $issue"
        done
        return 1
    fi

    if [[ ${#warnings[@]} -gt 0 ]]; then
        echo -e "${YELLOW}Warnings (non-blocking):${NC}"
        for warning in "${warnings[@]}"; do
            echo -e "  ${YELLOW}⚠️${NC}  $warning"
        done
    fi

    return 0
}

validate_spec_structure() {
    local file="$1"
    local content
    content=$(cat "$file")

    echo "Checking spec sections..."

    # Validate required fields exist
    if ! echo "$content" | grep -qiE "^#.*problem|problem.*statement"; then
        echo -e "  ${RED}❌${NC} Missing problem statement"
        return 1
    fi
    echo -e "  ${GREEN}✓${NC} Problem statement"

    if ! echo "$content" | grep -qiE "success.*criter|acceptance.*criter"; then
        echo -e "  ${RED}❌${NC} Missing success criteria"
        return 1
    fi
    echo -e "  ${GREEN}✓${NC} Success criteria"

    # Check for common vague terms
    local vague=$(echo "$content" | grep -iE "properly|efficiently|should work|good|nice|reasonable" || true)
    if [[ -n "$vague" ]]; then
        echo -e "  ${YELLOW}⚠️${NC}  Contains vague terms (see instruction)"
    fi

    echo -e "  ${GREEN}✓${NC} Structure valid"
    return 0
}

validate_prp_structure() {
    local file="$1"
    local content
    content=$(cat "$file")

    echo "Checking PRP structure..."

    # Validate required PRP sections
    if ! echo "$content" | grep -q "^# PRP:"; then
        echo -e "  ${RED}❌${NC} Missing PRP metadata"
        return 1
    fi
    echo -e "  ${GREEN}✓${NC} PRP metadata"

    if ! echo "$content" | grep -q "## Phase"; then
        echo -e "  ${RED}❌${NC} Missing phase sections"
        return 1
    fi
    echo -e "  ${GREEN}✓${NC} Phase sections"

    if ! echo "$content" | grep -q "### Deliverables\|^### F[0-9]"; then
        echo -e "  ${RED}❌${NC} Missing deliverables"
        return 1
    fi
    echo -e "  ${GREEN}✓${NC} Deliverables"

    if ! echo "$content" | grep -q "Success Criteria\|^| SC-"; then
        echo -e "  ${RED}❌${NC} Missing success criteria"
        return 1
    fi
    echo -e "  ${GREEN}✓${NC} Success criteria"

    echo -e "  ${GREEN}✓${NC} Structure valid"
    return 0
}

# Check if spec has changed since last command
spec_has_changed() {
    local spec_file="$1"
    local state_file="$2"

    if [[ ! -f "$state_file" ]]; then
        return 0  # New spec
    fi

    # Compare file hashes
    local current_hash=$(md5sum < "$spec_file" | cut -d' ' -f1)
    local stored_hash=$(grep -o '"spec_hash":"[^"]*"' "$state_file" | cut -d'"' -f4)

    [[ "$current_hash" != "$stored_hash" ]]
}
