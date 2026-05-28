---
name: mysql
description: MySQL 学习资料（原理 + 调优）
---

# MySQL 学习资料

## 1. 一条 SQL 的执行流程（需要能画出来）
- 连接器（权限/连接管理）
- 查询缓存（MySQL 8 移除，了解即可）
- 解析器（语法树）
- 优化器（索引选择、join 顺序）
- 执行器（调用存储引擎接口）
- InnoDB：Buffer Pool、Redo/Undo、二阶段提交（Redo + Binlog）

---

## 2. InnoDB 存储结构
- Page（默认 16KB）
- B+Tree：叶子节点存数据（聚簇）或主键（非聚簇）
- 聚簇索引：主键索引，叶子节点存整行
- 二级索引：叶子节点存主键值（回表）

---

## 3. 索引与 SQL 优化
### 3.1 联合索引最左前缀
- `(a,b,c)` 可用：`a`、`a,b`、`a,b,c`
- 注意：范围查询会影响后续列利用

### 3.2 覆盖索引
- 只从索引就能返回结果，避免回表

### 3.3 explain 要看什么
- type（ALL、range、ref、const…）
- key/rows/Extra（Using index/Using filesort/Using temporary）

---

## 4. 事务与锁
### 4.1 ACID
- 原子性：Undo
- 持久性：Redo
- 隔离性：锁 + MVCC
- 一致性：应用 + 数据库共同保证

### 4.2 MVCC
- 隐藏列：trx_id、roll_pointer
- ReadView：决定当前版本能不能被看到

### 4.3 锁
- 行锁、间隙锁（Gap Lock）、临键锁（Next-Key Lock）
- 避免死锁：固定顺序更新、减少范围锁、合适索引

---

## 5. 可运行示例代码建议
- MySQL demo 需要依赖驱动与数据库环境；如果你要我补一个 `jdbc` 小例子，我可以在仓库里加（需你提供连接信息或使用本地 docker）。

---

## 6. 高频面试题
1. 为什么 InnoDB 用 B+Tree，不用 BTree/Hash？
2. 聚簇索引和二级索引的区别？回表是什么？
3. RR 隔离级别如何避免幻读？Next-Key Lock 是什么？
4. MVCC 的 ReadView 怎么工作？
