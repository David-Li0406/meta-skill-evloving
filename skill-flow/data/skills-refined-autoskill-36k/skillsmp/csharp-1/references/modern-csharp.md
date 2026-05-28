# Modern C# Features (C# 10+)

## Records

```csharp
// Record class (reference type)
public record User(string Name, string Email);

// Record struct (value type, C# 10)
public readonly record struct Point(int X, int Y);

// With expressions
var user = new User("John", "john@example.com");
var updated = user with { Email = "new@example.com" };

// Primary constructor for records
public record Order(int Id, decimal Total)
{
    public string Status { get; init; } = "Pending";
}
```

## Primary Constructors (C# 12)

```csharp
// On classes and structs
public class UserService(IUserRepository repository, ILogger<UserService> logger)
{
    public User GetUser(int id)
    {
        logger.LogInformation("Getting user {Id}", id);
        return repository.FindById(id);
    }
}

// Parameters captured as fields
public class BankAccount(string accountId, decimal initialBalance)
{
    private decimal _balance = initialBalance;

    public string AccountId => accountId;
    public decimal Balance => _balance;
}
```

## Pattern Matching

```csharp
// Type patterns
object obj = GetValue();
if (obj is string s && s.Length > 0)
{
    Console.WriteLine(s);
}

// Property patterns
if (user is { Name: "Admin", Status: UserStatus.Active })
{
    GrantAdminAccess();
}

// List patterns (C# 11)
int[] numbers = { 1, 2, 3, 4, 5 };
var result = numbers switch
{
    [1, 2, ..] => "Starts with 1, 2",
    [.., 4, 5] => "Ends with 4, 5",
    [_, _, 3, _, _] => "Middle is 3",
    [] => "Empty",
    _ => "Other"
};

// Relational patterns
string GetWaterState(int tempC) => tempC switch
{
    < 0 => "Solid",
    >= 0 and < 100 => "Liquid",
    >= 100 => "Gas",
};
```

## Nullable Reference Types

```csharp
#nullable enable

public class UserService
{
    // Non-nullable parameter
    public User GetUser(string id)
    {
        // Must return non-null User
    }

    // Nullable return
    public User? FindUser(string id)
    {
        return _users.FirstOrDefault(u => u.Id == id);
    }

    // Null-forgiving operator (use sparingly!)
    public string GetName(User? user)
    {
        return user!.Name; // Assert not null
    }

    // Required members (C# 11)
    public required string Name { get; init; }
}

// Null coalescing
string name = user?.Name ?? "Unknown";
string email = user?.Email ?? throw new ArgumentException();
```

## Collection Expressions (C# 12)

```csharp
// Simple initialization
int[] numbers = [1, 2, 3, 4, 5];
List<string> names = ["Alice", "Bob"];
Span<int> span = [1, 2, 3];

// Spread operator
int[] first = [1, 2, 3];
int[] second = [4, 5, 6];
int[] combined = [..first, ..second]; // [1, 2, 3, 4, 5, 6]

// Empty collection
List<User> users = [];
```

## Raw String Literals (C# 11)

```csharp
// Multi-line strings with preserved formatting
string json = """
    {
        "name": "John",
        "email": "john@example.com"
    }
    """;

// With interpolation
string html = $"""
    <html>
        <body>
            <h1>{title}</h1>
        </body>
    </html>
    """;

// Escape sequences not needed
string path = """C:\Users\John\Documents""";
```

## File-Scoped Types (C# 11)

```csharp
// Only visible within file
file class InternalHelper
{
    public static void DoWork() { }
}

file record struct TempData(string Value);
```

## Static Abstract Members in Interfaces (C# 11)

```csharp
public interface IParsable<TSelf> where TSelf : IParsable<TSelf>
{
    static abstract TSelf Parse(string s);
    static virtual TSelf Default => default!;
}

public readonly struct Point : IParsable<Point>
{
    public int X { get; }
    public int Y { get; }

    public static Point Parse(string s)
    {
        var parts = s.Split(',');
        return new Point(int.Parse(parts[0]), int.Parse(parts[1]));
    }
}

// Generic math
public static T Sum<T>(T[] values) where T : INumber<T>
{
    T result = T.Zero;
    foreach (var value in values)
        result += value;
    return result;
}
```

## Async/Await Patterns

```csharp
// ConfigureAwait for library code
public async Task<User> GetUserAsync(int id)
{
    var data = await _repository.FindAsync(id).ConfigureAwait(false);
    return MapToUser(data);
}

// IAsyncEnumerable
public async IAsyncEnumerable<User> GetAllUsersAsync(
    [EnumeratorCancellation] CancellationToken ct = default)
{
    await foreach (var user in _repository.StreamAllAsync().WithCancellation(ct))
    {
        yield return user;
    }
}

// Parallel async
var tasks = ids.Select(id => GetUserAsync(id));
var users = await Task.WhenAll(tasks);
```

## Best Practices Summary

| Feature | When to Use | When to Avoid |
|---------|-------------|---------------|
| Records | DTOs, immutable data | Entities with identity |
| Primary constructors | Simple DI, thin classes | Complex initialization |
| Nullable references | All new code | Legacy migration (gradual) |
| Pattern matching | Complex conditionals | Simple equality checks |
| Collection expressions | New collections | Modifying existing |
| Raw strings | JSON, SQL, multi-line | Simple strings |
