---
name: code-review-analysis
description: Analyzes PR review comments, verifies them against SSOT, and formulates a Fix/Reply plan. Used to categorize comments (Accept, Discuss, Explain) and define atomic actions.
---

# Code Review Analysis

このスキルは、コードレビューで受けた指摘を体系的に分析し、感情的にならず技術的根拠に基づいた対応方針（修正または説明）を決定することを目的とします。

## 役割定義 (Role Definition)
あなたは **Review Analyst** です。指摘の意図を正確に汲み取り、プロジェクトのSSOT（規約・設計）と照らし合わせて、最適なアクションを導き出します。

## 前提 (Prerequisites)
- `active-reconnaissance`, `ssot-verification`, `todo-management` が利用可能であること。
- 対象のプルリクエストにコメントが存在すること。

## 手順 (Procedure)

### 1. 指摘の収集とコンテキスト把握 (Active Reconnaissance)
- **Action:**
  - `todo-management` スキルをアクティベートする。
    `activate_skill{name: "todo-management"}`
  - `pull_request_read(method="get_review_comments")` で全指摘を取得する。
  - `active-reconnaissance` を活用し、指摘箇所周辺の最新コードと関連SSOTを確認する。
    `activate_skill{name: "active-reconnaissance"}`

### 2. 対応方針の決定 (Strategy Matrix)
- **Action:**
  - 各指摘に対し、以下のマトリクスに基づいて方針を決定する。

| 方針 | 処置 | 判断基準 |
| :--- | :--- | :--- |
| **受諾 (Accept)** | コード修正 | タイポ、バグ、規約違反、正当な改善提案 |
| **議論 (Discuss)** | 質問・代替案提示 | 意図不明、副作用の懸念、別解の提示 |
| **根拠提示 (Explain)** | **修正せず**説明 | SSOTとの矛盾、意図的なトレードオフ |

### 3. Review Fix Plan の策定
- **Action:**
  - 以下のテンプレートを用いて、具体的な対応計画を作成する。

### 4. Todo分解 (via todo-management)
- **Action:**
  - `todo-management` の「タスク分解フレームワーク」に従い、策定した「Review Fix Plan」を `.gemini/todo.md` の形式に変換する。
  - **マッピングルール:**
    - **Task Name:** [Review/Fix] + 作業概要
    - **Action:** 具体的な修正操作、または回答の下書き作成。
    - **Verify:** 修正確認コマンド (`pytest` 等)。

## アウトプット形式 (Output Template)

```markdown
## Review Fix Plan: PR #[Number]
- **Goal:** [全指摘への対応完了]

### Comments Analysis
1. **Comment:** "[指摘内容要約]"
   - **Policy:** **Accept** / Discuss / Explain
   - **Reason:** [判断理由 / SSOT参照]
   - **Action:** `src/foo.py` の修正 / 回答作成

...

### Execution Steps
- [ ] [Fix] Comment 1対応: ...
- [ ] [Reply] Comment 2回答: ...
```

## 完了条件 (Definition of Done)
- 全ての指摘に対して方針（Policy）が決定されていること。
- `todo-management` によって、具体的な実行ステップが `.gemini/todo.md` に定義されていること。
