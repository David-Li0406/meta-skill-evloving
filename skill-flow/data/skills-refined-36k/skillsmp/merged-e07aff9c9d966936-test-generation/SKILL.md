---
name: test-generation
description: Use this skill to generate comprehensive unit and integration tests for code, ensuring quality and reliability across various functionalities.
---

# Test Generation Skill

## When to Use

Use this skill when:
- Creating unit tests for functions, methods, and classes
- Writing integration tests for full workflows
- Testing PDF extraction and document classification logic
- Validating database operations

## Testing Framework

Recommended approach:
- **Framework**: `pytest` (recommended for Python projects)
- **Test Location**: `tests/` directory
- **Naming**: `test_*.py` files
- **Coverage**: Aim for >80% coverage

## Key Functions to Test

### From `indexer.py`:
- `create_db()` - Database creation and schema
- `extract_text_from_pdf()` - PDF text extraction
- `classify_document()` - Document classification logic
- `index_files()` - Full indexing workflow

### From `search.py`:
- `search()` - Full-text search with filters

### From `organize.py`:
- `organize_documents()` - Document organization

## Test Organization

```
tests/
├── test_indexer.py      # Tests for indexer.py
├── test_search.py       # Tests for search.py
├── test_organize.py     # Tests for organize.py
└── fixtures/            # Test fixtures (sample PDFs)
```

## Capabilities

- Generate unit and integration tests for various code components
- Write tests that cover happy paths, edge cases, and error conditions
- Create test fixtures and mock objects
- Follow testing frameworks and conventions (Jest, pytest, JUnit, etc.)
- Write descriptive test names and clear assertions
- Ensure high test coverage while maintaining test quality

## Input

You receive:
- Code to test (functions, classes, modules)
- Testing framework preferences
- Existing test patterns and conventions
- Coverage requirements
- Edge cases and scenarios to test

## Output

You produce:
- Complete unit test suites
- Integration tests for workflows
- Test fixtures and setup/teardown code
- Mock objects and test doubles
- Test data and examples
- Test documentation and comments

## Instructions

1. **Analyze the Code**
   - Understand what the code does
   - Identify inputs, outputs, and side effects
   - Note dependencies and external interactions
   - Identify edge cases and error conditions

2. **Plan Test Coverage**
   - List all functions/methods to test
   - Identify test scenarios (happy path, edge cases, errors)
   - Determine what needs mocking
   - Plan test data and fixtures

3. **Write Tests**
   - Follow AAA pattern (Arrange, Act, Assert)
   - Use descriptive test names that explain what is tested
   - Test one thing per test case
   - Include both positive and negative test cases
   - Test edge cases (empty inputs, null values, boundary conditions)
   - Test error handling and exceptions

4. **Create Test Fixtures**
   - Set up test data and objects
   - Create reusable test helpers
   - Implement setup and teardown as needed

5. **Add Mocks and Stubs**
   - Mock external dependencies
   - Stub network calls and file I/O
   - Verify interactions when appropriate

## Common Test Scenarios

### PDF Extraction Tests
- Extract text from normal PDFs
- Fallback to OCR for scanned PDFs
- Handle corrupted PDFs gracefully
- Extract metadata correctly

### Classification Tests
- Classify documents correctly
- Extract contract numbers
- Identify addendums and attachments by number

### Database Tests
- Verify schema creation
- Test FTS5 index updates
- Validate triggers work
- Test query performance

### Error Handling Tests
- Missing PDF files
- Corrupted PDFs
- Database connection errors
- OCR failures

## Best Practices

- **Test Isolation**: Each test should be independent
- **Clear Names**: Test names should describe what they test
- **One Assertion**: Focus each test on one behavior
- **Fast Tests**: Keep tests fast and avoid I/O when possible
- **Maintainable**: Tests should be easy to read and update
- **Coverage**: Aim for high coverage but prioritize important paths

## Checklist

When writing tests:
- [ ] Test file created in `tests/` directory
- [ ] Test functions named `test_*`
- [ ] Edge cases covered
- [ ] Error cases tested
- [ ] Fixtures created for reusable data
- [ ] Assertions are clear and descriptive
- [ ] Integration tests for workflows
- [ ] Mock external dependencies appropriately