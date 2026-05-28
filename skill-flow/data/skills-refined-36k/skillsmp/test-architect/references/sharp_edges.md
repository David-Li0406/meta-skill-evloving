# Test Architect - Sharp Edges

## Test Database Not Isolated

### **Id**
test-database-not-isolated
### **Summary**
Tests share database, pass alone but fail together
### **Severity**
high
### **Situation**
Integration tests with real database
### **Why**
  Test A creates user with email "test@example.com".
  Test B also tries to create user with same email.
  Run separately: both pass. Run together: unique constraint violation.
  Order-dependent failures are maddening to debug.
  
### **Solution**
  1. Use unique identifiers per test:
     user_email = f"test_{uuid4().hex[:8]}@example.com"
  
  2. Truncate tables between tests:
     @pytest.fixture(autouse=True)
     async def clean_db(database):
         yield
         await database.execute("TRUNCATE users CASCADE")
  
  3. Use transactions that rollback:
     @pytest.fixture
     async def db_session(database):
         async with database.transaction() as tx:
             yield tx
             await tx.rollback()
  
  4. Separate database per test file (for parallelization):
     database_url = f"test_db_{os.getpid()}"
  
### **Symptoms**
  - Tests pass in isolation, fail in suite
  - Random test failures in CI
  - "Unique constraint violation" in test logs
### **Detection Pattern**
fixture.*scope.*session|shared.*database|@pytest.fixture.*scope

## Async Test Not Awaited

### **Id**
async-test-not-awaited
### **Summary**
Async assertions not awaited, test passes falsely
### **Severity**
critical
### **Situation**
Testing async Python code
### **Why**
  async def test_create(): assert create_memory() creates a coroutine, not a result.
  The assertion checks truthiness of coroutine object (always truthy).
  Test passes but nothing was actually tested.
  
### **Solution**
  1. Always await async calls:
     async def test_create():
         result = await create_memory()
         assert result.id is not None
  
  2. Use pytest-asyncio correctly:
     @pytest.mark.asyncio
     async def test_create():
         ...
  
  3. Enable warnings in pytest.ini:
     filterwarnings = error::RuntimeWarning
  
  4. Use linter rule to catch:
     # ruff: enable RUF006 (asyncio-dangling-task)
  
### **Symptoms**
  - Tests pass but functionality is broken
  - "coroutine was never awaited" warnings
  - Async tests complete instantly
### **Detection Pattern**
assert.*\(\)(?!.*await)|async def test.*(?!.*await)

## Mock Hides Real Bug

### **Id**
mock-hides-real-bug
### **Summary**
Over-mocking hides integration bugs
### **Severity**
medium
### **Situation**
Unit tests with many mocks
### **Why**
  You mock the database, mock the cache, mock the API.
  Test passes! But in production, the database returns different
  types, the cache has serialization issues, the API has pagination.
  Mocks encoded your assumptions, not reality.
  
### **Solution**
  1. Prefer fakes over mocks for complex dependencies:
     # Fake: in-memory implementation with real behavior
     class FakeMemoryStore:
         def __init__(self):
             self._data = {}
         async def get(self, id): return self._data.get(id)
         async def set(self, id, value): self._data[id] = value
  
  2. Mock at system boundaries, not internally:
     # Mock external API, not your own repository
  
  3. Use integration tests for component interactions:
     # Real database, real cache, mock only external services
  
  4. Contract tests verify mock accuracy:
     # Verify mocks match real service behavior
  
### **Symptoms**
  - Unit tests pass, integration tests fail
  - Works in test, fails in production
  - Tests don't catch obvious bugs
### **Detection Pattern**
mock.*mock.*mock|patch.*patch.*patch|@mock.patch

## Flaky Async Timing

### **Id**
flaky-async-timing
### **Summary**
Tests flaky due to timing assumptions
### **Severity**
high
### **Situation**
Testing async operations with sleeps
### **Why**
  await asyncio.sleep(0.1) # Wait for background task
  Works on your machine. CI is slower, task not done in 100ms.
  Test fails randomly. You increase to 500ms. Now tests are slow AND flaky.
  
### **Solution**
  1. Use condition waiting, not fixed sleeps:
     async def wait_for(condition, timeout=5.0):
         start = time.monotonic()
         while not condition():
             if time.monotonic() - start > timeout:
                 raise TimeoutError("Condition not met")
             await asyncio.sleep(0.01)
  
     await wait_for(lambda: task.is_complete)
  
  2. Return completable futures:
     task = await start_background_task()
     await task.wait()  # Explicit completion signal
  
  3. Use asyncio.wait_for with reasonable timeout:
     await asyncio.wait_for(operation(), timeout=5.0)
  
  4. For event-driven, use asyncio.Event:
     event = asyncio.Event()
     # Task sets event when done
     await asyncio.wait_for(event.wait(), timeout=5.0)
  
### **Symptoms**
  - Tests pass locally, fail in CI
  - Tests fail under high system load
  - Random timeouts in async tests
### **Detection Pattern**
sleep\(|time\.sleep|asyncio\.sleep.*0\.

## Test Data Not Representative

### **Id**
test-data-not-representative
### **Summary**
Test data too simple, misses real-world edge cases
### **Severity**
medium
### **Situation**
Testing with hardcoded sample data
### **Why**
  Test uses {"name": "John"}. Works great.
  Production gets {"name": "José María García-López"}.
  Encoding issues, length limits, regex failures.
  Your tests only tested the happy path.
  
### **Solution**
  1. Use property-based testing for data variety:
     @given(st.text())
     def test_handles_any_name(name):
         result = process_name(name)
         assert result is not None
  
  2. Include edge cases explicitly:
     @pytest.mark.parametrize("name", [
         "John",
         "José María García-López",
         "李明",
         "",
         "A" * 1000,
         "John\x00Doe",  # Null byte
         "<script>alert(1)</script>",
     ])
  
  3. Use faker for realistic variety:
     from faker import Faker
     fake = Faker(['en_US', 'zh_CN', 'es_ES'])
     name = fake.name()
  
  4. Snapshot production data (anonymized) for tests
  
### **Symptoms**
  - Tests pass, production fails on real data
  - Edge cases discovered by users
  - Encoding/length errors in production
### **Detection Pattern**
test.*John|test.*example\.com|hardcoded.*test

## Missing Cleanup Leaks Resources

### **Id**
missing-cleanup-leaks-resources
### **Summary**
Test creates resources but doesn't clean up
### **Severity**
medium
### **Situation**
Tests that create files, connections, or external resources
### **Why**
  Each test creates temp file. 1000 tests = 1000 files.
  Disk fills up. Or tests create database connections without closing.
  Connection pool exhausted. CI hangs.
  
### **Solution**
  1. Use context managers and fixtures:
     @pytest.fixture
     def temp_file():
         path = tempfile.mktemp()
         yield path
         os.unlink(path)  # Always runs
  
  2. Use try/finally in tests:
     async def test_connection():
         conn = await create_connection()
         try:
             # test logic
         finally:
             await conn.close()
  
  3. Use pytest-asyncio's event loop cleanup:
     @pytest.fixture(scope="function")
     async def client():
         client = AsyncClient()
         yield client
         await client.aclose()
  
  4. Monitor resource usage in CI:
     pytest --resource-monitor
  
### **Symptoms**
  - CI runs slower over time
  - "Too many open files" errors
  - Tests hang waiting for resources
### **Detection Pattern**
tempfile|open\(|create.*connection

## Snapshot Test Brittleness

### **Id**
snapshot-test-brittleness
### **Summary**
Snapshot tests break on irrelevant changes
### **Severity**
medium
### **Situation**
Using snapshot testing for complex outputs
### **Why**
  Snapshot test captures entire JSON response.
  Someone adds new optional field. 50 snapshots break.
  Reviewer auto-approves updates. Actual bugs slip through.
  
### **Solution**
  1. Snapshot only stable parts:
     snapshot.assert_match(
         result.to_dict(exclude=['created_at', 'request_id'])
     )
  
  2. Use targeted assertions instead:
     assert result.status == "success"
     assert len(result.items) == 3
  
  3. Normalize variable data:
     snapshot.assert_match(
         normalize_timestamps(result)
     )
  
  4. Review snapshot diffs carefully:
     # Don't auto-approve, understand what changed
  
### **Symptoms**
  - Snapshot tests break on unrelated changes
  - Developers auto-update without reviewing
  - Real bugs hidden in noise of snapshot updates
### **Detection Pattern**
snapshot|assert_match|toMatchSnapshot

## Ci Only Failures Hard To Debug

### **Id**
ci-only-failures-hard-to-debug
### **Summary**
Tests fail only in CI, impossible to reproduce locally
### **Severity**
high
### **Situation**
Tests passing locally but failing in CI
### **Why**
  Your machine: 16 cores, 32GB RAM, SSD, single test run.
  CI: 2 cores, 4GB RAM, shared disk, parallel tests.
  Timing, resource limits, parallelism all different.
  
### **Solution**
  1. Run tests in Docker locally:
     docker run --cpus=2 --memory=4g pytest
  
  2. Run tests in parallel locally:
     pytest -n auto  # Same as CI
  
  3. Add CI-like constraints:
     pytest --timeout=30  # Fail slow tests
  
  4. Log extensively on failure:
     @pytest.hookimpl(hookwrapper=True)
     def pytest_runtest_makereport(item, call):
         outcome = yield
         if call.excinfo:
             log_debug_info(item)
  
  5. Use CI debug mode:
     # GitHub Actions: re-run with debug logging
  
### **Symptoms**
  - "Works on my machine"
  - CI failures not reproducible
  - Tests timeout only in CI
### **Detection Pattern**
CI|github.*actions|gitlab.*ci