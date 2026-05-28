---
name: database-design
description: 数据库设计和优化最佳实践。用于设计数据库架构、优化查询性能、数据建模、索引策略等。支持 SQL 和 NoSQL 数据库。
allowed-tools: Read, Grep, Glob, Edit
---

# 数据库设计与优化

## 数据建模

### 关系型数据库设计原则

#### 范式化
```sql
-- 第一范式（1NF）：原子性
❌ 不好
CREATE TABLE users (
  id INT,
  name VARCHAR(100),
  phones VARCHAR(255) -- '123,456,789'
);

✅ 好
CREATE TABLE users (
  id INT PRIMARY KEY,
  name VARCHAR(100)
);

CREATE TABLE user_phones (
  id INT PRIMARY KEY,
  user_id INT,
  phone VARCHAR(20),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- 第二范式（2NF）：消除部分依赖
-- 第三范式（3NF）：消除传递依赖
```

#### 反范式化（性能优化）
```sql
-- 适度反范式化以提高查询性能
CREATE TABLE orders (
  id INT PRIMARY KEY,
  user_id INT,
  user_name VARCHAR(100), -- 冗余字段，避免 JOIN
  total_amount DECIMAL(10,2),
  created_at TIMESTAMP
);
```

### 表设计最佳实践

```sql
CREATE TABLE users (
  -- 主键：使用 BIGINT 或 UUID
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  -- 或
  id CHAR(36) PRIMARY KEY, -- UUID

  -- 业务字段
  email VARCHAR(255) NOT NULL UNIQUE,
  username VARCHAR(50) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,

  -- 状态字段
  status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',

  -- 时间戳（必需）
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP NULL, -- 软删除

  -- 索引
  INDEX idx_email (email),
  INDEX idx_username (username),
  INDEX idx_status (status),
  INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 索引策略

### 索引类型

#### B-Tree 索引（默认）
```sql
-- 单列索引
CREATE INDEX idx_email ON users(email);

-- 复合索引（顺序很重要）
CREATE INDEX idx_user_status_created ON users(user_id, status, created_at);

-- 使用规则：最左前缀原则
-- 可以使用：user_id
-- 可以使用：user_id, status
-- 可以使用：user_id, status, created_at
-- 不能使用：status
-- 不能使用：created_at
```

#### 唯一索引
```sql
CREATE UNIQUE INDEX idx_email ON users(email);
```

#### 全文索引
```sql
CREATE FULLTEXT INDEX idx_content ON articles(title, content);

-- 使用
SELECT * FROM articles
WHERE MATCH(title, content) AGAINST('search term' IN NATURAL LANGUAGE MODE);
```

### 索引优化原则

1. **选择性高的列**：区分度高的列适合建索引
2. **查询频繁的列**：WHERE、JOIN、ORDER BY 中的列
3. **避免过多索引**：影响写入性能
4. **复合索引顺序**：选择性高的列在前

```sql
-- ✅ 好的索引
CREATE INDEX idx_status_created ON orders(status, created_at);
-- status 选择性高，created_at 用于排序

-- ❌ 不好的索引
CREATE INDEX idx_gender ON users(gender);
-- gender 只有 2-3 个值，选择性太低
```

## 查询优化

### EXPLAIN 分析
```sql
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';

-- 关注：
-- type: ALL（全表扫描）< index < range < ref < eq_ref < const
-- key: 使用的索引
-- rows: 扫描的行数
-- Extra: Using filesort, Using temporary（需要优化）
```

### 避免全表扫描
```sql
-- ❌ 不好
SELECT * FROM users WHERE YEAR(created_at) = 2024;

-- ✅ 好
SELECT * FROM users
WHERE created_at >= '2024-01-01' AND created_at < '2025-01-01';
```

### 避免 SELECT *
```sql
-- ❌ 不好
SELECT * FROM users WHERE id = 1;

-- ✅ 好
SELECT id, name, email FROM users WHERE id = 1;
```

### 分页优化
```sql
-- ❌ 不好（深分页）
SELECT * FROM users ORDER BY id LIMIT 100000, 20;

-- ✅ 好（使用游标）
SELECT * FROM users WHERE id > 100000 ORDER BY id LIMIT 20;
```

### JOIN 优化
```sql
-- 小表驱动大表
-- ✅ 好
SELECT u.*, o.*
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active';

-- 避免子查询，使用 JOIN
-- ❌ 不好
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders WHERE status = 'completed');

-- ✅ 好
SELECT DISTINCT u.*
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed';
```

## 事务管理

### ACID 原则
```sql
START TRANSACTION;

-- 原子性（Atomicity）
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- 一致性（Consistency）
-- 余额总和不变

-- 隔离性（Isolation）
-- 事务之间互不干扰

-- 持久性（Durability）
-- 提交后永久保存

COMMIT;
-- 或
ROLLBACK;
```

### 隔离级别
```sql
-- READ UNCOMMITTED（读未提交）- 脏读
-- READ COMMITTED（读已提交）- 不可重复读
-- REPEATABLE READ（可重复读）- 幻读（MySQL 默认）
-- SERIALIZABLE（串行化）- 性能最差

SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
```

### 死锁预防
```sql
-- 1. 按相同顺序访问资源
-- 2. 缩短事务时间
-- 3. 使用较低的隔离级别
-- 4. 添加合理的超时

-- 检测死锁
SHOW ENGINE INNODB STATUS;
```

## NoSQL 数据库

### MongoDB 设计模式

#### 嵌入式文档
```javascript
// ✅ 一对少：嵌入
{
  _id: ObjectId("..."),
  name: "John Doe",
  addresses: [
    { street: "123 Main St", city: "NYC" },
    { street: "456 Oak Ave", city: "LA" }
  ]
}
```

#### 引用
```javascript
// ✅ 一对多：引用
// users collection
{
  _id: ObjectId("user1"),
  name: "John Doe"
}

// orders collection
{
  _id: ObjectId("order1"),
  user_id: ObjectId("user1"),
  total: 100
}
```

### Redis 使用模式

```javascript
// 缓存
await redis.setex('user:123', 3600, JSON.stringify(user));

// 计数器
await redis.incr('page:views');

// 排行榜
await redis.zadd('leaderboard', score, userId);

// 分布式锁
const lock = await redis.set('lock:resource', 'token', 'NX', 'EX', 10);
```

## 数据库性能优化

### 连接池配置
```javascript
const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'password',
  database: 'mydb',
  connectionLimit: 10, // 根据负载调整
  queueLimit: 0,
  waitForConnections: true
});
```

### 批量操作
```sql
-- ❌ 不好
INSERT INTO users (name) VALUES ('User1');
INSERT INTO users (name) VALUES ('User2');
INSERT INTO users (name) VALUES ('User3');

-- ✅ 好
INSERT INTO users (name) VALUES
  ('User1'),
  ('User2'),
  ('User3');
```

### 分区表
```sql
CREATE TABLE orders (
  id BIGINT,
  user_id BIGINT,
  created_at DATE
)
PARTITION BY RANGE (YEAR(created_at)) (
  PARTITION p2022 VALUES LESS THAN (2023),
  PARTITION p2023 VALUES LESS THAN (2024),
  PARTITION p2024 VALUES LESS THAN (2025)
);
```

### 读写分离
```javascript
// 主库：写操作
const master = createConnection(masterConfig);
await master.query('INSERT INTO users ...');

// 从库：读操作
const slave = createConnection(slaveConfig);
await slave.query('SELECT * FROM users ...');
```

## 数据迁移

### 版本化迁移
```sql
-- migrations/001_create_users_table.sql
CREATE TABLE users (
  id BIGINT PRIMARY KEY,
  name VARCHAR(100)
);

-- migrations/002_add_email_to_users.sql
ALTER TABLE users ADD COLUMN email VARCHAR(255);
CREATE INDEX idx_email ON users(email);
```

### 零停机迁移
```sql
-- 1. 添加新列（可空）
ALTER TABLE users ADD COLUMN new_field VARCHAR(100) NULL;

-- 2. 双写（应用层）
-- 同时写入旧字段和新字段

-- 3. 数据迁移
UPDATE users SET new_field = old_field WHERE new_field IS NULL;

-- 4. 切换读取
-- 应用层改为读取新字段

-- 5. 删除旧列
ALTER TABLE users DROP COLUMN old_field;
```

## 备份和恢复

### 备份策略
```bash
# 全量备份
mysqldump -u root -p mydb > backup.sql

# 增量备份（binlog）
mysqlbinlog --start-datetime="2024-01-01 00:00:00" \
            --stop-datetime="2024-01-02 00:00:00" \
            mysql-bin.000001 > incremental.sql

# 自动化备份
0 2 * * * /usr/bin/mysqldump -u root -p mydb > /backups/$(date +\%Y\%m\%d).sql
```

### 恢复
```bash
# 恢复全量备份
mysql -u root -p mydb < backup.sql

# 恢复增量备份
mysql -u root -p mydb < incremental.sql
```

## 监控指标

### 关键指标
```sql
-- 慢查询
SHOW VARIABLES LIKE 'slow_query_log';
SHOW VARIABLES LIKE 'long_query_time';

-- 连接数
SHOW STATUS LIKE 'Threads_connected';
SHOW STATUS LIKE 'Max_used_connections';

-- 缓存命中率
SHOW STATUS LIKE 'Qcache_hits';
SHOW STATUS LIKE 'Qcache_inserts';

-- 锁等待
SHOW STATUS LIKE 'Table_locks_waited';
SHOW STATUS LIKE 'Innodb_row_lock_waits';
```

## 安全最佳实践

### SQL 注入防护
```javascript
// ❌ 不好
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ✅ 好
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);
```

### 权限管理
```sql
-- 最小权限原则
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'password';
GRANT SELECT, INSERT, UPDATE ON mydb.* TO 'app_user'@'localhost';

-- 只读用户
CREATE USER 'readonly'@'localhost' IDENTIFIED BY 'password';
GRANT SELECT ON mydb.* TO 'readonly'@'localhost';
```

### 数据加密
```sql
-- 敏感字段加密
CREATE TABLE users (
  id BIGINT PRIMARY KEY,
  email VARCHAR(255),
  ssn VARBINARY(255) -- 加密存储
);

-- 应用层加密/解密
INSERT INTO users (email, ssn) VALUES ('user@example.com', AES_ENCRYPT('123-45-6789', 'key'));
SELECT email, AES_DECRYPT(ssn, 'key') FROM users;
```

## 检查清单

设计或审查数据库时检查：

- [ ] 表结构符合范式要求
- [ ] 主键和外键定义正确
- [ ] 索引策略合理
- [ ] 查询性能优化
- [ ] 事务使用正确
- [ ] 连接池配置合理
- [ ] 备份策略完善
- [ ] 监控指标设置
- [ ] 安全防护到位
- [ ] 迁移脚本版本化
- [ ] 文档完整
