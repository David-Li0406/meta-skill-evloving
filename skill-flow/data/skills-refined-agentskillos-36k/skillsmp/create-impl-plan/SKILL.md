---
name: create-impl-plan
description: |
  구현 계획 수립. Use when (1) "계획 세워줘", "설계해줘",
  (2) 복잡한 기능 구현 전, (3) 리팩토링 계획.

  ⚠️ 특화된 계획은 별도 스킬 사용:
  - 테스트 계획 → write-test 스킬
tools: [Read, Glob, Grep, Task]
model: inherit
---

> **🔔 호출 시 메시지**: 이 Skill이 호출되면 반드시 `[SEMO] Skill: create-impl-plan` 시스템 메시지를 첫 줄에 출력하세요.

# create-impl-plan Skill

> 기능 구현 및 리팩토링 계획 수립

## 역할 범위

| 이 스킬에서 처리 | 다른 스킬에서 처리 |
|-----------------|-------------------|
| ✅ 기능 구현 계획 | ❌ Sprint 계획 → `sprint-master` |
| ✅ 리팩토링 계획 | ❌ Roadmap 계획 → `roadmap-planner` |
| ✅ 기술적 설계 | ❌ 테스트 계획 → `tester` |
| ✅ 의존성 분석 | ❌ 배포 계획 → `deployer` |

## Workflow

```text
요청 분석
    ↓
1. 요구사항 파악
    ↓
2. 기존 코드베이스 분석 (Glob, Grep)
    ↓
3. 구현 단계 정의
    ↓
4. 의존성 및 리스크 분석
    ↓
5. 계획서 출력
```

## 계획서 템플릿

### 기능 구현 계획

```markdown
## 구현 계획: {기능명}

### 1. 요구사항 요약
- {요구사항 1}
- {요구사항 2}

### 2. 영향 범위 분석
| 파일/모듈 | 변경 유형 | 설명 |
|----------|----------|------|
| {파일1} | 수정 | {설명} |
| {파일2} | 신규 | {설명} |

### 3. 구현 단계
1. **단계 1**: {설명}
   - Task: {세부 작업}
2. **단계 2**: {설명}
   - Task: {세부 작업}

### 4. 의존성
- {외부 라이브러리/API}
- {내부 모듈 의존성}

### 5. 리스크
| 리스크 | 영향도 | 대응 방안 |
|--------|--------|----------|
| {리스크} | 높음/중간/낮음 | {대응} |

### 6. 예상 결과물
- [ ] {결과물 1}
- [ ] {결과물 2}
```

### 리팩토링 계획

```markdown
## 리팩토링 계획: {대상}

### 1. 현재 문제점
- {문제 1}
- {문제 2}

### 2. 목표 상태
- {목표 1}
- {목표 2}

### 3. 리팩토링 전략
- [ ] **Phase 1**: {안전한 변경}
- [ ] **Phase 2**: {구조 변경}
- [ ] **Phase 3**: {최적화}

### 4. 테스트 전략
- 기존 테스트 보존
- 리팩토링 단계별 검증

### 5. 롤백 계획
- {롤백 시나리오}
```

## 출력 형식

```markdown
[SEMO] Skill: planner → 계획 수립 완료

## {계획 유형}: {대상}

{계획서 내용}

---
다음 단계: skill:implement로 구현 진행
```

## 계획 유형별 라우팅

```text
"계획 세워줘" 요청
    │
    ├─ "Sprint 계획" / "이터레이션"
    │   └→ biz/management: sprint-master
    │
    ├─ "Roadmap" / "분기 계획" / "마일스톤"
    │   └→ biz/management: roadmap-planner
    │
    ├─ "테스트 계획" / "QA 계획"
    │   └→ tester 스킬
    │
    └─ "기능 구현" / "리팩토링" / "설계"
        └→ 이 스킬 (planner)
```

## References

- [implement Skill](../implement/SKILL.md) - 계획 후 구현
- [sprint-master Agent](../../biz/management/agents/sprint-master/) - Sprint 계획
- [roadmap-planner Agent](../../biz/management/agents/roadmap-planner/) - Roadmap 계획
