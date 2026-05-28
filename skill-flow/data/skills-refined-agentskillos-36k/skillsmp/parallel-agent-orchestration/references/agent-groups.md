# Agent Groups Reference

병렬 에이전트 오케스트레이션에서 사용하는 에이전트 그룹 정의입니다.

## 1. Dev Group (개발)

개발 관련 작업을 병렬로 수행합니다.

| Agent | 역할 | Model | 토큰 비용 |
|-------|------|-------|----------|
| architect | 설계 및 구조 분석 | sonnet | 높음 |
| coder | 코드 구현 | sonnet | 높음 |
| tester | 테스트 작성 | sonnet | 중간 |
| docs | 문서화 | haiku | 낮음 |

**사용 시점**:
- 새 기능 구현
- 대규모 리팩토링
- 모듈 재설계

**호출 예시**:
```python
Task(subagent_type="parallel-agent-orchestration",
     prompt="--group dev --task '사용자 인증 모듈 구현'")
```

---

## 2. Test Group (테스트)

다양한 수준의 테스트를 병렬로 실행합니다.

| Agent | 역할 | Model | 토큰 비용 |
|-------|------|-------|----------|
| unit | 단위 테스트 실행 | haiku | 낮음 |
| integration | 통합 테스트 실행 | sonnet | 중간 |
| e2e | E2E 테스트 실행 | sonnet | 높음 |
| security | 보안 테스트 실행 | sonnet | 중간 |

**사용 시점**:
- Phase 2 테스트 실행
- FINAL_CHECK 검증
- 배포 전 회귀 테스트

**호출 예시**:
```python
Task(subagent_type="parallel-agent-orchestration",
     prompt="--group test --task '전체 테스트 실행'")
```

---

## 3. Review Group (리뷰)

코드 품질 및 보안 리뷰를 병렬로 수행합니다.

| Agent | 역할 | Model | 토큰 비용 |
|-------|------|-------|----------|
| code-reviewer | 코드 리뷰 | sonnet | 중간 |
| security-auditor | 보안 리뷰 | sonnet | 중간 |
| architect-reviewer | 아키텍처 리뷰 | opus | 높음 |

**사용 시점**:
- Phase 2.5 코드 리뷰
- PR 생성 전 검증
- 중요 변경사항 리뷰

**호출 예시**:
```python
Task(subagent_type="parallel-agent-orchestration",
     prompt="--group review --task 'PR #123 리뷰'")
```

---

## 에이전트 선택 가이드

### 작업 유형별 권장 그룹

| 작업 유형 | 권장 그룹 | 권장 에이전트 |
|----------|----------|-------------|
| 새 기능 | dev | 전체 |
| 버그 수정 | dev | coder + tester |
| 테스트 추가 | test | unit + integration |
| PR 생성 전 | review | 전체 |
| 배포 전 | test + review | e2e + security + security-auditor |
| 문서화 | dev | docs |
| 성능 최적화 | dev + test | architect + coder + integration |

### Model Tiering 전략

| 복잡도 | 권장 Model | 예시 작업 |
|--------|-----------|----------|
| 높음 | opus | 아키텍처 설계, 복잡한 리뷰 |
| 중간 | sonnet | 일반 구현, 테스트, 분석 |
| 낮음 | haiku | 간단한 검증, 문서화 |

---

## 커스텀 그룹 정의

`run_parallel.py`에서 커스텀 에이전트 조합 가능:

```bash
# 개별 에이전트 지정
python run_parallel.py \
  --agents "architect,coder,security-auditor" \
  --task "보안 중심 기능 구현"

# 타임아웃 설정 (초)
python run_parallel.py \
  --group dev \
  --timeout 600 \
  --task "대규모 리팩토링"
```

---

## 에이전트 의존성

```
dev group:
  architect → coder → tester → docs
              (순차적 의존 가능)

test group:
  unit ─┬─→ integration ─→ e2e
        └─→ security
            (부분 병렬)

review group:
  code-reviewer ─┐
  security-auditor ─┼─→ 최종 판단
  architect-reviewer ─┘
            (완전 병렬)
```

---

## 참조

- CLAUDE.md 섹션 7: Agents
- docs/AGENTS_REFERENCE.md
- src/agents/parallel_workflow.py
