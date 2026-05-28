# {バグ名} - プロセス進捗

**コマンド**: /fix-bug
**開始日時**: {YYYY-MM-DD HH:mm}

---

## Phase 1: バグ情報収集

Step 1: 初期入力の受け取り
Step 2: 初期入力の解釈と確認
Step 3: ステアリングディレクトリ作成
Step 4: 影響度と環境の確認
Step 5: investigation.md レビュー・承認

---

## Phase 2: 原因調査

Step 6: コードベース調査（file-finder エージェント）
Step 7: 影響範囲分析（impact-analyzer エージェント）
Step 8: 修正計画の策定、fix-plan.md 作成
Step 9: fix-plan.md レビュー・承認

---

## Phase 3: 実装計画

Step 10: tasklist.md 作成
Step 11: 最終確認
Step 12: ブランチ作成・コミット

---

## 生成されたファイル

- investigation.md（Phase 1 完了時）
- fix-plan.md（Phase 2 完了時）
- tasklist.md（Phase 3 完了時）

---

## 備考

<!-- メモや特記事項をここに記録 -->

---

## TodoWrite用データ

```json
[
  {"content": "Step 1: 初期入力を受け取り", "activeForm": "初期入力を受け取り中", "status": "pending"},
  {"content": "Step 2: 初期入力を解釈・要約", "activeForm": "初期入力を解釈中", "status": "pending"},
  {"content": "Step 2: 不足情報を質問", "activeForm": "不足情報を質問中", "status": "pending"},
  {"content": "Step 3: ディレクトリ作成", "activeForm": "ディレクトリを作成中", "status": "pending"},
  {"content": "Step 3: progress.md 作成", "activeForm": "progress.mdを作成中", "status": "pending"},
  {"content": "Step 3: investigation.md 作成・記入", "activeForm": "investigation.mdを作成中", "status": "pending"},
  {"content": "Step 4: 影響度を確認", "activeForm": "影響度を確認中", "status": "pending"},
  {"content": "Step 4: 発生環境を確認", "activeForm": "発生環境を確認中", "status": "pending"},
  {"content": "Step 4: investigation.md 更新", "activeForm": "investigation.mdを更新中", "status": "pending"},
  {"content": "Step 5: investigation.md をユーザーに提示", "activeForm": "investigation.mdのレビューを依頼中", "status": "pending"},
  {"content": "Step 5: ユーザーの「承認」を取得", "activeForm": "investigation.mdの承認を取得中", "status": "pending"},
  {"content": "Step 6: file-finder エージェント実行", "activeForm": "file-finderでコードベースを調査中", "status": "pending"},
  {"content": "Step 6: investigation.md「原因分析」セクション記入", "activeForm": "原因分析を記入中", "status": "pending"},
  {"content": "Step 7: impact-analyzer エージェント実行", "activeForm": "impact-analyzerで影響範囲を分析中", "status": "pending"},
  {"content": "Step 7: investigation.md「影響範囲」セクション記入", "activeForm": "影響範囲を記入中", "status": "pending"},
  {"content": "Step 8: 修正方針を検討", "activeForm": "修正方針を検討中", "status": "pending"},
  {"content": "Step 8: テスト計画を検討", "activeForm": "テスト計画を検討中", "status": "pending"},
  {"content": "Step 8: fix-plan.md 作成", "activeForm": "fix-plan.mdを作成中", "status": "pending"},
  {"content": "Step 9: fix-plan.md をユーザーに提示", "activeForm": "fix-plan.mdのレビューを依頼中", "status": "pending"},
  {"content": "Step 9: ユーザーの「承認」を取得", "activeForm": "fix-plan.mdの承認を取得中", "status": "pending"},
  {"content": "Step 10: tasklist.md 作成", "activeForm": "tasklist.mdを作成中", "status": "pending"},
  {"content": "Step 11: サマリーを表示", "activeForm": "サマリーを表示中", "status": "pending"},
  {"content": "Step 12: フィックスブランチ作成", "activeForm": "フィックスブランチを作成中", "status": "pending"},
  {"content": "Step 12: ステアリングドキュメントをコミット", "activeForm": "ステアリングドキュメントをコミット中", "status": "pending"},
  {"content": "Step 12: 完了メッセージを表示", "activeForm": "完了メッセージを表示中", "status": "pending"}
]
```
