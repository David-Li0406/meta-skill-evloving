---
name: code-patterns
description: Enforces LSP-first exploration, subagent delegation, and mandatory code review patterns. Use before starting any code work.
---

# Code Patterns Enforcer

## Purpose

코드 작업 시 일관된 패턴을 강제합니다:
1. **LSP First**: grep/glob 대신 LSP 도구 사용
2. **Subagent Delegation**: 복잡한 작업은 전문 에이전트에 위임
3. **Mandatory Code Review**: 코드 변경 후 리뷰 필수

## When to Use

- 코드 탐색/분석 작업 시작 전
- 새로운 기능 구현 시작 전
- 리팩토링 또는 버그 수정 전
- "패턴 체크", "규칙 확인" 요청 시

## LSP-First Pattern (MANDATORY)

### Before ANY Code Exploration

**STOP and ask**: Can LSP do this?

| Task | LSP Operation | FORBIDDEN Alternative |
|------|---------------|----------------------|
| 함수/클래스 정의 찾기 | `goToDefinition` | ❌ grep/glob |
| 파일 내 심볼 개요 | `documentSymbol` | ❌ cat/read entire file |
| 프로젝트 심볼 검색 | `workspaceSymbol` | ❌ grep |
| 참조 추적 | `findReferences` | ❌ grep |
| 타입/문서 정보 | `hover` | ❌ read entire file |
| 인터페이스 구현체 | `goToImplementation` | ❌ grep |
| 호출 그래프 분석 | `incomingCalls`/`outgoingCalls` | ❌ manual trace |

### LSP Usage Examples

```bash
# Find where function is defined
LSP goToDefinition file.ts:25:10

# Get all symbols in a file
LSP documentSymbol file.ts:1:1

# Search for symbol across project
LSP workspaceSymbol file.ts:1:1  # with query pattern

# Find all references to a symbol
LSP findReferences file.ts:25:10

# Get type info and documentation
LSP hover file.ts:25:10
```

### When LSP is NOT Available

1. LSP 서버가 해당 파일 타입 미지원 시
2. 텍스트 검색이 명확히 필요한 경우 (로그 메시지, 주석)
3. 파일 패턴 기반 탐색 (설정 파일 찾기)

## Subagent Delegation Pattern (MANDATORY)

### Auto-Trigger Rules

**Before starting work, check:**

| Condition | Required Agent | Trigger |
|-----------|----------------|---------|
| 3+ 파일 탐색 필요 | `Explore` | 자동 |
| 3+ 단계 구현 필요 | `Plan` | 자동 |
| 아키텍처 이해 필요 | `Explore` | 자동 |
| 파일 분리/클래스 추출 | `refactoring-expert` | 자동 |
| 코드 변경 완료 | `superpowers:code-reviewer` | **항상** |
| 원인 불명확한 버그 | `root-cause-analyst` | 버그 분석 |
| 인증/권한/API 보안 | `security-engineer` | 보안 검토 |
| 성능 이슈 | `performance-engineer` | 성능 분석 |
| 외부 정보 필요 | `deep-research-agent` | 리서치 |

### Delegation Examples

```markdown
# Explore agent for codebase understanding
Task(Explore, "Find all authentication-related files and understand the auth flow")

# Plan agent for implementation
Task(Plan, "Design implementation strategy for user notification feature")

# Parallel agents for independent tasks
Task(Explore, "Find API endpoints") || Task(Explore, "Find test files")

# Code review after changes (MANDATORY)
Task(superpowers:code-reviewer, "Review the authentication changes")
```

### Self-Check Before Action

```yaml
Before ANY code work:
  □ 이 작업이 3단계 이상인가? → Plan agent 사용
  □ 여러 파일을 탐색해야 하는가? → Explore agent 사용
  □ 코드 구조를 변경하는가? → refactoring-expert 사용

After ANY code change:
  □ 코드를 수정했는가? → code-reviewer 사용 (필수!)
```

## Mandatory Code Review Pattern

### When Code Review is REQUIRED

- **모든** 코드 변경 후
- 새 기능 구현 완료 후
- 버그 수정 완료 후
- 리팩토링 완료 후
- PR/커밋 생성 전

### Code Review Workflow

```yaml
1. 코드 변경 완료
2. 변경 사항 확인 (git diff)
3. Code reviewer 호출:
   Task(superpowers:code-reviewer, "Review changes for [feature/fix]")
4. 피드백 반영
5. 필요시 재리뷰
6. 커밋/PR 생성
```

## Red Flags - STOP

이런 생각이 들면 **멈추고** 패턴 확인:

| 잘못된 생각 | 올바른 행동 |
|------------|------------|
| "grep으로 빨리 찾자" | LSP workspaceSymbol 사용 |
| "파일 읽어서 확인하자" | LSP documentSymbol 사용 |
| "간단해서 바로 수정" | 3단계 이상이면 Plan agent |
| "테스트 통과했으니 완료" | code-reviewer 호출 필수 |
| "혼자 할 수 있어" | 복잡하면 subagent 위임 |

## Pattern Compliance Checklist

### Before Starting

- [ ] LSP 사용 가능한 작업인가?
- [ ] 3단계 이상 작업인가? (→ Plan)
- [ ] 3개 이상 파일 탐색인가? (→ Explore)
- [ ] 코드 구조 변경인가? (→ refactoring-expert)

### During Work

- [ ] LSP 도구로 탐색하고 있는가?
- [ ] 필요한 곳에 subagent 위임했는가?
- [ ] 작업 진행 상황을 TodoWrite로 추적하는가?

### After Completion

- [ ] 코드 변경이 있었는가? (→ code-reviewer 필수)
- [ ] 피드백 반영했는가?
- [ ] 테스트 통과했는가?

## Integration

- **superpowers:code-reviewer**: 코드 리뷰 요청
- **superpowers:systematic-debugging**: 버그 분석
- **superpowers:test-driven-development**: TDD 워크플로우
