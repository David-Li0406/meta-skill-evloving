# 分层架构设计模式

GoFrame 采用经典的三层（或四层）架构设计，实现关注点分离。

## 三层架构

```
┌─────────────────────────────────────────────────┐
│                   Controller                    │
│              (请求接收、参数校验)                 │
└─────────────────────┬───────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│                    Logic                        │
│               (核心业务逻辑处理)                  │
└─────────────────────┬───────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│                    Model                        │
│                (数据模型定义)                    │
└─────────────────────────────────────────────────┘
```

## 1. Controller 层

Controller 负责接收请求、参数校验，调用 Logic 层处理业务逻辑。

### 设计原则

- 保持轻量，只做请求转发
- 使用依赖注入方式注入 Logic 层
- 每个模块创建独立的 Controller 文件

### 示例代码

```go
// internal/controller/user/user.go
package user

import (
    "context"

    "your-project/api/user/v1"
    "your-project/internal/logic/user"
)

type Controller struct {
    userLogic *logic.User
}

// New 创建控制器实例，注入 Logic 层依赖
func New() v1.UserController {
    return &Controller{
        userLogic: logic.New(),
    }
}

func (c *Controller) Register(ctx context.Context, req *v1.RegisterReq) (res *v1.RegisterRes, err error) {
    return c.userLogic.Register(ctx, req)
}
```

## 2. Logic 层

Logic 层是核心业务处理单元，负责具体的业务规则实现。

### 设计原则

- 事务处理在 Logic 层进行
- 复杂的业务逻辑集中在 Logic 层
- 保持 Controller 和 Logic 的单向依赖

### 示例代码

```go
// internal/logic/user/user.go
package user

import (
    "context"

    "your-project/api/user/v1"
    "your-project/internal/model"
)

type User struct {
    // 注入数据库实例或其他服务
    db *gdb.DB
}

func New() *User {
    return &User{
        db: g.DB(),
    }
}

func (l *User) Register(ctx context.Context, req *v1.RegisterReq) (*v1.RegisterRes, error) {
    // 业务逻辑实现
    return &v1.RegisterRes{}, nil
}
```

## 3. Model 层

Model 层定义数据结构，包括实体和数据传输对象。

### 设计原则

- 实体与数据库表对应
- 使用 `dc:` tag 添加字段描述用于 API 文档
- 区分输入参数和输出结构

### 示例代码

```go
// internal/model/user.go
package model

// Entity 是数据库表对应的实体结构
type User struct {
    Id        int       `json:"id"      dc:"用户ID"`
    Username  string    `json:"username" dc:"用户名"`
    Password  string    `json:"-"       dc:"密码（不输出）"`
    CreatedAt *gtime.Time `json:"created_at" dc:"创建时间"`
    UpdatedAt *gtime.Time `json:"updated_at" dc:"更新时间"`
}

// CreateUserInput 创建用户的输入参数
type CreateUserInput struct {
    Username string
    Password string
}
```
