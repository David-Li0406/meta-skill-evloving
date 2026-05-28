# Modern Java Features (Java 17+)

## Records (Java 14+, final in 16)

```java
// Before: verbose POJO
public class UserDTO {
    private final String name;
    private final String email;

    public UserDTO(String name, String email) {
        this.name = name;
        this.email = email;
    }

    // getters, equals, hashCode, toString...
}

// After: records
public record UserDTO(String name, String email) {}

// Records can have compact constructors
public record User(String name, String email) {
    public User {
        Objects.requireNonNull(name);
        email = email.toLowerCase();
    }
}
```

## Sealed Classes (Java 17)

```java
// Restrict which classes can extend
public sealed class Shape permits Circle, Rectangle, Triangle {}

public final class Circle extends Shape {}
public final class Rectangle extends Shape {}
public non-sealed class Triangle extends Shape {}

// Pattern matching with sealed types
public double area(Shape shape) {
    return switch (shape) {
        case Circle c -> Math.PI * c.radius() * c.radius();
        case Rectangle r -> r.width() * r.height();
        case Triangle t -> 0.5 * t.base() * t.height();
    };
}
```

## Pattern Matching for switch (Java 21)

```java
// Type patterns in switch
Object obj = getObject();
String result = switch (obj) {
    case String s -> "String: " + s;
    case Integer i -> "Integer: " + i;
    case null -> "null";
    default -> "Unknown";
};

// Record patterns
record Point(int x, int y) {}
record Line(Point start, Point end) {}

void printLine(Object obj) {
    if (obj instanceof Line(Point(int x1, int y1), Point(int x2, int y2))) {
        System.out.printf("Line from (%d,%d) to (%d,%d)%n", x1, y1, x2, y2);
    }
}
```

## Text Blocks (Java 15)

```java
// Before
String json = "{\n" +
              "  \"name\": \"John\",\n" +
              "  \"age\": 30\n" +
              "}";

// After
String json = """
    {
      "name": "John",
      "age": 30
    }
    """;

// With string formatting
String html = """
    <html>
      <body>
        <h1>%s</h1>
      </body>
    </html>
    """.formatted(title);
```

## Virtual Threads (Java 21)

```java
// High-throughput concurrent applications
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    IntStream.range(0, 10_000).forEach(i -> {
        executor.submit(() -> {
            Thread.sleep(Duration.ofSeconds(1));
            return i;
        });
    });
}

// Structured concurrency (preview)
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    Future<String> user = scope.fork(() -> fetchUser());
    Future<Integer> order = scope.fork(() -> fetchOrder());

    scope.join();
    scope.throwIfFailed();

    return new Response(user.resultNow(), order.resultNow());
}
```

## Optional Enhancements

```java
// Stream from Optional
optional.stream().forEach(System.out::println);

// or() for chaining
Optional<String> result = optional1
    .or(() -> optional2)
    .or(() -> Optional.of("default"));

// ifPresentOrElse
optional.ifPresentOrElse(
    value -> process(value),
    () -> handleEmpty()
);
```

## Collection Factory Methods

```java
// Immutable collections
List<String> list = List.of("a", "b", "c");
Set<String> set = Set.of("x", "y", "z");
Map<String, Integer> map = Map.of("one", 1, "two", 2);

// Collectors improvements
Map<String, List<User>> grouped = users.stream()
    .collect(Collectors.groupingBy(User::department));

// toList() shorthand (Java 16)
List<String> names = users.stream()
    .map(User::name)
    .toList();
```

## var Local Variable Type Inference

```java
// Use for obvious types
var users = new ArrayList<User>();
var response = httpClient.send(request);

// Don't use when type is unclear
var result = service.process(); // What is result?

// Use in for-loops
for (var entry : map.entrySet()) {
    var key = entry.getKey();
    var value = entry.getValue();
}
```

## Best Practices

| Feature | When to Use | When to Avoid |
|---------|-------------|---------------|
| Records | DTOs, value objects | Entities with identity |
| Sealed classes | Known hierarchy | Open extension needed |
| Virtual threads | I/O-bound tasks | CPU-bound tasks |
| var | Obvious types, long generic types | Unclear return types |
| Text blocks | Multi-line strings, JSON, SQL | Single line strings |
