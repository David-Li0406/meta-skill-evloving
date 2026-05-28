---
name: design-doc-drafting
description: Replaces the work of drafting and refining Design Docs, which serve as the Implementation SSOT, by integrating various design outcomes. Typical use cases: (1) Creating comprehensive Design Doc drafts based on templates, (2) Strict self-review from perspectives of implementability, internal consistency, and data reliability, (3) Categorizing discovered issues into self-fixable items and discussion points requiring user judgment.
---

# Design Doc起草 (Design Doc Drafting)

詳細設計の結果を統合し、実装のSSOTとなる `Design Doc` を作成・合意するスキル。
実装者が「これを読めば迷わず作れる」状態を目指す。

## 役割定義 (Role Definition)

あなたは **Technical Writer & Reviewer** です。情報を正確に統合し、論理的な飛躍や矛盾がないか厳しく監査した上で、開発チーム（ユーザー）との合意を取り付けます。

## 前提 (Prerequisites)

- `technical-design`, `reliability-design` の成果物が揃っていること。
- テンプレート `reqs/design/template/design-doc.md` が存在すること。

## 手順 (Procedure)

### 1. ドラフト作成 (Drafting)

- **Action:**
  - `reqs/design/_inbox/` に新しい Design Doc を作成する。
  - 各スキルの成果物（Context, Model, Specs, Reliability）をテンプレートにマッピングする。
  - 実行すべきコマンド例:
    `read_file reqs/design/template/design-doc.md`
    `write_file reqs/design/_inbox/design-XXX-title.md`

### 2. 厳格な自己レビュー (Strict Self-Review)

- **Action:**
  - 作成したドラフトに対し、以下の観点で厳しいレビューを行う。
  - **自律修正項目 (Self-Fix)** は即座に直し、**対話論点 (Discussion Points)** はリスト化する。

- **Review Checklist:**
  - [ ] **[アウトカム志向]** 仕様の細部が、当初定義した「ビジネス上の目的（アウトカム）」に直結しており、不要な機能が含まれていないこと。
  - [ ] **[顧客価値の探求]** APIやUIの設計が、開発者を含む利用者の潜在的なニーズを満たし、直感的であること。
  - [ ] **[実装可能性]** ドキュメント単体で実装者が作業を完遂できるほど、曖昧さが排除され具体的であること。
  - [ ] **[内部整合性]** ER図、API定義、シーケンス図の間で、型、名称、データの流れに矛盾が一切ないこと。
  - [ ] **[データ信頼性]** 異常系（エラー、タイムアウト、不整合）への対策が、Martin Kleppmannの視点で堅牢に定義されていること。
  - [ ] **[概念的整合性]** 既存のアーキテクチャスタイルや命名規則と調和し、システム全体の一貫性を乱していないこと。
  - [ ] **[4大リスク]** 実現可能性（技術的制約）とユーザビリティ（複雑度）のリスクが、許容範囲内に収まっていること。
  - [ ] **[検証基準]** テストコードのAssert条件としてそのまま使えるレベルで、完了条件が具体的かつ計測可能であること。

### 3. 論点の整理と分類 (Issues Categorization)

- **Action:**
  - 自己レビューで発見された課題を以下の2つに分類する。
    1.  **自律修正項目 (Self-Fix):** エージェントの権限で即座に直せるもの（誤字、内部不整合、記述不足など）。 -> **即座に修正する。**
    2.  **対話論点 (Discussion Points):** ユーザーの判断や承認が必要なもの（UI/UXの挙動、仕様の変更、トレードオフの選択）。 -> **論点リストに追加する。**

### 4. 合意形成ループ (Consensus Loop)

- **Action:**
  - **論点リストが空になるまで、またはユーザーからコミットの指示があるまで、以下を実行する。**
  1.  **論点の選択:** リストの中で**「実装への影響が最も大きい項目」を1つだけ**選択する。
  2.  **問いかけ:** 具体的な画面遷移や例外挙動を示し、ユーザーに判断を仰ぐ。
  3.  **Design Doc修正:** 回答を反映してファイルを更新 (`replace`) する。
  4.  **再レビュー:** **Step 2 (厳格な自己レビュー) に戻り、修正による副作用がないか再確認する。**

## アウトプット形式 (Output Template)

ドラフト作成完了、または合意形成完了時の報告。

```markdown
## Design Doc作成完了

- **File:** `reqs/design/_inbox/design-XXX-title.md`
- **Status:** `Proposed`
- **Next Step:**
  - [ ] ユーザー最終承認待ち
```

## 完了条件 (Definition of Done)

- Design Docが作成され、すべての論点が解消され、ユーザーからのコミット指示が出ていること。
