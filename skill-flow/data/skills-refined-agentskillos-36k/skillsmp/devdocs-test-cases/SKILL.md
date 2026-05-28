---
name: devdocs-test-cases
description: Design test cases based on requirements. Use when users need test case design, testing strategy, or QA planning. Triggers on keywords like "test cases", "test design", "unit test", "integration test", "e2e test".
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion
---

# 测试用例设计

基于需求文档设计测试用例，建立验收标准与测试用例的追溯关系。

## 语言规则

- 支持中英文提问
- 统一中文回复
- 使用中文生成文档

## 触发条件

- 用户已完成需求文档
- 用户要求设计测试用例
- 用户需要测试覆盖策略

## 前置条件

- 需求文档：`docs/devdocs/01-requirements.md`
- 如不存在，建议先运行 `/devdocs-requirements`

## 核心理念

### 测试用例来源

```
功能点 (F-XXX)
    │
    └── 用户故事 (US-XXX)
            │
            └── 验收标准 (AC-XXX)
                    │
                    ├── 单元测试 (UT-XXX)  ← 验证内部逻辑
                    │
                    ├── 集成测试 (IT-XXX)  ← 验证组件协作
                    │
                    └── E2E 测试 (E2E-XXX) ← 验证用户场景
```

**关键原则**：
- 测试用例从需求推导，不是从代码推导
- 每个验收标准至少有一个测试用例覆盖
- 测试类型根据验收标准的性质选择

### 测试类型选择

| 验收标准类型 | 推荐测试类型 | 示例 |
|--------------|--------------|------|
| 输入验证规则 | 单元测试 | "邮箱格式校验" → UT |
| 业务逻辑规则 | 单元测试 + 集成测试 | "密码加密存储" → UT + IT |
| 用户交互流程 | E2E 测试 | "完成注册流程" → E2E |
| 组件间协作 | 集成测试 | "发送验证邮件" → IT |

## 编号规范

| 类型 | 前缀 | 格式 | 示例 |
|------|------|------|------|
| 单元测试 | UT | UT-XXX | UT-001, UT-002 |
| 集成测试 | IT | IT-XXX | IT-001, IT-002 |
| E2E 测试 | E2E | E2E-XXX | E2E-001, E2E-002 |

## 工作流程

```
1. 读取需求文档
   │
   ▼
2. 提取功能点、用户故事、验收标准
   │
   ▼
3. 为每个验收标准选择测试类型
   │
   ▼
4. 设计单元测试用例 (UT-XXX)
   │
   ▼
5. 设计集成测试用例 (IT-XXX)
   │
   ▼
6. 设计 E2E 测试用例 (E2E-XXX)
   │
   ▼
7. 生成追溯矩阵
   │
   ▼
8. 用户确认
```

## 输出文件

**主文件**：`docs/devdocs/03-test-cases.md`

### 文档拆分规则

当满足以下条件时，应拆分文档：
- 测试用例总数超过 **30 个**
- 文档超过 **300 行**
- 单一测试类型用例超过 **15 个**

**拆分方式**：

```
docs/devdocs/
├── 03-test-cases.md           # 主文档：测试策略、覆盖率要求、追溯矩阵
├── 03-test-unit.md            # 单元测试用例（UT-XXX）
├── 03-test-integration.md     # 集成测试用例（IT-XXX）
└── 03-test-e2e.md             # E2E 测试用例（E2E-XXX）
```

**拆分内容分配**：

| 文件 | 包含内容 |
|------|----------|
| 03-test-cases.md | 测试策略、覆盖率要求、追溯矩阵、测试用例汇总 |
| 03-test-unit.md | 所有单元测试用例详情（UT-001 ~ UT-XXX） |
| 03-test-integration.md | 所有集成测试用例详情（IT-001 ~ IT-XXX） |
| 03-test-e2e.md | 所有 E2E 测试用例详情（E2E-001 ~ E2E-XXX） |

**主文档保留内容**：
- 测试策略说明
- 覆盖率目标
- 完整追溯矩阵（F → US → AC → 测试）
- 各子文档的用例范围说明

**小型项目**：如测试用例较少（< 30 个），可合并为单一文件 `03-test-cases.md`。

详细模板参见：
- [templates/test-cases-template.md](templates/test-cases-template.md)
- [templates/unit-test-template.md](templates/unit-test-template.md)
- [templates/integration-test-template.md](templates/integration-test-template.md)
- [templates/e2e-test-template.md](templates/e2e-test-template.md)

## 测试用例概览文档结构

```markdown
# 测试用例：<功能名称>

## 1. 测试策略
## 2. 覆盖率要求
## 3. 追溯矩阵
## 4. 测试用例汇总
```

## 追溯矩阵

追溯矩阵是核心产出，展示需求与测试的完整关联。

**格式**：
```markdown
| 功能点 | 用户故事 | 验收标准 | 单元测试 | 集成测试 | E2E测试 | 状态 |
|--------|----------|----------|----------|----------|---------|------|
| F-001 | US-001 | AC-001 | UT-001 | - | E2E-001 | ✅ |
| F-001 | US-001 | AC-002 | UT-002 | - | E2E-001 | ✅ |
| F-001 | US-002 | AC-004 | UT-003, UT-004 | IT-001 | - | ✅ |
```

**状态说明**：
- ✅ 完整覆盖：有对应测试用例
- ⚠️ 部分覆盖：测试用例不足
- ❌ 未覆盖：无测试用例

## 测试用例格式

### 单元测试用例

```markdown
| 编号 | 验收标准 | 测试对象 | 场景 | 输入 | 预期输出 | 优先级 |
|------|----------|----------|------|------|----------|--------|
| UT-001 | AC-001 | validateEmail() | 有效邮箱 | "test@example.com" | true | P0 |
| UT-002 | AC-002 | validateEmail() | 无效格式 | "invalid" | false | P0 |
```

### 集成测试用例

```markdown
| 编号 | 验收标准 | 测试场景 | 涉及组件 | 预期结果 | 优先级 |
|------|----------|----------|----------|----------|--------|
| IT-001 | AC-004 | 密码加密存储 | UserService + DB | 密码以 bcrypt 格式存储 | P0 |
```

### E2E 测试用例

```markdown
| 编号 | 用户故事 | 验收标准 | 操作步骤 | 预期结果 | 优先级 |
|------|----------|----------|----------|----------|--------|
| E2E-001 | US-001 | AC-001~AC-003 | 1. 打开注册页<br>2. 输入邮箱密码<br>3. 点击注册 | 注册成功，收到验证邮件 | P0 |
```

## 覆盖率要求

| 测试类型 | 覆盖目标 | 覆盖要求 |
|----------|----------|----------|
| 单元测试 | 核心业务逻辑 | 行覆盖率 ≥ 80%，分支覆盖率 ≥ 80% |
| 集成测试 | 组件协作场景 | 每个功能点至少 1 个 IT |
| E2E 测试 | 用户故事 | 每个 P0 用户故事至少 1 个 E2E |

## 约束

### 追溯约束
- [ ] 每个验收标准至少有 1 个测试用例覆盖
- [ ] 必须生成追溯矩阵
- [ ] 追溯矩阵必须覆盖所有 AC

### 用例设计约束
- [ ] 测试用例必须关联验收标准编号
- [ ] 每个用例必须有明确的预期结果
- [ ] 优先级必须标注 (P0/P1/P2)

### 覆盖约束
- [ ] P0 验收标准必须 100% 测试覆盖
- [ ] P0 用户故事必须有 E2E 测试
- [ ] 单元测试行覆盖率目标 ≥ 80%

### 质量约束（参考 `/testing-guide`）
- [ ] 测试名称必须描述预期行为
- [ ] 禁止弱断言（toBeDefined, toBeTruthy 不能作为唯一断言）
- [ ] Mock 只用于外部依赖

## 与其他 Skill 的关系

| Skill | 关系 |
|-------|------|
| `/devdocs-requirements` | 前置：提供 F/US/AC 作为测试设计依据 |
| `/testing-guide` | 协作：编写测试代码时的质量约束 |
| `/devdocs-dev-tasks` | 后续：测试用例转化为开发任务 |

## 下一步

完成后建议运行 `/devdocs-dev-tasks` 进行开发任务拆分。
