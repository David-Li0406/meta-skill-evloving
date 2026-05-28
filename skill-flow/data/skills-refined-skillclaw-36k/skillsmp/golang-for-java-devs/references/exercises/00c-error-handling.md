# Exercise 00c: Error Handling Philosophy

**Time:** 15 minutes
**Goal:** Understand why Go uses error returns instead of exceptions

## The Java Pattern

Java uses exceptions for error handling:

```java
public User findById(String id) {
    return repository.findById(id)
        .orElseThrow(() -> new UserNotFoundException(id));
}

// somewhere, maybe
try {
    User user = service.findById(id);
} catch (UserNotFoundException e) {
    // handle
}
```

Exceptions can be:
- **Checked:** Must be caught or declared (`throws`)
- **Unchecked:** Can propagate silently (RuntimeException)

## The Go Way

Go treats errors as values:

```go
func findByID(id string) (*User, error) {
    user, err := repo.FindByID(id)
    if err != nil {
        return nil, fmt.Errorf("finding user %s: %w", id, err)
    }
    return user, nil
}

// caller must handle
user, err := service.FindByID(id)
if err != nil {
    // must handle - can't ignore
}
```

## Why Errors as Values?

### 1. Errors are explicit

You can see the error path in the code:

```go
user, err := findUser(id)
if err != nil {
    return nil, err
}

account, err := findAccount(user.AccountID)
if err != nil {
    return nil, err
}
```

### 2. Errors can't be accidentally ignored

In Java, unchecked exceptions propagate silently. In Go:

```go
user, _ := findUser(id)  // explicit ignore - code reviewer sees this
```

### 3. Error handling is just code

No special syntax, no try/catch, no control flow disruption:

```go
if err != nil {
    // handle it - log, wrap, return, whatever
}
```

## Your Task

Convert this Java-style code to idiomatic Go error handling:

```java
public Order processOrder(String orderId) throws OrderException {
    Order order = orderRepository.findById(orderId)
        .orElseThrow(() -> new OrderNotFoundException(orderId));

    if (order.getStatus() == Status.CANCELLED) {
        throw new OrderAlreadyCancelledException(orderId);
    }

    try {
        paymentService.charge(order);
    } catch (PaymentFailedException e) {
        throw new OrderException("Payment failed", e);
    }

    order.setStatus(Status.COMPLETED);
    return orderRepository.save(order);
}
```

---

## Step by Step

### 1. Define sentinel errors (3 min)

```go
var (
    ErrOrderNotFound     = errors.New("order not found")
    ErrOrderCancelled    = errors.New("order already cancelled")
    ErrPaymentFailed     = errors.New("payment failed")
)
```

### 2. Convert to error returns (7 min)

```go
func (s *OrderService) ProcessOrder(ctx context.Context, orderID string) (*Order, error) {
    order, err := s.repo.FindByID(ctx, orderID)
    if err != nil {
        if errors.Is(err, ErrNotFound) {
            return nil, fmt.Errorf("order %s: %w", orderID, ErrOrderNotFound)
        }
        return nil, fmt.Errorf("finding order: %w", err)
    }

    if order.Status == StatusCancelled {
        return nil, fmt.Errorf("order %s: %w", orderID, ErrOrderCancelled)
    }

    if err := s.payment.Charge(ctx, order); err != nil {
        return nil, fmt.Errorf("charging order %s: %w", orderID, ErrPaymentFailed)
    }

    order.Status = StatusCompleted
    if err := s.repo.Save(ctx, order); err != nil {
        return nil, fmt.Errorf("saving order: %w", err)
    }

    return order, nil
}
```

### 3. Handle errors at call site (5 min)

```go
order, err := service.ProcessOrder(ctx, orderID)
if err != nil {
    switch {
    case errors.Is(err, ErrOrderNotFound):
        return nil, status.Error(codes.NotFound, err.Error())
    case errors.Is(err, ErrOrderCancelled):
        return nil, status.Error(codes.FailedPrecondition, err.Error())
    case errors.Is(err, ErrPaymentFailed):
        return nil, status.Error(codes.Internal, "payment processing failed")
    default:
        return nil, status.Error(codes.Internal, "internal error")
    }
}
```

## Error Wrapping

Use `%w` to wrap errors with context:

```go
if err != nil {
    return nil, fmt.Errorf("processing order %s: %w", id, err)
}
```

The `%w` verb preserves the original error for `errors.Is` and `errors.As`:

```go
// wrapped error still matches
if errors.Is(err, ErrNotFound) {
    // matches even through wrapping
}
```

## Custom Error Types

For errors that need additional data:

```go
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed on %s: %s", e.Field, e.Message)
}

// usage
return nil, &ValidationError{Field: "email", Message: "invalid format"}

// checking
var valErr *ValidationError
if errors.As(err, &valErr) {
    fmt.Printf("field %s failed: %s\n", valErr.Field, valErr.Message)
}
```

## When NOT to Use Errors

Use `panic` only for programmer errors (bugs):

```go
func MustCompile(pattern string) *regexp.Regexp {
    re, err := regexp.Compile(pattern)
    if err != nil {
        panic(err)  // programmer provided invalid regex
    }
    return re
}

// setup time - panic is ok
var emailRegex = MustCompile(`^[a-z]+@[a-z]+\.[a-z]+$`)
```

## The Error Handling Pattern

```go
result, err := doSomething()
if err != nil {
    // option 1: return as-is
    return nil, err

    // option 2: wrap with context
    return nil, fmt.Errorf("doing something: %w", err)

    // option 3: handle and continue
    log.Printf("warning: %v", err)
    result = defaultValue

    // option 4: check specific error
    if errors.Is(err, ErrNotFound) {
        return nil, ErrCustomNotFound
    }
}
```

## What Just Happened?

| Java | Go |
|------|-----|
| Exceptions interrupt flow | Errors are regular returns |
| Can ignore unchecked exceptions | Must explicitly ignore errors |
| try/catch syntax | if err != nil |
| throw new Exception() | return nil, err |
| Exception chaining | Error wrapping with %w |
| instanceof | errors.Is, errors.As |

## The Mental Shift

**Java thinking:** "Exceptions will bubble up and someone will catch them."

**Go thinking:** "Each function handles or explicitly propagates errors."

The explicit nature feels verbose at first, but it makes error paths visible and traceable.

## Checkpoint

- [ ] I can return errors from functions
- [ ] I understand error wrapping with fmt.Errorf
- [ ] I can use errors.Is and errors.As
- [ ] I accept that explicit error handling has benefits

**Next:** Exercise 00d - Simplicity and Explicitness
