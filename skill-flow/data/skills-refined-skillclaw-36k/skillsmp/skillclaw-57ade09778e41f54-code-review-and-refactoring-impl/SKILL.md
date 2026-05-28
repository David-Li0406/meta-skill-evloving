---
name: code-review-and-refactoring-implementation
description: Use this skill when you need to manage the code review and refactoring processes effectively, ensuring high-quality code through structured planning, execution, and closure.
---

# Code Review and Refactoring Implementation (Orchestrator)

このスキルは、コードレビューとリファクタリングのプロセスを安全かつ確実に完遂するためのオーケストレーションスキルです。`task-management` スキルのフレームワークを採用し、建設的な対話と高品質なコード改善を実現します。

## 役割定義 (Role Definition)
あなたは **Code Quality Lead** です。レビュアーからのフィードバックを基に、システムをより洗練された状態へと引き上げる「橋渡し役」としての役割を担います。

## 前提 (Prerequisites)
- PRに対してコードレビューの指摘（Change Requests / Comments）が存在し、リファクタリング対象のコードに動作を保証するための既存テストが存在すること。

## 手順 (Procedure)

### 1. 計画フェーズ (State 1: Planning)
- **Action:**
  1. タスクマネジメントを開始する。
     `activate_skill{name: "task-management"}`
  2. 指摘を分析し、SMART目標を設定する。
     `activate_skill{name: "code-review-analysis"}`
     `activate_skill{name: "objective-setting"}`
     *   各コメントを「修正必須（Must Fix）」「議論・質問（Discuss）」「提案（Suggestion）」に分類し、対応方針を決定する。
  3. Todoを作成・登録する。
     `activate_skill{name: "todo-management"}`
     *   指摘対応の実行計画を `.gemini/todo.md` に作成する。
     *   ブランチ切り替え、個別の指摘に対する修正タスク、回答作成タスク、最終確認、Push/Submitまでを論理的な順序でリスト化する。

### 2. 実行フェーズ (State 2: Execution)
- **Action:**
  - `task-management` の実行サイクルに従い、Todoを順次消化する。
  - **修正:**
    `activate_skill{name: "tdd-refactoring"}`
    *   「修正必須」の項目についてコード変更を行う。既存テストを壊さないよう注意し、必要であればテストを追加・修正する。
  - **回答:**
    *   「議論」「提案」に対して、技術的根拠に基づいた回答を作成する。感情的な反論は避け、建設的な議論を心がける。

### 3. 完了フェーズ (State 3: Closing)
- **Action:**
  - `task-management` の完了フローに従う。
  - **Audit:**
    `activate_skill{name: "tdd-audit"}`
    *   全ての指摘への対応（修正or回答）が漏れなく行われているか、修正後のコードが品質基準（Lint/Test）を満たしているかを確認する。
  - **Retrospective:**
    `activate_skill{name: "retrospective"}`
    *   今回のレビュー指摘から得られた学び（コーディング規約の曖昧さ、設計の改善点など）を整理し、チーム全体へのフィードバックとして記録する。

## 完了条件 (Definition of Done)
- 全ての指摘に対して「修正」または「回答」が完了していること。
- 修正後のコードが全てのテスト・Linterを通過していること。
- PRが更新され、レビュアーへの通知が完了していること。
- 外部からの振る舞いが変わっていないことが全てのテストで証明されていること。
- コード品質（可読性、保守性、テスト容易性）が目標通り向上していること。
- PRが作成され、振り返りまで完了していること。