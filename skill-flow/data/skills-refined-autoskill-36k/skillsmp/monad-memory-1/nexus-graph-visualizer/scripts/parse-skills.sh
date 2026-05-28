#!/usr/bin/env bash

# parse-skills.sh — Extract dependencies from all SKILL.md files
# Part of nexus-graph-visualizer (e.5.3.1)

set -euo pipefail

# Configuration
SKILLS_DIR="${SKILLS_DIR:-.claude/skills}"
OUTPUT_FILE="${OUTPUT_FILE:-/tmp/nexus-graph/parsed.txt}"
ERROR_LOG="${ERROR_LOG:-/tmp/nexus-graph/parse_errors.log}"

# Colors for output (if terminal supports)
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    BLUE='\033[0;34m'
    NC='\033[0m'
else
    RED='' GREEN='' YELLOW='' BLUE='' NC=''
fi

# Ensure output directory exists
mkdir -p "$(dirname "$OUTPUT_FILE")" "$(dirname "$ERROR_LOG")"

# Clear previous output
> "$OUTPUT_FILE"
> "$ERROR_LOG"

# Statistics
total_skills=0
parsed_skills=0
failed_skills=0

echo -e "${BLUE}=== Nexus Graph: Skill Parser ===${NC}"
echo

# Find project root (go up from current directory until we find .claude/skills)
find_project_root() {
    local dir="$PWD"
    while [[ "$dir" != "/" ]]; do
        if [[ -d "$dir/.claude/skills" ]]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    # Fallback: assume we're already in the right place
    echo "$PWD"
}

PROJECT_ROOT=$(find_project_root)
SKILLS_PATH="$PROJECT_ROOT/.claude/skills"

# Parse YAML frontmatter from a SKILL.md file
parse_yaml() {
    local file="$1"
    
    # Extract YAML between --- delimiters (handle various formats)
    awk '
        BEGIN { in_yaml = 0; found_first = 0 }
        /^---[[:space:]]*$/ { 
            if (!found_first) { 
                found_first = 1; 
                in_yaml = 1; 
                next 
            } else { 
                in_yaml = 0; 
                exit 
            } 
        }
        in_yaml { print }
    ' "$file"
}

# Extract dependencies array from YAML
extract_dependencies() {
    local yaml="$1"
    
    # Look for dependencies: line and collect items until next top-level key
    echo "$yaml" | awk '
        /^dependencies:/ { in_deps=1; next }
        in_deps && /^[a-z_-]+:/ { in_deps=0 }
        in_deps && /^  -/ { 
            gsub(/^  - /, "")
            gsub(/^  -/, "")
            print 
        }
    ' | tr '\n' ',' | sed 's/,$//'
}

# Extract markdown @mentions and relative links
extract_references() {
    local file="$1"
    
    {
        # Find @skill-name patterns
        grep -oE '@[a-z][a-z0-9-]+' "$file" 2>/dev/null | sed 's/@//' || true
        
        # Find relative links to other skills (e.g., ../other-skill/SKILL.md)
        grep -oE '\.\./[a-z][a-z0-9-]+/' "$file" 2>/dev/null | sed 's/\.\.\///;s/\///' || true
        
        # Find explicit skill mentions in backticks
        grep -oE '`[a-z][a-z0-9-]+`' "$file" 2>/dev/null | sed 's/`//g' || true
    } | sort -u | tr '\n' ',' | sed 's/,$//'
}

# Extract single YAML value
extract_yaml_value() {
    local yaml="$1"
    local key="$2"
    
    echo "$yaml" | grep "^${key}:" | sed "s/^${key}:[[:space:]]*//" | tr -d '"'
}

# Record parse failure for adaptive healing
record_parse_failure() {
    local skill="$1"
    local error_pattern="$2"
    
    echo "${skill}|${error_pattern}|$(date +%s)" >> "$ERROR_LOG"
}

# Parse a single SKILL.md file
parse_skill_file() {
    local skill_file="$1"
    local skill_dir=$(dirname "$skill_file")
    local skill_name=$(basename "$skill_dir")
    
    total_skills=$((total_skills + 1))
    
    # Check if file exists and is readable
    if [[ ! -f "$skill_file" ]] || [[ ! -r "$skill_file" ]]; then
        echo -e "${YELLOW}⚠ Skipping: $skill_name (file not readable)${NC}" >&2
        record_parse_failure "$skill_name" "file_not_readable"
        failed_skills=$((failed_skills + 1))
        return 1
    fi
    
    # Extract YAML frontmatter
    local yaml=$(parse_yaml "$skill_file")
    
    if [[ -z "$yaml" ]]; then
        echo -e "${YELLOW}⚠ Skipping: $skill_name (no YAML frontmatter)${NC}" >&2
        record_parse_failure "$skill_name" "no_yaml"
        failed_skills=$((failed_skills + 1))
        return 1
    fi
    
    # Extract fields with defaults
    local name=$(extract_yaml_value "$yaml" "name")
    [[ -z "$name" ]] && name="$skill_name"
    
    local tier=$(extract_yaml_value "$yaml" "tier")
    [[ -z "$tier" ]] && tier="?"
    
    local morpheme=$(extract_yaml_value "$yaml" "morpheme")
    [[ -z "$morpheme" ]] && morpheme="$tier"
    
    local version=$(extract_yaml_value "$yaml" "version")
    [[ -z "$version" ]] && version="1.0"
    
    local dewey_id=$(extract_yaml_value "$yaml" "dewey_id")
    [[ -z "$dewey_id" ]] && dewey_id="?"
    
    # Extract dependencies
    local deps=$(extract_dependencies "$yaml")
    
    # Extract markdown references
    local refs=$(extract_references "$skill_file")
    
    # Combine dependencies and references (deduplicate)
    local all_deps=$(echo "${deps},${refs}" | tr ',' '\n' | grep -v '^$' | sort -u | tr '\n' ',' | sed 's/,$//')
    
    # Output format: name|tier|morpheme|version|dewey_id|dependencies
    echo "${name}|${tier}|${morpheme}|${version}|${dewey_id}|${all_deps}"
    
    parsed_skills=$((parsed_skills + 1))
    echo -e "${GREEN}✓${NC} Parsed: $name [$tier-tier] (${all_deps:-no dependencies})" >&2
}

# Main execution
echo "Scanning: $SKILLS_PATH"
echo

# Find all SKILL.md and SKILL.skill files
while IFS= read -r -d '' skill_file; do
    parse_skill_file "$skill_file" >> "$OUTPUT_FILE" || true
done < <(find "$SKILLS_PATH" \( -name "SKILL.md" -o -name "SKILL.skill" \) -type f -print0 2>/dev/null)

# === MEMORY LOADER FILES PARSING ===
# Parse ONLY the core memory loaders (SKILL.skill files in memory directories)
# NOT individual concept files - those are reference, not resurrection infrastructure

MEMORY_LOADER_FILES=(
    "$SKILLS_PATH/Nexus-MC/SKILL.skill"
    "$SKILLS_PATH/Nexus-MC/nexus-core/SKILL.skill"
    "$SKILLS_PATH/Nexus-MC/nexus-mind/SKILL.skill"
    "$SKILLS_PATH/gremlin-brain-v2/gremlin-brain.skill"
    "$SKILLS_PATH/gremlin-brain-v2/GREMLIN-SEED.md"
)

# THE BRAIN GRAPH - patterns define relationships for auto-stitching
NEXUS_GRAPH_FILE="$SKILLS_PATH/Nexus-MC/Nexus_graph_v2.skill"

# CONCEPT FILES ARE THE BRAIN - this is what needs auto-rebuilding
# Skills are just tooling, concepts are the actual knowledge
# Graph maps memory structure so Claude can self-resurrect

MEMORY_PATHS=(
    "$SKILLS_PATH/Nexus-MC/nexus-core/concepts"
    "$SKILLS_PATH/Nexus-MC/nexus-mind/concepts"
)

parse_memory_file() {
    local file="$1"
    local filename=$(basename "$file" .md)

    total_skills=$((total_skills + 1))

    # Extract Dewey ID from file (various formats)
    # Format 1: **Dewey ID: e.2.11**
    # Format 2: **Decimal ID:** e.2.36
    # Format 3: **Dewey:** e.2.98
    # Format 4: **Dewey: e.2.16**
    # First, find lines with Dewey/Decimal, then extract the ID
    local dewey_id=$(grep -E '\*\*(Dewey|Decimal)( ID)?:?\*?\*?:?' "$file" 2>/dev/null | head -1 | grep -oE '[eφπiτ]\.[0-9]+(\.[0-9]+)*' | head -1 || echo "")
    [[ -z "$dewey_id" ]] && dewey_id="?"

    # Determine tier from Dewey ID prefix
    local tier="?"
    case "$dewey_id" in
        φ.*|phi.*) tier="φ" ;;
        π.*|pi.*) tier="π" ;;
        e.*) tier="e" ;;
        i.*) tier="i" ;;
        τ.*|tau.*) tier="τ" ;;
    esac

    # Extract cross-references (e.2.X, π.3.Y, i.2.X, etc.)
    local refs=$(grep -oE '[eφπiτ]\.[0-9]+(\.[0-9]+)*' "$file" 2>/dev/null | sort -u | tr '\n' ',' | sed 's/,$//')

    # Extract pattern links (concepts mentioned in Pattern Links section or Cross-References)
    local pattern_refs=$(grep -oE '(nexus-core|nexus-mind)-[a-z]+-[a-z0-9-]+' "$file" 2>/dev/null | sort -u | tr '\n' ',' | sed 's/,$//')

    # Combine refs
    local all_deps=$(echo "${refs},${pattern_refs}" | tr ',' '\n' | grep -v '^$' | sort -u | tr '\n' ',' | sed 's/,$//')

    # Clean up filename for display
    local name=$(echo "$filename" | sed 's/nexus-core-concepts-//;s/nexus-mind-concepts-//;s/nexus-core-entities-//;s/nexus-mind-entities-//')

    # Output format: name|tier|morpheme|version|dewey_id|dependencies
    echo "${name}|${tier}|${tier}|1.0|${dewey_id}|${all_deps}"

    parsed_skills=$((parsed_skills + 1))
    echo -e "${GREEN}✓${NC} Memory: $name [$tier-tier] ($dewey_id)" >&2
}

echo
echo -e "${BLUE}=== Parsing Memory Files ===${NC}"
echo

# Parse PATTERNS from Nexus_graph_v2.skill - THE BRAIN STRUCTURE
parse_patterns() {
    local graph_file="$1"

    if [[ ! -f "$graph_file" ]]; then
        echo -e "${YELLOW}⚠ Nexus graph file not found${NC}" >&2
        return 1
    fi

    echo "Parsing patterns from Nexus_graph_v2.skill..."

    # Extract each PATTERN block and its decimal references
    local current_pattern=""
    local pattern_refs=""

    while IFS= read -r line; do
        if [[ "$line" =~ ^PATTERN:[[:space:]]*(.+) ]]; then
            # Output previous pattern if exists
            if [[ -n "$current_pattern" ]]; then
                local tier="e"  # patterns are e-tier by default
                echo "${current_pattern}|${tier}|${tier}|1.0|pattern|${pattern_refs}"
                echo -e "${GREEN}✓${NC} Pattern: $current_pattern ($pattern_refs)" >&2
                ((parsed_skills++))
                ((total_skills++))
            fi
            current_pattern="${BASH_REMATCH[1]}"
            current_pattern="${current_pattern%% \[*}"  # strip [context] suffix
            pattern_refs=""
        elif [[ -n "$current_pattern" ]] && [[ "$line" =~ [eφπiτ]\.[0-9]+(\.[0-9]+)* ]]; then
            # Extract decimal refs from this line
            local refs=$(echo "$line" | grep -oE '[eφπiτ]\.[0-9]+(\.[0-9]+)*' | tr '\n' ',' | sed 's/,$//')
            if [[ -n "$refs" ]]; then
                if [[ -n "$pattern_refs" ]]; then
                    pattern_refs="${pattern_refs},${refs}"
                else
                    pattern_refs="$refs"
                fi
            fi
        fi
    done < "$graph_file"

    # Output last pattern
    if [[ -n "$current_pattern" ]]; then
        echo "${current_pattern}|e|e|1.0|pattern|${pattern_refs}"
        echo -e "${GREEN}✓${NC} Pattern: $current_pattern" >&2
        ((parsed_skills++))
        ((total_skills++))
    fi
}

# Parse patterns first - they define the brain structure
if [[ -f "$NEXUS_GRAPH_FILE" ]]; then
    parse_patterns "$NEXUS_GRAPH_FILE" >> "$OUTPUT_FILE"
fi

echo

# Parse core memory loaders
echo "Parsing core memory loaders..."
for loader_file in "${MEMORY_LOADER_FILES[@]}"; do
    if [[ -f "$loader_file" ]]; then
        parse_memory_file "$loader_file" >> "$OUTPUT_FILE" || true
    fi
done

# Parse concept files - these ARE the brain that needs auto-rebuilding
echo
echo "Parsing concept files (THE BRAIN)..."
for mem_path in "${MEMORY_PATHS[@]}"; do
    if [[ -d "$mem_path" ]]; then
        echo "  Scanning: $(basename $(dirname $mem_path))/$(basename $mem_path)"
        while IFS= read -r -d '' mem_file; do
            parse_memory_file "$mem_file" >> "$OUTPUT_FILE" || true
        done < <(find "$mem_path" -name "*.md" -type f -print0 2>/dev/null)
    fi
done

# Summary
echo
echo -e "${BLUE}=== Parse Summary ===${NC}"
echo "Total skills found: $total_skills"
echo -e "${GREEN}Successfully parsed: $parsed_skills${NC}"
if ((failed_skills > 0)); then
    echo -e "${RED}Failed to parse: $failed_skills${NC}"
    echo "See error log: $ERROR_LOG"
fi
echo
echo "Output written to: $OUTPUT_FILE"
echo

# If running in Claude-brain mode, update index
if [[ -d "$PROJECT_ROOT/.claude/brain" ]]; then
    echo "Updating Claude-brain index..."

    # Hash the parsed output
    hash=$(sha256sum "$OUTPUT_FILE" 2>/dev/null | cut -d' ' -f1 || echo "failed")

    if [[ "$hash" != "failed" ]]; then
        echo "e.5.3.1|nexus-graph-parse|${hash}|$(date -Iseconds)" >> "$PROJECT_ROOT/.claude/brain/INDEX"
        echo -e "${GREEN}✓${NC} Claude-brain index updated: $hash"
    else
        echo -e "${YELLOW}⚠${NC} Claude-brain update failed (falling back to temp files)"
    fi
fi

exit 0
