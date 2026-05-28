---
name: agent-scaffolder
description: "Use when user says 'agent を作りたい', 'create agent', 'scaffold agent', '新しい agent', 'agent 作成', or discusses creating a new climpt agent. Generates .agent/{name}/ directory with all required files including agent.json, steps_registry.json, schemas, and prompts."
allowed-tools: [Read, Write, Edit, Bash, Glob, AskUserQuestion]
---

# Agent Scaffolder

Climpt Agent の雛形を生成する Skill。

## 使用方法

### 1. 情報収集

ユーザーに以下を確認:

1. **Agent 名** (必須): kebab-case (例: `my-agent`, `code-reviewer`)
2. **説明**: Agent の目的
3. **completionType**: 完了条件の種類

### completionType 選択肢

| タイプ            | 用途                | 設定                  |
| ----------------- | ------------------- | --------------------- |
| `externalState`   | Issue/PR の状態監視 | `maxIterations`       |
| `iterationBudget` | 固定回数で終了      | `maxIterations`       |
| `keywordSignal`   | キーワードで終了    | `completionKeyword`   |
| `stepMachine`     | Step グラフで判定   | `steps_registry.json` |

### 2. Scaffolding 実行

```bash
deno run -A ${CLAUDE_PLUGIN_ROOT}/skills/agent-scaffolder/scripts/scaffold.ts \
  --name <agent-name> \
  --description "<説明>" \
  --completion-type <type>
```

### 3. 生成される構造

```
.agent/{agent-name}/
├── agent.json              # Agent 定義
├── steps_registry.json     # Step マッピング
├── schemas/
│   └── step_outputs.schema.json
└── prompts/
    ├── system.md
    └── steps/
        ├── initial/default/f_default.md       # Work step: 初期化
        ├── continuation/default/f_default.md  # Work step: 継続
        ├── verification/default/f_default.md  # Verification step: 検証
        └── closure/default/f_default.md       # Closure step: 完了
```

### 4. 次のステップ案内

生成後、ユーザーに以下を案内:

1. `prompts/system.md` を編集して Agent の役割を定義
2. `prompts/steps/` 配下の各プロンプトをカスタマイズ
3. 必要に応じて `steps_registry.json` に Step を追加
4. `deno run -A agents/scripts/run-agent.ts --agent {name} --dry-run` で検証

### 5. intentSchemaRef の形式

**重要**: `structuredGate.intentSchemaRef` は**解決済み Step スキーマ内**の
内部ポインタ (`#/properties/...`) を使用すること。Runner は `outputSchemaRef.schema`
で Step スキーマを解決した後に `intentSchemaRef` を適用するため、
`definitions` を含むパスは動作しない。

```json
// ✅ 正しい形式: 解決済みスキーマへのポインタ
"intentSchemaRef": "#/properties/next_action/properties/action"

// ❌ 禁止: definitions を含むパス（解決後に存在しない）
"intentSchemaRef": "#/definitions/initial.default/properties/next_action/properties/action"

// ❌ 禁止: 外部ファイル参照
"intentSchemaRef": "common.schema.json#/$defs/nextAction/properties/action"
```

共通定義を使う場合は、Step スキーマ内で `$ref` で参照し、
`intentSchemaRef` は解決後のローカルポインタを指定する。

## 詳細ドキュメント

- `agents/docs/builder/01_quickstart.md` - クイックスタート
- `agents/docs/builder/02_agent_definition.md` - agent.json 詳細
- `agents/docs/builder/03_builder_guide.md` - ビルダーガイド
- `agents/docs/builder/04_config_system.md` - 設定システム
