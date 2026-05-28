---
name: debugging
description: Use this skill when debugging issues, analyzing errors, or troubleshooting incidents through systematic methods and log analysis.
---

# 调试技能

本技能提供系统化的调试方法和技巧。

## 触发条件

- 调试代码问题
- 分析错误日志
- 调查性能问题
- 排查生产事故
- 修复 Bug

## 调试原则

### 黄金法则

1. **复现问题** - 先能稳定复现，再开始调试
2. **最小化** - 找到最小可复现用例
3. **二分法** - 缩小问题范围
4. **假设验证** - 提出假设，验证假设
5. **记录过程** - 记录尝试过的方法

### 调试流程

```
问题描述 → 复现问题 → 缩小范围 → 定位原因 → 修复验证 → 记录总结
```

## 问题描述模板

```markdown
## 问题描述

[简要描述问题现象]

## 预期行为

[期望的正确行为]

## 实际行为

[实际观察到的行为]

## 复现步骤

1. [步骤1]
2. [步骤2]
3. [步骤3]

## 环境信息

- OS: [操作系统]
- Node/Python 版本: [版本]
- 相关依赖版本: [版本]

## 错误信息

[完整的错误堆栈或日志]

## 已尝试的方案

- [ ] 方案1 - 结果
- [ ] 方案2 - 结果
```

## 日志调试

### 有效的日志输出

```typescript
// ❌ 无用的日志
console.log("here");
console.log(data);

// ✅ 有信息量的日志
console.log("[UserService.createUser] 开始创建用户:", {
  email: user.email,
  timestamp: new Date().toISOString(),
});
```

```python
# ❌ 无用的日志
print("here")
print(data)

# ✅ 有信息量的日志
import logging
logger = logging.getLogger(__name__)

logger.info(f"[create_user] 开始创建用户: email={email}")
```

### 日志级别使用

| 级别  | 用途           | 示例               |
| ----- | -------------- | ------------------ |
| DEBUG | 详细调试信息   | 函数参数、中间状态 |
| INFO  | 正常操作信息   | 用户登录、订单创建 |
| WARN  | 警告但可继续   | 配置缺失使用默认值 |
| ERROR | 错误但可恢复   | API 调用失败重试   |
| FATAL | 致命错误需退出 | 数据库连接失败     |

## 断点调试

### VS Code 调试配置

```json
// .vscode/launch.json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Node.js",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/src/index.ts",
      "preLaunchTask": "tsc: build",
      "outFiles": ["${workspaceFolder}/dist/**/*.js"]
    },
    {
      "name": "Debug Python",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal"
    }
  ]
}
```

### 条件断点

```typescript
// 在循环中只在特定条件暂停
for (const item of items) {
  // 条件断点: item.id === 'target-id'
  processItem(item);
}
```

## 网络调试

### 请求/响应日志

```typescript
// Axios 拦截器
axios.interceptors.request.use((config) => {
  console.log("[HTTP Request]", {
    method: config.method,
    url: config.url,
    data: config.data,
  });
  return config;
});
```

### cURL 调试

```bash
# 详细输出
curl -v https://api.example.com/users
```

## 数据库调试

### 查询日志

```typescript
// Prisma 查询日志
const prisma = new PrismaClient({
  log: [
    { emit: "event", level: "query" },
    { emit: "stdout", level: "info" },
    { emit: "stdout", level: "warn" },
    { emit: "stdout", level: "error" },
  ],
});
```

### 慢查询分析

```sql
-- PostgreSQL 查询计划
EXPLAIN ANALYZE
SELECT * FROM orders WHERE user_id = '123';
```

## 性能调试

### 时间测量

```typescript
// 简单计时
const start = performance.now();
await someOperation();
console.log(`耗时: ${performance.now() - start}ms`);
```

## 前端调试

### Console 方法

```typescript
// 分组输出
console.group("用户数据");
console.log("ID:", user.id);
console.log("Name:", user.name);
console.groupEnd();
```

## 常见问题排查

### 异步问题

```typescript
// ❌ 忘记 await
async function fetchData() {
  const data = fetch("/api/data"); // 缺少 await
}
```

### 闭包陷阱

```typescript
// ❌ 闭包捕获变量
for (var i = 0; i < 5; i++) {
  setTimeout(() => console.log(i), 100); // 全部输出 5
}
```

## 调试清单

```markdown
## 调试前

- [ ] 能稳定复现问题吗？
- [ ] 最小复现用例是什么？
- [ ] 最近改动了什么？

## 调试中

- [ ] 查看错误日志和堆栈
- [ ] 添加必要的日志输出
- [ ] 使用断点逐步执行
- [ ] 检查输入数据是否正确
- [ ] 检查环境变量和配置

## 调试后

- [ ] 修复是否解决了根本原因？
- [ ] 是否需要添加测试？
- [ ] 是否需要更新文档？
- [ ] 是否有类似问题需要检查？
```

## 最佳实践

1. **先复现后调试** - 不能复现就无法确认修复
2. **二分法定位** - 缩小问题范围
3. **记录尝试** - 避免重复无效尝试
4. **查看最近改动** - git diff, git log
5. **橡皮鸭调试** - 向他人解释问题
6. **休息一下** - 换个思路
7. **搜索错误信息** - 可能他人遇到过
8. **检查假设** - 你认为正确的可能是错的
9. **简化问题** - 去除无关因素
10. **写测试固化** - 防止问题复现