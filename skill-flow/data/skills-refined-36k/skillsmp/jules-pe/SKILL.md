---
name: jules-pe
description: Jules（Gemini エージェント）にプロンプト生成を委譲するためのスキル
hegemonikon: Praxis-H
trigger:
  - プロンプト生成を Jules に
  - Jules でプロンプト
  - PE を Jules で
---

# Jules PE Skill

## 概要

このスキルは、プロンプト生成タスクを **Jules（Gemini エージェント）** に委譲するための実験的なスキルです。

## 仮説

Antigravity Runtime は `.agent/skills/` と `AGENTS.md` のルールを読み込み、タスクに応じて適切なエージェントを選択する可能性がある。

## 使用方法

### 1. AGENTS.md にルールを追加

プロジェクトルートに `AGENTS.md` を作成し、以下のルールを記述:

```markdown
## プロンプト生成タスクのルーティング

When the task involves generating prompts (*.prompt files):
- Prefer Gemini 3 Pro for generation tasks
- Use Claude for design and review tasks
- Follow the Prompt-Lang v2 specification
```

### 2. このスキルの発動条件

以下のキーワードでこのスキルが発動:
- 「プロンプト生成を Jules に」
- 「Jules でプロンプト」
- 「PE を Jules で」

### 3. 実行フロー

```
Claude（設計）
  ↓ 指示書を .ai/JULIUS_TASK.md に出力
  ↓
Runtime がルールを解析
  ↓ 「プロンプト生成 → Gemini 優先」を検出
  ↓
Jules/Gemini（生成）
  ↓ .prompt ファイルを生成
  ↓
Claude（検証）
  ↓ パーサーで検証
```

---

## 指示書テンプレート

Jules に渡す指示書（`.ai/JULIUS_TASK.md`）のテンプレート:

```markdown
# Prompt Generation Task

## Task Type
Prompt Engineering (PE)

## Requirements
### Phase 0 分析結果
- **Archetype**: [Precision / Speed / Autonomy / Creative / Safety]
- **勝利条件**: [何を最大化するか]

### Prompt-Lang 要件
- @role: [役割の定義]
- @goal: [目標の定義]
- @context: [リソースの種類]
- @rubric: [評価次元数]

## Output
- **ファイルパス**: forge/prompt-lang/prompts/[name].prompt
- **フォーマット**: Prompt-Lang v2

## References
- `docs/specs/prompt-lang-v2-spec.md`
- `.agent/skills/utils/meta-prompt-generator/SKILL.md`

## Success Criteria
- [ ] パーサーでエラーなくパース
- [ ] @rubric が 4次元以上
- [ ] @examples が詳細
```

---

## 検証コマンド

```bash
# 生成されたプロンプトを検証
python M:\Hegemonikon\forge\prompt-lang\prompt_lang.py parse [ファイルパス]
```

---

## 実験ステータス

**実験中** — Runtime が AGENTS.md のルールを読み込んで Jules を優先するか検証中
