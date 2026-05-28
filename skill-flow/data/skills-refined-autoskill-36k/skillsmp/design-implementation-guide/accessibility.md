# アクセシビリティ実装

## コントラスト比

### 基準

| 要素 | 最小比率 | 根拠 |
|-----|---------|------|
| 本文テキスト | 4.5:1 | WCAG AA |
| 大きなテキスト（18pt+） | 3:1 | WCAG AA |
| 太字テキスト（14pt+太字） | 3:1 | WCAG AA |
| UIコンポーネント境界 | 3:1 | WCAG 2.2 |

### 検証方法

1. [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)で確認
2. 背景色変更時は必ず再検証
3. 状態色（success/warning/error/info）は各トーンで同一比率を確保

### 自動テスト

```js
// axe-coreをCIパイプラインに追加
await axe.run({ rules: { 'color-contrast': { enabled: true } } });
```

## キーボード操作

### ネイティブ要素を優先

```html
<!-- Good -->
<button type="submit">送信</button>

<!-- Bad: カスタム要素は最小限に -->
<div role="button" tabindex="0" onclick="...">送信</div>
```

### カスタム要素の要件

- `tabindex="0"` でフォーカス可能に
- `role` 属性でセマンティクスを付与
- Enter/Space キーで動作を実装
- WAI-ARIA APGパターンに準拠

### キーボードパターン

| キー | 動作 |
|-----|------|
| Tab / Shift+Tab | 要素間移動 |
| Enter / Space | 決定 |
| Escape | キャンセル/閉じる |
| 矢印キー | リスト内移動（roving tabindex） |

### ダイアログ例

```js
dialog.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    dialog.close();
    triggerButton.focus();
  }
});
```

## 状態の伝達

### 視覚とARIA両方で伝達

```html
<button aria-disabled="true" disabled class="btn-disabled">
  <span aria-hidden="true">🚫</span> 送信不可
</button>
```

```css
.btn-disabled {
  background: var(--color-surface-variant);
  color: var(--color-on-surface-variant);
  opacity: 0.38; /* Material 3規定 */
}
```

### フォーカス表示

```css
button:focus-visible {
  outline: 3px solid var(--color-primary);
  outline-offset: 2px;
}
```

**色だけで状態を示すな** - アイコン・テキスト・ボーダー太さを併用

## タッチターゲット

### 最小サイズ

| プラットフォーム | 最小サイズ |
|----------------|-----------|
| iOS/Android | 44×44px (44dp/pt) |
| Web (デスクトップ) | 24×24px |

### 実装

```css
button {
  min-block-size: 44px;
  min-inline-size: 44px;
  padding: 0;
}

/* タッチ領域拡張 */
button::before {
  content: '';
  position: absolute;
  inset: -8px;
}
```

## エラー処理

### エラー要約（ページ上部）

```html
<div id="error-summary" role="alert" tabindex="-1" hidden>
  <h2>以下の問題を修正してください</h2>
  <ul>
    <li><a href="#email">メールアドレスに@を含めてください</a></li>
    <li><a href="#password">パスワードは8文字以上必要です</a></li>
  </ul>
</div>
```

### 送信失敗時の処理

```js
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const errors = validateForm(form);

  if (errors.length > 0) {
    const summary = document.getElementById('error-summary');
    summary.hidden = false;
    summary.focus(); // フォーカス移動

    errors.forEach(err => showError(err.field, err.message));
  }
});
```

### 個別エラーの紐付け

```html
<label for="password">パスワード</label>
<input id="password" type="password"
       aria-describedby="password-hint password-error"
       aria-invalid="true">
<span id="password-hint">8文字以上、数字を含む</span>
<span id="password-error" role="alert" class="error-text">
  パスワードは8文字以上必要です
</span>
```

### エラーメッセージの原則

❌ 「入力エラー」「無効な入力」
✅ 「メールアドレスに@を含めてください（例: user@example.com）」

テンプレート: **[何が問題か] + [どうすればよいか]**

## バリデーション通知

### 同期検証（リアルタイム）

```html
<label for="username">ユーザー名
  <span aria-live="polite" id="username-hint">
    残り<span id="char-count">20</span>文字
  </span>
</label>
<input id="username" maxlength="20" aria-describedby="username-hint">
```

```js
input.addEventListener('input', (e) => {
  const remaining = 20 - e.target.value.length;
  document.getElementById('char-count').textContent = remaining;
});
```

### 非同期検証（API応答）

```html
<input id="email" type="email" aria-describedby="email-status">
<div id="email-status" role="status"></div>
```

```js
async function checkEmailAvailability(email) {
  const response = await fetch(`/api/check-email?email=${email}`);
  const data = await response.json();
  const status = document.getElementById('email-status');

  if (data.available) {
    status.textContent = '✓ 利用可能';
    status.className = 'success';
  } else {
    status.textContent = '✗ すでに登録済み';
    status.className = 'error';
  }
}

input.addEventListener('blur', (e) => {
  if (e.target.validity.valid) {
    checkEmailAvailability(e.target.value);
  }
});
```

### aria-invalidの更新

```js
function showError(input, message) {
  input.setAttribute('aria-invalid', 'true');
  const errorId = input.id + '-error';
  input.setAttribute('aria-describedby', errorId);

  const errorSpan = document.getElementById(errorId);
  errorSpan.textContent = message;
  errorSpan.style.display = 'block';
}
```

## よくある落とし穴

1. **aria-labelだけで状態を伝え、視覚変化を欠く**
   - 色覚異常やロービジョンユーザーが見落とす

2. **カスタムコンポーネントにキーボード操作を実装し忘れ**
   - `<div onclick="...">` だけではTabで到達不可

3. **エラーメッセージが曖昧**
   - 「入力エラー」だけでは何をすべきか不明

4. **非同期検証の結果をaria-liveで通知しない**
   - スクリーンリーダーが変化を検出できない

## 参考

- [WCAG 2.2 SC 1.4.3 - コントラスト](https://www.w3.org/WAI/WCAG22/quickref/#contrast-minimum)
- [WCAG 2.2 SC 2.1.1 - キーボード](https://www.w3.org/WAI/WCAG22/quickref/#keyboard)
- [WCAG 2.2 SC 1.4.1 - 色の使用](https://www.w3.org/WAI/WCAG22/quickref/#use-of-color)
- [WAI-ARIA APG](https://www.w3.org/WAI/ARIA/apg/)
- [GOV.UK Error Summary](https://design-system.service.gov.uk/components/error-summary/)
- [GOV.UK Error Message](https://design-system.service.gov.uk/components/error-message/)
- [Inclusive Components](https://inclusive-components.design/)
