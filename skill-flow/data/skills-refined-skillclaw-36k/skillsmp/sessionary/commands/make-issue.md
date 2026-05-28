---
description: 이슈 생성 또는 기존 이슈에 계획서 보강
argument-hint: <issue-number | 자연어 요구사항>
---

# Issue Maker

입력: $ARGUMENTS

## 분기 판단

- 숫자 입력 → 기존 이슈 조회: `gh issue view $ARGUMENTS --json title,body,labels`
- 그 외 → **빈 이슈 먼저 생성 후** 연구 시작

```bash
# 신규 이슈: 빈 깡통 이슈 먼저 생성
gh issue create --title "{임시 제목}" --body "계획 작성 중..."
# 생성된 이슈 번호를 이후 모든 작업에 사용
```

---

## 반복 사이클: 연구 → 계획 → Issue 반영 → 피드백

최종 승인이 될 때까지 아래 사이클을 반복한다.

### 1단계: 연구

**목표**: 사실에 기반한 자료 수집. 추측이나 가정 금지.

수행 항목:
1. **사용자 요구사항 정리** (가장 중요한 진실)
   - 사용자가 명시한 요구사항을 원문 그대로 기록
   - 요구사항의 핵심 목표와 제약조건 파악
   - 불명확한 부분은 AskUserQuestion으로 즉시 확인

2. **코드베이스 분석**
   - Grep/Glob으로 관련 코드 탐색
   - 현재 구현 상태, 사용 중인 패턴, 의존성 파악
   - 실제 코드를 읽고 동작 방식 확인

3. **도메인 지식 수집**
   - `/spec-loader`로 관련 spec 문서 로드
   - 필요시 WebSearch로 real world example, 업계 표준, 베스트 프랙티스 조사

4. **연구 결과 파일 저장**
   - `.claude/tmp/research-{issue-number}.md`에 저장 (처음부터 이슈 번호 사용)
   - **요구사항 섹션을 최상단에 배치**
   - 발견한 사실만 나열 (출처 명시)
   - 불확실한 부분은 "확인 필요"로 표시
   - 피드백 반영 시 파일 업데이트

### 2단계: 계획

**목표**: 연구 결과를 근거로 해결 방안 수립

수행 항목:
1. **연구 파일 참조**
   - `.claude/tmp/research-{issue-number}.md` 읽어서 근거 확보

2. **방안 선택**
   - 가능한 접근 방식 나열
   - 각 방식의 장단점 비교
   - 선택한 방안과 그 근거 명시

3. **의사결정 정리**
   - 결정된 사항: 근거와 함께 기록
   - 모호한 사항: AskUserQuestion으로 질문

4. **계획서 초안 작성** (하단 템플릿 참조)

### 3단계: Issue 반영

**승인 대기 없이** 계획서를 즉시 GitHub issue에 반영한다.

```bash
gh issue edit {issue-number} --title "{제목}" --body "{계획서}"
# Project 추가 (필요시)
gh project item-add <PROJECT_NUMBER> --owner @me --url <이슈URL>
```

연구 파일도 함께 업데이트: `.claude/tmp/research-{issue-number}.md`

### 4단계: 피드백 대기

사용자에게 계획서 검토 요청.

- **최종 승인** → 5단계 진행
- **피드백** → 연구 파일 업데이트 후 1단계부터 다시 시작. 승인될 때까지 반복.

**승인 키워드 감지**: 사용자 입력에 다음 키워드가 포함되면 승인으로 판단
- "승인", "approve", "LGTM", "좋아", "진행해", "ok", "확정"

### 5단계: 승인 후 처리

1. **Issue에 `approved` 라벨 추가**
   ```bash
   gh issue edit {issue-number} --add-label "approved"
   ```

2. **도메인 문서 동기화 실행**
   ```bash
   # Step 1: Issue 키워드 추출
   keywords=$(python3 .claude/skills/doc-sync/scripts/extract_issue_keywords.py {issue-number})

   # Step 2: 관련 문서 필터링
   related_docs=$(python3 .claude/skills/doc-sync/scripts/filter_related_docs.py "$keywords")
   ```

3. **관련 문서가 있으면** Master Agent가 변경 필요성 판단 후 Sub-agent로 업데이트 위임
   - 각 문서별로 Task tool 사용하여 병렬 처리
   - 변경된 문서가 있으면 커밋:
   ```bash
   git add docs/spec/
   git commit -m "docs: Issue #{issue-number} 기획 반영하여 spec 문서 업데이트

   Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
   ```

4. **연구 파일 정리** (선택적)
   - `.claude/tmp/research-{issue-number}.md`는 이후 참조용으로 유지하거나 삭제

---

## 계획서 템플릿

`.github/ISSUE_TEMPLATE/⚒️-tech-issue.md` 파일을 참조하여 작성한다.

---

## 출력

- 생성/수정된 이슈 번호
- 다음 단계: `/resolve-issue {이슈번호}`
