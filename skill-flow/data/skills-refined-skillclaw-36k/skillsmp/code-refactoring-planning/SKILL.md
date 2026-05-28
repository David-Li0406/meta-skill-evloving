---
name: code-refactoring-planning
description: Analyzes code smells and architectural violations to formulate a concrete Refactoring Plan. Used for (1) identifying technical debt, (2) defining As-Is vs To-Be states, and (3) planning safe, atomic refactoring steps.
---

# Code Refactoring Planning

このスキルは、既存コードのリファクタリングを行う前に「何を」「なぜ」「どのように」改善するかを明確にし、破壊的な変更やデグレードを防ぐための計画策定を目的とします。

## 役割定義 (Role Definition)
あなたは **Refactoring Architect** です。コードの匂いやアーキテクチャ違反を特定し、SSOT（あるべき姿）に適合させるための安全な移行計画を立てます。

## 前提 (Prerequisites)
- 既存スキル `active-reconnaissance`, `ssot-verification`, `todo-management` が利用可能であること。
- リファクタリング対象のコードまたは課題が特定されていること。

## 手順 (Procedure)

### 1. 能動的偵察 (Active Reconnaissance)
- **Action:**
  - `todo-management` スキルをアクティベートする。
    `activate_skill{name: "todo-management"}`
  - `active-reconnaissance` スキルを活用し、対象コードの現状（Reality）と関連するSSOT（Intent）を調査する。
    `activate_skill{name: "active-reconnaissance"}`
  - **構造分析:**
    - `read_file` でコードの匂い (Code Smells)、重複、複雑度を確認する。
    - アーキテクチャ違反（依存方向の逆転、責務の混在）を特定する。
  - **リスク評価:**
    - 対象コードの規模（行数）、複雑度（ネスト）、テストカバレッジを確認する。
    - `pytest` を実行し、現状のテストが全てパスすること（Safety Net）を確認する。**失敗する状態でのリファクタリングは禁止。**

### 2. Refactoring Plan の策定
- **Action:**
  - 収集した情報に基づき、以下のテンプレートを用いて具体的な計画を作成する。
  - **Checklist:**
    - [ ] **As-Is:** 現状の問題点は具体的か？（推測ではなく事実か？）
    - [ ] **To-Be:** 目指す状態は SSOT (ADR/Spec) に準拠しているか？
    - [ ] **Safety:** 変更を安全に行うための戦略（Options）は検討されたか？

### 3. Todo分解 (via todo-management)
- **Action:**
  - `todo-management` の「タスク分解フレームワーク」に従い、策定した「Refactoring Plan」を `.gemini/todo.md` の形式に変換する。
  - **マッピングルール:**
    - **Task Name:** [Refactor] + 簡潔な作業名
    - **Action:** 具体的なツール操作（`replace`, `write_file` 等）と、**その根拠となるドキュメントの参照**。
    - **Verify:** 成功を判定するコマンド（`pytest`, `mypy` 等）と、期待される結果。

### 4. レビューと洗練 (Review & Refinement)
- **Action:**
  - 以下の「4大リスク」の観点でPlan全体を自己評価し、懸念があれば計画を修正する。
    - [ ] **価値 (Value):** 本当にこのリファクタリングで保守性や可読性が向上するか？（自己満足ではないか？）
    - [ ] **ユーザビリティ (Usability):** 外部インターフェースへの影響はないか？
    - [ ] **実現可能性 (Feasibility):** 計画された時間と技術で完遂できるか？既存テスト修正が過大ではないか？
    - [ ] **ビジネス生存性 (Viability):** リスク（デグレード）に見合うリターンはあるか？
  - `todo-review` を実行し、計画が原子レベルまで砕かれているか確認する。
    `activate_skill{name: "todo-review"}`
  - **修正フロー:**
    - **方針・設計レベルの不備:** Step 2 (Refactoring Plan の策定) に戻る。
    - **タスク粒度・記述の不備:** Step 3 (Todo分解) に戻る。

## アウトプット形式 (Output Template)

```markdown
## Refactoring Plan: [Target Module/Path]
- **Goal:** [SMART目標]
- **Context:** [参照ドキュメント一覧]

### Analysis
- **As-Is:** [現状の問題点: Code Smells, Architecture Violations]
- **To-Be:** [あるべき姿: SSOT/ADR準拠]
- **Gap:** [解決すべき乖離]

### Strategy
- **Options:**
    - **Option A (Ideal):** [抜本的な修正案]
    - **Option B (Pragmatic):** [現実的・段階的な修正案]
- **Selection:** [選択した案] (理由: ...)

### Steps (High Level)
1. [Step 1]
2. [Step 2]
...

- **Risks:** [4 Big Risks + テスト修正の見積もり]
```

---
※ 詳細な実行ステップは上記マッピングルールに従い `.gemini/todo.md` に展開されました。

## 完了条件 (Definition of Done)
- ユーザーに Refactoring Plan を提示し、合意を得ていること。
- `todo-management` によって、実行フェーズの具体的かつ原子的なステップが `.gemini/todo.md` に定義されていること。
