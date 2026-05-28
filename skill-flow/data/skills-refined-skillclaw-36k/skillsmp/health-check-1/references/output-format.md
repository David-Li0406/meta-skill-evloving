# Output Format

## 성공 시

```markdown
=== SEMO 환경 검증 결과 ===

## 필수 도구

✅ GitHub CLI: v2.40.0
✅ Git: v2.43.0
✅ Node.js: v20.10.0
✅ pnpm: v8.14.0
✅ Supabase CLI: v1.142.0
⚠️  PostgreSQL: 미설치 (선택, 유사시 디버깅에 필요)

## 인증 및 권한

✅ GitHub 인증: 완료
✅ semicolon-devteam 멤버십: 확인
✅ docs 레포 접근: 가능
✅ core-supabase 레포 접근: 가능

## 조직 참여

✅ Slack 워크스페이스 참여: 확인

## SEMO 메타데이터 (~/.claude.json)

✅ 파일 존재
✅ SEMO 메타데이터 존재
  - role: parttimer
  - position: developer
  - boarded: true
  - healthCheckPassed: true
  - lastHealthCheck: 2025-11-25T10:30:00Z

## SEMO 패키지 설치

✅ semo-core: 설치됨
✅ semo-next: 설치됨
✅ CLAUDE.md → semo-next/CLAUDE.md
✅ agents → semo-next/agents
✅ skills → semo-next/skills
✅ commands/SEMO → ../semo-next/commands

## 글로벌 MCP 서버 설정 (~/.claude.json)

✅ mcpServers 필드 존재
✅ 글로벌 MCP: context7 설정됨
✅ 글로벌 MCP: sequential-thinking 설정됨

=== 결과 ===
✅ 모든 필수 항목 통과
⚠️  1개 선택 항목 미설치 (PostgreSQL)

**다음 단계**: 온보딩 완료. 업무 할당을 대기하거나 `/SEMO:onboarding`으로 SEMO 학습을 진행하세요.
```

## 실패 시

```markdown
=== SEMO 환경 검증 결과 ===

✅ GitHub CLI: v2.40.0
❌ Git: 미설치
✅ Node.js: v20.10.0
❌ pnpm: 미설치
❌ Supabase CLI: 미설치

❌ GitHub 인증: 필요
✅ semicolon-devteam 멤버십: 확인
❌ docs 레포 접근: 불가

=== 결과 ===
❌ 5개 필수 항목 미통과

**해결 방법**:

### 1. Git 설치
```bash
brew install git
```

### 2. pnpm 설치
```bash
npm install -g pnpm
```

### 3. Supabase CLI 설치
```bash
brew install supabase/tap/supabase
```

### 4. GitHub 인증
```bash
gh auth login
```

### 5. docs 레포 접근
- GitHub Organization 멤버십 확인
- 관리자에게 권한 요청

### 6. 글로벌 MCP 서버 설정

```bash
# ~/.claude.json에 mcpServers 추가
jq '. + {
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    }
  }
}' ~/.claude.json > ~/.claude.json.tmp && mv ~/.claude.json.tmp ~/.claude.json
```

**재검증**: `/SEMO:health-check` 명령어로 다시 확인하세요.
```

## SEMO 메타데이터 저장

검증 완료 시 `~/.claude.json`에 SEMO 메타데이터 저장:

```json
{
  "SEMO": {
    "role": "parttimer",
    "position": "developer",
    "boarded": true,
    "healthCheckPassed": true,
    "lastHealthCheck": "2025-11-25T10:30:00Z",
    "participantProjects": []
  }
}
```

## 재검증 정책

- **온보딩 시**: 필수 실행
- **업무 시작 시**: orchestrator가 자동 실행 (30일 경과 시)
- **수동 요청 시**: `/SEMO:health-check` 명령어
