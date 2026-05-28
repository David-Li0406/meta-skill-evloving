# 連携パターン詳細

ArchitectureGuardianと他のサブエージェントとの連携パターン。

## 連携パターン一覧

| パターン | 起動元 | 起動先 | シーン |
| :--- | :--- | :--- | :--- |
| 設計→生成 | ArchitectureGuardian | GeneratorOperator | 設計提案後、ファイル生成を依頼 |
| 監査→レビュー | ArchitectureGuardian | CodeReviewer | 違反検出後、詳細レビューを依頼 |
| レビュー→監査（自動） | CodeReviewer | ArchitectureGuardian | アーキテクチャ違反を検知した際に自動起動 |
| 監査→デバッグ | ArchitectureGuardian | Debugger | 違反修正時にエラーが発生 |

---

## パターン1: ArchitectureGuardian → GeneratorOperator

### シーン

設計提案後、ファイル生成を依頼

### フロー

```text
ユーザー
  ↓ 「〜の設計を提案して」
ArchitectureGuardian（設計提案）
  ↓ 設計書 + 生成コマンド提示
ユーザー
  ↓ 提案に基づき起動
GeneratorOperator（ファイル生成）
```

### 具体例

**ユーザー**: `@ArchitectureGuardian 「認証機能の設計を提案して」`

**ArchitectureGuardian応答**:

```markdown
## アーキテクチャ設計書: 認証機能

### 3大層分解

1. UI層: `app/routes/login.tsx`
2. lib層: `app/lib/auth/passwordValidator.ts`
3. data-io層: `app/data-io/auth/authService.server.ts`

### 生成コマンド

以下の順序で実行してください：

```bash
npm run generate -- --category lib --service auth --name passwordValidator
npm run generate -- --category data-io --service auth --name authService
npm run generate -- --category ui --ui-type route --service auth --name login
```

次に、@GeneratorOperator を呼び出してこれらのファイルを生成しましょうか？
```

**ユーザー**: `@GeneratorOperator`（設計書のコマンドを実行）

---

## パターン2: ArchitectureGuardian → CodeReviewer

### シーン

違反検出後、詳細レビューを依頼

### フロー

```text
ユーザー
  ↓ 「アーキテクチャをチェックして」
ArchitectureGuardian（違反検出）
  ↓ 違反レポート
ユーザー
  ↓ （違反修正後）詳細レビュー依頼
CodeReviewer（詳細レビュー）
```

### 具体例

**ユーザー**: `@ArchitectureGuardian 「app/lib/auth/passwordValidator.ts のアーキテクチャをチェックして」`

**ArchitectureGuardian応答**:

```markdown
## アーキテクチャ違反レポート

### 🟡 Warning: lib層から data-io層のimport

**ファイル**: `app/lib/auth/passwordValidator.ts`
**違反内容**: lib層から data-io層のimportが検出されました

#### 修正方針

lib層は他層に依存してはいけません。...（修正方針）

修正後、@CodeReviewer で詳細レビュー（命名規則、TypeScript品質含む）をお願いします。
```

**ユーザー**: （修正後）`@CodeReviewer 「app/lib/auth/passwordValidator.ts のレビューをお願いします」`

---

## パターン3: CodeReviewer → ArchitectureGuardian（自動起動）

### シーン

CodeReviewerがアーキテクチャ違反を検知した際に自動起動

### フロー

```text
ユーザー
  ↓ 「レビューして」
CodeReviewer（コードレビュー）
  ↓ アーキテクチャ違反を検知
CodeReviewer（自動連携）
  ↓ 違反情報を渡す
ArchitectureGuardian（自動起動）
  ↓ 修正ガイダンスを提示
ユーザー
```

### 具体例

**ユーザー**: `@CodeReviewer 「ダッシュボード機能のレビューをお願いします」`

**CodeReviewer応答**:

```markdown
レビューを開始します...

【アーキテクチャ違反を検知】

ファイル: app/lib/auth/login.ts
違反: lib層でfetchを使用（副作用の実行）

@ArchitectureGuardian に修正ガイダンスを依頼します。
```

**ArchitectureGuardian応答**（自動起動）:

```markdown
【事後是正ガイダンス】

❌ **重大な違反: lib層で副作用を実行**

**違反箇所**:
- ファイル: app/lib/auth/login.ts
- 行: `const response = await fetch('/api/login', {...})`
- 重要度: 🔴 Critical

**なぜ違反なのか？**
lib層は「純粋関数のみ」を配置する層です。fetchはネットワーク通信という副作用を伴うため、lib層で実行できません。

**修正方針**:
1. lib層には純粋なバリデーションロジックのみを残す
2. fetch処理は data-io層の `.server.ts` ファイルに移動
3. UI層のloader/actionから data-io層を呼び出す

**具体的な修正手順**:

Step 1: lib層を純粋ロジックに修正

```typescript
// app/lib/auth/loginValidator.ts
export function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export function validatePassword(password: string): boolean {
  return password.length >= 8;
}
```

Step 2: data-io層にfetch処理を移動

```bash
npm run generate -- --category data-io --service auth --name loginService
```

Step 3: UI層から data-io層を呼び出す

```typescript
// app/routes/login.tsx
import { validateEmail, validatePassword } from '~/lib/auth/loginValidator';
import { loginUser } from '~/data-io/auth/loginService.server';

export async function action({ request }: ActionArgs) {
  const formData = await request.formData();
  const email = formData.get('email');
  const password = formData.get('password');

  // バリデーション（lib層）
  if (!validateEmail(email) || !validatePassword(password)) {
    return json({ error: 'Invalid input' }, { status: 400 });
  }

  // API呼び出し（data-io層）
  return await loginUser(email, password);
}
```

修正後、以下を実行してください：

1. `npm run typecheck` - 型チェック
2. `npm run test` - ユニットテスト実行
3. `@CodeReviewer` - 再レビュー依頼
```

---

## パターン4: ArchitectureGuardian → Debugger

### シーン

違反修正時にエラーが発生

### フロー

```text
ArchitectureGuardian
  ↓ 修正ガイダンス提示
ユーザー
  ↓ 修正実行
エラー発生
  ↓
Debugger（エラー解析）
```

### 具体例

**ArchitectureGuardian**: 修正ガイダンスを提示

**ユーザー**: 修正実行 → エラー発生

**ユーザー**: `@Debugger 「ArchitectureGuardianの修正案を実行したらエラーが出ました」`

**Debugger**: エラー解析と修正方針を提示

---

## 連携のベストプラクティス

### 新規機能開発の推奨フロー

```text
1. @ArchitectureGuardian 「〜の設計を提案して」
   ↓ 設計書を受け取る

2. @GeneratorOperator
   ↓ 設計書のコマンドを実行

3. （実装）

4. @CodeReviewer 「〜のレビューをお願いします」
   ↓ レビュー結果を確認
   ↓ （違反があれば）ArchitectureGuardianが自動起動

5. 修正 → @CodeReviewer（再レビュー）
```

### アーキテクチャ違反修正の推奨フロー

```text
1. @ArchitectureGuardian 「〜のアーキテクチャをチェックして」
   ↓ 違反レポートを受け取る

2. 修正実行
   ↓ （エラーが出たら）

3. @Debugger 「エラーが出ました」
   ↓ エラー解析

4. 修正 → @CodeReviewer（確認）
```

### 設計相談の推奨フロー

```text
1. @ArchitectureGuardian 「設計思想について教えて」
   ↓ 教育コンテンツを受け取る

2. @ArchitectureGuardian 「どのサブエージェントを使えばいい？」
   ↓ 推薦を受け取る

3. 推薦されたエージェントを起動
```

## 注意事項

- **自動起動はCodeReviewerからのみ**: ArchitectureGuardianの自動起動は、現在CodeReviewerがアーキテクチャ違反を検知した際にのみ発動します
- **複数エージェントの併用**: タスクによっては、複数のエージェントを順次使用することが推奨されます
- **推薦は提案**: ArchitectureGuardianのサブエージェント推薦はあくまで提案です。状況に応じて判断してください
