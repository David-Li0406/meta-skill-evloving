---
name: Java Collections & Streams
description: Collections framework, Stream API, functional interfaces, and Optional patterns.
metadata:
  labels: [java, collections, streams, functional]
  triggers:
    files: ['**/*.java']
    keywords: [List, Map, Set, Stream, Optional, Collector, Collectors, HashMap, ArrayList, LinkedList, TreeMap]
---

# Java Collections & Streams Standards

## Collections Framework

```java
// Choose the right collection
List<String> list = new ArrayList<>();     // Random access, dynamic size
List<String> linked = new LinkedList<>();  // Frequent insertions/deletions
Set<String> set = new HashSet<>();         // Unique elements, O(1) lookup
Set<String> sorted = new TreeSet<>();      // Sorted unique elements
Map<K, V> map = new HashMap<>();           // Key-value pairs, O(1) lookup
Map<K, V> linked = new LinkedHashMap<>();  // Insertion order preserved
Map<K, V> tree = new TreeMap<>();          // Sorted by keys

// Immutable collections (Java 9+)
List<String> immutable = List.of("a", "b", "c");
Set<Integer> immutableSet = Set.of(1, 2, 3);
Map<String, Integer> immutableMap = Map.of("a", 1, "b", 2);

// Unmodifiable wrappers
List<String> unmodifiable = Collections.unmodifiableList(mutableList);
// Or with copyOf (Java 10+)
List<String> copy = List.copyOf(mutableList);
```

## Stream API

```java
// Basic pipeline
List<String> result = items.stream()
    .filter(item -> item.isActive())
    .map(Item::getName)
    .sorted()
    .distinct()
    .collect(Collectors.toList());

// Parallel streams (use with caution)
long count = largeList.parallelStream()
    .filter(this::expensiveCheck)
    .count();

// FlatMap for nested structures
List<String> allTags = posts.stream()
    .flatMap(post -> post.getTags().stream())
    .distinct()
    .toList();  // Java 16+

// Reduce operations
int sum = numbers.stream()
    .reduce(0, Integer::sum);

Optional<Integer> max = numbers.stream()
    .reduce(Integer::max);
```

## Collectors

```java
// Group by
Map<Status, List<Order>> byStatus = orders.stream()
    .collect(Collectors.groupingBy(Order::getStatus));

// Group by with downstream collector
Map<Status, Long> countByStatus = orders.stream()
    .collect(Collectors.groupingBy(
        Order::getStatus,
        Collectors.counting()
    ));

// Partition by predicate
Map<Boolean, List<User>> partitioned = users.stream()
    .collect(Collectors.partitioningBy(User::isActive));

// To map
Map<String, User> byId = users.stream()
    .collect(Collectors.toMap(
        User::getId,
        Function.identity(),
        (existing, replacement) -> existing  // Merge function
    ));

// Joining strings
String csv = items.stream()
    .map(Item::getName)
    .collect(Collectors.joining(", "));

// Statistics
IntSummaryStatistics stats = orders.stream()
    .collect(Collectors.summarizingInt(Order::getQuantity));
```

## Optional

```java
// Return Optional for nullable results
public Optional<User> findById(String id) {
    return Optional.ofNullable(repository.get(id));
}

// Chain operations
String email = findById(id)
    .filter(User::isActive)
    .map(User::getEmail)
    .orElse("unknown@example.com");

// Throw on absence
User user = findById(id)
    .orElseThrow(() -> new UserNotFoundException(id));

// Conditional execution
findById(id).ifPresent(this::sendNotification);

// With fallback computation
User user = findById(id)
    .orElseGet(() -> createDefaultUser());

// Stream of Optional (Java 9+)
List<User> activeUsers = ids.stream()
    .map(this::findById)
    .flatMap(Optional::stream)
    .filter(User::isActive)
    .toList();
```

## Best Practices

1. **Prefer immutable collections** from factories (List.of, Set.of, Map.of)
2. **Size collections** when capacity is known: `new ArrayList<>(100)`
3. **Use appropriate collection** for use case (HashMap vs TreeMap)
4. **Avoid null in collections** - use Optional or empty collections
5. **Stream once** - streams cannot be reused after terminal operation
6. **Parallel streams carefully** - only for CPU-bound, large datasets
7. **Optional for returns only** - never as fields or parameters

## References

- [Stream Pipelines](references/stream-pipelines.md) - Advanced stream patterns
- [Collectors Patterns](references/collectors-patterns.md) - Custom collectors, complex aggregations
