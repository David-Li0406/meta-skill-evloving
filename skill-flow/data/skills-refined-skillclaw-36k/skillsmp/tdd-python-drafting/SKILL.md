---
name: tdd-python-drafting
description: Replaces the creation of test code based on specifications and the minimal implementation to pass them (Red/Green) in Python projects. Typical use cases: (1) Creating failing tests (Red) based on API or logic specifications, (2) Implementing Python UseCase or Domain Logic layers to pass tests (Green), (3) Constructing pure unit tests isolated from external dependencies using unittest.mock, etc.
---

# TDD Drafting (Python)

詳細仕様書（Spec）と共通実装計画（Plan）に基づき、Pythonプロジェクトにおいて**TDDのRed/Greenサイクル**を実行して機能を実装するスキル。
「機能するPythonコード（Working Code）」を作ることに集中し、品質向上（Refactoring）は `tdd-python-refactoring` に委譲する。

## 役割 (Role)

あなたは **Python TDD Implementer** です。
仕様書をテストケースに変換し、そのテストを通すための最小限の Python 実装（Minimum Viable Implementation）を行います。

## 手順 (Procedure)

### 0. 準備 (Preparation)

実装計画（`docs/implementation/plans/*.md`）を確認し、以下を把握する。
- **Layer Structure:** コードを配置すべきパッケージ/モジュール。
- **Mocking Strategy:** `unittest.mock` や `pytest-mock` の使用方針。
- **Type Definitions:** 使用すべき共通型 (`typing`, `pydantic` 等)。

### 1. Red Phase (Test First)

仕様書（`docs/specs/*.md`）の要件を満たすテストコードを作成する。

- **Action:**
  1.  `tests/` 配下に適切なテストファイルを作成/更新する。
  2.  **正常系（Happy Path）** と **異常系（Error Path/Edge Cases）** のテストケースを記述する。
  3.  **検証:** `python-verification` を実行し、**期待通りに失敗（Red）** することを確認する。
      - `activate_skill{name: "python-verification"}`

### 2. Green Phase (Implementation)

テストをパスさせるための最小限のプロダクトコード（UseCase, Domain Logic）を実装する。

- **Action:**
  1.  `src/` 配下にプロダクトコードファイルを作成/更新する。
  2.  **型ヒント（Type Hints）** を必須とし、ロジックを実装する。
  3.  **検証:** `python-verification` を実行し、**全てパス（Green）** することを確認する。
      - `activate_skill{name: "python-verification"}`

### 3. リファクタリング連携 (Refactoring Connection)

Green状態になった直後、**必ず** `tdd-python-refactoring` を呼び出し、Pythonコードとしての品質を高める。

- **Action:**
  - `activate_skill{name: "tdd-python-refactoring"}` を実行する。

### 4. 監査と納品 (Audit & Delivery)

実装とリファクタリングが完了したら、成果物を監査して納品する。

- **Action:**
  - **Full Audit:**
    - 品質検証: `activate_skill{name: "python-verification"}` (Ruff, Mypy, Pytest)
    - SSOTチェック: `activate_skill{name: "ssot-verification"}` (仕様との整合性確認)
  - **Commit & PR:**
    - `activate_skill{name: "github-commit"}`
    - `activate_skill{name: "github-pull-request"}`

## アウトプット (Output)

- 仕様を満たし、テストがパスする Python コード。
- `tdd-python-refactoring` によって洗練され、`python-verification` を通過した状態であること。