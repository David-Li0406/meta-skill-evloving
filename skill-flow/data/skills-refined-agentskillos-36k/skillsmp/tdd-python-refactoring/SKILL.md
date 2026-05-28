---
name: tdd-python-refactoring
description: Replaces the refactoring work of improving quality and maintainability of passed Python code without changing behavior. Typical use cases: (1) Enhancing type safety by eliminating Any types and tightening type hints (Mypy compliance), (2) Optimizing readability by introducing PEP 8 compliance or Pythonic idioms, (3) Resolving circular imports or redefining module responsibilities for structural improvement.
---

# TDD Refactoring Cycle (Python)

`tdd-python-drafting` によって作成された「動くPythonコード（Green）」に対し、品質基準（SSOT, PEP 8, Type Safety）を満たすまで **「分析 → 改善 → 検証」** のサイクルを反復するスキル。

## 役割定義 (Role Definition)
あなたは **Python Code Craftsman** です。動くコード（Working Code）を、Pythonicで維持可能なコード（Clean Code）へと昇華させます。

## 前提 (Prerequisites)
- テストがパスしている状態（Green）であること。

## 手順 (Procedure)

### 1. 現状分析 (Analyze)

- **Input:**
  - 現在のコード（Product & Test）。
  - `activate_skill{name: "python-verification"}` の出力 (Ruff, Mypy)。
  - プロジェクトの規約（Coding Guidelines, SSOT）。

- **Action:**
  - **Static Analysis:** `python-verification` を実行し、Linterのエラーや型ヒントの欠落を特定する。
  - **Code Smell Detection:** `activate_skill{name: "active-reconnaissance"}` を使用し、非Pythonicな記述、重複、複雑すぎる関数を特定する。
  - **Gap Analysis:** 「動くコード」と「あるべき姿（Clean Architecture/SSOT）」のギャップを分析する。

### 2. 改善 (Refactor)

- **Action:**
  - **振る舞いを変えずに** 構造のみを変更する（ボーイスカウト・ルール）。
  - `replace` や `write_file` を使用してコードを修正する。
  - **Priorities:**
    1.  **Type Safety:** `Any` 型を排除し、具体的な型定義を行う。
    2.  **Readability:** PEP 8 に準拠し、リスト内包表記などを適切に使用して可読性を高める。
    3.  **Structure:** 循環インポートを回避し、モジュールの責務を明確にする。

### 3. 検証 (Verify)

- **Action:**
  - `activate_skill{name: "python-verification"}` を実行し、**テストが引き続きGreenであること**を確認しつつ、静的解析のエラーが減少/解消したことを確認する。

### 4. 自己レビューと反復 (Self-Review & Iterate)

以下のチェックリストに基づき、さらなる改善が必要か判断する。

- **Checklist:**
  - [ ] **Pythonic:** イディオム（`with` 文, ジェネレータ等）を適切に使っているか？
  - [ ] **Type Hints:** 全ての関数の引数と戻り値に型ヒントがあるか？ (`Mypy` clean)
  - [ ] **Docstrings:** 公開関数/クラスに Google Style の Docstring があるか？
  - [ ] **Complexity:** 複雑度（Cyclomatic Complexity）が高すぎないか？

- **Decision:**
  - 改善点があれば **Step 1** に戻る。
  - 全てクリアしていれば終了する。

## 完了条件 (Definition of Done)
- `python-verification` (Ruff, Mypy, Pytest) の警告がゼロである。
- コードが Pythonic であり、SSOTに準拠している。
