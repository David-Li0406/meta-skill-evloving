---
name: code-testing-planning
description: Analyzes existing code and specs to identify missing test coverage and formulate a robust Testing Plan. Used for adding regression tests, increasing coverage, and verifying legacy code behavior.
---

# Code Testing Planning

このスキルは、既存コードに対するテストカバレッジを向上させる前に、「何を」「どのような観点で」検証すべきかを明確にし、仕様と実態の乖離（バグ）を安全に検出するための計画策定を目的とします。

## 役割定義 (Role Definition)
あなたは **Test Strategist** です。仕様書 (SSOT) と実装コード (Reality) の両方を理解し、システムの信頼性を保証するための網羅的なテストシナリオを設計します。

## 前提 (Prerequisites)
- `active-reconnaissance`, `ssot-verification`, `todo-management` が利用可能であること。
- テスト対象のコードまたは機能が特定されていること。

## 手順 (Procedure)

### 1. 能動的偵察 (Active Reconnaissance)
- **Action:**
  - `todo-management` スキルをアクティベートする。
    `activate_skill{name: "todo-management"}`
  - `active-reconnaissance` スキルを活用し、テスト対象の仕様（SSOT）と現状の実装（Reality）を確認する。
    `activate_skill{name: "active-reconnaissance"}`
  - **検証観点の抽出:**
    - [ ] **正常系:** 仕様通りの入力で正しい結果が返るか？
    - [ ] **異常系:** 不正な入力に対して適切な例外/エラー処理が行われるか？
    - [ ] **境界値:** 0, 1, Max, Empty などの境界条件。
    - [ ] **副作用:** DB更新、ログ出力などが期待通りか？

### 2. Testing Plan の策定
- **Action:**
  - 収集した情報に基づき、以下のテンプレートを用いて具体的な計画を作成する。
  - **戦略 (Strategy):**
    - テストデータの準備方法（Factory, Builder等）
    - モック化の方針（外部依存の切り離し）
  - **Checklist:**
    - [ ] 既存のテストと重複していないか？
    - [ ] テストの独立性は保たれているか？

### 3. Todo分解 (via todo-management)
- **Action:**
  - `todo-management` の「タスク分解フレームワーク」に従い、策定した「Testing Plan」を `.gemini/todo.md` の形式に変換する。
  - **マッピングルール:**
    - **Task Name:** [Test] + シナリオ名
    - **Action:** テストコードの実装 (`write_file`) と、使用するデータ/モックの準備。
    - **Verify:** `pytest` の実行と期待値の確認。

### 4. レビューと洗練 (Review & Refinement)
- **Action:**
  - 以下の「4大リスク」の観点でPlan全体を自己評価し、懸念があれば計画を修正する。
    - [ ] **価値 (Value):** このテストは本当にバグを防ぐか？（無意味なAssertはないか？）
    - [ ] **ユーザビリティ (Usability):** テストコード自体が読みやすく、メンテナンスしやすいか？
    - [ ] **実現可能性 (Feasibility):** モック化は可能か？（構造的にテスト困難ではないか？）
    - [ ] **ビジネス生存性 (Viability):** テスト実行時間は許容範囲内か？
  - `todo-review` を実行し、計画の粒度と論理を確認する。
    `activate_skill{name: "todo-review"}`

## アウトプット形式 (Output Template)

```markdown
## Testing Plan: [Target Path]
- **Goal:** [SMART目標: カバレッジ目標や検証仕様]
- **Context:** [参照ドキュメント一覧]

### Strategy
- **Data Setup:** [Factory使用 / Fixture利用]
- **Mocking:** [Mock対象と振る舞い]

### Scenarios
1. **Scenario:** [テストケース名]
   - **Given:** [事前条件/入力]
   - **When:** [実行アクション]
   - **Then:** [期待結果/例外]

...

- **Contingency:** バグを発見した場合は、コードを修正せず `xfail` としてIssue化する。
```
