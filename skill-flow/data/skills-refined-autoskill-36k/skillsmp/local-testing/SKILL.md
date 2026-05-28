---
name: local-testing
description: Use when testing features with local backend integration - runs codebase E2E tests by default, uses Claude in Chrome only when explicitly requested with --browser flag
---

# Local Testing

## Overview

로컬 백엔드와 프론트엔드를 함께 띄우고 테스트를 수행하는 워크플로우.

**Core principle:**
- **기본**: 코드베이스 E2E 테스트 실행
- **선택**: `--browser` 플래그 시 Claude in Chrome으로 실시간 브라우저 인터랙션

## No Mock Data Policy

**중요**: 이 테스트 환경은 Mock 데이터를 사용하지 않습니다.

- **Mock 사용 금지**: MSW, Jest mock, fixture 데이터 사용 안함
- **실제 로컬 서버 사용**: 모든 API 호출은 실제 백엔드 서버로 전송
- **실제 데이터베이스 사용**: PostgreSQL (Docker) 또는 기타 DB
- **실제 인증 사용**: 실제 인증 플로우 테스트

```
Frontend (localhost:PORT)
    ↓ HTTP requests
Backend (localhost:API_PORT)
    ↓ Database queries
Database (localhost:DB_PORT)
```

## When to Use

- 개발한 기능을 로컬에서 실제 백엔드와 연동 테스트
- "로컬에서 테스트", "백엔드 연동 테스트" 언급
- API 호출과 UI 상호작용을 함께 검증

**Don't use for:**
- 프로덕션/스테이징 환경 테스트
- 백엔드 없이 프론트만 테스트

## Usage

```bash
# E2E 테스트 실행 (기본, 권장)
/local-testing [test-name]

# 브라우저 인터랙션 테스트 (요청 시에만)
/local-testing [page-path] --browser
```

## Testing Modes

### Mode 1: E2E Test (Default)

**When**: 자동화된 테스트, CI/CD, 반복 가능한 검증

```yaml
workflow:
  1. 서버 상태 확인 (curl health check)
  2. E2E 테스트 실행 (pnpm test:e2e 또는 npm run test:e2e)
  3. 결과 리포트 확인
```

### Mode 2: Browser (--browser flag)

**When**: 수동 디버깅, 실시간 UI 확인, 복잡한 인터랙션 탐색

```yaml
workflow:
  1. 서버 상태 확인
  2. Claude in Chrome 연결
  3. 로그인 수행 (필요시)
  4. 페이지 탐색 및 인터랙션
  5. 네트워크/콘솔 검증
```

## Quick Reference

| Mode | Command | Use Case |
|------|---------|----------|
| Default | E2E test runner | 자동화된 E2E 테스트, 회귀 테스트 |
| --browser | Claude in Chrome | 수동 디버깅, 실시간 확인 |

## Implementation: E2E Test (Default)

### Phase 1: Server Check

```bash
# Verify servers are running (adjust ports for your project)
curl -s http://localhost:API_PORT/health > /dev/null && echo "✅ Backend OK" || echo "❌ Backend not running"
curl -s http://localhost:FRONTEND_PORT > /dev/null && echo "✅ Frontend OK" || echo "❌ Frontend not running"
```

### Phase 2: Run E2E Tests

```bash
# Run all E2E tests (adjust command for your project)
pnpm test:e2e
# or
npm run test:e2e

# Run specific test file
pnpm test:e2e tests/e2e/login.spec.ts

# Run tests matching pattern
pnpm test:e2e --grep "login"
```

### Phase 3: Review Results

```bash
# View test report (if html reporter configured)
open playwright-report/index.html

# Check test output for failures
```

## Implementation: Browser Mode (--browser flag)

### Phase 1: Check Servers

```bash
# Check and start if needed
curl -s http://localhost:API_PORT/health > /dev/null || echo "❌ Start backend first"
curl -s http://localhost:FRONTEND_PORT > /dev/null || echo "❌ Start frontend first"
```

### Phase 2: Connect Chrome

```bash
# Get tab context
mcp-cli call claude-in-chrome/tabs_context_mcp '{"createIfEmpty": true}'

# Navigate to frontend
mcp-cli call claude-in-chrome/navigate '{"url": "http://localhost:FRONTEND_PORT", "tabId": <TAB_ID>}'
```

### Phase 3: Authentication (if needed)

```bash
# Read page for login form
mcp-cli call claude-in-chrome/read_page '{"tabId": <TAB_ID>, "filter": "interactive"}'

# Type credentials
mcp-cli call claude-in-chrome/computer '{"tabId": <TAB_ID>, "action": "left_click", "ref": "<EMAIL_REF>"}'
mcp-cli call claude-in-chrome/computer '{"tabId": <TAB_ID>, "action": "key", "text": "cmd+a"}'
mcp-cli call claude-in-chrome/computer '{"tabId": <TAB_ID>, "action": "type", "text": "test@example.com"}'
mcp-cli call claude-in-chrome/computer '{"tabId": <TAB_ID>, "action": "key", "text": "Tab"}'
mcp-cli call claude-in-chrome/computer '{"tabId": <TAB_ID>, "action": "type", "text": "password"}'
mcp-cli call claude-in-chrome/computer '{"tabId": <TAB_ID>, "action": "key", "text": "Enter"}'
```

### Phase 4: Navigate & Test

```bash
# Navigate to target page
mcp-cli call claude-in-chrome/navigate '{"url": "http://localhost:FRONTEND_PORT/<path>", "tabId": <TAB_ID>}'

# Read page structure
mcp-cli call claude-in-chrome/read_page '{"tabId": <TAB_ID>}'
```

### Phase 5: Verification

```bash
# Check network requests
mcp-cli call claude-in-chrome/read_network_requests '{"tabId": <TAB_ID>}'

# Check console for errors
mcp-cli call claude-in-chrome/read_console_messages '{"tabId": <TAB_ID>, "pattern": "error|Error"}'
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| 서버 미실행 상태로 테스트 | curl로 health check 먼저 |
| E2E 테스트 환경 미설정 | Playwright 설치 및 설정 확인 |
| 탭 ID 재사용 (browser mode) | 매번 tabs_context_mcp 호출 |
| 로그인 없이 페이지 접근 | 인증 필요 페이지는 로그인 먼저 |
| Backend 코드 변경 미반영 | 서버 재시작 또는 재빌드 |

## Red Flags - STOP

- 서버 시작 안 됨 → 에러 로그 확인
- 로그인 실패 → test credentials 확인
- 페이지 로드 안 됨 → 네트워크/콘솔 에러 확인
- API 호출 실패 → 백엔드 로그 확인

## E2E Test Best Practices

### Element Selection

```typescript
// ❌ Bad - Selects wrong element
const heading = page.locator('h1').first();

// ✅ Good - Targets page content
const heading = page.locator('main h1').first();
```

### Error State Testing

```typescript
test('should not display error state', async ({ page }) => {
  await page.waitForLoadState('networkidle');
  await expect(page.locator('text=Error')).not.toBeVisible();
});
```

## Integration

- **E2E 테스트**: 기본 테스트 방법
- **Claude in Chrome**: 브라우저 인터랙션 (--browser)
- **superpowers:systematic-debugging**: 테스트 중 버그 발견 시
- **superpowers:requesting-code-review**: 테스트 성공 후 코드 리뷰
