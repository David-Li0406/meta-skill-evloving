---
name: code-review-checklist
description: 代码审查清单和最佳实践。用于审查代码质量、安全性、性能和可维护性。
allowed-tools: Read, Grep, Glob
---

# 代码审查清单

## 代码质量

### 可读性
- [ ] 变量和函数命名清晰、有意义
- [ ] 代码结构清晰，逻辑易懂
- [ ] 复杂逻辑有注释说明
- [ ] 避免过深的嵌套（最多 3-4 层）
- [ ] 函数长度合理（一般不超过 50 行）

```typescript
// ❌ 不好
function p(d) {
  return d.filter(x => x.a > 10).map(x => x.b);
}

// ✅ 好
function getActiveUserNames(users: User[]) {
  const activeUsers = users.filter(user => user.age > 10);
  return activeUsers.map(user => user.name);
}
```

### 代码复用
- [ ] 避免重复代码（DRY 原则）
- [ ] 提取公共逻辑到函数或工具类
- [ ] 使用设计模式简化代码

### 错误处理
- [ ] 所有可能失败的操作都有错误处理
- [ ] 错误信息清晰、有帮助
- [ ] 避免空的 catch 块
- [ ] 使用适当的错误类型

```typescript
// ❌ 不好
try {
  await fetchData();
} catch (e) {
  // 空的 catch
}

// ✅ 好
try {
  await fetchData();
} catch (error) {
  console.error('Failed to fetch data:', error);
  showErrorToast('无法加载数据，请稍后重试');
  throw error;
}
```

### 边界条件
- [ ] 处理空值、null、undefined
- [ ] 处理空数组、空对象
- [ ] 处理极端值（0, -1, 最大值）
- [ ] 处理并发和竞态条件

## 性能

### 算法效率
- [ ] 时间复杂度合理
- [ ] 避免不必要的循环嵌套
- [ ] 使用合适的数据结构

### 前端性能
- [ ] 避免不必要的重渲染
- [ ] 大列表使用虚拟滚动
- [ ] 图片懒加载和优化
- [ ] 代码分割和懒加载

### 数据库查询
- [ ] 避免 N+1 查询
- [ ] 使用索引
- [ ] 分页处理大数据集
- [ ] 避免 SELECT *

## 安全性

### 输入验证
- [ ] 所有用户输入都经过验证
- [ ] 防止 SQL 注入
- [ ] 防止 XSS 攻击
- [ ] 防止 CSRF 攻击

```typescript
// ❌ 不好 - SQL 注入风险
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ✅ 好 - 使用参数化查询
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);
```

### 敏感信息
- [ ] 不在代码中硬编码密钥、密码
- [ ] 敏感数据加密存储
- [ ] 日志不包含敏感信息
- [ ] API 密钥使用环境变量

### 权限控制
- [ ] 验证用户权限
- [ ] 最小权限原则
- [ ] 防止越权访问

## 测试

### 测试覆盖
- [ ] 核心逻辑有单元测试
- [ ] 边界条件有测试
- [ ] 错误场景有测试
- [ ] 测试命名清晰

```typescript
describe('calculateDiscount', () => {
  it('should return 10% discount for orders over $100', () => {
    expect(calculateDiscount(150)).toBe(15);
  });

  it('should return 0 for orders under $100', () => {
    expect(calculateDiscount(50)).toBe(0);
  });

  it('should handle zero amount', () => {
    expect(calculateDiscount(0)).toBe(0);
  });
});
```

### 可测试性
- [ ] 函数职责单一
- [ ] 避免全局状态
- [ ] 依赖可注入
- [ ] 避免副作用

## 架构和设计

### SOLID 原则
- [ ] 单一职责原则（SRP）
- [ ] 开闭原则（OCP）
- [ ] 里氏替换原则（LSP）
- [ ] 接口隔离原则（ISP）
- [ ] 依赖倒置原则（DIP）

### 代码组织
- [ ] 文件和目录结构清晰
- [ ] 模块职责明确
- [ ] 依赖关系合理
- [ ] 避免循环依赖

## TypeScript 特定

### 类型安全
- [ ] 避免使用 any
- [ ] 类型定义完整
- [ ] 使用严格模式
- [ ] 泛型使用恰当

```typescript
// ❌ 不好
function process(data: any) {
  return data.value;
}

// ✅ 好
interface Data {
  value: string;
}

function process(data: Data): string {
  return data.value;
}
```

## React 特定

### Hooks 使用
- [ ] 遵循 Hooks 规则
- [ ] 依赖数组正确
- [ ] 避免过度使用 useEffect
- [ ] 自定义 Hooks 复用逻辑

### 组件设计
- [ ] Props 类型定义清晰
- [ ] 避免 props drilling
- [ ] 状态管理合理
- [ ] 性能优化适当

## 文档

### 代码注释
- [ ] 复杂逻辑有注释
- [ ] 公共 API 有 JSDoc
- [ ] TODO/FIXME 有说明
- [ ] 注释与代码同步

```typescript
/**
 * 计算订单折扣
 * @param amount - 订单金额
 * @param userLevel - 用户等级 (1-5)
 * @returns 折扣金额
 */
function calculateDiscount(amount: number, userLevel: number): number {
  // 实现逻辑
}
```

### README 和文档
- [ ] 安装说明清晰
- [ ] 使用示例完整
- [ ] API 文档准确
- [ ] 更新日志维护

## Git 和版本控制

### 提交
- [ ] 提交信息清晰
- [ ] 每个提交是独立的功能
- [ ] 避免提交调试代码
- [ ] 避免提交敏感信息

### 分支
- [ ] 分支命名规范
- [ ] 及时合并主分支
- [ ] 解决冲突正确

## 审查流程

1. **快速浏览**：了解改动的整体目的
2. **详细审查**：逐行检查代码
3. **运行测试**：确保测试通过
4. **本地测试**：必要时本地运行
5. **提供反馈**：建设性的意见
6. **跟进修改**：确认问题已解决

## 反馈原则

- 具体明确，指出具体问题
- 提供改进建议，不只是批评
- 区分必须修改和建议优化
- 保持友好和专业
- 认可好的代码

```markdown
<!-- ❌ 不好的反馈 -->
这段代码不好

<!-- ✅ 好的反馈 -->
这个函数有 80 行，建议拆分成更小的函数以提高可读性。
可以将验证逻辑提取到 validateInput() 函数中。
```
