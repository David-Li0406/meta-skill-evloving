# 修正案生成プロンプト

## AI役割定義

あなたは修正案生成の専門家です。
根本原因に基づき、複数の修正アプローチを提案し、テスト戦略を含めてください。

## 前提条件

**02-analyze.mdで特定した以下の情報を使用**:

- 直接原因
- 根本原因
- 影響レイヤー
- 再発防止策

## 思考プロセス（CoT）

以下の順序で段階的に修正案を生成してください：

```text
Step 1: 修正の優先度を決定
  → immediate / scheduled / backlog

Step 2: 推奨アプローチを考案
  → 最もシンプルで効果的な方法は？

Step 3: 代替アプローチを考案
  → 他にどんな方法があるか？（最低1つ）

Step 4: 各アプローチのPros/Consを評価
  → メリット・デメリットは何か？

Step 5: 修正コード例を作成
  → Before/Afterのコードを示す

Step 6: テスト戦略を策定
  → どのテストを追加・修正すべきか？

Step 7: Next Actionsを明確化
  → 具体的な作業順序を提示
```

## 実行手順

### 1. 修正の優先度決定

| 優先度 | 判定基準 | 対応時期 |
| :--- | :--- | :--- |
| **immediate** | P0 (Critical)、ブロッカー | 即座 |
| **scheduled** | P1 (Error)、通常バグ | 当日〜翌日 |
| **backlog** | P2 (Warning)、改善 | 計画的に |

### 2. 修正アプローチの考案

**最低2つのアプローチを提案**:

1. **推奨アプローチ（Approach A）**: 最もシンプルで効果的
2. **代替アプローチ（Approach B以降）**: 別の選択肢

各アプローチに以下を含める：

- **説明**: 何をするか
- **Pros**: メリット
- **Cons**: デメリット
- **コード例**: Before/After
- **作業時間**: 見積もり

### 3. レイヤー別の修正パターン

#### lib層の修正

**よくある修正パターン**:

| パターン | 説明 | 例 |
| :--- | :--- | :--- |
| **ガード節追加** | エッジケースの処理 | `if (total === 0) return 0;` |
| **型定義の厳密化** | any型の排除 | `string \| undefined` → `string` |
| **バリデーション追加** | 入力値の検証 | `if (!isValid(input)) throw new Error()` |
| **エラーハンドリング** | 例外処理 | `try-catch`の追加 |

#### data-io層の修正

**よくある修正パターン**:

| パターン | 説明 | 例 |
| :--- | :--- | :--- |
| **エラーハンドリング強化** | fetch のエラー処理 | `try-catch`、リトライロジック |
| **型安全性向上** | レスポンス型の検証 | Zodによるバリデーション |
| **タイムアウト追加** | 長時間待機の防止 | `AbortController`使用 |
| **ログ追加** | デバッグ情報の記録 | `console.error`、構造化ログ |

#### ui層の修正

**よくある修正パターン**:

| パターン | 説明 | 例 |
| :--- | :--- | :--- |
| **loader/action修正** | データ取得・更新の最適化 | `loader`での事前取得 |
| **エラーバウンダリ追加** | UIレベルのエラー処理 | ErrorBoundary コンポーネント |
| **状態管理の簡素化** | 不要な状態の削除 | Remixのloader/actionを活用 |
| **条件付きレンダリング** | データの有無に応じた表示 | `{data ? <Component /> : <Fallback />}` |

### 4. テスト戦略の策定

修正に応じたテスト戦略を提案：

#### 追加すべきテストケース

- **エッジケース**: 境界値、null、空配列等
- **失敗シナリオ**: エラーハンドリングの検証
- **統合テスト**: 層間の連携確認

#### テスト例

```typescript
describe('{function-name} edge cases', () => {
  it('should handle {edge-case-1}', () => {
    expect({function-name}({input})).toBe({expected});
  });

  it('should throw error for {invalid-input}', () => {
    expect(() => {function-name}({invalid-input})).toThrow();
  });

  it('should handle {edge-case-2}', () => {
    expect({function-name}({input})).toBe({expected});
  });
});
```

### 5. Next Actionsの明確化

具体的な作業順序を提示：

```text
1. ✅ {action1}（{estimated-time}）
2. ✅ {action2}（{estimated-time}）
3. ✅ {action3}（{estimated-time}）
4. 📝 {documentation-update}（{estimated-time}）

総作業時間: 約{total-time}
```

## 完了条件チェックリスト

- [ ] 修正の優先度を決定した
- [ ] 最低2つのアプローチを提案した
- [ ] 各アプローチにPros/Consを記載した
- [ ] Before/Afterのコード例を示した
- [ ] テスト戦略を策定した
- [ ] Next Actionsを明確化した

## Output形式

```markdown
## 修正案

### 優先度

**Priority**: {immediate / scheduled / backlog}
**作業時間**: 約{total-time}
**Breaking Change**: {Yes / No}

---

### 推奨アプローチ（Approach A）

#### 説明

{what-to-do}

#### 修正コード

**Before**:

```typescript
// 問題のコード
{before-code}
```

**After**:

```typescript
// 修正後
{after-code}
```

#### Pros

- ✅ {pro1}
- ✅ {pro2}
- ✅ {pro3}

#### Cons

- {con1}（該当する場合）

#### 作業時間

約{estimated-time}

---

### 代替アプローチ（Approach B）

#### 説明

{alternative-approach}

#### 修正コード

**Before**:

```typescript
{before-code}
```

**After**:

```typescript
{after-code}
```

#### Pros

- ✅ {pro1}
- ✅ {pro2}

#### Cons

- ⚠️ {con1}
- ⚠️ {con2}

#### 作業時間

約{estimated-time}

---

## テスト戦略

### 追加すべきテストケース

```typescript
describe('{test-suite-name}', () => {
  it('{test-case-1}', () => {
    // {test-code-1}
  });

  it('{test-case-2}', () => {
    // {test-code-2}
  });

  it('{test-case-3}', () => {
    // {test-code-3}
  });
});
```

### E2Eテストの修正（該当する場合）

```typescript
// {e2e-test-modification}
```

---

## Next Actions

1. ✅ **Approach Aで修正**（{time1}）
2. ✅ **エッジケーステストを追加**（{time2}）
3. ✅ **テスト実行して確認**（{time3}）
   ```bash
   npm run typecheck
   npm test
   ```
4. 📝 **{documentation-update}**（{time4}）

**総作業時間**: 約{total-time}

---

## 再発防止策

### 短期的対策

- {immediate-prevention1}
- {immediate-prevention2}

### 中期的対策

- {medium-prevention1}
- {medium-prevention2}

### 長期的対策

- {long-prevention1}
- {long-prevention2}

---

## 関連情報

**影響を受けるファイル**:
- {file1}
- {file2}

**関連ドキュメント**:
- {doc1}
- {doc2}

**関連エージェント**:
- @CodeReviewer（修正後のレビュー）
- @GeneratorMaintainer（テンプレート修正が必要な場合）
```

## 修正案の品質基準

### ✅ 良い修正案

- **シンプル**: 最小限の変更で問題を解決
- **テスト可能**: テストで検証できる
- **保守性**: 将来の変更に強い
- **アーキテクチャ準拠**: 3大層アーキテクチャに沿っている

### ❌ 悪い修正案

- **複雑**: 不要な変更が含まれる
- **テスト不可**: 検証方法が不明
- **技術的負債**: 将来の問題を引き起こす
- **アーキテクチャ違反**: 層の責務を超えている

## アプローチ選択のガイドライン

### 推奨アプローチ（Approach A）の条件

- ✅ シンプルで理解しやすい
- ✅ 既存コードへの影響が最小
- ✅ パフォーマンスへの影響がない
- ✅ テストが容易

### 代替アプローチが優れる場合

- 将来の拡張性が重要
- パフォーマンスが重要
- 一貫性を保つため（既存パターンに合わせる）

## 修正例

### 例1: lib層のエッジケース対応

**Before**:

```typescript
export function progressCalculator(completed: number, total: number): number {
  const progress = (completed / total) * 100;
  return Math.min(progress, 100);
}
```

**After（Approach A - ガード節）**:

```typescript
export function progressCalculator(completed: number, total: number): number {
  // ガード節: total が 0 の場合は 0% を返す
  if (total === 0) {
    return 0;
  }

  const progress = (completed / total) * 100;
  return Math.min(progress, 100);
}
```

**Pros**: シンプル、読みやすい、影響最小

**After（Approach B - Math.max）**:

```typescript
export function progressCalculator(completed: number, total: number): number {
  const progress = (completed / Math.max(total, 1)) * 100;
  return Math.min(progress, 100);
}
```

**Pros**: ガード節不要
**Cons**: total = 0 の意味が不明確

### 例2: data-io層のエラーハンドリング

**Before**:

```typescript
export async function getUser(id: string) {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}
```

**After（Approach A - try-catch）**:

```typescript
export async function getUser(id: string) {
  try {
    const response = await fetch(`/api/users/${id}`);

    if (!response.ok) {
      throw new Error(`Failed to fetch user: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching user:', error);
    throw error;
  }
}
```

**Pros**: エラーハンドリング、ログ記録

**After（Approach B - レスポンス検証）**:

```typescript
import { z } from 'zod';

const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
});

export async function getUser(id: string) {
  try {
    const response = await fetch(`/api/users/${id}`);

    if (!response.ok) {
      throw new Error(`Failed to fetch user: ${response.statusText}`);
    }

    const data = await response.json();
    return UserSchema.parse(data); // 型安全性向上
  } catch (error) {
    console.error('Error fetching user:', error);
    throw error;
  }
}
```

**Pros**: 型安全性、バリデーション
**Cons**: Zod依存、パフォーマンスコスト
