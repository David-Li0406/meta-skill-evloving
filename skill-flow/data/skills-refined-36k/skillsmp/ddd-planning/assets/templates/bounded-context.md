# Bounded Context 정의서

## Context 정보

| 항목 | 내용 |
|------|------|
| **Context명** | {{CONTEXT_NAME}} |
| **영문명** | {{CONTEXT_NAME_EN}} |
| **도메인 분류** | Core / Supporting / Generic |
| **담당 팀** | {{TEAM_NAME}} |
| **작성일** | {{DATE}} |

## 개요

{{CONTEXT_DESCRIPTION}}

## 핵심 책임

1. {{RESPONSIBILITY_1}}
2. {{RESPONSIBILITY_2}}
3. {{RESPONSIBILITY_3}}

## Ubiquitous Language

| 한글 | 영문 | 정의 |
|------|------|------|
| {{TERM_KO_1}} | {{TERM_EN_1}} | {{DEFINITION_1}} |
| {{TERM_KO_2}} | {{TERM_EN_2}} | {{DEFINITION_2}} |
| {{TERM_KO_3}} | {{TERM_EN_3}} | {{DEFINITION_3}} |

## Aggregate 목록

| Aggregate | 설명 | Root Entity |
|-----------|------|-------------|
| {{AGGREGATE_1}} | {{DESC_1}} | {{ROOT_1}} |
| {{AGGREGATE_2}} | {{DESC_2}} | {{ROOT_2}} |

## Domain Events

| 이벤트명 | 설명 | Aggregate |
|---------|------|-----------|
| {{EVENT_1}} | {{EVENT_DESC_1}} | {{EVENT_AGG_1}} |
| {{EVENT_2}} | {{EVENT_DESC_2}} | {{EVENT_AGG_2}} |

## 외부 의존성

### Upstream (이 Context가 의존하는)

| Context | 관계 패턴 | 설명 |
|---------|----------|------|
| {{UPSTREAM_1}} | {{PATTERN_1}} | {{RELATION_DESC_1}} |

### Downstream (이 Context에 의존하는)

| Context | 관계 패턴 | 설명 |
|---------|----------|------|
| {{DOWNSTREAM_1}} | {{PATTERN_2}} | {{RELATION_DESC_2}} |

## 기술 스택

- **언어/프레임워크**: {{TECH_STACK}}
- **데이터베이스**: {{DATABASE}}
- **메시징**: {{MESSAGING}}

## API 경계

### 제공 API (Published)

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| {{ENDPOINT_1}} | {{METHOD_1}} | {{API_DESC_1}} |

### 소비 API (Consumed)

| 엔드포인트 | 제공 Context | 설명 |
|-----------|-------------|------|
| {{CONSUMED_1}} | {{PROVIDER_1}} | {{CONSUMED_DESC_1}} |

## 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| 1.0.0 | {{DATE}} | 최초 작성 |
