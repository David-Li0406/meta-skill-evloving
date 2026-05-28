# Integration Patterns for Scripts and Skills

Best practices for using VSCode CLI in automation, scripts, and Claude skills.

## Safe File Opening Pattern

**Always validate before opening:**

```bash
FILE_PATH="$1"
LINE="${2:-1}"
COLUMN="${3:-0}"

# Validation
if [[ ! -f "$FILE_PATH" ]]; then
    echo "Error: File not found: $FILE_PATH" >&2
    exit 1
fi

# Convert to absolute path
ABS_PATH="$(cd "$(dirname "$FILE_PATH")" && pwd)/$(basename "$FILE_PATH")"

# Open safely
code -g "$ABS_PATH:$LINE:$COLUMN"
```

## Error Location Navigation

**Open file at compiler/linter error location:**

```bash
# Parse error output
ERROR_FILE="src/main.c"
ERROR_LINE="42"
ERROR_COL="15"

# Open at exact error location
echo "Opening error location: $ERROR_FILE:$ERROR_LINE:$ERROR_COL"
code -g "$ERROR_FILE:$ERROR_LINE:$ERROR_COL"
```

## TODO Finding and Navigation

**Search for TODOs and open at location:**

```bash
# Find all TODO(human) markers
grep -n "TODO(human)" *.py | while IFS=: read -r file line content; do
    echo "$file:$line - $content"
done

# Open specific TODO
code -g publisher.py:36
```

**Interactive TODO selection:**

```bash
# Create numbered list
grep -n "TODO" *.js | nl

# User selects number, open that file:line
selected_todo=$(grep -n "TODO" *.js | sed -n "${TODO_NUM}p")
file=$(echo "$selected_todo" | cut -d: -f1)
line=$(echo "$selected_todo" | cut -d: -f2)

code -g "$file:$line"
```

## Relative to Absolute Path Conversion

**Ensure reliable path resolution:**

```bash
# Convert relative path to absolute
to_absolute_path() {
    local path="$1"

    if [[ "$path" = /* ]]; then
        # Already absolute
        echo "$path"
    else
        # Convert to absolute
        echo "$(cd "$(dirname "$path")" && pwd)/$(basename "$path")"
    fi
}

# Usage
ABS_FILE=$(to_absolute_path "$RELATIVE_FILE")
code -g "$ABS_FILE:$LINE"
```

## Path with Spaces Handling

**Always quote paths:**

```bash
# Safe quoting function
open_at_line() {
    local file="$1"
    local line="$2"

    # Quote the entire file:line argument
    code -g "$file:$line"
}

# Usage
open_at_line "my project/src/app.js" 42
```

## Multiple File Opening with Context

**Open related files with informative output:**

```bash
echo "Opening MQTT publisher and subscriber files:"

echo "  - Publisher TODO at line 36 (connection setup)"
code -g PiPico/publisher.py:36

echo "  - Subscriber TODO at line 45 (callback implementation)"
code -g PiPico/subscriber.py:45
```

## Window Behavior for Skills

**Avoid disrupting user's current work:**

```bash
# Option 1: New window (safest, doesn't disturb current work)
code -n -g "$FILE:$LINE"

# Option 2: Reuse window (convenient, adds as tab)
code -r -g "$FILE:$LINE"

# Option 3: Default behavior (reuses window)
code -g "$FILE:$LINE"
```

**Recommendation for skills:** Use default behavior (no -n or -r) to match user expectations.

## Error Handling Wrapper

**Comprehensive error handling:**

```bash
safe_open_code() {
    local file="$1"
    local line="${2:-1}"
    local col="${3:-0}"

    # Validate file exists
    if [[ ! -f "$file" ]]; then
        echo "Error: File not found: $file" >&2
        return 1
    fi

    # Validate line is a number
    if ! [[ "$line" =~ ^[0-9]+$ ]]; then
        echo "Error: Line must be a number: $line" >&2
        return 1
    fi

    # Validate column is a number
    if ! [[ "$col" =~ ^[0-9]+$ ]]; then
        echo "Error: Column must be a number: $col" >&2
        return 1
    fi

    # Convert to absolute path
    local abs_path
    abs_path="$(cd "$(dirname "$file")" && pwd)/$(basename "$file")"

    # Open with error handling
    if ! code -g "$abs_path:$line:$col"; then
        echo "Error: Failed to open file in VSCode" >&2
        return 1
    fi

    echo "Opened $file at line $line, column $col"
    return 0
}

# Usage
safe_open_code "src/app.js" 42 10
```

## Grep Integration

**Open grep results at specific line:**

```bash
# Search for pattern and open matches
pattern="$1"
grep -n "$pattern" *.js | while IFS=: read -r file line content; do
    echo "Found in $file at line $line: $content"
    read -p "Open this file? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        code -g "$file:$line"
    fi
done
```

## Git Diff Integration

**Open files with changes:**

```bash
# Get list of changed files
git diff --name-only | while read -r file; do
    # Get first changed line number
    first_change=$(git diff "$file" | grep -m1 "^@@" | \
                   sed 's/^@@ -[0-9,]* +\([0-9]*\).*/\1/')

    if [[ -n "$first_change" ]]; then
        echo "Opening $file at line $first_change (first change)"
        code -g "$file:$first_change"
    fi
done
```

## Context Provision

**Always provide context when opening files:**

```bash
# Good: Tells user why file is being opened
echo "Opening authentication logic at the security vulnerability (line 42)"
code -g src/auth.js:42

# Good: Explains what's at this location
echo "Opening publisher.py at line 36 (MQTT connection TODO)"
code -g publisher.py:36

# Less helpful: No context
code -g file.js:42
```

## Batch Opening with Delays

**Avoid overwhelming user with many files:**

```bash
files_to_open=(
    "file1.js:10"
    "file2.js:20"
    "file3.js:30"
)

for file_spec in "${files_to_open[@]}"; do
    echo "Opening $file_spec"
    code -g "$file_spec"
    sleep 0.5  # Brief delay between opens
done
```

## Platform Detection

**Handle different operating systems:**

```bash
# Detect platform and adjust accordingly
case "$(uname -s)" in
    Linux*)     editor_cmd="code" ;;
    Darwin*)    editor_cmd="code" ;;  # macOS
    CYGWIN*|MINGW*|MSYS*)
        # Windows with Git Bash
        editor_cmd="code"
        ;;
    *)
        echo "Unknown platform" >&2
        exit 1
        ;;
esac

# Use detected command
"$editor_cmd" -g "$FILE:$LINE"
```
