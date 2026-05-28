# SQL・BigQuery ガイド

## 目次
- 基本クエリ
- 集計関数
- ウィンドウ関数
- 結合
- BigQuery固有機能
- パフォーマンス最適化

## 基本クエリ

### SELECT

```sql
-- 基本
SELECT name, email FROM users;

-- 条件
SELECT * FROM orders WHERE status = 'completed';

-- ソート
SELECT * FROM products ORDER BY price DESC;

-- 制限
SELECT * FROM users LIMIT 100;

-- 重複排除
SELECT DISTINCT category FROM products;

-- エイリアス
SELECT 
    first_name AS "名",
    last_name AS "姓",
    first_name || ' ' || last_name AS full_name
FROM users;
```

### WHERE条件

```sql
-- 比較
WHERE price > 1000
WHERE status = 'active'
WHERE created_at >= '2025-01-01'

-- 複数条件
WHERE status = 'active' AND price > 1000
WHERE category = 'A' OR category = 'B'

-- IN
WHERE category IN ('A', 'B', 'C')

-- BETWEEN
WHERE price BETWEEN 1000 AND 5000
WHERE date BETWEEN '2025-01-01' AND '2025-01-31'

-- LIKE
WHERE name LIKE '田%'      -- 前方一致
WHERE email LIKE '%@gmail.com'  -- 後方一致
WHERE name LIKE '%田中%'   -- 部分一致

-- NULL
WHERE phone IS NULL
WHERE email IS NOT NULL
```

## 集計関数

```sql
SELECT
    COUNT(*) AS total_count,
    COUNT(DISTINCT user_id) AS unique_users,
    SUM(amount) AS total_amount,
    AVG(amount) AS avg_amount,
    MIN(amount) AS min_amount,
    MAX(amount) AS max_amount
FROM orders;
```

### GROUP BY

```sql
SELECT
    category,
    COUNT(*) AS count,
    SUM(amount) AS total
FROM orders
GROUP BY category;

-- 複数列でグループ化
SELECT
    EXTRACT(YEAR FROM created_at) AS year,
    EXTRACT(MONTH FROM created_at) AS month,
    SUM(amount) AS total
FROM orders
GROUP BY year, month
ORDER BY year, month;
```

### HAVING

```sql
SELECT
    category,
    COUNT(*) AS count,
    SUM(amount) AS total
FROM orders
GROUP BY category
HAVING COUNT(*) >= 10
ORDER BY total DESC;
```

## ウィンドウ関数

### ROW_NUMBER / RANK / DENSE_RANK

```sql
SELECT
    *,
    ROW_NUMBER() OVER (ORDER BY amount DESC) AS row_num,
    RANK() OVER (ORDER BY amount DESC) AS rank,
    DENSE_RANK() OVER (ORDER BY amount DESC) AS dense_rank
FROM orders;

-- パーティション別
SELECT
    category,
    name,
    amount,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY amount DESC) AS rank_in_category
FROM products;
```

### 累積・移動集計

```sql
SELECT
    date,
    amount,
    SUM(amount) OVER (ORDER BY date) AS cumulative_sum,
    AVG(amount) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg_7d
FROM daily_sales;
```

### LAG / LEAD

```sql
SELECT
    date,
    amount,
    LAG(amount, 1) OVER (ORDER BY date) AS prev_amount,
    LEAD(amount, 1) OVER (ORDER BY date) AS next_amount,
    amount - LAG(amount, 1) OVER (ORDER BY date) AS diff_from_prev
FROM daily_sales;
```

### FIRST_VALUE / LAST_VALUE

```sql
SELECT
    category,
    name,
    amount,
    FIRST_VALUE(name) OVER (PARTITION BY category ORDER BY amount DESC) AS top_product
FROM products;
```

## 結合

```sql
-- INNER JOIN
SELECT o.*, u.name
FROM orders o
INNER JOIN users u ON o.user_id = u.id;

-- LEFT JOIN
SELECT u.*, COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;

-- 複数テーブル結合
SELECT 
    o.id,
    u.name AS user_name,
    p.name AS product_name,
    oi.quantity
FROM orders o
JOIN users u ON o.user_id = u.id
JOIN order_items oi ON o.id = oi.order_id
JOIN products p ON oi.product_id = p.id;
```

## BigQuery固有機能

### 日付関数

```sql
-- 現在日時
SELECT CURRENT_TIMESTAMP(), CURRENT_DATE()

-- 日付抽出
SELECT
    EXTRACT(YEAR FROM created_at) AS year,
    EXTRACT(MONTH FROM created_at) AS month,
    EXTRACT(DAY FROM created_at) AS day,
    EXTRACT(DAYOFWEEK FROM created_at) AS dow

-- 日付計算
SELECT
    DATE_ADD(CURRENT_DATE(), INTERVAL 7 DAY),
    DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH),
    DATE_DIFF(end_date, start_date, DAY) AS days_diff

-- 日付フォーマット
SELECT FORMAT_DATE('%Y年%m月', date) AS formatted_date

-- 日付トランケート
SELECT DATE_TRUNC(created_at, MONTH) AS month_start
```

### 配列・構造体

```sql
-- 配列
SELECT ARRAY_AGG(name) AS names FROM users;

SELECT * FROM products, UNNEST(tags) AS tag WHERE tag = 'sale';

-- 構造体
SELECT
    user.id,
    user.profile.name,
    user.profile.email
FROM users_with_profile;
```

### WITH句（CTE）

```sql
WITH monthly_sales AS (
    SELECT
        DATE_TRUNC(created_at, MONTH) AS month,
        SUM(amount) AS total
    FROM orders
    GROUP BY month
),
growth AS (
    SELECT
        month,
        total,
        LAG(total) OVER (ORDER BY month) AS prev_total,
        (total - LAG(total) OVER (ORDER BY month)) / LAG(total) OVER (ORDER BY month) * 100 AS growth_rate
    FROM monthly_sales
)
SELECT * FROM growth;
```

### PIVOT

```sql
SELECT * FROM (
    SELECT category, EXTRACT(MONTH FROM date) AS month, amount
    FROM sales
)
PIVOT (SUM(amount) FOR month IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12));
```

## パフォーマンス最適化

### パーティションフィルタ

```sql
-- ✅ パーティション列でフィルタ
SELECT * FROM `project.dataset.events`
WHERE DATE(event_timestamp) = '2025-01-15';

-- ❌ パーティション列を加工
SELECT * FROM `project.dataset.events`
WHERE EXTRACT(DATE FROM event_timestamp) = '2025-01-15';
```

### 必要な列のみ選択

```sql
-- ❌ SELECT *
SELECT * FROM large_table;

-- ✅ 必要な列のみ
SELECT id, name, created_at FROM large_table;
```

### APPROX関数

```sql
-- 近似カウント（高速）
SELECT APPROX_COUNT_DISTINCT(user_id) FROM events;

-- 近似パーセンタイル
SELECT APPROX_QUANTILES(amount, 100)[OFFSET(50)] AS median FROM orders;
```

### クラスタリング

```sql
-- クラスタ化テーブルの作成
CREATE TABLE `project.dataset.orders`
PARTITION BY DATE(created_at)
CLUSTER BY user_id, status
AS SELECT * FROM source_orders;
```
