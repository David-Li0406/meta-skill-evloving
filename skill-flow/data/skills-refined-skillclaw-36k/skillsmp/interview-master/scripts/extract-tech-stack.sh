#!/usr/bin/env bash

# extract-tech-stack.sh - Identify technologies from codebase
# Usage: ./extract-tech-stack.sh <repo-path> <author>

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

usage() {
    cat <<EOF
Usage: $0 <repo-path> <author>

Extract technology stack from git repository by analyzing files modified by author.

Arguments:
  repo-path   Path to git repository
  author      Author name or email

Examples:
  $0 /path/to/repo "Jane Doe"
  $0 /path/to/repo "jane@example.com"

Output:
  JSON formatted technology stack analysis
EOF
    exit 1
}

if [[ $# -lt 2 ]]; then
    usage
fi

REPO_PATH="$1"
AUTHOR="$2"

if [[ ! -d "$REPO_PATH/.git" ]]; then
    echo "Error: Not a git repository: $REPO_PATH" >&2
    exit 1
fi

cd "$REPO_PATH" || exit 1

echo -e "${GREEN}Extracting tech stack for author: $AUTHOR${NC}" >&2

# Get all files modified by author
FILES=$(git log --author="$AUTHOR" --name-only --pretty=format: --no-merges | sort | uniq | grep -v '^$')

# Count file extensions
declare -A EXTENSIONS
declare -A LANGUAGES
while IFS= read -r file; do
    if [[ -f "$file" ]]; then
        ext="${file##*.}"
        if [[ "$ext" != "$file" ]]; then
            EXTENSIONS[$ext]=$((${EXTENSIONS[$ext]:-0} + 1))
        fi
    fi
done <<< "$FILES"

# Map extensions to languages
for ext in "${!EXTENSIONS[@]}"; do
    case "$ext" in
        js) LANGUAGES["JavaScript"]=$((${LANGUAGES["JavaScript"]:-0} + ${EXTENSIONS[$ext]})) ;;
        ts) LANGUAGES["TypeScript"]=$((${LANGUAGES["TypeScript"]:-0} + ${EXTENSIONS[$ext]})) ;;
        tsx) LANGUAGES["TypeScript"]=$((${LANGUAGES["TypeScript"]:-0} + ${EXTENSIONS[$ext]})) ;;
        jsx) LANGUAGES["JavaScript"]=$((${LANGUAGES["JavaScript"]:-0} + ${EXTENSIONS[$ext]})) ;;
        py) LANGUAGES["Python"]=$((${LANGUAGES["Python"]:-0} + ${EXTENSIONS[$ext]})) ;;
        java) LANGUAGES["Java"]=$((${LANGUAGES["Java"]:-0} + ${EXTENSIONS[$ext]})) ;;
        go) LANGUAGES["Go"]=$((${LANGUAGES["Go"]:-0} + ${EXTENSIONS[$ext]})) ;;
        rs) LANGUAGES["Rust"]=$((${LANGUAGES["Rust"]:-0} + ${EXTENSIONS[$ext]})) ;;
        rb) LANGUAGES["Ruby"]=$((${LANGUAGES["Ruby"]:-0} + ${EXTENSIONS[$ext]})) ;;
        php) LANGUAGES["PHP"]=$((${LANGUAGES["PHP"]:-0} + ${EXTENSIONS[$ext]})) ;;
        cs) LANGUAGES["C#"]=$((${LANGUAGES["C#"]:-0} + ${EXTENSIONS[$ext]})) ;;
        cpp|cc|cxx) LANGUAGES["C++"]=$((${LANGUAGES["C++"]:-0} + ${EXTENSIONS[$ext]})) ;;
        c|h) LANGUAGES["C"]=$((${LANGUAGES["C"]:-0} + ${EXTENSIONS[$ext]})) ;;
        swift) LANGUAGES["Swift"]=$((${LANGUAGES["Swift"]:-0} + ${EXTENSIONS[$ext]})) ;;
        kt|kts) LANGUAGES["Kotlin"]=$((${LANGUAGES["Kotlin"]:-0} + ${EXTENSIONS[$ext]})) ;;
        scala) LANGUAGES["Scala"]=$((${LANGUAGES["Scala"]:-0} + ${EXTENSIONS[$ext]})) ;;
        dart) LANGUAGES["Dart"]=$((${LANGUAGES["Dart"]:-0} + ${EXTENSIONS[$ext]})) ;;
        sql) LANGUAGES["SQL"]=$((${LANGUAGES["SQL"]:-0} + ${EXTENSIONS[$ext]})) ;;
        sh|bash) LANGUAGES["Shell"]=$((${LANGUAGES["Shell"]:-0} + ${EXTENSIONS[$ext]})) ;;
    esac
done

# Detect frameworks from package files
declare -A FRAMEWORKS
if [[ -f "package.json" ]]; then
    if grep -q '"react"' package.json 2>/dev/null; then
        FRAMEWORKS["React"]=1.0
    fi
    if grep -q '"next"' package.json 2>/dev/null; then
        FRAMEWORKS["Next.js"]=1.0
    fi
    if grep -q '"vue"' package.json 2>/dev/null; then
        FRAMEWORKS["Vue.js"]=1.0
    fi
    if grep -q '"@angular' package.json 2>/dev/null; then
        FRAMEWORKS["Angular"]=1.0
    fi
    if grep -q '"express"' package.json 2>/dev/null; then
        FRAMEWORKS["Express.js"]=1.0
    fi
    if grep -q '"nestjs' package.json 2>/dev/null; then
        FRAMEWORKS["NestJS"]=1.0
    fi
fi

if [[ -f "requirements.txt" ]]; then
    if grep -q 'django' requirements.txt 2>/dev/null; then
        FRAMEWORKS["Django"]=1.0
    fi
    if grep -q 'flask' requirements.txt 2>/dev/null; then
        FRAMEWORKS["Flask"]=1.0
    fi
    if grep -q 'fastapi' requirements.txt 2>/dev/null; then
        FRAMEWORKS["FastAPI"]=1.0
    fi
fi

# Detect databases
declare -A DATABASES
if [[ -f "package.json" ]]; then
    grep -q '"pg"' package.json 2>/dev/null && DATABASES["PostgreSQL"]=1.0
    grep -q '"mysql' package.json 2>/dev/null && DATABASES["MySQL"]=1.0
    grep -q '"mongodb' package.json 2>/dev/null && DATABASES["MongoDB"]=1.0
    grep -q '"redis"' package.json 2>/dev/null && DATABASES["Redis"]=1.0
fi

if [[ -f "requirements.txt" ]]; then
    grep -q 'psycopg2' requirements.txt 2>/dev/null && DATABASES["PostgreSQL"]=1.0
    grep -q 'pymongo' requirements.txt 2>/dev/null && DATABASES["MongoDB"]=1.0
    grep -q 'redis' requirements.txt 2>/dev/null && DATABASES["Redis"]=1.0
fi

# Detect DevOps tools
declare -A TOOLS
[[ -f "Dockerfile" ]] && TOOLS["Docker"]=1.0
[[ -f "docker-compose.yml" ]] && TOOLS["Docker Compose"]=1.0
[[ -d ".github/workflows" ]] && TOOLS["GitHub Actions"]=1.0
[[ -f ".gitlab-ci.yml" ]] && TOOLS["GitLab CI"]=1.0
[[ -f "Jenkinsfile" ]] && TOOLS["Jenkins"]=1.0

# Output JSON
cat <<EOF
{
  "languages": [
$(
    total_files=0
    for count in "${LANGUAGES[@]}"; do
        total_files=$((total_files + count))
    done
    first=true
    for lang in "${!LANGUAGES[@]}"; do
        count=${LANGUAGES[$lang]}
        percentage=$(awk "BEGIN {printf \"%.1f\", ($count / $total_files) * 100}")
        [[ "$first" == true ]] && first=false || echo ","
        echo -n "    {\"name\": \"$lang\", \"file_count\": $count, \"percentage\": $percentage}"
    done
    echo
)
  ],
  "frameworks": [
$(
    first=true
    for fw in "${!FRAMEWORKS[@]}"; do
        [[ "$first" == true ]] && first=false || echo ","
        echo -n "    {\"name\": \"$fw\", \"confidence\": ${FRAMEWORKS[$fw]}}"
    done
    echo
)
  ],
  "databases": [
$(
    first=true
    for db in "${!DATABASES[@]}"; do
        [[ "$first" == true ]] && first=false || echo ","
        echo -n "    {\"name\": \"$db\", \"confidence\": ${DATABASES[$db]}}"
    done
    echo
)
  ],
  "tools": [
$(
    first=true
    for tool in "${!TOOLS[@]}"; do
        [[ "$first" == true ]] && first=false || echo ","
        echo -n "    {\"name\": \"$tool\", \"confidence\": ${TOOLS[$tool]}}"
    done
    echo
)
  ]
}
EOF

echo -e "${GREEN}✓ Tech stack extraction complete!${NC}" >&2
