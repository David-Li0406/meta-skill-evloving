---
name: agentic-development-workflow
description: Use this skill for optimizing AI agent collaboration and workflow in development tasks, including principles of agentic development, context management, automation, and productivity techniques.
---

# AI 에이전트 개발 및 워크플로우 (Agentic Development and Workflow)

> **"AI는 부조종사, 주인공은 당신입니다"**
> AI 에이전트는 개발자의 생각을 증폭시키고 반복 작업을 대신하지만, 최종 결정권과 책임은 항상 개발자에게 있습니다.

## When to use this skill

- AI 에이전트와 협업 세션 시작 시
- 복잡한 작업 시작 전 접근 방식 결정
- 컨텍스트 관리 전략 수립
- 생산성 향상을 위한 워크플로우 점검
- 팀원에게 AI 협업 사용법 온보딩
- 일상적인 AI 에이전트 작업 최적화

---

## 1. 에이전틱 개발 원칙 (Agentic Development Principles)

### 원칙 1: 분해하고 정복하라 (Divide and Conquer)

AI는 크고 모호한 작업보다 **작고 명확한 지시**에 훨씬 더 좋은 성능을 발휘합니다.

#### 적용 방법

| 잘못된 예 | 올바른 예 |
|----------|----------|
| "로그인 페이지 만들어줘" | 1. "로그인 폼 UI 컴포넌트 생성" |
| | 2. "로그인 API 엔드포인트 작성" |
| | 3. "인증 로직 연결" |
| | 4. "테스트 코드 작성" |

### 원칙 2: 컨텍스트는 우유와 같다 (Context is like Milk)

컨텍스트(AI의 작업 기억)는 항상 **신선하고 압축된 상태**로 유지해야 합니다. 오래된 정보는 AI 성능을 저하시킴.

#### 컨텍스트 관리 전략

- 단일 목적 대화 유지
- HANDOFF.md 기법 사용
- 컨텍스트 상태 모니터링

### 원칙 3: 올바른 추상화 수준 선택

상황에 따라 적절한 추상화 수준을 선택합니다.

| 모드 | 설명 | 사용 시점 |
|------|------|----------|
| **Vibe Coding** | 전체 구조만 보는 높은 수준 | 빠른 프로토타이핑 |
| **Deep Dive** | 코드 한 줄씩 파고드는 낮은 수준 | 버그 수정, 성능 최적화 |

### 원칙 4: 자동화의 자동화 (Automation of Automation)

같은 작업을 3번 이상 반복했다면 → 자동화 방법을 찾아라.

### 원칙 5: 계획 모드 vs 실행 모드

- **계획 모드**: 복잡한 작업에 대한 분석 및 검토
- **실행 모드**: 간단하고 명확한 작업 수행

### 원칙 6: 검증과 회고 (Verify and Reflect)

출력 검증 방법:
1. 테스트 코드 작성
2. 시각적 검토
3. Draft PR 생성
4. 자기 검증 요청

---

## 2. 에이전트별 주요 명령어

### Claude Code 명령어

| 명령어 | 기능 | 사용 시점 |
|--------|------|----------|
| `/init` | CLAUDE.md 초안 자동 생성 | 새 프로젝트 시작 |
| `/clear` | 대화 내용 초기화 | 컨텍스트 오염 시 |
| `/context` | 컨텍스트 윈도우 X-Ray | 성능 저하 시 |

### Gemini CLI 명령어

| 명령어 | 기능 |
|--------|------|
| `gemini` | 대화 시작 |

### Codex CLI 명령어

| 명령어 | 기능 |
|--------|------|
| `codex` | 대화 시작 |

---

## 3. Git/GitHub 워크플로우 통합

### 자동 커밋 메시지 생성
```
"변경 사항을 분석하고 적절한 커밋 메시지를 작성한 후 커밋해줘"
```

### Draft PR 자동 생성
```
"현재 브랜치의 변경 사항으로 draft PR을 만들어줘."
```

---

## 4. MCP 서버 활용 (Multi-Agent)

### 주요 MCP 서버

| MCP 서버 | 기능 | 용도 |
|----------|------|------|
| Playwright | 웹 브라우저 제어 | E2E 테스트 |
| Supabase | 데이터베이스 쿼리 | DB 직접 접근 |

### MCP 활용 예시
```bash
# Gemini: 대용량 분석
> ask-gemini "@src/ 전체 코드베이스 구조 분석해줘"
```

---

## 5. Multi-Agent 워크플로우 패턴

### 오케스트레이션 패턴
```
[Claude] 계획 수립 → [Gemini] 분석/리서치 → [Codex] 실행/테스트
```

---

## Quick Reference

### 6대 원칙 요약
```
1. 분해정복    → 작고 명확한 단계로 분할
2. 컨텍스트   → 신선하게, 단일 목적 대화
3. 추상화     → Vibe ↔ Deep Dive 상황별
4. 자동화     → 3회 반복 시 자동화
5. 계획/실행  → 계획 70-90%, 실행 10-30%
6. 검증/회고  → 테스트, PR, 자기 검증
```

### 핵심 질문
```
- 이 작업을 더 작게 나눌 수 있는가?
- 컨텍스트가 오염되지 않았는가?
- 올바른 추상화 수준인가?
- 3번 이상 반복했는가?
- 계획을 먼저 세웠는가?
- 결과를 검증했는가?
```

---

## References

- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [ykdojo claude-code-tips](https://github.com/ykdojo/claude-code-tips)
- [Ado's Advent of Claude](https://adocomplete.com/advent-of-claude-2025/)