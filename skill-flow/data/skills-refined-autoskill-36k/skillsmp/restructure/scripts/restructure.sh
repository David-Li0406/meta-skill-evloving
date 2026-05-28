#!/bin/bash

# =============================================================================
# restructure.sh - gemini-cli를 사용한 마크다운 파일 재구조화 스크립트
# =============================================================================
# 사용법: ./restructure.sh <파일경로>
# 예시: ./restructure.sh "🚨Temporary/📖Books/📕혐오/HATE/4. Introduction.md"
# 출력: 같은 디렉토리에 "Restructured_" 접두사가 붙은 파일 생성
# =============================================================================

set -e

# 스크립트 위치 기준 경로 설정
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPT_FILE="$SCRIPT_DIR/prompt.md"

# =============================================================================
# 함수 정의
# =============================================================================

print_usage() {
    echo "사용법: $0 <파일경로>"
    echo ""
    echo "예시:"
    echo "  $0 \"🚨Temporary/📖Books/📕혐오/HATE/4. Introduction.md\""
    echo ""
    echo "출력:"
    echo "  같은 디렉토리에 \"Restructured_\" 접두사가 붙은 파일 생성"
}

print_error() {
    echo "[ERROR] $1" >&2
}

print_info() {
    echo "[INFO] $1"
}

# =============================================================================
# 인자 검증
# =============================================================================

if [ $# -eq 0 ]; then
    print_error "파일 경로가 제공되지 않았습니다."
    echo ""
    print_usage
    exit 1
fi

INPUT_FILE="$1"

# 파일 존재 확인 (ls 사용 - macOS 유니코드 정규화 문제 우회)
if ! ls "$INPUT_FILE" >/dev/null 2>&1; then
    print_error "파일을 찾을 수 없습니다: $INPUT_FILE"
    exit 1
fi

# 프롬프트 파일 존재 확인
if ! ls "$PROMPT_FILE" >/dev/null 2>&1; then
    print_error "프롬프트 파일을 찾을 수 없습니다: $PROMPT_FILE"
    exit 1
fi

# =============================================================================
# 경로 처리
# =============================================================================

# 디렉토리와 파일명 분리
DIR_PATH="$(dirname "$INPUT_FILE")"
FILE_NAME="$(basename "$INPUT_FILE")"

# 출력 파일 경로 생성
OUTPUT_FILE="$DIR_PATH/Restructured_$FILE_NAME"

# =============================================================================
# 정보 출력
# =============================================================================

print_info "입력 파일: $INPUT_FILE"
print_info "출력 파일: $OUTPUT_FILE"
print_info "프롬프트: $PROMPT_FILE"
print_info "모델: gemini-3-flash-preview"
echo ""

# =============================================================================
# gemini-cli 실행
# =============================================================================

print_info "gemini-cli 실행 중..."

# XML 태그로 시스템 프롬프트와 콘텐츠 구분
COMBINED_PROMPT="<System_Prompt>
$(cat "$PROMPT_FILE")
</System_Prompt>

<Content>
$(cat "$INPUT_FILE")
</Content>"

# gemini-cli headless mode 실행
gemini -m gemini-3-flash-preview -p "$COMBINED_PROMPT" > "$OUTPUT_FILE"

# =============================================================================
# 결과 확인
# =============================================================================

if [ -f "$OUTPUT_FILE" ]; then
    print_info "완료! 출력 파일이 생성되었습니다: $OUTPUT_FILE"
else
    print_error "출력 파일 생성에 실패했습니다."
    exit 1
fi
