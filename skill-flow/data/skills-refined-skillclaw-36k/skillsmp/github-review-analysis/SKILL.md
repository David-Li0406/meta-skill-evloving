---
name: github-review-analysis
description: Replaces the task of analyzing and categorizing PR review comments and formulating executable fix plans. Typical use cases: (1) Automatically checking unresolved comments against surrounding code and SSOT consistency, (2) Categorizing feedback into "Accept, Discuss, or Explain" to clarify response policies, (3) Generating analysis reports including specific fix plans and executing fixes autonomously.
---

# GitHub Review Analysis

プルリクエストについたレビューコメントを読み込み、内容を分析し、対応方針を決定して実行に移すためのスキル。
コメントを「受諾（Accept）」「議論（Discuss）」「説明（Explain）」に分類し、必要な処置を体系的に行う。

## 役割定義 (Role Definition)
あなたは **Review Analyst (レビュー分析官)** です。
レビュアーの指摘を鵜呑みにせず、プロジェクトのSSOT（System Context, ADR, 規約）と照合し、妥当性を判断した上で最適なアクションを導き出します。

## 前提 (Prerequisites)
- 対象のプルリクエスト番号（`PR #X`）が判明していること。

## 手順 (Procedure)

### 1. 指摘の収集 (Fetch & Observe)
- **Action:**
  - `pull_request_read(method="get_review_comments")` を実行し、未解決のレビューコメントを取得する。
  - 指摘されたファイルや関連するコード/ドキュメントを `read_file` し、コンテキストを把握する。

### 2. 分析と分類 (Analyze & Categorize)
各コメントを以下の基準で分類し、対応方針を決定する。

| Category | Description | Action |
| :--- | :--- | :--- |
| **Accept (受諾)** | 明らかなバグ、タイポ、規約違反、または妥当な改善提案。 | **修正**を行う。 |
| **Discuss (議論)** | 意図が不明確、副作用の懸念がある、または別解が存在する場合。 | 論点を整理し、**ユーザーに判断を仰ぐ**。 |
| **Explain (説明)** | 指摘がSSOTや既存の決定（ADR）と矛盾する場合、または意図的なトレードオフである場合。 | コードは修正せず、**返信コメント案**を作成する。 |

### 3. レポート作成と実行計画 (Report & Plan)
分析結果を以下のテンプレートで出力し、方針を提示する。
**「Accept」の項目については、レポート提示後に直ちに修正作業へ移行してよいかユーザーに確認、または自律的に修正を開始する。**

## アウトプット形式 (Analysis Report)

```markdown
## Review Analysis Report: PR #<Number>

### Summary
- **Total Comments:** <N>
- **Accept:** <N> (修正対象)
- **Discuss/Explain:** <N> (要確認)

### Details

#### 1. [Accept] <File Path> (L<Line>)
- **Comment:** "<Summary of comment>"
- **Reason:** タイポ修正のため / <Doc>の記述と整合させるため。
- **Plan:** <具体的な修正内容>

#### 2. [Discuss] <File Path> (L<Line>)
- **Comment:** "..."
- **Analysis:** レビュアーはAを提案していますが、ADR-XXXではBを採用しています。
- **Question:** Aに変更しますか？ それともADRに基づいてBを維持（説明）しますか？

...
```

## 完了条件 (Definition of Done)
- 全てのコメントに対して分類（Category）と方針（Plan）が決定されていること。
- レポートが出力されていること。