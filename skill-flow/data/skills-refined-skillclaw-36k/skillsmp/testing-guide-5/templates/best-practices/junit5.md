# JUnit 5 最佳实践

Java 测试框架 JUnit 5 的配置和最佳实践指南。

## 目录

- [项目配置](#项目配置)
- [测试结构](#测试结构)
- [断言最佳实践](#断言最佳实践)
- [参数化测试](#参数化测试)
- [Mock 策略](#mock-策略)
- [异步测试](#异步测试)
- [测试生命周期](#测试生命周期)
- [覆盖率配置](#覆盖率配置)

---

## 项目配置

### Maven 配置

```xml
<!-- pom.xml -->
<properties>
    <junit.version>5.10.1</junit.version>
    <mockito.version>5.8.0</mockito.version>
    <assertj.version>3.24.2</assertj.version>
</properties>

<dependencies>
    <!-- JUnit 5 -->
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>${junit.version}</version>
        <scope>test</scope>
    </dependency>

    <!-- AssertJ (推荐的断言库) -->
    <dependency>
        <groupId>org.assertj</groupId>
        <artifactId>assertj-core</artifactId>
        <version>${assertj.version}</version>
        <scope>test</scope>
    </dependency>

    <!-- Mockito -->
    <dependency>
        <groupId>org.mockito</groupId>
        <artifactId>mockito-core</artifactId>
        <version>${mockito.version}</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.mockito</groupId>
        <artifactId>mockito-junit-jupiter</artifactId>
        <version>${mockito.version}</version>
        <scope>test</scope>
    </dependency>
</dependencies>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.2.3</version>
        </plugin>
    </plugins>
</build>
```

### Gradle 配置

```kotlin
// build.gradle.kts
plugins {
    java
    jacoco
}

dependencies {
    testImplementation("org.junit.jupiter:junit-jupiter:5.10.1")
    testImplementation("org.assertj:assertj-core:3.24.2")
    testImplementation("org.mockito:mockito-core:5.8.0")
    testImplementation("org.mockito:mockito-junit-jupiter:5.8.0")
}

tasks.test {
    useJUnitPlatform()
    finalizedBy(tasks.jacocoTestReport)
}

tasks.jacocoTestReport {
    dependsOn(tasks.test)
    reports {
        xml.required.set(true)
        html.required.set(true)
    }
}

tasks.jacocoTestCoverageVerification {
    violationRules {
        rule {
            limit {
                minimum = "0.80".toBigDecimal()
            }
        }
    }
}
```

---

## 测试结构

### 基本结构

```java
import org.junit.jupiter.api.*;
import static org.assertj.core.api.Assertions.*;

@DisplayName("UserService 测试")
class UserServiceTest {

    private UserService userService;
    private UserRepository userRepository;

    @BeforeEach
    void setUp() {
        userRepository = new InMemoryUserRepository();
        userService = new UserService(userRepository);
    }

    @AfterEach
    void tearDown() {
        userRepository.clear();
    }

    @Nested
    @DisplayName("createUser 方法")
    class CreateUser {

        @Test
        @DisplayName("应该创建用户当输入有效时")
        void shouldCreateUserWhenInputIsValid() {
            // Arrange
            CreateUserRequest request = new CreateUserRequest("test@example.com", "Test User");

            // Act
            User result = userService.createUser(request);

            // Assert
            assertThat(result.getId()).isNotNull();
            assertThat(result.getEmail()).isEqualTo("test@example.com");
            assertThat(result.getName()).isEqualTo("Test User");
        }

        @Test
        @DisplayName("应该抛出异常当邮箱已存在时")
        void shouldThrowExceptionWhenEmailExists() {
            // Arrange
            userRepository.save(new User("existing@example.com", "Existing"));
            CreateUserRequest request = new CreateUserRequest("existing@example.com", "New User");

            // Act & Assert
            assertThatThrownBy(() -> userService.createUser(request))
                .isInstanceOf(DuplicateEmailException.class)
                .hasMessageContaining("existing@example.com");
        }
    }
}
```

### 测试命名规范

```java
// ❌ 不好的命名
@Test
void test1() {}

@Test
void testGetUser() {}

// ✅ 好的命名 - 使用 @DisplayName
@Test
@DisplayName("应该返回用户当用户存在时")
void shouldReturnUserWhenUserExists() {}

@Test
@DisplayName("应该抛出 NotFoundException 当用户不存在时")
void shouldThrowNotFoundExceptionWhenUserDoesNotExist() {}

// ✅ 好的命名 - 方法名描述行为
@Test
void getUser_shouldReturnUser_whenUserExists() {}

@Test
void getUser_shouldThrowNotFoundException_whenUserDoesNotExist() {}
```

---

## 断言最佳实践

### 使用 AssertJ (推荐)

```java
import static org.assertj.core.api.Assertions.*;

// ❌ JUnit 原生断言 - 功能有限
assertEquals("expected", actual);
assertTrue(condition);
assertNotNull(result);

// ✅ AssertJ - 流畅、可读、功能丰富
assertThat(actual).isEqualTo("expected");
assertThat(condition).isTrue();
assertThat(result).isNotNull();

// 字符串断言
assertThat(email)
    .isNotBlank()
    .contains("@")
    .endsWith(".com");

// 集合断言
assertThat(users)
    .hasSize(3)
    .extracting(User::getName)
    .containsExactly("Alice", "Bob", "Charlie");

// 对象断言
assertThat(user)
    .hasFieldOrPropertyWithValue("name", "Test")
    .hasFieldOrPropertyWithValue("email", "test@example.com");

// 异常断言
assertThatThrownBy(() -> userService.getUser(-1))
    .isInstanceOf(IllegalArgumentException.class)
    .hasMessage("ID must be positive");

assertThatCode(() -> userService.validateEmail("valid@example.com"))
    .doesNotThrowAnyException();
```

### 禁止弱断言

```java
// ❌ 弱断言 - 几乎不验证任何东西
assertThat(result).isNotNull();
assertThat(list).isNotEmpty();
assertThat(value).isInstanceOf(String.class);

// ✅ 强断言 - 验证具体值
assertThat(result.getStatus()).isEqualTo(Status.SUCCESS);
assertThat(list).hasSize(3).contains("item1", "item2");
assertThat(value).isEqualTo("expected string");
```

### 自定义断言

```java
// 创建自定义断言类
public class UserAssert extends AbstractAssert<UserAssert, User> {

    public UserAssert(User actual) {
        super(actual, UserAssert.class);
    }

    public static UserAssert assertThat(User actual) {
        return new UserAssert(actual);
    }

    public UserAssert hasEmail(String email) {
        isNotNull();
        if (!actual.getEmail().equals(email)) {
            failWithMessage("Expected email to be <%s> but was <%s>",
                email, actual.getEmail());
        }
        return this;
    }

    public UserAssert isActive() {
        isNotNull();
        if (!actual.isActive()) {
            failWithMessage("Expected user to be active");
        }
        return this;
    }
}

// 使用自定义断言
@Test
void shouldCreateActiveUser() {
    User user = userService.createUser(request);

    UserAssert.assertThat(user)
        .hasEmail("test@example.com")
        .isActive();
}
```

---

## 参数化测试

### 基本参数化

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.*;

@ParameterizedTest
@ValueSource(strings = {"", " ", "  ", "\t", "\n"})
@DisplayName("应该拒绝空白用户名")
void shouldRejectBlankUsername(String username) {
    assertThatThrownBy(() -> userService.validateUsername(username))
        .isInstanceOf(ValidationException.class);
}

@ParameterizedTest
@ValueSource(ints = {-1, 0, -100})
@DisplayName("应该拒绝非正数ID")
void shouldRejectNonPositiveId(int id) {
    assertThatThrownBy(() -> userService.getUser(id))
        .isInstanceOf(IllegalArgumentException.class);
}

@ParameterizedTest
@NullAndEmptySource
@ValueSource(strings = {" ", "\t"})
@DisplayName("应该拒绝无效邮箱")
void shouldRejectInvalidEmail(String email) {
    assertThat(validator.isValidEmail(email)).isFalse();
}
```

### CSV 参数源

```java
@ParameterizedTest
@CsvSource({
    "100, 0, 100",      // 无折扣
    "100, 10, 90",      // 10% 折扣
    "200, 25, 150",     // 25% 折扣
    "1000, 50, 500"     // 50% 折扣
})
@DisplayName("应该正确计算折扣")
void shouldCalculateDiscount(int price, int discountPercent, int expected) {
    int result = calculator.applyDiscount(price, discountPercent);
    assertThat(result).isEqualTo(expected);
}

@ParameterizedTest
@CsvFileSource(resources = "/test-data/discount-cases.csv", numLinesToSkip = 1)
@DisplayName("应该处理所有折扣场景")
void shouldHandleAllDiscountScenarios(int price, int discount, int expected) {
    assertThat(calculator.applyDiscount(price, discount)).isEqualTo(expected);
}
```

### 方法参数源

```java
@ParameterizedTest
@MethodSource("provideInvalidEmails")
@DisplayName("应该拒绝无效邮箱格式")
void shouldRejectInvalidEmailFormats(String email, String reason) {
    assertThat(validator.isValidEmail(email))
        .as("Email '%s' should be invalid: %s", email, reason)
        .isFalse();
}

static Stream<Arguments> provideInvalidEmails() {
    return Stream.of(
        Arguments.of("plaintext", "缺少 @"),
        Arguments.of("@example.com", "缺少本地部分"),
        Arguments.of("user@", "缺少域名"),
        Arguments.of("user@.com", "域名以点开头"),
        Arguments.of("user@domain..com", "连续的点")
    );
}

@ParameterizedTest
@MethodSource("provideUsersForValidation")
@DisplayName("应该验证用户对象")
void shouldValidateUserObjects(User user, boolean expectedValid) {
    assertThat(validator.isValid(user)).isEqualTo(expectedValid);
}

static Stream<Arguments> provideUsersForValidation() {
    return Stream.of(
        Arguments.of(new User("valid@email.com", "Name"), true),
        Arguments.of(new User("", "Name"), false),
        Arguments.of(new User("valid@email.com", ""), false),
        Arguments.of(new User(null, "Name"), false)
    );
}
```

### 枚举参数源

```java
@ParameterizedTest
@EnumSource(UserRole.class)
@DisplayName("所有角色应该有有效的权限集")
void allRolesShouldHaveValidPermissions(UserRole role) {
    Set<Permission> permissions = roleService.getPermissions(role);
    assertThat(permissions).isNotEmpty();
}

@ParameterizedTest
@EnumSource(value = UserRole.class, names = {"ADMIN", "SUPER_ADMIN"})
@DisplayName("管理员角色应该有删除权限")
void adminRolesShouldHaveDeletePermission(UserRole role) {
    Set<Permission> permissions = roleService.getPermissions(role);
    assertThat(permissions).contains(Permission.DELETE);
}
```

---

## Mock 策略

### 使用 Mockito

```java
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    private OrderRepository orderRepository;

    @Mock
    private PaymentGateway paymentGateway;

    @Mock
    private NotificationService notificationService;

    @InjectMocks
    private OrderService orderService;

    @Test
    @DisplayName("应该创建订单并发送通知")
    void shouldCreateOrderAndSendNotification() {
        // Arrange
        Order order = new Order("user-1", List.of(new Item("item-1", 100)));
        when(orderRepository.save(any(Order.class)))
            .thenAnswer(inv -> {
                Order o = inv.getArgument(0);
                o.setId("order-123");
                return o;
            });
        when(paymentGateway.charge(anyString(), anyInt()))
            .thenReturn(new PaymentResult(true, "txn-456"));

        // Act
        Order result = orderService.createOrder(order);

        // Assert
        assertThat(result.getId()).isEqualTo("order-123");
        assertThat(result.getStatus()).isEqualTo(OrderStatus.CONFIRMED);

        // 验证调用
        verify(orderRepository).save(order);
        verify(paymentGateway).charge("user-1", 100);
        verify(notificationService).sendOrderConfirmation(eq("order-123"), anyString());
    }

    @Test
    @DisplayName("应该回滚订单当支付失败时")
    void shouldRollbackOrderWhenPaymentFails() {
        // Arrange
        Order order = new Order("user-1", List.of(new Item("item-1", 100)));
        when(orderRepository.save(any())).thenReturn(order);
        when(paymentGateway.charge(anyString(), anyInt()))
            .thenReturn(new PaymentResult(false, null));

        // Act & Assert
        assertThatThrownBy(() -> orderService.createOrder(order))
            .isInstanceOf(PaymentFailedException.class);

        verify(orderRepository).delete(order);
        verify(notificationService, never()).sendOrderConfirmation(anyString(), anyString());
    }
}
```

### 参数捕获

```java
@Test
@DisplayName("应该用正确的参数调用通知服务")
void shouldCallNotificationServiceWithCorrectParams() {
    // Arrange
    ArgumentCaptor<String> emailCaptor = ArgumentCaptor.forClass(String.class);
    ArgumentCaptor<String> messageCaptor = ArgumentCaptor.forClass(String.class);

    // Act
    userService.registerUser(new CreateUserRequest("test@example.com", "Test"));

    // Assert
    verify(notificationService).sendEmail(emailCaptor.capture(), messageCaptor.capture());

    assertThat(emailCaptor.getValue()).isEqualTo("test@example.com");
    assertThat(messageCaptor.getValue()).contains("Welcome");
}
```

### Mock 静态方法

```java
import org.mockito.MockedStatic;

@Test
@DisplayName("应该使用当前时间创建记录")
void shouldCreateRecordWithCurrentTime() {
    LocalDateTime fixedTime = LocalDateTime.of(2024, 1, 15, 10, 30);

    try (MockedStatic<LocalDateTime> mockedTime = mockStatic(LocalDateTime.class)) {
        mockedTime.when(LocalDateTime::now).thenReturn(fixedTime);

        Record record = recordService.createRecord("data");

        assertThat(record.getCreatedAt()).isEqualTo(fixedTime);
    }
}
```

---

## 异步测试

### CompletableFuture 测试

```java
@Test
@DisplayName("应该异步获取用户数据")
void shouldFetchUserDataAsync() throws Exception {
    // Arrange
    when(userRepository.findByIdAsync(1L))
        .thenReturn(CompletableFuture.completedFuture(new User(1L, "Test")));

    // Act
    CompletableFuture<User> future = userService.getUserAsync(1L);

    // Assert
    User result = future.get(5, TimeUnit.SECONDS);
    assertThat(result.getName()).isEqualTo("Test");
}

@Test
@DisplayName("应该处理异步异常")
void shouldHandleAsyncException() {
    // Arrange
    CompletableFuture<User> failedFuture = new CompletableFuture<>();
    failedFuture.completeExceptionally(new UserNotFoundException(1L));
    when(userRepository.findByIdAsync(1L)).thenReturn(failedFuture);

    // Act
    CompletableFuture<User> future = userService.getUserAsync(1L);

    // Assert
    assertThatThrownBy(() -> future.get(5, TimeUnit.SECONDS))
        .hasCauseInstanceOf(UserNotFoundException.class);
}
```

### 超时测试

```java
@Test
@Timeout(value = 5, unit = TimeUnit.SECONDS)
@DisplayName("应该在5秒内完成处理")
void shouldCompleteWithinTimeout() {
    Result result = slowService.processData(largeDataSet);
    assertThat(result.isSuccess()).isTrue();
}

@Test
@DisplayName("应该在超时时抛出异常")
void shouldThrowOnTimeout() {
    assertThatThrownBy(() -> slowService.processWithTimeout(data, Duration.ofMillis(100)))
        .isInstanceOf(TimeoutException.class);
}
```

---

## 测试生命周期

### 生命周期回调

```java
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class DatabaseIntegrationTest {

    private DataSource dataSource;
    private Connection connection;

    @BeforeAll
    void setUpDatabase() {
        dataSource = createTestDataSource();
    }

    @AfterAll
    void tearDownDatabase() {
        closeDataSource(dataSource);
    }

    @BeforeEach
    void setUpConnection() throws SQLException {
        connection = dataSource.getConnection();
        connection.setAutoCommit(false);
    }

    @AfterEach
    void rollbackTransaction() throws SQLException {
        connection.rollback();
        connection.close();
    }

    @Test
    void shouldInsertUser() throws SQLException {
        // 测试会在 afterEach 中自动回滚
        userDao.insert(connection, new User("test@example.com"));

        User found = userDao.findByEmail(connection, "test@example.com");
        assertThat(found).isNotNull();
    }
}
```

### 条件测试执行

```java
@Test
@EnabledOnOs(OS.LINUX)
@DisplayName("只在 Linux 上运行")
void linuxOnlyTest() {}

@Test
@EnabledOnJre(JRE.JAVA_17)
@DisplayName("只在 Java 17 上运行")
void java17OnlyTest() {}

@Test
@EnabledIfEnvironmentVariable(named = "CI", matches = "true")
@DisplayName("只在 CI 环境运行")
void ciOnlyTest() {}

@Test
@EnabledIf("customCondition")
@DisplayName("根据自定义条件运行")
void conditionalTest() {}

boolean customCondition() {
    return System.getProperty("run.integration.tests") != null;
}

@Test
@DisabledIfSystemProperty(named = "skip.slow.tests", matches = "true")
@DisplayName("慢速测试")
void slowTest() {}
```

### 测试顺序

```java
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
class OrderedTest {

    @Test
    @Order(1)
    void firstTest() {}

    @Test
    @Order(2)
    void secondTest() {}

    @Test
    @Order(3)
    void thirdTest() {}
}

// 按方法名排序
@TestMethodOrder(MethodOrderer.MethodName.class)
class AlphabeticalTest {}

// 随机顺序（推荐，确保测试独立性）
@TestMethodOrder(MethodOrderer.Random.class)
class RandomOrderTest {}
```

---

## 覆盖率配置

### JaCoCo Maven 配置

```xml
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.11</version>
    <executions>
        <execution>
            <goals>
                <goal>prepare-agent</goal>
            </goals>
        </execution>
        <execution>
            <id>report</id>
            <phase>test</phase>
            <goals>
                <goal>report</goal>
            </goals>
        </execution>
        <execution>
            <id>check</id>
            <goals>
                <goal>check</goal>
            </goals>
            <configuration>
                <rules>
                    <rule>
                        <element>BUNDLE</element>
                        <limits>
                            <limit>
                                <counter>LINE</counter>
                                <value>COVEREDRATIO</value>
                                <minimum>0.80</minimum>
                            </limit>
                            <limit>
                                <counter>BRANCH</counter>
                                <value>COVEREDRATIO</value>
                                <minimum>0.80</minimum>
                            </limit>
                        </limits>
                    </rule>
                </rules>
            </configuration>
        </execution>
    </executions>
</plugin>
```

### 排除配置

```xml
<configuration>
    <excludes>
        <!-- 排除生成的代码 -->
        <exclude>**/generated/**</exclude>
        <!-- 排除配置类 -->
        <exclude>**/*Config.*</exclude>
        <!-- 排除 DTO -->
        <exclude>**/dto/**</exclude>
        <!-- 排除 Application 入口 -->
        <exclude>**/*Application.*</exclude>
    </excludes>
</configuration>
```

---

## 常用命令

```bash
# 运行所有测试
mvn test

# 运行特定测试类
mvn test -Dtest=UserServiceTest

# 运行特定测试方法
mvn test -Dtest=UserServiceTest#shouldCreateUser

# 运行带 tag 的测试
mvn test -Dgroups=integration

# 生成覆盖率报告
mvn test jacoco:report

# 检查覆盖率门禁
mvn test jacoco:check

# Gradle 命令
./gradlew test
./gradlew test --tests "UserServiceTest"
./gradlew jacocoTestReport
./gradlew jacocoTestCoverageVerification
```

---

## 参考资源

- [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/)
- [AssertJ Documentation](https://assertj.github.io/doc/)
- [Mockito Documentation](https://javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mockito.html)
- [JaCoCo Documentation](https://www.jacoco.org/jacoco/trunk/doc/)
