# Validation Process

> package-validator의 5단계 검증 프로세스

## Phase 1: 파일 구조 스캔

```bash
# 1. Agent 파일 수집
agents/*.md

# 2. Skill 디렉토리 수집
skills/*/

# 3. Command 파일 수집 (해당 시)
commands/SEMO/*.md

# 4. 설정 파일 확인
CLAUDE.md, agents/orchestrator.md
```

## Phase 2: Frontmatter 검증

각 Agent/Skill 파일에 대해:

1. YAML Frontmatter 파싱
2. 필수 필드 존재 검증
3. 필드 값 형식 검증
4. name 필드와 파일명 일치 검증

```bash
# Frontmatter 추출 및 검증
head -n 10 {file} | grep -E "^(name|description|tools):"
```

## Phase 3: CLAUDE.md 일관성 검증

### Agents 섹션

- 테이블 내 각 Agent 파일 존재 확인
- 누락된 Agent 없는지 확인
- 파일 경로 정확성 확인

### Skills 섹션

- 테이블 내 각 Skill 디렉토리 존재 확인
- 누락된 Skill 없는지 확인
- 파일 경로 정확성 확인

### Commands 섹션

- 테이블 내 각 Command 파일 존재 확인
- 누락된 Command 없는지 확인

## Phase 4: orchestrator 라우팅 검증

1. Routing Decision Table 파싱
2. 각 Route To Agent 실제 존재 확인
3. Agent 파일명과 라우팅 이름 일치 확인

```bash
# orchestrator.md에서 라우팅 테이블 추출
grep -E "^\| .+ \| \`" agents/orchestrator.md
```

## Phase 5: 네이밍 규칙 검증

```bash
# kebab-case 검증 (소문자, 하이픈만 허용)
pattern: ^[a-z0-9]+(-[a-z0-9]+)*$

# 이중 콜론 방지 검증
commands/SEMO/ 내 파일명에 ':' 프리픽스 없음 확인
```

## Input Schema

```json
{
  "package": "semo-po|semo-next|semo-meta",
  "scope": "full|agents|skills|commands|config"
}
```

**Parameters**:
- `package`: 검증 대상 패키지
- `scope`: 검증 범위
  - `full`: 전체 검증
  - `agents`: Agent만
  - `skills`: Skill만
  - `commands`: Command만
  - `config`: CLAUDE.md만
