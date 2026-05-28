# 使用例

ArchitectureGuardianの具体的な使用例。

## 例1: 新機能「ダッシュボード」開発

開発の全フェーズでArchitectureGuardianがどのように活用されるかを示す例。

### フェーズ1: 設計

**ユーザー**:

```text
@ArchitectureGuardian 「ダッシュボード画面を作りたい。どういう設計がいい？」
```

**ArchitectureGuardian応答**:

```markdown
## アーキテクチャ設計書: ダッシュボード画面

### 1. 要件整理

**コア機能**:
- ユーザーの進捗状況を表示
- 最近の活動履歴を表示

**拡張機能（後回し）**:
- グラフ表示
- エクスポート機能

### 2. 3大層分解

| 層 | ファイル | 責務 |
| :--- | :--- | :--- |
| UI層 | app/routes/dashboard/index.tsx | ダッシュボードUIの描画 |
| lib層 | app/lib/dashboard/progressCalculator.ts | 進捗率計算ロジック |
| data-io層 | app/data-io/dashboard/dashboardLoader.server.ts | ダッシュボードデータ取得 |

### 3. Outside-In TDDフロー

**Phase 1: E2Eテスト作成**

```typescript
// tests/e2e/screen/dashboard.screen.spec.ts
test('ダッシュボード画面が正しく表示される', async ({ page }) => {
  await page.goto('/dashboard');
  await expect(page.locator('h1')).toContainText('Dashboard');
  await expect(page.locator('[data-testid="progress"]')).toBeVisible();
});
```

**Phase 2: ユニットテスト + 実装**

1. lib層: progressCalculator.ts + progressCalculator.test.ts
2. data-io層: dashboardLoader.server.ts + dashboardLoader.test.ts
3. UI層: index.tsx（E2Eでカバー）

### 4. 生成コマンド

```bash
npm run generate -- --category lib --service dashboard --name progressCalculator
npm run generate -- --category data-io --service dashboard --name dashboardLoader
npm run generate -- --category ui --ui-type route --service dashboard --name index
npm run generate -- --category e2e --service dashboard --name dashboard.screen
```

次に、@GeneratorOperator を呼び出してこれらのファイルを生成しましょうか？
```

### フェーズ2: 実装

開発者が実装を行う。誤って`progressCalculator.ts`内で`fetch`を呼び出してしまう。

```typescript
// app/lib/dashboard/progressCalculator.ts（違反コード）
export async function calculateProgress(userId: string) {
  // ❌ lib層でfetch（副作用）
  const response = await fetch(`/api/users/${userId}/progress`);
  const data = await response.json();
  return (data.completed / data.total) * 100;
}
```

### フェーズ3: レビュー

**ユーザー**:

```text
@CodeReviewer 「ダッシュボード機能の実装が終わったのでレビューをお願いします」
```

**CodeReviewer応答**:

```markdown
レビューを開始します...

【アーキテクチャ違反を検知】

違反を1件検知しました。@ArchitectureGuardian に詳細なガイダンスを依頼します。
```

**ArchitectureGuardian応答**（自動起動）:

```markdown
【アーキテクチャ違反是正ガイダンス】

❌ **重大な違反: 3大層アーキテクチャ違反**

- **ファイル**: `app/lib/dashboard/progressCalculator.ts`
- **違反内容**: lib層（純粋ロジック層）で副作用である`fetch`が呼び出されています。
- **理由**: lib層はテスト容易性を担保するため、副作用から完全に隔離されている必要があります。

**修正案**:

1. `fetch`処理を`app/data-io/dashboard/dashboardLoader.server.ts`に移動してください。
2. `progressCalculator.ts`は、`dashboardLoader`から渡されたデータを元に計算処理のみを行う純粋関数にしてください。

**修正後のコード**:

```typescript
// app/lib/dashboard/progressCalculator.ts（修正後）
export function calculateProgress(completed: number, total: number): number {
  return (completed / total) * 100;
}

// app/data-io/dashboard/dashboardLoader.server.ts（修正後）
export async function getDashboardData(userId: string) {
  const response = await fetch(`/api/users/${userId}/progress`);
  return response.json();
}
```

修正後、以下を実行してください：

1. `npm run typecheck` - 型チェック
2. `npm run test` - ユニットテスト実行
3. `@CodeReviewer` - 再レビュー依頼
```

---

## 例2: アーキテクチャ違反のチェック

既存コードのアーキテクチャ違反をチェックする例。

**ユーザー**:

```text
@ArchitectureGuardian 「app/lib/auth/login.ts のアーキテクチャをチェックして」
```

**ArchitectureGuardian応答**:

```markdown
## アーキテクチャ違反レポート

### 対象ファイル

- app/lib/auth/login.ts

### 違反サマリー

| 重要度 | 件数 |
| :--- | :--- |
| 🔴 Critical | 1 |
| 🟡 Warning | 0 |
| 🔵 Info | 0 |

---

## 違反詳細

### 🔴 Critical: lib層で副作用を実行

**ファイル**: `app/lib/auth/login.ts`
**行**: 5
**違反内容**: lib層でfetchを使用（副作用の実行）

#### なぜ違反なのか？

lib層は「純粋関数のみ」を配置する層です。fetchはネットワーク通信という副作用を伴うため、lib層で実行できません。純粋関数のみに制限することで、テスト容易性が向上します。

#### 修正方針

1. lib層には純粋なバリデーションロジックのみを残す
2. fetch処理は data-io層の `.server.ts` ファイルに移動
3. UI層のloader/actionから data-io層を呼び出す

#### 修正コード例

**Before**:

```typescript
// app/lib/auth/login.ts
export async function login(email: string, password: string) {
  const response = await fetch('/api/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
  return response.json();
}
```

**After**:

```typescript
// app/lib/auth/loginValidator.ts（lib層）
export function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export function validatePassword(password: string): boolean {
  return password.length >= 8;
}

// app/data-io/auth/loginService.server.ts（data-io層）
export async function login(email: string, password: string) {
  const response = await fetch('/api/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
  return response.json();
}
```

#### 修正コマンド

```bash
npm run generate -- --category data-io --service auth --name loginService
```

---

## 修正後の検証

以下を順に実行してください：

```bash
# 1. 型チェック
npm run typecheck

# 2. ユニットテスト実行
npm test

# 3. リント実行
npm run lint:all

# 4. CodeReviewerで再レビュー
@CodeReviewer
```
```

---

## 例3: サブエージェント推薦

どのサブエージェントを使うべきか迷った時の例。

**ユーザー**:

```text
@ArchitectureGuardian 「新しいテンプレートを追加したいんだけど、どのサブエージェントを使えばいい？」
```

**ArchitectureGuardian応答**:

```markdown
## サブエージェント推薦

### あなたのタスク

新しいテンプレートを追加したい

### 推薦エージェント

**GeneratorMaintainer**

### 推薦理由

テンプレートの追加・修正・管理はGeneratorMaintainerの専門領域です。テンプレートの一貫性を保ちながら、プロジェクトの規約に沿ったテンプレートを作成できます。

### 呼び出し例

```text
@GeneratorMaintainer 「lib層のhelper用テンプレートを追加して」
```

### このエージェントの強み

- テンプレートの保守と更新に特化
- プロジェクト規約に沿ったテンプレート作成
- テンプレートリントによる品質保証

### 他の選択肢

- **GeneratorOperator**: テンプレートからファイルを生成する場合（テンプレート自体は作成しない）
```

---

## 例4: 設計思想の学習

設計思想について学習する例。

**ユーザー**:

```text
@ArchitectureGuardian 「なぜlib層で副作用を実行してはいけないのか教えて」
```

**ArchitectureGuardian応答**:

```markdown
## 「lib層で副作用を実行してはいけない」理由

### なぜこのルールが必要か？

lib層は**純粋関数のみ**を配置する層です。純粋関数とは、同じ入力に対して常に同じ出力を返す関数です。

### 解決する問題

1. **テスト困難**: 副作用があると、テスト時にモックが必要になり、テストが複雑化
2. **予測不可能**: 外部の状態に依存するため、同じ入力でも異なる出力になる可能性
3. **再利用困難**: 副作用があると、どこからでも安全に呼び出せない

### 基本原則

| 原則 | 説明 |
| :--- | :--- |
| 純粋関数のみ | 同じ入力 → 同じ出力 |
| 副作用禁止 | fetch、localStorage、DOM操作等の禁止 |
| 他層への依存禁止 | lib層は独立した存在 |

### 具体例

#### ❌ 違反コード

```typescript
// app/lib/user/userLoader.ts
export async function getUser(id: string) {
  // ❌ lib層でfetch（副作用）
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}
```

**問題点**:
- テスト時にAPIサーバーが必要（または複雑なモックが必要）
- ネットワーク状態によって結果が変わる
- 他の環境で再利用困難

#### ✅ 準拠コード

```typescript
// app/lib/user/userFormatter.ts（lib層）
export function formatUserName(firstName: string, lastName: string): string {
  return `${lastName} ${firstName}`;
}

export function isAdult(age: number): boolean {
  return age >= 18;
}

// app/data-io/user/userService.server.ts（data-io層）
export async function getUser(id: string) {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}
```

**改善点**:
- lib層は純粋関数のみ（テストが容易）
- 副作用はdata-io層で実行
- lib層はどこからでも安全に呼び出せる

### さらに詳しく学ぶには

- `docs/ARCHITECTURE_MANIFESTO2.md` - 3大層アーキテクチャの詳細
- `develop/service-name/GUIDING_PRINCIPLES.md` - テスト駆動開発との関係

### よくある誤解

- **誤解**: lib層で何もできない
- **正しい理解**: lib層は純粋関数（計算、バリデーション、フォーマット等）を担う重要な層
```

---

## 例5: 複数ファイルのチェック

複数のファイルを同時にチェックする例。

**ユーザー**:

```text
@ArchitectureGuardian 「以下のファイルのアーキテクチャをチェックして」
- app/lib/auth/login.ts
- app/lib/dashboard/progressCalculator.ts
- app/routes/dashboard/index.tsx
```

**ArchitectureGuardian応答**:

```markdown
## アーキテクチャ違反レポート（複数ファイル）

### 対象ファイル

- app/lib/auth/login.ts
- app/lib/dashboard/progressCalculator.ts
- app/routes/dashboard/index.tsx

### 違反サマリー

| ファイル | 🔴 Critical | 🟡 Warning | 🔵 Info |
| :--- | :--- | :--- | :--- |
| app/lib/auth/login.ts | 1 | 0 | 0 |
| app/lib/dashboard/progressCalculator.ts | 1 | 0 | 0 |
| app/routes/dashboard/index.tsx | 0 | 1 | 0 |

---

## ファイル1: app/lib/auth/login.ts

### 🔴 Critical: lib層で副作用を実行

（詳細は例2と同様）

---

## ファイル2: app/lib/dashboard/progressCalculator.ts

### 🔴 Critical: lib層で副作用を実行

（詳細は例1と同様）

---

## ファイル3: app/routes/dashboard/index.tsx

### 🟡 Warning: UI層にビジネスロジック

**ファイル**: `app/routes/dashboard/index.tsx`
**行**: 15
**違反内容**: UI層に複雑な計算ロジックが含まれています

#### 修正方針

複雑な計算ロジックは lib層に移動してください。

（修正コード例）

---

## 修正優先順位

1. 🔴 Critical: app/lib/auth/login.ts（最優先）
2. 🔴 Critical: app/lib/dashboard/progressCalculator.ts（最優先）
3. 🟡 Warning: app/routes/dashboard/index.tsx
```

---

## まとめ

ArchitectureGuardianは、開発の各フェーズで以下のように活用できます：

| フェーズ | 活用方法 | 例 |
| :--- | :--- | :--- |
| 設計 | 設計提案を受ける | 例1 |
| 実装後 | アーキテクチャ違反をチェック | 例2 |
| タスク開始前 | サブエージェント推薦を受ける | 例3 |
| 学習 | 設計思想を学ぶ | 例4 |
| レビュー | 複数ファイルをチェック | 例5 |
