# 代码实现详细指引

> 本文档提供代码实现阶段的详细指导，包括编码规范、常见模式和最佳实践。

---

## 实施策略

### 1. 定位目标文件

#### 方法1: Issue 中的明确路径

```markdown
示例 Issue:
"修改 src/main/java/cn/com/itlead/controller/UserController.java 
中的 validateEmail 方法"

→ 直接定位文件
```

#### 方法2: 关键词搜索

```bash
# 搜索方法名
grep -r "validateEmail" src/

# 搜索类名
grep -r "class ProductController" src/

# 搜索注解
grep -r "@RestController" src/
```

#### 方法3: 语义搜索

使用 VS Code 的 `semantic_search` 工具:

```
搜索: email validation logic in user controller
```

---

## 编码规范

### Java/Spring Boot 项目

#### 修改前检查

```java
// 1. 检查类的完整结构
public class UserController {
    // 找到目标方法
    public boolean validateEmail(String email) {
        // 当前实现
    }
}

// 2. 查看相关依赖
import java.util.regex.Pattern;

// 3. 查看相关测试
@Test
public void testValidateEmail() { ... }
```

#### 修改原则

```java
// ❌ 不好的修改（改动过大）
public boolean validateEmail(String email) {
    // 完全重写整个方法，引入新的库
    return EmailValidator.getInstance().isValid(email);
}

// ✅ 好的修改（最小改动）
public boolean validateEmail(String email) {
    // Issue #123: 支持 RFC 5322 格式，允许 + 符号
    String regex = "^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$";
    return email.matches(regex);
}
```

#### 注释规范

```java
// ✅ 好的注释
// Issue #123: 支持 RFC 5322 邮箱格式，允许 + 符号
// 修改原因: 当前正则无法识别 "user+tag@example.com"

// ❌ 不好的注释
// 修改了正则表达式
```

---

### Python 项目

#### 代码风格

```python
# ❌ 不符合 PEP 8
def validateEmail(email):
    regex="^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$"
    return bool(re.match(regex,email))

# ✅ 符合 PEP 8
def validate_email(email: str) -> bool:
    """
    验证邮箱格式（支持 RFC 5322）
    
    Args:
        email: 待验证的邮箱地址
        
    Returns:
        bool: 邮箱格式是否有效
        
    Issue: #123
    """
    regex = r"^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return bool(re.match(regex, email))
```

---

### JavaScript/TypeScript 项目

#### TypeScript 类型安全

```typescript
// ❌ 类型不明确
function validateEmail(email) {
    const regex = /^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
    return regex.test(email);
}

// ✅ 类型明确
/**
 * 验证邮箱格式（支持 RFC 5322）
 * @param email - 待验证的邮箱地址
 * @returns 邮箱格式是否有效
 * @issue #123
 */
function validateEmail(email: string): boolean {
    const regex = /^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
    return regex.test(email);
}
```

---

## 常见模式

### 模式1: 修改业务逻辑

**场景**: Bug 修复、逻辑优化

```java
// 示例: 修复价格计算精度问题
// 修改前
public double calculatePrice(double price, double discount) {
    return price * discount;
}

// 修改后
public double calculatePrice(double price, double discount) {
    // Issue #456: 价格保留2位小数，避免精度问题
    BigDecimal priceDecimal = new BigDecimal(String.valueOf(price));
    BigDecimal discountDecimal = new BigDecimal(String.valueOf(discount));
    return priceDecimal.multiply(discountDecimal)
                       .setScale(2, RoundingMode.HALF_UP)
                       .doubleValue();
}
```

### 模式2: 添加参数验证

```java
// 示例: 为方法添加参数校验
// 修改前
public Product getProductById(Long id) {
    return productRepository.findById(id).orElse(null);
}

// 修改后
public Product getProductById(Long id) {
    // Issue #789: 添加参数验证
    if (id == null || id <= 0) {
        throw new IllegalArgumentException("产品ID必须为正数");
    }
    return productRepository.findById(id)
            .orElseThrow(() -> new ProductNotFoundException("产品不存在: " + id));
}
```

### 模式3: 添加配置项

```yaml
# 示例: 添加新的配置项
# application.yml 修改前
server:
  port: 8080

# 修改后（Issue #101: 添加最大上传文件大小配置）
server:
  port: 8080
spring:
  servlet:
    multipart:
      max-file-size: 10MB  # Issue #101
      max-request-size: 10MB
```

### 模式4: 更新文档

```markdown
<!-- README.md 修改前 -->
## 安装
```bash
mvn clean install
```

<!-- 修改后（Issue #202: 补充 Java 版本要求） -->
## 安装

**前置要求**:
- Java 11 或更高版本  <!-- Issue #202 -->
- Maven 3.6+

```bash
mvn clean install
```
```

---

## 测试用例同步更新

### 原则: 代码改动必须有测试覆盖

```java
// 代码修改
public boolean validateEmail(String email) {
    // 支持 + 符号
    String regex = "^[A-Za-z0-9+_.-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$";
    return email.matches(regex);
}

// 必须新增测试
@Test
public void testValidateEmail_WithPlusSign() {
    // Given
    String email = "user+tag@example.com";
    
    // When
    boolean result = userController.validateEmail(email);
    
    // Then
    assertTrue(result, "应该支持带 + 号的邮箱格式");
}

@Test
public void testValidateEmail_WithHyphen() {
    // 同时测试其他特殊字符
    assertTrue(userController.validateEmail("user-name@example.com"));
}
```

---

## 错误处理

### 添加异常处理

```java
// ❌ 不好的实现（吞掉异常）
public Product getProduct(Long id) {
    try {
        return productRepository.findById(id).get();
    } catch (Exception e) {
        return null;
    }
}

// ✅ 好的实现（明确异常类型）
public Product getProduct(Long id) {
    return productRepository.findById(id)
            .orElseThrow(() -> new ProductNotFoundException(
                "产品不存在: " + id
            ));
}
```

---

## 性能考虑

### 避免性能回退

```java
// ❌ 不好的实现（N+1 查询）
public List<OrderDTO> getOrders() {
    List<Order> orders = orderRepository.findAll();
    return orders.stream()
            .map(order -> {
                User user = userRepository.findById(order.getUserId()).get();
                return new OrderDTO(order, user);
            })
            .collect(Collectors.toList());
}

// ✅ 好的实现（批量查询）
public List<OrderDTO> getOrders() {
    List<Order> orders = orderRepository.findAll();
    Set<Long> userIds = orders.stream()
            .map(Order::getUserId)
            .collect(Collectors.toSet());
    Map<Long, User> users = userRepository.findAllById(userIds)
            .stream()
            .collect(Collectors.toMap(User::getId, u -> u));
    return orders.stream()
            .map(order -> new OrderDTO(order, users.get(order.getUserId())))
            .collect(Collectors.toList());
}
```

---

## 代码审查自检清单

### 提交前必查

- [ ] 代码通过编译（无语法错误）
- [ ] 修改符合 Issue 描述
- [ ] 保持原有代码风格（缩进、命名）
- [ ] 添加/更新了测试用例
- [ ] 添加了必要注释（说明修改原因）
- [ ] 没有引入新的警告
- [ ] 没有注释掉的调试代码
- [ ] 没有 TODO/FIXME 标记（除非必要）

### 质量检查

- [ ] 边界条件处理（null、空字符串、负数等）
- [ ] 异常处理完善
- [ ] 日志记录合理
- [ ] 资源正确关闭（数据库连接、文件句柄）
- [ ] 线程安全（如果涉及并发）

---

## 工具使用

### VS Code 快捷操作

```
1. 格式化代码: Shift+Alt+F
2. 重命名符号: F2
3. 查找引用: Shift+F12
4. 跳转到定义: F12
5. 智能提示: Ctrl+Space
```

### Git 操作

```bash
# 查看修改
git diff

# 暂存文件
git add src/main/java/cn/com/itlead/controller/UserController.java

# 提交（关联 Issue）
git commit -m "fix: 修复邮箱验证正则表达式 (fixes #123)"

# 查看提交
git log --oneline -1
```

---

## 示例完整流程

### 场景: 修复价格显示精度问题

**Issue #456**: "产品价格显示不准确，9.95 显示为 9.949999"

#### 1. 定位文件

```bash
grep -r "getPrice" src/
# 找到: src/main/java/cn/com/itlead/service/ProductService.java
```

#### 2. 分析问题

```java
// 当前代码
public double getPrice(Long productId) {
    Product product = productRepository.findById(productId).get();
    return product.getPrice() * product.getDiscount();  // 精度丢失
}
```

#### 3. 实施修改

```java
import java.math.BigDecimal;
import java.math.RoundingMode;

public double getPrice(Long productId) {
    Product product = productRepository.findById(productId)
            .orElseThrow(() -> new ProductNotFoundException(productId));
    
    // Issue #456: 使用 BigDecimal 避免浮点精度问题
    BigDecimal price = new BigDecimal(String.valueOf(product.getPrice()));
    BigDecimal discount = new BigDecimal(String.valueOf(product.getDiscount()));
    
    return price.multiply(discount)
                .setScale(2, RoundingMode.HALF_UP)  // 保留2位小数
                .doubleValue();
}
```

#### 4. 更新测试

```java
@Test
public void testGetPrice_Precision() {
    // Given
    Product product = new Product();
    product.setPrice(9.95);
    product.setDiscount(1.0);
    when(productRepository.findById(1L)).thenReturn(Optional.of(product));
    
    // When
    double price = productService.getPrice(1L);
    
    // Then
    assertEquals(9.95, price, 0.001, "价格应精确到2位小数");
}
```

#### 5. 运行测试

```bash
mvn test -Dtest=ProductServiceTest#testGetPrice_Precision
```

#### 6. 提交

```bash
git add src/main/java/cn/com/itlead/service/ProductService.java
git add src/test/java/cn/com/itlead/service/ProductServiceTest.java
git commit -m "fix: 修复产品价格浮点精度问题 (fixes #456)

- 使用 BigDecimal 替代 double 运算
- 价格保留2位小数，四舍五入
- 新增精度测试用例

Fixes #456"
```

---

## 总结

**关键原则**:
1. **最小修改**: 只改必要的代码
2. **测试驱动**: 先写/更新测试，再改代码
3. **保持风格**: 遵循项目规范
4. **清晰注释**: 说明修改原因（关联 Issue）
5. **完整提交**: 代码+测试+文档一起提交

**下一步**: 阅读 `testing-checklist.md` 了解测试验证流程。
