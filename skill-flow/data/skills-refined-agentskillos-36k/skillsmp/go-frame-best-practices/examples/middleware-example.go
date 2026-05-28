// 中间件示例代码

package main

import (
    "net/http"

    "github.com/gogf/gf/v2/frame/g"
    "github.com/gogf/gf/v2/net/ghttp"
    "github.com/gogf/gf/v2/util/gconv"
)

// CORS 中间件 - 处理跨域
func MiddlewareCORS(r *ghttp.Request) {
    r.Response.CORSDefault()
    r.Middleware.Next()
}

// Auth 中间件 - 认证检查
func MiddlewareAuth(r *ghttp.Request) {
    token := r.Get("token")
    if gconv.String(token) == "123456" {
        r.Middleware.Next()
    } else {
        r.Response.WriteStatus(http.StatusForbidden)
    }
}

// Log 中间件 - 请求日志
func MiddlewareLog(r *ghttp.Request) {
    r.Middleware.Next()
    errStr := ""
    if err := r.GetError(); err != nil {
        errStr = err.Error()
    }
    g.Log().Println(r.Response.Status, r.URL.Path, errStr)
}

// ResponseMiddleware 统一响应格式
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

func main() {
    s := g.Server()

    // 全局中间件
    s.Use(ResponseMiddleware)

    // 分组路由
    s.Group("/api.v1", func(group *ghttp.RouterGroup) {
        group.Middleware(MiddlewareAuth, MiddlewareCORS)

        group.GET("/user/list", func(r *ghttp.Request) {
            r.Response.Write("user list")
        })

        group.POST("/user/create", func(r *ghttp.Request) {
            r.Response.Write("user created")
        })
    })

    s.SetPort(8199)
    s.Run()
}
