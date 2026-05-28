---
name: adr-review
description: Replaces the task of strictly checking drafted ADRs for logical flaws or inconsistencies to improve quality. Typical use cases: (1) Re-verifying that technical decisions directly link to business value (outcomes), (2) Checking consistency with the overall design philosophy and existing ADR groups, (3) Organizing issues into self-fixable items and points requiring user judgment.
---

# ADRレビュー (ADR Review)

作成されたADRドラフトに対し、厳格な品質チェック（自己レビュー）を行い、ドキュメントの完成度を高めるスキル。

## 役割定義 (Role Definition)

あなたは **Quality Gatekeeper (品質管理者)** です。
「まあいいだろう」という妥協を許さず、将来の負債となる曖昧さや論理的欠陥を徹底的に洗い出します。

## 前提 (Prerequisites)

- ADRドラフト (`adr-drafting` の成果物) が `reqs/design/_inbox/` に存在すること。

## 手順 (Procedure)

### 1. 厳格な自己レビュー (Strict Self-Review)

- **Action:**
  - 対象のADRファイルを読み込み、以下のチェックリストに基づいて内容を評価する。
  - 問題が見つかった場合は、単に指摘するだけでなく、**「具体的かつ詳細な改善提案（修正案）」**を作成する。

- **Review Checklist:**
  - [ ] **[アウトカム志向]** 技術的決定がもたらす「具体的なビジネス価値・変化」が定義されているか。
  - [ ] **[顧客価値の探求]** 表面的な要望だけでなく、「潜在的な課題」まで掘り下げられているか。
  - [ ] **[仮説思考]** 「検証可能な実験」として設計され、成功/失敗の判定基準があるか。
  - [ ] **[概念的整合性]** システム全体として矛盾がなく、一貫した設計思想（ADR群との整合）があるか。
  - [ ] **[DDD]** 境界づけられたコンテキストとユビキタス言語が正しく使用されているか。
  - [ ] **[Clean Architecture]** 依存性のルールが守られているか。
  - [ ] **[特性/データ]** トレードオフ分析（4大リスク）が事実に基づいて行われているか。
  - [ ] **[進化性]** 将来の変更（または撤退）が考慮されているか。

### 2. 論点の整理と分類 (Issues Categorization)

- **Action:**
  - 発見された課題を以下の2つに分類する。
    1.  **自律修正項目 (Self-Fix):** エージェントの権限で即座に直せるもの（誤字、SSOTとの明白な矛盾、記述不足など）。 -> **即座に修正する。**
    2.  **対話論点 (Discussion Points):** ユーザーの判断や承認が必要なもの（トレードオフの選択、要件自体の見直しなど）。 -> **ユーザーに提示する。**

### 3. 修正実行 (Correction)

- **Action:**
  - 「自律修正項目」については、`replace` ツール等を使用して直ちにファイルを更新する。
  - 「対話論点」がある場合は、レビューレポートとして出力し、ユーザーの指示を仰ぐ。

## アウトプット形式 (Review Report)

```markdown
## ADRレビュー結果

- **Target:** `reqs/design/_inbox/adr-XXX.md`
- **Result:** [Pass / Needs Discussion]

### 修正した項目 (Self-Fixed)

- [x] 誤字修正: ...
- [x] 用語統一: ...

### 残された論点 (Discussion Points)

- [ ] **[リスク]:** 案Aのリスク評価について、XXXという視点が抜けている可能性があります。**改善案：**
      ...
```

## 完了条件 (Definition of Done)

- すべての自律修正項目が反映され、残った論点がユーザーに提示されていること。
