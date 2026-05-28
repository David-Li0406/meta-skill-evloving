# 実装例

## 完全なフォーム実装

### HTML

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>実装サンプル</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="container">
    <!-- エラー要約 -->
    <div id="error-summary" role="alert" tabindex="-1" hidden>
      <h2>以下の問題を修正してください</h2>
      <ul id="error-list"></ul>
    </div>

    <form id="sample-form" novalidate>
      <div class="form-group">
        <label for="email">メールアドレス</label>
        <input
          type="email"
          id="email"
          name="email"
          required
          aria-describedby="email-error"
          aria-invalid="false">
        <span id="email-error" class="error-text" role="alert"></span>
      </div>

      <button type="submit" class="btn-primary">送信</button>
    </form>
  </div>

  <script src="script.js"></script>
</body>
</html>
```

### CSS（tokens.css生成後）

```css
/* Style Dictionaryで生成されたトークン */
:root {
  --color-primary: #6750A4;
  --color-on-primary: #FFFFFF;
  --color-error: #BA1A1A;
  --color-on-error: #FFFFFF;
  --color-surface: #FEF7FF;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --typography-body-size: clamp(1rem, 0.875rem + 0.5vw, 1.125rem);
  --typography-body-line-height: 1.5;
}

* {
  box-sizing: border-box;
}

body {
  font-size: var(--typography-body-size);
  line-height: var(--typography-body-line-height);
  background: var(--color-surface);
  margin: 0;
  padding: var(--spacing-md);
}

.container {
  max-inline-size: 600px;
  margin-inline: auto;
}

/* エラー要約 */
#error-summary {
  background: var(--color-error);
  color: var(--color-on-error);
  padding: var(--spacing-md);
  margin-block-end: var(--spacing-md);
  border-inline-start: 4px solid currentColor;
}

#error-summary:focus {
  outline: 3px solid var(--color-primary);
  outline-offset: 2px;
}

#error-summary ul {
  margin: 0;
  padding-inline-start: var(--spacing-md);
}

#error-summary a {
  color: var(--color-on-error);
  text-decoration: underline;
}

/* フォーム */
.form-group {
  margin-block-end: var(--spacing-md);
}

label {
  display: block;
  margin-block-end: var(--spacing-sm);
  font-weight: 600;
}

input {
  inline-size: 100%;
  padding-block: var(--spacing-sm);
  padding-inline: var(--spacing-sm);
  font-size: inherit;
  border: 2px solid currentColor;
  border-radius: 4px;
}

input:focus-visible {
  outline: 3px solid var(--color-primary);
  outline-offset: 2px;
}

input[aria-invalid="true"] {
  border-color: var(--color-error);
}

.error-text {
  display: none;
  color: var(--color-error);
  margin-block-start: var(--spacing-sm);
  font-size: 0.875rem;
}

.error-text:not(:empty) {
  display: block;
}

/* ボタン */
.btn-primary {
  background: var(--color-primary);
  color: var(--color-on-primary);
  border: none;
  padding-block: 12px;
  padding-inline: var(--spacing-md);
  min-block-size: 44px;
  min-inline-size: 44px;
  font-size: inherit;
  font-weight: 600;
  cursor: pointer;
  border-radius: 4px;
  position: relative;
}

.btn-primary:hover::before {
  content: '';
  position: absolute;
  inset: 0;
  background: var(--color-on-primary);
  opacity: 0.08;
  border-radius: inherit;
}

.btn-primary:focus-visible {
  outline: 3px solid var(--color-primary);
  outline-offset: 2px;
}

.btn-primary:active::before {
  opacity: 0.12;
}
```

### JavaScript

```js
const form = document.getElementById('sample-form');
const emailInput = document.getElementById('email');
const errorSummary = document.getElementById('error-summary');
const errorList = document.getElementById('error-list');

form.addEventListener('submit', (e) => {
  e.preventDefault();

  // エラーをリセット
  clearErrors();

  // バリデーション
  const errors = [];

  if (!emailInput.value) {
    errors.push({
      field: emailInput,
      message: 'メールアドレスを入力してください'
    });
  } else if (!emailInput.validity.valid) {
    errors.push({
      field: emailInput,
      message: 'メールアドレスに@を含めてください（例: user@example.com）'
    });
  }

  if (errors.length > 0) {
    showErrors(errors);
  } else {
    alert('送信成功！');
  }
});

function showErrors(errors) {
  // エラー要約を表示
  errorSummary.hidden = false;
  errorList.innerHTML = '';

  errors.forEach(error => {
    const { field, message } = error;

    // 要約にリンクを追加
    const li = document.createElement('li');
    const link = document.createElement('a');
    link.href = `#${field.id}`;
    link.textContent = message;
    link.addEventListener('click', (e) => {
      e.preventDefault();
      field.focus();
    });
    li.appendChild(link);
    errorList.appendChild(li);

    // 個別フィールドにエラー表示
    field.setAttribute('aria-invalid', 'true');
    const errorSpan = document.getElementById(`${field.id}-error`);
    errorSpan.textContent = message;
  });

  // エラー要約へフォーカス移動
  errorSummary.focus();
}

function clearErrors() {
  errorSummary.hidden = true;
  errorList.innerHTML = '';

  document.querySelectorAll('[aria-invalid="true"]').forEach(field => {
    field.setAttribute('aria-invalid', 'false');
  });

  document.querySelectorAll('.error-text').forEach(span => {
    span.textContent = '';
  });
}
```

## レスポンシブ実装

### 流体スケールでブレークポイント不要化

```css
:root {
  --space-s: clamp(0.5rem, 0.25rem + 1vw, 1rem);
  --space-m: clamp(1rem, 0.5rem + 2vw, 2rem);
  --space-l: clamp(2rem, 1rem + 4vw, 4rem);
}

.container {
  padding-inline: var(--space-m);
  gap: var(--space-s);
}
```

### コンテナクエリ

```css
.card-container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card {
    grid-template-columns: 1fr 1fr;
  }
}
```

### RTL対応

```css
/* 物理方向（非推奨） */
margin-left: 1rem; /* RTLで反転しない */

/* 論理プロパティ（推奨） */
margin-inline-start: 1rem; /* RTLで自動反転 */
```

### 縦書き対応

```css
.vertical-text {
  writing-mode: vertical-rl;
  text-orientation: upright;
}
```

## アクセシブルなボタン実装

```html
<button type="button" class="icon-button" title="メニューを開く">
  <span class="icon" aria-hidden="true">☰</span>
  <span class="visually-hidden">メニューを開く</span>
</button>
```

```css
.icon-button {
  min-block-size: 44px;
  min-inline-size: 44px;
  position: relative;
}

/* タッチ領域拡張 */
.icon-button::before {
  content: '';
  position: absolute;
  inset: -8px;
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}
```

## 非同期検証の実装

```html
<div class="form-group">
  <label for="username">ユーザー名</label>
  <input
    id="username"
    type="text"
    aria-describedby="username-status"
  >
  <div id="username-status" role="status" class="status"></div>
</div>
```

```js
const usernameInput = document.getElementById('username');
const usernameStatus = document.getElementById('username-status');

let debounceTimer;

usernameInput.addEventListener('input', (e) => {
  clearTimeout(debounceTimer);

  if (e.target.value.length < 3) {
    usernameStatus.textContent = '';
    return;
  }

  debounceTimer = setTimeout(async () => {
    usernameStatus.textContent = '確認中...';

    try {
      const response = await fetch(`/api/check-username?name=${e.target.value}`);
      const data = await response.json();

      if (data.available) {
        usernameStatus.textContent = '✓ 利用可能';
        usernameStatus.className = 'status success';
      } else {
        usernameStatus.textContent = '✗ すでに使用されています';
        usernameStatus.className = 'status error';
      }
    } catch (error) {
      usernameStatus.textContent = '確認できませんでした';
      usernameStatus.className = 'status error';
    }
  }, 500);
});
```

## チェックリスト

### 実装前

- [ ] トークン定義を確認
- [ ] コントラスト比を検証
- [ ] キーボード操作を設計

### 実装中

- [ ] 論理プロパティを使用
- [ ] ネイティブ要素を優先
- [ ] ARIAを適切に付与

### 実装後

- [ ] Tab操作で全要素に到達可能
- [ ] エラー時にフォーカス移動
- [ ] スクリーンリーダーで検証
