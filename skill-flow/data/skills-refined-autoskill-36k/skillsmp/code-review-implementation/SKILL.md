---
name: code-review-implementation
description: Orchestrates the Code Review process (Analysis -> Fix -> Reply/Close). Manages the workflow by invoking specialized sub-skills like code-review-analysis, tdd-refactoring, and tdd-audit. Used for (1) addressing change requests from reviewers (fixes), (2) providing technical explanations or justifications for design choices (replies), and (3) improving code quality based on feedback before merging.
---

# Code Review Implementation (Orchestrator)

コードレビュー指摘への対応を、感情論ではなく技術的プロセスとして確実に完遂するためのオーケストレーションスキル。
`task-management` スキルのフレームワークを採用し、建設的な対話と高品質な修正を実現する。

## 役割定義 (Role Definition)
あなたは **Review Responder** です。レビュアーからのフィードバックを糧に、システムをより洗練された状態へと引き上げる「橋渡し役」を担います。

## 前提 (Prerequisites)
- PRに対してコードレビューの指摘（Change Requests / Comments）が存在すること。

## 手順 (Procedure)

### 1. 計画フェーズ (State 1: Planning)
- **Action:**
  1. タスクマネジメントを開始する。
     `activate_skill{name: "task-management"}`
  2. 指摘を分析し、SMART目標を設定する。
     `activate_skill{name: "code-review-analysis"}`
     *   各コメントを「修正必須（Must Fix）」「議論・質問（Discuss）」「提案（Suggestion）」に分類し、対応方針を決定する。
     `activate_skill{name: "objective-setting"}`
     *   全ての指摘に対して「修正」または「回答」を行うことを目標とする。
  3. Todoを作成・登録する。
     `activate_skill{name: "todo-management"}`
     *   指摘対応の実行計画を `.gemini/todo.md` に作成する。
     *   ブランチ切り替え、個別の指摘に対する修正タスク、回答作成タスク、最終確認、そしてPush/Submitまでを論理的な順序でリスト化する。

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