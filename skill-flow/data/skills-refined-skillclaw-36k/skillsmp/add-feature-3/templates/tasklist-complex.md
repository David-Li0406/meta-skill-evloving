# {機能名} - タスクリスト（複合ページ）

**ステータス**: 計画中 | 実装中 | 完了
**作成日**: {YYYY-MM-DD}
**設計**: [design.md](./design.md)
**機能タイプ**: D. 複合ページ

---

## 用途

複数機能を持つ新規ページ、ウィザード形式のフロー、複雑な状態管理が必要な画面

## タスク

| # | タスク | 対象ファイル | ステータス |
|---|--------|-------------|-----------|
| 1 | ページ設計（状態・フロー） | - | [ ] |
| 2 | 型定義追加 | `src/types/` | [ ] |
| **3** | **🔴 APIエンドポイントテスト作成** | `src/app/api/**/route.test.ts` | [ ] |
| **4** | **🟢 APIエンドポイント実装** | `src/app/api/**/route.ts` | [ ] |
| **5** | **🔵 APIエンドポイントリファクタリング** | - | [ ] |
| **6** | **🔴 カスタムフックテスト作成** | `src/hooks/**/*.test.ts` | [ ] |
| **7** | **🟢 カスタムフック実装** | `src/hooks/**/*.ts` | [ ] |
| **8** | **🔵 カスタムフックリファクタリング** | - | [ ] |
| **9** | **🔴 メインコンポーネントテスト作成** | `src/components/**/*.test.tsx` | [ ] |
| **10** | **🟢 メインコンポーネント実装** | `src/components/**/*.tsx` | [ ] |
| **11** | **🔵 メインコンポーネントリファクタリング** | - | [ ] |
| **12** | **🔴 サブコンポーネントテスト作成** | `src/components/**/*.test.tsx` | [ ] |
| **13** | **🟢 サブコンポーネント・モーダル実装** | `src/components/**/*.tsx` | [ ] |
| **14** | **🔵 サブコンポーネントリファクタリング** | - | [ ] |
| 15 | エラーハンドリング実装 | | [ ] |
| 16 | 統合テスト | - | [ ] |

**TDDサイクルの凡例**:
- 🔴 Red: テスト作成（失敗するテスト）
- 🟢 Green: 最小実装（テストをパス）
- 🔵 Refactor: コード改善（テスト維持）

**参考ファイル**: `src/components/speech/SpeechAdd.tsx`, `src/components/phrase/PhraseAdd.tsx`

**注意**: 複数のローディング状態を管理、ボタンの有効/無効条件を明確に

---

## TodoWrite用データ

```json
[
  {"content": "[エージェント] file-finder: 関連ファイル検索", "activeForm": "file-finderで関連ファイルを検索中", "status": "pending"},
  {"content": "ページ設計（状態・フロー）", "activeForm": "ページ設計中", "status": "pending"},
  {"content": "型定義追加", "activeForm": "型定義を追加中", "status": "pending"},
  {"content": "🔴 APIエンドポイントテスト作成", "activeForm": "APIエンドポイントのテストを作成中（Red Phase）", "status": "pending"},
  {"content": "🟢 APIエンドポイント実装", "activeForm": "APIエンドポイントを実装中（Green Phase）", "status": "pending"},
  {"content": "🔵 APIエンドポイントリファクタリング", "activeForm": "APIエンドポイントをリファクタリング中（Refactor Phase）", "status": "pending"},
  {"content": "🔴 カスタムフックテスト作成", "activeForm": "カスタムフックのテストを作成中（Red Phase）", "status": "pending"},
  {"content": "🟢 カスタムフック実装", "activeForm": "カスタムフックを実装中（Green Phase）", "status": "pending"},
  {"content": "🔵 カスタムフックリファクタリング", "activeForm": "カスタムフックをリファクタリング中（Refactor Phase）", "status": "pending"},
  {"content": "🔴 メインコンポーネントテスト作成", "activeForm": "メインコンポーネントのテストを作成中（Red Phase）", "status": "pending"},
  {"content": "🟢 メインコンポーネント実装", "activeForm": "メインコンポーネントを実装中（Green Phase）", "status": "pending"},
  {"content": "🔵 メインコンポーネントリファクタリング", "activeForm": "メインコンポーネントをリファクタリング中（Refactor Phase）", "status": "pending"},
  {"content": "🔴 サブコンポーネントテスト作成", "activeForm": "サブコンポーネントのテストを作成中（Red Phase）", "status": "pending"},
  {"content": "🟢 サブコンポーネント・モーダル実装", "activeForm": "サブコンポーネント・モーダルを実装中（Green Phase）", "status": "pending"},
  {"content": "🔵 サブコンポーネントリファクタリング", "activeForm": "サブコンポーネントをリファクタリング中（Refactor Phase）", "status": "pending"},
  {"content": "エラーハンドリング実装", "activeForm": "エラーハンドリングを実装中", "status": "pending"},
  {"content": "統合テスト", "activeForm": "統合テスト中", "status": "pending"},
  {"content": "[エージェント] build-executor: ビルド確認", "activeForm": "build-executorでビルドを確認中", "status": "pending"},
  {"content": "[エージェント] test-runner: テスト・Lint確認", "activeForm": "test-runnerでテスト・Lintを確認中", "status": "pending"},
  {"content": "[エージェント] code-reviewer: コードレビュー", "activeForm": "code-reviewerでコードをレビュー中", "status": "pending"},
  {"content": "[エージェント] security-checker: セキュリティチェック", "activeForm": "security-checkerでセキュリティをチェック中", "status": "pending"},
  {"content": "[エージェント] review-docs: ドキュメント整合性確認", "activeForm": "review-docsでドキュメント整合性を確認中", "status": "pending"}
]
```
