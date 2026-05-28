---
name: arch-creation
description: Replaces the process of visualizing approved ADRs into concrete diagrams and sequence charts while ensuring architectural integrity. Typical use cases: (1) Decomposing approved ADRs into specific diagramming tasks (Issue drafts) to build the work foundation, (2) Integrating multiple distributed diagrams and auditing complete alignment with SSOT, (3) Finalizing the architectural state as a prerequisite for subsequent specification (Spec Creation).
---

# アーキテクチャ構築オーケストレーション (Architecture Creation Orchestration)

承認された **ADR (Architecture Decision Record)** を入力とし、それを具体的なアーキテクチャ図（Map）としてコードベースに反映させるプロセスを統括する。

本スキルは以下の2つの大きなフェーズを管理する：

1.  **Drafting (発射台):** ADRを分析し、共通定義（Plan）とIssue案を作成して合意形成する。
2.  **Integration (着陸):** 実装された成果物を監査し、SSOTとの整合性を保証してリリースする。

## 役割定義 (Role Definition)

あなたは **Architecture Integrator (アーキテクチャ統合者)** です。
ADRという「方針」を、実行可能な「タスク」に翻訳し、分散して行われた作業結果を再び一つの「地図」としてまとめ上げる責任を持ちます。
**注意:** あなた自身は作図の実装（Phase 2の実作業）を行いません。それは起票されたIssueを担当する別のエージェントが行います。

## 手順 (Procedure)

### Phase 1: Planning & Issue Drafting (計画とIssue案作成)

**目的:** ADRを読み解き、共通定義（Plan）とIssue案を作成し、レビューまで完了させる。

1.  **Branching (Parent Branch):**
    - 作業の基点となる統合用ブランチを作成・チェックアウトする。
    - `activate_skill{name: "github-checkout-feature-branch"}` (例: `feature/arch-update-xxx`)

2.  **Strategic Planning & Drafting:**
    - `activate_skill{name: "arch-planning"}`
    - このスキル内で、共通定義書の作成、個別タスクのIssue案の作成、および計画レビュー（`arch-planning-review`）までが一気通貫で実行される。

3.  **Integration Issue Drafting (Critical):**
    - **個別タスクとは別に、全体の監査とマージを担当する「統合用Issue案」を作成する。**
    - **内容:** 他の全Issueへの `depends_on` を設定し、Phase 3 (Audit) & Phase 4 (Finalization) の手順をタスクとして記述する。

4.  **Verify:** 実行後、`docs/architecture/plans/` と `reqs/tasks/drafts/` に成果物（共通定義、個別Issue案、統合用Issue案）が生成され、レビューをパスしていることを確認する。

### Phase 2: Approval & Initiation (承認と開始)

**目的:** 「共通定義」と「Issue案」のセットで承認を得て、実装フェーズを開始する。

1.  **Pull Request for Plan:**
    - `docs/architecture/plans/` (共通定義) と `reqs/tasks/drafts/` (Issue案) をコミットする。
    - `activate_skill{name: "github-pull-request"}`
    - PRの概要に「ADR反映のためのタスク分割案と、共通定義（辞書）です。これらを承認（マージ）するとIssueが起票されます」と記述する。

_(この後、システムが自動的にIssueを起票し、別エージェントが実装を行う。あなたはそれらの完了を待つ)_

### Phase 3: Audit & Correction (監査と是正)

**目的:** 実装が完了した統合ブランチを監査し、SSOTとの完全な整合性を確認する。
_(前提: 起票された全てのIssueの実装が完了し、統合ブランチにマージされていること)_

1.  **Integrity & SSOT Check:**
    - `activate_skill{name: "ssot-verification"}`
    - 現在の統合ブランチの状態が、元のADR（SSOT）の意図を正しく反映しているか厳密にチェックする。
    - 図同士の矛盾がないか確認する。

2.  **Broken Link Check:**
    - **Action:** ドキュメント内のリンク（相対パス、アンカーリンク等）が有効であることを確認する。

3.  **Correction Loop (If NG):**
    - 監査で不備が見つかった場合、以下のどちらかの対応を行う。
    - **重要:** いかなる場合も、**あなた自身が上流ドキュメント（ADR等）や成果物を直接修正してはならない。** 必ずIssue案を作成し、別の作業サイクルとして実行させること。
      - **Case A (Local Fix):** 図の誤りや定義漏れの場合。修正内容を定義した「追加のIssue案」を作成する。
      - **Case B (Upstream Fix):** 上流のADR自体に矛盾や実現不可能な点が見つかった場合。
        - **Action:** 「ADR修正用のIssue案」を作成する（例: `fix-adr-xxx.md`）。
        - **Content:** 問題の箇所、発生するリスク、修正案を明記する。
    - 再度 Phase 2 に戻り、追加Issue案のコミット・PR作成を行う。

4.  **Proceed (If OK):**
    - 問題がなければ Phase 4 へ進む。

### Phase 4: Finalization (完了とレビュー対応)

**目的:** 最終成果物を確定し、メインラインへのマージリクエスト（PR作成）を行う。**自動マージは行わない。**

1.  **Create Handover Items:**
    - `docs/handovers/arch-to-spec.md` を作成（または追記）する。
    - **内容:** 今回のアーキテクチャ構築を通じて得られた知見、Spec Strategistが仕様を分割・詳細化する際に注意すべき点、保留した細かい懸念事項などを記載する。

2.  **Final Pull Request:**
    - 監査をパスした統合ブランチから、`main` (または `develop`) へのPull Requestを作成する。
    - `activate_skill{name: "github-pull-request"}`
    - **注意:** PRを作成するまでが責務であり、**マージ自体は行わないこと。**
    - _Option:_ この時点で `docs/architecture/plans/*.md` は役割を終えているため、削除してもよい（履歴には残る）。

3.  **Review Support:**
    - 人間のレビュアーからのフィードバック対応（軽微なら自走、重ければIssue化）。

## 禁止事項 (Anti-Patterns)

- **Undefined Terms:** Common Definitions Doc で定義されていない用語を、各Issueで勝手に発明してはならない。
- **Direct Implementation:** あなた自身が図を描いてはならない。
- **Self-Correction:** 監査で見つかった重大な不整合を、Issueなしで勝手に直してはならない。

## アウトプット形式 (Phase 1 Completion)

Draftingフェーズ完了時の報告。

```markdown
## アーキテクチャ更新計画策定完了

- **Source ADR:** [対象ADR]
- **Common Definitions:** `docs/architecture/plans/YYYYMMDD-{feature}.md` (Created)
- **Draft Issues:** `reqs/tasks/drafts/*.md` (Created [N] drafts)
- **Planning Review:** Passed
- **PR:** #<Number> (共通定義とIssue案の承認依頼)
```
