---
name: code-review
description: 审查代码质量、性能、安全性和设计模式。检查项目特定的反模式（降级处理、错误处理、类型安全）。使用此 Skill 来审查 PR、优化代码、或检查 TypeScript 类型安全性。
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# 代码审查 Skill

## 审查检查清单

### 错误处理
- [ ] try-catch 使用具体错误类型（不是 `any`）
- [ ] 错误有用户提示（不只是 console.log）
- [ ] 没有空 catch 块
- [ ] Promise.allSettled 失败有提示

### 数据验证
- [ ] 没有 `as any`（或有充分理由并注释）
- [ ] 使用 `??` 而非 `||` 作为默认值
- [ ] 可选链不超过 2 层
- [ ] TypeScript strict 模式通过

### 降级处理
- [ ] 降级时有用户通知
- [ ] 没有 SecureStore 静默降级到 AsyncStorage
- [ ] 区分开发/生产环境

### 配置管理
- [ ] 没有硬编码超时/重试次数
- [ ] 没有硬编码 GPS/URL
- [ ] 角色判断使用枚举

### TODO/安全
- [ ] 生产代码没有 TODO/FIXME
- [ ] Token 使用 SecureStore
- [ ] 不记录敏感信息到日志

## 自动化检查命令

```bash
cd /Users/jietaoxie/my-prototype-logistics/frontend/CretasFoodTrace

# TypeScript 检查
npx tsc --noEmit --skipLibCheck

# 查找反模式
grep -r "as any" src/ --include="*.ts" --include="*.tsx" | head -20
grep -r "TODO\|FIXME" src/ --include="*.ts" --include="*.tsx" | head -20
grep -r "setTimeout.*[0-9]\{4,\}" src/ --include="*.ts" --include="*.tsx"
grep -r "AsyncStorage.*token" src/ --include="*.ts" --include="*.tsx"

# 查找大文件
find src/ -name "*.ts" -o -name "*.tsx" | xargs wc -l | sort -rn | head -10
```

## 项目特定规则

### 禁止使用的 API 客户端

| 禁止使用 | 应该使用 |
|----------|----------|
| `attendanceApiClient` | `timeclockApiClient` |
| `employeeApiClient` | `userApiClient` |
| `enhancedApiClient` | `apiClient` |

### TypeScript 配置

- `strict: true`
- `noImplicitAny: true`
- `strictNullChecks: true`

## 参考

- 详细规范: `CLAUDE.md` 中的 "禁止的开发模式"
- ESLint: `.eslintrc.js`
