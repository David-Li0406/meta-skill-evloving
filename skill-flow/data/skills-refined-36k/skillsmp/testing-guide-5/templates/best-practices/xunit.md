# xUnit / NUnit 最佳实践

C# / .NET 测试框架的配置和最佳实践指南。

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

### xUnit 项目配置

```xml
<!-- TestProject.csproj -->
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <IsPackable>false</IsPackable>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
    <PackageReference Include="xunit" Version="2.6.4" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.5.6">
      <IncludeAssets>runtime; build; native; contentfiles; analyzers</IncludeAssets>
      <PrivateAssets>all</PrivateAssets>
    </PackageReference>
    <PackageReference Include="FluentAssertions" Version="6.12.0" />
    <PackageReference Include="Moq" Version="4.20.70" />
    <PackageReference Include="coverlet.collector" Version="6.0.0">
      <IncludeAssets>runtime; build; native; contentfiles; analyzers</IncludeAssets>
      <PrivateAssets>all</PrivateAssets>
    </PackageReference>
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\MyProject\MyProject.csproj" />
  </ItemGroup>

</Project>
```

### NUnit 项目配置

```xml
<!-- TestProject.csproj -->
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <IsPackable>false</IsPackable>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
    <PackageReference Include="NUnit" Version="4.0.1" />
    <PackageReference Include="NUnit3TestAdapter" Version="4.5.0" />
    <PackageReference Include="FluentAssertions" Version="6.12.0" />
    <PackageReference Include="Moq" Version="4.20.70" />
    <PackageReference Include="coverlet.collector" Version="6.0.0" />
  </ItemGroup>

</Project>
```

---

## 测试结构

### xUnit 基本结构

```csharp
using Xunit;
using FluentAssertions;

namespace MyProject.Tests;

public class UserServiceTests
{
    private readonly UserService _sut;  // System Under Test
    private readonly Mock<IUserRepository> _userRepositoryMock;

    public UserServiceTests()
    {
        _userRepositoryMock = new Mock<IUserRepository>();
        _sut = new UserService(_userRepositoryMock.Object);
    }

    [Fact]
    public void CreateUser_ShouldCreateUser_WhenInputIsValid()
    {
        // Arrange
        var request = new CreateUserRequest("test@example.com", "Test User");
        _userRepositoryMock
            .Setup(r => r.Save(It.IsAny<User>()))
            .Returns((User u) => { u.Id = Guid.NewGuid(); return u; });

        // Act
        var result = _sut.CreateUser(request);

        // Assert
        result.Id.Should().NotBeEmpty();
        result.Email.Should().Be("test@example.com");
        result.Name.Should().Be("Test User");
    }

    [Fact]
    public void CreateUser_ShouldThrowException_WhenEmailExists()
    {
        // Arrange
        _userRepositoryMock
            .Setup(r => r.ExistsByEmail("existing@example.com"))
            .Returns(true);
        var request = new CreateUserRequest("existing@example.com", "New User");

        // Act
        var act = () => _sut.CreateUser(request);

        // Assert
        act.Should().Throw<DuplicateEmailException>()
            .WithMessage("*existing@example.com*");
    }
}
```

### NUnit 基本结构

```csharp
using NUnit.Framework;
using FluentAssertions;

namespace MyProject.Tests;

[TestFixture]
public class UserServiceTests
{
    private UserService _sut;
    private Mock<IUserRepository> _userRepositoryMock;

    [SetUp]
    public void SetUp()
    {
        _userRepositoryMock = new Mock<IUserRepository>();
        _sut = new UserService(_userRepositoryMock.Object);
    }

    [TearDown]
    public void TearDown()
    {
        // 清理资源
    }

    [Test]
    public void CreateUser_ShouldCreateUser_WhenInputIsValid()
    {
        // Arrange
        var request = new CreateUserRequest("test@example.com", "Test User");

        // Act
        var result = _sut.CreateUser(request);

        // Assert
        result.Email.Should().Be("test@example.com");
    }
}
```

### 测试分组

```csharp
// xUnit - 使用嵌套类分组
public class UserServiceTests
{
    public class CreateUserTests
    {
        [Fact]
        public void ShouldCreateUser_WhenInputIsValid() { }

        [Fact]
        public void ShouldThrowException_WhenEmailExists() { }
    }

    public class GetUserTests
    {
        [Fact]
        public void ShouldReturnUser_WhenUserExists() { }

        [Fact]
        public void ShouldReturnNull_WhenUserNotFound() { }
    }
}

// xUnit - 使用 Trait 分组
[Trait("Category", "Unit")]
[Trait("Feature", "UserManagement")]
public class UserServiceTests { }

// NUnit - 使用 Category
[TestFixture]
[Category("Unit")]
public class UserServiceTests
{
    [Test]
    [Category("CreateUser")]
    public void CreateUser_ShouldWork() { }
}
```

### 测试命名规范

```csharp
// ❌ 不好的命名
[Fact]
public void Test1() { }

[Fact]
public void TestGetUser() { }

// ✅ 好的命名 - 方法名_场景_预期结果
[Fact]
public void GetUser_WhenUserExists_ReturnsUser() { }

[Fact]
public void GetUser_WhenUserNotFound_ReturnsNull() { }

[Fact]
public void CreateUser_WhenEmailInvalid_ThrowsValidationException() { }

// ✅ 好的命名 - Should 风格
[Fact]
public void ShouldReturnUser_WhenUserExists() { }

[Fact]
public void ShouldThrowValidationException_WhenEmailInvalid() { }
```

---

## 断言最佳实践

### 使用 FluentAssertions (推荐)

```csharp
using FluentAssertions;

// ❌ xUnit 原生断言
Assert.Equal("expected", actual);
Assert.True(condition);
Assert.NotNull(result);

// ✅ FluentAssertions - 流畅、可读
actual.Should().Be("expected");
condition.Should().BeTrue();
result.Should().NotBeNull();

// 字符串断言
email.Should()
    .NotBeNullOrWhiteSpace()
    .And.Contain("@")
    .And.EndWith(".com");

// 集合断言
users.Should()
    .HaveCount(3)
    .And.Contain(u => u.Name == "Alice")
    .And.BeInAscendingOrder(u => u.Name);

// 对象断言
user.Should().BeEquivalentTo(new
{
    Name = "Test",
    Email = "test@example.com",
    IsActive = true
});

// 异常断言
var act = () => userService.GetUser(-1);
act.Should().Throw<ArgumentException>()
    .WithMessage("*must be positive*")
    .And.ParamName.Should().Be("id");

// 异步异常断言
var act = async () => await userService.GetUserAsync(-1);
await act.Should().ThrowAsync<ArgumentException>();

// 执行时间断言
var act = () => slowOperation.Execute();
act.ExecutionTime().Should().BeLessThan(TimeSpan.FromSeconds(5));
```

### 禁止弱断言

```csharp
// ❌ 弱断言 - 几乎不验证任何东西
result.Should().NotBeNull();
list.Should().NotBeEmpty();
value.Should().BeOfType<string>();

// ✅ 强断言 - 验证具体值
result.Status.Should().Be(Status.Success);
list.Should().HaveCount(3).And.Contain("item1", "item2");
value.Should().Be("expected string");
```

### 自定义断言

```csharp
// 创建自定义断言扩展
public static class UserAssertionExtensions
{
    public static UserAssertions Should(this User user)
    {
        return new UserAssertions(user);
    }
}

public class UserAssertions
{
    private readonly User _user;

    public UserAssertions(User user)
    {
        _user = user;
    }

    public AndConstraint<UserAssertions> BeActive()
    {
        _user.IsActive.Should().BeTrue("user should be active");
        return new AndConstraint<UserAssertions>(this);
    }

    public AndConstraint<UserAssertions> HaveEmail(string email)
    {
        _user.Email.Should().Be(email);
        return new AndConstraint<UserAssertions>(this);
    }
}

// 使用自定义断言
[Fact]
public void ShouldCreateActiveUser()
{
    var user = _sut.CreateUser(request);

    user.Should()
        .BeActive()
        .And.HaveEmail("test@example.com");
}
```

---

## 参数化测试

### xUnit Theory

```csharp
[Theory]
[InlineData("", false)]
[InlineData(" ", false)]
[InlineData("invalid", false)]
[InlineData("test@", false)]
[InlineData("test@example.com", true)]
public void ValidateEmail_ShouldReturnExpectedResult(string email, bool expected)
{
    var result = _validator.ValidateEmail(email);
    result.Should().Be(expected);
}

[Theory]
[InlineData(100, 0, 100)]
[InlineData(100, 10, 90)]
[InlineData(200, 25, 150)]
[InlineData(1000, 50, 500)]
public void ApplyDiscount_ShouldCalculateCorrectly(
    decimal price, int discountPercent, decimal expected)
{
    var result = _calculator.ApplyDiscount(price, discountPercent);
    result.Should().Be(expected);
}
```

### MemberData

```csharp
public class UserValidationTests
{
    [Theory]
    [MemberData(nameof(InvalidEmailTestCases))]
    public void ValidateEmail_ShouldRejectInvalidEmails(string email, string reason)
    {
        var result = _validator.ValidateEmail(email);
        result.Should().BeFalse(because: reason);
    }

    public static IEnumerable<object[]> InvalidEmailTestCases =>
        new List<object[]>
        {
            new object[] { "plaintext", "缺少 @" },
            new object[] { "@example.com", "缺少本地部分" },
            new object[] { "user@", "缺少域名" },
            new object[] { "user@.com", "域名以点开头" },
            new object[] { "user@domain..com", "连续的点" }
        };
}
```

### ClassData

```csharp
public class UserTestDataGenerator : IEnumerable<object[]>
{
    public IEnumerator<object[]> GetEnumerator()
    {
        yield return new object[] { new User("valid@email.com", "Name"), true };
        yield return new object[] { new User("", "Name"), false };
        yield return new object[] { new User("valid@email.com", ""), false };
        yield return new object[] { new User(null, "Name"), false };
    }

    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
}

[Theory]
[ClassData(typeof(UserTestDataGenerator))]
public void ValidateUser_ShouldReturnExpectedResult(User user, bool expected)
{
    var result = _validator.IsValid(user);
    result.Should().Be(expected);
}
```

### NUnit TestCase

```csharp
[TestCase("", false)]
[TestCase(" ", false)]
[TestCase("test@example.com", true)]
public void ValidateEmail_ShouldReturnExpectedResult(string email, bool expected)
{
    var result = _validator.ValidateEmail(email);
    result.Should().Be(expected);
}

[TestCaseSource(nameof(DiscountTestCases))]
public void ApplyDiscount_ShouldCalculateCorrectly(
    decimal price, int discount, decimal expected)
{
    var result = _calculator.ApplyDiscount(price, discount);
    result.Should().Be(expected);
}

private static IEnumerable<TestCaseData> DiscountTestCases()
{
    yield return new TestCaseData(100m, 0, 100m).SetName("无折扣");
    yield return new TestCaseData(100m, 10, 90m).SetName("10%折扣");
    yield return new TestCaseData(200m, 25, 150m).SetName("25%折扣");
}
```

---

## Mock 策略

### 使用 Moq

```csharp
using Moq;

public class OrderServiceTests
{
    private readonly Mock<IOrderRepository> _orderRepoMock;
    private readonly Mock<IPaymentGateway> _paymentMock;
    private readonly Mock<INotificationService> _notificationMock;
    private readonly OrderService _sut;

    public OrderServiceTests()
    {
        _orderRepoMock = new Mock<IOrderRepository>();
        _paymentMock = new Mock<IPaymentGateway>();
        _notificationMock = new Mock<INotificationService>();
        _sut = new OrderService(
            _orderRepoMock.Object,
            _paymentMock.Object,
            _notificationMock.Object);
    }

    [Fact]
    public void CreateOrder_ShouldCreateAndNotify()
    {
        // Arrange
        var order = new Order("user-1", new[] { new Item("item-1", 100) });
        _orderRepoMock
            .Setup(r => r.Save(It.IsAny<Order>()))
            .Callback<Order>(o => o.Id = Guid.NewGuid())
            .Returns((Order o) => o);
        _paymentMock
            .Setup(p => p.Charge(It.IsAny<string>(), It.IsAny<decimal>()))
            .Returns(new PaymentResult(true, "txn-456"));

        // Act
        var result = _sut.CreateOrder(order);

        // Assert
        result.Id.Should().NotBeEmpty();
        result.Status.Should().Be(OrderStatus.Confirmed);

        // 验证调用
        _orderRepoMock.Verify(r => r.Save(order), Times.Once);
        _paymentMock.Verify(p => p.Charge("user-1", 100), Times.Once);
        _notificationMock.Verify(
            n => n.SendOrderConfirmation(It.IsAny<Guid>(), It.IsAny<string>()),
            Times.Once);
    }

    [Fact]
    public void CreateOrder_ShouldRollback_WhenPaymentFails()
    {
        // Arrange
        var order = new Order("user-1", new[] { new Item("item-1", 100) });
        _paymentMock
            .Setup(p => p.Charge(It.IsAny<string>(), It.IsAny<decimal>()))
            .Returns(new PaymentResult(false, null));

        // Act
        var act = () => _sut.CreateOrder(order);

        // Assert
        act.Should().Throw<PaymentFailedException>();
        _orderRepoMock.Verify(r => r.Delete(order), Times.Once);
        _notificationMock.Verify(
            n => n.SendOrderConfirmation(It.IsAny<Guid>(), It.IsAny<string>()),
            Times.Never);
    }
}
```

### 参数捕获

```csharp
[Fact]
public void RegisterUser_ShouldSendWelcomeEmail()
{
    // Arrange
    var request = new CreateUserRequest("test@example.com", "Test");
    string? capturedEmail = null;
    string? capturedMessage = null;

    _notificationMock
        .Setup(n => n.SendEmail(It.IsAny<string>(), It.IsAny<string>()))
        .Callback<string, string>((email, message) =>
        {
            capturedEmail = email;
            capturedMessage = message;
        });

    // Act
    _sut.RegisterUser(request);

    // Assert
    capturedEmail.Should().Be("test@example.com");
    capturedMessage.Should().Contain("Welcome");
}

// 使用 Capture
[Fact]
public void RegisterUser_ShouldSendWelcomeEmail_UsingCapture()
{
    // Arrange
    var emailCapture = new List<string>();
    _notificationMock
        .Setup(n => n.SendEmail(Capture.In(emailCapture), It.IsAny<string>()));

    // Act
    _sut.RegisterUser(new CreateUserRequest("test@example.com", "Test"));

    // Assert
    emailCapture.Should().ContainSingle().Which.Should().Be("test@example.com");
}
```

### Mock 序列调用

```csharp
[Fact]
public void RetryOperation_ShouldRetryOnFailure()
{
    // Arrange
    _externalServiceMock
        .SetupSequence(s => s.Call())
        .Throws(new TimeoutException())
        .Throws(new TimeoutException())
        .Returns(new Result(true));

    // Act
    var result = _sut.CallWithRetry();

    // Assert
    result.IsSuccess.Should().BeTrue();
    _externalServiceMock.Verify(s => s.Call(), Times.Exactly(3));
}
```

---

## 异步测试

### 异步测试基础

```csharp
[Fact]
public async Task GetUserAsync_ShouldReturnUser_WhenUserExists()
{
    // Arrange
    var expectedUser = new User(1, "Test");
    _userRepoMock
        .Setup(r => r.FindByIdAsync(1))
        .ReturnsAsync(expectedUser);

    // Act
    var result = await _sut.GetUserAsync(1);

    // Assert
    result.Should().BeEquivalentTo(expectedUser);
}

[Fact]
public async Task GetUserAsync_ShouldThrow_WhenUserNotFound()
{
    // Arrange
    _userRepoMock
        .Setup(r => r.FindByIdAsync(It.IsAny<int>()))
        .ReturnsAsync((User?)null);

    // Act
    var act = async () => await _sut.GetUserAsync(999);

    // Assert
    await act.Should().ThrowAsync<UserNotFoundException>();
}
```

### 取消令牌测试

```csharp
[Fact]
public async Task LongOperation_ShouldCancel_WhenTokenCancelled()
{
    // Arrange
    var cts = new CancellationTokenSource();
    cts.CancelAfter(TimeSpan.FromMilliseconds(100));

    // Act
    var act = async () => await _sut.LongOperationAsync(cts.Token);

    // Assert
    await act.Should().ThrowAsync<OperationCanceledException>();
}

[Fact]
public async Task ProcessAsync_ShouldRespectCancellation()
{
    // Arrange
    var cts = new CancellationTokenSource();
    var task = _sut.ProcessAsync(cts.Token);

    // Act
    cts.Cancel();

    // Assert
    await FluentActions
        .Awaiting(() => task)
        .Should().ThrowAsync<OperationCanceledException>();
}
```

### 并发测试

```csharp
[Fact]
public async Task ConcurrentAccess_ShouldBeThreadSafe()
{
    // Arrange
    var counter = new ThreadSafeCounter();
    var tasks = Enumerable.Range(0, 100)
        .Select(_ => Task.Run(() => counter.Increment()));

    // Act
    await Task.WhenAll(tasks);

    // Assert
    counter.Value.Should().Be(100);
}
```

---

## 测试生命周期

### xUnit 生命周期

```csharp
// xUnit 每个测试创建新实例，构造函数相当于 SetUp
public class UserServiceTests : IDisposable
{
    private readonly UserService _sut;
    private readonly TestDatabase _db;

    public UserServiceTests()
    {
        // 每个测试前执行
        _db = new TestDatabase();
        _sut = new UserService(_db.Connection);
    }

    public void Dispose()
    {
        // 每个测试后执行
        _db.Dispose();
    }

    [Fact]
    public void Test1() { }
}

// 共享资源 - 使用 IClassFixture
public class DatabaseFixture : IDisposable
{
    public TestDatabase Database { get; }

    public DatabaseFixture()
    {
        Database = new TestDatabase();
        Database.Migrate();
    }

    public void Dispose() => Database.Dispose();
}

public class UserServiceTests : IClassFixture<DatabaseFixture>
{
    private readonly DatabaseFixture _fixture;

    public UserServiceTests(DatabaseFixture fixture)
    {
        _fixture = fixture;
    }

    [Fact]
    public void Test1()
    {
        // 使用 _fixture.Database
    }
}

// 跨多个测试类共享 - 使用 ICollectionFixture
[CollectionDefinition("Database")]
public class DatabaseCollection : ICollectionFixture<DatabaseFixture> { }

[Collection("Database")]
public class UserTests
{
    public UserTests(DatabaseFixture fixture) { }
}

[Collection("Database")]
public class OrderTests
{
    public OrderTests(DatabaseFixture fixture) { }
}
```

### NUnit 生命周期

```csharp
[TestFixture]
public class UserServiceTests
{
    private TestDatabase _db;
    private UserService _sut;

    [OneTimeSetUp]
    public void OneTimeSetUp()
    {
        // 所有测试前执行一次
        _db = new TestDatabase();
        _db.Migrate();
    }

    [OneTimeTearDown]
    public void OneTimeTearDown()
    {
        // 所有测试后执行一次
        _db.Dispose();
    }

    [SetUp]
    public void SetUp()
    {
        // 每个测试前执行
        _sut = new UserService(_db.Connection);
        _db.BeginTransaction();
    }

    [TearDown]
    public void TearDown()
    {
        // 每个测试后执行
        _db.RollbackTransaction();
    }
}
```

---

## 覆盖率配置

### Coverlet 配置

```json
// coverlet.runsettings
<?xml version="1.0" encoding="utf-8" ?>
<RunSettings>
  <DataCollectionRunSettings>
    <DataCollectors>
      <DataCollector friendlyName="XPlat Code Coverage">
        <Configuration>
          <Format>cobertura,opencover</Format>
          <Exclude>[*]*.Migrations.*,[*]*.Generated.*</Exclude>
          <ExcludeByFile>**/Migrations/*.cs,**/*.Designer.cs</ExcludeByFile>
          <ExcludeByAttribute>
            Obsolete,GeneratedCodeAttribute,CompilerGeneratedAttribute
          </ExcludeByAttribute>
          <SingleHit>false</SingleHit>
          <UseSourceLink>true</UseSourceLink>
        </Configuration>
      </DataCollector>
    </DataCollectors>
  </DataCollectionRunSettings>
</RunSettings>
```

### 覆盖率门禁

```xml
<!-- Directory.Build.props -->
<Project>
  <PropertyGroup>
    <CollectCoverage>true</CollectCoverage>
    <CoverletOutputFormat>cobertura</CoverletOutputFormat>
    <Threshold>80</Threshold>
    <ThresholdType>line,branch</ThresholdType>
    <ThresholdStat>total</ThresholdStat>
  </PropertyGroup>
</Project>
```

---

## 常用命令

```bash
# 运行所有测试
dotnet test

# 运行特定项目
dotnet test MyProject.Tests

# 运行特定测试
dotnet test --filter "FullyQualifiedName~UserServiceTests"
dotnet test --filter "Category=Unit"

# 生成覆盖率报告
dotnet test --collect:"XPlat Code Coverage"

# 使用 coverlet
dotnet test /p:CollectCoverage=true /p:CoverletOutputFormat=cobertura

# 生成 HTML 报告 (需要 ReportGenerator)
reportgenerator -reports:coverage.cobertura.xml -targetdir:coveragereport

# 检查覆盖率门禁
dotnet test /p:CollectCoverage=true /p:Threshold=80
```

---

## 参考资源

- [xUnit Documentation](https://xunit.net/docs/getting-started/netcore/cmdline)
- [NUnit Documentation](https://docs.nunit.org/)
- [FluentAssertions Documentation](https://fluentassertions.com/introduction)
- [Moq Quickstart](https://github.com/moq/moq4/wiki/Quickstart)
- [Coverlet Documentation](https://github.com/coverlet-coverage/coverlet)
