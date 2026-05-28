# {機能名} - タスクリスト（機能修正）

**ステータス**: 計画中 | 実装中 | 完了
**作成日**: {YYYY-MM-DD}
**変更要求**: [change-request.md](./change-request.md)
**影響分析**: [impact-analysis.md](./impact-analysis.md)

---

## 用途

既存機能の改善、仕様変更、動作変更

## タスク

| # | タスク | 対象ファイル | ステータス |
|---|--------|-------------|-----------|
| **1** | **[オプション] 🔴 テスト作成** | `*.test.ts` | [ ] |
| 2 | 🟢 修正実装（TDD使用時はテストパス確認） | - | [ ] |
| 3 | 🔵 リファクタリング（必要に応じて） | - | [ ] |
| 4 | 既存機能の動作確認 | - | [ ] |
| 5 | 新しい動作の確認 | - | [ ] |
| 6 | [エージェント] build-executor: ビルド確認 | - | [ ] |
| 7 | [エージェント] test-runner: テスト・Lint | - | [ ] |
| 8 | [エージェント] code-reviewer: コードレビュー | - | [ ] |
| 9 | [エージェント] security-checker: セキュリティ | - | [ ] |
| 10 | [エージェント] review-docs: ドキュメント | - | [ ] |

**TDDサイクルの凡例**（オプション使用時）:
- 🔴 Red: 期待動作テスト作成（失敗 or 変更前の動作を確認）
- 🟢 Green: 変更実装（テストをパス）
- 🔵 Refactor: コード改善（テスト維持）

**参考ファイル**: impact-analysis.md の「1. 影響を受けるコンポーネント」セクション

**注意**: 後方互換性を最大限維持すること、既存機能への影響を最小限に抑える

---

## TodoWrite用データ

```json
[
  {"content": "[オプション] 🔴 テスト作成", "activeForm": "テストを作成中（Red Phase）", "status": "pending"},
  {"content": "🟢 修正実装", "activeForm": "修正を実装中（Green Phase）", "status": "pending"},
  {"content": "🔵 リファクタリング", "activeForm": "リファクタリング中（Refactor Phase）", "status": "pending"},
  {"content": "既存機能の動作確認", "activeForm": "既存機能の動作確認中", "status": "pending"},
  {"content": "新しい動作の確認", "activeForm": "新しい動作を確認中", "status": "pending"},
  {"content": "[エージェント] build-executor: ビルド確認", "activeForm": "build-executorでビルドを確認中", "status": "pending"},
  {"content": "[エージェント] test-runner: テスト・Lint確認", "activeForm": "test-runnerでテスト・Lintを確認中", "status": "pending"},
  {"content": "[エージェント] code-reviewer: コードレビュー", "activeForm": "code-reviewerでコードをレビュー中", "status": "pending"},
  {"content": "[エージェント] security-checker: セキュリティチェック", "activeForm": "security-checkerでセキュリティをチェック中", "status": "pending"},
  {"content": "[エージェント] review-docs: ドキュメント整合性確認", "activeForm": "review-docsでドキュメント整合性を確認中", "status": "pending"}
]
```
