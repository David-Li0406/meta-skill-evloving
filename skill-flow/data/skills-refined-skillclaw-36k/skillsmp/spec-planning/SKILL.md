---
name: spec-planning
description: Replaces the work of analyzing requirements, formulating strategies to create high-quality detailed specifications, creating shared definitions, and decomposing tasks. Typical use cases: (1) Defining ubiquitous language and shared data types to be unified across all specifications, (2) Organizing Issue drafts in units of "one task per specification file" that allow for parallel work, (3) Defining TDD Verification Criteria (normal, error, boundary) as guidelines for implementers writing test code.
---

# Specification Planning

要件（Issue/ADR）を分析し、開発者が実装に着手できるレベルの「詳細仕様書（Specs）」を作成するための計画を策定・実行するスキル。
共通定義の策定、Issue案の作成、および自己レビューまでを一気通貫で行い、高品質な仕様策定計画を作成する。

## 役割 (Role)

**Spec Strategist (仕様戦略家)**
「何を実装するか」ではなく、「どのドキュメントに、どのような粒度で仕様を記述するか」を設計する。
特に、作成される仕様書が**後続の「Implementer（実装者）」にとって、迷いなくコードとテストを書ける内容になること**を保証する。

## 前提 (Prerequisites)

- 入力となる要件（Issue）または上位設計（Arch/Design Doc）が存在すること。

## 手順 (Procedure)

### 0. 前工程の確認 (Handover Analysis)

**目的:** 前フェーズ（Arch Creation）からの申し送り事項を読み込み、設計のコンテキストを継承する。

- **Action:**
  - `docs/handovers/arch-to-spec.md` が存在する場合、その内容を `read_file` する。
  - 前フェーズで「保留された事項」や「特に注意すべき境界」を把握し、今回のPlanningに反映させる。

### 1. 目標設定 (Objective Setting)

**目的:** 今回のPlanning活動のゴールと成功基準を明確にする。

- **Action:**
  - `activate_skill{name: "objective-setting"}`
  - 今回の仕様策定において、「誰に」「何を」伝えることが最も重要か（Value）を定義し、それを満たすためのSMART目標を設定する。
  - _Goal:_ 「**Implementer (実装者)** が、迷わずTDD（テスト駆動開発）を開始できるレベルのIssue案と共通定義を作成し、レビューをパスする。」

### 2. 意図の抽出と共通定義 (Intent & Common Definitions)

**目的:** 全タスクで統一すべき「用語」や「規約」を先に定義し、仕様間の不整合を防ぐ。

- **Action:**
  - `activate_skill{name: "active-reconnaissance"}` でIssue/ADRと現状の仕様書群を分析。
  - **Common Definitions Doc** (`docs/specs/plans/YYYYMMDD-{feature}-plan.md`) を作成し、以下を定義する。
    - **Ubiquitous Language:** 実装コード（クラス名、変数名）として使用されるべき用語の定義。
    - **Data Models:** エンティティやデータ構造の共通型定義。
    - **Error Codes:** 実装者がテストで検証すべき共通エラーコード。
    - **API Paths:** エンドポイントのパス構造。
    - **Doc Structure:** 作成する仕様書のディレクトリ構成とファイル名規則。

### 3. タスク分割と検証条件 (Slicing & Criteria Strategy)

**目的:** 並列作業可能かつ、自己完結する単位でタスクを分割し、TDD可能な検証条件を定義する。

- **Action:**
  - **Slicing Strategy:** **Atomic Slice (1 Issue = 1 Spec File)** を原則とする。
  - **Output Definition:** 次のステップのために、以下の構成案を確定する。
    1.  **Draft Issue List:** 作成するIssue案のタイトルとファイル名。
    2.  **Output Directory:** `reqs/tasks/drafts/{starting_doc_name}/` (例: `reqs/tasks/drafts/arch-005-payment/`)。
    3.  **Target Scope:** 各Issueで作成/更新する具体的な仕様ファイル名。
    4.  **TDD Criteria (Critical for Implementer):** その仕様書に基づき、実装者がテストコードを書くための具体的な観点。
        - **Happy Path:** 正常な入力に対し、どのような状態変化や戻り値が期待されるか。
        - **Error Path:** 具体的にどの条件で、どの例外/エラーコードが発生すべきか。
        - **Boundary:** 最大長、最小値、Null許容などの境界条件。

    **Example:**
    - Directory: `reqs/tasks/drafts/arch-005-payment/`
    - Issue: `[API Spec] Create User Registration API`
      - Files: `docs/specs/api/user-registration.md`
      - **Verify (TDD Criteria):**
        - 「パスワードが8文字未満の場合、`400 Bad Request` とエラーコード `PASSWORD_TOO_SHORT` が返ること」が仕様書に明記されているか？
        - 「重複アドレス登録時、`409 Conflict` が返ること」が仕様書に明記されているか？

### 4. Issue案の作成 (Issue Drafting)

**目的:** 定義された戦略に基づき、具体的なIssue案ファイルを作成する。

- **Action:**
  - `activate_skill{name: "issue-drafting"}`
  - Step 3 で定義した各タスクについて、Issue案を作成する。
  - **Mandatory:** 全てのIssue案本文に以下を含めるよう指示する：
    1.  Step 2で作成した **Common Definitions Doc へのリンク**。
    2.  **成果物のターゲット:** 「この仕様書の主な読者は **Implementer (実装者)** であり、彼らが迷わずコードとテストを書ける（TDDを回せる）レベルの具体性を提供すること」という旨の指示。
    3.  Step 3で定義した **TDD Criteria (検証項目)**。「Verify」セクションに記載する。

### 5. 計画レビュー (Planning Review)

**目的:** 作成された計画（共通定義 + Issue案）の品質を保証する。

- **Action:**
  - `activate_skill{name: "spec-planning-review"}`
  - 作成された共通定義書とIssue案をレビューする。
  - **Resulting Value Check:** 「このIssue案の通りに仕様書が作成された場合、実装者は迷わずTDDを開始できるか？」という視点でチェックする。
  - **Correction:** 修正が必要な場合は、直ちにファイル (`docs/specs/plans/*.md`, `reqs/tasks/drafts/*.md`) を更新する。

## アウトプット (Output)

`spec-creation` がコミットすべきアーティファクト一式。

1.  **Common Definitions Doc:** `docs/specs/plans/{date}-{name}.md`
2.  **Draft Issues:** `reqs/tasks/drafts/*.md` (TDD Criteriaを含む)
3.  **Review Report:** (Console Output or Comment)
