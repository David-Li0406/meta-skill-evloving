# Aggregate 설계서

## 기본 정보

| 항목 | 내용 |
|------|------|
| **Aggregate명** | {{AGGREGATE_NAME}} |
| **Bounded Context** | {{CONTEXT_NAME}} |
| **Aggregate Root** | {{ROOT_ENTITY}} |
| **작성일** | {{DATE}} |

## 개요

{{AGGREGATE_DESCRIPTION}}

## 구조

```mermaid
classDiagram
    class {{ROOT_ENTITY}} {
        +{{ROOT_ENTITY}}Id id
        {{PROPERTIES}}
        {{METHODS}}
    }

    class {{VALUE_OBJECT_1}} {
        {{VO_PROPERTIES}}
    }

    {{ROOT_ENTITY}} *-- {{VALUE_OBJECT_1}}
```

## Aggregate Root

### {{ROOT_ENTITY}}

| 속성 | 타입 | 설명 | 필수 |
|------|------|------|------|
| id | {{ROOT_ENTITY}}Id | 고유 식별자 | ✅ |
| {{PROP_1}} | {{TYPE_1}} | {{PROP_DESC_1}} | {{REQUIRED_1}} |
| {{PROP_2}} | {{TYPE_2}} | {{PROP_DESC_2}} | {{REQUIRED_2}} |

### 행위 (Behavior)

| 메서드 | 설명 | Domain Event |
|--------|------|--------------|
| {{METHOD_1}}() | {{METHOD_DESC_1}} | {{EVENT_1}} |
| {{METHOD_2}}() | {{METHOD_DESC_2}} | {{EVENT_2}} |

## Value Objects

### {{VALUE_OBJECT_1}}

| 속성 | 타입 | 설명 |
|------|------|------|
| {{VO_PROP_1}} | {{VO_TYPE_1}} | {{VO_DESC_1}} |

**유효성 규칙**:
- {{VALIDATION_RULE_1}}

## 불변식 (Invariants)

1. **{{INVARIANT_1}}**
   - 설명: {{INVARIANT_DESC_1}}
   - 검증 시점: {{WHEN_1}}

2. **{{INVARIANT_2}}**
   - 설명: {{INVARIANT_DESC_2}}
   - 검증 시점: {{WHEN_2}}

## Domain Events

### {{EVENT_1}}

| 속성 | 타입 | 설명 |
|------|------|------|
| aggregateId | String | Aggregate ID |
| {{EVENT_PROP_1}} | {{EVENT_TYPE_1}} | {{EVENT_PROP_DESC_1}} |
| occurredAt | Instant | 발생 시각 |

**발행 조건**: {{EVENT_CONDITION_1}}

**구독자**:
- {{SUBSCRIBER_1}}: {{SUBSCRIBER_ACTION_1}}

## Repository

```kotlin
interface {{AGGREGATE_NAME}}Repository {
    fun save({{AGGREGATE_VAR}}: {{ROOT_ENTITY}}): {{ROOT_ENTITY}}
    fun findById(id: {{ROOT_ENTITY}}Id): {{ROOT_ENTITY}}?
    {{CUSTOM_QUERIES}}
}
```

## 생명주기

```mermaid
stateDiagram-v2
    [*] --> {{STATE_1}}
    {{STATE_1}} --> {{STATE_2}}: {{TRANSITION_1}}
    {{STATE_2}} --> {{STATE_3}}: {{TRANSITION_2}}
    {{STATE_3}} --> [*]
```

## 예시 코드

```kotlin
// Aggregate 생성
val {{AGGREGATE_VAR}} = {{ROOT_ENTITY}}.create(
    {{CREATE_PARAMS}}
)

// 행위 수행
{{AGGREGATE_VAR}}.{{METHOD_1}}({{METHOD_PARAMS}})

// 저장
repository.save({{AGGREGATE_VAR}})
```

## 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| 1.0.0 | {{DATE}} | 최초 작성 |
