# Prompt Builder TOML Schema

## 概要

プロンプトビルダー設定ファイル（prompt_builder.toml）のスキーマ定義です。Team、Evaluator、Judgmentの各コンポーネントに配信するプロンプトテンプレートを定義します。

## ファイル配置

- パス: `$MIXSEEK_WORKSPACE/configs/prompt_builder.toml`
- 例: `workspaces/my-workspace/configs/prompt_builder.toml`

## 必須フィールド

### [prompt_builder] セクション

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `team_user_prompt` | string (multiline) | Team (Leader Agent) に渡すプロンプトテンプレート |
| `evaluator_user_prompt` | string (multiline) | Evaluator に渡すプロンプトテンプレート |
| `judgment_user_prompt` | string (multiline) | Judgment Client に渡すプロンプトテンプレート |

## テンプレート別の利用可能変数

### team_user_prompt / judgment_user_prompt

| 変数名 | 型 | 説明 |
|--------|-----|------|
| `user_prompt` | string | 元のユーザプロンプト |
| `round_number` | int | 現在のラウンド番号（1始まり） |
| `submission_history` | string | 過去のSubmission履歴（整形済み文字列） |
| `ranking_table` | string | リーダーボード情報（整形済み文字列） |
| `team_position_message` | string | チーム順位メッセージ |
| `current_datetime` | string | 現在日時（ISO 8601形式、タイムゾーン付き） |

### evaluator_user_prompt

| 変数名 | 型 | 説明 |
|--------|-----|------|
| `user_prompt` | string | 元のユーザプロンプト |
| `submission` | string | 評価対象のエージェント提出内容 |
| `current_datetime` | string | 現在日時（ISO 8601形式、タイムゾーン付き） |

## Jinja2構文ルール

### 変数展開

```jinja2
{{ user_prompt }}
{{ round_number }}
```

### 条件分岐

```jinja2
{% if round_number == 1 %}
ラウンド1の指示
{% elif round_number == 2 %}
ラウンド2の指示
{% else %}
それ以降の指示
{% endif %}
```

### コメント

```jinja2
{# これはコメントです。出力されません #}
```

### 空白制御

```jinja2
{%- if condition -%}  {# 前後の空白を除去 #}
内容
{%- endif -%}
```

## 設定例

### 最小構成

```toml
[prompt_builder]
team_user_prompt = """
# タスク
{{ user_prompt }}
"""

evaluator_user_prompt = """
# 評価対象
{{ submission }}
"""

judgment_user_prompt = """
# 判定対象
{{ submission_history }}
"""
```

### ラウンド別指示

```toml
[prompt_builder]
team_user_prompt = """
---
現在日時: {{ current_datetime }}
---

# ユーザタスク
{{ user_prompt }}

# ラウンド {{ round_number }}

{% if round_number == 1 %}
## 初期調査フェーズ
- 広範な情報収集を行ってください
- 主要な情報源を特定してください
{% elif round_number == 2 %}
## 深掘りフェーズ
- 前回の結果を分析してください
- 不足している情報を補完してください

### 前回の提出
{{ submission_history }}
{% else %}
## 最終統合フェーズ
- すべての情報を統合してください
- 最終的な回答を作成してください

### これまでの提出履歴
{{ submission_history }}
{% endif %}
"""

evaluator_user_prompt = """
---
現在日時: {{ current_datetime }}
---

# 評価タスク
以下の提出内容を、ユーザタスクに対する適切性で評価してください。

## ユーザタスク
{{ user_prompt }}

## 提出内容
{{ submission }}

## 評価観点
1. 正確性: 情報は正確か
2. 網羅性: 必要な情報が揃っているか
3. 構造性: 論理的に整理されているか
"""

judgment_user_prompt = """
---
現在日時: {{ current_datetime }}
---

# 継続判定タスク
調査を継続するか終了するかを判定してください。

## ユーザタスク
{{ user_prompt }}

## 提出履歴
{{ submission_history }}

## 現在の順位
{{ ranking_table }}

## 判定基準
- **継続**: 情報が不十分、重要な観点が欠落している場合
- **終了**: ユーザタスクに対して十分な回答が可能な場合
"""
```

### 競合形式（リーダーボード活用）

```toml
[prompt_builder]
team_user_prompt = """
# 競合タスク
{{ user_prompt }}

## ラウンド情報
- 現在のラウンド: {{ round_number }}
- {{ team_position_message }}

## リーダーボード
{{ ranking_table }}

{% if round_number > 1 %}
## 過去の提出
{{ submission_history }}

上位チームの戦略を参考に、より良い回答を目指してください。
{% endif %}
"""

evaluator_user_prompt = """
# 競合評価
以下の提出を他チームと比較して評価してください。

## タスク
{{ user_prompt }}

## 提出内容
{{ submission }}
"""

judgment_user_prompt = """
# 競合判定
十分な品質に達したか判定してください。

## リーダーボード
{{ ranking_table }}

## 履歴
{{ submission_history }}
"""
```

## バリデーションルール

1. **必須フィールド**: 3つのプロンプトフィールドすべてが必要
2. **Jinja2構文**: 有効なJinja2テンプレートであること
3. **変数名**: 定義された変数のみ使用可能
4. **マルチライン**: トリプルクォート `"""` を使用

```python
# バリデーション例
import tomllib
from jinja2 import Environment

with open("prompt_builder.toml", "rb") as f:
    config = tomllib.load(f)

pb = config.get("prompt_builder", {})
env = Environment()

required = ["team_user_prompt", "evaluator_user_prompt", "judgment_user_prompt"]
for field in required:
    assert field in pb, f"Missing required field: {field}"
    env.parse(pb[field])  # Jinja2構文チェック
```

## 関連ファイル

- orchestrator設定: `configs/orchestrator.toml`
- evaluator設定: `configs/evaluator.toml`
- team設定: `configs/agents/team-*.toml`
