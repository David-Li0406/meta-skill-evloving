#!/bin/bash
# Generate code-index.json for a project
# Usage: ./generate-code-index.sh [project-root]
#
# This script extracts:
# - concepts: Maps domain concepts to file locations
# - entry_points: Maps API routes to handler files
# - exports: Maps files to their exported symbols
# - types: Maps type names to definition locations

set -e

PROJECT_ROOT="${1:-.}"
OUTPUT_DIR="$PROJECT_ROOT/.claude"
OUTPUT_FILE="$OUTPUT_DIR/code-index.json"

mkdir -p "$OUTPUT_DIR"

# Detect project type
detect_project_type() {
    if [ -f "$PROJECT_ROOT/package.json" ]; then
        if grep -q '"next"' "$PROJECT_ROOT/package.json" 2>/dev/null; then
            echo "nextjs"
        elif grep -q '"express"' "$PROJECT_ROOT/package.json" 2>/dev/null; then
            echo "express"
        else
            echo "node"
        fi
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

# Temp files for collecting data
CONCEPTS_TMP=$(mktemp)
ENTRY_POINTS_TMP=$(mktemp)
EXPORTS_TMP=$(mktemp)
TYPES_TMP=$(mktemp)

cleanup() {
    rm -f "$CONCEPTS_TMP" "$ENTRY_POINTS_TMP" "$EXPORTS_TMP" "$TYPES_TMP"
}
trap cleanup EXIT

# ============================================================================
# CONCEPT EXTRACTION
# Maps semantic concepts to file locations based on file/folder names and content
# ============================================================================

extract_concepts() {
    echo "Extracting concepts..."

    # Define concept patterns: "concept_name:pattern1|pattern2|pattern3"
    local concepts=(
        "authentication:auth|login|logout|signin|signout|session|jwt|oauth"
        "authorization:permission|role|access|policy|guard"
        "database:prisma|sequelize|typeorm|mongoose|knex|sql|query|migration|db"
        "api:route|endpoint|controller|handler"
        "error_handling:error|exception|fault"
        "validation:valid|schema|zod|yup|joi"
        "testing:test|spec|mock|stub|fixture"
        "logging:logger|winston|pino"
        "caching:cache|redis|memcache"
        "email:email|mail|smtp|sendgrid"
        "payments:payment|stripe|paypal|billing|invoice"
        "uploads:upload|multer|s3|storage"
        "websockets:socket|realtime|pubsub"
        "scheduling:cron|schedule|job|queue|worker"
    )

    for concept_def in "${concepts[@]}"; do
        local concept_name="${concept_def%%:*}"
        local patterns="${concept_def#*:}"

        # Search for files matching the pattern (in file path only)
        local files=$(find "$PROJECT_ROOT" -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.py" -o -name "*.go" -o -name "*.rs" \) \
            -not -path "*/node_modules/*" \
            -not -path "*/.next/*" \
            -not -path "*/dist/*" \
            -not -path "*/build/*" \
            -not -path "*/__pycache__/*" \
            -not -path "*/target/*" \
            2>/dev/null | grep -iE "/($patterns)[^/]*$|/($patterns)/" | head -10)

        if [ -n "$files" ]; then
            # Convert to relative paths and join with commas
            local rel_files=""
            for f in $files; do
                local rel=$(echo "$f" | sed "s|^$PROJECT_ROOT/||")
                if [ -z "$rel_files" ]; then
                    rel_files="$rel"
                else
                    rel_files="$rel_files,$rel"
                fi
            done
            echo "$concept_name:$rel_files" >> "$CONCEPTS_TMP"
        fi
    done
}

# ============================================================================
# ENTRY POINT EXTRACTION
# Finds API routes, CLI commands, and main entry points
# ============================================================================

extract_entry_points_nextjs() {
    echo "Extracting Next.js API routes..."

    # Find App Router API routes
    find "$PROJECT_ROOT/src/app" "$PROJECT_ROOT/app" -name "route.ts" -o -name "route.js" 2>/dev/null | while read -r file; do
        # Extract the route path from file location (macOS compatible)
        local route_path=$(echo "$file" | sed -E 's|.*/app/api||' | sed -E 's|/route\.ts$||' | sed -E 's|/route\.js$||' | sed -E 's|\[([^]]+)\]|:\1|g')

        # Find HTTP methods defined in the file
        local methods=$(grep -oE "export (async )?function (GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)" "$file" 2>/dev/null | grep -oE "(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)" | sort -u)

        for method in $methods; do
            # Find line number of the handler
            local line=$(grep -n "export.*function $method" "$file" 2>/dev/null | head -1 | cut -d: -f1)
            local rel_path=$(echo "$file" | sed "s|$PROJECT_ROOT/||")
            echo "$method /api$route_path:$rel_path:$line" >> "$ENTRY_POINTS_TMP"
        done
    done

    # Find Pages Router API routes
    find "$PROJECT_ROOT/src/pages/api" "$PROJECT_ROOT/pages/api" -name "*.ts" -o -name "*.js" 2>/dev/null | while read -r file; do
        local route_path=$(echo "$file" | sed -E 's|.*/pages/api||; s|\.(ts|js)$||; s|\[([^]]+)\]|:\1|g; s|/index$||')
        local rel_path=$(echo "$file" | sed "s|$PROJECT_ROOT/||")
        echo "* /api$route_path:$rel_path:1" >> "$ENTRY_POINTS_TMP"
    done
}

extract_entry_points_express() {
    echo "Extracting Express routes..."

    # Find route definitions
    grep -rn --include="*.ts" --include="*.js" -E "(app|router)\.(get|post|put|patch|delete|all)\s*\(" "$PROJECT_ROOT" 2>/dev/null \
        | grep -v node_modules \
        | while read -r line; do
            local file=$(echo "$line" | cut -d: -f1)
            local lineno=$(echo "$line" | cut -d: -f2)
            local method=$(echo "$line" | grep -oE "\.(get|post|put|patch|delete|all)" | tr -d '.' | tr '[:lower:]' '[:upper:]')
            local path=$(echo "$line" | grep -oE "['\"][^'\"]+['\"]" | head -1 | tr -d "'" | tr -d '"')
            local rel_path=$(echo "$file" | sed "s|$PROJECT_ROOT/||")

            if [ -n "$path" ]; then
                echo "$method $path:$rel_path:$lineno" >> "$ENTRY_POINTS_TMP"
            fi
        done
}

extract_entry_points_python() {
    echo "Extracting Python routes..."

    # FastAPI routes
    grep -rn --include="*.py" -E "@(app|router)\.(get|post|put|patch|delete)\s*\(" "$PROJECT_ROOT" 2>/dev/null \
        | grep -v __pycache__ \
        | while read -r line; do
            local file=$(echo "$line" | cut -d: -f1)
            local lineno=$(echo "$line" | cut -d: -f2)
            local method=$(echo "$line" | grep -oE "\.(get|post|put|patch|delete)" | tr -d '.' | tr '[:lower:]' '[:upper:]')
            local path=$(echo "$line" | grep -oE "['\"][^'\"]+['\"]" | head -1 | tr -d "'" | tr -d '"')
            local rel_path=$(echo "$file" | sed "s|$PROJECT_ROOT/||")

            if [ -n "$path" ]; then
                echo "$method $path:$rel_path:$lineno" >> "$ENTRY_POINTS_TMP"
            fi
        done

    # Flask routes
    grep -rn --include="*.py" -E "@(app|bp|blueprint)\.route\s*\(" "$PROJECT_ROOT" 2>/dev/null \
        | grep -v __pycache__ \
        | while read -r line; do
            local file=$(echo "$line" | cut -d: -f1)
            local lineno=$(echo "$line" | cut -d: -f2)
            local path=$(echo "$line" | grep -oE "['\"][^'\"]+['\"]" | head -1 | tr -d "'" | tr -d '"')
            local rel_path=$(echo "$file" | sed "s|$PROJECT_ROOT/||")

            if [ -n "$path" ]; then
                echo "* $path:$rel_path:$lineno" >> "$ENTRY_POINTS_TMP"
            fi
        done
}

extract_entry_points() {
    case "$PROJECT_TYPE" in
        nextjs) extract_entry_points_nextjs ;;
        express|node) extract_entry_points_express ;;
        python) extract_entry_points_python ;;
    esac
}

# ============================================================================
# EXPORT EXTRACTION
# Maps files to their exported symbols
# ============================================================================

extract_exports_typescript() {
    echo "Extracting TypeScript/JavaScript exports..."

    find "$PROJECT_ROOT" -type f \( -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \) \
        -not -path "*/node_modules/*" \
        -not -path "*/.next/*" \
        -not -path "*/dist/*" \
        -not -path "*/*.spec.*" \
        -not -path "*/*.test.*" \
        2>/dev/null | while read -r file; do

        # Extract named exports
        local exports=$(grep -oE "export (const|let|var|function|class|type|interface|enum) [a-zA-Z_][a-zA-Z0-9_]*" "$file" 2>/dev/null \
            | sed -E 's/export (const|let|var|function|class|type|interface|enum) //' \
            | sort -u \
            | tr '\n' ',' \
            | sed 's/,$//')

        # Also get export { ... } style exports
        local named_exports=$(grep -oE "export \{[^}]+\}" "$file" 2>/dev/null \
            | sed 's/export {//; s/}//; s/,/ /g; s/as [^ ]*//g' \
            | tr -s ' ' '\n' \
            | grep -v '^$' \
            | sort -u \
            | tr '\n' ',' \
            | sed 's/,$//')

        # Combine exports
        if [ -n "$exports" ] && [ -n "$named_exports" ]; then
            exports="$exports,$named_exports"
        elif [ -n "$named_exports" ]; then
            exports="$named_exports"
        fi

        if [ -n "$exports" ]; then
            local rel_path=$(echo "$file" | sed "s|$PROJECT_ROOT/||")
            echo "$rel_path:$exports" >> "$EXPORTS_TMP"
        fi
    done
}

extract_exports_python() {
    echo "Extracting Python exports..."

    find "$PROJECT_ROOT" -type f -name "*.py" \
        -not -path "*/__pycache__/*" \
        -not -path "*/venv/*" \
        -not -path "*/.venv/*" \
        -not -name "test_*.py" \
        -not -name "*_test.py" \
        2>/dev/null | while read -r file; do

        # Get __all__ if defined
        local all_exports=$(grep -oE "__all__\s*=\s*\[[^\]]+\]" "$file" 2>/dev/null \
            | grep -oE "['\"][^'\"]+['\"]" \
            | tr -d "'" \
            | tr -d '"' \
            | tr '\n' ',' \
            | sed 's/,$//')

        # Fallback to top-level function/class definitions
        if [ -z "$all_exports" ]; then
            all_exports=$(grep -E "^(def|class|async def) [a-zA-Z_][a-zA-Z0-9_]*" "$file" 2>/dev/null \
                | grep -v "^def _" \
                | sed -E 's/^(def|class|async def) ([a-zA-Z_][a-zA-Z0-9_]*).*/\2/' \
                | sort -u \
                | tr '\n' ',' \
                | sed 's/,$//')
        fi

        if [ -n "$all_exports" ]; then
            local rel_path=$(echo "$file" | sed "s|$PROJECT_ROOT/||")
            echo "$rel_path:$all_exports" >> "$EXPORTS_TMP"
        fi
    done
}

extract_exports() {
    case "$PROJECT_TYPE" in
        nextjs|express|node) extract_exports_typescript ;;
        python) extract_exports_python ;;
    esac
}

# ============================================================================
# TYPE EXTRACTION
# Maps type/interface/class names to definition locations
# ============================================================================

extract_types_typescript() {
    echo "Extracting TypeScript types..."

    find "$PROJECT_ROOT" -type f \( -name "*.ts" -o -name "*.tsx" \) \
        -not -path "*/node_modules/*" \
        -not -path "*/.next/*" \
        -not -path "*/dist/*" \
        2>/dev/null | while read -r file; do

        # Extract type, interface, and enum definitions
        grep -nE "^export (type|interface|enum|class) [A-Z][a-zA-Z0-9_]*" "$file" 2>/dev/null | while read -r match; do
            local lineno=$(echo "$match" | cut -d: -f1)
            local name=$(echo "$match" | grep -oE "(type|interface|enum|class) [A-Z][a-zA-Z0-9_]*" | awk '{print $2}')
            local rel_path=$(echo "$file" | sed "s|$PROJECT_ROOT/||")

            if [ -n "$name" ]; then
                echo "$name:$rel_path:$lineno" >> "$TYPES_TMP"
            fi
        done
    done
}

extract_types_python() {
    echo "Extracting Python types..."

    find "$PROJECT_ROOT" -type f -name "*.py" \
        -not -path "*/__pycache__/*" \
        -not -path "*/venv/*" \
        -not -path "*/.venv/*" \
        2>/dev/null | while read -r file; do

        # Extract class definitions (as types) and TypedDict
        grep -nE "^class [A-Z][a-zA-Z0-9_]*|^[A-Z][a-zA-Z0-9_]*\s*=\s*TypedDict" "$file" 2>/dev/null | while read -r match; do
            local lineno=$(echo "$match" | cut -d: -f1)
            local name=$(echo "$match" | grep -oE "class [A-Z][a-zA-Z0-9_]*|^[A-Z][a-zA-Z0-9_]*" | head -1 | sed 's/class //')
            local rel_path=$(echo "$file" | sed "s|$PROJECT_ROOT/||")

            if [ -n "$name" ]; then
                echo "$name:$rel_path:$lineno" >> "$TYPES_TMP"
            fi
        done
    done
}

extract_types() {
    case "$PROJECT_TYPE" in
        nextjs|express|node) extract_types_typescript ;;
        python) extract_types_python ;;
    esac
}

# ============================================================================
# JSON OUTPUT GENERATION
# ============================================================================

generate_json() {
    echo "Generating JSON output..."

    # Start JSON
    cat > "$OUTPUT_FILE" << 'EOF'
{
  "version": "1.0",
EOF
    echo "  \"generated\": $(date +%s)," >> "$OUTPUT_FILE"
    echo "  \"project_type\": \"$PROJECT_TYPE\"," >> "$OUTPUT_FILE"

    # Concepts
    echo '  "concepts": {' >> "$OUTPUT_FILE"
    local first=true
    while IFS=: read -r concept files; do
        if [ -n "$concept" ] && [ -n "$files" ]; then
            if [ "$first" = true ]; then
                first=false
            else
                echo "," >> "$OUTPUT_FILE"
            fi
            # Convert comma-separated file list to JSON array
            local json_files=$(echo "$files" | sed 's/,/", "/g')
            printf '    "%s": ["%s"]' "$concept" "$json_files" >> "$OUTPUT_FILE"
        fi
    done < "$CONCEPTS_TMP"
    echo '' >> "$OUTPUT_FILE"
    echo '  },' >> "$OUTPUT_FILE"

    # Entry points
    echo '  "entry_points": {' >> "$OUTPUT_FILE"
    first=true
    while IFS=: read -r route file line; do
        if [ -n "$route" ]; then
            if [ "$first" = true ]; then
                first=false
            else
                echo "," >> "$OUTPUT_FILE"
            fi
            printf '    "%s": "%s:%s"' "$route" "$file" "$line" >> "$OUTPUT_FILE"
        fi
    done < "$ENTRY_POINTS_TMP"
    echo '' >> "$OUTPUT_FILE"
    echo '  },' >> "$OUTPUT_FILE"

    # Exports
    echo '  "exports": {' >> "$OUTPUT_FILE"
    first=true
    while IFS=: read -r file exports; do
        if [ -n "$file" ] && [ -n "$exports" ]; then
            if [ "$first" = true ]; then
                first=false
            else
                echo "," >> "$OUTPUT_FILE"
            fi
            local json_exports=$(echo "$exports" | sed 's/,/", "/g')
            printf '    "%s": ["%s"]' "$file" "$json_exports" >> "$OUTPUT_FILE"
        fi
    done < "$EXPORTS_TMP"
    echo '' >> "$OUTPUT_FILE"
    echo '  },' >> "$OUTPUT_FILE"

    # Types
    echo '  "types": {' >> "$OUTPUT_FILE"
    first=true
    while IFS=: read -r name file line; do
        if [ -n "$name" ]; then
            if [ "$first" = true ]; then
                first=false
            else
                echo "," >> "$OUTPUT_FILE"
            fi
            printf '    "%s": "%s:%s"' "$name" "$file" "$line" >> "$OUTPUT_FILE"
        fi
    done < "$TYPES_TMP"
    echo '' >> "$OUTPUT_FILE"
    echo '  }' >> "$OUTPUT_FILE"

    echo '}' >> "$OUTPUT_FILE"
}

# ============================================================================
# MAIN
# ============================================================================

echo "Generating code index for: $PROJECT_ROOT"
echo "Output: $OUTPUT_FILE"
echo ""

extract_concepts
extract_entry_points
extract_exports
extract_types
generate_json

echo ""
echo "Done! Generated $OUTPUT_FILE"
echo ""

# Show stats
echo "Stats:"
echo "  Concepts: $(wc -l < "$CONCEPTS_TMP" | tr -d ' ')"
echo "  Entry points: $(wc -l < "$ENTRY_POINTS_TMP" | tr -d ' ')"
echo "  Files with exports: $(wc -l < "$EXPORTS_TMP" | tr -d ' ')"
echo "  Types: $(wc -l < "$TYPES_TMP" | tr -d ' ')"
