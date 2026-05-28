# 测试验证检查清单

> 本文档提供测试验证阶段的详细指导，包括测试层次、失败处理和质量门标准。

---

## 测试层次（按优先级）

### P0: 必须通过的测试

#### 1. 编译检查

**Java/Maven**:
```bash
mvn clean compile
```

**Python**:
```bash
python -m py_compile src/**/*.py
# 或使用 mypy 做类型检查
mypy src/
```

**Node.js/TypeScript**:
```bash
npm run build
# 或
tsc --noEmit
```

**验收标准**: 0 errors

---

#### 2. 单元测试

**Java/Maven**:
```bash
# 运行所有测试
mvn test

# 运行特定测试类
mvn test -Dtest=UserControllerTest

# 运行特定测试方法
mvn test -Dtest=UserControllerTest#testValidateEmail
```

**Python**:
```bash
# 使用 pytest
pytest tests/

# 运行特定测试
pytest tests/test_user_controller.py::test_validate_email

# 显示详细输出
pytest -v tests/
```

**Node.js**:
```bash
# 使用 Jest
npm test

# 运行特定测试
npm test -- UserController.test.ts

# 监听模式
npm test -- --watch
```

**验收标准**: 100% 测试通过

---

### P1: 推荐通过的检查

#### 3. 代码风格检查

**Java**:
```bash
# Checkstyle
mvn checkstyle:check

# SpotBugs
mvn spotbugs:check

# PMD
mvn pmd:check
```

**Python**:
```bash
# Flake8（风格+语法）
flake8 src/

# Black（格式化检查）
black --check src/

# pylint（代码质量）
pylint src/
```

**JavaScript/TypeScript**:
```bash
# ESLint
npm run lint

# Prettier
npm run format:check
```

**验收标准**: 0 warnings（或遵循项目配置）

---

#### 4. 测试覆盖率

**Java**:
```bash
mvn test jacoco:report

# 查看报告
open target/site/jacoco/index.html
```

**Python**:
```bash
pytest --cov=src --cov-report=html tests/

# 查看报告
open htmlcov/index.html
```

**Node.js**:
```bash
npm test -- --coverage

# 查看报告
open coverage/lcov-report/index.html
```

**验收标准**: 
- 新增代码覆盖率 ≥80%
- 整体覆盖率不下降

---

### P2: 可选的深度检查

#### 5. 集成测试

```bash
# Java
mvn verify

# Python
pytest tests/integration/

# Node.js
npm run test:integration
```

#### 6. 安全扫描

```bash
# Java - OWASP Dependency Check
mvn dependency-check:check

# Node.js - npm audit
npm audit

# Python - Safety
safety check
```

---

## 测试失败处理流程

### 第1次失败: 自动分析修复

```
测试失败
    ↓
🔍 分析失败原因
    ├─ 语法错误 → 查看编译错误信息
    ├─ 断言失败 → 查看期望值 vs 实际值
    ├─ 异常抛出 → 查看堆栈跟踪
    └─ 超时 → 检查死循环或性能问题
    ↓
📝 定位问题代码行
    ↓
🔧 生成修复方案
    ↓
💻 应用修复
    ↓
🔄 重新运行测试
```

### 第2次失败: 深度分析

```
测试再次失败
    ↓
🤔 反思修复方案
    ├─ 修复方向是否正确？
    ├─ 是否引入了新问题？
    └─ 是否需要调整测试用例？
    ↓
🔧 生成新的修复方案（或更新测试）
    ↓
🔄 重新运行测试
```

### 第3次失败: 人工介入

```
测试第3次失败
    ↓
⚠️ 标记为"需要人工介入"
    ↓
📊 生成失败分析报告
    ↓
👤 通知用户
```

---

## 常见失败场景处理

### 场景1: 编译错误

**错误示例**:
```
[ERROR] /src/main/java/UserController.java:[45,20] 
cannot find symbol
  symbol:   variable emial
  location: class UserController
```

**分析**: 变量名拼写错误

**修复**: 
```java
// 修复前
return emial.matches(regex);

// 修复后
return email.matches(regex);
```

---

### 场景2: 断言失败

**错误示例**:
```
testValidateEmail_WithPlusSign()
Expected :true
Actual   :false
```

**分析**: 正则表达式未生效

**修复**:
```java
// 检查正则是否包含 +
String regex = "^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$";
//                         ↑ 确保包含 +
```

---

### 场景3: 异常抛出

**错误示例**:
```
java.lang.NullPointerException
    at ProductService.getPrice(ProductService.java:23)
```

**分析**: 未做 null 检查

**修复**:
```java
// 修复前
public double getPrice(Long id) {
    Product product = productRepository.findById(id).get();  // NPE
    return product.getPrice();
}

// 修复后
public double getPrice(Long id) {
    Product product = productRepository.findById(id)
            .orElseThrow(() -> new ProductNotFoundException(id));
    return product.getPrice();
}
```

---

### 场景4: 测试超时

**错误示例**:
```
Test timeout after 5000ms
```

**可能原因**:
1. 死循环
2. 数据库查询慢
3. 外部API调用超时

**分析**:
```java
// 检查是否有死循环
while (true) {  // ⚠️ 危险
    // ...
}

// 检查是否有阻塞调用
Thread.sleep(Long.MAX_VALUE);  // ⚠️ 危险
```

**修复**: 添加循环终止条件或超时控制

---

### 场景5: 测试数据问题

**错误示例**:
```
Expected: 9.95
Actual:   0.0
```

**分析**: Mock 数据未设置

**修复**:
```java
// 修复前
when(productRepository.findById(1L)).thenReturn(Optional.of(new Product()));

// 修复后
Product product = new Product();
product.setId(1L);
product.setPrice(9.95);  // 设置测试数据
when(productRepository.findById(1L)).thenReturn(Optional.of(product));
```

---

## 测试结果报告模板

### ✅ 测试通过报告

```markdown
✅ 测试验证通过

**编译检查**: ✅ 成功（0 errors）
**单元测试**: ✅ 通过 (15/15)
  - UserControllerTest.testValidateEmail: ✅
  - UserControllerTest.testValidateEmail_WithPlusSign: ✅ (新增)
  - UserControllerTest.testValidateEmail_Invalid: ✅
  - ...

**代码风格**: ✅ 通过 (0 warnings)
**测试覆盖率**: ✅ 82.3% (+2.1%)

**总耗时**: 8.3秒

**下一步**: 准备创建 Pull Request
```

---

### ❌ 测试失败报告

```markdown
❌ 测试验证失败（第1次尝试）

**失败测试**: 
- UserControllerTest.testValidateEmail_WithPlusSign

**失败原因**: 
断言失败 - Expected true but was false

**失败代码行**: 
UserController.java:45

**根因分析**:
正则表达式未包含 + 符号支持

**修复方案**:
将正则表达式从 `^[A-Za-z0-9]+@...` 
修改为 `^[A-Za-z0-9+_.-]+@...`

**状态**: 🔧 正在应用修复...
```

---

### ⚠️ 人工介入报告

```markdown
⚠️ 需要人工介入

**问题**: 测试失败3次，自动修复未成功

**失败测试**: UserControllerTest.testValidateEmail_WithPlusSign

**失败历史**:
1. 第1次: 正则表达式错误 → 已修复
2. 第2次: 测试数据错误 → 已修复  
3. 第3次: 仍然失败，原因不明

**当前代码**:
```java
public boolean validateEmail(String email) {
    String regex = "^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$";
    return email.matches(regex);
}
```

**测试代码**:
```java
@Test
public void testValidateEmail_WithPlusSign() {
    assertTrue(userController.validateEmail("user+tag@example.com"));
}
```

**建议**:
1. 手动调试测试用例
2. 检查是否有其他依赖或配置问题
3. 或更新 Issue 描述，提供更多上下文

**操作**: 
- 已暂停自动流程
- 已在 Issue 中添加评论说明情况
```

---

## 质量门标准

### 最低标准（P0）

- [ ] 编译通过（0 errors）
- [ ] 单元测试通过（100%）
- [ ] 核心功能测试覆盖

**不满足P0 → 不创建 PR**

---

### 推荐标准（P1）

- [ ] 代码风格检查通过
- [ ] 测试覆盖率 ≥80%
- [ ] 无 SonarQube 严重问题

**不满足P1 → PR 中标注 warning**

---

### 卓越标准（P2）

- [ ] 集成测试通过
- [ ] 性能测试无回退
- [ ] 安全扫描通过
- [ ] 文档完整

**满足P2 → PR 中标注 excellent**

---

## 测试命令速查表

### Java/Maven

| 任务 | 命令 |
|------|------|
| 编译 | `mvn compile` |
| 测试 | `mvn test` |
| 风格检查 | `mvn checkstyle:check` |
| 覆盖率 | `mvn test jacoco:report` |
| 集成测试 | `mvn verify` |
| 完整检查 | `mvn clean verify` |

### Python

| 任务 | 命令 |
|------|------|
| 语法检查 | `python -m py_compile src/**/*.py` |
| 测试 | `pytest tests/` |
| 风格检查 | `flake8 src/` |
| 覆盖率 | `pytest --cov=src tests/` |
| 类型检查 | `mypy src/` |

### Node.js

| 任务 | 命令 |
|------|------|
| 编译 | `npm run build` |
| 测试 | `npm test` |
| 风格检查 | `npm run lint` |
| 覆盖率 | `npm test -- --coverage` |
| 格式检查 | `npm run format:check` |

---

## 调试技巧

### 1. 查看详细测试输出

```bash
# Maven
mvn test -X

# pytest
pytest -vv tests/

# Jest
npm test -- --verbose
```

### 2. 运行单个测试

```bash
# Maven
mvn test -Dtest=ClassName#methodName

# pytest
pytest tests/test_file.py::test_function

# Jest
npm test -- --testNamePattern="test name"
```

### 3. 测试覆盖率热点

```bash
# 查看未覆盖的代码行
pytest --cov=src --cov-report=term-missing tests/
```

---

## 总结

**测试验证核心流程**:
1. ✅ P0 测试（编译 + 单元测试）
2. ⭐ P1 检查（风格 + 覆盖率）
3. 🔄 失败处理（最多3次自动修复）
4. 👤 人工介入（超过3次失败）

**质量门控制**:
- P0 不通过 → ❌ 不创建 PR
- P1 不通过 → ⚠️ PR 标注 warning
- P2 全通过 → ✅ PR 标注 excellent

**下一步**: 阅读 `pr-template.md` 了解 PR 创建流程。
