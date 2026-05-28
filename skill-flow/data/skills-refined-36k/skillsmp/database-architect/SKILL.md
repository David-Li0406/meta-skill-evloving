---
name: "database-architect"
description: "Activates when user requests database design, schema planning, index optimization, sharding strategies, read-write separation, or multi-tenant data isolation. Do NOT use for NoSQL/Redis design (use redis-architect). Examples: 'Design user schema', 'Optimize MySQL indexes'."
---

# Database Architect Skill

## 🧠 Expertise

資深資料庫架構師，專精於 MySQL/PostgreSQL 大規模資料庫設計、效能調優與高可用架構。

---

## 1. 資料庫設計原則

### 1.1 垂直分割策略

**定義**：將一張大表依欄位使用頻率拆分為多張表。

**適用場景**：
- 高頻查詢欄位與低頻查詢欄位混合
- 頻繁更新欄位與靜態資料混合
- 大型欄位（TEXT、BLOB）與小型欄位混合

**設計模式**：
```sql
-- ❌ 錯誤：單表設計
CREATE TABLE users (
    id, email, status,           -- 高頻查詢
    nickname, phone, address,    -- 低頻查詢
    avatar_blob, bio_text,       -- 大型欄位
    login_count, last_login      -- 頻繁更新
);

-- ✅ 正確：垂直分割
CREATE TABLE users (id, email, status);           -- 核心表
CREATE TABLE user_profiles (user_id, nickname, phone, address);  -- 低頻
CREATE TABLE user_media (user_id, avatar_blob, bio_text);        -- 大型欄位
CREATE TABLE user_security (user_id, login_count, last_login);   -- 高頻更新
```

---

### 1.2 水平分區策略

**適用場景**：
- 資料量超過百萬筆
- 有明確的分區鍵（時間、租戶 ID）

**分區類型**：

| 類型 | 使用情境 | 範例 |
|-----|---------|------|
| **RANGE** | 按時間分區 | 日誌、交易記錄 |
| **HASH** | 均勻分散 | 用戶資料 |
| **LIST** | 離散值分組 | 地區、類別 |

**MySQL 分區範例**：
```sql
CREATE TABLE transactions (
    id BIGINT UNSIGNED AUTO_INCREMENT,
    tenant_id VARCHAR(50) NOT NULL,
    amount DECIMAL(20,8) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (UNIX_TIMESTAMP(created_at)) (
    PARTITION p202501 VALUES LESS THAN (UNIX_TIMESTAMP('2025-02-01')),
    PARTITION p202502 VALUES LESS THAN (UNIX_TIMESTAMP('2025-03-01')),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

---

## 2. 索引優化策略

### 2.1 索引設計原則

| 原則 | 說明 |
|-----|------|
| **選擇性高優先** | 區分度高的欄位放複合索引前面 |
| **覆蓋索引** | 讓索引包含所有查詢欄位 |
| **最左前綴** | 複合索引遵循最左匹配原則 |
| **避免函數** | 不要在索引欄位上使用函數 |

### 2.2 索引類型選擇

```sql
-- 單欄位索引：單一條件查詢
CREATE INDEX idx_users_status ON users(status);

-- 複合索引：多條件查詢（順序重要）
CREATE INDEX idx_orders_status_date ON orders(status, created_at);

-- 覆蓋索引：避免回表查詢
CREATE INDEX idx_users_email_name ON users(email, name);

-- 唯一索引：確保唯一性
CREATE UNIQUE INDEX uk_users_email ON users(email);
```

### 2.3 索引紅旗標誌

- ❌ `WHERE YEAR(created_at) = 2024` — 函數包裹索引欄位
- ❌ `LIKE '%keyword%'` — 前綴通配符無法使用索引
- ❌ `OR` 條件的多欄位 — 可能無法有效使用索引
- ❌ 過多索引 — 影響寫入效能

---

## 3. 多租戶資料隔離

### 3.1 隔離策略比較

| 策略 | 隔離程度 | 複雜度 | 適用規模 |
|-----|---------|-------|---------|
| **共享資料庫 + 租戶欄位** | 低 | 低 | 小規模 |
| **共享資料庫 + 獨立 Schema** | 中 | 中 | 中規模 |
| **獨立資料庫** | 高 | 高 | 大規模/合規要求 |

### 3.2 租戶欄位設計

```sql
-- 每張表必須有 tenant_id
CREATE TABLE orders (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    tenant_id VARCHAR(50) NOT NULL,
    -- 其他欄位...
    
    INDEX idx_tenant_id (tenant_id),
    UNIQUE KEY uk_tenant_order_no (tenant_id, order_no)
);

-- 應用層強制過濾
-- ✅ Laravel Global Scope
class TenantScope implements Scope {
    public function apply(Builder $builder, Model $model) {
        $builder->where('tenant_id', tenant()->id);
    }
}
```

---

## 4. 讀寫分離架構

### 4.1 架構設計

```
┌─────────────────────────────────────────┐
│              Application                 │
├─────────────────────────────────────────┤
│         Connection Router                │
│   ┌─────────────┬─────────────┐         │
│   │   Master    │   Slave(s)  │         │
│   │   (Write)   │   (Read)    │         │
│   └─────────────┴─────────────┘         │
└─────────────────────────────────────────┘
```

### 4.2 Laravel 配置

```php
// config/database.php
'mysql' => [
    'read' => [
        'host' => [
            env('DB_READ_HOST_1'),
            env('DB_READ_HOST_2'),
        ],
    ],
    'write' => [
        'host' => env('DB_WRITE_HOST'),
    ],
    'sticky' => true,  // 寫入後讀取主庫避免延遲
],
```

### 4.3 複製延遲處理

- 重要查詢使用 `DB::connection('mysql::write')`
- 設定 `sticky` 選項處理讀己所寫
- 監控複製延遲，超過閾值切換主庫

---

## 5. 備份恢復策略

### 5.1 備份類型

| 類型 | 頻率 | 用途 |
|-----|-----|------|
| **全量備份** | 每日 | 完整恢復 |
| **增量備份** | 每小時 | 快速恢復 |
| **Binlog** | 即時 | 點時恢復 |

### 5.2 RTO/RPO 目標

| 指標 | 定義 | 建議值 |
|-----|------|-------|
| **RTO** | 恢復時間目標 | < 15 分鐘 |
| **RPO** | 資料丟失容忍 | < 5 分鐘 |

---

## 6. 效能監控指標

### 6.1 關鍵指標

| 指標 | 健康值 | 警告值 |
|-----|-------|-------|
| 查詢響應時間 | < 100ms | > 500ms |
| 連接數使用率 | < 70% | > 90% |
| Buffer Pool 命中率 | > 99% | < 95% |
| 慢查詢數量 | < 10/hr | > 50/hr |

### 6.2 監控查詢

```sql
-- 慢查詢統計
SELECT * FROM mysql.slow_log 
WHERE start_time >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
ORDER BY query_time DESC LIMIT 20;

-- 連接數監控
SHOW STATUS WHERE Variable_name IN (
    'Threads_connected', 'Threads_running', 'Max_used_connections'
);

-- InnoDB Buffer Pool
SHOW STATUS WHERE Variable_name LIKE 'Innodb_buffer_pool%';
```

---

## 7. 設計檢查清單

### 設計階段
- [ ] 是否進行了垂直分割？
- [ ] 高頻更新資料是否獨立？
- [ ] 索引設計是否基於查詢模式？
- [ ] 多租戶隔離策略是否明確？

### 實施階段
- [ ] EXPLAIN 每個關鍵查詢
- [ ] 測試百萬級資料量
- [ ] 驗證並發更新場景
- [ ] 確認備份恢復流程
