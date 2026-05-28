# Testing Strategy

## Layered Testing

Implement multiple levels of testing for comprehensive coverage:

```
┌─────────────────────────────────────┐
│     End-to-End Tests (Few)         │  Slow, expensive, high confidence
├─────────────────────────────────────┤
│   Integration Tests (Some)          │  Medium speed/cost, medium confidence
├─────────────────────────────────────┤
│    Unit Tests (Many)                │  Fast, cheap, foundational
└─────────────────────────────────────┘
        Testing Pyramid
```

### Unit Tests

Test individual functions or classes in isolation.

**C++ with Google Test**:
```cpp
#include <gtest/gtest.h>

class Calculator {
public:
    int add(int a, int b) { return a + b; }
    int divide(int a, int b) {
        if (b == 0) throw std::invalid_argument("Division by zero");
        return a / b;
    }
};

TEST(CalculatorTest, Addition) {
    Calculator calc;
    EXPECT_EQ(calc.add(2, 3), 5);
    EXPECT_EQ(calc.add(-1, 1), 0);
}

TEST(CalculatorTest, DivisionByZero) {
    Calculator calc;
    EXPECT_THROW(calc.divide(10, 0), std::invalid_argument);
}

TEST(CalculatorTest, Division) {
    Calculator calc;
    EXPECT_EQ(calc.divide(10, 2), 5);
}
```

**Kotlin with JUnit**:
```kotlin
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.assertThrows
import kotlin.test.assertEquals

class CalculatorTest {
    private val calculator = Calculator()

    @Test
    fun `addition works correctly`() {
        assertEquals(5, calculator.add(2, 3))
        assertEquals(0, calculator.add(-1, 1))
    }

    @Test
    fun `division by zero throws exception`() {
        assertThrows<IllegalArgumentException> {
            calculator.divide(10, 0)
        }
    }

    @Test
    fun `division works correctly`() {
        assertEquals(5, calculator.divide(10, 2))
    }
}
```

**Python with pytest**:
```python
import pytest

class TestCalculator:
    def test_addition(self):
        calc = Calculator()
        assert calc.add(2, 3) == 5
        assert calc.add(-1, 1) == 0

    def test_division_by_zero(self):
        calc = Calculator()
        with pytest.raises(ValueError, match="Division by zero"):
            calc.divide(10, 0)

    def test_division(self):
        calc = Calculator()
        assert calc.divide(10, 2) == 5
```

### Integration Tests

Test interactions between components.

**Example: Database Integration**:
```cpp
class DatabaseIntegrationTest : public ::testing::Test {
protected:
    void SetUp() override {
        // Create test database
        db_ = std::make_unique<Database>("test.db");
        db_->initialize();
    }

    void TearDown() override {
        // Clean up test database
        db_.reset();
        std::remove("test.db");
    }

    std::unique_ptr<Database> db_;
};

TEST_F(DatabaseIntegrationTest, SaveAndRetrieveUser) {
    User user{"Alice", "alice@example.com"};

    // Save to database
    db_->save(user);

    // Retrieve from database
    auto retrieved = db_->findByEmail("alice@example.com");

    ASSERT_TRUE(retrieved.has_value());
    EXPECT_EQ(retrieved->name, "Alice");
    EXPECT_EQ(retrieved->email, "alice@example.com");
}
```

### Performance Tests

Verify performance requirements are met.

```cpp
#include <benchmark/benchmark.h>

static void BM_SortLargeArray(benchmark::State& state) {
    std::vector<int> data(state.range(0));
    std::generate(data.begin(), data.end(), std::rand);

    for (auto _ : state) {
        auto copy = data;
        std::sort(copy.begin(), copy.end());
    }
}

BENCHMARK(BM_SortLargeArray)->Range(1<<10, 1<<18);
```

## Test Fixtures

Manage test setup and cleanup efficiently.

### C++ Fixtures

```cpp
class UserManagerTest : public ::testing::Test {
protected:
    void SetUp() override {
        // Common setup for all tests
        manager_ = std::make_unique<UserManager>();
        testUser_ = User{"Test", "test@example.com"};
    }

    void TearDown() override {
        // Common cleanup
        manager_.reset();
    }

    std::unique_ptr<UserManager> manager_;
    User testUser_;
};

TEST_F(UserManagerTest, AddUser) {
    EXPECT_TRUE(manager_->add(testUser_));
    EXPECT_EQ(manager_->count(), 1);
}

TEST_F(UserManagerTest, RemoveUser) {
    manager_->add(testUser_);
    EXPECT_TRUE(manager_->remove(testUser_.email));
    EXPECT_EQ(manager_->count(), 0);
}
```

### Python Fixtures

```python
import pytest

@pytest.fixture
def user_manager():
    """Fixture that provides a clean UserManager for each test."""
    manager = UserManager()
    yield manager
    # Cleanup happens after test
    manager.close()

@pytest.fixture
def test_user():
    """Fixture that provides a test user."""
    return User(name="Test", email="test@example.com")

def test_add_user(user_manager, test_user):
    assert user_manager.add(test_user)
    assert user_manager.count() == 1

def test_remove_user(user_manager, test_user):
    user_manager.add(test_user)
    assert user_manager.remove(test_user.email)
    assert user_manager.count() == 0
```

### Kotlin Fixtures

```kotlin
class UserManagerTest {
    private lateinit var manager: UserManager
    private lateinit var testUser: User

    @BeforeEach
    fun setUp() {
        manager = UserManager()
        testUser = User("Test", "test@example.com")
    }

    @AfterEach
    fun tearDown() {
        manager.close()
    }

    @Test
    fun `adding user increases count`() {
        assertTrue(manager.add(testUser))
        assertEquals(1, manager.count())
    }
}
```

## Coverage Goals

### Target: 80% Code Coverage

Aim for at least **80% test coverage** across the codebase.

**Measure coverage**:

**C++ with lcov**:
```bash
# Compile with coverage flags
g++ -fprofile-arcs -ftest-coverage test.cpp -o test

# Run tests
./test

# Generate coverage report
lcov --capture --directory . --output-file coverage.info
genhtml coverage.info --output-directory coverage_report
```

**Python with pytest-cov**:
```bash
# Run tests with coverage
pytest --cov=mypackage --cov-report=html --cov-report=term

# View report
# HTML report in htmlcov/index.html
```

**Kotlin/Java with JaCoCo**:
```kotlin
// build.gradle.kts
plugins {
    jacoco
}

tasks.jacocoTestReport {
    reports {
        xml.required.set(true)
        html.required.set(true)
    }
}

tasks.test {
    finalizedBy(tasks.jacocoTestReport)
}
```

```bash
./gradlew test jacocoTestReport
# Report in build/reports/jacoco/test/html/index.html
```

### What to Cover

Priority for test coverage:

1. **Critical business logic** - 100% coverage required
2. **Public APIs** - All public functions/methods
3. **Error handling paths** - Exception cases
4. **Edge cases** - Boundary conditions
5. **Integration points** - External dependencies

What **not** to test extensively:

- Trivial getters/setters
- Framework/library code
- Generated code
- Simple data classes (unless they have logic)

## Edge Cases and Failure Scenarios

### Test Edge Cases

```cpp
TEST(StringProcessorTest, EdgeCases) {
    StringProcessor processor;

    // Empty input
    EXPECT_EQ(processor.process(""), "");

    // Very long input
    std::string longString(1000000, 'a');
    EXPECT_NO_THROW(processor.process(longString));

    // Special characters
    EXPECT_NO_THROW(processor.process("!@#$%^&*()"));

    // Unicode
    EXPECT_NO_THROW(processor.process("你好世界"));

    // Null characters
    std::string withNull = "Hello\0World";
    EXPECT_NO_THROW(processor.process(withNull));
}
```

### Test Failure Scenarios

```cpp
TEST(FileReaderTest, FailureScenarios) {
    FileReader reader;

    // File doesn't exist
    EXPECT_THROW(reader.open("nonexistent.txt"), FileNotFoundError);

    // Insufficient permissions
    EXPECT_THROW(reader.open("/root/restricted.txt"), PermissionError);

    // Disk full (mock scenario)
    MockFileSystem fs;
    fs.setDiskFull(true);
    EXPECT_THROW(reader.write("data"), DiskFullError);

    // Network timeout (for network readers)
    MockNetwork network;
    network.setLatency(std::chrono::seconds(100));
    EXPECT_THROW(reader.fetch("url"), TimeoutError);
}
```

### Parameterized Tests

Test multiple inputs efficiently:

**C++ with Google Test**:
```cpp
class PrimeNumberTest : public ::testing::TestWithParam<std::pair<int, bool>> {};

TEST_P(PrimeNumberTest, IsPrime) {
    auto [number, expectedResult] = GetParam();
    EXPECT_EQ(isPrime(number), expectedResult);
}

INSTANTIATE_TEST_SUITE_P(
    PrimeNumbers,
    PrimeNumberTest,
    ::testing::Values(
        std::make_pair(2, true),
        std::make_pair(3, true),
        std::make_pair(4, false),
        std::make_pair(17, true),
        std::make_pair(20, false)
    )
);
```

**Python with pytest**:
```python
@pytest.mark.parametrize("number,expected", [
    (2, True),
    (3, True),
    (4, False),
    (17, True),
    (20, False),
])
def test_is_prime(number, expected):
    assert is_prime(number) == expected
```

## Test Organization

### File Structure

```
project/
├── src/
│   ├── module1.cpp
│   └── module2.cpp
└── tests/
    ├── unit/
    │   ├── test_module1.cpp
    │   └── test_module2.cpp
    ├── integration/
    │   └── test_integration.cpp
    └── performance/
        └── benchmark_module1.cpp
```

### Naming Conventions

- **Test files**: `test_<module>.cpp`, `<Module>Test.kt`, `test_<module>.py`
- **Test cases**: Descriptive names that explain what's being tested
  - Good: `TEST(UserManager, AddingDuplicateUserReturnsFalse)`
  - Bad: `TEST(UserManager, Test1)`

### Test Independence

Each test should be independent:

```cpp
// ❌ Tests depend on each other
TEST(BadTest, Step1) {
    globalState = initializeState();
}

TEST(BadTest, Step2) {
    // Depends on Step1 running first
    processState(globalState);
}

// ✅ Tests are independent
TEST(GoodTest, Initialize) {
    auto state = initializeState();
    EXPECT_TRUE(state.isValid());
}

TEST(GoodTest, Process) {
    auto state = initializeState();  // Own setup
    processState(state);
    EXPECT_TRUE(state.isProcessed());
}
```

## Continuous Integration

### Run Tests Automatically

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Build
        run: cmake -B build && cmake --build build

      - name: Run unit tests
        run: cd build && ctest --output-on-failure

      - name: Generate coverage
        run: |
          cmake --build build --target coverage
          bash <(curl -s https://codecov.io/bash)
```

### Quality Gates

Fail the build if quality drops:

```yaml
- name: Check coverage threshold
  run: |
    coverage=$(pytest --cov=mypackage --cov-report=term | grep TOTAL | awk '{print $4}' | sed 's/%//')
    if [ "$coverage" -lt 80 ]; then
      echo "Coverage $coverage% is below 80% threshold"
      exit 1
    fi
```
