# Frontend Health Checker

> Kiểm tra sức khỏe frontend tự động using Puppeteer

## Cài đặt nhanh

```bash
cd frontend
npm install puppeteer
```

## Cách sử dụng

### 1. Tạo health check script

```javascript
const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    headless: "new",
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();

  // Capture console errors
  page.on('console', msg => {
    if (msg.type() === 'error') {
      console.log('Console Error:', msg.text());
    }
  });

  // Navigate and check
  await page.goto('http://localhost:3000');
  // ... more checks

  await browser.close();
})();
```

### 2. Chạy script

```bash
BASE_URL=http://localhost:3000 node health_check.js
```

## Trigger phrases

- "check frontend for errors"
- "kiểm tra console errors"
- "test all pages for broken links"
- "frontend health check"
- "audit frontend stability"

## Output format

```
=== FRONTEND HEALTH CHECK REPORT ===

Total pages checked: 10
Failed pages: 0
Pages with console errors: 2
Pages with network errors: 1

--- /dashboard (http://localhost:3000/dashboard) ---
Status: success
Console Errors (1):
  - Warning: Text content did not match
Network Errors (1):
  - GET /api/v1/stats [401]
```

## Pages được check

| Type | Pages |
|------|-------|
| Public | `/`, `/login`, `/register`, `/blog` |
| Protected | `/dashboard`, `/dashboard/stats`, `/dashboard/posts`, `/dashboard/users-manager`, `/dashboard/settings`, `/user/profile` |

## Xem thêm

- [SKILL.md](SKILL.md) - Tài liệu chi tiết
- [examples.js](examples.js) - Ví dụ scripts
