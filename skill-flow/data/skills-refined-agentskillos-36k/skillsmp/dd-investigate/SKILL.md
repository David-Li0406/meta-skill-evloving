---
name: dd-investigate
description: Datadogでサービス状態を調査。「Datadogで調べて」「サービスの状態確認」「エラー調査」等で起動。
user-invocable: true
allowed-tools:
  - mcp__datadog-mcp__analyze_datadog_logs
  - mcp__datadog-mcp__search_datadog_logs
  - mcp__datadog-mcp__search_datadog_spans
  - mcp__datadog-mcp__get_datadog_metric
  - mcp__datadog-mcp__search_datadog_services
  - mcp__datadog-mcp__search_datadog_monitors
  - mcp__datadog-mcp__search_datadog_incidents
  - mcp__datadog-mcp__get_datadog_trace
---

# dd-investigate

Datadog調査のSubagent用テンプレート集。

## 基本原則

1. 集計 → パターン → 詳細の順でアプローチ
2. 生データは最後の手段

## 使い方

Taskツールで委譲。メインには要約だけ返る：

```
Task:
  subagent_type: "general-purpose"
  prompt: "dd-investigateの「エラー調査」テンプレートで {service} を調査。結果を3行で要約。"
```

---

## テンプレート集

### 1. エラー調査

対象: サービスのエラー状況を把握したい

```
Task:
  subagent_type: "general-purpose"
  prompt: |
    {service} のエラー状況を調査。

    手順:
    1. analyze_datadog_logs で時系列カウント
       filter: "service:{service} status:error"
       sql_query: "SELECT DATE_TRUNC('minute', timestamp) as min, count(*) FROM logs GROUP BY DATE_TRUNC('minute', timestamp) ORDER BY min DESC"
       from: "now-1h", max_tokens: 3000

    2. search_datadog_logs でパターン確認
       query: "service:{service} status:error"
       use_log_patterns: true, max_tokens: 2000

    結果を要約:
    - エラー数の推移（増加傾向/安定/減少）
    - 主なエラーパターン
    - 推奨アクション（あれば）
```

### 2. レイテンシ調査

対象: サービスの応答速度を確認したい

```
Task:
  subagent_type: "general-purpose"
  prompt: |
    {service} のレイテンシを調査。

    手順:
    1. get_datadog_metric でp99レイテンシ
       queries: ["p99:trace.http.request.duration{service:{service}}"]
       from: "now-1h", raw_data: false, max_tokens: 3000

    2. 異常があれば search_datadog_spans で遅いリクエスト
       query: "service:{service} @duration:>1000000000"
       max_tokens: 3000

    結果を要約:
    - p99レイテンシの状況
    - 遅いリクエストのパターン（あれば）
```

### 3. インシデント確認

対象: 現在のインシデント状況を把握したい

```
Task:
  subagent_type: "general-purpose"
  prompt: |
    アクティブなインシデントを確認。

    手順:
    1. search_datadog_incidents
       query: "state:(active OR stable)"
       max_tokens: 3000

    結果を要約:
    - インシデント数
    - 重要度別の内訳
    - 各インシデントの概要（1行ずつ）
```

### 4. サービス全体ヘルスチェック

対象: 特定サービスの総合的な状態確認

```
Task:
  subagent_type: "general-purpose"
  prompt: |
    {service} の総合ヘルスチェック。

    手順:
    1. analyze_datadog_logs でstatus別カウント
       filter: "service:{service}"
       sql_query: "SELECT status, count(*) FROM logs GROUP BY status"
       from: "now-1h", max_tokens: 2000

    2. search_datadog_monitors で関連モニター状態
       query: "tag:service:{service}"
       max_tokens: 2000

    結果を要約:
    - ログのstatus分布
    - アラート状態のモニター（あれば）
    - 総合判定: 正常/警告/異常
```

### 5. 特定トレース調査

対象: trace_idから詳細を追いたい

```
Task:
  subagent_type: "general-purpose"
  prompt: |
    トレース {trace_id} を調査。

    手順:
    1. get_datadog_trace
       trace_id: "{trace_id}"
       only_service_entry_spans: true
       max_tokens: 5000

    結果を要約:
    - リクエストフロー
    - ボトルネック箇所
    - エラー発生箇所（あれば）
```

### 6. ログ検索（キーワード）

対象: 特定のキーワードでログを探したい

```
Task:
  subagent_type: "general-purpose"
  prompt: |
    "{keyword}" を含むログを調査。

    手順:
    1. analyze_datadog_logs でサービス別カウント
       filter: "{keyword}"
       sql_query: "SELECT service, count(*) FROM logs GROUP BY service ORDER BY count(*) DESC"
       from: "now-1h", max_tokens: 2000

    2. 上位サービスのログパターン
       search_datadog_logs
       query: "service:{top_service} {keyword}"
       use_log_patterns: true, max_tokens: 2000

    結果を要約:
    - どのサービスで発生しているか
    - 主なパターン
```

