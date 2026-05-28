---
name: context-creation
description: Replaces the process of defining the system's overall picture (SSOT) and dynamically maintaining alignment between codebase reality and design maps. Typical use cases: (1) Defining initial system boundaries and domain models at project start, (2) Updating outdated documentation to match the current state of the implementation as it progresses, (3) Building firm prerequisite knowledge (SSOT) before initiating significant Architecture Decision Records (ADR).
---

# システムコンテキスト作成・維持 (Context Creation & Maintenance)

システムの全体像（SSOT）を定義、または最新化するオーケストレーションスキル。
**OODAループ (Observe -> Orient -> Decide -> Act)** を採用し、現実（コード/ADR）と地図（ドキュメント）の整合性を動的に保証する。

## 役割定義 (Role Definition)
あなたは **Chief Cartographer (地図製作責任者)** です。現実と地図の乖離を許さず、常にチームが正しい方向へ進めるよう導きます。

## 前提 (Prerequisites)
- プロジェクト開始時、または大規模な変更後、あるいは定期的なドキュメントメンテナンス時。

## 手順 (Procedure)

### Phase 0: Preparation (準備)

1.  **Branching:**
    - 作業を開始する前に、適切なフィーチャーブランチに切り替える。
    - `activate_skill{name: "github-checkout-feature-branch"}` (例: `feature/update-context-xxx`)

### Phase 1: Observe (調査・観察)

**目的:** 「現実（Reality）」と「既存の地図（Map）」の乖離（Gap）を特定する。

1.  **Reality Check (現状把握):**
    - `activate_skill{name: "active-reconnaissance"}`
    - 最新のコードベース、ディレクトリ構成、主要な設定ファイル（`pyproject.toml`, `package.json`等）を調査する。
    - 実際に稼働している外部システム連携や、実装された主要コンポーネントを特定する。

2.  **Map Analysis (既存文書確認):**
    - 既存の `docs/system-context.md` を読み込む。
    - 「ドキュメントにはあるがコードにはない機能」や「コードにはあるがドキュメントにはない機能」をリストアップする。

### Phase 2: Orient (状況判断・地図設計)

**目的:** 特定されたGapを埋めるための「新しい地図」の構成案を作成する。

1.  **Domain Modeling (用語と境界の整理):**
    - `activate_skill{name: "domain-modeling"}`
    - コード内で使われている用語（クラス名、変数名）と、ビジネス用語（Ubiquitous Language）の対応関係を整理する。
    - システムの境界線（Boundaries）を再定義する。

2.  **Hypothesis & Options (境界・構造の仮説立案):**
    - `activate_skill{name: "context-hypothesis"}`
    - 発見されたGapを解消するための解決策（境界の再定義、コンポーネントの分割等）を、以下の3つの視点で立案・分析する。
      - **実証的仮説 (Grounded):** 確定しているビジネス要件と外部制約（事実）に基づき、システムが果たすべき責任範囲を正確に定義する堅実案。
      - **飛躍的仮説 (Leap):** システムの将来的な拡張性や、あるべき理想の境界線を先回りして提示する理想追求案。
      - **逆説的仮説 (Paradoxical):** 既存のシステム境界や依存関係を根本から見直し、構造を劇的にシンプル化する破壊的提案。

3.  **Visualization Strategy (図解の構想):**
    - `activate_skill{name: "context-diagram"}`
    - システムの全体像を表す C4 Context Diagram (Mermaid) の更新案を作成する。
    - 外部システム（User, External System）との関係性が正しく表現されているか確認する。

### Phase 3: Decide (合意形成・収束)

**目的:** 更新内容についてユーザーと合意する。

1.  **Gap Resolution (論点整理):**
    - `activate_skill{name: "decision-support"}`
    - Phase 1で見つかったGapのうち、「ドキュメントを直すべきか（コードが正）」、「コードを直すべきか（ドキュメントが正）」、あるいは「どちらも修正が必要か」を判断する。
    - ユーザーに問いかけ、SSOTとしてあるべき姿を確定させる。

### Phase 4: Act (記述・実行)

**目的:** 決定事項をドキュメントに反映し、SSOTを更新する。

ユーザーに対し、以下の2択からアクションを選択してもらい実行する。

1.  **Option A: Work in Progress (記述・レビュー・保存)**
    - **ドラフトを作成し、フィードバックを得る。**
    - `activate_skill{name: "context-drafting"}`
      - `docs/system-context.md` を更新する。
      - Phase 2で作図したMermaid図を埋め込む。
    - **Self-Review:**
      - `activate_skill{name: "context-review"}`
      - 作成したドキュメントを監査し、コードとの乖離や抽象度のミスを自動修正する。
    - `activate_skill{name: "github-commit"}` (保存)
    - コミット後、再度 Orient に戻るか Act を続けるかを確認する。

2.  **Option B: Done (完了・PR・次へ)**
    - 内容が承認され、SSOTの更新を完了する場合。
    - `activate_skill{name: "github-pull-request"}` (PR作成)
    - **Retrospective:**
      `activate_skill{name: "retrospective"}`
      - ドキュメント維持プロセスの効率と品質を振り返る。

## 禁止事項 (Anti-Patterns)

- **Ignoring Reality:** コードの実態を無視して、理想だけのドキュメントを作ってはならない。
- **Over-Complexity:** システムコンテキスト図（Level 1）に、詳細なクラス設計（Level 3/4）の情報を詰め込んではならない。
- **Silent Update:** ユーザーの合意なしに、用語の定義やシステムの境界を勝手に変更してはならない。

## アウトプット形式 (Final Report)

全工程完了時の報告。

```markdown
## コンテキスト更新完了 (OODA Loop Completed)

- **Phase 1 (Observe):** [特定されたGap]
- **Phase 2 (Orient):** [再定義された境界/モデル]
- **Phase 3 (Decide):** [解決方針]
- **Phase 4 (Act):**
  - **Updated File:** `docs/system-context.md`
  - **PR:** #<Number>
```
