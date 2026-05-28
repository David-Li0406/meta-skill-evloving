---
name: spec-creation
description: Replaces the entire process of translating high-level designs (Architecture/Design Docs) into detailed technical specifications (Specs) that developers can implement immediately. Typical use cases: (1) Decomposing large design changes into specific specification tasks (Issue drafts), (2) Auditing and integrating consistency between multiple distributed specification documents (API, DB, Logic), (3) Finalizing a rigorous set of specifications as the formal input for Test-Driven Development (TDD).
---

# Specification Creation Orchestration

上位の設計ドキュメント（Architecture Map または Design Doc）を入力とし、それを開発者がそのままコードに落とし込めるレベルの「詳細仕様書（Specs）」に変換するプロセスを統括する。

本スキルは以下の2つの大きなフェーズを管理する：

1.  **Planning & Drafting (発射台):** 上位設計を分析し、**共通定義（Common Definitions）** と **Issue案（Draft Issues）** を作成して合意形成する。
2.  **Integration (着陸):** 作成された詳細仕様書を監査し、上位設計（SSOT）との整合性を保証してリリースする。

## 役割定義 (Role Definition)

あなたは **Specification Integrator (仕様統合者)** です。
抽象的な「設計（What/Why）」を、具体的な「実装指示（How）」に翻訳し、複数の仕様書を一貫性のあるドキュメントセットとしてまとめ上げる責任を持ちます。
**注意:** あなた自身は仕様書の執筆（Phase 2の実作業）を行いません。それは起票されたIssueを担当する別のエージェントが行います。

## 手順 (Procedure)

### Phase 1: Planning & Issue Drafting (計画とIssue案作成)

**目的:** 上位設計（Arch/Design Doc）を読み解き、仕様策定のための「共通定義」と「Issue案」を作成し、レビューまで完了させる。

1.  **Branching (Parent Branch):**
    - 作業の基点となる統合用ブランチを作成・チェックアウトする。
    - `activate_skill{name: "github-checkout-feature-branch"}` (例: `feature/spec-update-xxx`)

2.  **Strategic Planning & Drafting:**
    - `activate_skill{name: "spec-planning"}`
    - このスキルを使用し、Common Definitions と 個別の Issue 案を作成する。

3.  **Integration Issue Drafting (Critical):**
    - **個別の仕様策定タスクとは別に、全体の監査とマージを担当する「統合用Issue案」を作成する。**
    - **内容:** 他の全仕様Issueへの `depends_on` を設定し、Phase 3 (Audit) & Phase 4 (Finalization) の手順をタスクとして記述する。

4.  **Verify:** `ssot-verification` を使用し、計画と全Issue案が上位設計（Arch/Design Doc）と矛盾していないか確認する。

### Phase 2: Approval & Initiation (承認と開始)

**目的:** 「共通定義」と「Issue案」のセットで承認を得て、実装フェーズ（他エージェントへの委譲）を開始する。

1.  **Pull Request for Plan:**
    - `docs/specs/plans/` (共通定義) と `reqs/tasks/drafts/` (Issue案) をコミットする。
    - `activate_skill{name: "github-pull-request"}`
    - PRの概要に「上位設計反映のための仕様策定計画（共通定義）とタスク分割案です。これらを承認（マージ）するとIssueが起票されます」と明記し、承認を求める。

_(この後、システムが自動的にIssueを起票し、別エージェントが仕様書の執筆を行う。あなたはそれらの完了を待つ)_

### Phase 3: Audit & Correction (監査と是正)

**目的:** 仕様策定が完了した統合ブランチを監査し、上位設計および共通定義との整合性を確認する。
_(前提: 起票された全てのIssueが完了し、統合ブランチにマージされていること)_

1.  **Traceability & SSOT Check:**
    - `activate_skill{name: "ssot-verification"}`
    - 作成された詳細仕様書（`docs/specs/*.md`）が、以下の2点と整合しているか厳密にチェックする。
      1.  **上位設計 (Architecture/Design Doc):** 本来の意図や要件を満たしているか。
      2.  **共通定義 (Common Definitions):** 定義された用語やデータ型、方針に従っているか。
    - 仕様書同士の整合性（例: API仕様とDB仕様で型が合っているか）を確認する。

2.  **Link Validation:**
    - ドキュメント内のリンク切れ（相対パス、アンカーリンク等）がないか確認する。

3.  **Correction Loop (If NG):**
    - 監査で不備が見つかった場合、以下のどちらかの対応を行う。
    - **重要:** いかなる場合も、**あなた自身が上流ドキュメント（Arch/Design Doc）や仕様書を直接修正してはならない。** 必ずIssue案を作成し、別の作業サイクルとして実行させること。
      - **Case A (Local Fix):** 仕様書の記述ミスや定義漏れの場合。修正内容を定義した「追加のIssue案」を作成する。
      - **Case B (Upstream Fix):** 上流のArch/Design Docに矛盾や見落としが見つかった場合。
        - **Action:** 「上位設計修正用のIssue案」を作成する（例: `fix-arch-xxx.md`）。
        - **Content:** 発見された不整合、実装上のブロッカー要因、修正提案を明記する。
    - 再度 Phase 2 に戻り、追加Issue案のコミット・PR作成を行う。

4.  **Proceed (If OK):**
    - 問題がなければ Phase 4 へ進む。

### Phase 4: Finalization (完了とレビュー対応)

**目的:** 最終成果物を確定し、メインラインへのマージリクエスト（PR作成）を行う。**自動マージは行わない。**

1.  **Create Handover Items:**
    - `docs/handovers/spec-to-tdd.md` を作成（または追記）する。
    - **内容:** 今回の詳細仕様策定を通じて得られた知見、ImplementerがTDDで実装する際に特に注意すべきエッジケース、テストデータ作成時のヒントなどを記載する。

2.  **Final Pull Request:**
    - 監査をパスした統合ブランチから、`main` (または `develop`) へのPull Requestを作成する。
    - `activate_skill{name: "github-pull-request"}`
    - **注意:** PRを作成するまでが責務であり、**マージ自体は行わないこと。**
    - _Option:_ この時点で `docs/specs/plans/*.md` は役割を終えているため、削除してもよい（履歴には残る）。

3.  **Review Support:**
    - 人間のレビュアーからのフィードバック対応（軽微なら `spec-refactoring` で自走、重ければIssue化）。

## 禁止事項 (Anti-Patterns)

- **Undefined Terms:** Common Definitions Doc で定義されていない用語を、各Issueで勝手に発明してはならない。
- **Vague Instructions:** Issue案に「いい感じに仕様を書いて」といった曖昧な指示を書いてはならない。テンプレートと必須項目を指定すること。
- **Direct Writing:** あなた自身が仕様書を書いてはならない。
- **Ignoring SSOT:** 上位設計に書かれていない独自の仕様を勝手に追加してはならない（必要なら上位設計の修正プロセスに戻るべき）。

## アウトプット形式 (Phase 1 Completion)

Draftingフェーズ完了時の報告。

```markdown
## 詳細仕様策定タスク定義完了

- **Source Design:** [上位設計ドキュメント]
- **Common Definitions:** `docs/specs/plans/YYYYMMDD-{feature}.md` (Created)
- **Draft Issues:** `reqs/tasks/drafts/*.md` (Created [N] drafts)
- **PR:** #<Number> (共通定義とIssue案の承認依頼)
- **Next Step:** PR承認後、詳細仕様書の執筆タスクが開始されます。
```
