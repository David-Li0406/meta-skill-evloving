#!/bin/bash
#
# List Docs - 프로젝트의 마크다운 문서 목록을 TOON 포맷으로 출력
# TOON: Token-Oriented Object Notation (https://github.com/toon-format/toon)

set -euo pipefail

# .claude/skills/list-docs/ 에 설치된다고 가정
PROJECT_ROOT="$(cd "$(dirname "$0")/../../../" && pwd)"

# Default options
TARGET_PATH=""

# YAML frontmatter에서 description 추출
get_metadata() {
  local file="$1"
  local full_path="$PROJECT_ROOT/$file"

  if [ ! -f "$full_path" ]; then
    echo ""
    return
  fi

  first_line=$(head -1 "$full_path")
  if [ "$first_line" != "---" ]; then
    echo ""
    return
  fi

  desc=$(awk '/^---$/{if(++c==2)exit} c==1 && /^description:/{sub(/^description:[[:space:]]*/, ""); print}' "$full_path")
  # 쉼표를 세미콜론으로 치환 (CSV 형식 유지)
  desc=$(echo "$desc" | tr ',' ';')
  # 100자 제한
  if [ ${#desc} -gt 100 ]; then
    desc="${desc:0:100}..."
  fi
  echo "$desc"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --path=*)
      TARGET_PATH="${1#*=}"
      shift
      ;;
    --help|-h)
      echo "Usage: $0 [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  --path=<dir>  특정 경로로 시작하는 문서만 조회"
      echo "  --help, -h    도움말 표시"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# 문서 파일 목록 수집
docs=$(find "$PROJECT_ROOT" \
  -type f -name "*.md" \
  -not -path "*/node_modules/*" \
  -not -path "*/.next/*" \
  -not -path "*/.git/*" \
  -not -path "*/dist/*" \
  -not -path "*/build/*" \
  -not -path "*/coverage/*" \
  -not -path "*/.context/*" \
  -not -path "*/.github/*" \
  2>/dev/null \
  | sed "s|$PROJECT_ROOT/||" \
  | sort)

# 경로 필터링 (path로 시작하는 파일 포함)
if [ -n "$TARGET_PATH" ]; then
  docs=$(echo "$docs" | grep "^${TARGET_PATH}" || true)
fi

# 컨텍스트에 이미 로드되는 파일들 제외
docs=$(echo "$docs" | grep -v "CLAUDE.md$" | grep -v "GEMINI.md$" | grep -v "AGENTS.md$" | grep -v "AGENTS-GOVERNANCE.md$" | grep -v "/\.claude/" || true)

# 통계 계산
if [ -z "$docs" ]; then
  total=0
else
  total=$(echo "$docs" | wc -l | tr -d ' ')
fi

if [ "$total" -eq 0 ]; then
  echo "docs[0]{path,desc}:"
  exit 0
fi

# TOON 포맷 출력
echo "docs[${total}]{path,desc}:"

while IFS= read -r file; do
  desc=$(get_metadata "$file")
  if [ -n "$desc" ]; then
    echo "${file},${desc}"
  else
    echo "${file},"
  fi
done <<< "$docs"
