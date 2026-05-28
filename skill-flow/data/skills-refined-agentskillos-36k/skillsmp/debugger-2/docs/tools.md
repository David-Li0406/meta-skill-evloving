# デバッグツール一覧

レイヤー別の推奨デバッグツールと使用方法。

## レイヤー別ツール

### lib層のデバッグツール

| ツール | 用途 | 使用方法 |
| :--- | :--- | :--- |
| **Vitest debugger** | ユニットテストのデバッグ | `npm run test:ui` でUIモード起動 |
| **console.log** | 戦略的なログ出力 | 計算途中の値を確認 |
| **tsc --noEmit** | 型チェック | `npm run typecheck` で実行 |
| **TypeScript Playground** | 型推論の確認 | <https://www.typescriptlang.org/play> |

#### Vitest UIモード

```bash
# UIモードでテストを実行
npm run test:ui

# または scripts/ を使用
.claude/skills/debugger/scripts/run-test-debug.sh
```

**機能**:
- テストの実行/停止
- ブレークポイント
- 変数のインスペクション
- カバレッジ表示

#### console.log の戦略的配置

```typescript
export function progressCalculator(completed: number, total: number): number {
  console.log('Input:', { completed, total }); // 入力確認

  if (total === 0) {
    console.log('Guard: total is 0, returning 0'); // ガード節
    return 0;
  }

  const progress = (completed / total) * 100;
  console.log('Progress:', progress); // 計算結果

  return Math.min(progress, 100);
}
```

---

### data-io層のデバッグツール

| ツール | 用途 | 使用方法 |
| :--- | :--- | :--- |
| **Network tab（DevTools）** | ネットワークリクエストの確認 | ブラウザのDevToolsで確認 |
| **Playwright trace viewer** | E2Eテストのトレース確認 | `npx playwright show-trace trace.zip` |
| **モックサーバーログ** | API応答の確認 | MSW等のログ確認 |
| **curl/httpie** | API直接確認 | コマンドラインでAPI確認 |

#### Network tabの使用

**確認項目**:
- リクエストURL
- リクエストヘッダー
- リクエストボディ
- レスポンスステータス
- レスポンスボディ
- タイミング

#### Playwright trace viewer

```bash
# トレース有効化でテスト実行
npx playwright test --trace on

# トレース表示
npx playwright show-trace trace.zip
```

**機能**:
- ネットワークリクエストの確認
- コンソールログの確認
- スクリーンショット
- DOMスナップショット

#### API直接確認

```bash
# curlで確認
curl -X GET https://api.example.com/users/123

# httpieで確認（見やすい）
http GET https://api.example.com/users/123
```

---

### ui層のデバッグツール

| ツール | 用途 | 使用方法 |
| :--- | :--- | :--- |
| **React DevTools** | コンポーネント状態の確認 | ブラウザ拡張機能 |
| **Playwright debugger** | E2Eテストのデバッグ | `npm run test:e2e:debug` |
| **Lighthouse** | パフォーマンス測定 | DevToolsまたはCLI |
| **React Profiler** | レンダリング最適化 | React DevTools内 |

#### React DevTools

**機能**:
- コンポーネントツリーの確認
- Props/Stateの確認
- Hookの値の確認
- コンポーネントの更新原因の追跡

**使用方法**:
1. ブラウザ拡張機能をインストール
2. DevToolsの「Components」タブを開く
3. コンポーネントを選択して状態確認

#### Playwright debugger

```bash
# デバッグモードでE2Eテスト実行
npm run test:e2e:debug

# または scripts/ を使用
.claude/skills/debugger/scripts/run-e2e-debug.sh
```

**機能**:
- ステップ実行
- ブレークポイント
- セレクタの確認
- スクリーンショット

#### Lighthouse

```bash
# CLIで実行
npx lighthouse http://localhost:3000 --view

# DevToolsで実行
# DevTools > Lighthouse タブ > Generate report
```

**測定項目**:
- Performance
- Accessibility
- Best Practices
- SEO

---

## デバッグコマンド

### ユニットテスト

```bash
# 通常実行
npm test

# UIモードで実行
npm run test:ui

# カバレッジ付き
npm run test:coverage

# 特定のファイルのみ
npm test progressCalculator
```

### E2Eテスト

```bash
# 通常実行
npm run test:e2e

# デバッグモード
npm run test:e2e:debug

# ヘッドレスモード無効化
npm run test:e2e:headed

# 特定のテストのみ
npm run test:e2e -- dashboard.spec.ts
```

### 型チェック

```bash
# 型チェック実行
npm run typecheck

# または scripts/ を使用
.claude/skills/debugger/scripts/run-typecheck.sh

# 詳細表示
npm run typecheck -- --pretty
```

### リント

```bash
# すべてのリント実行
npm run lint:all

# ESLintのみ
npm run lint

# Markdownのみ
npm run lint:md
```

### ビルド

```bash
# ビルド実行
npm run build

# クリーンビルド
npm run clean && npm run build

# 型チェック付きビルド
npm run typecheck && npm run build
```

---

## デバッグのベストプラクティス

### console.logの効果的な使用

#### ✅ 良い例

```typescript
// 構造化されたログ
console.log('User data:', { id, name, email });

// タイムスタンプ付き
console.log(`[${new Date().toISOString()}] Processing user:`, userId);

// 条件付きログ
if (process.env.NODE_ENV === 'development') {
  console.log('Debug:', debugInfo);
}
```

#### ❌ 悪い例

```typescript
// 情報が少ない
console.log('here');

// ログが多すぎる
console.log(data);
console.log(data.user);
console.log(data.user.name);
```

### デバッガーのブレークポイント

#### VSCode

```typescript
// デバッガー設定（.vscode/launch.json）
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Vitest",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "test:ui"],
      "console": "integratedTerminal"
    }
  ]
}
```

#### ブラウザ

```typescript
// コード内でブレークポイント
function progressCalculator(completed: number, total: number): number {
  debugger; // ← ここで停止

  if (total === 0) {
    return 0;
  }

  return (completed / total) * 100;
}
```

### パフォーマンス計測

```typescript
// 実行時間計測
console.time('progressCalculator');
const result = progressCalculator(completed, total);
console.timeEnd('progressCalculator');

// メモリ使用量
console.log('Memory:', process.memoryUsage());
```

---

## トラブルシューティング

### よくある問題と解決方法

#### テストがタイムアウトする

**原因**: 非同期処理の待機不足

**解決**:
```typescript
// タイムアウト延長
test('async operation', async () => {
  // ...
}, 10000); // 10秒に延長
```

#### E2Eテストが不安定

**原因**: 要素の読み込み待機不足

**解決**:
```typescript
// 明示的な待機
await page.waitForSelector('[data-testid="element"]');
await page.click('[data-testid="element"]');
```

#### 型エラーが解決しない

**原因**: 型定義キャッシュの問題

**解決**:
```bash
# TypeScriptキャッシュクリア
rm -rf node_modules/.cache
npm run typecheck
```

#### ビルドが遅い

**原因**: キャッシュの破損

**解決**:
```bash
# クリーンビルド
npm run clean
npm run build
```

---

## 参照

- `docs/strategies.md` - レイヤー別デバッグ戦略
- `prompts/01-diagnose.md` - エラー診断の手順
- `scripts/run-test-debug.sh` - テストデバッグスクリプト
- `scripts/run-e2e-debug.sh` - E2Eデバッグスクリプト
- `scripts/run-typecheck.sh` - 型チェックスクリプト
