// Logic 层示例代码
// internal/logic/user/user.go

package user

import (
    "context"
    "errors"

    "your-project/api/user/v1"
    "your-project/internal/model"
)

type User struct {
    db *gdb.DB
}

func New() *User {
    return &User{
        db: g.DB(),
    }
}

// Register 用户注册
func (l *User) Register(ctx context.Context, req *v1.RegisterReq) (*v1.RegisterRes, error) {
    // 检查用户名是否已存在
    count, err := l.db.Model("user").Where("username", req.Username).Count()
    if err != nil {
        return nil, err
    }
    if count > 0 {
        return nil, errors.New("用户名已存在")
    }

    // 创建用户
    id, err := l.db.Model("user").InsertAndGetId(g.Map{
        "username": req.Username,
        "password": req.Password, // 实际开发中应加密
        "status":   1,
    })
    if err != nil {
        return nil, err
    }

    return &v1.RegisterRes{
        Id: int32(id),
    }, nil
}

// Login 用户登录
func (l *User) Login(ctx context.Context, req *v1.LoginReq) (*v1.LoginRes, error) {
    var user *model.User
    err := l.db.Model("user").
        Where("username", req.Username).
        Where("password", req.Password).
        Where("status", 1).
        Scan(&user)

    if err != nil {
        return nil, errors.New("用户名或密码错误")
    }

    // 生成 Token（示例，实际应使用 JWT 等）
    token := "token_" + req.Username

    return &v1.LoginRes{
        Token: token,
        User: &v1.UserInfo{
            Id:       int32(user.Id),
            Username: user.Username,
        },
    }, nil
}

// GetUserInfo 获取用户信息
func (l *User) GetUserInfo(ctx context.Context, uid int) (*v1.GetUserInfoRes, error) {
    var user *model.User
    err := l.db.Model("user").Where("id", uid).Scan(&user)
    if err != nil {
        return nil, err
    }

    return &v1.GetUserInfoRes{
        Id:       int32(user.Id),
        Username: user.Username,
    }, nil
}
