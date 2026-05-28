---
name: adr-creation
description: Replaces the entire process of formulating Architecture Decision Records (ADRs) based on the OODA loop. Typical use cases: (1) Defining the specific scope and components of the system to be implemented next, (2) Evaluating technical trade-offs to select optimal implementation strategies (e.g., library choice or data patterns), (3) Fixing decisions as a formal blueprint (Blueprint) before proceeding to structural design (arch-creation).
---

# ADR作成オーケストレーション (ADR Creation Orchestration)

ADR作成プロセスを**OODAループ (Observe -> Orient -> Decide -> Act)** に基づく4段階のフローとして実行する。
事前にTodoリストでタスクを固定するのではなく、各フェーズでの「気付き」と「対話」を通じて、動的に意思決定プロセスを進める。

## 役割定義 (Role Definition)

あなたは **Architecture Facilitator (アーキテクチャ・ファシリテーター)** です。
一方的にドキュメントを作るのではなく、ユーザーに判断材料（事実・選択肢・トレードオフ）を提供し、質の高い意思決定を引き出すことが役割です。

## 手順 (Procedure)

### Phase 0: Preparation (準備)

1.  **Branching:**
    - 作業を開始する前に、適切なフィーチャーブランチに切り替える。
    - `activate_skill{name: "github-checkout-feature-branch"}`

### Phase 1: Observe (調査・観察)

**目的:** 意思決定に必要な「事実」を集める。憶測で語らず、コードと現状を直視する。

1.  **ユーザーヒアリング:**
    - ユーザーが抱えている課題感、解決したいこと、制約条件を聞き出す。
2.  **Active Reconnaissance (偵察):**
    - `activate_skill{name: "active-reconnaissance"}`
    - 関連する既存コード、既存ADR、仕様書を調査する。
    - 「何が実装済みで、何が欠けているか」の事実（Fact）を収集する。

### Phase 2: Orient (状況判断・多角分析)

**目的:** 集めた事実を解釈し、可能性を広げる（発散）。

1.  **Domain Modeling (構造整理):**
    - `activate_skill{name: "domain-modeling"}`
    - 問題領域の用語定義、関係性の整理を行い、メンタルモデルを合わせる。
2.  **Hypothesis & Options (仮説立案):**
    - `activate_skill{name: "context-hypothesis"}`
    - 解決策の選択肢（Options）を、以下の3つの視点で洗い出す。
      - **実証的仮説 (Grounded):** 現状の事実とSSOTに基づいた堅実な本命案。
      - **飛躍的仮説 (Leap):** 「ユーザーの真の理想」を先回りして提示する理想追求案。
      - **逆説的仮説 (Paradoxical):** 既存の前提を覆し、パラダイムシフトを起こす破壊的イノベーション案。
    - 各案のトレードオフ（Pros/Cons）を分析する。

### Phase 3: Decide (意思決定・収束)

**目的:** 収束を促すための問いを立て、記述すべき方針を確定させる。

1.  **Bottleneck Resolution (論点整理と問い):**
    - `activate_skill{name: "decision-support"}` を使用し、合意へのボトルネックを特定する。
    - 現在の分析結果とユーザーの意向を統合し、解像度を高めるための「たった一つの問い」を投げる。
2.  **Steer Acquisition (記述方針の確定):**
    - ユーザーの回答から「ADRにどう記述すべきか（または何が不足しているか）」の方針を固める。
    - **Insight:** 議論を停滞させないため、方針が固まったら速やかに Phase 4 (Act) へ移り、ドキュメントとして可視化する。

### Phase 4: Act (記述・実行)

**目的:** 決定（または現在の仮説）を可視化し、フィードバックの土台を作る。

ユーザーに対し、以下の2択からアクションを選択してもらい実行する。

1.  **Option A: Work in Progress (記述・レビュー・保存)**
    - **議論を前進させるための「プロトタイプ」作成。**
    - `activate_skill{name: "adr-drafting"}` (記述)
    - `activate_skill{name: "adr-review"}` (自己レビュー)
    - `activate_skill{name: "github-commit"}` (保存)
    - **Role:** 具体的なドキュメントを提示することで、ユーザーからより深いフィードバックを引き出す。修正が必要な場合は再度 Phase 3 または 4-1 を繰り返す。

2.  **Option B: Done (完了・PR・次へ)**
    - ドキュメントの内容にユーザーが最終承認し、ADR作成を完了する場合。
    - `activate_skill{name: "github-pull-request"}` (PR作成)
    - PR作成後、**Architecture Implementation (アーキテクチャの具体化・実装)** へ進むことを提案して終了する。

## 禁止事項 (Anti-Patterns)

- **Todoリストの事前作成:** OODAループは状況に応じて次の手が変化するため、最初に全てのタスクを固定してはならない。
- **スキップ:** 「調査」や「分析」を飛ばして、いきなり「記述」に入ってはならない。
- **独断:** 選択肢の提示なしに、エージェントが勝手に解決策を一つに絞ってはならない。

## アウトプット形式 (Final Report)

全工程完了時の報告。

```markdown
## ADR作成完了 (OODA Loop Completed)

- **Phase 1 (Observe):** [調査範囲]
- **Phase 2 (Orient):** [検討した選択肢]
- **Phase 3 (Decide):** [決定事項/記述方針]
- **Phase 4 (Act):**
  - **Artifact:** `reqs/design/_inbox/adr-XXX.md`
  - **PR:** #<Number>
  - **Next:** Proposed Architecture Implementation
```
