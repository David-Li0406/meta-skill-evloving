# 数据库操作和事务处理

GoFrame ORM 组件提供便捷的数据库操作接口。

## 基础 CRUD 操作

### 创建（Insert）

```go
// 单条插入
id, err := g.DB().Model("user").InsertAndGetId(g.Map{
    "username": "test",
    "password": "123456",
    "status":   1,
})

// 批量插入
_, err := g.DB().Model("user").Insert(g.Slice{
    g.Map{"username": "user1", "password": "pass1"},
    g.Map{"username": "user2", "password": "pass2"},
})
```

### 读取（Query）

```go
// 查询单条记录
var user *User
err := g.DB().Model("user").Where("id", 1).Scan(&user)

// 查询多条记录
var users []*User
err := g.DB().Model("user").Where("status", 1).Scan(&users)

// 条件查询
err := g.DB().Model("user").
    Where("status", 1).
    Where("username like ?", "%test%").
    OrderDesc("created_at").
    Limit(10).
    Scan(&users)
```

### 更新（Update）

```go
_, err := g.DB().Model("user").
    Where("id", 1).
    Update(g.Map{
        "username": "new_name",
        "status":   0,
    })

// 使用 Raw 防止 SQL 注入
_, err := g.DB().Model("account").
    Where("id", accountId).
    Update(g.Map{"balance": gdb.Raw("balance - ?", amount)})
```

### 删除（Delete）

```go
_, err := g.DB().Model("user").Where("id", 1).Delete()

// 软删除（更新状态）
_, err := g.DB().Model("user").
    Where("id", 1).
    Update(g.Map{"status": -1})
```

## 事务处理

### 基本事务

```go
err := g.DB().Transaction(ctx, func(ctx context.Context, tx *gdb.TX) error {
    // 业务逻辑
    _, err := tx.Model("order").Insert(orderData)
    if err != nil {
        return err
    }

    _, err = tx.Model("product").Where("id", productId).
        Update(g.Map{"stock": gdb.Raw("stock - ?", quantity)})

    return err
})
```

### 带隔离级别的事务

```go
import "database/sql"

err := db.TransactionWithOptions(ctx, gdb.TxOptions{
    Isolation: sql.LevelRepeatableRead,  // 可重复读
}, func(ctx context.Context, tx gdb.TX) error {
    // 事务逻辑
    return nil
})
```

### 常用隔离级别

| 隔离级别 | 说明 | 使用场景 |
|---------|------|---------|
| LevelDefault | 默认隔离级别 | 一般场景 |
| LevelReadUncommitted | 读未提交 | 对一致性要求不高的查询 |
| LevelReadCommitted | 读已提交 | 避免脏读 |
| LevelRepeatableRead | 可重复读 | 电商订单、库存处理 |
| LevelSerializable | 串行化 | 银行转账、金融交易 |
