---
name: issue-review
description: Replaces the task of strictly auditing created Issue drafts to ensure they align with the project's SSOT and agent values. Typical use cases: (1) Verifying the existence of linked file paths and format checking of metadata, (2) Quality auditing from perspectives of outcome-orientation and rigor across roles, (3) Detecting conceptual inconsistencies and providing specific improvement proposals.
---

# Issue Review (Value & Reality Driven Audit)

作成された `reqs/tasks/drafts/*.md` を厳格にレビューするスキル。
形式的な品質だけでなく、読み込んだSSOTとの整合性を検証し、各エージェントの価値観に合致しているかを監査する。

## 役割 (Role)

**Quality Auditor (品質監査人)**
作業担当者の視点に立ち、「この指示だけで迷わず完遂できるか？」を問うとともに、アーキテクトの視点で「これは正しい方向への一歩か？」を問う。

## 手順 (Procedure)

### 1. 比較対象のロード (Load Context)

- **Action:**
  - レビュー対象のIssueドラフトを読み込む。
  - `activate_skill{name: "active-reconnaissance"}` を実行し、Issue内で参照されている ADR, Common Definitions Doc, および `docs/system-context.md` の内容を正確に把握する。

### 2. 形式と物理的整合性の監査 (Formal & Physical Audit)

- **Checklist:**
  - [ ] **Meta Integrity:** `roadmap`, `task_id`, `labels` が正しく埋まっているか？
  - [ ] **Link Validation:** リンクされているファイルパスは実在するか？
  - [ ] **Structure:** セクション 1 ～ 6 が全て存在し、テンプレート構造を維持しているか？
  - [ ] **No Placeholders:** `{{title}}` 等の変数が残っていないか？

### 3. 価値観に基づく監査 (Value-Driven Audit)

読み込んだドキュメントと比較し、各エージェントの行動規範に合致しているか精査する。

#### A. SYSTEM_ARCHITECT Perspective (全体最適と価値)

- [ ] **Outcome-Oriented:** 「作業（Output）」だけでなく「達成すべき状態（Outcome）」がゴールとして定義されているか？
- [ ] **Domain-Centric:** ドメイン（ビジネス）の用語で意図が語られているか？
- [ ] **Context Integrity:** ADR/Common Definitions の方針と矛盾していないか？

#### B. TECHNICAL_DESIGNER Perspective (明確性と厳密性)

- [ ] **Clarity & Rigor:** 曖昧な表現が排除され、解釈の余地がないほど厳密か？
- [ ] **Implementation-Aware:** 実装者が迷わないレベルまで、手順やテンプレートが具体的か？
- [ ] **Visual/Explicit:** 複雑な構造に対し、図解や具体的な構成への言及があるか？

#### C. BACKENDCODER Perspective (実装と品質)

- [ ] **Simplicity (YAGNI):** タスクの範囲が必要最小限に絞られているか？
- [ ] **Test-Driven / Verifiable:** 完了条件（DoD）に客観的な検証方法が含まれているか？
- [ ] **Negative Constraints:** 「やってはいけないこと」が明記されているか？

### 4. SSOT整合性検証 (SSOT Verification)

- **Action:**
  - `activate_skill{name: "ssot-verification"}` を実行し、概念レベルでの不整合や原則への違反がないかを最終確認する。

### 5. 指摘と是正 (Finding & Correction)

- **Action:**
  - 各問題点に対し、具体的な改善案をセットで提示する。
  - **Rule:** 改善案が具体的に提案できない項目は、指摘として扱わない（無効とする）。

- **Decision:**
  - **Branch A: Has Proposal (改善案あり)**
    - 一点でも改善案が存在する場合は、直ちに `issue-drafting` を再呼び出しして作り直させる。
    - `activate_skill{name: "issue-drafting"}`
  - **Branch B: No Proposal (改善案なし)**
    - 全てのチェックをパスし、改善案がゼロの場合のみ、レビュー完了（Approved）とする。

## アウトプット (Output)

レビュー結果レポート。
