---
name: implement-feature
description: 設計済み機能のTDD実装ワークフロー
---

# Implement Feature Command

`/add-feature` で作成された設計ドキュメントに基づいて、TDDで実装を進めるコマンドです。
**検証は `/verify-feature`、PR作成は `/create-pr` で行います。**

## 前提条件

`docs/steering/{日付}-{機能名}/` に以下が存在すること:
- `requirements.md`（要件定義）
- `design.md`（技術設計）
- `tasklist.md`（タスクリスト）

## Phase 1: 実装準備

### Step 1: 設計ドキュメント読み込みとTodoWrite初期化

```
実装を開始します！

📁 **ステアリングディレクトリ**: `docs/steering/{YYYYMMDD}-{feature-name}/`

設計ドキュメントを確認しています...
```

以下を読み込む:
1. `requirements.md` - 要件とゴールの確認
2. `design.md` - 技術設計の確認（実装中はこのファイルを参照）
3. `tasklist.md` - 「TodoWrite用データ」セクションのJSONを取得

**TodoWrite初期化**:
- `tasklist.md` の末尾にある「TodoWrite用データ」のJSON配列を抽出
- **必ず TodoWrite ツールを呼び出して**タスクリストを初期化
- 最初のタスクを `in_progress` に設定

※ TodoWrite初期化後、`tasklist.md` は参照不要。実装詳細は `design.md` を参照する。

初期化後に表示:
```
タスクリストを初期化しました。

**タスク数**: {total}
**残り**: {pending}
```

---

## Phase 2: TDD実装

### Step 3: TDDサイクル - Red Phase（テスト作成）

```
🔴 **Red Phase**: まずテストを書きます。

TodoWriteの現在のタスクに対応するテストファイルを作成します。
テストは失敗する状態（Red）で開始します。

**テストファイル作成手順**:
1. `design.md` の「6. テスト戦略」に記載したテストケースを確認
2. 対象ファイルと同階層にテストファイルを作成
   - コンポーネント: `ComponentName.test.tsx`
   - フック: `useHookName.test.ts`
   - APIルート: `route.test.ts`
3. テストケースを実装
4. `npm run test:watch` でテスト失敗を確認
```

### Step 4: TDDサイクル - Green Phase（最小実装）

```
🟢 **Green Phase**: テストを通す最小限のコードを実装します。

design.md に従いつつ、まずはテストを通すことを優先してください。
完璧な実装でなくてOKです。
```

### Step 5: TDDサイクル - Refactor Phase（リファクタリング）

```
🔵 **Refactor Phase**: コードを改善します。

テストがパスした状態を維持しながら:
- 重複の除去
- 命名の改善
- パフォーマンス最適化

を行います。リファクタリング後もテストがパスすることを確認してください。
```

### Step 6: TDDサイクル繰り返し

TodoWriteの残りのタスクに対して、Step 3-5 を繰り返す。
各タスク完了時にTodoWriteのステータスを `completed` に更新。

**TDDサイクルの凡例**:
- 🔴 Red: テスト作成（失敗するテスト）
- 🟢 Green: 最小実装（テストをパス）
- 🔵 Refactor: コード改善（テスト維持）

---

## Phase 3: 完了

### Step 7: 完了処理

すべてのタスクが完了したら:

```
TDD実装が完了しました！

**完了したタスク**: {total}

次のステップ:
1. `/verify-feature` で検証を実行
2. 必要に応じて修正
3. `/create-pr` でPRを作成
```

---

## エラーハンドリング

- **テスト失敗が解消できない**: 3回失敗でユーザーに相談
- **設計と実装の乖離**: ユーザーに確認し、必要なら design.md を更新
