# Mockito Testing Patterns

## Basic Mocking

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    private UserRepository userRepository;

    @Mock
    private OrderRepository orderRepository;

    @InjectMocks
    private OrderService orderService;

    @Test
    void shouldCreateOrder() {
        // Given
        User user = new User(1L, "John");
        when(userRepository.findById(1L)).thenReturn(Optional.of(user));
        when(orderRepository.save(any(Order.class))).thenAnswer(inv -> {
            Order order = inv.getArgument(0);
            order.setId(100L);
            return order;
        });

        // When
        Order order = orderService.createOrder(1L, List.of(item1, item2));

        // Then
        assertNotNull(order);
        assertEquals(100L, order.getId());
        verify(orderRepository).save(any(Order.class));
    }
}
```

## Stubbing

```java
// Return value
when(mock.method()).thenReturn(value);

// Throw exception
when(mock.method()).thenThrow(new RuntimeException());

// Multiple calls
when(mock.method())
    .thenReturn(first)
    .thenReturn(second)
    .thenThrow(new RuntimeException());

// Argument matchers
when(userRepo.findByEmail(anyString())).thenReturn(user);
when(userRepo.findByAge(argThat(age -> age > 18))).thenReturn(adults);

// Void methods
doNothing().when(mock).voidMethod();
doThrow(new RuntimeException()).when(mock).voidMethod();
```

## Verification

```java
// Called once (default)
verify(mock).method();

// Called specific times
verify(mock, times(3)).method();
verify(mock, never()).method();
verify(mock, atLeast(2)).method();
verify(mock, atMost(5)).method();

// With argument capture
ArgumentCaptor<Order> captor = ArgumentCaptor.forClass(Order.class);
verify(orderRepo).save(captor.capture());
Order saved = captor.getValue();
assertEquals(expectedTotal, saved.getTotal());

// Verification order
InOrder inOrder = inOrder(first, second);
inOrder.verify(first).method();
inOrder.verify(second).method();

// No more interactions
verifyNoMoreInteractions(mock);
```

## Spying

```java
// Partial mock - real object with stubbed methods
@Spy
private List<String> spiedList = new ArrayList<>();

@Test
void shouldSpyRealObject() {
    spiedList.add("one");
    spiedList.add("two");

    verify(spiedList).add("one");
    assertEquals(2, spiedList.size()); // Real behavior

    // Override specific method
    doReturn(100).when(spiedList).size();
    assertEquals(100, spiedList.size());
}
```

## BDD Style

```java
import static org.mockito.BDDMockito.*;

@Test
void shouldProcessPayment() {
    // Given
    given(paymentGateway.process(any())).willReturn(PaymentResult.SUCCESS);

    // When
    boolean result = paymentService.pay(order);

    // Then
    then(paymentGateway).should().process(any());
    assertThat(result).isTrue();
}
```

## Static Mocking

```java
try (MockedStatic<Utils> utilities = mockStatic(Utils.class)) {
    utilities.when(() -> Utils.generateId()).thenReturn("mocked-id");
    
    String id = Utils.generateId();
    
    assertEquals("mocked-id", id);
}
```
