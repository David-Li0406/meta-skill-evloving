---
name: active-reconnaissance
description: Replaces the work of actively investigating and identifying gaps between the ideal (user request) and reality (code/documents). Typical use cases: (1) Uncovering existing ADRs or constraints that contradict requests, (2) Identifying specific code or paths affected by abstract requests, (3) Initial risk assessment based on feasibility and technical debt.
---

# 能動的偵察 (Active Reconnaissance)

ユーザーの「こうしたい（理想）」という依頼に対し、プロジェクトの「こうなっている（現実）」を能動的に調査し、その間の**ギャップ（乖離）**を特定するスキル。
新しいADR（アーキテクチャ意思決定）を起草する前に、推測ではなく事実に基づいたコンテキストを構築することを目的とする。

## 役割定義 (Role Definition)

あなたは **Detective (探偵)** です。ユーザーの依頼という「証言」と、コードやADRという「現場の証拠」を照らし合わせ、そこに潜む矛盾や未解決の課題を洗い出します。

## 前提 (Prerequisites)

- ユーザーからの新しい機能追加、変更、または設計に関する依頼があること。

## 手順 (Procedure)

### 1. 意図の抽出 (Intent Extraction)

- **Action:**
  - `objective-analysis` スキルを活用し、ユーザーの依頼から「何を変えたいのか（理想の状態）」を抽出する。
    `activate_skill{name: "objective-analysis"}`
- **Checklist:**
  - [ ] **[Alignment]** ユーザーが解決したい本質的な課題は何かを定義したか？

### 2. 現状の証拠収集 (Reality Scouting)

- **Action:**
  - 依頼に関連する既存の決定（ADR）と実装コードを調査し、現実の状態を把握する。
  - 実行すべきコマンド例:
    `read_file docs/system-context.md`
    `ls reqs/design/_approved/`
    `search_code --pattern "<related_keyword>"`
    `read_file <relevant_files>`

- **Checklist:**
  - [ ] **[Context]** 依頼内容と衝突する、または制約となる既存のADRはあるか？
  - [ ] **[Context]** 実際のコード実装は、ドキュメントの記述（SSOT）と一致しているか？

### 3. ギャップ分析 (Gap Analysis)

- **Action:**
  - ユーザーの理想（Step 1）とプロジェクトの現実（Step 2）を比較し、具体的な乖離（ギャップ）を特定する。
  - **安全性:** 「できるはず」という思い込みを排除し、不可能な制約や技術的負債による障害を浮き彫りにする。

- **Checklist:**
  - [ ] **[Safety]** ユーザーの認識（例：「簡単に変更できる」）と実態（例：「密結合で困難」）に乖離はないか？
  - [ ] **[Efficiency]** 既存の仕組みで解決できるのに、ユーザーが新しい仕組みを作ろうとしていないか？

### 4. 初期リスク評価 (Initial Risk Assessment)

- **Action:**
  - 特定されたギャップや要望に対し、以下の4大リスクの観点から初期評価を行う。
  - **リスクがある場合は、ラフドラフトの `Context` または `Problem` に明記する。**

- **Checklist:**
  - [ ] **価値 (Value):** 本当にユーザーやビジネスの価値向上に繋がるか？（無駄な機能ではないか？）
  - [ ] **ユーザビリティ (Usability):** その変更は利用者（開発者含む）にとって使いやすいか？
  - [ ] **実現可能性 (Feasibility):** 技術的・時間的制約の中で現実的に完了できるか？（技術的負債の影響は？）
  - [ ] **ビジネス生存性 (Viability):** 法務・コスト・セキュリティ上の致命的問題はないか？

## アウトプット形式 (Output Template)

偵察結果を元に、ラフドラフトを **ファイルとして作成** すること。
目的に応じてテンプレートと出力ファイル名を切り替える。

1.  **テンプレート選択:**
    - **ADRの場合:** `reqs/design/template/adr.md`
    - **Design Docの場合:** `reqs/design/template/design-doc.md`
2.  **ドラフト作成:** テンプレートの内容を読み込み、調査結果を埋めて `reqs/design/_inbox/` に保存する。
    - **ADR:** `adr-XXX-<title>.md`
    - **Design Doc:** `design-XXX-<title>.md`
3.  **記述内容:**
    - **Context/Background:** ユーザーの意図、関連する既存決定、現状の実装状況、初期リスク評価の結果。
    - **Problem/Issues:** 特定されたギャップ（論理的矛盾や技術的課題）。

```markdown
## 偵察完了報告

- **Rough Draft Created:** `reqs/design/_inbox/<file_name>.md`
- **Type:** ADR / Design Doc
- **Findings:**
  - ユーザーの要望は既存の [ADR-005] と矛盾するため、Problemセクションにその旨を記載しました。
  - 実装コードの現状（`src/auth/`）を Context に追記しました。
  - **リスク評価:** 実現可能性(Feasibility)に懸念があるため、Contextに詳細を記録しました。
```

## 完了条件 (Definition of Done)

- 目的に応じたドラフトファイル（ADRまたはDesign Doc）が作成され、現状認識とギャップが記述されていること。
