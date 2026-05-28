---
name: context-hypothesis
description: Replaces the design study of formulating and analyzing "verifiable hypotheses" that align with SSOT based on domain models and requirements. Typical use cases: (1) Proposing optimal solutions following Clean Architecture or DDD principles, (2) Constructing multi-perspective hypotheses from grounded, leap, and paradoxical viewpoints, (3) Comparing each proposal quantitatively and qualitatively based on 4 Big Risks (Value, Feasibility, UI, Viability).
---

# コンテキスト仮説立案 (Context Hypothesis)

ドメインモデルと要件に基づき、SSOTと整合する「検証可能な仮説（構造・境界・方針）」を立案し、代替案と比較分析するスキル。
ADR（アーキテクチャ決定）だけでなく、System Context（境界定義）や Design Doc（設計方針）の策定にも使用される。

## 役割定義 (Role Definition)

あなたは **Context Architect (コンテキスト・アーキテクト)** です。技術的な実現可能性だけでなく、ビジネス価値、運用コスト、将来の拡張性を含めた「全体最適」の視点で判断を下します。

## 前提 (Prerequisites)

- ドメインモデル (`domain-modeling` の成果物) が存在すること。
- 解決すべき課題と制約条件が明確であること。

## 手順 (Procedure)

### 1. 戦略的評価軸の選定 (Strategy Selection)

- **Action:**
  - 今回の意思決定において、特に重要視すべき **3つの設計原則（評価軸）** をリストから選択する。これが「実証的仮説」の設計思想の核となる。
    - **依存性:** Robert C. Martin (Clean Architecture)
    - **特性:** Mark Richards (Architecture Characteristics)
    - **データ:** Martin Kleppmann (Data Consistency)
    - **進化性:** Martin Fowler (Evolutionary Architecture)
    - **ドメイン:** Eric Evans (DDD) / 境界づけられたコンテキスト

### 2. 多角的仮説の構築 (Hypothesis Formulation)

- **Action:**
  - 以下の3つのアプローチで仮説を構築する。
    1.  **実証的仮説 (Grounded Hypothesis):**
        - **構築ロジック:** 現状の事実（Evidence）とSSOTに基づいた、最も堅実で論理的な「本命案」。
        - ドメインモデル、既存制約、現在のユーザー要望を最短距離で満たす構造を導き出す。

    2.  **飛躍的仮説 (Leap Hypothesis):**
        - **構築ロジック:** 「ユーザーは本当はここまでやりたいのではないか？」という潜在的な理想や長期的な野心にフォーカスした「理想追求案」。
        - 現在の制約を一度取り払い、提供価値を最大化するための飛躍的な構造を提示する。

    3.  **逆説的仮説 (Paradoxical Hypothesis):**
        - **構築ロジック:** 「パラダイムシフト」と「破壊的イノベーション」の視点に立ち、既存のルールや前提を覆す「ゲームチェンジ案」。
        - 一見すると非効率や非常識に見えるかもしれないが、既存の延長線上にはない別次元の価値（低コスト化、シンプル化、全く新しい体験）を創出する可能性を探る。

- **Checklist:**
  - [ ] **[Context]** 実証的仮説は既存のSSOT（既決事項）と矛盾していないか？（整合性チェック）
  - [ ] **[Alignment]** 3つの仮説はそれぞれ異なるトレードオフ（メリット/デメリット）を持っているか？

### 3. 比較分析と決定 (Comparison & Decision)

- **Action:**
  - 3つの仮説を **4大リスク（価値、実現性、ユーザビリティ、生存性）** で評価し、最も「無理・無駄・ムラ」が少ない案を採用する。
  - アウトプットの比較表を埋める。

## アウトプット形式 (Output Template)

比較分析の結果を以下の形式で出力し、呼び出し元のドキュメント（ADR, Context, Design Doc）に反映させる。

```markdown
## 仮説比較分析 (Hypothesis Analysis)

### 1. 採用した戦略（評価軸）

今回、以下の3点を最優先事項として設計を行いました。

1. **[原則名]:** (選定理由: 例「頻繁な仕様変更に耐えるため」)
2. **[原則名]:** ...
3. **[原則名]:** ...

### 2. 多角的仮説の比較

| 項目          | 実証的仮説 (Grounded)  | 飛躍的仮説 (Leap)    | 逆説的仮説 (Paradoxical) |
| :------------ | :--------------------- | :------------------- | :----------------------- |
| **設計思想**  | 事実に基づく論理的解決 | 潜在的ニーズへの飛躍 | 既存活用と別手段の統合   |
| **4大リスク** | (価値/実現/UI/生存)    | (価値/実現/UI/生存)  | (価値/実現/UI/生存)      |
| **判定**      | **採用 (Recommended)** | 却下 (理由...)       | 却下 (理由...)           |

### 3. 結論

実証的仮説を採用します。理由は、[原則名]を満たしつつ、飛躍的仮説のような[リスク]を回避し、逆説的仮説では満たせない[要件]をクリアできるためです。
```

## 完了条件 (Definition of Done)

- 推奨する案が論理的に導き出され、代替案との比較（4大リスクおよび設計原則に基づく）が明確に記述されていること。
