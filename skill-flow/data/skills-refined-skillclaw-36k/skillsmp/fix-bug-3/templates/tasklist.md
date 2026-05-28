# {バグ名} - タスクリスト

**ステータス**: 計画中 | 実装中 | 完了
**作成日**: {YYYY-MM-DD}
**調査結果**: [investigation.md](./investigation.md)
**修正計画**: [fix-plan.md](./fix-plan.md)

---

## 用途

バグ修正、不具合対応、緊急修正

## タスク

| # | タスク | 対象ファイル | ステータス |
|---|--------|-------------|-----------|
| **1** | **[オプション] 🔴 リグレッションテスト作成** | `*.test.ts` | [ ] |
| 2 | 修正実装（🟢 TDD使用時はテストパス確認） | | [ ] |
| 3 | 🔵 リファクタリング（必要に応じて） | | [ ] |
| 4 | 修正確認テスト | fix-plan.md参照 | [ ] |
| 5 | 回帰テスト | | [ ] |
| 6 | 動作確認 | - | [ ] |
| 7 | 🔧 ビルド確認 | - | [ ] |
| 8 | 🧪 テスト・Lint | - | [ ] |
| 9 | 🔍 コードレビュー | 変更ファイル | [ ] |
| 10 | 🔒 セキュリティチェック | 変更ファイル | [ ] |
| 11 | 📝 ドキュメント整合性 | docs/ | [ ] |

**TDDサイクルの凡例**（オプション使用時）:
- 🔴 Red: バグ再現テスト作成（失敗するテスト）
- 🟢 Green: バグ修正（テストをパス）
- 🔵 Refactor: コード改善（テスト維持）

**参考ファイル**: investigation.md の「5. 原因分析」セクション

**注意**: 最小限の修正で問題を解決すること、関連する箇所の回帰テストを必ず実施

---

## TodoWrite用データ

```json
[
  {"content": "[オプション] 🔴 リグレッションテスト作成", "activeForm": "リグレッションテストを作成中（Red Phase）", "status": "pending"},
  {"content": "🟢 修正実装", "activeForm": "修正を実装中（Green Phase）", "status": "pending"},
  {"content": "🔵 リファクタリング", "activeForm": "リファクタリング中（Refactor Phase）", "status": "pending"},
  {"content": "修正確認テスト", "activeForm": "修正確認テストを実行中", "status": "pending"},
  {"content": "回帰テスト", "activeForm": "回帰テストを実行中", "status": "pending"},
  {"content": "動作確認", "activeForm": "動作確認中", "status": "pending"},
  {"content": "[エージェント] build-executor: ビルド確認", "activeForm": "build-executorでビルドを確認中", "status": "pending"},
  {"content": "[エージェント] test-runner: テスト・Lint確認", "activeForm": "test-runnerでテスト・Lintを確認中", "status": "pending"},
  {"content": "[エージェント] code-reviewer: コードレビュー", "activeForm": "code-reviewerでコードをレビュー中", "status": "pending"},
  {"content": "[エージェント] security-checker: セキュリティチェック", "activeForm": "security-checkerでセキュリティをチェック中", "status": "pending"},
  {"content": "[エージェント] review-docs: ドキュメント整合性確認", "activeForm": "review-docsでドキュメント整合性を確認中", "status": "pending"}
]
```
