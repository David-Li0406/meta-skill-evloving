---
name: code-refactoring-implementation
description: Orchestrates the entire Code Refactoring process (Planning -> Execution -> Closing). Manages the workflow by invoking specialized sub-skills like code-refactoring-planning, tdd-refactoring, and tdd-audit. Used for (1) repaying technical debt (e.g., extracting logic from fat controllers), (2) improving architectural compliance (e.g., enforcing dependency rules), and (3) preparing legacy code for new features (e.g., decoupling).
---

# Code Refactoring Implementation (Orchestrator)

大規模なリファクタリングタスクを、安全かつ確実に完遂するためのオーケストレーションスキル。
`task-management` スキルのフレームワークを採用し、外部からの振る舞いを変えずに内部構造を改善する。

## 役割定義 (Role Definition)
あなたは **Refactoring Lead** です。技術的負債を解消し、システムの柔軟性と保守性を高める「彫刻家」としての役割を担います。

## 前提 (Prerequisites)
- リファクタリング対象のコードに、動作を保証するための既存テスト（または追加したガードレールテスト）が存在すること。

## 手順 (Procedure)

### 1. 計画フェーズ (State 1: Planning)
- **Action:**
  1. タスクマネジメントを開始する。
     `activate_skill{name: "task-management"}`
  2. コードの匂いを分析し、SMART目標（As-Is/To-Be）を設定する。
     `activate_skill{name: "objective-analysis"}`
     `activate_skill{name: "objective-setting"}`
     *   対象コードの問題点（複雑度、結合度、重複など）を特定し、リファクタリング後の理想的な状態（To-Be）を定義する。
  3. Todoを作成・登録する。
     `activate_skill{name: "code-refactoring-planning"}`
     *   `code-refactoring-planning` スキルを活用し、安全なリファクタリング手順を `.gemini/todo.md` に展開する。
     *   計画は「小さなステップ」の連続で構成し、各ステップでテストがパスすることを確認できる粒度にする。ガードレールテストの追加もここに含める。

### 2. 実行フェーズ (State 2: Execution)
- **Action:**
  - `task-management` の実行サイクルに従い、Todoを順次消化する。
  - **Refactorサイクル:**
    `activate_skill{name: "tdd-refactoring"}`
    *   実際のコード変更を行う。このスキル内で `pytest` を頻繁に実行し、振る舞いが変わっていないことを常に保証しながら進める。
  - **Compliance Check:**
    *   変更後の構造がプロジェクトのアーキテクチャ原則（依存方向など）に違反していないかを確認する。

### 3. 完了フェーズ (State 3: Closing)
- **Action:**
  - `task-management` の完了フローに従う。
  - **Audit:**
    `activate_skill{name: "tdd-audit"}`
    *   最終的なコード品質、テストパス、およびリグレッションがないことを確認する。
  - **Retrospective:**
    `activate_skill{name: "retrospective"}`
    *   リファクタリングによる効果（可読性向上、複雑度低下など）を評価し、今後のメンテナンス指針としての知見を残す。

## 完了条件 (Definition of Done)
- 外部からの振る舞いが変わっていないことが全てのテストで証明されていること。
- コード品質（可読性、保守性、テスト容易性）が目標通り向上していること。
- PRが作成され、振り返りまで完了していること。