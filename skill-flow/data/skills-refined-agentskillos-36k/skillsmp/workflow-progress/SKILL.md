---
name: workflow-progress
description: |
  워크플로우 진행 상황 조회. Use when (1) 현재 워크플로우 진행도 확인,
  (2) 워크플로우 히스토리 조회, (3) 진행 중인 워크플로우 목록.
tools: [Bash, Read]
model: inherit
---

> **시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: workflow-progress 호출` 메시지를 첫 줄에 출력하세요.

# workflow-progress Skill

> 워크플로우 인스턴스 진행 상황 조회

## Purpose

실행 중인 워크플로우의 진행 상황, 히스토리, 현재 단계를 조회합니다.

## Workflow

```
진행 상황 조회 요청
    ↓
1. 조회 타입 결정 (목록/상세)
2. DB에서 진행 상황 조회
3. 결과 포맷팅
    ↓
완료
```

## Input

```yaml
# 전체 목록 조회 (기본)
mode: "list"

# 특정 인스턴스 상세 조회
mode: "detail"
instance_id: "uuid"  # 또는 instance_name으로 검색
```

## Output

### 목록 조회

```markdown
[SEMO] Skill: workflow-progress 완료

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
[SEMO] Skill: workflow-progress 완료

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

## SQL Queries

> **Note**: 모든 쿼리는 `semo` 스키마를 사용합니다. `workflow_nodes`는 FK 기반 (`skill_id`, `agent_id`)입니다.

### 목록 조회

```sql
-- View 사용 (권장)
SELECT
  wi.id,
  wi.instance_name,
  wd.name AS workflow_name,
  wd.command_name,
  vwn.node_key,
  vwn.name AS current_step,
  vwn.skill_name,
  vwn.agent_name,
  vwn.phase,
  wi.status,
  wi.created_at
FROM semo.workflow_instances wi
JOIN semo.workflow_definitions wd ON wd.id = wi.workflow_definition_id
LEFT JOIN semo.v_workflow_nodes vwn ON vwn.id = wi.current_node_id
WHERE wi.status IN ('active', 'paused')
ORDER BY wi.created_at DESC
LIMIT 20;
```

### 상세 조회 (히스토리)

```sql
SELECT
  vwn.node_key,
  vwn.name,
  vwn.skill_name,
  vwn.agent_name,
  vwn.phase,
  wne.status,
  wne.decision_result,
  wne.completed_at
FROM semo.workflow_node_executions wne
JOIN semo.v_workflow_nodes vwn ON vwn.id = wne.node_id
WHERE wne.workflow_instance_id = '{instance_id}'
ORDER BY wne.created_at;
```

### 진행률 계산

```sql
SELECT
  (SELECT COUNT(*) FROM semo.workflow_node_executions
   WHERE workflow_instance_id = '{instance_id}'
     AND status = 'completed') AS completed_nodes,
  (SELECT COUNT(*) FROM semo.workflow_nodes
   WHERE workflow_definition_id = '{workflow_id}') AS total_nodes;
```

## View 활용

```sql
-- v_workflow_nodes 뷰: skill/agent 이름 자동 JOIN
SELECT * FROM semo.v_workflow_nodes
WHERE workflow_definition_id = '{workflow_id}';

-- v_skills 뷰: package 정보 포함
SELECT * FROM semo.v_skills WHERE is_active = true;

-- v_agents 뷰: package 정보 포함
SELECT * FROM semo.v_agents WHERE is_active = true;
```

## 완료 메시지

```markdown
[SEMO] Skill: workflow-progress 완료

{progress_table}

💡 워크플로우 재개: `skill:workflow-resume {instance_id}`
```

## DB Schema

### FK 관계

```text
workflow_instances.workflow_definition_id → workflow_definitions.id
workflow_instances.current_node_id → workflow_nodes.id
workflow_node_executions.workflow_instance_id → workflow_instances.id
workflow_node_executions.node_id → workflow_nodes.id
workflow_nodes.skill_id → skills.id
workflow_nodes.agent_id → agents.id
```

### Views

| View | 설명 |
| ---- | ---- |
| `semo.v_workflow_nodes` | skill/agent 이름 자동 JOIN |
| `semo.v_skills` | package 정보 포함 |
| `semo.v_agents` | package 정보 포함 |

## Related Skills

- `workflow-start` - 워크플로우 시작
- `workflow-resume` - 중단된 워크플로우 재개
