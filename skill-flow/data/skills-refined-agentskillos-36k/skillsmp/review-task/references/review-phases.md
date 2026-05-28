# Review Phases

> review-task Skill의 6단계 리뷰 프로세스

## Phase 1: 메타데이터 검증

### 1.1 Draft 상태 확인

```bash
# 이슈 정보 조회
gh issue view {issue_number} --repo {owner}/{repo} --json title,labels,state

# Draft 체크 (제목 접두사)
# ❌ [Draft] 메타태그 기능구현
# ✅ 메타태그 기능구현

# Draft 체크 (라벨)
# ❌ labels: ["draft", "feature"]
# ✅ labels: ["feature"]
```

**검증 로직**:

```javascript
const isDraft =
  title.startsWith('[Draft]') ||
  title.startsWith('[DRAFT]') ||
  labels.includes('draft');
```

**결과**:

| 상태 | 메시지 |
|------|--------|
| ✅ Pass | `Draft 전환 완료 - 일반 이슈로 전환됨` |
| 🔴 Fail | `Draft 상태 - [Draft] 접두사 또는 draft 라벨 존재` |

### 1.2 브랜치명 규칙 검증

**규칙**: `{이슈번호}-{영문-기능명}`

```bash
# 현재 브랜치명 확인
BRANCH=$(git branch --show-current)

# 이슈 번호 추출
ISSUE_NUM=$(echo $BRANCH | grep -oE '^[0-9]+')

# 규칙 검증
# ✅ 565-metatag-implements
# ✅ 123-user-authentication
# ❌ feature/metatag (이슈 번호 없음)
# ❌ metatag-565 (번호가 뒤에 위치)
```

**검증 로직**:

```javascript
const branchPattern = /^(\d+)-[a-z0-9-]+$/;
const isValidBranch = branchPattern.test(branchName);
const branchIssueNum = branchName.match(/^(\d+)/)?.[1];
const matchesIssue = branchIssueNum === targetIssueNum;
```

**결과**:

| 상태 | 메시지 |
|------|--------|
| ✅ Pass | `브랜치명 규칙 준수: {branch} ↔ #{issue}` |
| 🟡 Warn | `브랜치명 불일치: {branch} (예상: {issue}-xxx)` |

---

## Phase 2: 테스트 구조 검증

### 2.1 테스트 섹션 분리 확인

이슈 본문에서 테스트 섹션 구조 확인:

```markdown
## 테스트

### 개발자 테스트 (자동화)
- [ ] 유닛 테스트: 메타태그 생성 함수
- [ ] 통합 테스트: OG 이미지 렌더링

### QA 테스트 (수동)
- [ ] 각 페이지별 메타태그 확인
- [ ] SNS 공유 시 미리보기 확인
```

**검증 로직**:

```javascript
const hasDevTest = /개발자\s*테스트|자동화\s*테스트|Unit\s*Test/i.test(body);
const hasQATest = /QA\s*테스트|수동\s*테스트|Manual\s*Test/i.test(body);
const isSeparated = hasDevTest && hasQATest;
```

**결과**:

| 상태 | 메시지 |
|------|--------|
| ✅ Pass | `테스트 섹션 분리됨 - 개발자/QA 구분 명확` |
| 🟡 Warn | `테스트 섹션 미분리 - 개발자 테스트와 QA 테스트 구분 권장` |
| 🔴 Fail | `테스트 섹션 없음 - 테스트 계획 필요` |

### 2.2 테스트 코드 존재 확인

```bash
# 관련 테스트 파일 검색
find . -name "*.test.ts" -o -name "*.spec.ts" | xargs grep -l "{feature}"

# 테스트 실행
npm test -- --coverage --testPathPattern="{feature}"
```

---

## Phase 3: 아키텍처 검증

### 3.1 DDD 레이어 준수

**기대 구조**:

```
app/{domain}/
├── _repositories/     # 서버 데이터 접근
├── _api-clients/      # 브라우저 HTTP 클라이언트
├── _hooks/            # React Query + 상태
├── _components/       # 도메인 UI
└── page.tsx           # 라우트
```

**검증 명령**:

```bash
# 레이어 구조 확인
ls -la app/{domain}/

# 레이어 위반 검색
grep -r "'use client'" app/*/_repositories/  # ❌ Repository에 use client
grep -r "createServerSupabaseClient" app/*/_components/  # ❌ Component에서 서버 클라이언트
```

### 3.2 팀 컨벤션 준수

**Constitution 원칙 체크**:

```bash
# 1. Server-First (서버 컴포넌트 우선)
grep -c "'use client'" app/{domain}/**/*.tsx

# 2. Type Safety (타입 안전성)
grep -rn ": any" app/{domain}/ --include="*.ts" --include="*.tsx"

# 3. Debug 코드
grep -rn "console\.log\|debugger" app/{domain}/ --include="*.ts" --include="*.tsx"
```

**결과**:

| 상태 | 메시지 |
|------|--------|
| ✅ Pass | `DDD 아키텍처 준수 - 4레이어 구조 확인` |
| 🔴 Fail | `레이어 위반 - {위반 내용}` |

---

## Phase 4: 기능 구현 확인

### 4.1 Acceptance Criteria 추출

이슈 본문에서 AC 항목 추출:

```markdown
## Acceptance Criteria

- [ ] 페이지별 동적 메타태그 생성
- [ ] OG:image 자동 생성
- [ ] Twitter Card 지원
- [ ] 메타태그 미리보기 기능
```

**추출 패턴**:

```javascript
const acPatterns = [
  /##\s*Acceptance\s*Criteria[\s\S]*?(?=##|$)/i,
  /##\s*AC[\s\S]*?(?=##|$)/i,
  /##\s*요구사항[\s\S]*?(?=##|$)/i,
  /##\s*기능\s*요구[\s\S]*?(?=##|$)/i,
];
```

### 4.2 코드 매칭

각 AC 항목에 대해 관련 코드 검색:

```bash
# 키워드 기반 검색
grep -rn "{keyword}" app/ lib/ --include="*.ts" --include="*.tsx"

# 파일 패턴 검색
find . -name "*{feature}*" -type f
```

**결과 매핑**:

| AC 항목 | 상태 | 관련 코드 |
|---------|------|----------|
| 동적 메타태그 | ✅ | `app/layout.tsx:45` |
| OG:image | ✅ | `lib/og-image.ts:12` |
| Twitter Card | ❌ | - |

---

## Phase 5: 품질 게이트

### 5.1 자동화 검증

```bash
# ESLint
npm run lint

# TypeScript
npx tsc --noEmit

# Tests
npm test

# Coverage
npm test -- --coverage
```

### 5.2 결과 집계

| 체크 | 기준 | 상태 |
|------|------|------|
| ESLint | 0 errors | ✅/🔴 |
| TypeScript | 0 errors | ✅/🔴 |
| Tests | 100% passing | ✅/🔴 |
| Coverage | 80%/80%/70% | ✅/🟡 |

### 5.3 최종 판정

```javascript
const canPR =
  !isDraft &&
  acCompletionRate === 1.0 &&
  lintPassed &&
  tscPassed &&
  testsPassed;

const verdict = canPR
  ? '✅ PR 가능'
  : '🔴 PR 차단 - 수정 필요';
```

---

## Phase 6: PR 리뷰 코멘트 작성

> Phase 1-5 완료 후, 대상 PR에 리뷰 코멘트를 자동 작성

### 6.1 PR 탐색

```bash
# 현재 브랜치의 PR 조회
gh pr list --head $(git branch --show-current) --json number,url,state,title,isDraft

# 결과 예시
# [{"number": 42, "url": "https://github.com/...", "state": "OPEN", "title": "메타태그 구현", "isDraft": false}]
```

**PR 상태 확인**:

| 상태 | 처리 |
|------|------|
| PR 없음 | `⚠️ PR이 없습니다. PR 생성 후 다시 시도하세요.` |
| Draft PR | `⚠️ Draft PR입니다. Ready for Review 전환 후 다시 시도하세요.` |
| Open PR | ✅ 리뷰 코멘트 작성 진행 |
| Merged/Closed | `⚠️ PR이 이미 머지/종료되었습니다.` |

### 6.2 리뷰 타입 결정

Phase 1-5 결과에 따라 리뷰 타입 자동 결정:

```javascript
const getCriticalCount = (results) =>
  results.filter(r => r.severity === 'critical').length;

const getWarningCount = (results) =>
  results.filter(r => r.severity === 'warning').length;

const determineReviewType = (criticalCount, warningCount) => {
  if (criticalCount > 0) return 'REQUEST_CHANGES';
  if (warningCount > 0) return 'COMMENT';
  return 'APPROVE';
};
```

**리뷰 타입 매핑**:

| Critical | Warning | 리뷰 타입 | gh 옵션 |
|----------|---------|----------|---------|
| 0 | 0 | APPROVE | `--approve` |
| 0 | 1+ | COMMENT | `--comment` |
| 1+ | any | REQUEST_CHANGES | `--request-changes` |

### 6.3 리뷰 코멘트 생성

**코멘트 템플릿**:

```markdown
## 🔍 SEMO Review: #{issue_number}

### 리뷰 결과

| Phase | 상태 | 요약 |
|-------|------|------|
| 메타데이터 | {status} | {summary} |
| 테스트 구조 | {status} | {summary} |
| 아키텍처 | {status} | {summary} |
| 기능 구현 | {status} | {summary} |
| 품질 게이트 | {status} | {summary} |

### {Critical/Warning 상세 (있는 경우)}

{상세 내용}

---

🤖 *SEMO review-task Skill에 의해 자동 생성됨*
```

### 6.4 리뷰 제출

```bash
# APPROVE
gh pr review {pr_number} --approve --body "$(cat <<'EOF'
## 🔍 SEMO Review: #{issue_number}

### ✅ 리뷰 통과

모든 검증 항목을 통과했습니다.

| Phase | 상태 |
|-------|------|
| 메타데이터 | ✅ |
| 테스트 구조 | ✅ |
| 아키텍처 | ✅ |
| 기능 구현 | ✅ |
| 품질 게이트 | ✅ |

---
🤖 *SEMO review-task Skill*
EOF
)"

# COMMENT (경고 있음)
gh pr review {pr_number} --comment --body "$(cat <<'EOF'
## 🔍 SEMO Review: #{issue_number}

### 🟡 경고 사항

PR 진행 가능하나, 다음 사항 검토 권장:

{warning_details}

---
🤖 *SEMO review-task Skill*
EOF
)"

# REQUEST_CHANGES (Critical 있음)
gh pr review {pr_number} --request-changes --body "$(cat <<'EOF'
## 🔍 SEMO Review: #{issue_number}

### 🔴 수정 필요

다음 항목 수정 후 재요청 바랍니다:

{critical_details}

---
🤖 *SEMO review-task Skill*
EOF
)"
```

### 6.5 사용자 확인 (선택적)

리뷰 코멘트 작성 전 사용자 확인 옵션:

**자동 모드** (기본):

```bash
# 명시적 요청 시 자동 작성
"리뷰하고 PR에 코멘트 남겨줘"
```

**확인 모드**:

```bash
# 리뷰 완료 후 질문
"PR에 리뷰 코멘트 작성할까요? (Y/n)"
```

### 6.6 결과 보고

```markdown
## PR 리뷰 코멘트 작성 완료

**PR**: #{pr_number} - {pr_title}
**리뷰 타입**: {APPROVE|COMMENT|REQUEST_CHANGES}
**URL**: {pr_url}

리뷰 코멘트가 성공적으로 작성되었습니다.
```
