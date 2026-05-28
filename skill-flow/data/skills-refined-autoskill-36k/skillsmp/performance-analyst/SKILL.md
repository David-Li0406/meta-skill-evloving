---
name: "performance-analyst"
description: "Activates when user requests performance optimization, N+1 query analysis, caching strategy design, database tuning, or scalability assessment. Do NOT use for security audits. Examples: 'Optimize this slow query', 'Check for N+1 problems'."
---

# Performance Analyst Skill

## 🧠 Expertise

資深效能工程師，專精於資料庫優化、快取策略、系統擴展性設計，擁有大規模系統調優經驗。

---

## 1. 資料庫效能分析

### 1.1 N+1 查詢問題

**定義**：在迴圈中執行個別查詢，導致 1 + N 次資料庫請求。

**識別模式**：
```php
// ❌ N+1 Problem
$users = User::all();
foreach ($users as $user) {
    echo $user->profile->name;  // 每次迭代執行一次查詢
}

// ✅ Eager Loading 解決方案
$users = User::with('profile')->get();
foreach ($users as $user) {
    echo $user->profile->name;  // 無額外查詢
}
```

**檢測工具**：
- Laravel Debugbar
- `DB::enableQueryLog()` + `DB::getQueryLog()`
- Clockwork

---

### 1.2 索引優化

**需要索引的欄位**：
| 情境 | 建議 |
|-----|-----|
| WHERE 條件 | 單欄位索引 |
| JOIN 條件 | 外鍵索引 |
| ORDER BY | 排序欄位索引 |
| 複合條件 | 複合索引（順序重要） |
| 唯一值查詢 | UNIQUE 索引 |

**紅旗標誌**：
- ❌ 大表無主鍵/索引的 WHERE 條件
- ❌ LIKE '%keyword%' 查詢
- ❌ 函數包裹索引欄位：`WHERE YEAR(created_at) = 2024`

**索引建議**：
```sql
-- 複合索引順序：選擇性高的欄位在前
CREATE INDEX idx_orders_status_date ON orders(status, created_at);

-- 覆蓋索引：包含所有需要的欄位
CREATE INDEX idx_users_email_name ON users(email, name);
```

---

### 1.3 查詢優化

**選取欄位最小化**：
```php
// ❌ 選取所有欄位
User::all();

// ✅ 只選需要的欄位
User::select('id', 'name', 'email')->get();
```

**分頁處理**：
```php
// ❌ 載入全部資料
$users = User::all();

// ✅ 分頁查詢
$users = User::paginate(20);

// ✅ Cursor 分頁（大資料集）
$users = User::cursor();
```

**批次處理**：
```php
// ❌ 記憶體爆炸
$users = User::all();
foreach ($users as $user) { /* 處理 */ }

// ✅ Chunk 分批處理
User::chunk(1000, function ($users) {
    foreach ($users as $user) { /* 處理 */ }
});

// ✅ Lazy Collection（更省記憶體）
User::lazy()->each(function ($user) { /* 處理 */ });
```

---

## 2. 時間/空間複雜度分析

### 2.1 時間複雜度

| 複雜度 | 名稱 | 範例 |
|-------|------|------|
| O(1) | 常數 | 陣列索引存取、雜湊表查詢 |
| O(log n) | 對數 | 二元搜尋 |
| O(n) | 線性 | 單次迴圈 |
| O(n log n) | 線性對數 | 快速排序、合併排序 |
| O(n²) | 平方 | 雙重巢狀迴圈 |
| O(2ⁿ) | 指數 | 遞迴費氏數列 |

**紅旗標誌**：
- ❌ 隱藏的 O(n²) 巢狀迴圈
- ❌ 遞迴無 memoization
- ❌ 迴圈內執行 IO 操作

---

### 2.2 空間複雜度

**記憶體風險**：
```php
// ❌ 高記憶體使用
$allData = DB::table('big_table')->get();  // 全部載入記憶體

// ✅ 串流處理
DB::table('big_table')->cursor()->each(function ($row) {
    // 逐筆處理
});
```

**記憶體洩漏風險**：
- 迴圈內累積陣列
- 未釋放的資源（檔案Handle、Connection）
- 靜態變數累積

---

## 3. 快取策略

### 3.1 快取層級

| 層級 | 用途 | TTL 建議 |
|-----|-----|---------|
| **應用層快取** | 業務資料、查詢結果 | 5-60 分鐘 |
| **HTTP 快取** | 靜態資源、API 回應 | 1-24 小時 |
| **資料庫查詢快取** | 複雜查詢結果 | 1-5 分鐘 |
| **Session 快取** | 使用者狀態 | Session 生命週期 |

---

### 3.2 快取 Key 設計

**命名規範**：
```
{prefix}:{entity}:{identifier}:{version}
```

**範例**：
```php
// ✅ Good
"user_profile:123:v1"
"game_list:platform_1:active:v2"

// ❌ Bad
"user-profile-123"      // 不一致的分隔符
"userProfile:123"       // 命名風格不一致
"data:123"              // 缺乏語意
```

---

### 3.3 快取失效策略

| 策略 | 適用場景 | 優缺點 |
|-----|---------|-------|
| **TTL 過期** | 可容忍短暫過期的資料 | 簡單，但有過期窗口 |
| **主動失效** | 資料變更時清除 | 精確，但需追蹤變更 |
| **Cache Aside** | 讀多寫少 | 靈活，需處理併發 |
| **Write Through** | 寫入頻繁 | 一致性高，寫入較慢 |

**Laravel 快取範例**：
```php
// Cache Aside 模式
$user = Cache::remember("user:{$id}", 3600, function () use ($id) {
    return User::find($id);
});

// 主動失效
public function updateUser($id, $data): User
{
    $user = User::findOrFail($id);
    $user->update($data);
    Cache::forget("user:{$id}");
    return $user;
}
```

---

## 4. 擴展性評估

### 4.1 水平擴展檢查

| 項目 | 檢查要點 |
|-----|---------|
| **Session 管理** | 是否使用分散式 Session（Redis/Database） |
| **檔案儲存** | 是否使用共享儲存（S3/NFS） |
| **快取** | 是否使用分散式快取（Redis Cluster） |
| **任務佇列** | 是否使用外部佇列服務（Redis/SQS） |

**紅旗標誌**：
- ❌ 本地檔案 Session
- ❌ 本地檔案儲存
- ❌ 記憶體內快取（單機）
- ❌ 同步處理耗時任務

---

### 4.2 負載壓力點識別

| 元件 | 10x 負載 | 100x 負載 |
|-----|---------|----------|
| **資料庫** | 連接池、讀寫分離 | 分片、分表 |
| **快取** | Redis Cluster | 多層快取 |
| **應用伺服器** | 負載均衡 | 自動擴展 |
| **背景任務** | 多 Worker | 任務分區 |

---

### 4.3 瓶頸識別

**常見瓶頸**：
1. **資料庫連接數** - 使用連接池
2. **慢查詢** - 優化索引、快取
3. **同步 IO** - 改為非同步/佇列
4. **單點故障** - 高可用架構

**監控指標**：
| 指標 | 健康閾值 | 危險閾值 |
|-----|---------|---------|
| 響應時間 | < 200ms | > 1s |
| 資料庫查詢 | < 50ms | > 500ms |
| CPU 使用率 | < 70% | > 90% |
| 記憶體使用率 | < 80% | > 95% |

---

## 5. 效能審查評分標準

| 嚴重度 | 定義 | 範例 |
|-------|------|------|
| **嚴重** | 直接導致系統崩潰或極度緩慢 | N+1 大量查詢、記憶體洩漏 |
| **高** | 顯著影響效能（>3x 變慢） | 缺少關鍵索引、無分頁 |
| **中** | 可優化但非緊急 | 快取未啟用、過度查詢欄位 |
| **低** | 最佳實務偏離 | Key 命名不規範、TTL 未設定 |
