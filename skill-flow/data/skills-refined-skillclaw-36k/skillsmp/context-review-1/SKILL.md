---
name: context-review
description: Replaces the task of auditing whether the updated system context accurately reflects the "real code" to ensure reliability. Typical use cases: (1) Verifying that described external system integrations match actual imports or API calls, (2) Checking for appropriate abstraction levels as C4 Context, (3) Ensuring no contradictions in terminology or relationships between Mermaid diagrams and text descriptions.
---

# システムコンテキストレビュー (Context Review)

作成または更新された `system-context.md` に対し、厳格な品質チェック（自己レビュー）を行い、ドキュメントの信頼性を高めるスキル。

## 役割定義 (Role Definition)

あなたは **Map Auditor (地図監査人)** です。
「地図（ドキュメント）」が「現実（コード）」を正確に映し出しているか、そして旅行者（開発者）にとって分かりやすいかを徹底的に検証します。

## 前提 (Prerequisites)

- システムコンテキストのドラフト (`context-drafting` の成果物) が存在すること。
- 最新のコードベースの状態が把握できていること（`active-reconnaissance` 済みであること）。

## 手順 (Procedure)

### 1. 厳格な自己レビュー (Strict Self-Review)

- **Action:**
  - 対象の `docs/system-context.md` を読み込み、以下のチェックリストに基づいて内容を評価する。
  - 問題が見つかった場合は、単に指摘するだけでなく、**「具体的かつ詳細な改善提案（修正案）」**を作成する。

- **Review Checklist:**
  - [ ] **[Reality Alignment]** 記述されている外部システム連携やコンポーネントが、実際のコード（import, 設定ファイル, API call）と一致しているか。**嘘や願望が含まれていないか。**
  - [ ] **[Abstraction Level]** C4 Context (Level 1) として適切な抽象度か。内部の詳細すぎるクラス設計などが混ざっていないか。
  - [ ] **[Ubiquitous Language]** コード内で使用されている用語と、ドキュメントの用語が一致しているか。
  - [ ] **[Boundary Clarity]** システムの境界線（どこまでが自システムで、どこからが外部か）が明確に定義されているか。
  - [ ] **[Completeness]** 主要なアクター（User, Admin, External System）が漏れなく記述されているか。
  - [ ] **[Visual Consistency]** Mermaid図とテキストの記述に矛盾がないか。

### 2. 論点の整理と分類 (Issues Categorization)

- **Action:**
  - 発見された課題を以下の2つに分類する。
    1.  **自律修正項目 (Self-Fix):** エージェントの権限で即座に直せるもの（誤字、コードとの明白な矛盾、Mermaid記法エラーなど）。 -> **即座に修正する。**
    2.  **対話論点 (Discussion Points):** ユーザーの判断や承認が必要なもの（システム境界の変更、用語の再定義、不明瞭な外部連携の扱いなど）。 -> **ユーザーに提示する。**

### 3. 修正実行 (Correction)

- **Action:**
  - 「自律修正項目」については、`replace` ツール等を使用して直ちにファイルを更新する。
  - 「対話論点」がある場合は、レビューレポートとして出力し、ユーザーの指示を仰ぐ。

## アウトプット形式 (Review Report)

```markdown
## Contextレビュー結果

- **Target:** `docs/system-context.md`
- **Result:** [Pass / Needs Discussion]

### 修正した項目 (Self-Fixed)

- [x] Mermaid構文エラー修正: ...
- [x] 外部システム名の統一（コードに合わせて修正）: ...

### 残された論点 (Discussion Points)

- [ ] **[境界]:** "Payment Gateway" を外部システムとして扱うか、内部モジュールとして扱うか、コードの実装とドキュメントで解釈が揺れています。
      **提案：** `infra/payment` パッケージの実装を見る限り、外部APIラッパーであるため、Context図では「外部システム」として明示すべきです。
```

## 完了条件 (Definition of Done)

- すべての自律修正項目が反映され、残った論点がユーザーに提示されていること。
