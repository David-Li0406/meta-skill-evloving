---
name: skill-creator
description: Replaces the work of presiding over the creation of new skills or refinement of existing ones to capitalize agent capabilities as reproducible knowledge. Typical use cases: (1) Formalizing successful retrospective patterns into generic skills, (2) Designing safety protocols (4 axes) for complex operations, (3) Building standard workflows for introducing new tools or frameworks.
---

# スキル作成 (Skill Creator)

新しいスキルを作成、または既存スキルを大幅に改修するためのメタスキル。
エージェントの能力を拡張し、暗黙知を**「再現可能な形式知（SKILL）」**として資産化する。

## プロセス (Process)

### 1. コンセプト定義 (Concept Definition)
作成前に、以下の項目を言語化し、スキルの存在意義を定義する。

- **Name:** スキル名（ケバブケース: `my-new-skill`）。
- **Description:** スキルの目的と、**代表的なユースケースを3つ**記述する。
- **Trigger:** いつ、どのような状況でこのスキルを呼び出すべきか？
- **Goal:** このスキルを実行した結果、どのような成果物や状態が得られるか？
- **Anti-Pattern:** このスキルが「やってはいけないこと」は何か？（精神論の禁止、危険な操作など）

### 2. 品質設計 (Quality Design with 4 Axes)
新しいスキルがプロジェクトの品質基準を満たすよう、以下の4軸で具体的なアクションを設計する。

1.  **安全性 (Safety):**
    - 破壊的な操作の前に、必ず確認ステップ（Dry Run, diff確認など）が含まれているか？
    - エラー発生時のリカバリ手順や、停止判断基準が明確か？
2.  **効率性 (Efficiency & Concreteness):**
    - 最小の手数で完了するためのツール選定（例: `grep` より `search_code`）がされているか？
    - **そのまま実行可能な具体的なコマンド例** (`run_shell_command{...}`) が記述されているか？
    - ユーザーの介入を減らし、自律的に判断できる情報収集プロセスがあるか？
3.  **コンテキスト (Context):**
    - プロジェクト固有のルール（SSOT, コーディング規約）を参照するステップが含まれているか？
    - 「一般的な正解」ではなく「このプロジェクトでの正解」を導き出すよう指示されているか？
4.  **合意形成 (Alignment):**
    - 実行前に計画を提示し、ユーザーの承認を得るプロセスが必要な箇所はどこか？
    - **期待されるアウトプット形式（Markdownテンプレート）** が定義されているか？
    - 完了条件（Definition of Done）が明確に定義されているか？

### 3. ドラフト作成 (Drafting)
以下の標準テンプレートを使用し、`.gemini/skills/<skill-name>/SKILL.md` を作成する。

#### スキルテンプレート
```markdown
---
name: <skill-name>
description: <Brief description of what this skill does and when to use it.>
---

# <Skill Title>

<スキルの概要と目的>

## 役割定義 (Role Definition)
あなたは <Role Name> です。<Context/Responsibility> を担当します。

## 前提 (Prerequisites)
- このスキルを使用するための前提条件や、必要な権限/ツール。

## 手順 (Procedure)

### 1. <Step Name>
- **Action:**
  - 具体的な行動指示。
  - 実行すべきコマンド例:
    `run_shell_command{command: "..."}`

- **Checklist:**
  - [ ] 確認事項1
  - [ ] 確認事項2

### 2. <Step Name> (Quality Gate)
- **Safety:** 安全性を担保するためのコマンド実行例（diff確認など）。
- **Context:** 参照すべきドキュメントや規約。

## アウトプット形式 (Output Template)
このスキルが完了した際、または重要な中間報告を行う際は、以下の形式で出力すること。

```markdown
## <Title>
- **Result:** ...
    - **Evidence:** ...
```

## 完了条件 (Definition of Done)
- このスキルが完了したと言える状態の定義。
```
