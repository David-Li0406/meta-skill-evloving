# Stream Pipelines

## Lazy Evaluation

Streams are lazy - intermediate operations don't execute until a terminal operation is called.

```java
// Nothing happens until collect() is called
Stream<String> lazy = items.stream()
    .peek(i -> System.out.println("Processing: " + i))  // Not called yet
    .filter(i -> i.length() > 3)
    .map(String::toUpperCase);

// Terminal operation triggers execution
List<String> result = lazy.collect(Collectors.toList());
```

## Short-Circuit Operations

```java
// findFirst - stops at first match
Optional<User> first = users.stream()
    .filter(User::isAdmin)
    .findFirst();

// anyMatch - stops when condition is true
boolean hasAdmin = users.stream()
    .anyMatch(User::isAdmin);

// limit - stops after n elements
List<User> topThree = users.stream()
    .sorted(Comparator.comparing(User::getScore).reversed())
    .limit(3)
    .toList();

// takeWhile (Java 9+) - takes elements while predicate is true
List<Integer> untilNegative = numbers.stream()
    .takeWhile(n -> n >= 0)
    .toList();

// dropWhile (Java 9+) - drops elements while predicate is true
List<Integer> afterNegative = numbers.stream()
    .dropWhile(n -> n < 0)
    .toList();
```

## Advanced Mapping

```java
// flatMap for one-to-many
List<Tag> allTags = posts.stream()
    .flatMap(post -> post.getTags().stream())
    .distinct()
    .toList();

// mapMulti (Java 16+) - more efficient flatMap alternative
List<Integer> doubled = numbers.stream()
    .<Integer>mapMulti((num, consumer) -> {
        consumer.accept(num);
        consumer.accept(num * 2);
    })
    .toList();

// Conditional mapping
List<String> processed = items.stream()
    .map(item -> switch (item.getType()) {
        case A -> processTypeA(item);
        case B -> processTypeB(item);
        default -> item.getName();
    })
    .toList();
```

## Reducing Operations

```java
// Simple reduce
int sum = numbers.stream()
    .reduce(0, Integer::sum);

// Reduce with identity, accumulator, combiner (for parallel)
int total = orders.parallelStream()
    .reduce(
        0,                              // identity
        (acc, order) -> acc + order.getTotal(),  // accumulator
        Integer::sum                    // combiner (for parallel)
    );

// Collect vs Reduce
// Use collect for mutable reduction (building collections)
List<String> list = stream.collect(Collectors.toList());

// Use reduce for immutable reduction (computing single value)
Optional<BigDecimal> total = amounts.stream()
    .reduce(BigDecimal::add);
```

## Parallel Streams

```java
// When to use parallel streams:
// 1. Large dataset (> 10,000 elements)
// 2. CPU-bound operations (not I/O)
// 3. Independent operations (no shared mutable state)
// 4. Splittable data source (ArrayList, arrays)

// Good use case
long count = hugeList.parallelStream()  // ArrayList, large
    .filter(this::cpuIntensiveCheck)     // CPU-bound
    .count();

// Bad use cases
// - LinkedList (not easily splittable)
// - I/O operations (blocking, not CPU-bound)
// - Small datasets (overhead > benefit)
// - Operations with side effects

// Custom thread pool for parallel streams
ForkJoinPool customPool = new ForkJoinPool(4);
List<Result> results = customPool.submit(() ->
    items.parallelStream()
        .map(this::process)
        .toList()
).get();
```

## Infinite Streams

```java
// Generate infinite stream
Stream<UUID> uuids = Stream.generate(UUID::randomUUID);

// Iterate with seed
Stream<Integer> evens = Stream.iterate(0, n -> n + 2);

// Iterate with predicate (Java 9+)
Stream<Integer> limited = Stream.iterate(1, n -> n < 100, n -> n * 2);

// Use with limit
List<UUID> fiveUuids = Stream.generate(UUID::randomUUID)
    .limit(5)
    .toList();
```

## Debugging Streams

```java
// peek for debugging (remove in production)
List<String> result = items.stream()
    .peek(i -> log.debug("Before filter: {}", i))
    .filter(Item::isActive)
    .peek(i -> log.debug("After filter: {}", i))
    .map(Item::getName)
    .peek(n -> log.debug("After map: {}", n))
    .toList();

// Breakpoint-friendly version
List<String> result = items.stream()
    .filter(item -> {
        boolean active = item.isActive();  // Set breakpoint here
        return active;
    })
    .map(Item::getName)
    .toList();
```
