---
name: run-tests
description: Run tests for the wc_simd project using pytest. Use this skill to run all tests, specific test files, or individual test functions. Invoke with /run-tests.
---

# Testing

This skill runs tests for the wc_simd project using pytest.

## Run All Tests

```bash
pytest
```

## Run Specific Test File

```bash
pytest tests/test_pyspark.py
```

## Run Specific Test Function

```bash
pytest tests/test_pyspark.py::test_function_name
```

## Run with Verbose Output

```bash
pytest -v
```

## Run with Coverage

```bash
pytest --cov=wc_simd --cov-report=html
```

## Run Only Failed Tests

```bash
pytest --lf
```

## Run Tests Matching Pattern

```bash
pytest -k "embed"  # Run tests with "embed" in name
```

## Test Files

| File | Description |
|------|-------------|
| `tests/test_pyspark.py` | PySpark integration tests |
| `tests/test_embed.py` | Embedding service tests |
| `tests/test_llm.py` | LLM integration tests |

## Prerequisites

Ensure dependencies are installed:
```bash
uv sync
```

For Spark tests, ensure Docker Spark is running:
```bash
cd spark_docker_s3 && docker compose up -d --build
```

## Debugging Tests

```bash
# Drop into debugger on failure
pytest --pdb

# Show print statements
pytest -s

# Show local variables on failure
pytest -l
```
