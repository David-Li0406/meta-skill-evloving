# Fix Guide

> audit-semo에서 발견된 문제 유형별 수정 가이드

## Agent 문제 수정

### 🔴 model 필드 누락

**문제**:
```yaml
---
name: example-agent
description: ...
tools: [...]
# model 필드 없음
---
```

**수정**:
```yaml
---
name: example-agent
description: ...
tools: [...]
model: sonnet  # 추가
---
```

**Model 선택 기준**:

| 상황 | 권장 model |
|------|-----------|
| 복잡한 분석, 아키텍처 결정 | `opus` |
| 일반 구현, 품질 중심 작업 | `sonnet` |
| 단순 조회, 빠른 응답 필요 | `haiku` |
| Orchestrator (부모 모델 상속) | `inherit` |

**수정 위임**:
```markdown
[SEMO] Agent: agent-manager 호출 - update

대상: semo-next/agents/example-agent/example-agent.md
작업: Frontmatter에 model: sonnet 추가
```

---

### 🔴 PROACTIVELY 패턴 누락

**문제**:
```yaml
description: Code reviewer for pull requests.
```

**수정**:
```yaml
description: |
  Code reviewer for pull requests. PROACTIVELY use when:
  (1) PR 리뷰 요청, (2) 코드 품질 검토, (3) 보안 취약점 확인.
```

**패턴 규칙**:
- `PROACTIVELY use when:` 필수 포함
- 최소 2개 이상의 트리거 조건 명시
- 번호 형식: `(1) 조건1, (2) 조건2, (3) 조건3.`

---

### 🟡 200 lines 초과

**문제**: Agent 본문이 200 lines 초과

**수정 방법**:

1. **references/ 디렉토리 생성**:
```bash
mkdir -p semo-next/agents/example-agent/references
```

2. **상세 내용 분리**:
```text
agents/example-agent/
├── example-agent.md     # 핵심만 (~150 lines)
└── references/
    ├── workflow.md      # 상세 워크플로우
    ├── templates.md     # 출력 템플릿
    └── examples.md      # 사용 예시
```

3. **본문에 참조 링크 추가**:
```markdown
## References

- [Workflow 상세](references/workflow.md)
- [템플릿](references/templates.md)
```

---

### 🟡 금지 도구 사용

**문제**:
```yaml
tools:
  - grep_search      # ❌
  - write_to_file    # ❌
```

**수정**:
```yaml
tools:
  - grep             # ✅
  - write_file       # ✅
```

**도구명 매핑**:

| 금지 | 표준 |
|------|------|
| `grep_search` | `grep` |
| `write_to_file` | `write_file` |
| `read_file` | `read_file` (유지) |
| `slash_command` | `skill` |
| `web_fetch` | (제거 - 미사용) |

---

## Skill 문제 수정

### 🔴 시스템 메시지 누락

**문제**: Frontmatter 직후 시스템 메시지 없음

**수정**: Frontmatter 바로 다음 줄에 추가

```markdown
---
name: example-skill
description: ...
tools: [...]
---

> **🔔 시스템 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: example-skill 호출 - {context}` 시스템 메시지를 첫 줄에 출력하세요.

# example-skill Skill
...
```

**형식 규칙**:
- `> **🔔 시스템 메시지**:` 로 시작
- Skill 이름을 정확히 명시
- `{context}` 플레이스홀더 포함

---

### 🟡 "Use when" 패턴 누락

**문제**:
```yaml
description: Slack 채널에 메시지 전송.
```

**수정**:
```yaml
description: |
  Slack 채널에 메시지 전송. Use when (1) 릴리스 알림,
  (2) 이슈 알림, (3) 팀원 멘션 요청.
```

---

### 🟡 100 lines 초과

**문제**: SKILL.md가 100 lines 초과

**수정 방법**:

1. **references/ 디렉토리 생성**
2. **상세 내용 분리**:
```text
skills/example-skill/
├── SKILL.md              # 핵심만 (~80 lines)
└── references/
    ├── workflow.md       # 상세 워크플로우
    ├── api-commands.md   # API/CLI 명령어
    └── templates.md      # 메시지 템플릿
```

**분리 기준**:

| 섹션 | 위치 |
|------|------|
| Purpose, Quick Start | SKILL.md 유지 |
| 상세 워크플로우 | references/workflow.md |
| API/GraphQL 쿼리 | references/api-commands.md |
| 출력 템플릿 | references/templates.md |

---

## Command 문제 수정

### 🔴 Frontmatter 누락

**문제**: name 또는 description 없음

**수정**:
```markdown
---
name: example-command
description: 커맨드 설명
---
```

---

### 🟡 CLAUDE.md 미등록

**문제**: commands 디렉토리에 파일 있으나 CLAUDE.md에 미등록

**수정**: CLAUDE.md의 Commands 섹션에 추가

```markdown
## Commands

| 커맨드 | 설명 |
|--------|------|
| `/SEMO:example` | 커맨드 설명 |  <!-- 추가 -->
```

---

## 수정 자동화

### agent-manager 위임

```markdown
[SEMO] Agent: agent-manager 호출 - update

## 수정 대상
- semo-next/agents/example-agent/example-agent.md

## 수정 내용
1. Frontmatter에 `model: sonnet` 추가
2. description에 PROACTIVELY 패턴 추가
```

### skill-manager 위임

```markdown
[SEMO] Agent: skill-manager 호출 - update

## 수정 대상
- semo-po/skills/example-skill/SKILL.md

## 수정 내용
1. 시스템 메시지 추가 (Frontmatter 직후)
2. references/ 분리 (현재 150 lines)
```

---

## 수정 후 검증

```bash
# 수정 후 재검사
[SEMO] Skill: package-validator 호출 - semo-next

# 또는 전체 재감사
[SEMO] Skill: audit-semo 호출 - 전체
```
