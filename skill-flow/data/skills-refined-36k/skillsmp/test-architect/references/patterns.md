# Test Architect

## Patterns


---
  #### **Name**
Test Pyramid Design
  #### **Description**
Right balance of unit, integration, and e2e tests
  #### **When**
Designing test strategy for any project
  #### **Example**
    # Test Pyramid for AI Memory Service
    
    # Layer 1: Unit Tests (70% of tests)
    # - Fast (< 1ms each)
    # - No I/O, no database, no network
    # - Mock external dependencies
    # - Run on every commit
    
    # tests/unit/test_memory_scoring.py
    import pytest
    from mind.memory import calculate_salience
    
    class TestSalienceCalculation:
        """Unit tests for memory salience scoring."""
    
        def test_recent_memory_scores_higher(self):
            recent = calculate_salience(age_hours=1, access_count=1)
            old = calculate_salience(age_hours=720, access_count=1)
            assert recent > old
    
        def test_frequently_accessed_scores_higher(self):
            frequent = calculate_salience(age_hours=24, access_count=10)
            rare = calculate_salience(age_hours=24, access_count=1)
            assert frequent > rare
    
        @pytest.mark.parametrize("age,count,expected_range", [
            (0, 1, (0.9, 1.0)),
            (24, 5, (0.6, 0.8)),
            (720, 1, (0.1, 0.3)),
        ])
        def test_salience_ranges(self, age, count, expected_range):
            score = calculate_salience(age_hours=age, access_count=count)
            assert expected_range[0] <= score <= expected_range[1]
    
    # Layer 2: Integration Tests (20% of tests)
    # - Test component interactions
    # - Real database (test instance)
    # - Mock external services
    # - Run on PR merge
    
    # tests/integration/test_memory_repository.py
    import pytest
    from mind.repository import MemoryRepository
    
    @pytest.fixture
    async def repository(test_database):
        repo = MemoryRepository(test_database)
        yield repo
        await repo.clear_test_data()
    
    class TestMemoryRepository:
        """Integration tests for memory storage."""
    
        async def test_create_and_retrieve(self, repository):
            memory = await repository.create(
                content="Test memory",
                agent_id="agent_123"
            )
    
            retrieved = await repository.get(memory.id)
            assert retrieved.content == "Test memory"
    
        async def test_search_by_embedding(self, repository):
            # Uses real vector search
            memories = await repository.search_similar(
                embedding=[0.1] * 1536,
                limit=10
            )
            assert len(memories) <= 10
    
    # Layer 3: E2E Tests (10% of tests)
    # - Full system, real services
    # - User journey focused
    # - Run nightly or pre-release
    
    # tests/e2e/test_memory_workflow.py
    class TestMemoryWorkflow:
        """End-to-end memory lifecycle tests."""
    
        async def test_complete_memory_lifecycle(self, api_client):
            # Create memory via API
            response = await api_client.post("/memories", json={
                "content": "User prefers dark mode"
            })
            memory_id = response.json()["id"]
    
            # Retrieve and verify
            response = await api_client.get(f"/memories/{memory_id}")
            assert response.json()["content"] == "User prefers dark mode"
    
            # Consolidate and check
            await api_client.post(f"/memories/{memory_id}/consolidate")
            response = await api_client.get(f"/memories/{memory_id}")
            assert response.json()["consolidated"] is True
    

---
  #### **Name**
Property-Based Testing
  #### **Description**
Testing with generated inputs to find edge cases
  #### **When**
Complex logic, data transformations, parsers
  #### **Example**
    from hypothesis import given, strategies as st, assume
    import pytest
    
    # Property: encoding then decoding returns original
    @given(st.text())
    def test_roundtrip_encoding(text):
        encoded = encode_memory(text)
        decoded = decode_memory(encoded)
        assert decoded == text
    
    # Property: salience is always in valid range
    @given(
        age_hours=st.floats(min_value=0, max_value=10000),
        access_count=st.integers(min_value=0, max_value=1000)
    )
    def test_salience_always_valid(age_hours, access_count):
        score = calculate_salience(age_hours, access_count)
        assert 0.0 <= score <= 1.0
    
    # Property: search results are sorted by relevance
    @given(st.lists(st.floats(min_value=0, max_value=1), min_size=2))
    def test_search_results_sorted(scores):
        results = sort_by_relevance(scores)
        for i in range(len(results) - 1):
            assert results[i] >= results[i + 1]
    
    # Property: no duplicate IDs in results
    @given(st.lists(st.text(min_size=1), min_size=0, max_size=100))
    def test_no_duplicate_ids(items):
        result = process_items(items)
        ids = [r.id for r in result]
        assert len(ids) == len(set(ids))
    
    # Stateful testing for complex interactions
    from hypothesis.stateful import RuleBasedStateMachine, rule
    
    class MemoryStoreStateMachine(RuleBasedStateMachine):
        def __init__(self):
            super().__init__()
            self.store = MemoryStore()
            self.model = {}  # Simple dict as model
    
        @rule(key=st.text(), value=st.text())
        def add_memory(self, key, value):
            self.store.add(key, value)
            self.model[key] = value
    
        @rule(key=st.text())
        def get_memory(self, key):
            actual = self.store.get(key)
            expected = self.model.get(key)
            assert actual == expected
    
    TestMemoryStore = MemoryStoreStateMachine.TestCase
    

---
  #### **Name**
Test Isolation and Fixtures
  #### **Description**
Proper test isolation to prevent flakiness
  #### **When**
Setting up test infrastructure
  #### **Example**
    import pytest
    import asyncio
    from uuid import uuid4
    
    # Scope: function = new for each test
    # Scope: class = shared within test class
    # Scope: module = shared within file
    # Scope: session = shared across all tests
    
    @pytest.fixture(scope="session")
    def event_loop():
        """Create event loop for async tests."""
        loop = asyncio.new_event_loop()
        yield loop
        loop.close()
    
    @pytest.fixture(scope="session")
    async def database():
        """Session-scoped database for performance."""
        db = await create_test_database()
        await db.migrate()
        yield db
        await db.drop()
    
    @pytest.fixture(scope="function")
    async def clean_db(database):
        """Function-scoped cleanup for isolation."""
        yield database
        await database.truncate_all()
    
    @pytest.fixture
    def unique_agent_id():
        """Generate unique ID for test isolation."""
        return f"test_agent_{uuid4().hex[:8]}"
    
    @pytest.fixture
    async def test_memory(clean_db, unique_agent_id):
        """Create isolated test memory."""
        memory = await clean_db.memories.create(
            content="Test memory",
            agent_id=unique_agent_id
        )
        yield memory
        # Cleanup happens in clean_db fixture
    
    # Using fixtures for isolation
    class TestMemoryOperations:
        async def test_update_memory(self, test_memory, clean_db):
            # test_memory is unique to this test
            # clean_db ensures no cross-test pollution
            await clean_db.memories.update(
                test_memory.id,
                content="Updated"
            )
            updated = await clean_db.memories.get(test_memory.id)
            assert updated.content == "Updated"
    
        async def test_delete_memory(self, test_memory, clean_db):
            # Fresh test_memory, clean state
            await clean_db.memories.delete(test_memory.id)
            result = await clean_db.memories.get(test_memory.id)
            assert result is None
    

---
  #### **Name**
Contract Testing
  #### **Description**
Testing API contracts between services
  #### **When**
Microservices or API boundaries
  #### **Example**
    # Consumer-driven contract testing with Pact
    
    # Consumer side: what do I expect from the provider?
    # tests/contract/test_memory_api_consumer.py
    import pytest
    from pact import Consumer, Provider
    
    @pytest.fixture(scope="session")
    def pact():
        pact = Consumer('MemoryClient').has_pact_with(
            Provider('MemoryAPI'),
            pact_dir='./pacts'
        )
        pact.start_service()
        yield pact
        pact.stop_service()
        pact.publish_to_broker()
    
    def test_get_memory_contract(pact):
        expected = {
            "id": "mem_123",
            "content": "User prefers dark mode",
            "salience": 0.8
        }
    
        (pact
            .given("a memory with id mem_123 exists")
            .upon_receiving("a request for memory mem_123")
            .with_request("GET", "/memories/mem_123")
            .will_respond_with(200, body=expected))
    
        with pact:
            client = MemoryClient(pact.uri)
            memory = client.get("mem_123")
            assert memory.content == "User prefers dark mode"
    
    # Provider side: do I fulfill the contracts?
    # tests/contract/test_memory_api_provider.py
    from pact import Verifier
    
    def test_provider_fulfills_contracts():
        verifier = Verifier(
            provider='MemoryAPI',
            provider_base_url='http://localhost:8000'
        )
    
        output, _ = verifier.verify_pacts(
            './pacts/memory_client-memory_api.json',
            provider_states_setup_url='http://localhost:8000/_pact/setup'
        )
        assert output == 0
    

## Anti-Patterns


---
  #### **Name**
Testing Implementation Details
  #### **Description**
Tests that break when refactoring internal code
  #### **Why**
You can't refactor safely. Every internal change breaks tests that still work.
  #### **Instead**
Test behavior and outputs, not how code achieves them

---
  #### **Name**
Shared Mutable State
  #### **Description**
Tests that depend on order or share state
  #### **Why**
Tests pass alone, fail together. Debugging is nightmare.
  #### **Instead**
Isolate tests with fixtures, unique data, cleanup

---
  #### **Name**
Slow Test Suite
  #### **Description**
Unit tests taking minutes to run
  #### **Why**
Developers skip tests, push without running, CI becomes bottleneck.
  #### **Instead**
Unit tests < 1ms each, integration tests parallel, e2e minimal

---
  #### **Name**
Flaky Tests Ignored
  #### **Description**
Oh that test sometimes fails, just re-run
  #### **Why**
Team learns to ignore failures. Real bugs slip through.
  #### **Instead**
Fix or delete flaky tests immediately. Zero tolerance.

---
  #### **Name**
100% Coverage Goal
  #### **Description**
Adding tests just to hit coverage number
  #### **Why**
Coverage measures lines executed, not correctness. Useless tests.
  #### **Instead**
Focus on behavior coverage, critical paths, edge cases