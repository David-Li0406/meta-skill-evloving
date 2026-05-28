---
name: mixseek-config-management
description: Use this skill when you need to generate or validate MixSeek configuration files, including team, evaluator, and judgment settings.
---

# MixSeek Configuration Management

## 概要

MixSeek-Coreの設定ファイル（team.toml、evaluator.toml、judgment.toml）を生成または検証します。これにより、チーム構成、評価基準、スコアリング方法を定義し、設定ファイルの整合性を確認します。

## 前提条件

- ワークスペースが初期化されていること（`mixseek-workspace-init`参照）
- 環境変数 `MIXSEEK_WORKSPACE` が設定されていること（推奨）
- Pythonコマンドが利用可能であること（`detect-python-command` スキルで判別）

## 対応ファイルタイプ

| ファイルタイプ | 説明 | パス例 |
|---------------|------|--------|
| team | チーム設定 | `configs/agents/team-*.toml` |
| evaluator | 評価設定 | `configs/evaluators/evaluator.toml` |
| judgment | 判定設定 | `configs/judgment/judgment.toml` |

## 使用方法

### チーム設定生成

1. **要件のヒアリング**: ユーザーにチームの目的、必要なMember Agent、使用モデルを確認します。
2. **チーム構成の提案**: 一意のID、表示名、Leader Agent、Member Agentsを提案します。
3. **設定ファイルの生成**: 以下のテンプレートを基に設定ファイルを生成します。

```toml
[team]
team_id = "<team-id>"
team_name = "<チーム名>"
max_concurrent_members = 15

[team.leader]
system_instruction = """
あなたはチームのリーダーです。
"""
model = "google-gla:gemini-2.5-pro"
temperature = 0.7
timeout_seconds = 300

[[team.members]]
agent_name = "<member-name>"
agent_type = "<type>"
tool_name = "<tool_name>"
tool_description = "<description>"
model = "<model>"
system_instruction = """
あなたは<role>を担当するエージェントです。
"""
temperature = 0.2
```

4. **ファイルの保存**: 生成した設定を以下のパスに保存します。

```bash
$MIXSEEK_WORKSPACE/configs/agents/team-<team-id>.toml
```

5. **設定ファイルの検証**: 生成後は必ず検証を実行します。

```bash
uv run python .skills/mixseek-config-validate/scripts/validate-config.py \
    $MIXSEEK_WORKSPACE/configs/agents/team-<team-id>.toml --type team
```

### 評価設定生成

1. **要件のヒアリング**: ユーザーに評価の重点、重み付け、判定スタイルを確認します。
2. **メトリクス設定の提案**: 標準メトリクスから選択し、設定を提案します。
3. **設定ファイルの生成**: 以下のテンプレートを基に設定ファイルを生成します。

**evaluator.toml**:
```toml
default_model = "google-gla:gemini-2.5-pro"
temperature = 0.0

[[metrics]]
name = "<metric_name>"
weight = <weight>
```

**judgment.toml**:
```toml
model = "google-gla:gemini-2.5-pro"
temperature = 0.0
timeout_seconds = 60
```

4. **ファイルの保存**: 生成した設定を以下のパスに保存します。

```bash
$MIXSEEK_WORKSPACE/configs/evaluators/evaluator.toml
$MIXSEEK_WORKSPACE/configs/judgment/judgment.toml
```

5. **設定ファイルの検証**: 生成後は必ず検証を実行します。

```bash
uv run python .skills/mixseek-config-validate/scripts/validate-config.py \
    $MIXSEEK_WORKSPACE/configs/evaluators/evaluator.toml --type evaluator

uv run python .skills/mixseek-config-validate/scripts/validate-config.py \
    $MIXSEEK_WORKSPACE/configs/judgment/judgment.toml --type judgment
```

### 検証の実行

検証を実行する際は、以下のコマンドを使用します：

```bash
.skills/detect-python-command/scripts/run-python.sh \
    .skills/mixseek-config-validate/scripts/validate-config.py <file-path>
```

## トラブルシューティング

- **設定ファイルの検証**: `mixseek-config-validate`スキルで検証を行い、エラーがあれば修正します。
- **APIキーの確認**: 使用モデルに対応するAPIキーが設定されているか確認します。
- **ワークスペースパス**: `MIXSEEK_WORKSPACE`が正しく設定されているか確認します。

## 参照

- TOMLスキーマ詳細: `references/TOML-SCHEMA.md`
- Member Agentタイプ: `references/MEMBER-TYPES.md`
- 利用可能モデル: `.skills/mixseek-model-list/references/VALID-MODELS.md`