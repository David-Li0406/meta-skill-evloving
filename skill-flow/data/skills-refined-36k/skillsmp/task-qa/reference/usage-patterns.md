# 利用パターン（5パターン）

task-qa Skillの利用方法パターン集。

---

## パターン1: task-execからの呼び出し（標準ワークフロー）

```
ユーザー: task-exec #123 1.1
  → starter → executer → reviewer → qa
                                      ↓
                            task-qa.md（ラッパー）→ SKILL.md
                                      ↓
                            結果JSON返却 → task-qa.md完了報告生成
```

**重要**: 既存フォーマット（`## 🧪 品質保証フェーズ完了`）を維持

---

## パターン2: 独立使用（Model-Invoked）

**トリガーワード**: "QAを実行"、"品質保証を実施"、"テストを確認"

```
ユーザー: "docs/specs/tasks/user-auth/ のQAを実行して"
  → Skill自動起動 → QA実行 → 結果報告
```

---

## パターン3: CLI明示的呼び出し（将来機能）

```bash
claude skill task-qa --spec-dir docs/specs/tasks/user-auth/
```

---

## パターン4: CI/CD統合

GitHub Actionsで自動QA実行（将来実装）

---

## パターン5: 手動QAレビュー

```
ユーザー: "タスク1.1のQA結果を見せて"
  → qa-tests/phase1/1-1.md読み込み → 結果サマリー表示
```
