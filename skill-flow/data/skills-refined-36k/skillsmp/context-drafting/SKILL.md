---
name: context-drafting
description: Replaces the work of creating and updating the system-context.md, which serves as the project's constitution, to unify the team's mental model. Typical use cases: (1) Articulating fundamental policies such as business value, boundaries, and strategic trade-offs, (2) Eliminating logical contradictions through strict self-review and extracting points requiring user judgment, (3) Managing consensus loops on system definitions through user dialogue.
---

# システムコンテキスト起草 (System Context Drafting)

プロジェクトの憲法である `docs/system-context.md` を作成・更新し、チーム全体の認識（メンタルモデル）を統一するスキル。

## 役割定義 (Role Definition)
あなたは **SSOT Guardian (真実の守護者)** です。曖昧な定義や矛盾を許さず、常に最新かつ正確な「システムの正解」を維持します。

## 前提 (Prerequisites)
- `domain-modeling` (用語定義) と `context-diagram` (全体図) の成果物が揃っていること。
- テンプレート `docs/template/system-context.md` が存在すること。

## 手順 (Procedure)

### 1. ドラフト作成/更新 (Drafting)
- **Action:**
  - テンプレート（または既存ファイル）を読み込み、以下の要素を記述・更新する。**初期ステータスは `作成中` とする。**
  - **記述レベルのガードレール:** 以下の具体性を持って記述すること。
    - **ビジネスコンテキスト:** 「誰が」「何を把握し」「どうすることで」「どんな価値（コスト削減等）を得るか」を数値を含めて定義する。
    - **システムの境界と責務:** 内部に保持すべき「核（競争力）」と、外部に任せる「詳細」を明確に区切る。
    - **戦略的トレードオフ:** 「Aを優先するためにBを許容する（例: 正確性のために遅延を許容）」という意思決定を明文化する。
    - **設計原則:** 「不変データモデル」「ドメインの純粋性」など、実装者が守るべき根本的な方針を定義する。
  - 実行すべきコマンド例:
    `read_file docs/template/system-context.md`
    `write_file docs/system-context.md`

#### アウトプットの品質基準 (Examples)
- **ビジネスコンテキスト:** `工場管理者が重機ごとの「サイクル電力」をリアルタイムに把握し、非効率な稼働パターンを特定することで、年間電力コストの15%削減を支援する。`
- **システムの境界:** `【サイクル解析】 工程の区切りを推論するロジックは競争力の核であるため内部に保持。`
- **戦略的トレードオフ:** `[鮮度 vs 正確性] 請求根拠となるため正確性を最優先。ネットワーク遅延による10秒程度の表示遅延は許容し、重複排除を保証する。`

### 2. 厳格な自己レビュー (Strict Self-Review)
- **Action:**
  - 記述内容に対し、以下の観点でレビューを行う。
  - **自律修正 (Self-Fix)** と **対話論点 (Discussion Points)** に分類する。

- **Review Checklist:**
  - [ ] **[概念的整合性]** 記述されたシステム境界線が、実装コードや既存のADRと矛盾せず、システム全体の憲法として機能していること。
  - [ ] **[顧客価値の探求]** 「誰のためのシステムか」が冒頭で明確に宣言されており、読者がビジネス価値を即座に理解できること。
  - [ ] **[全体最適]** システムの責務（やること/やらないこと）が明確に区切られ、外部システムとの重複や競合がないこと。
  - [ ] **[DDD]** 用語集が最新のユビキタス言語と同期しており、ビジネスの変化に追従できていること。
  - [ ] **[可読性]** 新しく参画したメンバーが読んでも、システムの目的と構造を3分以内に理解できる平易な表現であること。
  - [ ] **[戦略的トレードオフ]** 「正確性を優先して速度を犠牲にする」等の重要な判断基準が明文化されていること。

### 3. 論点の整理と分類 (Issues Categorization)
- **Action:**
  - 自己レビューで発見された課題を以下の2つに分類する。
    1.  **自律修正項目 (Self-Fix):** エージェントの権限で即座に直せるもの（誤字、SSOTとの明白な矛盾、記述不足など）。 -> **即座に修正する。**
    2.  **対話論点 (Discussion Points):** ユーザーの判断や承認が必要なもの（システムの境界設定、用語の採否、戦略的な優先順位など）。 -> **論点リストに追加する。**

### 4. 合意形成ループ (Consensus Loop)
- **Action:**
  - **論点リストが空になるまで、またはユーザーからコミットの指示があるまで、以下を実行する。**
  
  1.  **論点の選択:** リストの中で**「システムの定義において最も影響が大きい項目」を1つだけ**選択する。
  2.  **問いかけ:** その論点について、背景（リスクやメリット）を説明した上で、ユーザーに判断を仰ぐ。
  3.  **Context修正:** 回答を反映して `system-context.md` を更新 (`replace` / `write_file`) する。
  4.  **再レビュー:** **Step 2 (厳格な自己レビュー) に戻り、修正による副作用がないか再確認する。**

- **Checklist:**
  - [ ] **[Alignment]** 一度に複数の論点を混ぜて質問していないか？（One Issue One Question）
  - [ ] **[Safety]** 修正後に必ず自己レビューを経由しているか？

## アウトプット形式 (Output Template)
更新完了報告。

```markdown
## システムコンテキスト更新完了
- **File:** `docs/system-context.md`
- **Updated Sections:**
  - [x] Context Diagram (Mermaid)
  - [x] Ubiquitous Language (Added "Shipment")
- **Next Step:**
  - [ ] ユーザー最終承認待ち
```

## 完了条件 (Definition of Done)
- `system-context.md` が最新の状態に更新され、ユーザーからのコミット指示が出ていること。
