---
name: workflow-management
description: Use this skill when you need to check the progress of a workflow or resume a paused workflow from its last state.
---

# Skill body

## Purpose

This skill allows you to view the progress of ongoing workflows and to resume any paused workflows from their last execution point.

## Workflow for Progress Check

```
진행 상황 조회 요청
    ↓
1. 조회 타입 결정 (목록/상세)
2. DB에서 진행 상황 조회
3. 결과 포맷팅
    ↓
완료
```

## Input for Progress Check

```yaml
# 전체 목록 조회 (기본)
mode: "list"

# 특정 인스턴스 상세 조회
mode: "detail"
instance_id: "uuid"  # 또는 instance_name으로 검색
```

## Output for Progress Check

### 목록 조회

```markdown
[SEMO] Skill: workflow-management 완료

📋 **진행 중인 워크플로우**

| 프로젝트 | 워크플로우 | 현재 단계 | Phase | 상태 |
|----------|-----------|-----------|-------|------|
| 자동차 딜러 앱 | greenfield | I5: Write Code | implementation | active |
| 커머스 MVP | greenfield | S4: Generate Spec | solutioning | active |
| 레거시 개선 | brownfield | P2: Has UI? | planning | paused |

총 3개 워크플로우 진행 중
```

### 상세 조회

```markdown
[SEMO] Skill: workflow-management 완료

📊 **워크플로우 진행 현황**

**프로젝트**: 자동차 딜러 앱
**워크플로우**: BMad Greenfield Project
**상태**: active
**진행률**: 14/22 노드 (63.6%)

---

### 📈 Phase별 진행

| Phase | 상태 | 노드 |
|-------|------|------|
| Discovery | ✅ 완료 | D0, D1 |
| Planning | ✅ 완료 | P1, P2, P3, P4 |
| Solutioning | ✅ 완료 | S1, S2, S3, S4, S5, S6, S7 |
| Implementation | 🔄 진행중 | I1, I2, I3, I4, **I5** |

---

### 📜 실행 히스토리

| 노드 | 이름 | 상태 | 결과 | 완료 시간 |
|------|------|------|------|-----------|
| D0 | Include Discovery? | ✅ | yes | 10:30 |
| D1 | Ideate | ✅ | - | 10:45 |
| P1 | Create PRD/Epic | ✅ | - | 11:00 |
| ... | ... | ... | ... | ... |
| I5 | Write Code | 🔄 | - | - |
```

## Workflow for Resuming a Workflow

```
워크플로우 재개 요청
    ↓
1. 인스턴스 상태 확인
2. 현재 노드 조회
3. 컨텍스트 복원
4. 노드 실행 재개
    ↓
완료 (노드 실행 계속)
```

## Input for Resuming a Workflow

```yaml
instance_id: "uuid"           # 인스턴스 ID (필수)
# 또는
instance_name: "자동차 딜러 앱" # 인스턴스 이름으로 검색
```

## Output for Resuming a Workflow

```markdown
[SEMO] Skill: workflow-management 완료

🔄 **워크플로우 재개**

| 항목 | 값 |
|------|-----|
| 프로젝트 | 자동차 딜러 앱 |
| 워크플로우 | BMad Greenfield Project |
| 재개 노드 | I5: Write Code |
| Phase | implementation |
| 진행률 | 14/22 (63.6%) |

▶️ 현재 노드를 계속 실행합니다...
```

## Execution Steps for Resuming a Workflow

### Step 1: 인스턴스 조회

```sql
SELECT
  wi.id,
  wi.instance_name,
  wi.status,
  wi.current_node_id,
  wi.context,
  wd.name AS workflow_name
FROM semo.workflow_instances wi
JOIN semo.workflow_definitions wd ON wd.id = wi.workflow_definition_id
WHERE wi.id = '{instance_id}'
   OR wi.instance_name ILIKE '%{instance_name}%';
```

### Step 2: 상태 확인

| 상태 | 처리 |
|------|------|
| active | 현재 노드 계속 실행 |
| paused | 상태를 active로 변경 후 실행 |
| completed | "이미 완료된 워크플로우입니다" |
| failed | 실패 원인 확인 후 재시도 여부 질문 |
| cancelled | "취소된 워크플로우입니다. 새로 시작하시겠습니까?" |

### Step 3: 현재 노드 정보 조회

```sql
-- View 사용 (권장)
SELECT
  vwn.node_key,
  vwn.name,
  vwn.node_type,
  vwn.skill_name,
  vwn.agent_name,
  vwn.decision_config,
  vwn.phase,
  wne.status AS execution_status,
  wne.id AS execution_id
FROM semo.v_workflow_nodes vwn
LEFT JOIN semo.workflow_node_executions wne ON wne.node_id = vwn.id
  AND wne.workflow_instance_id = '{instance_id}'
  AND wne.status IN ('running', 'pending')
WHERE vwn.id = '{current_node_id}';
```