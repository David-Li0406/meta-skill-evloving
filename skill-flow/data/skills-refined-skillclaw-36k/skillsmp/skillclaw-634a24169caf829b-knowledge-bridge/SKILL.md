---
name: knowledge-bridge
description: Use this skill when you need to connect external standards and project conventions, while also maintaining a library of anti-patterns.
---

# Knowledge Bridge Skill

知识桥接，连接外部规范和项目约定。

## 🔗 外部规范索引

> **注意**: 请将以下路径修改为你实际的本地路径。

```markdown
## 公司规范

- **前端规范**: ~/.claude/references/frontend-standards.md
- **后端规范**: ~/.claude/references/backend-standards.md
- **API规范**: ~/.claude/references/api-standards.md
```

## 🚫 反模式库 (Anti-Patterns)

### 通用反模式

```typescript
// ❌ 禁止: 使用 any 类型
const data: any = response.data;

// ✅ 正确: 明确类型
const data: UserResponse = response.data;
```

```typescript
// ❌ 禁止: 硬编码 Secret
const apiKey = 'sk-xxx';

// ✅ 正确: 环境变量
const apiKey = process.env.API_KEY;
```

### 数据库反模式

```typescript
// ❌ 禁止: N+1查询
for (const user of users) {
  const orders = await db.query('SELECT * FROM orders WHERE user_id = ?', [user.id]);
}

// ✅ 正确: 批量查询
const orders = await db.query('SELECT * FROM orders WHERE user_id IN (?)', [userIds]);
```

### 安全反模式

```typescript
// ❌ 禁止: SQL拼接
const sql = `SELECT * FROM users WHERE id = ${userId}`;

// ✅ 正确: 参数化查询
const user = await db.query('SELECT * FROM users WHERE id = $1', [userId]);
```

## 📝 项目约定

在项目 `.ai_state/conventions.md` 中记录：

```markdown
## 项目约定

### 命名规范
- 组件: PascalCase
- 函数: camelCase
- 常量: UPPER_SNAKE_CASE

### 文件结构
- 组件: src/components/
- 页面: src/pages/
- 工具: src/utils/

### Git规范
- feat: 新功能
- fix: 修复
- refactor: 重构
```

## 🔄 规范更新

代码审查意见应沉淀为可执行的规则：

```markdown
1. 发现问题
2. 记录到反模式库
3. 更新自动化检查
4. 形成持续改进闭环
```

## 使用方式

```javascript
// 加载知识桥接
skill.load("knowledge-bridge");

// 检查代码是否违反反模式
knowledge.checkAntiPatterns(code);

// 获取项目约定
knowledge.getConventions();
```