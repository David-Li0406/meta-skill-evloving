---
name: tdd-planning-review
description: Replaces the review task of strictly auditing whether the created implementation plan satisfies specification coverage and architectural compliance. Typical use cases: (1) Confirming that planned test cases cover error cases and boundary values from the specifications, (2) Verifying that code placement follows project conventions such as Clean Architecture, (3) Scrutinizing the feasibility of proceeding with implementation using the proposed TDD scenarios.
---

# TDD Planning Review

作成された実装計画（共通実装計画とIssue案）を、**TDD Leadの価値観**に基づいて厳格にレビューする。
「テストが仕様を網羅しているか」「実装方針がアーキテクチャに準拠しているか」を保証する。

## 役割 (Role)

**Implementation Auditor (実装計画監査人)**
実装者の代弁者として、計画書にあらゆる角度からツッコミを入れる。「このタスク定義で、本当にRed-Green-Refactorが回せるか？」を確認する。

## 手順 (Procedure)

### 1. 比較対象のロード (Load Context)

- **Action:**
  - `activate_skill{name: "active-reconnaissance"}` を実行し、Source Specs, Handover, および Current Architecture の内容を正確に把握する。

### 2. 共通実装計画の精査 (Audit Common Implementation Plan)

`docs/implementation/plans/*.md` を対象に、アーキテクチャ方針と技術的整合性をチェックする。

- **Strict Checklist:**
  - [ ] **Specs Alignment:** 仕様書で定義された要件（型、エラー、ロジック）がすべて考慮されているか？
  - [ ] **Layering Compliance:** 各コードの配置場所（Domain, UseCase, Infra）がクリーンアーキテクチャ等の規約に合致しているか？
  - [ ] **Test Strategy:** モックの方針やテスト範囲が、既存のテストパターンと整合しているか？
  - [ ] **Feasibility:** 提示された方針で、技術的に実装可能か？

### 3. Issue案の精査 (Audit Draft Issues)

`reqs/tasks/drafts/*.md` を対象にチェックする。

- **Action:**
  - `reqs/tasks/template/issue-draft.md` を `read_file` し、期待されるYAML Front Matterのキーとセクション構成を把握する。
  - 作成されたIssue案とテンプレートを比較し、構造が一致しているか厳密に確認する。

- **Strict Checklist:**
  - [ ] **Template Compliance:** `reqs/tasks/template/issue-draft.md` の全ての必須項目（YAMLキー、セクション見出し）が存在するか？
  - [ ] **Mandatory Reference:** 共通実装計画へのリンクと遵守指示が明記されているか？
  - [ ] **TDD Scenarios:** 「TDD Scenarios」セクションに、具体的なRed/Greenの手順が記載されているか？

### 4. SSOT整合性検証 (SSOT Verification)

- **Action:**
  - `activate_skill{name: "ssot-verification"}` を実行し、上位の ADR や Architecture Map との不整合がないかを最終確認する。

### 5. 指摘と是正 (Finding & Correction)

- **Action:**
  - 問題点に対し、具体的な改善案（修正すべき定義やシナリオ）を提示する。

- **Decision:**
  - **Branch A: Has Proposal (改善案あり)**
    - 指摘事項がある場合は、`tdd-planning` を再呼び出しして修正させる。
  - **Branch B: No Proposal (改善案なし)**
    - 全てのチェックをパスした場合のみ、レビュー完了（Approved）とする。

## アウトプット (Output)

レビュー結果レポート。
