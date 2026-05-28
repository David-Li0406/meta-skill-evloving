# 配置管理最佳实践

GoFrame 提供强大的配置管理组件，支持多种配置文件格式和配置源。

## 配置文件格式

### YAML 配置示例

```yaml
# manifest/config/config.yaml
server:
  address:     ":8888"
  openapiPath: "/api.json"
  swaggerPath: "/swagger"
  dumpRouterMap: false

database:
  default:
    link:  "mysql:root:12345678@tcp(127.0.0.1:3306)/test"
    debug:  true
    charset: "utf8mb4"

redis:
  default:
    address: "127.0.0.1:6379"
    db:      1
```

## 配置读取方式

### 使用 g.Cfg() 单例

```go
import (
    "github.com/gogf/gf/v2/frame/g"
    "github.com/gogf/gf/v2/os/gctx"
)

func main() {
    ctx := gctx.New()

    // 读取单个配置项
    address := g.Cfg().MustGet(ctx, "server.address").String()

    // 读取嵌套配置
    databaseConfig := g.Cfg().MustGet(ctx, "database.default").Map()

    // 读取带默认值的配置
    port := g.Cfg().Get(ctx, "server.port", 8080).Int()
}
```

### 使用配置适配器

```go
import (
    "github.com/gogf/gf/v2/os/gcfg"
    "github.com/gogf/gf/v2/os/gctx"
)

func main() {
    ctx := gctx.New()

    // 使用文件适配器创建配置对象
    adapter, err := gcfg.NewAdapterFile("config")
    if err != nil {
        panic(err)
    }
    config := gcfg.NewWithAdapter(adapter)

    fmt.Println(config.MustGet(ctx, "server.address").String())
}
```

## 配置层级访问

配置项支持使用 `.` 进行层级访问：

```go
// 访问深层配置
charset := g.Cfg().MustGet(ctx, "database.default.charset").String()

// 支持默认值
value := g.Cfg().Get(ctx, "not.exist.key", "default_value").String()
```

## 环境配置管理

GoFrame 支持通过环境变量覆盖配置：

```go
// 设置环境变量前缀
g.Cfg().SetEnvPrefix("MYAPP_")

// 环境变量格式
// MYAPP_SERVER_ADDRESS=:9090
```
