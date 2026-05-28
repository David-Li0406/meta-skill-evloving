# MySQL 事务与锁机制深度解析

## 一、事务隔离级别与实现原理

### 1.1 隔离级别 (Isolation Level)
| 隔离级别 | 脏读 | 不可重复读 | 幻读 | 实现方式 |
| :--- | :--- | :--- | :--- | :--- |
| **Read Uncommitted** | ✅ | ✅ | ✅ | 不加锁，读取最新版本 |
| **Read Committed (RC)** | ❌ | ✅ | ✅ | MVCC (每次 Select 生成 ReadView) |
| **Repeatable Read (RR)** | ❌ | ❌ | ❌ (InnoDB 解决) | MVCC (第一次 Select 生成 ReadView) + Gap Lock |
| **Serializable** | ❌ | ❌ | ❌ | 所有 Select 转为 Select ... in share mode |

### 1.2 MVCC (多版本并发控制) 原理

MVCC 使得 InnoDB 能够在不加锁的情况下实现并发读写。

#### 核心组件
1.  **隐藏字段**:
    *   `DB_TRX_ID`: 最近修改该行数据的事务 ID。
    *   `DB_ROLL_PTR`: 回滚指针，指向 Undo Log 中的旧版本。
    *   `DB_ROW_ID`: 隐藏主键。
2.  **Undo Log (回滚日志)**: 存储历史版本数据，形成版本链。
3.  **ReadView (一致性视图)**:
    *   `m_ids`: 当前活跃的事务 ID 列表。
    *   `min_trx_id`: 活跃事务中最小 ID。
    *   `max_trx_id`: 生成 ReadView 时系统分配的下一个 ID。

#### 可见性判断算法
当事务 A (ID=100) 读取某行数据 (trx_id=50) 时：
1.  如果 `trx_id < min_trx_id`: 说明该版本在事务 A 开启前已提交 -> **可见**。
2.  如果 `trx_id >= max_trx_id`: 说明该版本在事务 A 开启后才创建 -> **不可见**。
3.  如果 `min_trx_id <= trx_id < max_trx_id`:
    *   如果 `trx_id` 在 `m_ids` 中: 说明该版本由尚未提交的事务创建 -> **不可见**。
    *   如果 `trx_id` 不在 `m_ids` 中: 说明该版本由已提交事务创建 -> **可见**。

**结论**: RC 级别下，每次 Select 都重新生成 ReadView，所以能看到别的事务新提交的数据。RR 级别下，只有第一次 Select 生成 ReadView，后续复用，所以看不到。

## 二、InnoDB 锁机制

### 2.1 锁的分类
*   **共享锁 (S Lock)**: 读锁。`SELECT ... LOCK IN SHARE MODE`。
*   **排他锁 (X Lock)**: 写锁。`SELECT ... FOR UPDATE`, `UPDATE`, `DELETE`, `INSERT`。

### 2.2 行锁算法 (Row Locks)
InnoDB 的锁是**加在索引上**的，不是加在数据行上的。

1.  **Record Lock (记录锁)**: 锁住索引记录本身。
    *   `SELECT * FROM user WHERE id = 1 FOR UPDATE` (id 是主键)
2.  **Gap Lock (间隙锁)**: 锁住索引记录之间的间隙，防止插入 (解决幻读)。
    *   `SELECT * FROM user WHERE id > 10 FOR UPDATE`
3.  **Next-Key Lock**: Record Lock + Gap Lock。锁住左开右闭区间 `(5, 10]`。

### 2.3 间隙锁 (Gap Lock) 案例图解

假设表 `t` (id PK): 5, 10, 15, 20。

**案例 1: 等值查询 (不存在的记录)**
```sql
-- 事务 A
SELECT * FROM t WHERE id = 7 FOR UPDATE;
```
*   **分析**: id=7 不存在，落在 (5, 10) 区间。
*   **结果**: InnoDB 会加 Gap Lock `(5, 10)`。
*   **影响**: 其他事务插入 id=6, 8, 9 会被阻塞，直到 A 提交。

**案例 2: 范围查询**
```sql
-- 事务 A
SELECT * FROM t WHERE id > 10 FOR UPDATE;
```
*   **结果**: 锁住 `(10, 15]`, `(15, 20]`, `(20, +∞)`。
*   **注意**: 即使是 RC 级别，Update 语句也会加锁，但 RC 没有 Gap Lock，只有 Record Lock。这也是为什么 RR 比 RC 更容易死锁的原因。

## 三、死锁 (Deadlock) 分析

### 3.1 经典死锁案例 (AB - BA)
*   事务 A: `UPDATE user SET age=10 WHERE id=1;` (持有 id=1 X锁)
*   事务 B: `UPDATE user SET age=20 WHERE id=2;` (持有 id=2 X锁)
*   事务 A: `UPDATE user SET age=11 WHERE id=2;` (等待 id=2 X锁)
*   事务 B: `UPDATE user SET age=21 WHERE id=1;` (等待 id=1 X锁) -> **死锁**

### 3.2 间隙锁死锁
*   事务 A: `SELECT * FROM t WHERE id = 7 FOR UPDATE;` (持有 (5, 10) Gap Lock)
*   事务 B: `SELECT * FROM t WHERE id = 8 FOR UPDATE;` (Gap Lock 之间兼容，B 也持有 (5, 10) Gap Lock)
*   事务 A: `INSERT INTO t VALUES (7);` (被 B 的 Gap Lock 阻塞)
*   事务 B: `INSERT INTO t VALUES (8);` (被 A 的 Gap Lock 阻塞) -> **死锁**

### 3.3 如何排查
1.  查看死锁日志: `SHOW ENGINE INNODB STATUS`。
2.  查看 LATEST DETECTED DEADLOCK 部分。
