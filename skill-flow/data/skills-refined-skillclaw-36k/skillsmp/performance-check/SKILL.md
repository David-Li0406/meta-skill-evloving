---
name: performance-check
description: 協助檢查 PHP/Laravel 應用程式的效能問題。當需要優化資料庫查詢、分析記憶體使用、或評估快取策略時載入此技能。
---

# 效能檢查技能

本技能提供 PHP/Laravel 應用程式的效能審查指引，聚焦於資料庫優化、記憶體管理與快取策略。

## 資料庫效能

### N+1 查詢問題

**嚴重程度**: 🟡 高

**檢測模式**:
```php
// ❌ N+1 問題 - 每次迴圈都查詢
$users = User::all();
foreach ($users as $user) {
    echo $user->posts->count(); // 每次迴圈產生一次查詢
}

// ✅ 預載入 - 只有 2 次查詢
$users = User::with('posts')->get();
foreach ($users as $user) {
    echo $user->posts->count();
}
```

**檢查要點**:
- 是否在迴圈中存取 Eloquent 關聯
- 是否使用 `with()` 預載入關聯
- 巢狀關聯是否使用 `with(['relation.nested'])`

---

### 未分頁的大量查詢

**嚴重程度**: 🟡 高

**檢測模式**:
```php
// ❌ 危險 - 載入全部資料
$users = User::all();

// ✅ 分頁
$users = User::paginate(20);

// ✅ 游標分頁（大資料集）
$users = User::cursor();
```

**檢查要點**:
- 是否對大型資料表使用 `all()` 或 `get()`
- API 是否提供分頁參數
- 匯出功能是否使用 chunk 或 cursor

---

### 缺少索引

**檢測要點**:
- `WHERE` 條件欄位是否有索引
- `ORDER BY` 欄位是否有索引
- 外鍵欄位是否有索引
- 複合查詢是否需要複合索引

```php
// 以下查詢需要索引
User::where('email', $email)->first();        // email 需要索引
Order::where('user_id', $id)->get();          // user_id 需要索引
Log::orderBy('created_at', 'desc')->limit(10); // created_at 需要索引
```

---

### 過度選取欄位

**檢測模式**:
```php
// ❌ 選取全部欄位
$users = User::all();

// ✅ 只選需要的欄位
$users = User::select(['id', 'name', 'email'])->get();
```

---

## 記憶體管理

### 大資料集處理

**檢測模式**:
```php
// ❌ 一次載入全部到記憶體
$records = Record::all();
foreach ($records as $record) {
    process($record);
}

// ✅ 使用 chunk 分批處理
Record::chunk(1000, function ($records) {
    foreach ($records as $record) {
        process($record);
    }
});

// ✅ 使用 LazyCollection
Record::cursor()->each(function ($record) {
    process($record);
});
```

---

### 資源釋放

**檢查要點**:
- 檔案句柄是否正確關閉
- 資料庫連線是否釋放
- 暫存資料是否清理

---

## 快取策略

### 快取 Key 規範

**正確格式**: `前綴_描述:變數`

```php
// ✅ 正確
Cache::remember("user_profile:{$userId}", 3600, fn() => ...);
Cache::remember("game_code:{$platformId}:{$gameId}", 3600, fn() => ...);

// ❌ 錯誤
Cache::remember("user-profile-{$userId}", ...);  // 使用連字符
Cache::remember("userProfile:{$userId}", ...);   // 駝峰命名
```

---

### 快取失效策略

**檢查要點**:
- 是否設定合理的 TTL
- 資料更新時是否清除快取
- 是否使用標籤管理相關快取

```php
// 更新時清除快取
public function update(User $user, array $data)
{
    $user->update($data);
    Cache::forget("user_profile:{$user->id}");
}

// 使用標籤
Cache::tags(['users', 'profiles'])->flush();
```

---

## 效能指標閾值

| 指標 | 警告值 | 危險值 |
|-----|-------|-------|
| 單一請求查詢數 | > 10 | > 50 |
| 單一查詢時間 | > 100ms | > 500ms |
| 單一請求記憶體 | > 64MB | > 128MB |
| API 回應時間 | > 200ms | > 1000ms |

---

## 輸出格式

對每個效能問題提供：

| 類型 | 影響 | 檔案:行號 | 問題描述 | 優化建議 |
|------|-----|----------|---------|---------|
| N+1 | 🟡 高 | path:123 | 描述 | 使用 with() |
