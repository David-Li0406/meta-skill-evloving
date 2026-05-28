---
name: databricks-system-tables
description: |
  Databricks System Tables の分析・クエリ作成支援。Unity Catalog の system カタログに格納された運用データ（課金、監査ログ、ジョブ実行、クエリ履歴、リネージュ、コンピュートなど）を活用した分析・調査を行う際に使用。
  トリガー例: コスト分析、DBU使用量、課金レポート、監査ログ調査、ジョブ実行履歴、クエリパフォーマンス、テーブルリネージュ、クラスター利用状況の確認。
metadata:
  version: 1.0.0
---

## Overview

System Tables は Databricks がホストする運用データの分析ストアで、`system` カタログ配下に格納される。Delta Sharing で提供され、Unity Catalog ワークスペースからのみアクセス可能。

## スキーマ一覧と用途

### system.billing（課金）

| テーブル      | 用途                  | 主要カラム                                                     |
| ------------- | --------------------- | -------------------------------------------------------------- |
| `usage`       | DBU使用量・コスト分析 | `usage_date`, `sku_name`, `usage_quantity`, `usage_metadata.*` |
| `list_prices` | SKU単価履歴           | `sku_name`, `pricing.default`, `price_start_time`              |

**usage_metadata の主要フィールド:**

- `workspace_id`, `cluster_id`, `warehouse_id`, `job_id`, `job_run_id`, `notebook_id`

**コスト計算の注意:**

- `record_type` が `RETRACTION`/`RESTATEMENT` の場合は補正レコード
- 正確な合計: `SUM(usage_quantity) ... HAVING usage_quantity != 0`

### system.access（アクセス・監査）

| テーブル         | 用途                         | 主要カラム                                                           |
| ---------------- | ---------------------------- | -------------------------------------------------------------------- |
| `audit`          | 監査ログ（ユーザー操作追跡） | `event_time`, `action_name`, `user_identity.email`, `request_params` |
| `table_lineage`  | テーブル読み書きイベント     | `source_table_full_name`, `target_table_full_name`, `entity_type`    |
| `column_lineage` | カラムレベルリネージュ       | `source_column_name`, `target_column_name`                           |

**audit の主要 action_name:**

- `createTable`, `getTable`, `deleteTable`, `commandSubmit`, `runCommand`（verbose有効時）

### system.lakeflow（ジョブ・パイプライン）

| テーブル                | 用途                 | 主要カラム                                                                 |
| ----------------------- | -------------------- | -------------------------------------------------------------------------- |
| `jobs`                  | ジョブ定義           | `job_id`, `name`, `creator_user_name`, `settings`                          |
| `job_run_timeline`      | ジョブ実行履歴       | `job_id`, `run_id`, `period_start_time`, `period_end_time`, `result_state` |
| `job_task_run_timeline` | タスク実行詳細       | `job_id`, `task_key`, `compute_ids`, `termination_code`                    |
| `pipelines`             | DLTパイプライン定義  | `pipeline_id`, `name`, `creator_user_name`                                 |
| `pipeline_event_log`    | パイプライン更新履歴 | `pipeline_id`, `update_id`, `event_type`                                   |

**period_start/end_time について:**

- 1時間を超えるランは複数行に分割される（時間粒度の監視用）

### system.query（クエリ履歴）

| テーブル  | 用途                            | 主要カラム                                                                           |
| --------- | ------------------------------- | ------------------------------------------------------------------------------------ |
| `history` | SQL Warehouse/Serverless クエリ | `statement_id`, `executed_by`, `statement_text`, `total_duration_ms`, `query_source` |

**query_source 構造:**

```json
{
  "job_info": {"job_id": ..., "job_run_id": ...},
  "notebook_id": ...,
  "dashboard_id": ...,
  "alert_id": ...
}
```

### system.compute（コンピュート）

| テーブル           | 用途                       | 主要カラム                                                    |
| ------------------ | -------------------------- | ------------------------------------------------------------- |
| `clusters`         | クラスター設定履歴（SCD）  | `cluster_id`, `cluster_name`, `cluster_source`, `change_time` |
| `node_types`       | 利用可能ノードタイプ       | `node_type_id`, `num_cores`, `memory_mb`, `gpu_count`         |
| `node_timeline`    | ノード利用メトリクス       | `cluster_id`, `node_id`, `start_time`, `utilization`          |
| `warehouses`       | SQL Warehouse設定履歴      | `warehouse_id`, `name`, `cluster_size`, `change_time`         |
| `warehouse_events` | Warehouse起動/停止イベント | `warehouse_id`, `event_type`, `event_time`                    |

## よく使うクエリパターン

### 日別/月別コスト集計

```sql
SELECT
  DATE_TRUNC('month', usage_date) AS month,
  sku_name,
  SUM(usage_quantity) AS total_dbu,
  SUM(usage_quantity * p.pricing.default) AS estimated_cost
FROM system.billing.usage u
LEFT JOIN system.billing.list_prices p USING (sku_name)
WHERE usage_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY ALL
ORDER BY estimated_cost DESC
```

### ジョブ別コスト（Job Compute）

```sql
SELECT
  usage_metadata.job_id,
  j.name AS job_name,
  SUM(usage_quantity) AS total_dbu
FROM system.billing.usage u
LEFT JOIN system.lakeflow.jobs j
  ON u.usage_metadata.job_id = j.job_id
WHERE usage_metadata.job_id IS NOT NULL
  AND usage_date >= CURRENT_DATE - INTERVAL 7 DAYS
GROUP BY ALL
ORDER BY total_dbu DESC
```

### 失敗ジョブの調査

```sql
SELECT
  j.name,
  r.run_id,
  r.result_state,
  r.period_start_time,
  r.termination_code
FROM system.lakeflow.job_run_timeline r
JOIN system.lakeflow.jobs j USING (job_id)
WHERE r.result_state IN ('FAILED', 'TIMED_OUT', 'CANCELED')
  AND r.period_start_time >= CURRENT_DATE - INTERVAL 1 DAY
ORDER BY r.period_start_time DESC
```

### 長時間クエリの特定

```sql
SELECT
  executed_by,
  statement_text,
  total_duration_ms / 1000 / 60 AS duration_minutes,
  rows_produced
FROM system.query.history
WHERE total_duration_ms > 300000  -- 5分以上
  AND statement_type = 'SELECT'
ORDER BY total_duration_ms DESC
LIMIT 20
```

### テーブル利用頻度（人気テーブル）

```sql
SELECT
  source_table_full_name,
  COUNT(DISTINCT event_id) AS read_count
FROM system.access.table_lineage
WHERE event_date >= CURRENT_DATE - INTERVAL 7 DAYS
  AND source_table_full_name IS NOT NULL
GROUP BY source_table_full_name
ORDER BY read_count DESC
LIMIT 50
```

### ユーザー操作の監査

```sql
SELECT
  event_time,
  user_identity.email,
  action_name,
  request_params.full_name_arg AS table_name
FROM system.access.audit
WHERE action_name IN ('createTable', 'deleteTable', 'updatePermissions')
  AND event_date >= CURRENT_DATE - INTERVAL 7 DAYS
ORDER BY event_time DESC
```

## テーブル間 JOIN のキー

```
billing.usage.usage_metadata.job_id      ↔ lakeflow.jobs.job_id
billing.usage.usage_metadata.cluster_id  ↔ compute.clusters.cluster_id
billing.usage.usage_metadata.warehouse_id ↔ compute.warehouses.warehouse_id
lakeflow.job_run_timeline.job_id         ↔ lakeflow.jobs.job_id
query.history.statement_id               ↔ access.table_lineage.statement_id
access.table_lineage.entity_id           ↔ lakeflow.jobs.job_id (entity_type='JOB'時)
```

## 制限事項・注意点

1. **リアルタイム性なし**: データは1日を通して更新される。直近のイベントは遅延あり
2. **スキーマ変更**: 新カラムが随時追加される。`SELECT *` は避ける
3. **リージョン制約**: ほとんどのテーブルはリージョナル（同一リージョンのワークスペースのみ）
4. **Streaming時**: `skipChangeCommits=true` オプション必須
5. **Interactive Cluster コスト按分**: 複数ワークロード共有時は正確な按分不可

## 権限

System Tables へのアクセスには以下が必要:

- Account Admin かつ Metastore Admin による `USE` + `SELECT` 権限付与
- `GRANT USE CATALOG ON CATALOG system TO <principal>`
- `GRANT SELECT ON SCHEMA system.<schema> TO <principal>`

## スキーマ情報の動的取得

実際のカラム定義は Unity Catalog API または SQL で取得:

```sql
DESCRIBE EXTENDED system.billing.usage
```

```python
# REST API
GET /api/2.1/unity-catalog/tables/system.billing.usage
```
