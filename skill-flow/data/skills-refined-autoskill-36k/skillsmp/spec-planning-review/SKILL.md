---
name: spec-planning-review
description: Replaces the review process for strictly auditing specification formulation plans from a Technical Designer perspective to ensure developers can implement without confusion. Typical use cases: (1) Confirming definitions of terms, types, and error codes do not contradict existing specifications, (2) Scrutinizing the Verify section of Issue drafts for concrete test perspectives, (3) SSOT consistency verification to ensure no regressions from high-level designs (Arch/Design Docs).
---

# Specification Planning Review

作成された仕様策定計画（共通定義書とIssue案）を、**Technical Designerの価値観**に基づいて厳格にレビューする。
開発者が迷わず実装できる状態（Ready for Dev）でのみ次工程へ進むことを許可する。

## 役割 (Role)

**Spec Plan Auditor (仕様計画監査人)**
実装者の代弁者として、計画書にあらゆる角度からツッコミを入れる。「この仕様で本当にコードが書けるか？」「矛盾はないか？」を確認する。

## 手順 (Procedure)

### 1. 比較対象のロード (Load Context)

- **Action:**
  - `activate_skill{name: "active-reconnaissance"}` を実行し、Source Requirement (Issue/ADR), System Context, および Existing Specs の内容を正確に把握する。

### 2. 共通定義の精査 (Audit Common Definitions)

`docs/specs/plans/*.md` を対象に、`TECHNICAL_DESIGNER` の価値観に照らしてチェックする。

- **Strict Checklist:**
  - [ ] **Consistency:** 用語、型、エラーコードの定義が一貫しており、既存の仕様と矛盾していないか？
  - [ ] **Clarity:** 開発者が読んだ時に、複数の解釈が生まれないか？
  - [ ] **Feasibility:** 定義された内容は技術的に実現可能か？（上位設計の制約を守っているか）
  - [ ] **Completeness:** 今回のスコープで必要な共通項目が全て網羅されているか？

### 3. Issue案の精査 (Audit Draft Issues)

`reqs/tasks/drafts/*.md` を対象にチェックする。

- **Action:**
  - `reqs/tasks/template/issue-draft.md` を `read_file` し、期待されるYAML Front Matterのキーとセクション構成を把握する。
  - 作成されたIssue案とテンプレートを比較し、構造が一致しているか厳密に確認する。

- **Strict Checklist:**
  - [ ] **Template Compliance:** `reqs/tasks/template/issue-draft.md` の全ての必須項目（YAMLキー、セクション見出し）が存在するか？
  - [ ] **Mandatory Reference:** 共通定義書へのリンクと遵守指示が明記されているか？
  - [ ] **Atomic Scope:** 各タスクの範囲が明確で、担当者が迷わず作業開始できるか？
  - [ ] **Output Definition:** 作成すべきファイル名と場所が具体的に指定されているか？
  - [ ] **TDD Readiness (Critical):** 「Verify」セクションに、仕様書が満たすべき具体的な**テスト観点（正常系・異常系・境界値）**が記述されているか？
    - NG例: 「エラー処理を記述すること」
    - OK例: 「重複登録時に409エラーが返る仕様が含まれていること」

### 4. SSOT整合性検証 (SSOT Verification)

- **Action:**
  - `activate_skill{name: "ssot-verification"}` を実行し、上位設計（Arch/Design Doc）との不整合がないかを最終確認する。

### 5. 指摘と是正 (Finding & Correction)

- **Action:**
  - 各問題点に対し、具体的な改善案をセットで提示する。
  - **Rule:** 改善案が具体的に提案できない項目は、指摘として扱わない（無効とする）。

- **Decision:**
  - **Branch A: Has Proposal (改善案あり)**
    - 一点でも改善案が存在する場合は、直ちに `spec-planning` を再呼び出しして計画全体を作り直させる。
    - `activate_skill{name: "spec-planning"}`
  - **Branch B: No Proposal (改善案なし)**
    - 全てのチェックをパスし、改善案がゼロの場合のみ、レビュー完了（Approved）とする。

## アウトプット (Output)

レビュー結果レポート。