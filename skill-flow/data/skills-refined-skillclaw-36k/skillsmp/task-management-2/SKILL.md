---
name: task-management
description: Framework for systematic task execution using a state machine (Planning, Execution, Closing). Used for (1) complex feature implementation requiring multiple steps, (2) root-cause analysis and bug fixing, and (3) creation and organization of comprehensive design documents.
---

# タスクマネジメントフレームワーク (Task Management Framework)

タスクを確実に遂行するための状態遷移モデル。現在の自分の状態（State）を意識して行動する。

## State 1: Planning (計画)

- **いつ:** タスク開始時、または予期せぬエラーで計画が破綻した時。
- **Action:**
  1. **目標設定 (Goal Setting):** `objective-setting` スキルを使用して、具体的かつ実行可能な目標（SMART目標）を定義する。
  2. **Todo作成 (Todo Management):** `todo-management` スキルを使用して、目的達成に必要な原子的な手順を `.gemini/todo.md` に作成する。
     ※ リスク評価とレビューは `todo-management` スキル内で実施されるため、完了時点で高品質な計画が保証される。

## State 2: Execution (実行)

- **いつ:** Todoリスト（`.gemini/todo.md`）があり、内容について一切の懸念がなくなったとき。
- **Action:**
  1. **実行と適応:** `.gemini/todo.md` に基づき、タスクを順次実行する。
     - 各ステップ完了ごとに `.gemini/todo.md` のステータスを更新し、進捗を可視化し続ける。
     - **失敗時:** すぐに修正せず、ステータスを `[!]` とし、直ちに次のTodoへ進む。前提が崩れた後続タスクは `[-]` とする。

## State 3: Closing (完了・振り返り)

- **いつ:** 全てのTodoが `[x]` または `[-]` になった時。
- **Action:**
  1. **振り返り (Retrospective):** `retrospective` スキルを使用して、成果と課題を振り返り、次のアクションを決定する。
  2. **完了処理 (Cleanup):**
     - 作業が完了した `.gemini/todo.md` を整理または削除し、コンテキストをクリアする。

  3. **次のサイクルへ:**
     - 必要に応じてState 1へ戻る。
