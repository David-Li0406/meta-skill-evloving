# MySQL Execution Flow & Architecture (执行流程与架构)

## 一、一条 SQL 语句是如何执行的

MySQL 的架构大体分为 **Server 层** 和 **存储引擎层**。

![MySQL Architecture](https://img-blog.csdnimg.cn/20210508161100123.png)

1.  **连接器 (Connector)**
    - 负责跟客户端建立连接、获取权限、维持和管理连接。
    - 命令：`mysql -h <host> -P <port> -u <user> -p`

2.  **查询缓存 (Query Cache)** (MySQL 8.0 已移除)
    - 之前的查询结果以 Key-Value 对的形式存储。Key 是 SQL 语句，Value 是结果。
    - 弊大于利：表数据更新，相关缓存全部失效。

3.  **分析器 (Analyzer)**
    - **词法分析**：识别关键字 (select, from) 和标识符 (表名, 列名)。
    - **语法分析**：判断 SQL 语句是否满足 MySQL 语法。

4.  **优化器 (Optimizer)**
    - 决定使用哪个索引。
    - 决定 Join 表的连接顺序。
    - 生成执行计划。

5.  **执行器 (Executor)**
    - 判断是否有权限。
    - 根据执行计划调用存储引擎接口。

6.  **存储引擎 (Storage Engine)**
    - 负责数据的存储和提取。
    - 插件式架构，常用 InnoDB, MyISAM, Memory。
    - **InnoDB**：支持事务、行级锁、外键，是默认引擎。

## 二、InnoDB 关键特性与日志

### 1. Buffer Pool (缓冲池)
- **作用**：缓存磁盘上的数据页，减少磁盘 IO。
- **机制**：
    - 读取数据时，先看 Buffer Pool 中有没有，有则直接读取，无则从磁盘加载。
    - 修改数据时，先修改 Buffer Pool 中的页（标记为 **脏页**），后台线程定期刷脏到磁盘。
- **LRU 算法**：MySQL 对标准 LRU 做了改进（分代 LRU），防止全表扫描导致热数据被淘汰。

### 2. Redo Log (重做日志) - 物理日志
- **作用**：保证事务的 **持久性 (Durability)**，实现 **Crash-safe** 能力。
- **内容**：记录的是"在某个数据页上做了什么修改"。
- **机制**：**WAL (Write-Ahead Logging)** 技术，先写日志，再写磁盘。
- **结构**：循环写。write pos 是写入点，checkpoint 是擦除点。

### 3. Bin Log (归档日志) - 逻辑日志
- **作用**：用于主从复制 (Replication) 和数据恢复。
- **属于**：Server 层，所有引擎通用。
- **内容**：记录语句的原始逻辑 (如 "给 ID=2 这一行的 c 字段加 1")。
- **模式**：
    - `Statement`：记录 SQL 语句。
    - `Row`：记录行内容的变化（推荐）。
    - `Mixed`：混合模式。
- **写入机制**：追加写。

### 4. 两阶段提交 (Two-Phase Commit)
为了保证 Redo Log 和 Bin Log 的数据一致性。
1.  **Prepare 阶段**：引擎将更新记录写入 Redo Log，状态设为 prepare。
2.  **Commit 阶段**：Server 写 Bin Log，然后通知引擎将 Redo Log 状态设为 commit。

### 5. Undo Log (回滚日志) - 逻辑日志
- **作用**：保证事务的 **原子性 (Atomicity)** 和实现 **MVCC**。
- **内容**：记录数据的逻辑变化。
    - Insert -> 记录 Delete
    - Delete -> 记录 Insert
    - Update -> 记录反向 Update
- **回滚**：执行 Undo Log 中的逆操作。

### 6. Double Write (双写机制)
- **解决问题**：**页断裂 (Partial Page Write)**。
    - 数据库页大小 (16KB) 与 操作系统页大小 (4KB) 不一致。若写一半断电，页损坏，Redo Log 无法恢复。
- **机制**：
    1. 脏页先拷贝到内存中的 Double Write Buffer。
    2. 顺序写入系统表空间的 Double Write 区 (磁盘)。
    3. 离散写入数据文件。
- **恢复**：如果页损坏，先从 Double Write 区找到副本恢复，再应用 Redo Log。
