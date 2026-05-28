---
name: java-specific
version: 1.0.0
description: Java语言特有审查规则（JVM优化、Spring最佳实践、Java安全）
language: java
tags: [java, jvm, spring, maven]
frameworks: [spring, spring-boot, maven, gradle]
---

# Java特有审查规则

## JVM性能优化
- **内存管理**: 检查不必要的对象创建、自动装箱拆箱、StringBuilder使用
- **GC调优**: 避免内存泄漏、检查ThreadLocal清理、finalize方法使用
- **并发模型**: 正确使用线程池、避免synchronized过度使用、检查volatile使用

## Spring最佳实践
- **依赖注入**: 避免字段注入、推荐使用构造器注入、检查循环依赖
- **事务管理**: 事务边界是否合理、避免长事务、检查事务传播行为
- **REST设计**: HTTP方法使用正确、状态码选择、异常处理统一

## Java安全检查
- **反序列化**: 禁止反序列化不可信数据、使用ObjectInputFilter
- **JNDI注入**: 检查InitialContext使用、避免JNDI查找用户输入
- **XXE防护**: XML解析器禁用外部实体、使用安全的XML解析器

## Maven/Gradle检查
- **依赖管理**: 检查版本冲突、排除无用依赖、使用BOM管理版本
- **构建优化**: 检查重复依赖、优化构建缓存、使用并行构建

## 代码示例

### 正面示例 - Spring依赖注入
```java
@Service
public class UserService {
    private final UserRepository userRepository;
    private final EmailService emailService;
    
    // 推荐：构造器注入
    public UserService(UserRepository userRepository, EmailService emailService) {
        this.userRepository = userRepository;
        this.emailService = emailService;
    }
}
```

### 反面示例 - 字段注入
```java
@Service
public class UserService {
    @Autowired  // 不推荐：字段注入
    private UserRepository userRepository;
}
```

### 正面示例 - 事务管理
```java
@Transactional(propagation = Propagation.REQUIRED, isolation = Isolation.READ_COMMITTED)
public void transferMoney(Long fromAccount, Long toAccount, BigDecimal amount) {
    // 合理的事务边界
}
```

### 反面示例 - 长事务
```java
@Transactional
public void processLargeBatch() {
    // 避免：处理大量数据的长事务
    for (int i = 0; i < 10000; i++) {
        // 长时间处理
    }
}
