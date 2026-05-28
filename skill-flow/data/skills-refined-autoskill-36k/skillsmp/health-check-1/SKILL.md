---
name: health-check
description: |
  개발 환경 및 인증 상태 자동 검증. Use when (1) 온보딩 시 환경 확인,
  (2) 도구/인증 상태 체크, (3) `/SEMO:health-check` 명령,
  (4) orchestrator 업무 시작 시 자동 실행.
tools: [Bash, Read, Grep]
---

> **🔔 호출 시 메시지**: 이 Skill이 호출되면 `[SEMO] Skill: health-check` 시스템 메시지를 첫 줄에 출력하세요.

# health-check Skill

> 개발 환경 및 인증 상태 자동 검증 (통합 스킬)

## 🔴 플랫폼 자동 감지

> **이 스킬은 플랫폼을 자동 감지하여 해당 환경에 맞는 도구를 검증합니다.**

### 플랫폼 감지 순서

```bash
# 1. SEMO 메타데이터에서 position 확인
POSITION=$(cat ~/.claude.json 2>/dev/null | jq -r '.SEMO.position // "unknown"')

# 2. 프로젝트 파일로 Runtime 감지
detect_runtime() {
  if [ -f "next.config.ts" ] || [ -f "next.config.js" ] || [ -f "next.config.mjs" ]; then
    echo "nextjs"
  elif [ -f "build.gradle.kts" ] || [ -f "build.gradle" ]; then
    echo "spring"
  elif [ -f "docker-compose.yml" ] || [ -f "docker-compose.yaml" ]; then
    echo "infra"
  elif [ -f "go.mod" ]; then
    echo "go"
  else
    echo "generic"
  fi
}
```

### 플랫폼별 도구 매핑

| 플랫폼 | Position | 필수 도구 | 선택 도구 |
|--------|----------|-----------|----------|
| **nextjs** | developer | gh, git, node, pnpm, supabase | postgresql |
| **spring** | backend | gh, git, node, pnpm, supabase | postgresql |
| **infra** | infra | gh, git, docker | kubectl, terraform, nginx |
| **design** | designer | gh, git, node, pnpm, chrome | figma |
| **generic** | - | gh, git, node, pnpm | - |

---

## 트리거

- `/SEMO:health-check` 명령어
- "환경 확인", "도구 확인", "설치 확인" 키워드
- onboarding-master Agent에서 자동 호출
- orchestrator가 업무 시작 시 자동 실행 (30일 경과 시)

## 검증 항목 요약

### 필수 도구

| 도구 | 명령어 | 최소 버전 |
|------|--------|----------|
| GitHub CLI | `gh --version` | - |
| Git | `git --version` | - |
| Node.js | `node --version` | v18.0.0 |
| pnpm | `pnpm --version` | - |
| Supabase CLI | `supabase --version` | - |

### 인증 및 권한

| 항목 | 명령어 |
|------|--------|
| GitHub 인증 | `gh auth status` |
| Organization | `gh api user/orgs --jq '.[].login' \| grep semicolon-devteam` |
| docs 접근 | `gh api repos/semicolon-devteam/docs/contents/README.md` |
| core-supabase | `gh api repos/semicolon-devteam/core-supabase/contents/README.md` |

### 외부 서비스

| 항목 | 검증 방법 |
|------|----------|
| API 문서 사이트 | `curl` HTTP 200 체크 (`https://core-interface-ashen.vercel.app`) |

### SEMO 메타데이터

- 파일: `~/.claude.json`
- 필수 필드: `SEMO.role`, `SEMO.position`, `SEMO.boarded`, `SEMO.boardedAt`, `SEMO.healthCheckPassed`, `SEMO.lastHealthCheck`
- 검증 스크립트:

```bash
# SEMO 필드 존재 확인
cat ~/.claude.json | jq -e '.SEMO' >/dev/null 2>&1 || echo "❌ SEMO 메타데이터 없음"

# 필수 필드 검증
REQUIRED_FIELDS=("role" "position" "boarded" "boardedAt" "healthCheckPassed" "lastHealthCheck")
for field in "${REQUIRED_FIELDS[@]}"; do
  cat ~/.claude.json | jq -e ".SEMO.$field" >/dev/null 2>&1 || echo "❌ 필수 필드 누락: $field"
done

# position 값 검증 (developer)
POSITION=$(cat ~/.claude.json | jq -r '.SEMO.position')
VALID_POSITIONS=("developer" "po" "designer" "qa" "pm" "backend" "infra" "msa")
if [[ ! " ${VALID_POSITIONS[@]} " =~ " ${POSITION} " ]]; then
  echo "❌ 잘못된 position 값: $POSITION"
fi
```

**검증 성공 시**:
```markdown
✅ SEMO 메타데이터: 정상
  - role: fulltime
  - position: developer
  - boarded: true
  - boardedAt: 2025-12-09T10:30:00Z
  - healthCheckPassed: true
  - lastHealthCheck: 2025-12-09T10:30:00Z
```

**검증 실패 시**:
```markdown
❌ SEMO 메타데이터: 오류 발견

**문제**:
- ❌ 필수 필드 누락: lastHealthCheck
- ❌ 잘못된 position 값: dev (올바른 값: developer)

**해결**:
온보딩 프로세스를 완료하거나 `/SEMO:onboarding`을 실행하세요.
```

> **참조**: [SEMO Core Metadata Schema](https://github.com/semicolon-devteam/semo-core/blob/main/_shared/metadata-schema.md)

### SEMO 패키지 설치 상태

| 항목 | 검증 방법 |
|------|----------|
| 패키지 디렉토리 | `.claude/semo-core/`, `.claude/semo-next/` 존재 확인 |
| CLAUDE.md 심링크 | `.claude/CLAUDE.md` → `semo-next/CLAUDE.md` |
| agents 심링크 | `.claude/agents` → `semo-next/agents` |
| skills 심링크 | `.claude/skills` → `semo-next/skills` |
| commands 심링크 | `.claude/commands/SEMO` → `../semo-next/commands` |

### 글로벌 MCP 서버 설정 상태 (~/.claude.json)

| 항목 | 필수 | 설명 |
|------|------|------|
| mcpServers 필드 | ✅ | `~/.claude.json`에 mcpServers 존재 |
| context7 | ✅ | 라이브러리 문서 조회 |
| sequential-thinking | ✅ | 구조적 사고 분석 |

## 재검증 정책

- **온보딩 시**: 필수 실행
- **업무 시작 시**: 30일 경과 시 자동 실행
- **수동 요청 시**: `/SEMO:health-check` 명령어

## Related Skills

- `task-progress` - 작업 진행 추적
- Onboarding Agent - 온보딩 프로세스

## References

For detailed documentation, see:

- [Check Items](references/check-items.md) - 도구, 인증, 메타데이터 검증 상세
- [Output Format](references/output-format.md) - 성공/실패 출력, 해결 방법
