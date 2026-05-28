---
name: test-generator
description: Generates comprehensive unit and integration tests using xUnit, FluentAssertions, and NSubstitute
---

# Test Generator Skill

Bu skill, Merge E-Commerce Backend projesi için test dosyaları oluşturur.

## Ne Zaman Kullan

- "Test yaz", "unit test oluştur" dendiğinde
- Bir handler/service için test istendiğinde
- "Bu kodu test et" gibi isteklerde

## Test Türleri

### 1. Unit Test (Handler)

```
Merge.Tests/Unit/Application/{Module}/Commands/
└── {Name}CommandHandlerTests.cs
```

```csharp
public class {Name}CommandHandlerTests
{
    private readonly IRepository<{Entity}> _repository;
    private readonly IUnitOfWork _unitOfWork;
    private readonly IMapper _mapper;
    private readonly ILogger<{Name}CommandHandler> _logger;
    private readonly {Name}CommandHandler _sut;

    public {Name}CommandHandlerTests()
    {
        _repository = Substitute.For<IRepository<{Entity}>>();
        _unitOfWork = Substitute.For<IUnitOfWork>();
        _mapper = Substitute.For<IMapper>();
        _logger = Substitute.For<ILogger<{Name}CommandHandler>>();

        _sut = new {Name}CommandHandler(
            _repository,
            _unitOfWork,
            _mapper,
            _logger);
    }

    [Fact]
    public async Task Handle_ValidCommand_Returns{Result}()
    {
        // Arrange
        var command = new {Name}Command(/* valid data */);
        var entity = {Entity}.Create(/* data */);
        var expectedDto = new {Entity}Dto { /* data */ };

        _repository.AddAsync(Arg.Any<{Entity}>(), Arg.Any<CancellationToken>())
            .Returns(Task.CompletedTask);
        _unitOfWork.SaveChangesAsync(Arg.Any<CancellationToken>())
            .Returns(Task.FromResult(1));
        _mapper.Map<{Entity}Dto>(Arg.Any<{Entity}>())
            .Returns(expectedDto);

        // Act
        var result = await _sut.Handle(command, CancellationToken.None);

        // Assert
        result.Should().NotBeNull();
        result.Should().BeEquivalentTo(expectedDto);

        await _repository.Received(1).AddAsync(
            Arg.Any<{Entity}>(),
            Arg.Any<CancellationToken>());
        await _unitOfWork.Received(1).SaveChangesAsync(
            Arg.Any<CancellationToken>());
    }

    [Fact]
    public async Task Handle_InvalidCommand_ThrowsValidationException()
    {
        // Arrange
        var command = new {Name}Command(/* invalid data */);

        // Act
        var act = () => _sut.Handle(command, CancellationToken.None);

        // Assert
        await act.Should().ThrowAsync<ValidationException>();
    }
}
```

### 2. Unit Test (Entity)

```csharp
public class {Entity}Tests
{
    [Fact]
    public void Create_ValidData_ReturnsEntity()
    {
        // Arrange
        var name = "Test Name";

        // Act
        var entity = {Entity}.Create(name);

        // Assert
        entity.Should().NotBeNull();
        entity.Id.Should().NotBeEmpty();
        entity.Name.Should().Be(name);
        entity.DomainEvents.Should().ContainSingle()
            .Which.Should().BeOfType<{Entity}CreatedEvent>();
    }

    [Theory]
    [InlineData(null)]
    [InlineData("")]
    [InlineData("   ")]
    public void Create_InvalidName_ThrowsArgumentException(string? name)
    {
        // Act
        var act = () => {Entity}.Create(name!);

        // Assert
        act.Should().Throw<ArgumentException>();
    }
}
```

### 3. Integration Test

```csharp
public class {Entity}sControllerTests : IClassFixture<CustomWebApplicationFactory>
{
    private readonly HttpClient _client;
    private readonly CustomWebApplicationFactory _factory;

    public {Entity}sControllerTests(CustomWebApplicationFactory factory)
    {
        _factory = factory;
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task GetAll_ReturnsPagedResult()
    {
        // Act
        var response = await _client.GetAsync("/api/v1/{entities}");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);

        var content = await response.Content.ReadFromJsonAsync<PagedResult<{Entity}Dto>>();
        content.Should().NotBeNull();
        content!.Items.Should().NotBeEmpty();
    }

    [Fact]
    public async Task Create_ValidRequest_ReturnsCreated()
    {
        // Arrange
        var request = new Create{Entity}Command(/* data */);

        // Act
        var response = await _client.PostAsJsonAsync("/api/v1/{entities}", request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Created);
        response.Headers.Location.Should().NotBeNull();
    }
}
```

## Test Naming Convention

```
{Method}_{Scenario}_{ExpectedResult}
```

Örnekler:
- `Create_ValidData_ReturnsEntity`
- `Handle_ProductNotFound_ThrowsNotFoundException`
- `Update_ConcurrentModification_ThrowsConflictException`

## Kurallar

1. AAA pattern (Arrange-Act-Assert)
2. NSubstitute for mocking
3. FluentAssertions for assertions
4. Her public method için en az 2 test (happy + sad path)
5. Theory ile parameterized tests
