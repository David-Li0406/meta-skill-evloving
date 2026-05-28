---
name: doc-sync
description: 기획 승인 또는 PR merge 후 docs/spec 문서를 자동 동기화하는 skill. (1) make-issue에서 '승인' 키워드 감지 시, (2) pr-review-resolver 완료 후 merge 감지 시 자동 실행. 키워드 기반 필터링으로 context 절약.
---

# Document Sync Pipeline

기획 승인 및 PR merge 시 docs/spec 문서를 자동으로 동기화한다.

## 트리거 조건

### 트리거 1: 기획 승인 시 (make-issue에서 호출)
- 사용자가 make-issue 대화 중 '승인' 키워드 입력
- Issue에 `approved` 라벨 추가 후 문서 동기화 시작

### 트리거 2: PR Merge 후 (pr-review-resolver에서 호출)
- PR이 merged 상태로 감지될 때
- 문서 동기화 + Git 정리 작업 수행

---

## 파이프라인 1: 기획 승인 후 문서 동기화

### Step 1: Issue 키워드 추출

```bash
python3 .claude/skills/doc-sync/scripts/extract_issue_keywords.py {issue_number}
```

Output: JSON 형식의 키워드 목록
```json
{
  "domain": ["lecture", "ticket"],
  "infrastructure": [],
  "frontend": ["player"],
  "design": [],
  "new_concepts": ["새로운 개념"]
}
```

### Step 2: 관련 문서 필터링

```bash
python3 .claude/skills/doc-sync/scripts/filter_related_docs.py '{keywords_json}'
```

Output: 관련 문서 목록
```json
[
  {
    "path": "docs/spec/domain/lecture.md",
    "score": 0.85,
    "matched_keywords": ["lecture", "ticket"]
  }
]
```

### Step 3: 변경 필요성 판단

필터링된 문서 목록에서 **헤더 구조만** 추출하여 Master Agent가 판단.

판단 기준:
1. 새로운 개념 추가 필요
2. 기존 개념 변경/확장 필요
3. 예시/플로우 업데이트 필요

### Step 4: 문서 업데이트 (Sub-agent 위임)

변경이 필요한 문서별로 `doc-updater` sub-agent 생성하여 병렬 처리.

```text
Task tool 사용:
- subagent_type: "doc-updater" (또는 general-purpose)
- 각 문서 + 관련 Issue 섹션만 전달
```

### Step 5: 변경사항 커밋

```bash
git add docs/spec/
git commit -m "docs: Issue #{number} 기획 반영하여 spec 문서 업데이트"
```

---

## 파이프라인 2: PR Merge 후 동기화 + Git 정리

### Step 1: PR 상태 확인

```bash
python3 .claude/skills/doc-sync/scripts/check_pr_status.py
```

### Step 2: 코드→문서 연관성 분석

`references/doc-mapping.json`의 매핑 정보를 기반으로 변경된 코드와 관련된 문서 식별.

### Step 3: 문서 최신화 (필요시)

파이프라인 1의 Step 4와 동일한 방식으로 처리.

### Step 4: Git 정리 작업

```bash
bash .claude/skills/doc-sync/scripts/cleanup_after_merge.sh {branch_name}
```

수행 내용:
1. `git fetch origin -p` - 원격 브랜치 삭제 상태 반영
2. `git checkout main` - main 브랜치로 이동
3. `git pull origin main` - main 최신화
4. `git branch -d {branch}` - 작업 완료된 로컬 브랜치 삭제

---

## Context 절약 전략

| 단계 | 방식 | 효과 |
|------|------|------|
| Issue 처리 | Python으로 키워드만 추출 | 90%+ 데이터 감소 |
| 문서 필터링 | 매칭률 0.3 이상만 | 불필요한 문서 제외 |
| 변경 판단 | 헤더 구조만 전달 | 전체 문서 읽기 최소화 |
| 문서 업데이트 | 문서별 sub-agent | 개별 context 분리 |

---

## 주의사항

- 문서 업데이트 시 기존 구조 유지
- Mermaid 다이어그램, 테이블 형식 일관성 유지
- 새 섹션 추가 시 적절한 위치 선정
