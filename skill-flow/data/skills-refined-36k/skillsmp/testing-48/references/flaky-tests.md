# Diagnosing and Fixing Flaky Tests

Flaky tests erode trust in your test suite. Fix or delete them.

## Common Causes

### 1. Race Conditions

```javascript
// ❌ Flaky: Timing dependent
test('updates state', async () => {
  component.click();
  expect(component.state).toBe('updated');  // Might not be updated yet
});

// ✅ Fixed: Wait for condition
test('updates state', async () => {
  component.click();
  await waitFor(() => expect(component.state).toBe('updated'));
});
```

### 2. Shared State

```python
# ❌ Flaky: Tests share database state
def test_create_user():
    create_user(email="test@example.com")
    assert get_user_count() == 1  # Fails if other test created user

# ✅ Fixed: Isolate test data
def test_create_user(clean_db):
    create_user(email="test@example.com")
    assert get_user_count() == 1
```

### 3. Time Dependencies

```javascript
// ❌ Flaky: Depends on wall clock
test('expires after 1 hour', () => {
  const token = createToken();
  const oneHourLater = new Date(Date.now() + 3600001);
  expect(isExpired(token, oneHourLater)).toBe(true);  // Midnight edge case?
});

// ✅ Fixed: Mock time
test('expires after 1 hour', () => {
  jest.useFakeTimers().setSystemTime(new Date('2024-01-01T12:00:00'));
  const token = createToken();
  jest.advanceTimersByTime(3600001);
  expect(isExpired(token)).toBe(true);
});
```

### 4. Order Dependencies

```python
# ❌ Flaky: Depends on test order
class TestUser:
    def test_create(self):
        self.user = create_user()  # Sets class attribute

    def test_delete(self):
        delete_user(self.user.id)  # Fails if test_create didn't run first

# ✅ Fixed: Independent tests
class TestUser:
    @pytest.fixture
    def user(self):
        return create_user()

    def test_create(self, user):
        assert user.id is not None

    def test_delete(self, user):
        delete_user(user.id)
```

### 5. Network Dependencies

```go
// ❌ Flaky: Depends on external service
func TestFetchUser(t *testing.T) {
    user, err := FetchUser("https://api.example.com/users/1")
    assert.NoError(t, err)  // Fails when API is slow/down
}

// ✅ Fixed: Mock HTTP
func TestFetchUser(t *testing.T) {
    server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(200)
        w.Write([]byte(`{"id": 1, "name": "Test"}`))
    }))
    defer server.Close()

    user, err := FetchUser(server.URL + "/users/1")
    assert.NoError(t, err)
}
```

## Debugging Strategies

### Run Tests in Isolation

```bash
# Run single test repeatedly
pytest tests/test_user.py::test_create -x --count=100

# Find order-dependent failures
pytest tests/ --random-order

# Find parallel failures
pytest tests/ -n auto
```

### Add Logging

```python
# Temporary debugging
def test_flaky():
    print(f"State before: {get_state()}")
    do_action()
    print(f"State after: {get_state()}")
    assert condition()
```

### Check for Timeouts

```javascript
// Increase timeout to see if it's just slow
test('slow operation', async () => {
  await slowOperation();
}, 30000);  // 30s timeout
```

## Prevention Checklist

- [ ] **Isolate tests** - Each test sets up and tears down own data
- [ ] **Mock time** - Never use real clocks
- [ ] **Mock network** - Never call real external services
- [ ] **Use waitFor/eventually** - Don't rely on timing
- [ ] **Random test order** - Run `--random-order` in CI
- [ ] **Retry flaky tests** - But track and fix root causes
- [ ] **Parallelize early** - Find hidden dependencies

## When to Delete

Delete the test if:
- Root cause can't be found after reasonable investigation
- Test provides little value
- Cost of maintenance exceeds benefit

Better: No test than a flaky test that trains developers to ignore failures.
