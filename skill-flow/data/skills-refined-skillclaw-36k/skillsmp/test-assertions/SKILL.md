---
name: test-assertions
description: 'Write effective test assertions with clear error messages, null safety, and proper validation. Use when asked to "write assertions", "validate test results", "check conditions", "test expectations", or when writing any type of automated test. Applicable to Terraform, JavaScript, Python, Go, and other testing frameworks.'
---

# Test Assertions

Write clear, effective test assertions that validate behavior and provide helpful feedback when tests fail.

## When to Use This Skill

- User asks to "write assertions", "add test validation", "check conditions"
- Writing unit, integration, or end-to-end tests
- Validating test outcomes and expectations
- Testing error conditions and edge cases
- Ensuring test failures are easy to debug
- Writing negative tests (expect failures)

## Assertion Fundamentals

### Basic Structure

**Pattern:**
```
assert <condition> with <helpful error message>
```

**Terraform:**
```hcl
assert {
  condition     = aws_s3_bucket.bucket.bucket == "expected-name"
  error_message = "S3 bucket name did not match expected value"
}
```

**JavaScript (Jest):**
```javascript
expect(bucket.name).toBe('expected-name'); // Error: Expected: expected-name, Received: actual-name
```

**Python (pytest):**
```python
assert bucket.name == 'expected-name', "S3 bucket name did not match expected value"
```

**Go:**
```go
assert.Equal(t, "expected-name", bucket.Name, "S3 bucket name did not match expected value")
```

## Error Message Best Practices

### 1. Include Actual Values

**❌ Bad - No context:**
```hcl
assert {
  condition     = length(local.parsers) == 5
  error_message = "Wrong number of parsers"
}
```

**✅ Good - Shows actual value:**
```hcl
assert {
  condition     = length(local.parsers) == 5
  error_message = "Expected 5 parsers, got ${length(local.parsers)}"
}
```

**JavaScript:**
```javascript
// ✅ Jest automatically shows both values
expect(parsers.length).toBe(5);
// Output: Expected: 5, Received: 3
```

**Python:**
```python
# ❌ Bad
assert len(parsers) == 5, "Wrong count"

# ✅ Good - Include actual value
assert len(parsers) == 5, f"Expected 5 parsers, got {len(parsers)}"
```

### 2. Explain Expected Behavior

**❌ Bad - States the obvious:**
```hcl
assert {
  condition     = var.enabled == true
  error_message = "enabled is not true"
}
```

**✅ Good - Explains why:**
```hcl
assert {
  condition     = var.enabled == true
  error_message = "Module must be enabled to create resources"
}
```

**JavaScript:**
```javascript
// ✅ Custom message explains why
expect(module.enabled).toBe(true); // Use .toBe() for clarity
```

### 3. Reference External Documentation

**Terraform:**
```hcl
assert {
  condition     = contains(["ECSServiceAverageCPUUtilization", "ALBRequestCountPerTarget"], var.metric_type)
  error_message = "Invalid metric type. See https://docs.aws.amazon.com/autoscaling/application/APIReference/API_PredefinedMetricSpecification.html"
}
```

**JavaScript:**
```javascript
expect(['CPU', 'Memory'].includes(metricType))
  .toBe(true)
  .toThrow('Invalid metric. See AWS docs: https://...');
```

## Assertion Types

### 1. Equality Assertions

**Strict Equality:**
```javascript
// JavaScript
expect(value).toBe(expected);           // ===
expect(value).toStrictEqual(expected);  // Deep equality

// Python
assert value == expected
assert value is expected  # Identity check

// Go
assert.Equal(t, expected, value)
assert.Same(t, expected, value)  // Pointer equality
```

**Terraform:**
```hcl
assert {
  condition     = aws_s3_bucket.bucket.bucket == "expected"
  error_message = "Bucket name mismatch"
}
```

### 2. Truthiness Assertions

**JavaScript:**
```javascript
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeNull();
expect(value).toBeUndefined();
expect(value).toBeDefined();
```

**Python:**
```python
assert value
assert not value
assert value is None
assert value is not None
```

**Terraform:**
```hcl
assert {
  condition     = var.value != null
  error_message = "Value must not be null"
}
```

### 3. Comparison Assertions

**JavaScript:**
```javascript
expect(value).toBeGreaterThan(10);
expect(value).toBeGreaterThanOrEqual(10);
expect(value).toBeLessThan(100);
expect(value).toBeLessThanOrEqual(100);
```

**Python:**
```python
assert value > 10
assert value >= 10
assert value < 100
assert 10 <= value <= 100  # Range check
```

**Terraform:**
```hcl
assert {
  condition     = var.cpu >= 256 && var.cpu <= 16384
  error_message = "CPU must be between 256 and 16384"
}
```

### 4. Collection Assertions

**Contains:**
```javascript
// JavaScript
expect(array).toContain(item);
expect(array).toContainEqual({ id: 1 });
expect(string).toContain('substring');

// Python
assert item in array
assert 'substring' in string
assert {'id': 1} in array

// Terraform
assert {
  condition     = contains(var.allowed_values, var.value)
  error_message = "Value not in allowed list"
}
```

**Length:**
```javascript
// JavaScript
expect(array).toHaveLength(5);

// Python
assert len(array) == 5

// Terraform
assert {
  condition     = length(var.list) == 5
  error_message = "Expected 5 items"
}
```

**Empty:**
```javascript
// JavaScript
expect(array).toHaveLength(0);
expect(object).toEqual({});

// Python
assert not array  # Empty list is falsy
assert array == []
assert dict == {}
```

### 5. Type Assertions

**JavaScript:**
```javascript
expect(typeof value).toBe('string');
expect(value).toBeInstanceOf(Array);
expect(Array.isArray(value)).toBe(true);
```

**Python:**
```python
assert isinstance(value, str)
assert isinstance(value, list)
assert type(value) == str
```

**Terraform:**
```hcl
assert {
  condition     = can(regex("^arn:aws:", var.arn))
  error_message = "Value must be a valid ARN"
}
```

### 6. Pattern/Regex Assertions

**JavaScript:**
```javascript
expect(string).toMatch(/pattern/);
expect(string).toMatch(/^arn:aws:/);
```

**Python:**
```python
import re
assert re.match(r'^arn:aws:', string)
```

**Terraform:**
```hcl
assert {
  condition     = can(regex("^[a-z0-9-]+$", var.name))
  error_message = "Name must contain only lowercase letters, numbers, and hyphens"
}
```

### 7. Exception/Error Assertions

**JavaScript:**
```javascript
expect(() => {
  throwError();
}).toThrow();

expect(() => {
  throwError();
}).toThrow('Specific error message');

expect(() => {
  throwError();
}).toThrow(CustomError);
```

**Python:**
```python
import pytest

with pytest.raises(ValueError):
    raise_error()

with pytest.raises(ValueError, match="specific message"):
    raise_error()
```

**Terraform (expect_failures):**
```hcl
run "test_validation_fails" {
  command = plan

  variables {
    invalid_value = "wrong"
  }

  expect_failures = [
    var.input,
  ]
}
```

## Null Safety

### Terraform Null Safety

**Use try() for potentially null values:**
```hcl
assert {
  condition     = try(aws_s3_bucket.bucket.lifecycle_rule[0].enabled, false) == true
  error_message = "Lifecycle rule should be enabled"
}
```

**Check existence first:**
```hcl
assert {
  condition     = aws_s3_bucket.bucket.logging != null
  error_message = "Logging configuration is missing"
}
```

**Use can() to check if operation succeeds:**
```hcl
assert {
  condition     = can(regex("^arn:", var.arn))
  error_message = "Invalid ARN format"
}
```

### JavaScript Null Safety

**Optional chaining:**
```javascript
expect(bucket?.logging?.enabled).toBe(true);
```

**Nullish coalescing:**
```javascript
expect(bucket.logging ?? {}).toEqual({ enabled: true });
```

**Explicit checks:**
```javascript
expect(bucket.logging).toBeDefined();
expect(bucket.logging.enabled).toBe(true);
```

### Python Null Safety

**Check for None:**
```python
assert bucket.logging is not None
assert bucket.logging.enabled is True
```

**Use get() with default:**
```python
assert bucket.get('logging', {}).get('enabled') is True
```

## Multiple Assertions

### Group Related Assertions

**✅ Good - Related conditions in same test:**
```hcl
run "validate_s3_configuration" {
  assert {
    condition     = aws_s3_bucket.bucket.bucket == "test-bucket"
    error_message = "Invalid bucket name"
  }

  assert {
    condition     = aws_s3_bucket.bucket.versioning[0].enabled == true
    error_message = "Versioning should be enabled"
  }

  assert {
    condition     = aws_s3_bucket.bucket.server_side_encryption_configuration != null
    error_message = "Encryption should be configured"
  }
}
```

**JavaScript:**
```javascript
test('validate S3 configuration', () => {
  expect(bucket.name).toBe('test-bucket');
  expect(bucket.versioning.enabled).toBe(true);
  expect(bucket.encryption).toBeDefined();
});
```

### Separate Unrelated Assertions

**✅ Better - Separate concerns:**
```javascript
test('bucket has correct name', () => {
  expect(bucket.name).toBe('test-bucket');
});

test('bucket has versioning enabled', () => {
  expect(bucket.versioning.enabled).toBe(true);
});

test('bucket has encryption configured', () => {
  expect(bucket.encryption).toBeDefined();
});
```

## Advanced Assertion Patterns

### 1. Complex Object Matching

**JavaScript:**
```javascript
expect(user).toMatchObject({
  id: expect.any(Number),
  email: expect.stringContaining('@'),
  createdAt: expect.any(Date)
});
```

**Terraform:**
```hcl
assert {
  condition     = alltrue([
    contains(keys(local.user), "id"),
    contains(keys(local.user), "email"),
    can(regex("@", local.user.email))
  ])
  error_message = "User object structure invalid"
}
```

### 2. Collection Element Validation

**Terraform - All elements match:**
```hcl
assert {
  condition     = alltrue([
    for parser in local.parsers :
    contains(keys(parser), "name")
  ])
  error_message = "All parsers must have name field"
}
```

**JavaScript:**
```javascript
expect(parsers.every(p => 'name' in p)).toBe(true);
```

**Python:**
```python
assert all('name' in p for p in parsers)
```

### 3. Conditional Validation

**Terraform:**
```hcl
assert {
  condition     = var.enable_logging ? aws_s3_bucket.logs != null : true
  error_message = "Logging bucket required when enable_logging is true"
}
```

**JavaScript:**
```javascript
if (config.enableLogging) {
  expect(logsBucket).toBeDefined();
}
```

### 4. Range Validation

**Terraform:**
```hcl
assert {
  condition     = var.cpu >= 256 && var.cpu <= 16384 && var.cpu % 256 == 0
  error_message = "CPU must be between 256 and 16384 in increments of 256"
}
```

**Python:**
```python
assert 256 <= cpu <= 16384, f"CPU {cpu} out of range"
assert cpu % 256 == 0, f"CPU {cpu} must be multiple of 256"
```

### 5. Uniqueness Validation

**Terraform:**
```hcl
assert {
  condition     = length([for p in local.parsers : p.name]) == length(toset([for p in local.parsers : p.name]))
  error_message = "All parser names must be unique"
}
```

**JavaScript:**
```javascript
const names = parsers.map(p => p.name);
expect(new Set(names).size).toBe(names.length);
```

**Python:**
```python
names = [p['name'] for p in parsers]
assert len(names) == len(set(names)), "Parser names must be unique"
```

## Negative Testing (Expect Failures)

### Test That Validation Works

**Terraform:**
```hcl
# Test valid value passes
run "valid_environment" {
  variables {
    environment = "dev"
  }
  # Should succeed
}

# Test invalid value fails
run "invalid_environment" {
  command = plan

  variables {
    environment = "invalid"
  }

  expect_failures = [
    var.environment,
  ]
}
```

**JavaScript:**
```javascript
test('throws error for invalid environment', () => {
  expect(() => {
    validateEnvironment('invalid');
  }).toThrow('Environment must be dev, staging, or prod');
});
```

**Python:**
```python
def test_invalid_environment():
    with pytest.raises(ValueError, match="Environment must be"):
        validate_environment('invalid')
```

### Test Preconditions

**Terraform:**
```hcl
run "test_precondition_fails" {
  command = plan

  variables {
    instance_type = "t1.micro"  # Deprecated
  }

  expect_failures = [
    aws_instance.web,
  ]
}
```

## Assertion Anti-Patterns

### ❌ Testing Implementation Instead of Behavior

```javascript
// Bad - tests implementation
expect(service.cache.get).toHaveBeenCalled();

// Good - tests outcome
expect(result).toBe('cached-value');
```

### ❌ Vague Error Messages

```hcl
# Bad
assert {
  condition     = local.value == "expected"
  error_message = "Test failed"
}

# Good
assert {
  condition     = local.value == "expected"
  error_message = "Value should be 'expected' for proper configuration"
}
```

### ❌ Testing Multiple Unrelated Things

```javascript
// Bad - failure doesn't indicate what's wrong
test('everything works', () => {
  expect(bucket.name).toBe('test');
  expect(user.email).toBe('test@example.com');
  expect(lambda.runtime).toBe('nodejs18.x');
});

// Good - separate concerns
test('bucket has correct name', () => {
  expect(bucket.name).toBe('test');
});
```

### ❌ Brittle Assertions

```javascript
// Bad - breaks with any change
expect(result).toEqual({
  id: 1,
  name: 'John',
  email: 'john@example.com',
  createdAt: '2024-01-15T10:30:00Z',
  updatedAt: '2024-01-15T10:30:00Z',
  // ... 20 more fields
});

// Good - test what matters
expect(result).toMatchObject({
  id: expect.any(Number),
  name: 'John',
  email: expect.stringContaining('@')
});
```

## Framework-Specific Matchers

### Jest Matchers

```javascript
// Truthiness
expect(value).toBeTruthy();
expect(value).toBeFalsy();
expect(value).toBeNull();
expect(value).toBeUndefined();

// Numbers
expect(value).toBeGreaterThan(10);
expect(value).toBeCloseTo(0.3); // Floating point

// Strings
expect(string).toMatch(/pattern/);
expect(string).toContain('substring');

// Arrays/Iterables
expect(array).toContain(item);
expect(array).toHaveLength(3);

// Objects
expect(object).toHaveProperty('key');
expect(object).toMatchObject({ key: 'value' });

// Exceptions
expect(() => fn()).toThrow();
expect(promise).rejects.toThrow();

// Async
await expect(promise).resolves.toBe('value');
```

### Pytest Assertions

```python
# Basic
assert expression
assert expression, "error message"

# Approximation
assert value == pytest.approx(0.3)

# Exceptions
with pytest.raises(ValueError):
    raise_error()

with pytest.raises(ValueError, match="pattern"):
    raise_error()

# Warnings
with pytest.warns(UserWarning):
    trigger_warning()
```

### Go testify/assert

```go
import "github.com/stretchr/testify/assert"

// Equality
assert.Equal(t, expected, actual)
assert.NotEqual(t, expected, actual)

// Truthiness
assert.True(t, value)
assert.False(t, value)
assert.Nil(t, value)
assert.NotNil(t, value)

// Strings
assert.Contains(t, "hello world", "hello")
assert.Regexp(t, regexp.MustCompile("^[a-z]+$"), value)

// Collections
assert.Len(t, array, 5)
assert.Contains(t, array, item)
assert.ElementsMatch(t, expected, actual)

// Panics
assert.Panics(t, func() { panic("error") })
assert.NotPanics(t, func() { /* safe code */ })
```

## Best Practices Summary

### Do's

✅ **Include actual values in error messages**
✅ **Explain expected behavior, not just condition**
✅ **Test one concern per assertion when possible**
✅ **Use framework-specific matchers for clarity**
✅ **Write negative tests for validation**
✅ **Handle null/undefined safely**
✅ **Group related assertions logically**
✅ **Test behavior, not implementation**

### Don'ts

❌ **Don't write vague error messages**
❌ **Don't test unrelated things together**
❌ **Don't make assertions too brittle**
❌ **Don't test implementation details**
❌ **Don't ignore null safety**
❌ **Don't duplicate test logic in assertions**
❌ **Don't test what you've mocked**

## References

- **Jest Expect**: <https://jestjs.io/docs/expect>
- **Pytest Assertions**: <https://docs.pytest.org/en/stable/how-to/assert.html>
- **Go Testify**: <https://github.com/stretchr/testify>
- **Terraform Assertions**: <https://developer.hashicorp.com/terraform/language/tests#expect_failures>
- **Test Mocking**: Use the **test-mocking** skill for mocking patterns
- **Test Organization**: Use the **test-organization-patterns** skill for test structure
