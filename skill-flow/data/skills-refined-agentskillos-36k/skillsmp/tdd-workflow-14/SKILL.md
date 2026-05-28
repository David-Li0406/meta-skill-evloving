---
name: tdd-workflow
description: 测试驱动开发流程（TDD），包含红-绿-重构循环和测试最佳实践。
当编写新功能、重构代码、需要测试覆盖时使用。
Use when doing test-driven development, refactoring, or writing tests.
allowed-tools: "Bash,Read,Write,Edit,Grep"
---

# TDD Workflow - 测试驱动开发

测试驱动开发流程，通过红-绿-重构循环确保代码质量和可维护性。

## 核心循环：红-绿-重构

```
┌─────────┐    ┌─────────┐    ┌─────────┐
│   红    │ -> │   绿    │ -> │  重构   │
│ 写失败测试│    │ 让测试通过│   │ 优化代码 │
└─────────┘    └─────────┘    └─────────┘
     │                              │
     └──────────────┬───────────────┘
                    │
                    ▼
              重复循环
```

### 第一步：红（写失败的测试）

- 先写测试，测试**必须失败**
- 测试描述你想要的**行为**，而非实现
- 确保测试失败原因正确（非语法错误）

```bash
# ❌ 错误：先写代码
function add(a, b) { return a + b; }
test('add works', () => {});  // 没有断言

# ✅ 正确：先写测试
test('add returns sum of two numbers', () => {
  expect(add(2, 3)).toBe(5);
});
// 运行：测试失败（add 不存在）
```

### 第二步：绿（让测试通过）

- 写**最少**代码让测试通过
- 不要写超出测试范围的代码
- **允许丑陋代码**，通过即可

```javascript
// 最快让测试通过（即使丑陋）
function add(a, b) {
  return 5;  // 硬编码，但测试通过
}
```

### 第三步：重构（优化代码）

- 测试通过后，优化实现
- **保持测试绿色**
- 提取函数、消除重复、改善命名

```javascript
// 重构为正确实现
function add(a, b) {
  return a + b;
}
// 测试仍然通过 ✅
```

---

## 测试编写原则

### 1. 一个测试只验证一件事

```javascript
// ❌ 错误：测试多个行为
test('user operations', () => {
  user.setName('Alice');
  expect(user.name).toBe('Alice');
  user.save();
  expect(user.id).toBeDefined();
});

// ✅ 正确：分离测试
test('setName updates name', () => {
  user.setName('Alice');
  expect(user.name).toBe('Alice');
});

test('save assigns id', () => {
  user.save();
  expect(user.id).toBeDefined();
});
```

### 2. 测试行为，非实现

```javascript
// ❌ 错误：测试内部实现
test('uses cache', () => {
  expect(user.cache.get).toHaveBeenCalled();
});

// ✅ 正确：测试 observable 行为
test('returns cached data without fetch', () => {
  const first = user.getData();
  const second = user.getData();
  expect(second).toEqual(first);
  expect(fetch).not.toHaveBeenCalled();
});
```

### 3. 使用 Given-When-Then 结构

```javascript
test('user can withdraw funds', () => {
  // Given: 账户有 100 元
  account.balance = 100;

  // When: 取出 30 元
  account.withdraw(30);

  // Then: 余额为 70 元
  expect(account.balance).toBe(70);
});
```

---

## 重构安全网

### 重构前检查清单

- [ ] 所有测试通过
- [ ] 当前测试覆盖率足够
- [ ] 重构目标明确

### 重构中规则

1. **小步重构**：一次只改一处
2. **频繁运行测试**：每次修改后立即测试
3. **测试失败时停止**：不要在红灯时继续改代码

```bash
# 安全重构流程
npm test                    # 1. 确认绿灯
# 进行小改动
npm test                    # 2. 再次确认
# 继续或回滚
```

### 与 batch-file-ops 配合

批量重构时**必须**配合 TDD：

```
1. 先写测试保护现有行为
2. 用 batch-file-ops 执行重构
3. 测试验证重构正确性
4. 删除测试（如需要）或保留
```

---

## 常见触发场景

使用此技能时，你会听到：
- "为这个函数写测试"
- "TDD 实现..."
- "先写测试再写代码"
- "重构需要测试保护"
- "Write tests for..."
- "Refactor with tests"
- "TDD this feature"

---

## 测试命令参考

```bash
# Node.js (Jest/Vitest)
npm test
npm test -- --watch

# Python (pytest)
pytest
pytest -v

# Go
go test ./...
go test -v ./...
```
