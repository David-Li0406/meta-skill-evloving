---
name: arch-planning-review
description: Replaces the review process for strictly auditing created architecture update plans against ADRs and system contexts. Typical use cases: (1) Scrutinizing whether abstract definitions are correctly mapped to concrete file paths, (2) Confirming Issue drafts adhere to templates and have clear boundaries, (3) Verifying SSOT consistency to ensure no regressions or principle violations from existing designs.
---

# Architecture Planning Review

作成されたアーキテクチャ更新計画（共通定義書とIssue案）を、**SYSTEM_ARCHITECTの価値観**に基づいて厳格にレビューする。
完璧な状態（Zero Ambiguity）でのみ次工程へ進むことを許可する。

## 役割 (Role)

**Plan Auditor (計画監査人)**
ユーザーの代弁者として、計画書にあらゆる角度からツッコミを入れる。「これ以外に解釈しようがない」レベルまで記述を研ぎ澄ませる。

## 手順 (Procedure)

### 1. 比較対象のロード (Load Context)

- **Action:**
  - `activate_skill{name: "active-reconnaissance"}` を実行し、Source ADR, System Context, および As-Is Architecture の内容を正確に把握する。

### 2. 共通定義の精査 (Audit Common Definitions)

`docs/architecture/plans/*.md` を対象にチェックする。

- **Action:**
  - ドキュメント内の「SSOT Audit Log」セクションを確認し、**記載されているファイルが実際に存在し、内容が反映されているか**をチェックする。
  - 各レイヤー/コンポーネント定義に対し、「具体的なファイルパス（Physical Path）が書かれているか？」を批判的に確認する。

- **Strict Checklist:**
  - [ ] **Physical Mapping:** 抽象的な定義に対し、対応する具体的なディレクトリやファイルパスがマッピングされているか？
  - [ ] **No Jargon:** プロジェクト固有の定義なしに一般的な専門用語を使っていないか？
  - [ ] **SSOT Alignment:** 読み込んだADR/Contextと矛盾していないか？
  - [ ] **Audit Trail:** 参照したSSOTファイルの一覧が記録されているか？

- **Log Output:**
  - チェックリストの判定結果に加え、**「なぜその定義が不十分なのか（例：Infra層のパスが書かれていない）」** という具体的な指摘理由をログに出力する。

### 3. Issue案の精査 (Audit Draft Issues)

`reqs/tasks/drafts/*.md` を対象にチェックする。

- **Action:**
  - `reqs/tasks/template/issue-draft.md` を `read_file` し、期待されるYAML Front Matterのキーとセクション構成を把握する。
  - 作成されたIssue案とテンプレートを比較し、構造が一致しているか厳密に確認する。

- **Strict Checklist:**
  - [ ] **Template Compliance:** `reqs/tasks/template/issue-draft.md` の全ての必須項目（YAMLキー、セクション見出し）が存在するか？
  - [ ] **Mandatory Reference:** 共通定義書へのリンクと遵守指示が明記されているか？
  - [ ] **Clear Scope:** タスクの範囲（Boundary）が明確で、他のタスクと重複していないか？
  - [ ] **No Regression:** 以前の計画と比較し、デグレが起きていないか？

### 4. SSOT整合性検証 (SSOT Verification)

- **Action:**
  - `activate_skill{name: "ssot-verification"}` を実行し、概念レベルでの不整合や原則への違反がないかを最終確認する。

### 5. 指摘と是正 (Finding & Correction)

- **Action:**
  - 各問題点に対し、具体的な改善案をセットで提示する。
  - **Rule:** 改善案が具体的に提案できない項目は、指摘として扱わない（無効とする）。

- **Decision:**
  - **Branch A: Has Proposal (改善案あり)**
    - 一点でも改善案が存在する場合は、直ちに `arch-planning` を再呼び出しして計画全体を作り直させる。
    - `activate_skill{name: "arch-planning"}`
  - **Branch B: No Proposal (改善案なし)**
    - 全てのチェックをパスし、改善案がゼロの場合のみ、レビュー完了（Approved）とする。

## アウトプット (Output)

レビュー結果レポート。