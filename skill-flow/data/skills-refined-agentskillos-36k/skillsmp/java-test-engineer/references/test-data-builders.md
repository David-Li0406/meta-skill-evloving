# Test Data Builders Reference

Patterns for creating test fixtures with fluent APIs.

## Builder Pattern

```java
class UserBuilder {
    private String email = "default@test.com";
    private String name = "Test User";
    private List<Role> roles = List.of(Role.USER);

    static UserBuilder aUser() { return new UserBuilder(); }

    UserBuilder withEmail(String email) { this.email = email; return this; }
    UserBuilder withName(String name) { this.name = name; return this; }
    UserBuilder withRoles(Role... roles) { this.roles = List.of(roles); return this; }
    UserBuilder asAdmin() { return withRoles(Role.ADMIN); }

    User build() { return new User(email, name, roles); }
}

// Usage
var admin = aUser().withEmail("admin@test.com").asAdmin().build();
var regularUser = aUser().withName("John Doe").build();
```

## Mother Pattern

For complex objects with common configurations:

```java
class OrderMother {
    static Order pendingOrder() {
        return Order.builder()
            .status(PENDING)
            .items(List.of(ItemMother.defaultItem()))
            .createdAt(Instant.now())
            .build();
    }

    static Order completedOrder() {
        return pendingOrder().toBuilder()
            .status(COMPLETED)
            .completedAt(Instant.now())
            .build();
    }

    static Order cancelledOrder() {
        return pendingOrder().toBuilder()
            .status(CANCELLED)
            .cancelledAt(Instant.now())
            .cancelReason("Customer request")
            .build();
    }
}

class ItemMother {
    static OrderItem defaultItem() {
        return OrderItem.builder()
            .productId(ProductId.of(1L))
            .quantity(1)
            .unitPrice(Money.of(100, Currency.DKK))
            .build();
    }

    static OrderItem expensiveItem() {
        return defaultItem().toBuilder()
            .unitPrice(Money.of(10000, Currency.DKK))
            .build();
    }
}
```

## Combining Builders and Mothers

```java
@Test
void shouldCalculateOrderTotal() {
    var order = OrderMother.pendingOrder().toBuilder()
        .items(List.of(
            ItemMother.defaultItem(),
            ItemMother.expensiveItem()
        ))
        .build();

    assertThat(order.total()).isEqualTo(Money.of(10100, Currency.DKK));
}

@Test
void shouldApplyDiscountToLargeOrders() {
    var order = OrderMother.pendingOrder().toBuilder()
        .customer(aUser().asVipCustomer().build())
        .items(List.of(ItemMother.expensiveItem()))
        .build();

    var discounted = discountService.apply(order);

    assertThat(discounted.discount()).isGreaterThan(Money.ZERO);
}
```

## When to Use Each Pattern

| Pattern | Use When |
|---------|----------|
| Builder | Need flexibility in construction, many optional fields |
| Mother | Common configurations reused across tests |
| Combination | Complex domain with many variations |

## Anti-Patterns

```java
// BAD: hardcoded values everywhere
var user = new User("test@test.com", "Test", List.of(Role.USER));
var user2 = new User("test2@test.com", "Test2", List.of(Role.USER));

// GOOD: builders with meaningful names
var user = aUser().build();
var admin = aUser().asAdmin().build();
```
