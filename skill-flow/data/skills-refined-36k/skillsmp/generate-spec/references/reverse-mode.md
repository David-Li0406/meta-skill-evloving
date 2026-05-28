# Reverse Mode Details

> Task Issue → specs/ 파일 변환 상세 가이드

## 개요

Reverse Mode는 Task Issue를 Source of Truth로 사용하여 specs/ 파일을 역생성하는 모드입니다.

```text
Task Issue (Source of Truth)
         ↓
    generate-spec
         ↓
    specs/ 파일 생성
         ↓
    Task Issue 업데이트
```

## Task → spec.md 매핑

| Task 섹션 | spec.md 섹션 | 변환 로직 |
|----------|-------------|----------|
| Problem Context | Background | 직접 복사 |
| Problem Context | Problem Statement | 상세 확장 |
| Goals | Goals | 목록 형식 유지 |
| Constraints (Non-goals) | Non-goals | 추출 |
| User Scenario | User Stories | 테이블 → 스토리 변환 |
| Constraints | Technical Constraints | 병합 |
| 개발자 체크리스트 | Technical Constraints | 병합 |
| Acceptance Criteria | Acceptance Criteria | 직접 복사 |
| 엔지니어 테스트 | Unit Tests | 직접 복사 |
| QA 테스트 | E2E Tests | 직접 복사 |

## User Scenario 변환 예시

**Task의 User Scenario**:
```markdown
| Step | 사용자 액션 | 이 Task의 역할 |
|------|------------|---------------|
| 1 | 댓글 작성 버튼 클릭 | 입력 폼 표시 |
| 2 | 댓글 내용 입력 | 실시간 미리보기 |
| 3 | 제출 버튼 클릭 | API 호출 및 저장 |
```

**spec.md의 User Stories**:
```markdown
## User Stories

### 댓글 작성 플로우

**As a** 사용자
**I want to** 댓글을 작성할 수 있기를
**So that** 게시물에 의견을 남길 수 있다

**Acceptance Criteria**:
1. 댓글 작성 버튼 클릭 시 입력 폼이 표시된다
2. 댓글 내용 입력 시 실시간 미리보기가 표시된다
3. 제출 버튼 클릭 시 API를 호출하여 저장한다
```

## Task Issue 업데이트 로직

### sed 명령 상세

```bash
# 체크박스 업데이트 + 링크 추가
sed -e 's|- \[ \] specify → spec.md|- [x] specify → [spec.md](URL)|'
```

### 정규식 패턴

| 패턴 | 매칭 대상 | 변환 결과 |
|------|----------|----------|
| `- \[ \] specify → spec.md` | 미완료 specify | `- [x] specify → [link]` |
| `- \[ \] plan → plan.md` | 미완료 plan | `- [x] plan → [link]` |

### URL 생성 규칙

```bash
# 기본 패턴
https://github.com/semicolon-devteam/{repo}/blob/dev/specs/{N}-{feature}/{file}.md

# 예시
https://github.com/semicolon-devteam/cm-land/blob/dev/specs/5-comments/spec.md
```

## 오류 처리

| 오류 | 원인 | 해결 |
|------|------|------|
| Task 본문 파싱 실패 | 비표준 형식 | Forward Mode 사용 권장 |
| Issue 업데이트 실패 | 권한 문제 | gh auth 확인 |
| sed 치환 실패 | 체크리스트 형식 불일치 | 수동 업데이트 |

## 제한사항

- Task Issue 본문이 create-tasks 스킬 템플릿을 따라야 함
- 수동으로 생성된 Task는 Forward Mode 권장
- Speckit Progress 섹션이 없으면 업데이트 생략
