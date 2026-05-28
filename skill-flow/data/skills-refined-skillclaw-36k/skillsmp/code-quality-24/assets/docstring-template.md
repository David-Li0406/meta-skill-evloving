# Docstring Templates

## Python (Google Style)

### Function Template

```python
def function_name(param1: Type1, param2: Type2) -> ReturnType:
    """Short one-line description of function.

    Longer description if needed. Explain the purpose,
    any important details about behavior, and context.

    Args:
        param1: Description of first parameter.
        param2: Description of second parameter.

    Returns:
        Description of what is returned.

    Raises:
        ErrorType: When this error occurs.
        AnotherError: When this other error occurs.

    Examples:
        Basic usage:
        >>> result = function_name(value1, value2)
        >>> assert result == expected

        Edge case:
        >>> function_name(None, value2)
        Raises ValueError
    """
```

### Class Template

```python
class ClassName:
    """Short one-line description of class.

    Longer description of the class purpose and behavior.
    Include important usage notes.

    Attributes:
        attr1: Description of first attribute.
        attr2: Description of second attribute.

    Examples:
        >>> obj = ClassName(param1, param2)
        >>> obj.method()
        expected_result
    """

    def __init__(self, param1: Type1, param2: Type2) -> None:
        """Initialize ClassName.

        Args:
            param1: Description of first parameter.
            param2: Description of second parameter.
        """
```

### Method Template

```python
def method_name(self, param: Type) -> ReturnType:
    """Short description of what method does.

    Args:
        param: Description of parameter.

    Returns:
        Description of return value.

    Raises:
        ErrorType: When error condition occurs.
    """
```

---

## TypeScript (TSDoc Style)

### Function Template

```typescript
/**
 * Short one-line description of function.
 *
 * Longer description if needed. Explain the purpose,
 * any important details about behavior, and context.
 *
 * @param param1 - Description of first parameter
 * @param param2 - Description of second parameter
 * @returns Description of what is returned
 * @throws {ErrorType} When this error occurs
 *
 * @example
 * Basic usage:
 * ```typescript
 * const result = functionName(value1, value2);
 * console.log(result); // expected
 * ```
 *
 * @example
 * Edge case:
 * ```typescript
 * functionName(null, value2); // throws ValueError
 * ```
 */
function functionName(param1: Type1, param2: Type2): ReturnType {
```

### Class Template

```typescript
/**
 * Short one-line description of class.
 *
 * Longer description of the class purpose and behavior.
 * Include important usage notes.
 *
 * @example
 * ```typescript
 * const obj = new ClassName(param1, param2);
 * obj.method();
 * ```
 */
class ClassName {
  /** Description of property */
  property1: Type1;

  /** Description of property */
  property2: Type2;

  /**
   * Create a new ClassName instance.
   *
   * @param param1 - Description of first parameter
   * @param param2 - Description of second parameter
   */
  constructor(param1: Type1, param2: Type2) {
```

### Interface Template

```typescript
/**
 * Describes the shape of [concept].
 *
 * Used for [context/purpose].
 */
interface InterfaceName {
  /** Description of property */
  property1: Type1;

  /** Description of optional property */
  property2?: Type2;

  /**
   * Description of method.
   *
   * @param param - Description
   * @returns Description
   */
  methodName(param: Type): ReturnType;
}
```

---

## JavaScript (JSDoc Style)

### Function Template

```javascript
/**
 * Short one-line description of function.
 *
 * Longer description if needed.
 *
 * @param {Type1} param1 - Description of first parameter
 * @param {Type2} param2 - Description of second parameter
 * @returns {ReturnType} Description of what is returned
 * @throws {ErrorType} When this error occurs
 *
 * @example
 * const result = functionName(value1, value2);
 * // => expected
 */
function functionName(param1, param2) {
```

---

## Required Elements Checklist

Every public function/method must include:

- [ ] **Purpose** — One-line description of what it does
- [ ] **Parameters** — Each param with type and meaning
- [ ] **Returns** — What is returned and when
- [ ] **Side Effects** — State changes, I/O, mutations
- [ ] **Errors** — What exceptions can occur and why
- [ ] **Examples** — Realistic usage showing common cases

---

## Example: Complete Docstring

```python
def sell_item_to(self, item_id: str, buyer: Customer) -> Receipt:
    """Sell an item from shop inventory to a customer.

    Transfers ownership of the item from the shop to the buyer,
    processes payment, and updates inventory. This operation is
    atomic - if payment fails, inventory is not updated.

    Args:
        item_id: Unique identifier of the item to sell.
            Must exist in current inventory.
        buyer: Customer purchasing the item.
            Must have sufficient balance for the item price.

    Returns:
        Receipt containing:
        - transaction_id: Unique ID for this sale
        - item: The sold item details
        - amount: Price paid
        - timestamp: When the sale occurred

    Raises:
        ItemNotFoundError: If item_id doesn't exist in inventory.
        InsufficientBalanceError: If buyer.balance < item.price.
        ItemAlreadySoldError: If item was sold between check
            and purchase (race condition).
        PaymentProcessingError: If payment gateway fails.

    Side Effects:
        - Removes item from self.inventory
        - Debits buyer.balance by item.price
        - Credits self.revenue by item.price
        - Logs transaction to audit trail

    Examples:
        Basic sale:
        >>> shop = Shop(inventory=[item])
        >>> buyer = Customer(balance=100)
        >>> receipt = shop.sell_item_to(item.id, buyer)
        >>> assert receipt.amount == item.price
        >>> assert item.id not in shop.inventory
        >>> assert buyer.balance == 100 - item.price

        Handling insufficient balance:
        >>> poor_buyer = Customer(balance=0)
        >>> shop.sell_item_to(item.id, poor_buyer)
        Raises InsufficientBalanceError("Buyer balance 0 < item price 50")
    """
```

---

## When to Skip Docstrings

Docstrings may be omitted for:

- Private methods (prefix `_`) with obvious behavior
- Simple getters/setters
- Methods that override a documented parent method
- Test methods (the test name is the documentation)

**When in doubt, add the docstring.**
