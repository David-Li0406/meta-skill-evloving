---
name: todo-management
description: Skill for breaking down goals into atomic, verifiable steps and managing them in .gemini/todo.md. Used when (1) creating a detailed step-by-step execution plan, (2) tracking progress of multi-step operations to prevent errors, and (3) persisting context to resume work accurately.
---

# Todo管理 (Todo Management)

設定された目標を確実に達成するため、タスクを**最小単位（Atomic Steps）**に分解し、`.gemini/todo.md` で管理する。

## タスク分解フレームワーク (Atomic Decomposition)

目標を「一足飛び」に達成しようとせず、以下の基準で「確実な一歩」に分解する。

1. **調査と理解 (Understand):** まず現状を把握するステップ。
2. **計画と準備 (Plan):** 変更方針を固め、テストケースを準備するステップ。
3. **最小実装 (Implement):** 変更を小さく、動作確認可能な単位で適用するステップ。
4. **検証 (Verify):** 変更が正しいか確認するステップ。

**分解の基準:**
- **最終ステップがGoalの達成となるように、最初から最後まで完全に分解しきる。**
- 1つのステップは**「1つの実行アクション」と「1つの検証アクション」のペア**で構成する。
- 抽象的なタスク（「○○機能を実装する」）は禁止。具体的なコマンド単位まで砕く。

## 手順 (Procedures)

1. **情報収集 (Gather Information):**
   - ユーザーの発言、チャット履歴、Issue記述全文を収集する。
   - **必ずその時点の全てのSSOT（`docs/`、`reqs/`、最新コード）をチェックし**、現状を正確に把握する。
   - **現状と目標のギャップを明確にし**、何をする必要があるかを特定する。

2. **Todoの作成・更新:**
   収集した情報に基づき、`.gemini/todo.md` を作成または編集し、設定された目標とタスクの進捗状況を更新する。

3. **リスク評価 (Risk Assessment):**
   作成した `todo.md` を以下のチェックリストで評価する。
   **問題がある場合は、「具体的かつ詳細な改善提案」を作成し、即座に `todo.md` を修正する。**

   - [ ] **価値 (Value):** ユーザーやビジネスの価値向上に繋がるか？無駄な機能を作っていないか？
   - [ ] **ユーザビリティ (Usability):** 利用者にとって使いやすく、理解しやすいか？
   - [ ] **実現可能性 (Feasibility):** 技術的・時間的制約の中で現実的に完了できるか？
   - [ ] **ビジネス生存性 (Viability):** 法務・コスト・セキュリティ上の致命的問題はないか？

4. **レビューと洗練 (Review & Refine):**
   作成したTodoリストに対して `todo-review` スキルを実行し、計画の品質をチェックする。
   `activate_skill{name: "todo-review"}`
   **`todo-review` による指摘事項が完全になくなるまで**、手順2（Todoの修正）からのプロセスを繰り返す。

5. **完了:**
   レビューを通過した完全な実行計画（`.gemini/todo.md`）が完成した時点で本スキルの完了とする。

## ファイル形式 (.gemini/todo.md)

※以下は記述例（テンプレート）です。実際の内容は目標に合わせて作成してください。

```markdown
# Goal: <objective-settingで定義した目標>

## Tasks
<!-- Goal達成までの全ステップを記述する -->
- [ ] **Step 1:** <具体的な作業名>
  - Action: <実行するツールコマンド>
  - Verify: <成功を確認するツールコマンド>
- [ ] **Step 2:** ...
  - Action: ...
  - Verify: ...
...
- [ ] **Final Step:** <Goalの達成確認>
```

## ステータス定義
- `[ ]`: 未実行
- `[x]`: 完了
- `[!]`: 失敗（要分析・再計画）
- `[-]`: スキップ