---
name: chrome-automation
description: Chrome browser automation skill for AI-controlled testing and interaction. Use when performing browser automation, E2E testing, form filling, or UI verification tasks. Includes test credentials and common operation patterns.
---

# Chrome Automation Skill

AI によるブラウザ自動操作のためのスキル。テスト環境でのログイン、フォーム入力、スクリーンショット取得などを行う際に参照する。

## When to Use

- ブラウザを使った E2E テストの実行
- フォーム入力の自動化（特にログインフォーム）
- UI の動作確認とスクリーンショット取得
- ページコンテンツの抽出と検証

## Test Environment Credentials

テスト環境で使用可能なアカウント情報:

| Field | Value |
|-------|-------|
| Email | `sample01@gmail.com` |
| Password | `test123` |
| Login Page | `/login` |

**Note**: このアカウントはテスト専用です。本番環境では使用しないでください。

## Common Operations

### 1. Navigation

```typescript
// URL に移動
await page.goto('http://localhost:3000/login');

// ページ読み込み完了を待機
await page.waitForLoadState('networkidle');
```

### 2. Element Selection (Priority Order)

セレクタの優先順位（推奨順）:

1. **data-testid** (最も推奨)
   ```typescript
   await page.locator('[data-testid="login-button"]').click();
   ```

2. **id 属性**
   ```typescript
   await page.locator('#email-input').fill('sample01@gmail.com');
   ```

3. **name 属性**
   ```typescript
   await page.locator('[name="password"]').fill('test123');
   ```

4. **class 属性** (最終手段)
   ```typescript
   await page.locator('.submit-btn').click();
   ```

### 3. Form Filling

```typescript
// テキスト入力
await page.locator('#email').fill('sample01@gmail.com');
await page.locator('#password').fill('test123');

// セレクトボックス
await page.locator('#role-select').selectOption('staff');

// チェックボックス
await page.locator('#remember-me').check();

// フォーム送信
await page.locator('[type="submit"]').click();
```

### 4. Login Flow (Complete Example)

```typescript
async function performLogin(page: Page) {
  // ログインページに移動
  await page.goto('http://localhost:3000/login');
  await page.waitForLoadState('networkidle');

  // ログイン済みかチェック
  const isLoggedIn = await page.locator('[data-testid="user-menu"]').isVisible();
  if (isLoggedIn) {
    console.log('Already logged in');
    return;
  }

  // ログインフォーム入力
  await page.locator('#email').fill('sample01@gmail.com');
  await page.locator('#password').fill('test123');
  await page.locator('[type="submit"]').click();

  // ログイン完了を待機
  await page.waitForURL('**/dashboard', { timeout: 10000 });
}
```

### 5. Taking Screenshots

```typescript
// ページ全体のスクリーンショット
await page.screenshot({ path: 'screenshot.png', fullPage: true });

// 特定要素のスクリーンショット
await page.locator('#main-content').screenshot({ path: 'content.png' });

// 特定ビューポートサイズで撮影
await page.setViewportSize({ width: 1280, height: 720 });
await page.screenshot({ path: 'desktop-view.png' });
```

### 6. Extracting Page Content

```typescript
// テキスト取得
const title = await page.locator('h1').textContent();

// 複数要素のテキスト取得
const items = await page.locator('.list-item').allTextContents();

// 属性値取得
const href = await page.locator('a.nav-link').getAttribute('href');

// HTML 取得
const html = await page.locator('#content').innerHTML();
```

### 7. Waiting Strategies

```typescript
// 要素が表示されるまで待機
await page.locator('[data-testid="result"]').waitFor({ state: 'visible' });

// 要素が非表示になるまで待機
await page.locator('.loading-spinner').waitFor({ state: 'hidden' });

// ネットワークが静止するまで待機
await page.waitForLoadState('networkidle');

// 特定の URL パターンまで待機
await page.waitForURL('**/success');

// カスタムタイムアウト
await page.locator('#async-content').waitFor({ timeout: 15000 });
```

## Best Practices

### DO (推奨)

- **必ずページ読み込み完了を待機してから操作する**
  ```typescript
  await page.goto(url);
  await page.waitForLoadState('networkidle');
  ```

- **data-testid を優先的に使用する**
  ```typescript
  await page.locator('[data-testid="submit-button"]').click();
  ```

- **ログイン状態を事前にチェックする**
  ```typescript
  const isLoggedIn = await page.locator('[data-testid="logout-button"]').isVisible();
  if (!isLoggedIn) {
    await performLogin(page);
  }
  ```

- **適切なタイムアウトを設定する**
  ```typescript
  await page.locator('#slow-content').waitFor({ timeout: 30000 });
  ```

- **エラー時にスクリーンショットを取得する**
  ```typescript
  try {
    await page.locator('#element').click();
  } catch (error) {
    await page.screenshot({ path: 'error-state.png' });
    throw error;
  }
  ```

### DON'T (非推奨)

- **固定の sleep/delay を使用しない**
  ```typescript
  // Bad
  await new Promise(r => setTimeout(r, 3000));

  // Good
  await page.locator('#element').waitFor({ state: 'visible' });
  ```

- **脆弱なセレクタを使用しない**
  ```typescript
  // Bad - 構造に依存
  await page.locator('div > div > button').click();

  // Good - 意図が明確
  await page.locator('[data-testid="save-button"]').click();
  ```

- **ハードコードされた認証情報を本番コードに含めない**
  ```typescript
  // Bad - 本番コードに直接記述
  const password = 'test123';

  // Good - 環境変数を使用
  const password = process.env.TEST_PASSWORD;
  ```

## Error Handling

### Element Not Found

```typescript
async function safeClick(page: Page, selector: string): Promise<boolean> {
  try {
    const element = page.locator(selector);
    const isVisible = await element.isVisible();

    if (!isVisible) {
      console.warn(`Element not visible: ${selector}`);
      return false;
    }

    await element.click();
    return true;
  } catch (error) {
    console.error(`Failed to click element: ${selector}`, error);
    await page.screenshot({ path: `error-${Date.now()}.png` });
    return false;
  }
}
```

### Timeout Handling

```typescript
async function waitWithRetry(
  page: Page,
  selector: string,
  maxRetries: number = 3
): Promise<boolean> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      await page.locator(selector).waitFor({ timeout: 5000 });
      return true;
    } catch {
      console.log(`Retry ${i + 1}/${maxRetries} for: ${selector}`);
      await page.reload();
    }
  }
  return false;
}
```

## Selector Strategy Guide

| Scenario | Recommended Selector | Example |
|----------|---------------------|---------|
| ボタン・インタラクティブ要素 | `data-testid` | `[data-testid="submit-btn"]` |
| フォーム入力 | `id` or `name` | `#email`, `[name="password"]` |
| リスト内の特定項目 | `data-testid` + index | `[data-testid="item-0"]` |
| 動的コンテンツ | テキスト内容 | `text=Loading...` |
| アクセシビリティ | role + name | `role=button[name="Save"]` |

## Checklist Before Running Automation

- [ ] テスト環境の URL が正しいか確認
- [ ] 認証情報が有効か確認
- [ ] ネットワーク状態が安定しているか確認
- [ ] 必要な要素に `data-testid` が付与されているか確認
- [ ] タイムアウト設定が適切か確認
- [ ] エラー時のスクリーンショット保存パスが設定されているか確認
