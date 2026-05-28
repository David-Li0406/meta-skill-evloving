// Controller 层示例代码
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

// Register 用户注册
func (c *Controller) Register(ctx context.Context, req *v1.RegisterReq) (res *v1.RegisterRes, err error) {
    return c.userLogic.Register(ctx, req)
}

// Login 用户登录
func (c *Controller) Login(ctx context.Context, req *v1.LoginReq) (res *v1.LoginRes, err error) {
    return c.userLogic.Login(ctx, req)
}

// GetUserInfo 获取用户信息
func (c *Controller) GetUserInfo(ctx context.Context, req *v1.GetUserInfoReq) (res *v1.GetUserInfoRes, err error) {
    return c.userLogic.GetUserInfo(ctx, req.Uid)
}
