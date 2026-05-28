# jqwik Custom Arbitraries Reference

Advanced patterns for creating domain-specific test data generators.

## Domain-Specific Generators

```java
@Provide
Arbitrary<String> validCprs() {
    return Arbitraries.integers().between(1, 31).flatMap(day ->
        Arbitraries.integers().between(1, 12).flatMap(month ->
            Arbitraries.integers().between(0, 99).flatMap(year ->
                Arbitraries.integers().between(0, 9999).map(seq ->
                    String.format("%02d%02d%02d-%04d", day, month, year, seq)
                ))));
}

@Provide
Arbitrary<PhoneNumber> danishPhoneNumbers() {
    return Arbitraries.integers().between(10000000, 99999999)
        .map(n -> new PhoneNumber("+45", String.valueOf(n)));
}

@Provide
Arbitrary<Email> validEmails() {
    var locals = Arbitraries.strings().alpha().ofMinLength(1).ofMaxLength(20);
    var domains = Arbitraries.of("gmail.com", "outlook.com", "company.dk");
    return Combinators.combine(locals, domains)
        .as((local, domain) -> new Email(local + "@" + domain));
}
```

## Combining Arbitraries

```java
@Provide
Arbitrary<Order> orders() {
    return Combinators.combine(
        Arbitraries.longs().greaterOrEqual(1),
        orderStatuses(),
        Arbitraries.lists(orderItems()).ofMinSize(1).ofMaxSize(10),
        Arbitraries.of(Currency.DKK, Currency.EUR)
    ).as(Order::new);
}

@Provide
Arbitrary<OrderStatus> orderStatuses() {
    return Arbitraries.of(OrderStatus.class);
}
```

## Constraining Generation

```java
@Property
void shouldHandleValidAges(@ForAll @IntRange(min = 0, max = 150) int age) {
    assertThat(validator.isValidAge(age)).isTrue();
}

@Property
void shouldRejectEmptyStrings(@ForAll @NotEmpty String input) {
    // input will never be empty
}

@Property
void shouldWorkWithUniqueItems(@ForAll @UniqueElements List<String> items) {
    // items has no duplicates
}

@Property
void shouldHandleSmallLists(@ForAll @Size(max = 5) List<Integer> list) {
    // list has at most 5 elements
}
```

## Statistics and Reporting

Monitor test data distribution:

```java
@Property
void shouldDistributeEvenly(@ForAll @IntRange(min = 1, max = 100) int value) {
    Statistics.label("range")
        .collect(value <= 25 ? "1-25" :
                 value <= 50 ? "26-50" :
                 value <= 75 ? "51-75" : "76-100");

    // actual test
    assertThat(process(value)).isNotNull();
}
```

## Shrinking

jqwik automatically shrinks failing cases to the simplest reproduction:

```java
@Property
void listShouldNotExceedMax(@ForAll List<Integer> list) {
    assertThat(list.size()).isLessThan(100);
    // If fails with 150-item list, jqwik shrinks to exactly 100 items
}
```

## Combining with JUnit 5

```java
class UserValidatorTest {
    // Example-based for specific business cases
    @Test
    void shouldRejectKnownInvalidCpr_1234567890() {
        assertThat(validator.isValid("123456-7890")).isFalse();
    }

    // Property-based for general invariants
    @Property
    void shouldAcceptAllValidCprFormats(@ForAll("validCprs") String cpr) {
        assertThat(validator.isValid(cpr)).isTrue();
    }

    @Property
    void shouldRejectAllMalformedCprs(@ForAll("malformedCprs") String cpr) {
        assertThat(validator.isValid(cpr)).isFalse();
    }
}
```
