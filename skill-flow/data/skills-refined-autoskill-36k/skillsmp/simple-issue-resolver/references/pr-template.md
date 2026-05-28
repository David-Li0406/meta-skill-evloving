# PR 描述模板库

> 本文档提供不同类型 Issue 的 Pull Request 描述模板。

---

## 通用 PR 模板

```markdown
Fixes #{issue_number}

## 📋 变更说明

{从 Issue 中提取的核心需求，1-2句话概括}

## 🔧 实现细节

**修改文件**:
- `{文件路径1}`: {修改说明}
- `{文件路径2}`: {修改说明}

**代码行数**: +{added} -{deleted}

## ✅ 测试

- [x] 编译检查通过
- [x] 单元测试通过 ({passed}/{total})
- [x] 代码风格检查通过
- [x] {其他检查项}

**新增/修改测试用例**:
- `{测试方法名}`: {测试说明}

## 📝 相关 Issue

- Closes #{issue_number}

## 🤖 自动化说明

此 PR 由 `simple-issue-resolver` Skill 自动生成。
如有问题，请在评论中反馈。
```

---

## 模板1: Bug 修复类

```markdown
Fixes #{issue_number}

## 🐛 Bug 描述

{Bug 的现象和影响}

**复现步骤**:
1. {步骤1}
2. {步骤2}
3. {观察到的问题}

**预期行为**: {应该如何表现}

## 🔧 修复方案

**根因分析**:
{Bug 的根本原因，定位到具体代码行}

**修复方法**:
{采用的修复方案}

**修改文件**:
- `src/main/java/cn/com/itlead/controller/UserController.java`:
  - 第45行: 修正邮箱验证正则表达式，支持 + 符号
  - 添加参数 null 检查

## ✅ 验证

- [x] 原Bug场景已修复（手动验证）
- [x] 新增测试用例覆盖Bug场景
- [x] 回归测试通过（确保未引入新问题）
- [x] 边界条件测试通过

**测试用例**:
- `testValidateEmail_WithPlusSign()`: ✅ 验证支持 + 号邮箱
- `testValidateEmail_WithHyphen()`: ✅ 验证支持 - 号邮箱
- `testValidateEmail_StandardFormat()`: ✅ 回归测试标准格式

## 📸 修复前后对比

**修复前**:
```java
String regex = "^[A-Za-z0-9]+@[A-Za-z0-9]+\\.[A-Za-z]{2,}$";
```
❌ 无法匹配 "user+tag@example.com"

**修复后**:
```java
String regex = "^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$";
```
✅ 支持 RFC 5322 标准邮箱格式

## 📝 相关 Issue

- Closes #{issue_number}

## 🤖 自动化说明

此 PR 由 simple-issue-resolver 自动生成。
代码已通过自动化测试，但建议进行人工审查。
```

---

## 模板2: 新功能类

```markdown
Fixes #{issue_number}

## ✨ 功能说明

{新功能的用途和价值}

**用户故事**:
作为 {角色}，我希望 {功能}，以便 {目的}。

## 🔧 实现细节

**核心实现**:
{功能的主要实现逻辑}

**新增文件**:
- `{文件1}`: {说明}
- `{文件2}`: {说明}

**修改文件**:
- `{文件3}`: {修改说明}

**API 变更**（如有）:
- 新增接口: `GET /api/products?page={page}&size={size}`
- 请求参数: 
  - `page` (int, 可选): 页码，默认1
  - `size` (int, 可选): 每页大小，默认20
- 响应格式:
  ```json
  {
    "content": [...],
    "page": 1,
    "size": 20,
    "totalElements": 100,
    "totalPages": 5
  }
  ```

## ✅ 测试

- [x] 单元测试通过
- [x] 集成测试通过（如有）
- [x] 手动功能验证通过

**测试覆盖**:
- `testGetProductsWithPagination()`: ✅ 验证分页功能
- `testGetProductsDefaultPage()`: ✅ 验证默认参数
- `testGetProductsInvalidPage()`: ✅ 验证参数校验

## 📸 功能演示

**使用示例**:
```bash
# 请求第1页，每页20条
curl http://localhost:8080/api/products?page=1&size=20

# 响应
{
  "content": [...],
  "page": 1,
  "size": 20,
  "totalElements": 100
}
```

## 📝 相关 Issue

- Closes #{issue_number}

## 🚀 后续计划（可选）

- [ ] 添加排序功能
- [ ] 添加筛选功能
- [ ] 性能优化（缓存）

## 🤖 自动化说明

此 PR 由 simple-issue-resolver 自动生成。
```

---

## 模板3: 文档更新类

```markdown
Fixes #{issue_number}

## 📚 文档更新说明

{文档更新的目的}

## 📝 更新内容

**新增章节**:
- {章节名称}: {说明}

**修改章节**:
- {章节名称}: {修改说明}

**删除章节**:
- {章节名称}: {删除原因}

## ✅ 检查清单

- [x] 文档内容准确无误
- [x] 代码示例可运行
- [x] 链接有效
- [x] 格式统一（Markdown）
- [x] 无拼写错误

## 📸 更新前后对比

**更新前**:
```markdown
## 安装
```bash
mvn clean install
```
```

**更新后**:
```markdown
## 安装

**前置要求**:
- Java 11+
- Maven 3.6+

```bash
mvn clean install
```
```

## 📝 相关 Issue

- Closes #{issue_number}

## 🤖 自动化说明

此 PR 由 simple-issue-resolver 自动生成。
```

---

## 模板4: 配置修改类

```markdown
Fixes #{issue_number}

## ⚙️ 配置修改说明

{配置修改的目的和影响}

## 🔧 修改内容

**修改文件**: `{配置文件路径}`

**修改项**:
| 配置项 | 修改前 | 修改后 | 说明 |
|--------|--------|--------|------|
| `{配置键1}` | `{旧值}` | `{新值}` | {原因} |
| `{配置键2}` | `{旧值}` | `{新值}` | {原因} |

**影响范围**: {哪些功能受影响}

## ⚠️ 注意事项

- {注意事项1}
- {注意事项2}
- {是否需要重启服务}

## ✅ 验证

- [x] 配置格式正确（YAML/JSON/Properties）
- [x] 配置值合法
- [x] 应用程序启动成功
- [x] 相关功能正常工作

## 📝 相关 Issue

- Closes #{issue_number}

## 🤖 自动化说明

此 PR 由 simple-issue-resolver 自动生成。
```

---

## 模板5: 性能优化类

```markdown
Fixes #{issue_number}

## 🚀 性能优化说明

{性能问题描述和优化目标}

## 📊 性能对比

**优化前**:
- {指标1}: {数值}
- {指标2}: {数值}

**优化后**:
- {指标1}: {数值} ✅ 提升 {百分比}
- {指标2}: {数值} ✅ 提升 {百分比}

**测试环境**: {环境说明}

## 🔧 优化方案

**问题分析**:
{性能瓶颈分析}

**优化措施**:
1. {措施1}: {具体实现}
2. {措施2}: {具体实现}

**修改文件**:
- `{文件}`: {修改说明}

## ✅ 验证

- [x] 功能测试通过（确保优化未破坏功能）
- [x] 性能测试通过（达到预期指标）
- [x] 压力测试通过（稳定性验证）
- [x] 代码审查通过

## 📝 相关 Issue

- Closes #{issue_number}

## ⚠️ 风险评估

- {潜在风险1}
- {潜在风险2}
- {建议的灰度发布策略}

## 🤖 自动化说明

此 PR 由 simple-issue-resolver 自动生成。
建议进行详细的性能测试和代码审查。
```

---

## 模板6: 重构类

```markdown
Fixes #{issue_number}

## 🔨 重构说明

{重构的目的和动机}

## 📋 重构内容

**重构范围**: {哪些模块/类/方法}

**重构类型**:
- [ ] 提取方法
- [ ] 重命名
- [ ] 移动类/方法
- [ ] 简化条件表达式
- [ ] 其他: {说明}

**修改文件**:
- `{文件1}`: {重构说明}
- `{文件2}`: {重构说明}

## ✅ 质量保障

- [x] 所有测试通过（100%）
- [x] 功能行为无变化
- [x] 代码复杂度降低
- [x] 可读性提升
- [x] 无性能回退

**测试覆盖**: {覆盖率}

## 📸 重构前后对比

**重构前**:
```java
// 复杂的方法，70行代码
public void processOrder(Order order) {
    // ... 70行代码 ...
}
```

**重构后**:
```java
// 拆分为3个小方法
public void processOrder(Order order) {
    validateOrder(order);
    calculatePrice(order);
    saveOrder(order);
}

private void validateOrder(Order order) { ... }
private void calculatePrice(Order order) { ... }
private void saveOrder(Order order) { ... }
```

## 📝 相关 Issue

- Closes #{issue_number}

## 🤖 自动化说明

此 PR 由 simple-issue-resolver 自动生成。
建议重点审查业务逻辑是否保持一致。
```

---

## PR标题命名规范

### 格式

```
<type>: <简短描述> (fixes #<issue_number>)
```

### Type 类型

| Type | 说明 | 示例 |
|------|------|------|
| `fix` | Bug 修复 | `fix: 修复邮箱验证正则表达式 (fixes #123)` |
| `feat` | 新功能 | `feat: 添加产品列表分页功能 (fixes #456)` |
| `docs` | 文档更新 | `docs: 更新 README 安装说明 (fixes #789)` |
| `style` | 代码格式 | `style: 格式化代码缩进 (fixes #101)` |
| `refactor` | 代码重构 | `refactor: 简化订单处理逻辑 (fixes #202)` |
| `perf` | 性能优化 | `perf: 优化产品查询性能 (fixes #303)` |
| `test` | 测试相关 | `test: 添加用户服务测试用例 (fixes #404)` |
| `build` | 构建相关 | `build: 升级 Maven 依赖 (fixes #505)` |
| `ci` | CI/CD | `ci: 添加自动化测试流程 (fixes #606)` |
| `chore` | 杂项 | `chore: 更新 .gitignore (fixes #707)` |

---

## PR描述检查清单

提交 PR 前确认：

- [ ] 标题遵循命名规范
- [ ] 清晰说明变更内容
- [ ] 列出所有修改的文件
- [ ] 说明测试情况
- [ ] 关联相关 Issue
- [ ] 标注自动化生成
- [ ] 无敏感信息（密码、密钥）
- [ ] 格式正确（Markdown）

---

## 总结

**选择合适的模板**:
1. Bug 修复 → 模板1
2. 新功能 → 模板2
3. 文档更新 → 模板3
4. 配置修改 → 模板4
5. 性能优化 → 模板5
6. 代码重构 → 模板6

**PR 描述核心要素**:
- 📋 变更说明（What）
- 🔧 实现细节（How）
- ✅ 测试验证（Verify）
- 📝 关联 Issue（Link）

**下一步**: PR 创建后，等待 CI/CD 和人工审查。
