#!/bin/bash
# shellcheck shell=bash
# resolve-reference.sh — Resolve framework reference IDs to content
# Part of the Dialogue Framework
# Usage: resolve-reference.sh <id> [output_format]

set -euo pipefail

# Use Claude's project directory environment variable
PROJECT_ROOT="${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR must be set}"

# Artifact locations
# These can be customised per project via .dialogue/config.yaml
# TODO: Implement config file parsing when yq/similar available
#
# Current settings are for this project (framework development).
# Typical deployments would use docs/ for THY/REF/STR documents.
THEORY_DIR="implementation"
THEORY_PATTERN="theory_*.md"
REF_DIR="implementation"
REF_PATTERN="ref_*.md"
STR_DIR="implementation"
STR_PATTERN="str_*.md"
ADR_DIR="decisions"
ADR_PATTERN="ADR-*.md"
# Per-file log structure (FW-017)
DECISIONS_DIR=".dialogue/logs/decisions"
OBSERVATIONS_DIR=".dialogue/logs/observations"
TASKS_DIR=".dialogue/tasks"
# Process execution structure (FW-011)
PROCESSES_DEF_DIR="claude-plugin-evo/processes"
PROCESSES_INST_DIR=".dialogue/processes"
EXECUTIONS_DIR=".dialogue/logs/executions"

# Validate required arguments
if [[ $# -lt 1 ]]; then
    echo "Usage: resolve-reference.sh <id> [output_format]" >&2
    echo "  id:            Reference ID (e.g., THY-001, DEC-20260114-091633)" >&2
    echo "  output_format: full | metadata | path (default: full)" >&2
    exit 1
fi

ID="$1"
OUTPUT_FORMAT="${2:-full}"

# Validate output format
if [[ "$OUTPUT_FORMAT" != "full" && "$OUTPUT_FORMAT" != "metadata" && "$OUTPUT_FORMAT" != "path" ]]; then
    echo '{"status": "ERROR", "error": "output_format must be full, metadata, or path"}' >&2
    exit 1
fi

# Helper: JSON escape string
json_escape() {
    local s="$1"
    s="${s//\\/\\\\}"
    s="${s//\"/\\\"}"
    s="${s//$'\n'/\\n}"
    s="${s//$'\r'/\\r}"
    s="${s//$'\t'/\\t}"
    printf '%s' "$s"
}

# Helper: Output success result
output_success() {
    local id="$1"
    local type="$2"
    local location="$3"
    local content="${4:-}"

    if [[ "$OUTPUT_FORMAT" == "path" ]]; then
        echo "$location"
        return
    fi

    local escaped_content
    escaped_content=$(json_escape "$content")

    if [[ "$OUTPUT_FORMAT" == "metadata" ]]; then
        cat <<EOF
{
  "status": "RESOLVED",
  "id": "$id",
  "type": "$type",
  "location": "$location"
}
EOF
    else
        cat <<EOF
{
  "status": "RESOLVED",
  "id": "$id",
  "type": "$type",
  "location": "$location",
  "content": "$escaped_content"
}
EOF
    fi
}

# Helper: Output not found result
output_not_found() {
    local id="$1"
    local type="$2"
    local searched="$3"

    cat <<EOF
{
  "status": "NOT_FOUND",
  "id": "$id",
  "type": "$type",
  "error": "No content matching pattern found",
  "searched": $searched
}
EOF
}

# Helper: Output not supported result (framework source references)
output_not_supported() {
    local id="$1"
    local type="$2"

    cat <<EOF
{
  "status": "NOT_SUPPORTED",
  "id": "$id",
  "type": "$type",
  "error": "Framework source reference - not resolvable at runtime",
  "note": "F-N, C-N, I-N, G-N, E-N reference framework documentation, not project artifacts."
}
EOF
}

# Helper: Output invalid ID result
output_invalid_id() {
    local id="$1"

    cat <<EOF
{
  "status": "INVALID_ID",
  "id": "$id",
  "error": "ID does not match any known pattern",
  "known_patterns": [
    "THY-NNN: Theory documents",
    "REF-NNN: Reference documents",
    "STR-NNN: Strategy documents",
    "ADR-NNN: Architecture Decision Records",
    "F-N, C-N, I-N, G-N, E-N: Concept documents",
    "DEC-YYYYMMDD-HHMMSS: Decision log entries",
    "OBS-YYYYMMDD-HHMMSS: Observation log entries",
    "SH-NNN, CD-NNN, FW-NNN: Tasks",
    "PROC-P.S: Process definitions",
    "PINST-YYYYMMDD-HHMMSS: Process instances",
    "EXEC-YYYYMMDD-HHMMSS: Execution logs",
    "human:<id>, ai:<id>: Actors"
  ]
}
EOF
}

# Resolve based on ID pattern
resolve_id() {
    local id="$1"

    # Check for external URLs first
    if [[ "$id" =~ ^https?:// ]]; then
        cat <<EOF
{
  "status": "EXTERNAL",
  "id": "$id",
  "type": "URL",
  "note": "External URLs are not resolved; use WebFetch"
}
EOF
        return
    fi

    # Actor references
    if [[ "$id" =~ ^human:([a-zA-Z0-9_-]+)$ ]]; then
        local actor_id="${BASH_REMATCH[1]}"
        cat <<EOF
{
  "status": "RESOLVED",
  "id": "$id",
  "type": "ACTOR_HUMAN",
  "metadata": {
    "actor_type": "human",
    "identifier": "$actor_id"
  },
  "note": "Actor references resolve to metadata only"
}
EOF
        return
    fi

    if [[ "$id" =~ ^ai:([a-zA-Z0-9_-]+)$ ]]; then
        local actor_id="${BASH_REMATCH[1]}"
        cat <<EOF
{
  "status": "RESOLVED",
  "id": "$id",
  "type": "ACTOR_AI",
  "metadata": {
    "actor_type": "ai",
    "identifier": "$actor_id"
  },
  "note": "Actor references resolve to metadata only"
}
EOF
        return
    fi

    # Theory documents: THY-NNN
    if [[ "$id" =~ ^THY-([0-9]+)$ ]]; then
        local num="${BASH_REMATCH[1]}"
        local pattern="$THEORY_DIR/$THEORY_PATTERN"

        # Look for file containing THY-NNN in content or matching pattern
        local found_file=""
        while IFS= read -r -d '' file; do
            if grep -q "^# THY-$num:" "$file" 2>/dev/null || \
               grep -q "THY-$num" "$file" 2>/dev/null; then
                found_file="$file"
                break
            fi
        done < <(find "$PROJECT_ROOT/$THEORY_DIR" -name "$THEORY_PATTERN" -print0 2>/dev/null)

        if [[ -n "$found_file" ]]; then
            local rel_path="${found_file#$PROJECT_ROOT/}"
            local content
            content=$(cat "$found_file")
            output_success "$id" "DOCUMENT" "$rel_path" "$content"
        else
            output_not_found "$id" "DOCUMENT" "[\"$pattern\"]"
        fi
        return
    fi

    # Reference documents: REF-NNN
    if [[ "$id" =~ ^REF-([0-9]+)$ ]]; then
        local num="${BASH_REMATCH[1]}"
        local pattern="$REF_DIR/$REF_PATTERN"

        local found_file=""
        while IFS= read -r -d '' file; do
            if grep -q "^# REF-$num:" "$file" 2>/dev/null || \
               grep -q "REF-$num" "$file" 2>/dev/null; then
                found_file="$file"
                break
            fi
        done < <(find "$PROJECT_ROOT/$REF_DIR" -name "$REF_PATTERN" -print0 2>/dev/null)

        if [[ -n "$found_file" ]]; then
            local rel_path="${found_file#$PROJECT_ROOT/}"
            local content
            content=$(cat "$found_file")
            output_success "$id" "DOCUMENT" "$rel_path" "$content"
        else
            output_not_found "$id" "DOCUMENT" "[\"$pattern\"]"
        fi
        return
    fi

    # Strategy documents: STR-NNN
    if [[ "$id" =~ ^STR-([0-9]+)$ ]]; then
        local num="${BASH_REMATCH[1]}"
        local pattern="$STR_DIR/$STR_PATTERN"

        local found_file=""
        while IFS= read -r -d '' file; do
            if grep -q "^# STR-$num:" "$file" 2>/dev/null || \
               grep -q "STR-$num" "$file" 2>/dev/null; then
                found_file="$file"
                break
            fi
        done < <(find "$PROJECT_ROOT/$STR_DIR" -name "$STR_PATTERN" -print0 2>/dev/null)

        if [[ -n "$found_file" ]]; then
            local rel_path="${found_file#$PROJECT_ROOT/}"
            local content
            content=$(cat "$found_file")
            output_success "$id" "DOCUMENT" "$rel_path" "$content"
        else
            output_not_found "$id" "DOCUMENT" "[\"$pattern\"]"
        fi
        return
    fi

    # ADR documents: ADR-NNN
    if [[ "$id" =~ ^ADR-([0-9]+)$ ]]; then
        local num="${BASH_REMATCH[1]}"
        local padded_num
        padded_num=$(printf "%03d" "$num")
        local pattern="$ADR_DIR/ADR-$padded_num-*.md"

        local found_file=""
        if compgen -G "$PROJECT_ROOT/$ADR_DIR/ADR-$padded_num-*.md" > /dev/null 2>&1; then
            found_file=$(ls -1 "$PROJECT_ROOT/$ADR_DIR/ADR-$padded_num-"*.md 2>/dev/null | head -1)
        fi

        if [[ -n "$found_file" && -f "$found_file" ]]; then
            local rel_path="${found_file#$PROJECT_ROOT/}"
            local content
            content=$(cat "$found_file")
            output_success "$id" "ADR" "$rel_path" "$content"
        else
            output_not_found "$id" "ADR" "[\"$pattern\"]"
        fi
        return
    fi

    # Framework source references: F-N, C-N, I-N, G-N, E-N
    # These reference framework documentation, not project artifacts
    if [[ "$id" =~ ^F-([0-9]+)$ ]]; then
        output_not_supported "$id" "FOUNDATION"
        return
    fi

    if [[ "$id" =~ ^C-([0-9]+)$ ]]; then
        output_not_supported "$id" "CONCEPT"
        return
    fi

    if [[ "$id" =~ ^I-([0-9]+)$ ]]; then
        output_not_supported "$id" "INTEGRATION"
        return
    fi

    if [[ "$id" =~ ^G-([0-9]+)$ ]]; then
        output_not_supported "$id" "GUIDANCE"
        return
    fi

    if [[ "$id" =~ ^E-([0-9]+)$ ]]; then
        output_not_supported "$id" "EXAMPLE"
        return
    fi

    # Decision log entries: DEC-YYYYMMDD-HHMMSS
    if [[ "$id" =~ ^DEC-[0-9]{8}-[0-9]{6}$ ]]; then
        # Per-file structure (FW-017)
        local per_file="$PROJECT_ROOT/$DECISIONS_DIR/$id.yaml"
        local location="$DECISIONS_DIR/$id.yaml"

        if [[ -f "$per_file" ]]; then
            local entry
            entry=$(cat "$per_file")

            local escaped_entry
            escaped_entry=$(json_escape "$entry")
            if [[ "$OUTPUT_FORMAT" == "path" ]]; then
                echo "$location"
            elif [[ "$OUTPUT_FORMAT" == "metadata" ]]; then
                cat <<EOF
{
  "status": "RESOLVED",
  "id": "$id",
  "type": "DECISION",
  "location": "$location"
}
EOF
            else
                cat <<EOF
{
  "status": "RESOLVED",
  "id": "$id",
  "type": "DECISION",
  "location": "$location",
  "content": "$escaped_entry"
}
EOF
            fi
            return
        fi

        output_not_found "$id" "DECISION" "[\"$DECISIONS_DIR/$id.yaml\"]"
        return
    fi

    # Observation log entries: OBS-YYYYMMDD-HHMMSS
    if [[ "$id" =~ ^OBS-[0-9]{8}-[0-9]{6}$ ]]; then
        # Per-file structure (FW-017)
        local per_file="$PROJECT_ROOT/$OBSERVATIONS_DIR/$id.yaml"
        local location="$OBSERVATIONS_DIR/$id.yaml"

        if [[ -f "$per_file" ]]; then
            local entry
            entry=$(cat "$per_file")

            local escaped_entry
            escaped_entry=$(json_escape "$entry")
            if [[ "$OUTPUT_FORMAT" == "path" ]]; then
                echo "$location"
            elif [[ "$OUTPUT_FORMAT" == "metadata" ]]; then
                cat <<EOF
{
  "status": "RESOLVED",
  "id": "$id",
  "type": "OBSERVATION",
  "location": "$location"
}
EOF
            else
                cat <<EOF
{
  "status": "RESOLVED",
  "id": "$id",
  "type": "OBSERVATION",
  "location": "$location",
  "content": "$escaped_entry"
}
EOF
            fi
            return
        fi

        output_not_found "$id" "OBSERVATION" "[\"$OBSERVATIONS_DIR/$id.yaml\"]"
        return
    fi

    # Tasks: SH-NNN, CD-NNN, FW-NNN, DOC-NNN, VAL-NNN
    if [[ "$id" =~ ^(SH|CD|FW|DOC|VAL)-([0-9]+)$ ]]; then
        local prefix="${BASH_REMATCH[1]}"
        local num="${BASH_REMATCH[2]}"

        # Per-file structure (FW-017)
        local per_file="$PROJECT_ROOT/$TASKS_DIR/$id.yaml"
        local location="$TASKS_DIR/$id.yaml"

        if [[ -f "$per_file" ]]; then
            local entry
            entry=$(cat "$per_file")

            local escaped_entry
            escaped_entry=$(json_escape "$entry")
            if [[ "$OUTPUT_FORMAT" == "path" ]]; then
                echo "$location"
            elif [[ "$OUTPUT_FORMAT" == "metadata" ]]; then
                cat <<EOF
{
  "status": "RESOLVED",
  "id": "$id",
  "type": "TASK",
  "location": "$location"
}
EOF
            else
                cat <<EOF
{
  "status": "RESOLVED",
  "id": "$id",
  "type": "TASK",
  "location": "$location",
  "content": "$escaped_entry"
}
EOF
            fi
            return
        fi

        output_not_found "$id" "TASK" "[\"$TASKS_DIR/$id.yaml\"]"
        return
    fi

    # Process definitions: PROC-P.S (e.g., PROC-3.1)
    if [[ "$id" =~ ^PROC-([1-7])\.([0-9]+)$ ]]; then
        local phase="${BASH_REMATCH[1]}"
        local seq="${BASH_REMATCH[2]}"

        # Search for definition file containing this PROC ID
        local found_file=""
        local search_dir="$PROJECT_ROOT/$PROCESSES_DEF_DIR"

        if [[ -d "$search_dir" ]]; then
            while IFS= read -r -d '' file; do
                if grep -q "id:.*$id" "$file" 2>/dev/null || \
                   grep -q "id: \"$id\"" "$file" 2>/dev/null; then
                    found_file="$file"
                    break
                fi
            done < <(find "$search_dir" -name "process-*.yaml" -print0 2>/dev/null)
        fi

        if [[ -n "$found_file" ]]; then
            local rel_path="${found_file#$PROJECT_ROOT/}"
            local content
            content=$(cat "$found_file")
            output_success "$id" "PROCESS_DEFINITION" "$rel_path" "$content"
        else
            output_not_found "$id" "PROCESS_DEFINITION" "[\"$PROCESSES_DEF_DIR/process-*.yaml\"]"
        fi
        return
    fi

    # Process instances: PINST-YYYYMMDD-HHMMSS
    if [[ "$id" =~ ^PINST-[0-9]{8}-[0-9]{6}$ ]]; then
        local per_file="$PROJECT_ROOT/$PROCESSES_INST_DIR/$id.yaml"
        local location="$PROCESSES_INST_DIR/$id.yaml"

        if [[ -f "$per_file" ]]; then
            local entry
            entry=$(cat "$per_file")

            local escaped_entry
            escaped_entry=$(json_escape "$entry")
            if [[ "$OUTPUT_FORMAT" == "path" ]]; then
                echo "$location"
            elif [[ "$OUTPUT_FORMAT" == "metadata" ]]; then
                cat <<EOF
{
  "status": "RESOLVED",
  "id": "$id",
  "type": "PROCESS_INSTANCE",
  "location": "$location"
}
EOF
            else
                cat <<EOF
{
  "status": "RESOLVED",
  "id": "$id",
  "type": "PROCESS_INSTANCE",
  "location": "$location",
  "content": "$escaped_entry"
}
EOF
            fi
            return
        fi

        output_not_found "$id" "PROCESS_INSTANCE" "[\"$PROCESSES_INST_DIR/$id.yaml\"]"
        return
    fi

    # Execution logs: EXEC-YYYYMMDD-HHMMSS
    if [[ "$id" =~ ^EXEC-[0-9]{8}-[0-9]{6}$ ]]; then
        local per_file="$PROJECT_ROOT/$EXECUTIONS_DIR/$id.yaml"
        local location="$EXECUTIONS_DIR/$id.yaml"

        if [[ -f "$per_file" ]]; then
            local entry
            entry=$(cat "$per_file")

            local escaped_entry
            escaped_entry=$(json_escape "$entry")
            if [[ "$OUTPUT_FORMAT" == "path" ]]; then
                echo "$location"
            elif [[ "$OUTPUT_FORMAT" == "metadata" ]]; then
                cat <<EOF
{
  "status": "RESOLVED",
  "id": "$id",
  "type": "EXECUTION_LOG",
  "location": "$location"
}
EOF
            else
                cat <<EOF
{
  "status": "RESOLVED",
  "id": "$id",
  "type": "EXECUTION_LOG",
  "location": "$location",
  "content": "$escaped_entry"
}
EOF
            fi
            return
        fi

        output_not_found "$id" "EXECUTION_LOG" "[\"$EXECUTIONS_DIR/$id.yaml\"]"
        return
    fi

    # If we get here, ID didn't match any pattern
    output_invalid_id "$id"
}

# Main
resolve_id "$ID"
