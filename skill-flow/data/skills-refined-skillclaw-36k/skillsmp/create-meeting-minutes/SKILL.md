---
name: create-meeting-minutes
description: |
  정기 회의록 GitHub Discussion에 자동 생성.
  Use when (1) "정기 회의록 생성해줘", (2) /create-meeting-minutes 커맨드,
  (3) "이번 주 회의록 만들어줘", (4) 이터레이션 기반 회의록 생성 요청.
tools: [Bash, Read]
model: inherit
---

> **시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: create-meeting-minutes 호출` 시스템 메시지를 첫 줄에 출력하세요.

# create-meeting-minutes Skill

> 정기 회의록 GitHub Discussion에 자동 생성 (이터레이션 기반 제목)

## 🔴 데이터 소스 변경 (v3.0.0)

| 버전 | 데이터 소스 | 방식 |
|------|------------|------|
| v1.x | GitHub Discussions | GraphQL API |
| v2.x | Supabase | `discussions` 테이블 INSERT |
| **v3.0** | **GitHub Discussions** | `gh api graphql` (command-center) |

---

## Purpose

매주 정기 회의록을 **GitHub Discussion (command-center repository)**에 생성합니다. 제목은 `[{month}월 {분자}/{분모}] 정기 회고 & 회의` 형식으로 자동 생성됩니다.

## NON-NEGOTIABLE RULES

### 대상 Repository

| 항목 | 값 |
|------|-----|
| Owner | `semicolon-devteam` |
| Repository | `command-center` |
| Repository ID | `R_kgDOOdzh9w` |
| Category | `Meeting-Minutes` |
| Category ID | `DIC_kwDOOdzh984Cw9Lp` |

**로컬 파일 생성 금지** - 반드시 GitHub Discussion에 저장

### 제목 형식

```text
[{month}월 {분자}/{분모}] 정기 회고 & 회의

예시:
- [1월 1/5] 정기 회고 & 회의  (1월 1주차, 1월은 5주)
- [1월 3/5] 정기 회고 & 회의  (1월 3주차)
- [2월 2/4] 정기 회고 & 회의  (2월 2주차, 2월은 4주)
```

### 이터레이션 계산 규칙

```text
분모: 해당 월의 총 주 수 (4 또는 5)
분자: 현재 날짜가 해당 월의 몇 번째 주인지
```

## Execution Flow

```text
1. 현재 날짜 확인 (또는 입력된 날짜 사용)
   ↓
2. 이터레이션 계산
   - 해당 월의 총 주 수 (분모)
   - 현재 주차 (분자)
   ↓
3. 제목 생성: [{month}월 {분자}/{분모}] 정기 회고 & 회의
   ↓
4. 회의록 템플릿 생성 (meeting-minutes.yml 기반)
   ↓
5. GitHub Discussion 생성 (gh api graphql)
   ↓
6. 생성된 Discussion URL 반환
```

## GitHub Discussion 생성

### gh CLI 사용

```bash
#!/bin/bash
# 이터레이션 계산 후 Discussion 생성

# 변수 설정
REPO_ID="R_kgDOOdzh9w"
CATEGORY_ID="DIC_kwDOOdzh984Cw9Lp"

# 이터레이션 계산 (예: 1월 3/5)
MONTH=1
NUMERATOR=3
DENOMINATOR=5

# 제목 생성
TITLE="[${MONTH}월 ${NUMERATOR}/${DENOMINATOR}] 정기 회고 & 회의"

# 본문 생성 (meeting-minutes.yml 템플릿 기반)
BODY=$(cat << 'EOF'
## 📋 회의록 작성
팀 회의 내용을 기록합니다. 안건, 논의 내용, 결정사항을 명확히 작성해주세요.

### 📅 회의 일시
<!-- 회의 날짜와 시간을 입력하세요 -->


### 🏷️ 회의 유형
정기 회고&회의

### 👥 참석자
@reus-jeon @garden92 @Roki-Noh @kyago @Yeomsoyam

### 📝 회의 안건

#### 이터레이션 리뷰
- [ ] 리더그룹 각자 코멘트로 이터레이션 진행사항 공유
- [ ] 파트타이머: @reus-jeon @Roki-Noh 가 각 파트타이머 업무 진척 공유
- [ ] 리뷰: 팀 전체 진척도 리뷰

#### 서비스 운영 현황 보고
- [ ] 템플릿 기반 운영 현황 보고 - @Roki-Noh 가 댓글에 게시

### 🎙️ Clova Note 링크
<!-- Clova Note 녹음 링크를 입력하세요 -->


### 📎 추가 메모
<!-- 특이사항이나 추가로 기록할 내용 -->

EOF
)

# GitHub Discussion 생성
gh api graphql \
  -f query='mutation($repoId: ID!, $categoryId: ID!, $title: String!, $body: String!) {
    createDiscussion(input: {
      repositoryId: $repoId
      categoryId: $categoryId
      title: $title
      body: $body
    }) {
      discussion {
        number
        url
      }
    }
  }' \
  -f repoId="$REPO_ID" \
  -f categoryId="$CATEGORY_ID" \
  -f title="$TITLE" \
  -f body="$BODY"
```

## 이터레이션 계산 로직

### Bash 스크립트

```bash
#!/bin/bash
# 이터레이션 계산

TARGET_DATE="${1:-$(date +%Y-%m-%d)}"
YEAR=$(date -j -f "%Y-%m-%d" "$TARGET_DATE" +%Y 2>/dev/null || date -d "$TARGET_DATE" +%Y)
MONTH=$(date -j -f "%Y-%m-%d" "$TARGET_DATE" +%-m 2>/dev/null || date -d "$TARGET_DATE" +%-m)
DAY=$(date -j -f "%Y-%m-%d" "$TARGET_DATE" +%-d 2>/dev/null || date -d "$TARGET_DATE" +%-d)

# 해당 월의 1일 요일 (1=월, 7=일)
FIRST_DAY=$(date -j -f "%Y-%m-%d" "${YEAR}-$(printf %02d $MONTH)-01" +%u 2>/dev/null)

# 해당 월의 마지막 날짜
LAST_DAY=$(date -j -v+1m -v1d -v-1d -f "%Y-%m-%d" "${YEAR}-$(printf %02d $MONTH)-01" +%d 2>/dev/null)

# 총 주 수 계산
TOTAL_WEEKS=$(( (LAST_DAY + FIRST_DAY - 1) / 7 ))
if [ $(( (LAST_DAY + FIRST_DAY - 1) % 7 )) -gt 0 ]; then
  TOTAL_WEEKS=$((TOTAL_WEEKS + 1))
fi

# 현재 주차 계산
CURRENT_WEEK=$(( (DAY + FIRST_DAY - 1) / 7 ))
if [ $(( (DAY + FIRST_DAY - 1) % 7 )) -gt 0 ]; then
  CURRENT_WEEK=$((CURRENT_WEEK + 1))
fi

echo "MONTH=$MONTH"
echo "CURRENT_WEEK=$CURRENT_WEEK"
echo "TOTAL_WEEKS=$TOTAL_WEEKS"
echo "TITLE=[${MONTH}월 ${CURRENT_WEEK}/${TOTAL_WEEKS}] 정기 회고 & 회의"
```

## 사용 예시

### 기본 사용 (현재 날짜 기준)

```bash
/create-meeting-minutes

# 출력:
[SEMO] Skill: create-meeting-minutes 호출

이터레이션 계산 중...
- 현재 날짜: 2026-01-17
- 해당 월 총 주 수: 5
- 현재 주차: 3

제목: [1월 3/5] 정기 회고 & 회의

✅ Discussion 생성 완료
URL: https://github.com/semicolon-devteam/command-center/discussions/123
```

### 특정 날짜 지정

```bash
/create-meeting-minutes 2026-02-15

# 출력:
[SEMO] Skill: create-meeting-minutes 호출

이터레이션 계산 중...
- 지정 날짜: 2026-02-15
- 해당 월 총 주 수: 4
- 현재 주차: 3

제목: [2월 3/4] 정기 회고 & 회의

✅ Discussion 생성 완료
URL: https://github.com/semicolon-devteam/command-center/discussions/124
```

## Output

```markdown
[SEMO] Skill: create-meeting-minutes 완료

✅ 정기 회의록 생성 완료

**제목**: [{month}월 {분자}/{분모}] 정기 회고 & 회의
**URL**: https://github.com/semicolon-devteam/command-center/discussions/{number}

회의록을 열어서 안건과 내용을 채워주세요.
```

## 에러 처리

| 에러 | 원인 | 해결 |
|------|------|------|
| gh 인증 오류 | GitHub CLI 미로그인 | `gh auth login` 실행 |
| Repository not found | 권한 없음 | 레포지토리 접근 권한 확인 |
| Category not found | 카테고리 ID 오류 | 카테고리 ID 확인 |
| 잘못된 날짜 | 날짜 형식 오류 | `YYYY-MM-DD` 형식 사용 |

## References

- [command-center Discussion Template](.github/DISCUSSION_TEMPLATE/meeting-minutes.yml)
- [GitHub GraphQL API - createDiscussion](https://docs.github.com/en/graphql/reference/mutations#creatediscussion)

## Related

- `summarize-meeting` - 녹취록 기반 회의록 생성
- `create-decision-log` - 의사결정 로그 생성
- `notify-slack` - Slack 알림 전송
