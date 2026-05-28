# 项目目录结构详解

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

## 目录说明

### api/ - API 接口定义层
- 定义接口契约，对外暴露的 API
- 按模块划分，支持版本号管理
- 使用 protobuf 或 Go 结构体定义接口

### internal/ - 内部实现层
- `cmd/`：命令行启动入口，管理服务启动命令
- `controller/`：控制器层，负责接收请求、参数校验
- `logic/`：业务逻辑层，核心业务处理
- `model/`：数据模型层，定义数据结构

### manifest/ - 部署配置
- `config/`：配置文件（yaml、toml 等）
- `docker/`：Docker 部署配置

## 关键原则

1. **封装性**：`internal` 目录下的包只能被本项目导入，确保内部逻辑不对外暴露

2. **职责分离**：
   - 使用 `api` 定义接口契约
   - 使用 `internal` 实现具体逻辑
   - `cmd` 目录下管理服务启动命令

3. **模块化**：按业务模块划分目录，保持代码结构清晰
