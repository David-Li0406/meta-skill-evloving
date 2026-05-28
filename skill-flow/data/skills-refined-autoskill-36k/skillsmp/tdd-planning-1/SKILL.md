---
name: tdd-planning
description: Replaces the implementation strategy formulation work of analyzing detailed specifications and deciding how code and tests should be placed across layers. Typical use cases: (1) Mapping each element of the specification to domain, use case, or infrastructure layers, (2) Defining test scope, mocking policies, and shared stubs, (3) Designing specific TDD Scenarios for implementers to follow the Red-Green-Refactor cycle.
---

# TDD Planning (Implementation Strategy)

詳細仕様（Specs）を分析し、テスト駆動開発（TDD）によってユースケースおよびロジックを実装するための計画を策定・実行するスキル。
共通実装方針の策定、Issue案（TDDタスク）の作成、および自己レビューまでを一気通貫で行い、高品質な実装計画を作成する。

## 役割 (Role)

**Implementation Strategist (実装戦略家)**
「何を作るか」ではなく、「どの順序でテストを書き、どのレイヤー（Domain/UseCase/Infra）にどのような方針でコードを配置するか」を設計する。
特に、**Implementer（実装者）が迷わず Red-Green-Refactor サイクルを回せるレベルの「検証可能なIssue案」**を作成することを重視する。

## 前提 (Prerequisites)

- 入力となる詳細仕様書（Specs）および、前工程からの引継ぎ事項（Handover）が存在すること。

## 手順 (Procedure)

### 0. 前工程の確認 (Handover Analysis)

**目的:** 前フェーズ（Spec Creation）からの申し送り事項を読み込み、仕様のコンテキストを継承する。

- **Action:**
  - `docs/handovers/spec-to-tdd.md` を `read_file` する。
  - 仕様策定時に想定された「テストのヒント」や「エッジケース」を把握し、実装計画に反映させる。

### 1. 目標設定 (Objective Setting)

**目的:** 今回の実装活動のゴールと成功基準を明確にする。

- **Action:**
  - `activate_skill{name: "objective-setting"}`
  - 実装完了の定義（全テストパス、カバレッジ、アーキテクチャ準拠）をSMART目標として設定する。
  - _Goal:_ 「仕様書を完全に満たし、UseCaseロジックが正常に動作するコードとテストを完遂するためのIssue案を作成し、レビューをパスする。」

### 2. 意図の抽出と共通実装方針 (Intent & Implementation Policy)

**目的:** 全タスクで統一すべき「技術的判断」や「モックの方針」を先に定義し、実装の不整合を防ぐ。

- **Action:**
  - `activate_skill{name: "active-reconnaissance"}` でSpecsと既存コードのテストパターンを分析。
  - **Common Implementation Plan** (`docs/implementation/plans/YYYYMMDD-{feature}-plan.md`) を作成し、以下を定義する。
    - **Architecture Mapping:** 仕様書の各要素をどのディレクトリ/クラスに配置するか。
    - **Test Strategy:** ユニットテストの範囲、モック化する依存先（DB、外部API）の方針。
    - **Shared Stubs:** 複数のタスクで共有する基盤コードやスタブの定義。
    - **Coding Standards:** 今回特に遵守すべきパターン（例: 「Result型によるエラーハンドリングの統一」）。

### 3. タスク分割とTDDシナリオ (Slicing & TDD Scenarios)

**目的:** 独立して実装・テスト可能であり、かつマージ時の衝突が少ない単位でタスクを分割する。

- **Action:**
  - **Slicing Strategy:** **Feature/Component Slice** を原則とする。
    - _原則:_ 1つのユースケース、または1つの重要なドメインロジックにつき、1つのIssueを発行する。
  - **Output Definition:** 次のステップのために、以下の構成案を確定する。
    1.  **Draft Issue List:** 作成するIssue案のタイトルとファイル名（例: `tdd-usecase-registration.md`）。
    2.  **Output Directory:** `reqs/tasks/drafts/{starting_doc_name}/` (例: `reqs/tasks/drafts/spec-005-registration/`)。
    3.  **TDD Scenarios (Critical):** 実装者が `tdd-python-drafting` スキルで使用する具体的な Red/Green シナリオ。

    **Example:**
    - Directory: `reqs/tasks/drafts/spec-005-registration/`
    - Issue: `[TDD] Implement User Registration UseCase`
      - Files: `src/domain/`, `src/usecase/`, `tests/unit/`
      - **TDD Scenarios:**
        - **Red 1:** 未登録メールアドレスでの登録時、UseCaseが `User` オブジェクトを返すことを検証。

### 4. Issue案の作成 (Issue Drafting)

**目的:** 定義された戦略に基づき、具体的なIssue案ファイルを作成する。

- **Action:**
  - `activate_skill{name: "issue-drafting"}`
  - Step 3 で定義した各タスクについて、Issue案を作成する。
  - **Mandatory:** 全てのIssue案本文に以下を含めるよう指示する：
    1.  Step 2で作成した **Common Implementation Plan へのリンク**。
    2.  **成果物のターゲット:** 「このタスクの成果物は、仕様を完全に満たす **プロダクトコード（UseCase/Logic）** および **ユニットテスト** である」という明示。
    3.  Step 3で定義した **TDD Scenarios**。

### 5. 計画レビュー (Planning Review)

**目的:** 作成された計画（共通方針 + Issue案）の品質を保証する。

- **Action:**
  - `activate_skill{name: "tdd-planning-review"}`
  - 作成された共通実装計画とIssue案をレビューする。
  - **Audit View:** 「このIssue案があれば、実装者は迷わず `tdd-implementation` を起動してRed-Green-Refactorを回せるか？」という視点でチェックする。

## アウトプット (Output)

`tdd-creation` がコミットすべきアーティファクト一式。

1.  **Common Implementation Plan:** `docs/implementation/plans/{date}-{name}.md`
2.  **Draft Issues:** `reqs/tasks/drafts/*.md` (TDD Scenariosを含む)
3.  **Review Report:** (Console Output or Comment)
