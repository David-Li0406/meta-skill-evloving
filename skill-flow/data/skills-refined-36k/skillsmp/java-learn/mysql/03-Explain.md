# SQL Analysis & Optimization (语句分析与优化)

使用 `EXPLAIN` 关键字可以模拟优化器执行 SQL 查询语句，从而知道 MySQL 是如何处理你的 SQL 语句的。

## 一、Explain 字段详解

命令：`EXPLAIN SELECT ...`

| 字段 | 含义 |
| :--- | :--- |
| **id** | select 查询的序列号，表示查询中执行 select 子句或操作表的顺序。 |
| **select_type** | 查询的类型 (如 SIMPLE, PRIMARY, SUBQUERY, DERIVED)。 |
| **table** | 显示这一行的数据是关于哪张表的。 |
| **partitions** | 匹配的分区。 |
| **type** | **访问类型** (重要指标)。 |
| **possible_keys** | 显示可能应用在这张表上的索引。 |
| **key** | 实际使用的索引。如果为 NULL，则没有使用索引。 |
| **key_len** | 使用索引的字节数。 |
| **ref** | 显示索引的哪一列被使用了，如果可能的话，是一个常数。 |
| **rows** | 根据表统计信息及索引选用情况，大致估算出找到所需的记录所需要读取的行数。 |
| **filtered** | 查询条件过滤的行数百分比。 |
| **Extra** | **额外信息** (重要指标)。 |

### 1. id
- id 相同，执行顺序由上至下。
- id 不同，id 值越大优先级越高，越先被执行。

### 2. type (访问类型)
从最好到最差依次是：
**system > const > eq_ref > ref > range > index > ALL**

- **system**：表只有一行记录（系统表）。
- **const**：通过索引一次就找到了，用于 **Primary Key** 或 **Unique** 索引。
- **eq_ref**：唯一性索引扫描，对于每个索引键，表中只有一条记录与之匹配。常见于主键或唯一索引扫描。
- **ref**：非唯一性索引扫描，返回匹配某个单独值的所有行。
- **range**：只检索给定范围的行，使用一个索引来选择行。key 显示使用了哪个索引。常见于 `between`, `<`, `>`, `in` 等查询。
- **index**：**Full Index Scan**，遍历索引树。通常比 ALL 快，因为索引文件通常比数据文件小。
- **ALL**：**Full Table Scan**，全表扫描。

### 3. Extra (额外信息)
- **Using filesort**：说明 MySQL 会对数据使用一个外部的索引排序，而不是按照表内的索引顺序进行读取。**需要优化**。
- **Using temporary**：使用了临时表保存中间结果，MySQL 在对查询结果排序时使用临时表。常见于 `order by` 和 `group by`。**严重，需要优化**。
- **Using index**：表示相应的 select 操作中使用了 **覆盖索引 (Covering Index)**，避免访问了表的数据行，效率不错。
- **Using where**：使用了 where 过滤。
- **Using join buffer**：使用了连接缓存。

## 二、优化案例

### 1. 避免 `select *`
- 只查询需要的列，增加使用覆盖索引的可能性。

### 2. 最左前缀法则
- 联合索引 `(a, b, c)`。
- `where a=1 and b=2 and c=3` -> 用到 a, b, c
- `where a=1 and b=2` -> 用到 a, b
- `where a=1 and c=3` -> 只用到 a (c 失效)
- `where b=2` -> 不走索引 (a 缺失)

### 3. 不要在索引列上做任何操作
- 计算、函数、类型转换会导致索引失效而转向全表扫描。
- 例：`where left(name, 4) = 'test'` (失效)

### 4. 范围查询右边的列失效
- `where a=1 and b>2 and c=3` -> a, b 走索引，c 失效。

### 5. 尽量使用覆盖索引
- 减少 `select *`，查询列尽量和索引列一致。

### 6. `is null`, `is not null`
- 可能会导致索引失效（取决于数据分布）。

### 7. `like` 以通配符开头
- `like '%abc'` -> 索引失效。
- `like 'abc%'` -> 索引有效 (range)。
- 解决：使用覆盖索引可以挽救。

### 8. 字符串不加单引号
- 导致隐式类型转换，索引失效。
- 例：varchar 字段 `where name = 123` (失效)。

### 9. `or` 连接
- `or` 两边必须都有索引才会走索引，否则全表扫描。
