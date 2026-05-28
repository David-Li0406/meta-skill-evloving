# 常见错误速查表

## 后端错误 (Spring Boot)

| 错误 | 原因 | 解决命令 |
|------|------|----------|
| `Unknown column 'xxx' in 'field list'` | Entity 字段与数据库不匹配 | `ALTER TABLE xxx ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP` |
| `NullPointerException` | 空指针访问 | `ssh root@139.196.165.140 "grep -A30 'NullPointerException' /www/wwwroot/cretas/cretas-backend.log"` |
| `Infinite recursion` (JSON) | 循环引用 | 添加 `@JsonIgnore` 或 `@JsonBackReference` |
| `401 Unauthorized` | Token 过期/格式错误 | `echo "TOKEN" \| cut -d'.' -f2 \| base64 -d \| jq '.exp'` |
| `403 Forbidden` | 用户角色/工厂权限不匹配 | 检查 JWT 中的 role 和 factoryId |
| `404 Not Found` | 路径错误或资源不存在 | 确认 `/api/mobile/` 前缀和资源 ID |

## 前端错误 (React Native)

| 错误 | 原因 | 解决命令 |
|------|------|----------|
| `Network request failed` | 无法连接 API | `nc -zv 139.196.165.140 10010` |
| `timeout exceeded` | 请求超时 | 检查网络/增加超时时间 |
| `Property 'xxx' does not exist` | 类型定义缺失 | 更新 interface 添加属性 |
| `Type 'xxx' is not assignable` | 类型不匹配 | 检查 API 响应类型，避免 `as any` |
| 白屏/崩溃 | Metro 编译错误 | `npx expo start --clear` |
| 依赖冲突 | node_modules 损坏 | `rm -rf node_modules && npm install` |
| Native 模块错误 | prebuild 需要更新 | `npx expo prebuild --clean` |

## 数据库错误

| 错误 | 原因 | 解决命令 |
|------|------|----------|
| `Connection refused` | MySQL 未运行 | `mysql.server start` (macOS) |
| `Access denied` | 密码错误 | `mysql -u root -p` 验证 |
| `Too many connections` | 连接数超限 | `SHOW PROCESSLIST;` 然后杀死空闲连接 |

## 部署错误

| 错误 | 原因 | 解决命令 |
|------|------|----------|
| 端口被占用 | 旧进程未退出 | `lsof -i:10010 && kill -9 <PID>` |
| 内存不足 | JVM 内存过大 | `java -Xmx512m -jar app.jar` |
| 日志无输出 | 重定向/权限问题 | 检查 nohup 和磁盘空间 |

## Android 模拟器注意

- 使用 `10.0.2.2` 替代 `localhost` 访问本机 API

## 快速诊断

```bash
# 检查后端日志
ssh root@139.196.165.140 "tail -100 /www/wwwroot/cretas/cretas-backend.log"

# 验证 API 健康
curl http://139.196.165.140:10010/api/mobile/health

# 检查数据库
mysql -u root cretas_db -e "SELECT 1"

# 前端环境
npx expo doctor
```
