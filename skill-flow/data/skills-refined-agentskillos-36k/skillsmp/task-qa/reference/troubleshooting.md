# トラブルシューティング（6ケース）

QA実行時によくある問題と対処法。

---

## 5.1 Playwright MCP 接続失敗

**症状**: `Error: Failed to connect to Playwright MCP server`

**対処法**:
1. `claude mcp status` でステータス確認
2. `claude mcp restart playwright` で再起動
3. ポート確認: `lsof -i :3000`

---

## 5.2 requirements.md 不在

**症状**: `Error: requirements.md not found`

**対処法**:
1. 仕様書ディレクトリパスを確認
2. 不在の場合はspec-requirements-generatorで作成

**失敗分類**: D（環境問題）またはB（要件未定義）

---

## 5.3 qa-tests/ 書き込み権限エラー

**症状**: `Error: EACCES: permission denied`

**対処法**:
1. `ls -la {spec_dir}/qa-tests/` で権限確認
2. `chmod -R u+w {spec_dir}/qa-tests/` で権限変更
3. 不在時は `mkdir -p {spec_dir}/qa-tests/phase{N}/evidence/`

---

## 5.4 必須自動テストの失敗

**判定**: **必ずFAILURE**（PARTIAL禁止）

**対処法**: 失敗原因を分類（A/B/C/D）し適切な戻し先に差し戻し

---

## 5.5 タイムアウト問題

**症状**: `Timeout 30000ms exceeded`

**対処法**: Playwrightタイムアウトを60秒に延長

**失敗分類**: D（一時的遅延）またはC（パフォーマンス設計ミス）

---

## 5.6 AC抽出エラー

**症状**: `Warning: No Integration or E2E acceptance criteria found`

**対処法**:
1. requirements.mdで「検証レベル: Integration/E2E」の記載を確認
2. 必要な場合はB（要件齟齬）として差し戻し
