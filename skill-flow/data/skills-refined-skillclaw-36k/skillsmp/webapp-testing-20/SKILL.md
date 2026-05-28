---
name: webapp-testing
description: >
  Docker 환경에서 Playwright E2E 테스트 실행.
  브라우저 미종료 문제 해결, 스크린샷, 로그 캡처 지원.
version: 2.0.0

triggers:
  keywords:
    - "webapp test"
    - "E2E docker"
    - "playwright test"
    - "브라우저 테스트"
  file_patterns:
    - "playwright.config.ts"
    - "e2e/**/*"
  context:
    - "웹앱 E2E 테스트"
    - "Docker 환경 테스트"

capabilities:
  - safe_browser
  - docker_server_test
  - screenshot_capture

model_preference: sonnet

auto_trigger: false
---

# Web Application Testing (Docker 환경)

Docker Compose로 서버를 관리하는 환경에서 Playwright E2E 테스트를 실행합니다.

## Quick Start

```bash
# 서버 상태 확인
docker ps --filter "name=frontend"

# Playwright 테스트 실행
cd D:\AI\claude01\wsoptv\apps\web
npx playwright test

# 특정 테스트만
npx playwright test e2e/specs/auth/
```

## 핵심: 브라우저 종료 보장

**문제**: Playwright 브라우저가 종료되지 않는 경우 발생

### 해결 패턴 1: try-finally 필수

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = None
    try:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_default_timeout(30000)  # 30초 타임아웃

        page.goto('http://localhost:3000')
        page.wait_for_load_state('networkidle')
        # ... 테스트 로직

    finally:
        if browser:
            browser.close()  # 반드시 실행
```

### 해결 패턴 2: Context Manager 활용

```python
from playwright.sync_api import sync_playwright
from contextlib import contextmanager

@contextmanager
def safe_browser(headless=True):
    """브라우저 자동 종료 보장"""
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=headless)
    try:
        yield browser
    finally:
        browser.close()
        p.stop()

# 사용
with safe_browser() as browser:
    page = browser.new_page()
    page.goto('http://localhost:3000')
    # ... 테스트 로직
# 자동 종료됨
```

### 해결 패턴 3: 타임아웃 설정

```python
# 전역 타임아웃 (페이지 레벨)
page.set_default_timeout(30000)       # 30초
page.set_default_navigation_timeout(60000)  # 네비게이션 60초

# 개별 타임아웃
page.wait_for_selector('#login', timeout=10000)
page.click('button', timeout=5000)
```

### 해결 패턴 4: 강제 종료 스크립트

```powershell
# Windows: 남은 브라우저 프로세스 정리
taskkill /F /IM "chromium.exe" 2>$null
taskkill /F /IM "chrome.exe" 2>$null
taskkill /F /IM "firefox.exe" 2>$null

# 또는 Playwright CLI
npx playwright install --force  # 재설치로 정리
```

## Docker 환경 테스트 흐름

```
1. Docker 서버 확인
   docker ps | grep -E "frontend|backend"
       ↓
2. 서버 미실행 시 시작
   docker-compose up -d
       ↓
3. 헬스체크 대기
   curl -s http://localhost:3000/health || sleep 5
       ↓
4. Playwright 테스트 (타임아웃 설정)
   npx playwright test --timeout=60000
       ↓
5. 브라우저 종료 확인
   tasklist | findstr "chromium"
```

## Playwright Config 권장 설정

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  timeout: 60000,           // 테스트당 60초
  expect: { timeout: 10000 }, // assertion 10초

  use: {
    headless: true,
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'retain-on-failure',

    // 타임아웃 설정
    actionTimeout: 15000,
    navigationTimeout: 30000,
  },

  // 병렬 실행 시 리소스 관리
  workers: 2,  // 동시 브라우저 수 제한

  // 재시도 정책
  retries: 1,

  // 리포터
  reporter: [
    ['html', { open: 'never' }],
    ['list'],
  ],
});
```

## 트러블슈팅

### 브라우저 미종료

```bash
# 1. 프로세스 확인
tasklist | findstr "chromium"

# 2. 강제 종료
taskkill /F /IM "chromium.exe"

# 3. Playwright 캐시 정리
npx playwright install --force
```

### Docker 서버 연결 실패

```bash
# 1. 컨테이너 상태 확인
docker ps -a

# 2. 로그 확인
docker logs frontend -f

# 3. 네트워크 확인
docker network ls
curl http://localhost:3000
```

### 타임아웃 오류

```python
# networkidle 대신 domcontentloaded 사용 (더 빠름)
page.wait_for_load_state('domcontentloaded')

# 특정 요소 대기
page.wait_for_selector('[data-testid="app-loaded"]')
```

## Anti-Patterns

| 금지 | 이유 | 대안 |
|------|------|------|
| `browser.close()` 누락 | 좀비 프로세스 | try-finally 필수 |
| 무한 타임아웃 | 테스트 행 | 명시적 타임아웃 설정 |
| `sleep()` 남용 | 불안정, 느림 | `wait_for_selector()` |
| headless=False (CI) | 리소스 낭비 | headless=True |

## 관련

- `/check` - 린트 + 테스트 실행
- `/parallel test` - 병렬 테스트
- `debugging-workflow` - 테스트 실패 시 디버깅