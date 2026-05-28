#!/bin/bash
# Build knowledge search index from docs/ directory
# Generates .knowledge-index.json with titles, tags, and summaries

set -e

PROJECT_ROOT="${1:-.}"
INDEX_FILE="$PROJECT_ROOT/.knowledge-index.json"

# Scan directories for markdown files
scan_files() {
    find "$PROJECT_ROOT/docs" -name "*.md" -type f \
        ! -name ".gitkeep" \
        ! -path "*/auto-captured/*" \
        2>/dev/null | sort
}

# Extract title from markdown file (first # heading or filename)
extract_title() {
    local file="$1"
    local title
    title=$(grep -m1 '^# ' "$file" 2>/dev/null | sed 's/^# //')
    if [[ -z "$title" ]]; then
        title=$(basename "$file" .md | tr '-' ' ' | tr '_' ' ')
    fi
    echo "$title"
}

# Extract tags from frontmatter or content
extract_tags() {
    local file="$1"
    local tags=""

    # Try frontmatter tags: [tag1, tag2]
    tags=$(sed -n '/^---$/,/^---$/p' "$file" 2>/dev/null | \
        grep -E '^tags:' | \
        sed 's/^tags:\s*\[//; s/\].*//; s/,\s*/\n/g' | \
        tr -d ' "' | tr '\n' ',' | sed 's/,$//')

    # Fallback: look for Tags: line in content
    if [[ -z "$tags" ]]; then
        tags=$(grep -m1 '^[#*]*\s*Tags:' "$file" 2>/dev/null | \
            sed 's/.*Tags:\s*//; s/,\s*/,/g' | tr -d '`')
    fi

    echo "$tags"
}

# Extract first meaningful paragraph as summary (max 150 chars)
extract_summary() {
    local file="$1"
    local summary

    # Skip frontmatter and headings, get first paragraph
    summary=$(sed -n '/^---$/,/^---$/d; /^#/d; /^$/d; /^|/d; /^-/d; p' "$file" 2>/dev/null | \
        head -3 | tr '\n' ' ' | cut -c1-150)

    echo "$summary"
}

# Determine file type from path
get_file_type() {
    local file="$1"
    if [[ "$file" == *"/learnings/"* ]]; then
        echo "learning"
    elif [[ "$file" == *"/knowledge-base/"* ]]; then
        echo "knowledge"
    elif [[ "$file" == *"/retrospective/"* ]]; then
        echo "retrospective"
    elif [[ "$file" == *"/examples/"* ]]; then
        echo "example"
    elif [[ "$file" == *"/summaries/"* ]]; then
        echo "summary"
    else
        echo "other"
    fi
}

# Build index
build_index() {
    local entries=()
    local tag_map=()

    while IFS= read -r file; do
        local rel_path="${file#$PROJECT_ROOT/}"
        local title tags summary file_type

        title=$(extract_title "$file")
        tags=$(extract_tags "$file")
        summary=$(extract_summary "$file")
        file_type=$(get_file_type "$file")

        # Build entry JSON
        local entry
        entry=$(jq -n \
            --arg path "$rel_path" \
            --arg title "$title" \
            --arg tags "$tags" \
            --arg summary "$summary" \
            --arg type "$file_type" \
            '{
                path: $path,
                title: $title,
                tags: ($tags | split(",") | map(select(. != ""))),
                summary: $summary,
                type: $type
            }')

        entries+=("$entry")
    done < <(scan_files)

    # Combine entries into final index
    local generated
    generated=$(date -u '+%Y-%m-%dT%H:%M:%SZ')

    # Build tag index from entries
    printf '%s\n' "${entries[@]}" | jq -s --arg generated "$generated" '
        {
            generated: $generated,
            total: length,
            entries: .,
            tags: (
                [.[].tags[]] | group_by(.) | map({
                    key: .[0],
                    value: [
                        . as $tag |
                        $ARGS.positional[0][] |
                        select(.tags | index($tag[0])) |
                        .path
                    ]
                }) | from_entries
            ) // {},
            types: (group_by(.type) | map({key: .[0].type, value: length}) | from_entries)
        }
    ' --jsonargs "$(printf '%s\n' "${entries[@]}" | jq -s '.')" > "$INDEX_FILE"

    local count=${#entries[@]}
    echo "Index built: $INDEX_FILE ($count entries)" >&2
}

# Simple tag index (more reliable than complex jq)
build_simple_index() {
    local generated
    generated=$(date -u '+%Y-%m-%dT%H:%M:%SZ')

    local entries_json="[]"

    while IFS= read -r file; do
        [[ -z "$file" ]] && continue
        local rel_path="${file#$PROJECT_ROOT/}"
        local title tags summary file_type

        title=$(extract_title "$file")
        tags=$(extract_tags "$file")
        summary=$(extract_summary "$file")
        file_type=$(get_file_type "$file")

        entries_json=$(echo "$entries_json" | jq \
            --arg path "$rel_path" \
            --arg title "$title" \
            --arg tags "$tags" \
            --arg summary "$summary" \
            --arg type "$file_type" \
            '. += [{
                path: $path,
                title: $title,
                tags: ($tags | split(",") | map(select(. != ""))),
                summary: $summary,
                type: $type
            }]')
    done < <(scan_files)

    # Build final index
    echo "$entries_json" | jq --arg generated "$generated" '{
        generated: $generated,
        total: length,
        entries: .,
        types: (group_by(.type) | map({key: .[0].type, value: length}) | from_entries)
    }' > "$INDEX_FILE"

    local count
    count=$(echo "$entries_json" | jq 'length')
    echo "Index built: $INDEX_FILE ($count entries)" >&2
}

# Main
build_simple_index
