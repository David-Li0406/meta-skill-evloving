---
name: arch-refactoring
description: Replaces the "information organization" task of improving readability and consistency of architecture diagrams while maintaining accuracy. Typical use cases: (1) Optimizing cognitive load by minimizing crossing arrows and repositioning elements, (2) Grouping elements based on domain boundaries or Clean Architecture layers, (3) Visual standardization through fixing naming inconsistencies or adding legends.
---

# Architecture Refactoring

描かれた図を、情報の正確さを保ちつつ「誰が読んでも理解できる状態」へ昇華させるスキル。
`TECHNICAL_DESIGNER` の価値観（一貫性、明確性、視覚的伝達）に基づき、ノイズを排除し意図を際立たせる。

## 役割 (Role)

**Visual Architect (視覚的設計者)**
単に綺麗にするだけではない。Clean Architecture や DDD の概念に基づき、要素を適切にグルーピングし、認知負荷を下げる「情報の整理」を行う。

## 手順 (Procedure)

### 1. 認知負荷の最適化 (Cognitive Load Optimization)

- **Complexity Check:** 矢印の交差を最小化し、1つの図の主要要素を7±2個に収める。
- **Split Strategy:** 必要に応じて C4 Level ごとにファイルを分割する。

### 2. 意味ある構造化 (Semantic Grouping)

- **Domain Grouping:** ビジネス的な関連性が高い要素を `Boundary` で囲む。
- **Layer Grouping:** Clean Architecture のレイヤー（Infra, Interface, UseCase, Domain）ごとに配置を整理する。

### 3. 整合性と標準化 (Integrity & Standardization)

- **SSOT Check:** `activate_skill{name: "ssot-verification"}` を実行し、図がADRや上位設計と矛盾していないか確認する。
- **Annotation:** 循環参照や非推奨な依存関係には警告色の `Note` を配置する。
- **Legend:** 特殊な記法には凡例を追加する。
- **Mermaid Polish:** 配置方向（TB/LR）を調整し、視線の流れを自然にする。

### 4. 自己レビューと改善提案 (Self-Review & Proposal)

以下のチェックリストに基づき、図面とドキュメントの品質を自律的に向上させる。

- **Checklist & Proposal:**
  - [ ] **Simplicity (YAGNI):** 必須ではない複雑な詳細や、重複した記述はないか？
    - _Proposal:_ 不要な要素の削除や、冗長な記述の簡略化。
  - [ ] **Clean Architecture:** 図上の依存の方向（矢印）は正しいか？ レイヤーが適切に分離されているか？
    - _Proposal:_ 依存方向の修正や、適切な境界線（Boundary）の再設定。
  - [ ] **Naming (Ubiquitous Language):** 要素名はドメインの意図（Role）を正確に表しているか？
    - _Proposal:_ より適切な命名への変更、定義テキストの洗練。
  - [ ] **Readability:** 図の密度は適切か？ 注釈（Note）なしで構造を理解できるか？
    - _Proposal:_ 配置の最適化、複雑な部分の分解、または注釈の強化。
  - [ ] **User Value:** この図の詳細は、開発者が実装を判断するのに本当に役立つか？

- **Action:**
  - 提案の中から、**最も効果が高く、リスクが低い1つ**を選択し、宣言する。次ステップ（Iterate）へのインプットとする。

### 5. 反復 (Iterate)

- **Input:** Step 4 で選択された改善提案。
- **Action:**
  - 改善提案が存在する場合、それをターゲットとして `arch-drafting` を呼び出し、修正を行う。
    `activate_skill{name: "arch-drafting"}`
  - 改善提案がない（チェックリストが全てクリアされた）場合、リファクタリングサイクルを終了する。

## アウトプット (Output)

- 視覚的に整理され、意図が明確になった `docs/architecture/*.md`。
- (内容はDraftingフェーズから変更せず、表現のみを改善する)
