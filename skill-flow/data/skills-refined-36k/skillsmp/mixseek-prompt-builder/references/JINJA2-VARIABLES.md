# Jinja2 Variables Reference

## 概要

MixSeekのPromptBuilderで利用可能なJinja2変数の詳細リファレンスです。

## 変数一覧

### user_prompt

**型**: `string`
**利用可能**: team, evaluator, judgment
**説明**: ユーザーが指定した元のプロンプト

**生成タイミング**: ユーザー入力時

**例**:
```
AIの最新トレンドについて調査してください
```

**使用例**:
```jinja2
# ユーザタスク
{{ user_prompt }}
```

---

### round_number

**型**: `int`
**利用可能**: team, judgment
**説明**: 現在のラウンド番号（1始まり）

**生成タイミング**: 各ラウンド開始時

**値の範囲**: 1 以上の整数（orchestrator設定の`max_rounds`が上限）

**使用例**:
```jinja2
# ラウンド {{ round_number }}

{% if round_number == 1 %}
初回の指示
{% elif round_number == 2 %}
2回目の指示
{% else %}
3回目以降の指示
{% endif %}
```

---

### submission_history

**型**: `string`
**利用可能**: team, judgment
**説明**: 過去のSubmission履歴（整形済み文字列）

**生成タイミング**: ラウンド終了後、次ラウンド開始時

**整形方法**: 各チームの提出内容がマークダウン形式で整形される

**エッジケース**:
- ラウンド1では空文字列 `""`
- 複数チームの提出がある場合は順番に連結

**出力形式例**:
```markdown
## ラウンド1の提出

### team-alpha (スコア: 85.5)
AIの最新トレンドとして、以下の5つが挙げられます：
1. 生成AI（LLM）の進化
2. マルチモーダルAI
...

### team-beta (スコア: 78.2)
調査の結果、以下のトレンドを確認しました：
...
```

**使用例**:
```jinja2
{% if round_number > 1 %}
# 過去の提出履歴
{{ submission_history }}
{% endif %}
```

---

### ranking_table

**型**: `string`
**利用可能**: team, judgment
**説明**: リーダーボード情報（整形済み文字列）

**生成タイミング**: 各ラウンドの評価完了後

**整形方法**: マークダウンテーブル形式

**エッジケース**:
- ラウンド1の開始時は空または初期状態
- 同点の場合は提出順

**出力形式例**:
```markdown
| 順位 | チーム | スコア |
|------|--------|--------|
| 1 | team-alpha | 85.5 |
| 2 | team-beta | 78.2 |
| 3 | team-gamma | 72.0 |
```

**使用例**:
```jinja2
# 現在のリーダーボード
{{ ranking_table }}

上位チームを参考に、より良い回答を目指してください。
```

---

### team_position_message

**型**: `string`
**利用可能**: team, judgment
**説明**: チームの現在順位を示すメッセージ

**生成タイミング**: 各ラウンドの評価完了後

**エッジケース**:
- ラウンド1開始時は初期メッセージ
- 単一チームの場合も表示

**出力形式例**:
```
現在2位です。1位との差は7.3ポイントです。
```
```
現在1位をキープしています。
```

**使用例**:
```jinja2
## 順位情報
{{ team_position_message }}
```

---

### current_datetime

**型**: `string`
**利用可能**: team, evaluator, judgment
**説明**: 現在日時（ISO 8601形式、タイムゾーン付き）

**生成タイミング**: プロンプト展開時

**フォーマット**: `YYYY-MM-DDTHH:MM:SS+HH:MM`

**出力形式例**:
```
2026-01-22T15:30:45+09:00
```

**使用例**:
```jinja2
---
現在日時: {{ current_datetime }}
---

最新の情報（{{ current_datetime }} 時点）を調査してください。
```

---

### submission

**型**: `string`
**利用可能**: evaluator のみ
**説明**: 評価対象のエージェント提出内容

**生成タイミング**: エージェントの提出完了時

**説明**: Evaluatorが評価する対象となる、単一エージェントの提出内容

**使用例**:
```jinja2
# 評価対象の提出内容
{{ submission }}

## 評価基準
1. 正確性
2. 網羅性
3. 構造性
```

---

## 変数の利用可能範囲

| 変数名 | team | evaluator | judgment |
|--------|------|-----------|----------|
| `user_prompt` | o | o | o |
| `round_number` | o | - | o |
| `submission_history` | o | - | o |
| `ranking_table` | o | - | o |
| `team_position_message` | o | - | o |
| `current_datetime` | o | o | o |
| `submission` | - | o | - |

## ベストプラクティス

### 1. ラウンド1での履歴変数の扱い

ラウンド1では `submission_history` が空のため、条件分岐を使用:

```jinja2
{% if round_number > 1 %}
# 過去の提出履歴
{{ submission_history }}
{% else %}
{# ラウンド1では履歴なし #}
{% endif %}
```

### 2. 日時情報の活用

最新情報の取得を促す場合:

```jinja2
現在日時: {{ current_datetime }}

※ 可能な限り最新の情報（上記日時基準）を取得してください。
```

### 3. 競合形式での順位活用

順位情報を活用してモチベーション向上:

```jinja2
{{ team_position_message }}

{% if round_number > 1 %}
## 現在の順位
{{ ranking_table }}

上位チームの戦略を分析し、改善点を見つけてください。
{% endif %}
```

### 4. 段階的な指示の出し分け

ラウンドに応じた詳細な指示:

```jinja2
{% if round_number == 1 %}
## フェーズ1: 情報収集
- 幅広いキーワードで検索
- 主要な情報源を特定
{% elif round_number == 2 %}
## フェーズ2: 深掘り
- 前回の結果を分析
- 具体的なキーワードで再検索
{% elif round_number >= 3 %}
## フェーズ3: 統合
- 情報を検証・統合
- 最終回答を作成
{% endif %}
```

### 5. Evaluator用の評価観点

評価者に明確な基準を提示:

```jinja2
# 評価タスク

## 元のタスク
{{ user_prompt }}

## 提出内容
{{ submission }}

## 評価観点（各10点満点）
1. **正確性**: 情報は正確か
2. **網羅性**: 必要な情報が揃っているか
3. **構造性**: 論理的に整理されているか
4. **実用性**: 実際に役立つ内容か
```

## エラー回避

### 未定義変数の使用

利用可能でない変数を使用するとエラーになります:

```jinja2
{# evaluatorでsubmission_historyは使用不可 #}
{{ submission_history }}  {# エラー #}
```

### Jinja2構文エラー

よくある間違い:

```jinja2
{# 間違い: endifがない #}
{% if round_number == 1 %}
内容

{# 正しい #}
{% if round_number == 1 %}
内容
{% endif %}
```

```jinja2
{# 間違い: 変数展開で{% %}を使用 #}
{% user_prompt %}

{# 正しい #}
{{ user_prompt }}
```
