# Event Storming 결과

## 세션 정보

| 항목 | 내용 |
|------|------|
| **프로젝트** | {{PROJECT_NAME}} |
| **일시** | {{DATE}} |
| **참석자** | {{PARTICIPANTS}} |
| **범위** | {{SCOPE}} |

## Domain Events

### {{CONTEXT_1}}

| 순서 | 이벤트 | 설명 | Aggregate |
|------|--------|------|-----------|
| 1 | {{EVENT_1}} | {{DESC_1}} | {{AGG_1}} |
| 2 | {{EVENT_2}} | {{DESC_2}} | {{AGG_2}} |
| 3 | {{EVENT_3}} | {{DESC_3}} | {{AGG_3}} |

### {{CONTEXT_2}}

| 순서 | 이벤트 | 설명 | Aggregate |
|------|--------|------|-----------|
| 1 | {{EVENT_4}} | {{DESC_4}} | {{AGG_4}} |
| 2 | {{EVENT_5}} | {{DESC_5}} | {{AGG_5}} |

## Command-Event 흐름

```mermaid
flowchart LR
    subgraph {{FLOW_1}}
        A1[👤 {{ACTOR_1}}] --> C1[🟦 {{COMMAND_1}}]
        C1 --> AG1[🟨 {{AGGREGATE_1}}]
        AG1 --> E1[🟧 {{EVENT_1}}]
    end

    subgraph {{FLOW_2}}
        E1 --> P1[🟪 {{POLICY_1}}]
        P1 --> C2[🟦 {{COMMAND_2}}]
        C2 --> AG2[🟨 {{AGGREGATE_2}}]
        AG2 --> E2[🟧 {{EVENT_2}}]
    end
```

## Commands

| Actor | Command | Aggregate | Event | 설명 |
|-------|---------|-----------|-------|------|
| {{ACTOR_1}} | {{CMD_1}} | {{AGG_1}} | {{EVT_1}} | {{CMD_DESC_1}} |
| {{ACTOR_2}} | {{CMD_2}} | {{AGG_2}} | {{EVT_2}} | {{CMD_DESC_2}} |
| 시스템 | {{CMD_3}} | {{AGG_3}} | {{EVT_3}} | {{CMD_DESC_3}} |

## Policies (자동화 규칙)

| Policy명 | Trigger Event | Command | Target | 설명 |
|---------|---------------|---------|--------|------|
| {{POLICY_1}} | {{TRIGGER_1}} | {{CMD_1}} | {{TARGET_1}} | {{POL_DESC_1}} |
| {{POLICY_2}} | {{TRIGGER_2}} | {{CMD_2}} | {{TARGET_2}} | {{POL_DESC_2}} |

## Aggregates

| Aggregate | Context | Root Entity | 설명 |
|-----------|---------|-------------|------|
| {{AGG_1}} | {{CTX_1}} | {{ROOT_1}} | {{AGG_DESC_1}} |
| {{AGG_2}} | {{CTX_2}} | {{ROOT_2}} | {{AGG_DESC_2}} |

## Read Models

| Read Model | 사용처 | 데이터 소스 | 설명 |
|-----------|--------|-----------|------|
| {{RM_1}} | {{SCREEN_1}} | {{SOURCE_1}} | {{RM_DESC_1}} |
| {{RM_2}} | {{SCREEN_2}} | {{SOURCE_2}} | {{RM_DESC_2}} |

## External Systems

| 시스템 | 연동 방식 | 관련 Event/Command | 설명 |
|--------|----------|-------------------|------|
| {{EXT_1}} | {{INT_1}} | {{REL_1}} | {{EXT_DESC_1}} |

## Hot Spots (논쟁점)

| 번호 | 주제 | 상태 | 해결 방안 |
|------|------|------|----------|
| 🟥 1 | {{HOTSPOT_1}} | 미해결/해결됨 | {{SOLUTION_1}} |
| 🟥 2 | {{HOTSPOT_2}} | 미해결/해결됨 | {{SOLUTION_2}} |

## Bounded Context 도출

```mermaid
graph TB
    subgraph {{BC_1}}[{{BC_NAME_1}}]
        A1[{{AGG_1}}]
        A2[{{AGG_2}}]
    end

    subgraph {{BC_2}}[{{BC_NAME_2}}]
        A3[{{AGG_3}}]
        A4[{{AGG_4}}]
    end

    A1 -.->|Event| A3
    A2 -.->|Event| A4
```

## 다음 단계

1. [ ] Bounded Context 상세 정의
2. [ ] Aggregate 설계서 작성
3. [ ] Context Map 작성
4. [ ] Ubiquitous Language 용어집 정리

## 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| 1.0.0 | {{DATE}} | Event Storming 결과 정리 |
