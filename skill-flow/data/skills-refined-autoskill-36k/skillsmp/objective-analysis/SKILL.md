---
name: objective-analysis
description: Replaces the work of extracting the true intent behind user statements or Issues and formulating multi-perspective solution hypotheses. Typical use cases: (1) Structuring information using the 5W1H framework, (2) Formulating grounded, leap, and paradoxical hypotheses by integrating current status and SSOT, (3) Identifying missing information (Unknowns) required to verify hypotheses.
---

# 目的分析 (Objective Analysis)

ユーザーの発言やIssueの記述から、純粋な意図と背景を読み取るスキル。
**5W1Hフレームワーク**を用いて情報を整理し、手元の情報を鵜呑みにせず、事実に基づいた**仮説**として意図を定義する。

## プロセス (Process)

### 1. 情報収集 (Gather Information)

- ユーザーの発言、チャット履歴、Issue記述全文を収集する。
- **必ずその時点の全てのSSOT（`docs/`、`reqs/`、最新コード）をチェックし**、前提知識を最新化する。

### 2. 情報整理 (Structure with 5W1H)

収集した情報を以下のフレームワークに沿って整理する（まだ解釈は加えず、事実を並べる）。

- **Why (目的・背景):** 解決したい本質的課題、期待される価値。
- **What (要件・ゴール):** 最終的な完了状態、成果物。
- **Where (対象範囲):** 対象機能、ファイル、影響範囲。
- **Who (利用者):** ターゲットユーザー。
- **When (時期・優先度):** 緊急度、依存関係。
- **How (手段・制約):** 指定技術、制約条件。

### 3. 多角的仮説立案 (Hypothesize)

整理した事実とSSOTの知識を統合し、ユーザーの「真の意図」について性質の異なる3つの仮説を立てる。

1.  **実証的仮説 (Grounded Hypothesis):**
    - 整理した事実を積み上げた、最も論理的で順当な仮説。
    - 「AだからBである」という直接的な因果に基づく。
2.  **飛躍的仮説 (Leap Hypothesis):**
    - 事実を根拠としつつも、潜在的なニーズや将来的な拡張性まで想像した大胆な仮説。
    - 「Aということは、将来的にはCも必要になるのではないか」という洞察を含む。
3.  **逆説的仮説 (Paradoxical Hypothesis):**
    - 表層的な事実とは一見矛盾するが、より深い目的達成のためには有効な仮説。
    - 「Aと言っているが、真の解決策はAをやめること（または全く別のDを行うこと）ではないか」という批判的視点。

### 4. 検証項目の策定 (Validation Questions)

それぞれの仮説の確からしさを判断するために必要な情報（Unknowns）を特定し、ユーザーへの質問や調査項目としてリストアップする。

- どの情報があれば仮説が確定するか？
- どの事実が間違っていたら仮説が崩れるか？
