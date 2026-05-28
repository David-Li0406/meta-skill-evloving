---
name: data-analysis
description: データ分析・可視化・レポート作成。pandas、SQL、BigQuery、スプレッドシート操作、統計分析、グラフ作成。「データ分析」「SQL」「BigQuery」「pandas」「集計」「可視化」「レポート」に関する質問で使用。
---

# データ分析・可視化

## クイックスタート

### pandas 基本操作

```python
import pandas as pd

# 読み込み
df = pd.read_csv("data.csv")

# 基本統計
print(df.describe())

# フィルタリング
filtered = df[df["status"] == "active"]

# グループ集計
summary = df.groupby("category")["amount"].sum()
```

### BigQuery クエリ

```sql
SELECT
    DATE(created_at) AS date,
    COUNT(*) AS count,
    SUM(amount) AS total
FROM `project.dataset.orders`
WHERE created_at >= '2025-01-01'
GROUP BY date
ORDER BY date
```

## 分析フロー

1. **データ収集**: DB、API、ファイルから取得
2. **データクリーニング**: 欠損値、異常値処理
3. **探索的分析**: 傾向、分布、相関の把握
4. **集計・加工**: 必要な指標を算出
5. **可視化**: グラフ、ダッシュボード作成
6. **レポート**: 結果のまとめ

## 詳細ガイド

- **pandas操作**: [reference/pandas.md](reference/pandas.md)
- **SQL・BigQuery**: [reference/sql.md](reference/sql.md)
- **可視化**: [reference/visualization.md](reference/visualization.md)
- **統計分析**: [reference/statistics.md](reference/statistics.md)

## ユーティリティスクリプト

```bash
# データプロファイリング
python scripts/profile_data.py data.csv

# SQLクエリ実行・CSV出力
python scripts/query_to_csv.py query.sql output.csv

# レポート生成
python scripts/generate_report.py --input data.csv --output report.html
```

## ワークフロー: データ分析

```
進捗チェックリスト:
- [ ] 1. 目的・KPIの明確化
- [ ] 2. データソース特定・収集
- [ ] 3. データクリーニング
- [ ] 4. 探索的データ分析（EDA）
- [ ] 5. 詳細分析・仮説検証
- [ ] 6. 可視化・レポート作成
- [ ] 7. 結論・提言のまとめ
```
