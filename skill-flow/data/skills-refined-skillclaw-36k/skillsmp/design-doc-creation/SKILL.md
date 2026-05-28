---
name: design-doc-creation
description: Replaces the entire design process for architectural decision-making and overall structural design for new features or major changes. Typical use cases: (1) Formulating and evaluating multi-perspective approaches (hypotheses) based on user requirements and technical constraints, (2) Defining dependencies between major domain models and components, (3) Converging on design policies through user dialogue and obtaining Design Doc approval.
---

# Design Doc作成オーケストレーション (Design Doc Creation)

Design Doc作成プロセスを**OODAループ (Observe -> Orient -> Decide -> Act)** に基づく4段階のフローとして実行する。

本スキルの目的は、機能要件に対して「アーキテクチャ上の意思決定」と「全体構造の設計」を行い、人間との合意を形成することである。
詳細な実装指示（APIの型定義やメソッド単位の仕様）はここには含めず、後続の `spec-creation` スキルに委譲する。

- **Input:** 要件、課題、ADR
- **Process:** 構造設計、トレードオフ分析、合意形成
- **Output:** Design Doc (構造と方針が定義されたもの)
- **Next:** Spec Creation (エージェント向けの実装指示書作成)

## 役割定義 (Role Definition)

あなたは **Feature Architect (機能アーキテクト)** です。
「どう作るか」の大枠（構造・方針）を定義し、実装フェーズでの手戻りを防ぐための羅針盤を作ります。

## 手順 (Procedure)

### Phase 0: Preparation (準備)

1.  **Branching:**
    - 作業を開始する前に、適切なフィーチャーブランチに切り替える。
    - `activate_skill{name: "github-checkout-feature-branch"}`

### Phase 1: Observe (調査・観察)

**目的:** 設計の前提となる「事実」と「制約」を集める。

1.  **Requirement Analysis (要件確認):**
    - ユーザーに対し、今回の機能要件とスコープを確認する。
2.  **Active Reconnaissance (偵察):**
    - `activate_skill{name: "active-reconnaissance"}`
    - 関連する既存コードやADRを調査し、技術的制約や依存関係を特定する。

### Phase 2: Orient (機能アーキテクチャ設計)

**目的:** 機能レベルでの「意思決定」と「構造設計」を行う。

1.  **Design Decision (設計判断):**
    - `activate_skill{name: "context-hypothesis"}` (流用)
    - 機能を実現するためのアプローチを、以下の3つの視点（`context-hypothesis`準拠）で検討し、トレードオフを分析する。
      - **案A (実証的):** 基本に忠実でリスクの少ない案。
      - **案B (飛躍的):** 理想的なユーザー体験や将来性を追求した案。
      - **案C (逆説的):** 既存の仕組みをハックするような破壊的/代替的な案。
2.  **Structural Design (構造定義):**
    - `activate_skill{name: "domain-modeling"}`
    - `activate_skill{name: "arch-structural-design"}` (**High-Level Only**)
    - 主要なドメインモデル、コンポーネント構成、および主要なデータの流れ（シーケンス）を定義する。
    - **Focus:** 「型定義」ではなく「責務分担」と「依存関係」を決める。
3.  **Quality Policy (品質方針):**
    - `activate_skill{name: "arch-quality-design"}`
    - パフォーマンス、セキュリティ、エラー処理の「方針（Policy）」を定義する（具体的な閾値や実装コードはSpecで決める）。

### Phase 3: Decide (合意形成・収束)

**目的:** 設計方針を確定させる。

1.  **Design Review & Inquiry (論点整理):**
    - `activate_skill{name: "decision-support"}`
    - 設計上の分岐点についてユーザーと合意形成を行う。
2.  **Steer Acquisition (記述方針の確定):**
    - Design Docに記述すべき「決定事項」と「構造」の方針を固める。

### Phase 4: Act (記述・実行)

**目的:** Design Docを作成し、Spec作成フェーズへ接続する。

ユーザーに対し、以下の2択からアクションを選択してもらい実行する。

1.  **Option A: Work in Progress (記述・レビュー・保存)**
    - **設計方針を具体化し、ドラフトを作成する。**
    - `activate_skill{name: "design-doc-drafting"}` (記述)
    - `activate_skill{name: "github-commit"}` (保存)
    - コミット後、再度 Orient に戻るか Act を続けるかを確認する。

2.  **Option B: Done (完了・PR・次へ)**
    - Design Docの内容にユーザーが最終承認し、設計フェーズを完了する場合。
    - `activate_skill{name: "github-pull-request"}` (PR作成)
    - PR作成後、**Spec Creation (エージェント向け実装指示書の作成)** へ進むことを提案して終了する。
      - 推奨スキル: `spec-creation`

## 禁止事項 (Anti-Patterns)

- **Over-Specification:** メソッドの引数や戻り値の型まで詳細に定義してしまうこと（それはSpecの役割）。
- **Implementation Detail:** 実装コードの断片を書くこと（構造を示す疑似コードは可）。

## アウトプット形式 (Final Report)

全工程完了時の報告。

```markdown
## Design Doc作成完了 (OODA Loop Completed)

- **Phase 1 (Observe):** [調査範囲]
- **Phase 2 (Orient):** [設計方針/モデル構造]
- **Phase 3 (Decide):** [決定したアプローチ]
- **Phase 4 (Act):**
  - **Artifact:** `reqs/design/_inbox/design-XXX.md`
  - **PR:** #<Number>
  - **Next:** Spec Creation (Detailed Specification for Implementation)
```
