---
name: objective-setting
description: Replaces the work of translating abstract user intent into concrete and verifiable goals (SMART) for agent execution. Typical use cases: (1) Defining the Outcome (desired state) from conversations or Issues, (2) Breaking down goals into specific tool operations and parameter levels, (3) Defining verification commands and expected results for objective determination.
---

# 目標設定 (Objective Setting)

ユーザーの会話やIssueから目標を特定し、**エージェント向けSMARTの法則**に基づいて、自律的な行動が可能なレベルまで具体化する。

## プロセス (Process)

### 1. 意図の把握

`activate_skill{name: "objective-analysis"}` を実行し、ユーザーの真の意図と背景を理解する。

### 2. エージェント向けSMART分析 (Agent-SMART Analysis)

把握した意図を、エージェントが「抜け・漏れ・無理・無駄」なく自律実行できる観点で構造化する。

- **Specific (具体的アクションへの変換):**
  - 抽象的な意図を、使用する具体的なツールとパラメータ（ファイルパス、置換文字列等）のレベルまで落とし込めているか？
  - 「何を」だけでなく「どのツールでどう実行するか」が明確か。
- **Measurable (機械的な検証):**
  - 完了を判定するための具体的な検証コマンド（`pytest`, `ls`, `grep` 等）と、期待される実行結果が定義されているか？
  - 人間の目視確認に頼らず、機械的に「成功」を判定できるか。
- **Achievable (コンテキストの充足):**
  - その操作を行うために必要な情報（ファイルの内容、ログ、SSOTの定義）は既に手元にあるか？
  - 情報不足のまま実行（無理）しようとしていないか。不足しているなら目標を「調査」に切り替える。
- **Relevant (スコープの厳守):**
  - ユーザーの要求に対して「過剰」または「不足」していないか。要求に直結する最小限の変更（無駄の排除）か。
  - プロジェクトの規約やアーキテクチャ方針を逸脱していないか。
- **Time-boxed (1ターン完結):**
  - 1回の応答ターン内で確実にアウトプットを出し切れるサイズか。
  - 複雑すぎる場合は、1ターンで完遂可能な小さなステップに分解されているか。

### 3. 目標の洗練 (Refine with Review)

`activate_skill{name: "objective-review"}` を実行し、設定した目標を自己レビューする。
