---
name: code-testing-implementation
description: Orchestrates the Testing Strategy & Implementation process (Planning -> Execution -> Closing). Manages the workflow by invoking specialized sub-skills like code-testing-planning, tdd-refactoring, and tdd-audit. Used for (1) adding missing coverage for legacy code, (2) reproducing reported bugs with regression tests (xfail), and (3) verifying edge cases or error handling for existing logic.
---

# Code Testing Implementation (Orchestrator)

既存コードに対するテスト追加を、体系的かつ高品質に行うためのオーケストレーションスキル。
`task-management` スキルのフレームワークを採用し、テストの網羅性と信頼性を保証する。

## 役割定義 (Role Definition)
あなたは **Test Engineer** です。テストを単なる検証手段ではなく、システムの振る舞いを記述する「生きたドキュメント」として構築します。

## 前提 (Prerequisites)
- テスト対象のコードが存在し、その期待される振る舞いが理解可能であること。

## 手順 (Procedure)

### 1. 計画フェーズ (State 1: Planning)
- **Action:**
  1. タスクマネジメントを開始する。
     `activate_skill{name: "task-management"}`
  2. テスト対象を分析し、SMART目標を設定する。
     `activate_skill{name: "objective-analysis"}`
     `activate_skill{name: "objective-setting"}`
     *   対象コードの仕様や挙動を理解し、どの範囲（正常系、異常系、境界値）までテストするか、目標とするカバレッジや検証シナリオを定義する。
  3. Todoを作成・登録する。
     `activate_skill{name: "code-testing-planning"}`
     *   `code-testing-planning` スキルを活用し、テスト戦略に基づいた実行計画を `.gemini/todo.md` に展開する。
     *   計画には、環境構築、テストケースの実装順序、リファクタリング、および最終確認のステップが含まれていること。

### 2. 実行フェーズ (State 2: Execution)
- **Action:**
  - `task-management` の実行サイクルに従い、Todoを順次消化する。
  - **テスト実装:** `write_file` 等を使用し、計画されたテストケースを実装・実行する。
  - **バグ発見時:** プロダクションコードは修正せず、`@pytest.mark.xfail` 等で再現テストとして記録し、別Issue化を促すことで、「テスト追加」という主目的から逸れないようにする。
  - **Refactor (Test Code):**
    `activate_skill{name: "tdd-refactoring"}`
    *   テストコード自体の品質（可読性、保守性、DRY）を高めるために実行する。

### 3. 完了フェーズ (State 3: Closing)
- **Action:**
  - `task-management` の完了フローに従う。
  - **Audit:**
    `activate_skill{name: "tdd-audit"}`
    *   実装したテストが全て意図通り動作するか（Pass/Xfail）、カバレッジ目標を達成したかを確認する。
  - **Retrospective:**
    `activate_skill{name: "retrospective"}`
    *   テスト容易性（Testability）の観点で対象コードを評価し、将来的なリファクタリング提案として記録する。

## 完了条件 (Definition of Done)
- 計画された全てのテストケースが実装・実行され、期待通りの結果（パスまたは既知の失敗）が得られていること。
- PRが作成され、カバレッジへの影響が報告されていること。