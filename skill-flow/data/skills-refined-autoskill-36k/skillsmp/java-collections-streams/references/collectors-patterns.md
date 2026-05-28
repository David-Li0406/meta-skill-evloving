# Collectors Patterns

## Built-in Collectors

```java
// toList, toSet, toCollection
List<String> list = stream.collect(Collectors.toList());
Set<String> set = stream.collect(Collectors.toSet());
TreeSet<String> treeSet = stream.collect(Collectors.toCollection(TreeSet::new));

// Java 16+ shorthand
List<String> list = stream.toList();  // Returns unmodifiable list

// toMap with merge function
Map<String, User> userById = users.stream()
    .collect(Collectors.toMap(
        User::getId,
        Function.identity(),
        (existing, replacement) -> existing,  // Keep existing on duplicate
        LinkedHashMap::new  // Maintain insertion order
    ));
```

## Grouping Collectors

```java
// Simple groupingBy
Map<Department, List<Employee>> byDept = employees.stream()
    .collect(Collectors.groupingBy(Employee::getDepartment));

// With downstream collector
Map<Department, Long> countByDept = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.counting()
    ));

// Nested grouping
Map<Department, Map<Level, List<Employee>>> nested = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.groupingBy(Employee::getLevel)
    ));

// GroupingBy with mapping
Map<Department, Set<String>> namesByDept = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.mapping(
            Employee::getName,
            Collectors.toSet()
        )
    ));

// GroupingBy with reducing
Map<Department, Optional<Employee>> highestPaid = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.maxBy(Comparator.comparing(Employee::getSalary))
    ));
```

## Partitioning

```java
// Simple partition
Map<Boolean, List<User>> partition = users.stream()
    .collect(Collectors.partitioningBy(User::isActive));

List<User> active = partition.get(true);
List<User> inactive = partition.get(false);

// Partition with downstream
Map<Boolean, Long> counts = users.stream()
    .collect(Collectors.partitioningBy(
        User::isActive,
        Collectors.counting()
    ));
```

## Aggregation Collectors

```java
// Statistics
IntSummaryStatistics stats = orders.stream()
    .collect(Collectors.summarizingInt(Order::getQuantity));
// stats.getSum(), stats.getAverage(), stats.getMax(), stats.getMin(), stats.getCount()

// Sum with mapping
int totalQuantity = orders.stream()
    .collect(Collectors.summingInt(Order::getQuantity));

// Average
Double avgSalary = employees.stream()
    .collect(Collectors.averagingDouble(Employee::getSalary));

// Max/Min
Optional<Employee> highest = employees.stream()
    .collect(Collectors.maxBy(Comparator.comparing(Employee::getSalary)));
```

## Joining Collector

```java
// Simple join
String csv = names.stream()
    .collect(Collectors.joining(", "));

// With prefix and suffix
String json = items.stream()
    .map(Item::toJson)
    .collect(Collectors.joining(",\n", "[\n", "\n]"));
```

## Custom Collectors

```java
// Collector.of pattern
Collector<Person, ?, ImmutableList<Person>> toImmutableList =
    Collector.of(
        ImmutableList::<Person>builder,           // Supplier
        ImmutableList.Builder::add,               // Accumulator
        (b1, b2) -> b1.addAll(b2.build()),       // Combiner
        ImmutableList.Builder::build              // Finisher
    );

// Using collectingAndThen for transformation
List<User> unmodifiable = users.stream()
    .collect(Collectors.collectingAndThen(
        Collectors.toList(),
        Collections::unmodifiableList
    ));

// Teeing collector (Java 12+) - two collectors at once
record MinMax(int min, int max) {}

MinMax result = numbers.stream()
    .collect(Collectors.teeing(
        Collectors.minBy(Comparator.naturalOrder()),
        Collectors.maxBy(Comparator.naturalOrder()),
        (min, max) -> new MinMax(
            min.orElse(0),
            max.orElse(0)
        )
    ));
```

## Filtering Collector (Java 9+)

```java
// Filter within grouping
Map<Department, List<Employee>> seniorByDept = employees.stream()
    .collect(Collectors.groupingBy(
        Employee::getDepartment,
        Collectors.filtering(
            e -> e.getYearsOfService() > 5,
            Collectors.toList()
        )
    ));

// vs filter before grouping (different semantics)
// filtering: includes all departments, even with empty lists
// filter: excludes departments with no matching employees
```

## FlatMapping Collector (Java 9+)

```java
// FlatMap within grouping
Map<Author, Set<String>> tagsByAuthor = posts.stream()
    .collect(Collectors.groupingBy(
        Post::getAuthor,
        Collectors.flatMapping(
            post -> post.getTags().stream(),
            Collectors.toSet()
        )
    ));
```
