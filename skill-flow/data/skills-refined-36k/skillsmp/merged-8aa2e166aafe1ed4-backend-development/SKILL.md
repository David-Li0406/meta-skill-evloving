---
name: backend-development
description: Use this skill when you need to create test code or add packages in a Python/FastAPI backend project.
---

# Backend Development Skills

This skill provides guidelines and procedures for generating test code and adding packages in a Python/FastAPI backend project.

## Test Code Creation

This section outlines the approach for implementing test code, including unit tests, integration tests, and end-to-end tests.

### Implementation Principles

- Focus on manageable coverage rather than exhaustive testing.
- Prioritize normal cases in tests while limiting abnormal cases to the essentials.
- Avoid excessive quality demands for solo development.
- Do not implement tests that are primarily mocks for external APIs.
- **Data Creation via API**: Use API endpoints for test data creation (do not insert directly into the database).
  - Use `create_transaction` fixture for transactions.
  - Use `create_dividend` fixture for dividends.
- Actively utilize common fixtures defined in `conftest.py`.
- Add reusable setup logic to `conftest.py` for multiple tests.

### Database and Transactions

- Each test runs in an independent PostgreSQL database (using testcontainers).
- The `db_session` fixture operates within a transaction and automatically rolls back after tests.
- Use a template database for faster initialization.
- Create and commit users in a separate session when obtaining authentication tokens.

### Authentication

- General User: Use `auth_token` fixture (username: "testuser").
- Admin User: Use `auth_admin_token` fixture (username: "adminuser").
- Include `headers={"Authorization": f"Bearer {auth_token}"}` in API requests.

### Mocking External APIs

- The `mock_external_apis` fixture is automatically applied to all tests (autouse=True).
- Mocked APIs include:
  - AlphaVantage API (US stock information, exchange rates)
  - J-Quants API (Japanese stock information)
  - Yahoo Finance (stock price retrieval).
- **Stock Price Behavior**: Return different values for the first and subsequent calls.
  - Japanese stocks: 1st call 3000.0 yen, subsequent calls 3100.0 yen.
  - US stocks: 1st call 36000.0 yen, subsequent calls 37500.0 yen (converted).
- Tests that actually call external APIs are unnecessary (they are mocked).

### Test Data Setup

- **Japanese Stocks**: Use `setup_japanese_stock_data` fixture (buy 100 shares of 8058 at 3000 yen).
- **US Stocks**: Use `setup_us_stock_data` fixture (buy 10 shares of AAPL at 36054 yen).
- **Dividends**: Use `setup_dividend_data` fixture (dividend data for Japanese and US stocks).
- **Portfolio**: Use `setup_portfolio_test_data` fixture (all data for Japanese stocks, US stocks, and dividends).
- Combine these fixtures to establish the necessary initial state for tests.

### HTTP Client

- Asynchronous tests: Use `client` fixture (AsyncClient).
- Synchronous tests: Use `sync_client` fixture (TestClient).
- Database connections are automatically overridden for testing.

## Adding Packages

This section provides the correct method for adding packages to the project using `uv`.

### Instructions

1. Ensure the current directory is `src/api`.
2. Add a package using the `uv add <package-name>` command:
   - For regular dependencies: `uv add <package-name>`.
   - For development dependencies: `uv add -D <package-name>`.
3. After adding the package, verify that it is included in `pyproject.toml`.
4. Confirm that `uv.lock` has been updated.

### Important Notes

⚠️ **Do not edit `pyproject.toml` directly.**

Always use the `uv add` command to add packages. Directly editing `pyproject.toml` may prevent `uv.lock` from updating, leading to inconsistencies in dependencies.