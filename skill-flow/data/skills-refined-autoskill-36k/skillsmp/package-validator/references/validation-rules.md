# Validation Rules

> package-validator의 검증 규칙 상세 (Sub-Agent 최적화 규칙 적용)

## 1. Frontmatter 검증 (Sub-Agent 최적화)

### Agent Frontmatter (필수 4개 필드)

```yaml
---
name: {agent-name}                    # 파일명과 일치 (확장자 제외)
description: |                        # PROACTIVELY 패턴 필수
  {역할 요약}. PROACTIVELY use when:
  (1) {조건1}, (2) {조건2}, (3) {조건3},
  (4) {조건4}. {추가 설명}.
tools:                                 # 표준 도구명만 사용
  - read_file
  - write_file    # NOT write_to_file
  - grep          # NOT grep_search
model: sonnet                          # opus|sonnet|haiku|inherit (필수)
---
```

### Skill Frontmatter

```yaml
---
name: {skill-name}                    # 디렉토리명과 일치
description: {역할 요약}. Use when (1) {조건1}, (2) {조건2}, (3) {조건3}.
tools: [Bash, Read, Write]            # 사용 도구 명시
---
```

### 검증 항목

**필수 필드**:

- ✅ name 필드 존재 및 파일명 일치
- ✅ description 필드 존재 및 **PROACTIVELY use when:** 패턴 포함
- ✅ description에 번호된 트리거 조건 (1), (2), (3) 존재
- ✅ tools 필드 존재 (Agent 필수, Skill 권장)
- ✅ **model 필드 존재** (opus|sonnet|haiku|inherit 중 하나)

**도구 표준화**:

- ✅ `grep` 사용 (NOT grep_search)
- ✅ `write_file` 사용 (NOT write_to_file)
- ❌ `slash_command` 사용 금지
- ❌ `web_fetch` 사용 금지
- ❌ `mcp:*` 형식 사용 금지

**Model 선택 적합성**:

- ✅ Orchestrator → `inherit`
- ✅ 아키텍처/분석 Agent → `opus`
- ✅ 구현/품질 Agent → `sonnet`
- ✅ 교육/조회 Agent → `haiku`

## 2. 파일 네이밍 검증

### 규칙

- ✅ kebab-case 사용 (`agent-name.md`, `skill-name/`)
- ✅ 명확한 역할 표현
- ❌ camelCase, snake_case 금지
- ❌ 이중 콜론 발생 구조 금지 (예: `SAX/:command.md` → `/SEMO::command`)

### 검증 명령

```bash
# kebab-case 검증 (소문자, 하이픈만 허용)
pattern: ^[a-z0-9]+(-[a-z0-9]+)*$

# Agent 파일명 검증
agents/*.md → kebab-case 확인

# Skill 디렉토리명 검증
skills/*/ → kebab-case 확인

# Command 파일명 검증
commands/SEMO/*.md → 콜론 프리픽스 없음 확인
```

## 3. CLAUDE.md 검증

### 필수 섹션

```markdown
## Package Info
## SEMO란?
## Package Components
### Agents
### Skills
### Commands (선택적)
## Versioning Rules
## References
```

### 검증 항목

- ✅ 모든 필수 섹션 존재
- ✅ Agents 테이블에 실제 파일 존재하는 Agent만 나열
- ✅ Skills 테이블에 실제 디렉토리 존재하는 Skill만 나열
- ✅ Commands 테이블에 실제 파일 존재하는 Command만 나열
- ✅ 파일 경로 정확성 (상대 경로)

## 4. orchestrator.md 검증

### Routing Decision Table

```markdown
| User Intent | Route To | Detection Keywords |
|-------------|----------|-------------------|
| {intent} | `{agent-name}` | "{keyword1}", "{keyword2}" |
```

### 검증 항목

- ✅ 테이블에 나열된 Agent가 실제 존재
- ✅ Agent 파일명과 Route To 값 일치
- ✅ Detection Keywords 형식 정확 (쌍따옴표)

## 5. Progressive Disclosure 검증

### 구조

```
skills/{skill-name}/
    ├── SKILL.md        # 필수: 핵심 워크플로우 (<100 lines)
    └── references/     # 선택적: 상세 레퍼런스
        ├── workflow.md
        └── examples.md
```

### 검증 항목

- ✅ SKILL.md 파일 존재
- ✅ SKILL.md 100 lines 이하 (권장)
- ✅ references/ 디렉토리 존재 시 최소 1개 파일 포함
- ✅ SKILL.md에서 references/ 파일 참조 시 경로 정확성
