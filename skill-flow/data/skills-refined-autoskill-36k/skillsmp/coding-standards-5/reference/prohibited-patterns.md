# 禁止事項

## 絶対に使用禁止

### 1. any型の使用

```typescript
// ❌ 絶対禁止
const data: any = response;
function process(input: any): any { }
```

**理由:**
- TypeScriptの型チェック機能を完全に無効化
- ランタイムエラーの主要な原因
- IDEの補完・リファクタリング機能が働かない
- コードの可読性・保守性が著しく低下

**代替策:**
- `unknown`型を使用し、型ガードで絞り込む
- 適切なinterface/typeを定義する
- Generic型を活用する

### 2. eval()関数の使用

```typescript
// ❌ セキュリティリスクのため禁止
eval(userInput);
```

**理由:**
- XSS攻撃の主要な原因
- コードインジェクションのリスク
- パフォーマンスへの悪影響
- デバッグが困難

### 3. console.log の本番環境への残留

```typescript
// ❌ 本番環境では禁止（開発時は可）
console.log('debug info');
```

**理由:**
- パフォーマンスへの影響
- 機密情報の漏洩リスク
- ログの乱雑化

**対策:**
- 開発時のみ使用し、コミット前に削除
- 必要な場合はロギングライブラリを使用

### 4. var キーワードの使用

```typescript
// ❌ letまたはconstを使用
var userName = 'john';

// ✅ 推奨
const userName = 'john';
let counter = 0;
```

**理由:**
- 関数スコープによる予期しない動作
- ホイスティングによるバグ
- `let`/`const`はブロックスコープで安全

### 5. == 比較演算子の使用

```typescript
// ❌ 型強制が発生するため禁止
if (value == null) { }

// ✅ 厳密等価演算子を使用
if (value === null) { }
if (value == null) { } // nullとundefinedの両方をチェックする場合のみ例外
```

**理由:**
- 暗黙の型変換による予期しない動作
- デバッグが困難
- TypeScriptの型安全性を損なう

**唯一の例外:**
- `value == null` は `value === null || value === undefined` と等価で、これのみ許容

## 推奨されない書き方

### ネストの深い条件分岐

```typescript
// ❌ 避ける
if (condition1) {
  if (condition2) {
    if (condition3) {
      // 処理
    }
  }
}

// ✅ 早期リターンを使用
if (!condition1) return;
if (!condition2) return;
if (!condition3) return;
// 処理
```

### マジックナンバー

```typescript
// ❌ 避ける
if (user.age >= 18) { }
setTimeout(callback, 3000);

// ✅ 定数を定義
const LEGAL_AGE = 18;
const ANIMATION_DELAY_MS = 3000;

if (user.age >= LEGAL_AGE) { }
setTimeout(callback, ANIMATION_DELAY_MS);
```

### 命名付きエクスポートとデフォルトエクスポートの混在

```typescript
// ❌ 避ける
export function Button() { }
export default Button;

// ✅ どちらか一方を使用
export function Button() { }
// または
export default function Button() { }
```

## セキュリティ関連の禁止事項

### 機密情報のハードコーディング

```typescript
// ❌ 絶対禁止
const API_KEY = 'sk-1234567890abcdef';
const PASSWORD = 'secret123';

// ✅ 環境変数を使用
const API_KEY = process.env.API_KEY;
```

### ユーザー入力の直接利用

```typescript
// ❌ SQLインジェクションのリスク
const query = `SELECT * FROM users WHERE id = '${userId}'`;

// ✅ パラメータ化クエリを使用
const query = 'SELECT * FROM users WHERE id = $1';
await db.query(query, [userId]);
```

### 未検証データの表示

```typescript
// ❌ XSSのリスク
element.innerHTML = userInput;

// ✅ サニタイズまたはテキストとして扱う
element.textContent = userInput;
```
