---
name: Restructure
description: Restructure unorganized text into readable markdown documents using Gemini AI. Use when processing article scraps, converting messy notes to structured documents, or translating English content to Korean.
allowed-tools: Read, Bash, Glob
version: 1.0.0
updated: 2026-01-11
status: active
color: yellow
---

# Restructure: 텍스트 재구조화 스킬

정리되지 않은 텍스트(기사 스크랩, 메모 등)를 가독성 높은 마크다운 문서로 재구성한다. 원본의 의미와 내용은 일체 변경하지 않으면서 논리적인 구조를 부여한다.

---

## Quick Reference (30 seconds)

**Purpose**: 비정형 텍스트를 체계적인 마크다운 문서로 재구조화

**Execution Command**:
```bash
"{skill_scripts_dir}/restructure.sh" "{input_file_path}"
```

**Script Location**:
`.claude/skills/Restructure/scripts/restructure.sh`

**Prerequisites**:
- gemini-cli 설치 필요
- Model: gemini-3-flash-preview

**Output**: 같은 디렉토리에 `Restructured_` 접두사가 붙은 파일 생성

**Example**:
```bash
# 상대 경로
./restructure.sh "🚨Temporary/📖Books/📕혐오/HATE/4. Introduction.md"

# 절대 경로
./restructure.sh "/Users/seongjin/Documents/⭐성진이의 옵시디언/🚨Temporary/📖Books/📕혐오/HATE/4. Introduction.md"
```

---

## Implementation Guide (5 minutes)

### 기본 사용법

**Step 1**: gemini-cli 설치 확인
```bash
# gemini-cli가 설치되어 있는지 확인
which gemini
```

**Step 2**: 스크립트 실행
```bash
SKILL_DIR="/path/to/vault/.claude/skills/Restructure/scripts"
"$SKILL_DIR/restructure.sh" "/path/to/input.md"
```

### 입출력 구조

| 항목 | 설명 |
|------|------|
| 입력 | 정리되지 않은 마크다운 파일 |
| 출력 | `Restructured_[원본파일명].md` |
| 위치 | 입력 파일과 동일 디렉토리 |

**입출력 예시**:
```
입력: 4. Introduction.md
출력: Restructured_4. Introduction.md
```

### 스크립트 동작 흐름

1. **입력 검증**: 파일 경로와 프롬프트 파일 존재 확인
2. **프롬프트 구성**: 시스템 프롬프트와 입력 콘텐츠를 XML 태그로 결합
3. **AI 처리**: gemini-cli headless mode로 재구조화 실행
4. **출력 저장**: 결과를 `Restructured_` 접두사 파일로 저장

### 실행 출력 예시

```
[INFO] 입력 파일: /path/to/4. Introduction.md
[INFO] 출력 파일: /path/to/Restructured_4. Introduction.md
[INFO] 프롬프트: /path/to/prompt.md
[INFO] 모델: gemini-3-flash-preview

[INFO] gemini-cli 실행 중...
[INFO] 완료! 출력 파일이 생성되었습니다: /path/to/Restructured_4. Introduction.md
```

---

## Advanced Implementation (10+ minutes)

### 핵심 원칙

재구조화 작업은 세 가지 핵심 원칙을 따른다:

**1. 내용 보존의 원칙 (Content Fidelity)**
- 원본 텍스트의 정보, 주장, 뉘앙스, 사실 관계를 100% 유지
- 단어 하나, 문장 하나도 임의로 추가/삭제/수정/왜곡 금지

**2. 가독성 극대화의 원칙 (Readability Maximization)**
- 끊어진 문장을 자연스럽게 연결
- 문단 구분을 논리적으로 재조정
- 적절한 마크다운 서식 적용

**3. 형식 일관성의 원칙 (Formatting Consistency)**
- 모든 문서에 일관된 마크다운 규칙 적용
- 통일성 있고 전문적인 결과물 생성

### 번역 원칙 (영어 입력 시)

입력이 영어인 경우 평어체 한국어(~다, ~이다)로 번역하며 다음 원칙을 따른다:

| 항목 | 규칙 |
|------|------|
| 의도/톤/뉘앙스 | 원문의 의도와 톤을 한국어로 충실히 전달 |
| 자연스러운 표현 | 직역 피하고 한국어 화자가 읽기 편한 문장으로 재구성 |
| 관용적 표현 | 한국어권 독자가 이해할 수 있는 표현으로 옮기기 |
| 전문 용어 | 해당 분야의 한국어 표준 용법에 따라 정확하게 번역 |

### 고유명사 처리 규칙

**외국어 고유명사**: 원어 그대로 표기
```
Steve Jobs -> Steve Jobs (O)
Steve Jobs -> 스티브 잡스 (X)
```

**한국어 고유명사**: 원래 표기 유지
```
손흥민 -> 손흥민 (O)
손흥민 -> Son Heung-min (X)
```

**책/작품 제목**: 『』 형식으로 통일
```
'자유론', "자유론", <자유론> -> 『자유론』
```

### 마크다운 서식 적용 규칙

| 요소 | 처리 방식 |
|------|-----------|
| 소제목 | 내용 구분은 `##`, `###`으로 계층화 |
| 인용문 | 직접 인용, 대화, 강조 문구는 `>` 블록 처리 |
| 이미지+캡션 | 같은 줄에 이어서 작성: `![[img.png]] 캡션` |
| 목록 | 나열 항목은 `1.` 또는 `-` 사용 |
| 강조 | 중요 키워드는 `**굵게**` 처리 |
| 문헌 인용 | 『』 형식으로 통일 |

### 프롬프트 커스터마이징

`scripts/prompt.md` 파일을 수정하여 재구조화 방식을 조정할 수 있다:

```bash
# 프롬프트 파일 위치
.claude/skills/Restructure/scripts/prompt.md
```

**주요 설정 항목**:
- 출력 언어 설정 (현재: 평어체 한국어)
- 번역 원칙 조정
- 고유명사 처리 규칙
- 마크다운 서식 규칙

### 배치 처리

여러 파일을 순차적으로 처리:

```bash
SKILL_DIR="/path/to/vault/.claude/skills/Restructure/scripts"
for file in "/path/to/folder"/*.md; do
  "$SKILL_DIR/restructure.sh" "$file"
done
```

---

## Related Resources

**Dependencies**:
- gemini-cli: Google의 Gemini CLI 도구
- Model: gemini-3-flash-preview

**File Structure**:
```
.claude/skills/Restructure/
├── SKILL.md           # 이 문서
└── scripts/
    ├── restructure.sh # 메인 실행 스크립트
    └── prompt.md      # 시스템 프롬프트 (수정 가능)
```

---

## Works Well With

- `Prepare-Book` - PDF 책을 챕터별 마크다운으로 변환 후 재구조화에 활용
- `Describe-Images` - 이미지 링크 변환 후 텍스트 재구조화
- `Nano-Banana` - 재구조화된 콘텐츠로 PPT 슬라이드 생성

---

## Troubleshooting

**gemini 명령어를 찾을 수 없음**:
- gemini-cli가 설치되어 있는지 확인
- PATH에 gemini가 포함되어 있는지 확인
```bash
which gemini
```

**파일을 찾을 수 없음**:
- 파일 경로에 특수문자나 공백이 있는 경우 따옴표로 감싸기
- 절대 경로 사용 권장
```bash
./restructure.sh "/path/with spaces/file.md"
```

**프롬프트 파일을 찾을 수 없음**:
- `scripts/prompt.md` 파일이 존재하는지 확인
- 스크립트와 같은 디렉토리에 위치해야 함

**출력 파일이 생성되지 않음**:
- gemini-cli API 연결 상태 확인
- 네트워크 연결 확인
- API 할당량 확인

**빈 출력 파일**:
- 입력 파일이 비어있지 않은지 확인
- gemini-cli 로그 확인
- 모델 가용성 확인

**한글 깨짐 현상**:
- 터미널 인코딩이 UTF-8인지 확인
- 입력 파일 인코딩 확인
