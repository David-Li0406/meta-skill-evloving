---
name: adr-drafting
description: Replaces the work of drafting determined architectural hypotheses into logical and detailed ADR documents following standard formats. Typical use cases: (1) Recording the background, reasoning, and impact of decisions as a "story" for future developers, (2) Citing reconnaissance facts from the current codebase to justify solutions, (3) Articulating not only benefits but also trade-offs and residual risks (4 Big Risks) transparently.
---

# ADR起草 (ADR Drafting)

決定されたアーキテクチャ仮説を、プロジェクト標準のフォーマット（ADR）に従って正式なドキュメントとして記述するスキル。
単なる記録ではなく、**「未来の開発者（あるいは自分）への手紙」** として、背景・理由・影響を論理的かつ情熱を持って記述する。

## 役割定義 (Role Definition)

あなたは **Scribe (書記)** ですが、同時に **Storyteller (語り部)** でもあります。
`SYSTEM_ARCHITECT` の価値観に基づき、決定に至るまでの文脈と、その決定がもたらす未来を明確に描きます。

## 前提 (Prerequisites)

- 意思決定（Decision）が完了しており、採用する案と理由が明確であること。
- テンプレート (`reqs/design/template/adr.md` 等) が存在すること。

## 手順 (Procedure)

### 1. テンプレートの準備 (Preparation)

- **Action:**
  - `read_file` を使用して `reqs/design/template/` から適切なテンプレートを読み込む。
  - 出力先のファイル名を決定する（例: `reqs/design/_inbox/adr-XXX-title.md`）。

### 2. ドラフト作成 (Drafting Guidelines)

テンプレートの各セクションを、以下のガイドラインに従って記述する。

#### Context (背景と課題)

- **[Context Analysis]:** 「なぜ今、この決定が必要なのか？」をビジネスと技術の両面から記述する。
- **[Active Reconnaissance]:** `active-reconnaissance` スキルで得られた現状のコードやシステムが抱える具体的な問題点（事実）を引用する。
- **[Outcome-Oriented]:** 技術的な問題だけでなく、それがユーザー体験やビジネスにどう悪影響を与えているかを書く。

#### Decision (決定事項)

- **[Hypothesis-Driven]:** 採用した案を明確に宣言する（「案Aを採用する」）。
- **[Rationale]:** なぜその案を選んだのか、決定打となった理由（キードライバー）を論理的に説明する。
- **[Clean Architecture]:** その決定が依存性のルールや責務の分離にどう寄与するかを言及する。
- **[DDD]:** `activate_skill{name: "domain-modeling"}` で定義されたユビキタス言語を使用して記述する。

#### Consequences (影響と結果)

- **[Trade-offs]:** メリット（Positive）だけでなく、デメリット（Negative）やリスクを隠さずに書く。「銀の弾丸はない」ことを前提とする。
- **[4 Big Risks]:** 価値・実現性・ユーザビリティ・生存性の観点で、残存するリスクがあれば明記する。
- **[Evolutionary]:** この決定が将来の拡張や変更にどう影響するか（あるいはどう制限するか）を記述する。

#### Alternatives (検討した代替案)

- **[Comparison]:** 却下した案（案B:飛躍的、案C:逆説的 など）についても、「なぜ選ばなかったか」の理由を敬意を持って記録する。将来、状況が変わった時のための重要な手がかりとなる。

### 3. ファイル作成 (File Creation)

- **Action:**
  - `write_file` を使用してファイルを新規作成する。
  - 作成後、以下のチェックリストで内容を自己監査する。（より厳密なレビューが必要な場合は `activate_skill{name: "adr-review"}` を使用すること）

- **Checklist (MECE & Lean):**
  - [ ] **[Completeness (抜け漏れなし)]**
    - 決定に必要な「前提（Context）」「結論（Decision）」「理由（Rationale）」「影響（Consequences）」が全て記述されているか。
    - 空欄（TBD）や「後で決める」といった記述が残っていないか（決定できないならADRにすべきではない）。
  - [ ] **[Lean (無理無駄なし)]**
    - 将来の実装において、オーバーエンジニアリング（YAGNI違反）になる要素が含まれていないか。
    - 逆に、必要な拡張性が考慮されておらず、すぐに作り直しになるような「無理（短視眼的決定）」がないか。
  - [ ] **[Clarity (明瞭性)]**
    - 第三者が読んだとき、その決定に至るロジックを再現できるか。
    - 専門用語はユビキタス言語で統一され、曖昧な表現（「よしなに」「適宜」）は排除されているか。

## 完了条件 (Definition of Done)

- 指定されたパスにADRファイルが作成され、SYSTEM_ARCHITECTの価値観およびMECE/Leanの観点を満たした内容で記述されていること。
