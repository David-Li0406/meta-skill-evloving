---
name: testing-strategy-and-quality-audit
description: Use this skill when you need to develop a comprehensive testing strategy and perform quality audits on test suites.
---

# Testing Strategy and Quality Audit

## トリガー

- テスト計画が必要な時
- テストスイートのレビュー依頼
- テスト実行時間が長い
- Flaky testが発生
- 新規参画者のオンボーディング

---

## リスクベーステスト配分

| 層 | 件数 | 目的 |
|----|------|------|
| E2E | 2-5 | クリティカルパス検証 |
| Integration | 3-8 | コンポーネント連携検証 |
| Unit | 5-15 | ロジック単体検証 |

**原則**: E2E優先。Unit過多は設計問題のサイン。

---

## 監査プロセス

```text
1. 全テスト一覧化
2. Usefulness Score算出
3. カテゴリ分類
4. 削除候補特定
5. 改善提案
```

---

## Usefulness Score評価

### 計算式

```text
Score = Impact(1-5) × Probability(1-5)
```

### 判定基準

| スコア | 判定 | アクション |
|--------|------|------------|
| ≥20 | CRITICAL | 必須維持、最優先修正 |
| 15-19 | KEEP | 維持 |
| 10-14 | REVIEW | 再検討、統合検討 |
| <10 | REMOVE | 削除候補 |

### Impact基準

| 値 | 影響範囲 |
|----|----------|
| 5 | Money/Security/Data損失 |
| 4 | 主要機能停止 |
| 3 | UX劣化 |
| 2 | 軽微な不具合 |
| 1 | 見た目のみ |

### Probability基準

| 値 | 発生頻度 |
|----|----------|
| 5 | 毎日発生しうる |
| 4 | 週1以上 |
| 3 | 月1以上 |
| 2 | 年1以上 |
| 1 | ほぼ発生しない |

---

## 監査チェックリスト

### 1. ビジネス価値監査

- [ ] テストはビジネスロジックを検証しているか?
- [ ] フレームワーク機能のテストではないか?
- [ ] ユーザー価値に直結するか?

### 2. 重複監査

- [ ] 同じ振る舞いを複数テストしていないか?
- [ ] E2Eで担保されているのにUnitでも書いていないか?
- [ ] 統合可能なテストがないか?

### 3. 信頼性監査

- [ ] Flaky testはないか?
- [ ] 環境依存テストはないか?
- [ ] 実行順序依存はないか?

### 4. 保守性監査

- [ ] テスト名から意図が分かるか?
- [ ] 失敗時の原因特定が容易か?
- [ ] テストデータは明確か?

### 5. パフォーマンス監査

- [ ] 実行時間は許容範囲か?
- [ ] 不要なsetup/teardownはないか?
- [ ] 並列実行可能か?

---

## 削除対象テスト

- フレームワーク機能のテスト
- ビジネスロジック無関係
- 重複テスト
- Usefulness Score < 10

---

## 監査レポートフォーマット

```markdown
# テスト品質監査レポート

## サマリー

| 指標 | 値 |
|------|-----|
| 総テスト数 | X |
| CRITICAL (≥20) | X |
| KEEP (15-19) | X |
| REVIEW (10-14) | X |
| REMOVE (<10) | X |

## 削除推奨

| テスト | スコア | 理由 |
|--------|--------|------|
| test_xxx | 6 | フレームワークテスト |

## 改善推奨

| テスト | 現スコア | 改善案 |
|--------|----------|--------|
| test_yyy | 12 | 境界値追加で15+ |

## カバレッジギャップ

| 領域 | 現状 | 必要 |
|------|------|------|
| Money | 18 | 20+ |
```

---

## 自動監査ルール

```yaml
# .github/workflows/test-audit.yml
rules:
  - name: no-framework-tests
    pattern: "expect.*toBeInTheDocument|toBeDefined"
    action: warn

  - name: no-implementation-details
    pattern: "toHaveBeenCalledWith.*internal"
    action: warn

  - name: no-flaky-tests
    pattern: "retry|flaky|skip"
    action: error
```

---

## 禁止事項

- ❌ 監査なしのテスト追加
- ❌ スコア未記載のテスト
- ❌ 削除候補の放置
- ❌ Flakyテストの許容
- ❌ フレームワークテストの維持
- ❌ テストなしリリース
- ❌ Usefulness未評価のテスト追加
- ❌ E2E 2件未満/エンドポイント

---

## 品質ゲート

| 指標 | 閾値 |
|------|------|
| REMOVE比率 | <5% |
| Flaky率 | 0% |
| 平均スコア | ≥15 |
| カバレッジギャップ | 0 |