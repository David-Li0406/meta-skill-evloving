---
name: devdocs-bugfix
description: Test-first bug fixing workflow. Guide users through reproducing bugs, writing failing tests, fixing code, and committing. Use when users report bugs, need to fix issues, or mention keywords like "bug", "fix", "issue", "崩溃", "报错", "修复".
allowed-tools: Read, Write, Glob, Grep, Edit, Bash, AskUserQuestion
---

# Bug 修复

测试先行的 Bug 修复流程，确保每个修复都有回归测试保护。

## 语言规则

- 支持中英文提问
- 统一中文回复

## 触发条件

- 用户报告 Bug 或问题
- 用户提到"修复"、"bug"、"issue"、"崩溃"、"报错"
- 用户提供 Issue 编号或链接

## 核心理念

```
先证明 Bug 存在（失败测试），再修复代码，最后证明 Bug 已修复（测试通过）。
```

## 工作流程

```
1. 理解 Bug
   │
   ▼
2. 定位代码
   │
   ▼
3. 编写失败测试（证明 Bug 存在）
   │
   ├── 测试通过 → ⚠️ Bug 未复现，重新确认
   └── 测试失败 → ✅ 继续
   │
   ▼
4. 修复代码
   │
   ▼
5. 运行测试
   │
   ├── 测试失败 → 返回步骤 4
   └── 测试通过 → ✅ 继续
   │
   ▼
6. 询问用户：是否提交？
   │
   └── 生成 fix() 提交信息
```

## Step 1: 理解 Bug

收集 Bug 信息：

| 信息 | 来源 | 必要性 |
|------|------|--------|
| Bug 描述 | 用户输入 | 必须 |
| 复现步骤 | 用户输入 | 建议 |
| 预期行为 | 用户输入 | 建议 |
| 实际行为 | 用户输入 | 必须 |
| Issue 编号 | 用户输入 | 可选 |

如信息不足，使用 AskUserQuestion 询问。

## Step 2: 定位代码

搜索策略：

1. **关键词搜索**：根据 Bug 描述搜索相关代码
2. **错误信息搜索**：搜索报错信息中的关键字
3. **用户指定**：用户直接提供文件路径

```bash
# 搜索示例
grep -r "login" src/
grep -r "ErrorMessage" src/
```

向用户确认定位结果：

```markdown
找到以下相关代码：

1. `src/services/auth.ts:45` - login() 函数
2. `src/controllers/user.ts:23` - handleLogin()

请确认 Bug 位置，或提供更多信息。
```

## Step 3: 编写失败测试

### 测试命名规范

```
should [预期行为] when [触发条件]
```

**示例**：
- `should return error when username is empty`
- `should not crash when input contains special characters`
- `should handle null response from API`

### 测试结构

```typescript
describe('Bug fix: <Bug 描述>', () => {
  it('should <预期行为> when <条件>', () => {
    // Arrange - 构造触发 Bug 的条件
    const input = '';

    // Act & Assert - 验证预期行为
    expect(() => login(input, 'password')).toThrow('Username required');
  });
});
```

### 验证测试有效性

运行测试，确认测试失败：

```bash
npm test -- --testNamePattern="Bug fix"
```

- **测试失败** ✅ → Bug 已复现，继续修复
- **测试通过** ⚠️ → Bug 未复现，需重新确认：
  - 复现条件是否正确？
  - 测试用例是否准确描述了 Bug？

## Step 4: 修复代码

### 修复原则

- [ ] **最小改动**：只修改必要的代码
- [ ] **不引入新功能**：修复 Bug，不顺便重构
- [ ] **遵循现有风格**：与周围代码保持一致

### 修复约束

参考 `/code-quality` 约束：
- 函数不超过 50 行
- 参数不超过 5 个
- 依赖可注入

## Step 5: 运行测试

```bash
# 运行新增的 Bug 修复测试
npm test -- --testNamePattern="Bug fix"

# 运行全部测试，确保没有引入回归
npm test
```

- **新测试通过 + 全部测试通过** ✅ → 修复完成
- **新测试失败** → 返回步骤 4 继续修复
- **其他测试失败** → 检查是否引入回归

## Step 6: 提交

### 提交前检查

- [ ] 新增的测试通过
- [ ] 全部测试通过
- [ ] 代码符合规范

### 提交信息格式

遵循 `/commit-convention`：

```
fix(<scope>): <简述问题>

- 根因：<问题原因>
- 修复：<解决方案>

Fixes #<issue-number>
```

**示例**：

```
fix(auth): handle empty username in login

- 根因：login() 未校验空用户名，直接查询数据库导致异常
- 修复：添加用户名非空校验，返回明确错误信息

Fixes #123
```

## Skill 协作

| 场景 | 协作 Skill |
|------|-----------|
| 测试编写 | `/testing-guide` |
| 代码修改 | `/code-quality` |
| 文件操作 | `/git-safety` |
| 提交信息 | `/commit-convention` |

## 约束

### 流程约束

- [ ] **必须先编写失败测试，再修复代码**
- [ ] **测试必须先失败，证明 Bug 存在**
- [ ] **修复后测试必须通过**
- [ ] **不得跳过测试直接提交**

### 测试约束

- [ ] 测试名称描述 Bug 场景
- [ ] 测试覆盖 Bug 的触发条件
- [ ] 禁止弱断言（参考 `/testing-guide`）

### 提交约束

- [ ] 提交信息使用 `fix(<scope>):` 前缀
- [ ] 说明根因和修复方案
- [ ] 关联 Issue 编号（如有）

## 特殊情况

### Bug 无法复现

```
⚠️ 测试通过，Bug 未能复现。

可能原因：
1. 复现条件不完整
2. Bug 已在其他提交中修复
3. 环境差异导致无法复现

建议：
- 确认复现步骤是否完整
- 检查最近的相关提交
- 与报告者确认环境信息
```

### Bug 涉及多个模块

如 Bug 涉及多个模块，建议拆分为多个小修复：

```
1. 识别各模块的问题
2. 按模块分别修复
3. 每个模块单独提交
4. 最后集成测试
```

### Bug 暴露设计缺陷

如 Bug 暴露了设计问题：

```
1. 先用最小改动修复当前 Bug
2. 提交修复
3. 创建重构任务（可选）
4. 使用 /refactor 进行系统性改进
```

## 输出

此 Skill 不生成独立文档，只输出：
- 测试代码（新增的回归测试）
- Git commit
