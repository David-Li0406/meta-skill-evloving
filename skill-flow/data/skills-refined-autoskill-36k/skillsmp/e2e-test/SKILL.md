---
name: e2e-test
description: |
  Playwright E2E 테스트 실행. Use when (1) "E2E 테스트", "런타임 테스트",
  (2) 구현 완료 후 브라우저 검증, (3) PR 전 통합 테스트.
tools: [Bash, Playwright MCP]
triggers:
  - E2E 테스트해줘
  - 런타임 테스트
  - 브라우저 테스트
---

> **시스템 메시지**: `[SEMO] Skill: e2e-test 호출`

# E2E Test Skill

> Playwright 기반 런타임 테스트 자동화

## Purpose

구현 완료 후 실제 브라우저에서 동작을 검증합니다:

1. 페이지 로드 및 렌더링 확인
2. 주요 유저 플로우 테스트
3. 콘솔 에러 검출
4. 반응형 레이아웃 확인

## 🔴 필수 실행 시점 (NON-NEGOTIABLE)

> **구현 완료 후, PR 생성 전 반드시 E2E 테스트를 실행합니다.**

| 시점 | 동작 |
|------|------|
| v0.4.x CODE 완료 후 | E2E 테스트 자동 제안 |
| "리뷰해줘" 전 | E2E 통과 확인 |
| PR 생성 전 | E2E 결과 포함 필수 |

## Workflow

### Step 1: Dev Server 확인

```bash
# 개발 서버 실행 여부 확인
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000

# 실행 안 되어 있으면
npm run dev &
sleep 5
```

### Step 2: Playwright로 페이지 접근

```typescript
// MCP 호출
mcp__playwright__playwright_navigate({
  url: "http://localhost:3000/{path}",
  waitUntil: "networkidle"
})
```

### Step 3: 기본 검증

```typescript
// 1. 페이지 스냅샷
mcp__playwright__playwright_screenshot({ name: "page-load" })

// 2. 콘솔 에러 확인
mcp__playwright__playwright_console_logs({ type: "error" })

// 3. 주요 요소 확인
mcp__playwright__playwright_get_visible_text()
```

### Step 4: 인터랙션 테스트 (선택)

```typescript
// 버튼 클릭
mcp__playwright__playwright_click({ selector: "[data-testid='submit-btn']" })

// 폼 입력
mcp__playwright__playwright_fill({ selector: "input[name='email']", value: "test@example.com" })

// 결과 확인
mcp__playwright__playwright_screenshot({ name: "after-interaction" })
```

## Test Scenarios

### 기본 시나리오 (필수)

| # | 테스트 | 검증 내용 |
|---|--------|----------|
| 1 | 페이지 로드 | HTTP 200, 렌더링 완료 |
| 2 | 콘솔 에러 | JavaScript 에러 없음 |
| 3 | 주요 UI | 핵심 컴포넌트 표시 |

### 확장 시나리오 (권장)

| # | 테스트 | 검증 내용 |
|---|--------|----------|
| 4 | 유저 플로우 | 주요 인터랙션 동작 |
| 5 | 에러 상태 | 에러 UI 표시 |
| 6 | 빈 상태 | Empty State 표시 |
| 7 | 반응형 | 모바일/데스크톱 레이아웃 |

## Output Format

```markdown
## 🧪 E2E Test Results

**Environment**:
| 항목 | 값 |
|------|-----|
| URL | http://localhost:3000/{path} |
| Browser | Chromium (Playwright) |
| Viewport | 1280x720 |

### Test Results

| # | 테스트 | 결과 | 상세 |
|---|--------|------|------|
| 1 | 페이지 로드 | ✅ | 1.2s |
| 2 | 콘솔 에러 | ✅ | 0 errors |
| 3 | 주요 UI | ✅ | Header, List, Filter 확인 |
| 4 | 인터랙션 | ✅ | 버튼 클릭 정상 |

### Screenshots
- `page-load.png`: 초기 로드 상태
- `after-interaction.png`: 인터랙션 후 상태

### Status: ✅ E2E TEST PASSED
```

## 실패 시 처리

```markdown
## 🧪 E2E Test Results

### Status: ❌ E2E TEST FAILED

### 발견된 이슈

| # | 이슈 | 심각도 | 상세 |
|---|------|--------|------|
| 1 | 콘솔 에러 | 🔴 Critical | `TypeError: Cannot read property 'map' of undefined` |
| 2 | UI 미표시 | 🟡 Warning | Header 컴포넌트 미렌더링 |

### 권장 조치

1. **콘솔 에러 수정** (필수)
   - 파일: `app/{domain}/_components/{Component}.tsx`
   - 원인: 데이터 로딩 전 map 호출
   - 해결: Optional chaining 또는 로딩 상태 처리

2. **UI 확인** (권장)
   - Header import 확인

### 다음 단계

에러 수정 후 다시 E2E 테스트를 실행하세요:
> "E2E 테스트해줘"

**🚫 E2E 실패 시 PR 생성 차단**
```

## 반응형 테스트

```typescript
// 모바일 뷰포트
mcp__playwright__playwright_resize({ device: "iPhone 13" })
mcp__playwright__playwright_screenshot({ name: "mobile-view" })

// 데스크톱 뷰포트
mcp__playwright__playwright_resize({ width: 1920, height: 1080 })
mcp__playwright__playwright_screenshot({ name: "desktop-view" })
```

## PR 차단 조건

| 조건 | PR 가능 여부 |
|------|-------------|
| E2E 전체 통과 | ✅ 가능 |
| 콘솔 에러 있음 | ❌ 차단 |
| 주요 UI 미표시 | ❌ 차단 |
| 반응형 이슈 | ⚠️ 경고 (진행 가능) |

## Related Skills

- `verify` - PR 전 종합 검증
- `review-task` - 태스크 리뷰
- `git-workflow` - PR 생성

## References

- [Browser Testing Guide](../_shared/browser-testing.md)
- [Playwright MCP Documentation](https://github.com/anthropics/mcp-server-playwright)
