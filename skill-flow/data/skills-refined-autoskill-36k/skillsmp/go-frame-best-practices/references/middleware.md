# 中间件开发指南

GoFrame 中间件用于处理 HTTP 请求的通用逻辑，如认证、日志、跨域等。

## 中间件基础

### 定义中间件

```go
func MiddlewareAuth(r *ghttp.Request) {
    token := r.Get("token")
    if token == "123456" {
        r.Middleware.Next()
    } else {
        r.Response.WriteStatus(http.StatusForbidden)
    }
}

func MiddlewareLog(r *ghttp.Request) {
    r.Middleware.Next()
    errStr := ""
    if err := r.GetError(); err != nil {
        errStr = err.Error()
    }
    g.Log().Println(r.Response.Status, r.URL.Path, errStr)
}
```

## 统一响应格式中间件

```go
type Response struct {
    Code    int         `json:"code"`
    Message string      `json:"message"`
    Data    interface{} `json:"data"`
}

func ResponseMiddleware(r *ghttp.Request) {
    r.Middleware.Next()

    var (
        msg string
        res = r.GetHandlerResponse()
        err = r.GetError()
    )
    if err != nil {
        msg = err.Error()
    } else {
        msg = "OK"
    }
    r.Response.WriteJson(Response{
        Code:    0,
        Message: msg,
        Data:    res,
    })
}
```

## 错误处理中间件

```go
func ErrorHandler(r *ghttp.Request) {
    r.Middleware.Next()
    if err := r.GetError(); err != nil {
        r.Response.WriteJsonExit(CommonRes{
            Code:  500,
            Error: err.Error(),
        })
    }
}
```

## 分组路由中间件

```go
func main() {
    s := g.Server()

    // 全局中间件（所有路由都会执行）
    s.Use(ResponseMiddleware)

    // 分组路由
    s.Group("/api.v1", func(group *ghttp.RouterGroup) {
        // 分组中间件（只有 /api.v1 下的路由执行）
        group.Middleware(MiddlewareAuth, MiddlewareCORS)

        // 注册路由
        group.POST("/user/register", controller.Register)
        group.POST("/user/login", controller.Login)

        // 嵌套分组
        group.Group("/order", func(sub *ghttp.RouterGroup) {
            sub.GET("/list", controller.OrderList)
            sub.POST("/create", controller.OrderCreate)
        })
    })

    s.SetPort(8199)
    s.Run()
}
```

## 中间件执行顺序

1. 全局中间件（按注册顺序）
2. 分组中间件（按层级顺序）
3. 路由处理函数
4. 逆序执行各中间件的后续逻辑
