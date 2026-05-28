# {機能名} - プロセス進捗

**コマンド**: /modify-feature
**開始日時**: {YYYY-MM-DD HH:mm}

---

## Phase 1: 変更要求確認

Step 1: 初期入力の受け取り
Step 2: 初期入力の解釈と確認
Step 3: ステアリングディレクトリ作成
Step 4: 後方互換性と成功指標の確認
Step 5: change-request.md レビュー・承認

---

## Phase 2: 影響分析

Step 6: コードベース調査（file-finder エージェント）
Step 7: 影響範囲分析（impact-analyzer エージェント）、impact-analysis.md 作成
Step 8: impact-analysis.md レビュー・承認

---

## Phase 3: 実装計画

Step 9: 変更タイプ確認、tasklist.md 作成
Step 10: 最終確認
Step 11: ブランチ作成・コミット

---

## 生成されたファイル

- change-request.md（Phase 1 完了時）
- impact-analysis.md（Phase 2 完了時）
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
  {"content": "Step 3: change-request.md 作成・記入", "activeForm": "change-request.mdを作成中", "status": "pending"},
  {"content": "Step 4: 後方互換性を確認", "activeForm": "後方互換性を確認中", "status": "pending"},
  {"content": "Step 4: 成功指標を確認", "activeForm": "成功指標を確認中", "status": "pending"},
  {"content": "Step 4: change-request.md 更新", "activeForm": "change-request.mdを更新中", "status": "pending"},
  {"content": "Step 5: change-request.md をユーザーに提示", "activeForm": "change-request.mdのレビューを依頼中", "status": "pending"},
  {"content": "Step 5: ユーザーの「承認」を取得", "activeForm": "change-request.mdの承認を取得中", "status": "pending"},
  {"content": "Step 6: file-finder エージェント実行", "activeForm": "file-finderでコードベースを調査中", "status": "pending"},
  {"content": "Step 6: 調査結果をユーザーに報告", "activeForm": "調査結果を報告中", "status": "pending"},
  {"content": "Step 7: impact-analyzer エージェント実行", "activeForm": "impact-analyzerで影響範囲を分析中", "status": "pending"},
  {"content": "Step 7: impact-analysis.md 作成", "activeForm": "impact-analysis.mdを作成中", "status": "pending"},
  {"content": "Step 7: 「影響を受けるコンポーネント」セクション記入", "activeForm": "影響コンポーネントを記入中", "status": "pending"},
  {"content": "Step 7: 「リスク評価」セクション記入", "activeForm": "リスク評価を記入中", "status": "pending"},
  {"content": "Step 7: 「テスト戦略」セクション記入", "activeForm": "テスト戦略を記入中", "status": "pending"},
  {"content": "Step 8: impact-analysis.md をユーザーに提示", "activeForm": "impact-analysis.mdのレビューを依頼中", "status": "pending"},
  {"content": "Step 8: ユーザーの「承認」を取得", "activeForm": "impact-analysis.mdの承認を取得中", "status": "pending"},
  {"content": "Step 9: 変更タイプ（A/B/C/D）を確認", "activeForm": "変更タイプを確認中", "status": "pending"},
  {"content": "Step 9: tasklist.md 作成", "activeForm": "tasklist.mdを作成中", "status": "pending"},
  {"content": "Step 10: サマリーを表示", "activeForm": "サマリーを表示中", "status": "pending"},
  {"content": "Step 11: モディファイブランチ作成", "activeForm": "モディファイブランチを作成中", "status": "pending"},
  {"content": "Step 11: ステアリングドキュメントをコミット", "activeForm": "ステアリングドキュメントをコミット中", "status": "pending"},
  {"content": "Step 11: 完了メッセージを表示", "activeForm": "完了メッセージを表示中", "status": "pending"}
]
```
