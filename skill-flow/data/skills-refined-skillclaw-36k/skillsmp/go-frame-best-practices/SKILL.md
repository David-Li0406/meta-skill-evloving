---
name: go-frame-best-practices
description: 提供 GoFrame 框架的官方最佳实践指导，包括项目结构、分层架构、配置管理、数据校验、数据库操作、中间件开发等开发规范
---

# GoFrame 框架开发最佳实践

提供 GoFrame 框架的官方最佳实践指导，包括项目结构、分层架构、配置管理、数据校验、数据库操作、中间件开发等开发规范。

## 触发条件

当用户询问以下问题时，此 Skill 会被触发：
- go-frame 最佳实践
- go-frame 开发规范
- go-frame 项目结构
- go-frame 分层架构
- go-frame 路由注册
- go-frame 数据库操作
- go-frame 事务处理
- go-frame 配置管理
- go-frame 中间件
- go-frame API 文档
- go-frame 校验参数

## 核心内容

此 Skill 提供 GoFrame 框架开发的核心指导原则。详细内容包括项目目录结构、分层架构设计、配置管理、数据校验、数据库 CRUD 操作、事务处理、中间件开发、日志管理、API 文档生成等。

### 项目目录结构

GoFrame 官方推荐的标准目录结构如下：

```
├── api                  # API 接口定义层
│   └── user             # 按模块划分
│       └── v1           # 版本号
│           └── user.go  # 接口定义文件
├── internal
│   ├── cmd              # 命令行启动入口
│   │   └── cmd.go       # 服务启动命令
│   ├── controller       # 控制器层（请求接收）
│   │   └── user         # 按模块划分
│   │       └── user.go
│   ├── logic            # 业务逻辑层（核心）
│   │   └── user
│   │       └── user.go
│   ├── model            # 数据模型层
│   │   ├── entity.go    # 数据库实体
│   │   └── do.go        # 数据对象
│   └── service          # 服务层
├── manifest             # 部署配置
│   ├── config           # 配置文件
│   └── docker           # Docker 配置
├── go.mod
└── main.go
```

关键原则：
- `internal` 目录下的包只能被本项目导入，确保内部逻辑不对外暴露
- 使用 `api` 定义接口契约，`internal` 实现具体逻辑
- `cmd` 目录下管理服务启动命令

### 分层架构设计

GoFrame 采用经典的三层（或四层）架构设计：

1. **Controller 层**：负责接收请求、参数校验，调用 Logic 层处理业务逻辑。Controller 层保持轻量，只做请求转发，使用依赖注入方式注入 Logic 层。

2. **Logic 层**：是核心业务处理单元，负责具体的业务规则实现。事务处理在 Logic 层进行，保持 Controller 和 Logic 的单向依赖。

3. **Model 层**：定义数据结构，包括实体和数据传输对象。使用 `dc:` tag 添加字段描述用于 API 文档。

### 配置管理

GoFrame 使用 `g.Cfg()` 单例管理配置，支持多种配置文件格式（toml/yaml/yml/json/ini/xml/properties）。配置项支持层级访问（使用 `.` 分隔）。

### 数据校验

使用 `v:"规则#错误信息"` 格式定义校验规则，使用 `p:` tag 定义参数名，使用 `dc:` tag 添加字段描述。使用 `g.Validator()` 进行参数校验。

### 数据库操作

基础 CRUD 操作使用 `g.DB().Model()` 方法，事务处理使用 `Transaction()` 或 `TransactionWithOptions()` 方法。根据业务场景选择合适的隔离级别。

### 中间件开发

中间件使用 `r.Middleware.Next()` 执行后续逻辑，错误处理中间件放在最后。遵循职责单一原则。

### API 文档生成

使用 `s.SetOpenApiPath()` 和 `s.SetSwaggerPath()` 启用 Swagger 文档。使用 `g.Meta` 定义接口元信息，使用 `dc:` tag 描述字段含义。

## 参考资源

详细内容和代码示例请参考以下文件：
- `references/project-structure.md` - 项目目录结构详解
- `references/layered-architecture.md` - 分层架构设计模式
- `references/configuration.md` - 配置管理最佳实践
- `references/database.md` - 数据库操作和事务处理
- `references/middleware.md` - 中间件开发指南
- `examples/controller-example.go` - Controller 层示例代码
- `examples/logic-example.go` - Logic 层示例代码
- `examples/middleware-example.go` - 中间件示例代码

## 常用命令

| 命令 | 说明 |
|------|------|
| `gf run main.go` | 快速运行项目 |
| `gf gen ctrl` | 生成 Controller |
| `gf gen service` | 生成 Service |
| `gf gen pb` | 生成 Protobuf 文件 |

## 官方资源

- [GoFrame 官方文档](https://goframe.org/)
- [GoFrame GitHub](https://github.com/gogf/gf)
- [GoFrame 示例项目](https://github.com/gogf/gf-demo-user)
