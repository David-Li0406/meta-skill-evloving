---
name: error-code-guide
description: Use this skill to design consistent error codes following the PREFIX_CATEGORY_NUMBER format for defining error codes, establishing error handling, and designing APIs.
---

# 错误码指南

> **语言**: [English](../../../../../skills/claude-code/error-code-guide/SKILL.md) | 简体中文 | 繁體中文

**版本**: 1.0.0  
**最后更新**: 2025-12-30  
**适用范围**: Claude Code Skills

---

## 目的

此技能帮助设计一致的错误码，遵循标准格式，实现更好的调试、监控和用户体验。

## 快速参考

### 错误码格式

```
<前缀>_<类别>_<编号>
```

| 元素 | 说明 | 示例 |
|------|------|------|
| 前缀 (PREFIX) | 应用/服务识别码 | AUTH, PAY, USR |
| 类别 (CATEGORY) | 错误类别 | VAL, SYS, BIZ |
| 编号 (NUMBER) | 唯一数字识别码 | 001, 100, 404 |

### 示例

```
AUTH_VAL_001    → 认证验证错误
PAY_SYS_503     → 付款系统无法使用
USR_BIZ_100     → 用户商业规则违规
API_NET_408     → API 网络超时
```

### 错误类别

| 类别 | 全名 | 说明 | HTTP 状态码 |
|------|------|------|-------------|
| **VAL** | Validation | 客户端输入验证失败 | 400 |
| **BIZ** | Business | 商业规则违规 | 422 |
| **SYS** | System | 内部系统错误 | 500 |
| **NET** | Network | 通信错误 | 502/503/504 |
| **AUTH** | Auth | 安全相关错误 | 401/403 |

### 类别编号范围

| 范围 | 说明 | 示例 |
|------|------|------|
| *_VAL_001-099 | 字段验证 | 缺少必填字段 |
| *_VAL_100-199 | 格式验证 | 电子邮件格式无效 |
| *_VAL_200-299 | 约束验证 | 密码太短 |
| *_BIZ_001-099 | 状态违规 | 订单已取消 |
| *_BIZ_100-199 | 规则违规 | 超过 30 天无法退货 |
| *_BIZ_200-299 | 限制违规 | 超过每日限制 |
| *_AUTH_001-099 | 认证 | 账号密码错误 |
| *_AUTH_100-199 | 授权 | 权限不足 |
| *_AUTH_200-299 | Token/Session | Token 已过期 |

## HTTP 状态码对应

| 类别 | HTTP 状态码 | 说明 |
|------|-------------|------|
| VAL | 400 | Bad Request |
| BIZ | 422 | Unprocessable Entity |
| AUTH (001-099) | 401 | Unauthorized |
| AUTH (100-199) | 403 | Forbidden |
| SYS | 500 | Internal Server Error |
| NET | 502/503/504 | Gateway errors |

## 错误响应格式

### 单一错误

```json
{
  "success": false,
  "error": {
    "code": "AUTH_VAL_001",
    "message": "电子邮件为必填字段",
    "field": "email",
    "requestId": "req_abc123"
  }
}
```

### 多个错误

```json
{
  "success": false,
  "errors": [
    {
      "code": "AUTH_VAL_001",
      "message": "电子邮件为必填字段",
      "field": "email"
    },
    {
      "code": "AUTH_VAL_201",
      "message": "密码至少需要 8 个字符",
      "field": "password"
    }
  ],
  "requestId": "req_abc123"
}
```

## 内部错误对象

```typescript
interface ApplicationError {
  // 核心字段
  code: string;          // "AUTH_VAL_001"
  message: string;       // 技术消息（用于日志）

  // 用户界面
  userMessage: string;   // 本地化用户消息
  userMessageKey: string; // i18n 键值: "error.auth.val.001"

  // 上下文
  field?: string;        // 相关字段: "email"
  details?: object;      // 附加信息

  // 调试
  timestamp: string;     // ISO 8601
  requestId: string;     // 关联 ID
}
```

## 国际化 (i18n)

### 消息键值格式

```
error.<前缀>.<类别>.<编号>
```

### 翻译文件示例

```yaml
# en.yaml
error:
  auth:
    val:
      001: "Email is required"
      101: "Invalid email format"
    auth:
      001: "Invalid credentials"

# zh-TW.yaml
error:
  auth:
    val:
      001: "電子郵件為必填欄位"
      101: "電子郵件格式無效"
    auth:
      001: "帳號或密碼錯誤"
```

## 示例

### ✅ 良好的错误码

```javascript
AUTH_VAL_001  // 缺少必填字段: email
AUTH_VAL_101  // 电子邮件格式无效
ORDER_BIZ_001 // 订单已取消
ORDER_BIZ_201 // 超过每日购买限制
DB_SYS_001    // 数据库查询失败
SEC_AUTH_001  // 账号密码错误
SEC_AUTH_201  // Token 已过期
```

### ❌ 不良的错误码

```javascript
ERR_001       // 太模糊，没有前缀或类别
INVALID       // 不具描述性
error         // 不是错误码
AUTH_ERROR    // 缺少编号
```

## 检查清单

- [ ] 每个错误有唯一代码
- [ ] 类别符合错误类型
- [ ] 用户消息已本地化
- [ ] HTTP 状态码正确
- [ ] 错误已记录文件
- [ ] 代码已加入注册表

---

## 设置检测

此技能支持项目特定设置。

### 检测顺序

1. 检查代码库中现有的错误码模式
2. 检查 `CONTRIBUTING.md` 中的错误码指南
3. 若无找到，**预设使用 PREFIX_CATEGORY_NUMBER 格式**

### 首次设置

若未找到错误码标准：

1. 建议：「此项目尚未设置错误码标准。您要建立错误码注册表吗？」
2. 建议建立 `errors/registry.ts`：

```typescript
export const ErrorCodes = {
  AUTH_VAL_001: {
    code: 'AUTH_VAL_001',
    httpStatus: 400,
    messageKey: 'error.auth.val.001',
    description: '电子邮件字段为必填',
  },
  // ... 更多错误码
} as const;
```

---

## 相关标准

- [错误码标准](../../../core/error-code-standards.md)
- [日志标准](../../../core/logging-standards.md)

---

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2025-12-30 | 初始发布 |

---

## 授权

此技能采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 授权。

**来源**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)