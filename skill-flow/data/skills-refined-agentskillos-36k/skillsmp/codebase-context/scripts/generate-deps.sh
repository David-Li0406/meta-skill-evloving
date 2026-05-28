#!/bin/bash
# Generate dependency graph for a project
# Usage: ./generate-deps.sh [project-root] [format]
#
# Formats:
#   mermaid (default) - Mermaid flowchart syntax
#   dot               - GraphViz DOT format
#   json              - JSON adjacency list
#
# This script extracts import relationships and outputs a dependency graph.

set -e

PROJECT_ROOT="${1:-.}"
FORMAT="${2:-mermaid}"
OUTPUT_DIR="$PROJECT_ROOT/.claude"

mkdir -p "$OUTPUT_DIR"

case "$FORMAT" in
    mermaid) OUTPUT_FILE="$OUTPUT_DIR/deps.mermaid" ;;
    dot) OUTPUT_FILE="$OUTPUT_DIR/deps.dot" ;;
    json) OUTPUT_FILE="$OUTPUT_DIR/deps.json" ;;
    *) echo "Unknown format: $FORMAT"; exit 1 ;;
esac

# Detect project type
detect_project_type() {
    if [ -f "$PROJECT_ROOT/package.json" ]; then
        echo "node"
    elif [ -f "$PROJECT_ROOT/pyproject.toml" ] || [ -f "$PROJECT_ROOT/setup.py" ]; then
        echo "python"
    elif [ -f "$PROJECT_ROOT/Cargo.toml" ]; then
        echo "rust"
    elif [ -f "$PROJECT_ROOT/go.mod" ]; then
        echo "go"
    else
        echo "unknown"
    fi
}

PROJECT_TYPE=$(detect_project_type)
echo "Detected project type: $PROJECT_TYPE"

# Temp file for edges
EDGES_TMP=$(mktemp)
cleanup() { rm -f "$EDGES_TMP"; }
trap cleanup EXIT

# ============================================================================
# IMPORT EXTRACTION BY LANGUAGE
# ============================================================================

extract_imports_typescript() {
    echo "Extracting TypeScript/JavaScript imports..."

    find "$PROJECT_ROOT" -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \) \
        -not -path "*/node_modules/*" \
        -not -path "*/.next/*" \
        -not -path "*/dist/*" \
        -not -path "*/build/*" \
        -not -name "*.spec.*" \
        -not -name "*.test.*" \
        -not -name "*.d.ts" \
        2>/dev/null | while read -r file; do

        local rel_file=$(echo "$file" | sed "s|$PROJECT_ROOT/||")

        # Extract imports - match: import ... from '...' or import ... from "..."
        grep -oE "from ['\"][^'\"]+['\"]" "$file" 2>/dev/null \
            | sed "s/from ['\"]//; s/['\"]$//" \
            | while read -r import_path; do

            # Skip node_modules imports
            if [[ "$import_path" != .* ]] && [[ "$import_path" != @/* ]]; then
                continue
            fi

            # Resolve relative imports
            if [[ "$import_path" == .* ]]; then
                local dir=$(dirname "$file")

                # Resolve the path manually (works on macOS and Linux)
                # Combine dir + import_path and normalize
                local combined="$dir/$import_path"

                # Try common extensions
                for ext in ".ts" ".tsx" ".js" ".jsx" "/index.ts" "/index.tsx" "/index.js"; do
                    local full_path="$combined$ext"
                    # Normalize path by removing . and .. components
                    local dir_part=$(dirname "$full_path")
                    local base_part=$(basename "$full_path")
                    full_path=$(cd "$dir_part" 2>/dev/null && echo "$(pwd)/$base_part" || echo "")

                    if [ -n "$full_path" ] && [ -f "$full_path" ]; then
                        # Get absolute project root for accurate substitution
                        local abs_project_root=$(cd "$PROJECT_ROOT" && pwd)
                        local rel_import=$(echo "$full_path" | sed "s|^$abs_project_root/||")
                        echo "$rel_file -> $rel_import" >> "$EDGES_TMP"
                        break
                    fi
                done
            elif [[ "$import_path" == @/* ]]; then
                # Handle path aliases like @/lib/utils
                local alias_path=$(echo "$import_path" | sed 's|^@/||')

                # Try both with and without src/ prefix
                for base in "$PROJECT_ROOT/src" "$PROJECT_ROOT"; do
                    local src_path="$base/$alias_path"

                    for ext in "" ".ts" ".tsx" ".js" ".jsx" "/index.ts" "/index.tsx"; do
                        local full_path="$src_path$ext"
                        if [ -f "$full_path" ]; then
                            local rel_import=$(echo "$full_path" | sed "s|$PROJECT_ROOT/||")
                            echo "$rel_file -> $rel_import" >> "$EDGES_TMP"
                            break 2
                        fi
                    done
                done
            fi
        done
    done
}

extract_imports_python() {
    echo "Extracting Python imports..."

    find "$PROJECT_ROOT" -type f -name "*.py" \
        -not -path "*/__pycache__/*" \
        -not -path "*/venv/*" \
        -not -path "*/.venv/*" \
        -not -path "*/site-packages/*" \
        -not -name "test_*.py" \
        -not -name "*_test.py" \
        2>/dev/null | while read -r file; do

        local rel_file=$(echo "$file" | sed "s|$PROJECT_ROOT/||")

        # Extract: from package.module import ... and import package.module
        grep -E "^(from|import) [a-zA-Z_]" "$file" 2>/dev/null \
            | sed -E 's/^from ([^ ]+) import.*/\1/; s/^import ([^ ,]+).*/\1/' \
            | while read -r import_path; do

            # Skip standard library and external packages (heuristic: if not in project)
            local module_path=$(echo "$import_path" | tr '.' '/')
            local py_file="$PROJECT_ROOT/$module_path.py"
            local py_init="$PROJECT_ROOT/$module_path/__init__.py"

            if [ -f "$py_file" ]; then
                local rel_import=$(echo "$py_file" | sed "s|$PROJECT_ROOT/||")
                echo "$rel_file -> $rel_import" >> "$EDGES_TMP"
            elif [ -f "$py_init" ]; then
                local rel_import=$(echo "$py_init" | sed "s|$PROJECT_ROOT/||")
                echo "$rel_file -> $rel_import" >> "$EDGES_TMP"
            fi
        done
    done
}

extract_imports_go() {
    echo "Extracting Go imports..."

    # Get module name from go.mod
    local module_name=$(grep "^module " "$PROJECT_ROOT/go.mod" 2>/dev/null | awk '{print $2}')

    find "$PROJECT_ROOT" -type f -name "*.go" \
        -not -path "*/vendor/*" \
        -not -name "*_test.go" \
        2>/dev/null | while read -r file; do

        local rel_file=$(echo "$file" | sed "s|$PROJECT_ROOT/||")

        # Extract imports within the module
        grep -oE "\"$module_name/[^\"]+\"" "$file" 2>/dev/null \
            | tr -d '"' \
            | sed "s|$module_name/||" \
            | while read -r import_path; do

            # Find the actual Go file(s) in that package
            local pkg_dir="$PROJECT_ROOT/$import_path"
            if [ -d "$pkg_dir" ]; then
                # Link to the directory (packages, not files)
                echo "$rel_file -> $import_path/" >> "$EDGES_TMP"
            fi
        done
    done
}

extract_imports() {
    case "$PROJECT_TYPE" in
        node) extract_imports_typescript ;;
        python) extract_imports_python ;;
        go) extract_imports_go ;;
        *) echo "Unsupported project type: $PROJECT_TYPE"; exit 1 ;;
    esac
}

# ============================================================================
# OUTPUT GENERATION
# ============================================================================

# Group files into clusters for better visualization
detect_clusters() {
    # Extract unique directories at depth 2
    cut -d' ' -f1 "$EDGES_TMP" | while read -r file; do
        local dir=$(dirname "$file" | cut -d/ -f1-2)
        echo "$dir"
    done | sort -u
}

generate_mermaid() {
    echo "Generating Mermaid output..."

    cat > "$OUTPUT_FILE" << 'EOF'
%% Dependency Graph
%% Generated by codebase-context skill
%% Read this to understand import relationships

graph LR
EOF

    # Add subgraphs for major directories
    local clusters=$(detect_clusters)
    local current_cluster=""

    # Simplify file names for readability
    sort -u "$EDGES_TMP" | while read -r edge; do
        local from=$(echo "$edge" | cut -d' ' -f1)
        local to=$(echo "$edge" | cut -d' ' -f3)

        # Create node IDs (replace special chars)
        local from_id=$(echo "$from" | sed 's/[^a-zA-Z0-9]/_/g')
        local to_id=$(echo "$to" | sed 's/[^a-zA-Z0-9]/_/g')

        # Shorten labels
        local from_label=$(basename "$from" | sed 's/\.[^.]*$//')
        local to_label=$(basename "$to" | sed 's/\.[^.]*$//')

        echo "  ${from_id}[\"$from_label\"] --> ${to_id}[\"$to_label\"]" >> "$OUTPUT_FILE"
    done

    # Add a legend comment
    echo "" >> "$OUTPUT_FILE"
    echo "%% Full paths:" >> "$OUTPUT_FILE"
    sort -u "$EDGES_TMP" | head -20 | while read -r edge; do
        echo "%%   $edge" >> "$OUTPUT_FILE"
    done

    local total=$(wc -l < "$EDGES_TMP" | tr -d ' ')
    if [ "$total" -gt 20 ]; then
        echo "%%   ... and $((total - 20)) more edges" >> "$OUTPUT_FILE"
    fi
}

generate_dot() {
    echo "Generating DOT output..."

    cat > "$OUTPUT_FILE" << 'EOF'
// Dependency Graph
// Generated by codebase-context skill
// Render with: dot -Tsvg deps.dot -o deps.svg

digraph deps {
  rankdir=LR;
  node [shape=box, style=rounded, fontsize=10];
  edge [arrowsize=0.7];

EOF

    # Create clusters for top-level directories
    local clusters=$(detect_clusters)

    for cluster in $clusters; do
        local cluster_id=$(echo "$cluster" | sed 's/[^a-zA-Z0-9]/_/g')
        local cluster_label=$(echo "$cluster" | sed 's|/|/\\n|g')

        echo "  subgraph cluster_$cluster_id {" >> "$OUTPUT_FILE"
        echo "    label=\"$cluster_label\";" >> "$OUTPUT_FILE"
        echo "    style=dashed;" >> "$OUTPUT_FILE"

        # Add nodes in this cluster
        grep "^$cluster" "$EDGES_TMP" 2>/dev/null | cut -d' ' -f1 | sort -u | while read -r file; do
            local node_id=$(echo "$file" | sed 's/[^a-zA-Z0-9]/_/g')
            local node_label=$(basename "$file")
            echo "    \"$node_id\" [label=\"$node_label\"];" >> "$OUTPUT_FILE"
        done

        echo "  }" >> "$OUTPUT_FILE"
        echo "" >> "$OUTPUT_FILE"
    done

    # Add edges
    echo "  // Dependencies" >> "$OUTPUT_FILE"
    sort -u "$EDGES_TMP" | while read -r edge; do
        local from=$(echo "$edge" | cut -d' ' -f1)
        local to=$(echo "$edge" | cut -d' ' -f3)

        local from_id=$(echo "$from" | sed 's/[^a-zA-Z0-9]/_/g')
        local to_id=$(echo "$to" | sed 's/[^a-zA-Z0-9]/_/g')

        echo "  \"$from_id\" -> \"$to_id\";" >> "$OUTPUT_FILE"
    done

    echo "}" >> "$OUTPUT_FILE"
}

generate_json() {
    echo "Generating JSON output..."

    echo "{" > "$OUTPUT_FILE"
    echo "  \"generated\": $(date +%s)," >> "$OUTPUT_FILE"
    echo "  \"edges\": [" >> "$OUTPUT_FILE"

    local first=true
    sort -u "$EDGES_TMP" | while read -r edge; do
        local from=$(echo "$edge" | cut -d' ' -f1)
        local to=$(echo "$edge" | cut -d' ' -f3)

        if [ "$first" = true ]; then
            first=false
        else
            echo "," >> "$OUTPUT_FILE"
        fi
        printf '    {"from": "%s", "to": "%s"}' "$from" "$to" >> "$OUTPUT_FILE"
    done

    echo "" >> "$OUTPUT_FILE"
    echo "  ]," >> "$OUTPUT_FILE"

    # Also include adjacency list
    echo "  \"adjacency\": {" >> "$OUTPUT_FILE"

    local first=true
    cut -d' ' -f1 "$EDGES_TMP" | sort -u | while read -r file; do
        if [ "$first" = true ]; then
            first=false
        else
            echo "," >> "$OUTPUT_FILE"
        fi

        local deps=$(grep "^$file -> " "$EDGES_TMP" | cut -d' ' -f3 | sort -u | tr '\n' ',' | sed 's/,$//' | sed 's/,/", "/g')
        printf '    "%s": ["%s"]' "$file" "$deps" >> "$OUTPUT_FILE"
    done

    echo "" >> "$OUTPUT_FILE"
    echo "  }" >> "$OUTPUT_FILE"
    echo "}" >> "$OUTPUT_FILE"
}

# ============================================================================
# MAIN
# ============================================================================

echo "Generating dependency graph for: $PROJECT_ROOT"
echo "Format: $FORMAT"
echo "Output: $OUTPUT_FILE"
echo ""

extract_imports

# Check if we got any edges
if [ ! -s "$EDGES_TMP" ]; then
    echo "Warning: No dependencies found. This could mean:"
    echo "  - The project uses a language/framework not yet supported"
    echo "  - All imports are external packages"
    echo "  - The source directory structure is non-standard"
    exit 0
fi

case "$FORMAT" in
    mermaid) generate_mermaid ;;
    dot) generate_dot ;;
    json) generate_json ;;
esac

echo ""
echo "Done! Generated $OUTPUT_FILE"
echo ""
echo "Stats:"
echo "  Total edges: $(wc -l < "$EDGES_TMP" | tr -d ' ')"
echo "  Unique files: $(cat "$EDGES_TMP" | tr ' ' '\n' | grep -v '^->$' | sort -u | wc -l | tr -d ' ')"
