# Check Items

## 1. 필수 도구 설치

```yaml
gh_cli:
  command: "gh --version"
  required: true
  error: "GitHub CLI 미설치. `brew install gh` 실행 필요"

git:
  command: "git --version"
  required: true
  error: "Git 미설치. `brew install git` 실행 필요"

node:
  command: "node --version"
  required: true
  min_version: "v18.0.0"
  error: "Node.js 미설치 또는 v18 미만. `brew install node` 실행 필요"

pnpm:
  command: "pnpm --version"
  required: true
  error: "pnpm 미설치. `npm install -g pnpm` 실행 필요"

supabase:
  command: "supabase --version"
  required: true
  error: "Supabase CLI 미설치. `brew install supabase/tap/supabase` 실행 필요"
  note: "프론트엔드 개발자도 필수 (GraphQL/RPC 직접 연결)"

postgresql:
  command: "psql --version"
  required: false
  warn: "PostgreSQL 클라이언트 미설치 (선택). 유사시 디버깅에 필요"
```

## 2. 인증 및 권한

```yaml
github_auth:
  command: "gh auth status"
  required: true
  error: "GitHub 인증 필요. `gh auth login` 실행"

github_org:
  command: "gh api user/orgs --jq '.[].login' | grep semicolon-devteam"
  required: true
  error: "semicolon-devteam Organization 멤버십 없음. 관리자에게 초대 요청"

docs_access:
  command: "gh api repos/semicolon-devteam/docs/contents/README.md"
  required: true
  error: "docs 레포 접근 불가. Organization 멤버십 확인 필요"

core_supabase_access:
  command: "gh api repos/semicolon-devteam/core-supabase/contents/README.md"
  required: true
  error: "core-supabase 레포 접근 불가. Private repo 권한 확인 필요"
```

## 3. 외부 서비스 접근

```yaml
api_docs:
  url: "https://core-interface-ashen.vercel.app/#/"
  method: "curl_check"
  command: "curl -s -o /dev/null -w '%{http_code}' 'https://core-interface-ashen.vercel.app'"
  expected: "200"
  required: true
  error: "API 문서 사이트 접근 불가. 네트워크 연결 또는 VPN 확인 필요"
  note: "Semicolon API 명세 문서 (Swagger UI)"
```

### 검증 로직

```bash
# API 문서 접근 확인
HTTP_CODE=$(curl -s -o /dev/null -w '%{http_code}' 'https://core-interface-ashen.vercel.app' --max-time 10)
if [ "$HTTP_CODE" = "200" ]; then
  echo "✅ API 문서 사이트: 접근 가능"
else
  echo "❌ API 문서 사이트: 접근 불가 (HTTP $HTTP_CODE)"
fi
```

## 4. Slack 참여 (수동 확인)

```yaml
slack_workspace:
  method: "manual"
  question: "Slack 워크스페이스에 참여하셨나요? (y/n)"
  channels:
    - "#_공지"
    - "#_일반"
    - "#_협업"
    - "할당받은 프로젝트 채널 (#cm-*, #alarm-*, etc.)"
```

## 4. Claude Code Global Config 확인

```yaml
claude_json_check:
  file: "~/.claude.json"
  platform_paths:
    macOS: "~/.claude.json"
    Linux: "~/.claude.json"
    Windows: "~/.claude.json (WSL2 Linux filesystem)"
  checks:
    - file_exists: "~/.claude.json 파일 존재 여부"
    - sax_metadata: "SEMO 메타데이터 존재 여부"
    - required_fields:
        - "SEMO.role" (fulltime, parttimer, contractor)
        - "SEMO.position" (developer, po, designer)
        - "SEMO.boarded" (true/false)
        - "SEMO.healthCheckPassed" (true/false)
    - optional_fields:
        - "SEMO.lastHealthCheck" (ISO 8601 timestamp)
        - "SEMO.participantProjects" (array)
        - "SEMO.currentTask" (object: repo, issue, branch)
```

### Claude Config 검증 로직

```bash
# 1. 파일 존재 확인
if [ -f ~/.claude.json ]; then
  echo "✅ ~/.claude.json 파일 존재"
else
  echo "⚠️  ~/.claude.json 파일 없음 (첫 실행 시 자동 생성됨)"
fi

# 2. SEMO 메타데이터 확인 (jq 사용)
if jq -e '.SEMO' ~/.claude.json > /dev/null 2>&1; then
  echo "✅ SEMO 메타데이터 존재"

  # 필수 필드 확인
  ROLE=$(jq -r '.SEMO.role // "missing"' ~/.claude.json)
  POSITION=$(jq -r '.SEMO.position // "missing"' ~/.claude.json)
  BOARDED=$(jq -r '.SEMO.boarded // "missing"' ~/.claude.json)

  echo "  - role: $ROLE"
  echo "  - position: $POSITION"
  echo "  - boarded: $BOARDED"
else
  echo "⚠️  SEMO 메타데이터 없음 (온보딩 필요)"
fi
```

## 5. SEMO 패키지 설치 상태

```yaml
sax_package_installed:
  check_type: "directory_exists"
  paths:
    - ".claude/semo-core/"
    - ".claude/semo-next/"
  required: true
  error: "SEMO 패키지 미설치. `SEMO 업데이트해줘` 실행 필요"

symlinks_valid:
  check_type: "symlink_target"
  items:
    - path: ".claude/CLAUDE.md"
      expected_target: "semo-next/CLAUDE.md"
    - path: ".claude/agents"
      expected_target: "semo-next/agents"
    - path: ".claude/skills"
      expected_target: "semo-next/skills"
    - path: ".claude/commands/SEMO"
      expected_target: "../semo-next/commands"
      critical: true  # 🔴 누락 시 /SEMO:* 명령어 인식 불가
  required: true
  error: "심링크 연결 오류. `SEMO 업데이트해줘` 실행하여 심링크 재설정 필요"
```

> **🔴 중요**: `commands/SEMO` 심링크가 누락되면 `/SEMO:help`, `/SEMO:health-check` 등 모든 SEMO 명령어가 인식되지 않습니다.

### 패키지 검증 로직

```bash
# 1. 패키지 디렉토리 존재 확인
if [ -d ".claude/semo-core" ] && [ -d ".claude/semo-next" ]; then
  echo "✅ SEMO 패키지 설치됨"
else
  echo "❌ SEMO 패키지 미설치"
  echo "  → `SEMO 업데이트해줘` 실행 필요"
fi

# 2. 심링크 상태 확인
check_symlink() {
  local path=$1
  local expected=$2
  if [ -L "$path" ]; then
    actual=$(readlink "$path")
    if [ "$actual" = "$expected" ]; then
      echo "✅ $path → $expected"
    else
      echo "⚠️  $path → $actual (예상: $expected)"
    fi
  else
    echo "❌ $path 심링크 아님 또는 없음"
  fi
}

check_symlink ".claude/CLAUDE.md" "semo-next/CLAUDE.md"
check_symlink ".claude/agents" "semo-next/agents"
check_symlink ".claude/skills" "semo-next/skills"
check_symlink ".claude/commands/SEMO" "../semo-next/commands"
```

## 6. 글로벌 MCP 서버 설정 상태

> **참고**: 글로벌 `~/.claude.json`에 MCP 설정을 등록하면 모든 프로젝트에서 공통으로 사용됩니다.

```yaml
global_mcp_settings:
  file: "~/.claude.json"
  check_type: "json_field"
  field: "mcpServers"
  required: true
  error: "글로벌 MCP 설정 없음. ~/.claude.json에 mcpServers 추가 필요"

required_mcps:
  - name: "context7"
    description: "라이브러리 문서 조회"
    required: true
  - name: "sequential-thinking"
    description: "구조적 사고 분석"
    required: true
```

### 글로벌 MCP 검증 로직

```bash
# 1. ~/.claude.json 존재 확인
if [ -f ~/.claude.json ]; then
  echo "✅ ~/.claude.json 파일 존재"
else
  echo "❌ ~/.claude.json 파일 없음"
  echo "  → Claude Code 첫 실행 또는 설정 파일 생성 필요"
  exit 1
fi

# 2. mcpServers 필드 존재 확인
if jq -e '.mcpServers' ~/.claude.json > /dev/null 2>&1; then
  echo "✅ mcpServers 필드 존재"
else
  echo "❌ mcpServers 필드 없음"
  echo "  → ~/.claude.json에 mcpServers 설정 추가 필요"
fi

# 3. 필수 MCP 서버 설정 확인
check_global_mcp() {
  local mcp_name=$1
  if jq -e ".mcpServers.$mcp_name" ~/.claude.json > /dev/null 2>&1; then
    echo "✅ 글로벌 MCP: $mcp_name 설정됨"
  else
    echo "❌ 글로벌 MCP: $mcp_name 미설정 (필수)"
  fi
}

check_global_mcp "context7"
check_global_mcp "sequential-thinking"
```

### 글로벌 MCP 설정 템플릿

`~/.claude.json`에 추가할 MCP 설정:

```json
{
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
}
```

### 설정 방법

기존 `~/.claude.json`에 `mcpServers` 필드가 없는 경우:

```bash
# jq를 사용하여 mcpServers 추가
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
