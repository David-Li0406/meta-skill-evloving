---
name: verify-feature
description: 実装済み機能の検証ワークフロー（ビルド、テスト、レビュー、セキュリティ）
---

# Verify Feature Command

実装済みの機能に対して、各種検証エージェントを実行するコマンドです。
修正後に再実行することで、品質を確保できます。

## 前提条件

- `/implement-feature` で実装が完了していること
- または修正後に再検証が必要な状態であること

## 出力ファイル

```
docs/steering/{YYYYMMDD}-{feature-name}/
└── reports/          # 検証エージェントのレポート
    ├── build-executor.md   # ビルド結果
    ├── test-runner.md      # テスト・Lint結果
    ├── code-reviewer.md    # コードレビュー結果
    ├── security-checker.md # セキュリティチェック結果
    └── review-docs.md      # ドキュメント整合性結果
```

---

## 開始時の処理

コマンド実行時、**必ず TodoWrite ツールを呼び出して**タスクリストを初期化する。
末尾の「TodoWrite用データ」セクションのJSONを使用し、最初のタスクを `in_progress` に設定。

---

## Phase 1: 検証

以下のエージェントを順次実行し、問題があれば修正。各エージェントの結果は `reports/` ディレクトリに保存:

### Step 1: ビルド確認（build-executor エージェント）

```
**build-executor エージェントを実行します（独立コンテキスト）**

確認内容: `npm run build:local` でビルドエラーがないこと
```

→ レポート保存先: `docs/steering/{YYYYMMDD}-{feature-name}/reports/build-executor.md`

### Step 2: テスト・Lint（test-runner エージェント）

```
**test-runner エージェントを実行します（独立コンテキスト）**

確認内容: `npm run test && npm run lint` が通ること
```

→ レポート保存先: `docs/steering/{YYYYMMDD}-{feature-name}/reports/test-runner.md`

### Step 3: コードレビュー（code-reviewer エージェント）

```
**code-reviewer エージェントを実行します（独立コンテキスト）**

確認内容: 認証、バリデーション、型安全性
```

→ レポート保存先: `docs/steering/{YYYYMMDD}-{feature-name}/reports/code-reviewer.md`

### Step 4: セキュリティチェック（security-checker エージェント）

```
**security-checker エージェントを実行します（独立コンテキスト）**

確認内容: 認証・認可、インジェクション、OWASP Top 10
```

→ レポート保存先: `docs/steering/{YYYYMMDD}-{feature-name}/reports/security-checker.md`

### Step 5: ドキュメント整合性（review-docs エージェント）

```
**review-docs エージェントを実行します（独立コンテキスト）**

確認内容: 関連ドキュメントの整合性
```

→ レポート保存先: `docs/steering/{YYYYMMDD}-{feature-name}/reports/review-docs.md`

---

## Phase 2: 結果サマリー

### Step 6: 検証結果の表示

```
検証が完了しました！

## 検証結果サマリー

| 検証項目 | 結果 | 詳細 |
|----------|------|------|
| ビルド | ✅ / ❌ | reports/build-executor.md |
| テスト・Lint | ✅ / ❌ | reports/test-runner.md |
| コードレビュー | ✅ / ⚠️ / ❌ | reports/code-reviewer.md |
| セキュリティ | ✅ / ⚠️ / ❌ | reports/security-checker.md |
| ドキュメント | ✅ / ⚠️ / ❌ | reports/review-docs.md |

---

**次のステップ**:
- すべて ✅ の場合: `/create-pr` でPRを作成
- ❌ または ⚠️ がある場合: 修正後に再度 `/verify-feature` を実行
```

---

## エラーハンドリング

- **ビルド/テスト失敗**: エラー内容を表示し、修正を促す
- **レビューで Critical**: 即座の修正を推奨
- **レビューで Warning**: ユーザーに修正要否を確認

---

## 再検証について

修正後に再度 `/verify-feature` を実行すると:
- 既存のレポートは上書きされる
- すべての検証が再実行される

効率的な開発サイクル:
```
/implement-feature → /verify-feature → 修正 → /verify-feature → /create-pr
```

---

## TodoWrite用データ

```json
[
  {"content": "[エージェント] build-executor: ビルド確認", "activeForm": "build-executorでビルドを確認中", "status": "pending"},
  {"content": "[エージェント] test-runner: テスト・Lint確認", "activeForm": "test-runnerでテスト・Lintを確認中", "status": "pending"},
  {"content": "[エージェント] code-reviewer: コードレビュー", "activeForm": "code-reviewerでコードをレビュー中", "status": "pending"},
  {"content": "[エージェント] security-checker: セキュリティチェック", "activeForm": "security-checkerでセキュリティをチェック中", "status": "pending"},
  {"content": "[エージェント] review-docs: ドキュメント整合性確認", "activeForm": "review-docsでドキュメント整合性を確認中", "status": "pending"},
  {"content": "検証結果サマリー表示", "activeForm": "検証結果サマリーを表示中", "status": "pending"}
]
```
