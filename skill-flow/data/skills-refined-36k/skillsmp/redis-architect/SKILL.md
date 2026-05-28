---
name: "redis-architect"
description: "Activates when user requests Redis architecture design, caching patterns, distributed locks, pub/sub messaging, high availability setup, or queue system design. Do NOT use for SQL database design. Examples: 'Design Redis cache strategy', 'Implement distributed lock'."
---

# Redis Architect Skill

## 🧠 Expertise

資深 Redis 架構師，專精於分散式快取、高可用架構、訊息佇列與 NoSQL 資料結構設計。

---

## 1. Redis 資料結構與使用場景

### 1.1 資料結構選擇指南

| 資料結構 | 使用場景 | 時間複雜度 |
|---------|---------|-----------|
| **String** | 簡單快取、計數器、分散式鎖 | O(1) |
| **Hash** | 物件存儲、使用者 Session | O(1) |
| **List** | 訊息佇列、最新動態 | O(1) 頭尾操作 |
| **Set** | 標籤、唯一值集合、交集運算 | O(1) |
| **Sorted Set** | 排行榜、延遲佇列、時間線 | O(log n) |
| **Stream** | 事件流、訊息佇列（持久化） | O(1) |

### 1.2 使用範例

```php
// String - 簡單快取
Redis::set('user:123:profile', json_encode($profile));
Redis::setex('user:123:profile', 3600, json_encode($profile)); // 1小時過期

// Hash - 物件存儲（節省記憶體）
Redis::hset('user:123', 'name', 'John');
Redis::hset('user:123', 'email', 'john@example.com');
Redis::hgetall('user:123'); // 取得整個物件

// List - 訊息佇列
Redis::lpush('queue:emails', json_encode($email));
Redis::rpop('queue:emails'); // FIFO

// Set - 唯一值
Redis::sadd('user:123:tags', 'vip', 'premium');
Redis::sismember('user:123:tags', 'vip'); // 檢查成員

// Sorted Set - 排行榜
Redis::zadd('leaderboard', 1000, 'player:1');
Redis::zadd('leaderboard', 2500, 'player:2');
Redis::zrevrange('leaderboard', 0, 9); // Top 10
```

---

## 2. 快取模式

### 2.1 Cache Aside（旁路快取）

```php
// 讀取
public function getUser(int $id): User
{
    $key = "user:{$id}";
    
    $cached = Redis::get($key);
    if ($cached) {
        return User::fromArray(json_decode($cached, true));
    }
    
    $user = User::findOrFail($id);
    Redis::setex($key, 3600, json_encode($user));
    
    return $user;
}

// 更新時失效
public function updateUser(int $id, array $data): User
{
    $user = User::findOrFail($id);
    $user->update($data);
    Redis::del("user:{$id}");
    return $user;
}
```

### 2.2 Write Through（寫入穿透）

```php
public function updateUser(int $id, array $data): User
{
    $user = User::findOrFail($id);
    $user->update($data);
    
    // 同步更新快取
    Redis::setex("user:{$id}", 3600, json_encode($user));
    
    return $user;
}
```

### 2.3 快取穿透防護

```php
// 防止查詢不存在的資料
public function getUser(int $id): ?User
{
    $key = "user:{$id}";
    $cached = Redis::get($key);
    
    if ($cached === 'NULL') {
        return null; // 快取的空值
    }
    
    if ($cached) {
        return User::fromArray(json_decode($cached, true));
    }
    
    $user = User::find($id);
    
    if ($user) {
        Redis::setex($key, 3600, json_encode($user));
    } else {
        Redis::setex($key, 300, 'NULL'); // 快取空值 5 分鐘
    }
    
    return $user;
}
```

---

## 3. 分散式鎖

### 3.1 基本實作

```php
class RedisLock
{
    public function acquire(string $key, int $ttl = 10): ?string
    {
        $token = Str::uuid()->toString();
        
        $acquired = Redis::set(
            "lock:{$key}",
            $token,
            'EX', $ttl,
            'NX'  // 只在不存在時設置
        );
        
        return $acquired ? $token : null;
    }
    
    public function release(string $key, string $token): bool
    {
        // Lua 腳本確保原子性
        $script = <<<'LUA'
            if redis.call("get", KEYS[1]) == ARGV[1] then
                return redis.call("del", KEYS[1])
            else
                return 0
            end
        LUA;
        
        return Redis::eval($script, 1, "lock:{$key}", $token) === 1;
    }
}

// 使用
$lock = new RedisLock();
$token = $lock->acquire('order:123');

if ($token) {
    try {
        // 執行關鍵操作
        processOrder(123);
    } finally {
        $lock->release('order:123', $token);
    }
}
```

### 3.2 Laravel 內建鎖

```php
// 使用 Laravel Cache Lock
$lock = Cache::lock('order:123', 10);

if ($lock->get()) {
    try {
        processOrder(123);
    } finally {
        $lock->release();
    }
}

// 或使用阻塞方式
$lock = Cache::lock('order:123', 10);
$lock->block(5, function () {
    processOrder(123);
});
```

---

## 4. Pub/Sub 訊息模式

### 4.1 基本使用

```php
// 發布訊息
Redis::publish('channel:notifications', json_encode([
    'type' => 'order_created',
    'order_id' => 123,
]));

// 訂閱訊息（需要獨立進程）
Redis::subscribe(['channel:notifications'], function ($message, $channel) {
    $data = json_decode($message, true);
    handleNotification($data);
});
```

### 4.2 適用場景

| 場景 | 說明 |
|-----|------|
| 即時通知 | 廣播給所有訂閱者 |
| 快取失效 | 通知所有實例清除快取 |
| 事件廣播 | Laravel Echo 後端 |

### 4.3 限制

- **不保證送達**：訂閱者離線時訊息會丟失
- **無持久化**：需要持久化請使用 Stream

---

## 5. 高可用架構

### 5.1 Redis Sentinel

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Sentinel 1 │     │  Sentinel 2 │     │  Sentinel 3 │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │ 監控
       ┌───────────────────┼───────────────────┐
       │                   │                   │
┌──────▼──────┐     ┌──────▼──────┐     ┌──────▼──────┐
│   Master    │────▶│   Slave 1   │     │   Slave 2   │
└─────────────┘     └─────────────┘     └─────────────┘
```

**Laravel 配置**：
```php
// config/database.php
'redis' => [
    'client' => 'predis',
    'default' => [
        'tcp://sentinel1:26379',
        'tcp://sentinel2:26379',
        'tcp://sentinel3:26379',
        'options' => [
            'replication' => 'sentinel',
            'service' => 'mymaster',
        ],
    ],
],
```

### 5.2 Redis Cluster

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Master 1   │     │  Master 2   │     │  Master 3   │
│ Slot 0-5460 │     │ Slot 5461-  │     │ Slot 10923- │
│             │     │     10922   │     │     16383   │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
┌──────▼──────┐     ┌──────▼──────┐     ┌──────▼──────┐
│   Slave 1   │     │   Slave 2   │     │   Slave 3   │
└─────────────┘     └─────────────┘     └─────────────┘
```

**Laravel 配置**：
```php
'redis' => [
    'client' => 'predis',
    'clusters' => [
        'default' => [
            ['host' => 'node1', 'port' => 6379],
            ['host' => 'node2', 'port' => 6379],
            ['host' => 'node3', 'port' => 6379],
        ],
        'options' => [
            'cluster' => 'redis',
        ],
    ],
],
```

---

## 6. 持久化策略

### 6.1 RDB vs AOF

| 特性 | RDB | AOF |
|-----|-----|-----|
| **方式** | 快照 | 日誌追加 |
| **資料安全** | 可能丟失數分鐘 | 最多丟失 1 秒 |
| **效能** | 較高 | 較低 |
| **恢復速度** | 快 | 慢 |
| **適用場景** | 備份、災難恢復 | 資料安全要求高 |

### 6.2 建議配置

```bash
# 同時啟用 RDB 和 AOF
save 900 1      # 900秒內至少1次寫入則快照
save 300 10     # 300秒內至少10次寫入則快照
save 60 10000   # 60秒內至少10000次寫入則快照

appendonly yes
appendfsync everysec  # 每秒同步
```

---

## 7. Laravel 整合

### 7.1 佇列系統（Horizon）

```php
// config/horizon.php
'environments' => [
    'production' => [
        'supervisor-1' => [
            'connection' => 'redis',
            'queue' => ['high', 'default', 'low'],
            'balance' => 'auto',
            'minProcesses' => 1,
            'maxProcesses' => 10,
            'tries' => 3,
        ],
    ],
],
```

### 7.2 Session 存儲

```php
// config/session.php
'driver' => 'redis',
'connection' => 'session',  // 獨立連接

// config/database.php
'redis' => [
    'session' => [
        'host' => env('REDIS_HOST'),
        'port' => env('REDIS_PORT'),
        'database' => 1,  // 使用不同的 database
    ],
],
```

### 7.3 Rate Limiting

```php
// 使用 Redis 實作速率限制
RateLimiter::for('api', function (Request $request) {
    return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
});
```

---

## 8. 效能調優

### 8.1 記憶體優化

| 策略 | 說明 |
|-----|------|
| **Hash 小物件** | 使用 Hash 存儲小物件，比多個 String 更省記憶體 |
| **合理 TTL** | 設置過期時間，避免記憶體無限增長 |
| **LRU 淘汰** | 配置 `maxmemory-policy allkeys-lru` |

### 8.2 監控指標

| 指標 | 健康值 | 警告值 |
|-----|-------|-------|
| 記憶體使用率 | < 70% | > 90% |
| 命中率 | > 95% | < 80% |
| 連接數 | < 80% maxclients | > 90% |
| 延遲 | < 1ms | > 10ms |

### 8.3 監控命令

```bash
# 即時監控
redis-cli monitor

# 統計資訊
redis-cli info stats

# 記憶體分析
redis-cli memory doctor

# 慢查詢日誌
redis-cli slowlog get 10
```

---

## 9. Redis 檢查清單

### 架構設計
- [ ] 是否選擇正確的資料結構？
- [ ] 是否設置合理的 TTL？
- [ ] 高可用方案是否到位？
- [ ] 持久化策略是否配置？

### 效能
- [ ] 是否避免大 Key？
- [ ] 是否使用 Pipeline 批次操作？
- [ ] 是否監控記憶體使用？
- [ ] 是否有慢查詢監控？

### 安全
- [ ] 是否設置密碼？
- [ ] 是否限制網路存取？
- [ ] 是否禁用危險命令？
