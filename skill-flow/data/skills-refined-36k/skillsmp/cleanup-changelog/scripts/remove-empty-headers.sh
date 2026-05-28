#!/bin/bash

# Script to remove headers with empty sections from markdown files
# Usage: ./remove-empty-headers.sh <file1.md> [file2.md ...]

process_file() {
    local file="$1"
    local temp_file=$(mktemp)

    awk '
    # Check if line is a markdown header (any level)
    function is_header(line) {
        return (line ~ /^#{1,6} /)
    }

    # Check if line is a removable header (levels 3-6 only)
    function is_removable_header(line) {
        return (line ~ /^#{3,6} /)
    }

    {
        # Store all lines
        lines[NR] = $0
        is_header_line[NR] = is_header($0)
        is_removable_line[NR] = is_removable_header($0)
    }

    END {
        # Track which headers have content
        for (i = 1; i <= NR; i++) {
            if (is_header_line[i]) {
                has_content = 0

                # Look ahead to find if there is content before next header or EOF
                for (j = i + 1; j <= NR; j++) {
                    if (is_header_line[j]) {
                        # Hit another header, stop looking
                        break
                    }
                    # Check if line has content (not just empty/whitespace)
                    if (lines[j] ~ /[^[:space:]]/) {
                        has_content = 1
                        break
                    }
                }

                # Only remove if header is removable (L3-L6) AND empty
                # Always keep L1-L2 headers, and keep L3-L6 if they have content
                if (has_content || !is_removable_line[i]) {
                    print lines[i]
                }
            } else {
                # Not a header, always print
                print lines[i]
            }
        }
    }
    ' "$file" > "$temp_file"

    # Replace original file with processed version
    mv "$temp_file" "$file"
    echo "Processed: $file"
}

# Main script
if [ $# -eq 0 ]; then
    echo "Usage: $0 <file1.md> [file2.md ...]"
    echo "Removes headers with empty sections from markdown files"
    exit 1
fi

for file in "$@"; do
    if [ ! -f "$file" ]; then
        echo "Error: File '$file' not found"
        continue
    fi

    if [[ ! "$file" =~ \.md$ ]]; then
        echo "Warning: '$file' doesn't have .md extension, skipping"
        continue
    fi

    process_file "$file"
done
