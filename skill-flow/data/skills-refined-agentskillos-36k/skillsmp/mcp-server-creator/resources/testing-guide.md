# MCP Server Testing Guide for LLMs

This document provides comprehensive guidance on testing MCP servers using the official Python SDK, with extensive examples for LLM consumption and implementation.

## Overview

The Python SDK provides a `Client` class for testing MCP servers with an in-memory transport. This makes it easy to write tests without network overhead. The Client class simulates the real MCP protocol interactions but runs entirely in memory, making tests fast and isolated.

## Setting up Test Dependencies

To run tests, you'll need to install the following dependencies:

=== "pip"
    ```bash
    pip install pytest anyio
    ```

=== "uv"
    ```bash
    uv add pytest anyio
    ```

For snapshot testing (recommended for verifying outputs):
```bash
pip install inline-snapshot
```

## Basic Test Setup

### Example Server to Test

Let's assume you have a simple server with tools, resources, and prompts:

```python title="calculator_server.py"
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Calculator Server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.tool()
def multiply(x: float, y: float) -> float:
    """Multiply two numbers."""
    return x * y

@mcp.tool()
def divide(dividend: float, divisor: float) -> float:
    """Divide two numbers."""
    if divisor == 0:
        raise ValueError("Cannot divide by zero")
    return dividend / divisor

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting."""
    return f"Hello, {name}!"

@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt."""
    return f"Write a {style} greeting for someone named {name}."
```

### Basic Test Example

```python title="test_calculator_server.py"
import pytest
from mcp import Client

from calculator_server import mcp


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    async with Client(mcp, raise_exceptions=True) as c:
        yield c


@pytest.mark.anyio
async def test_call_add_tool(client: Client):
    result = await client.call_tool("add", {"a": 1, "b": 2})
    assert result.structuredContent["result"] == 3


@pytest.mark.anyio
async def test_call_multiply_tool(client: Client):
    result = await client.call_tool("multiply", {"x": 3.5, "y": 2.0})
    assert result.structuredContent["result"] == 7.0


@pytest.mark.anyio
async def test_call_divide_tool(client: Client):
    result = await client.call_tool("divide", {"dividend": 10.0, "divisor": 2.0})
    assert result.structuredContent["result"] == 5.0


@pytest.mark.anyio
async def test_division_by_zero_raises_error(client: Client):
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        await client.call_tool("divide", {"dividend": 10.0, "divisor": 0.0})


@pytest.mark.anyio
async def test_read_greeting_resource(client: Client):
    result = await client.read_resource("greeting://World")
    assert result == "Hello, World!"


@pytest.mark.anyio
async def test_call_greet_user_prompt(client: Client):
    result = await client.call_prompt("greet_user", {"name": "Alice", "style": "professional"})
    assert "professional" in result.lower()
    assert "alice" in result.lower()
```

## Advanced Testing Patterns

### Testing Multiple Tools with Complex Data

```python
from typing import List, Dict, Any


# Extended server with more complex tools
@mcp.tool()
def process_numbers(numbers: List[float], operation: str = "sum") -> Dict[str, float]:
    """Process a list of numbers with the specified operation."""
    if operation == "sum":
        result = sum(numbers)
    elif operation == "average":
        result = sum(numbers) / len(numbers) if numbers else 0
    elif operation == "max":
        result = max(numbers) if numbers else 0
    elif operation == "min":
        result = min(numbers) if numbers else 0
    else:
        raise ValueError(f"Unsupported operation: {operation}")

    return {
        "result": result,
        "count": len(numbers),
        "operation": operation
    }


@mcp.tool()
def analyze_text(text: str) -> Dict[str, Any]:
    """Analyze text and return statistics."""
    words = text.split()
    sentences = text.split('.')
    paragraphs = [p for p in text.split('\n\n') if p.strip()]

    return {
        "word_count": len(words),
        "character_count": len(text),
        "sentence_count": len([s for s in sentences if s.strip()]),
        "paragraph_count": len(paragraphs),
        "average_word_length": sum(len(word) for word in words) / len(words) if words else 0,
        "has_questions": '?' in text,
        "has_exclamations": '!' in text
    }


@pytest.mark.anyio
async def test_process_numbers_sum(client: Client):
    result = await client.call_tool("process_numbers", {
        "numbers": [1.0, 2.0, 3.0, 4.0, 5.0],
        "operation": "sum"
    })
    assert result.structuredContent["result"] == 15.0
    assert result.structuredContent["count"] == 5
    assert result.structuredContent["operation"] == "sum"


@pytest.mark.anyio
async def test_process_numbers_average(client: Client):
    result = await client.call_tool("process_numbers", {
        "numbers": [10.0, 20.0, 30.0],
        "operation": "average"
    })
    assert result.structuredContent["result"] == 20.0


@pytest.mark.anyio
async def test_analyze_text_basic(client: Client):
    text = "Hello world. This is a test."
    result = await client.call_tool("analyze_text", {"text": text})

    assert result.structuredContent["word_count"] == 6
    assert result.structuredContent["sentence_count"] == 2
    assert result.structuredContent["has_questions"] is False
    assert result.structuredContent["has_exclamations"] is False


@pytest.mark.anyio
async def test_analyze_text_complex(client: Client):
    text = "Hello world! How are you? This is a test.\n\nNew paragraph here."
    result = await client.call_tool("analyze_text", {"text": text})

    assert result.structuredContent["word_count"] == 11
    assert result.structuredContent["sentence_count"] == 3
    assert result.structuredContent["has_questions"] is True
    assert result.structuredContent["has_exclamations"] is True
    assert result.structuredContent["paragraph_count"] == 2
```

### Testing with Parametrized Inputs

```python
@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 1, 0),
    (100, 200, 300),
    (-5, -10, -15)
])
@pytest.mark.anyio
async def test_add_parametrized(client: Client, a: int, b: int, expected: int):
    """Test the add tool with various inputs."""
    result = await client.call_tool("add", {"a": a, "b": b})
    assert result.structuredContent["result"] == expected


@pytest.mark.parametrize("x,y,expected", [
    (2.0, 3.0, 6.0),
    (0.0, 5.0, 0.0),
    (-2.0, 4.0, -8.0),
    (1.5, 2.5, 3.75),
    (10.0, 0.5, 5.0)
])
@pytest.mark.anyio
async def test_multiply_parametrized(client: Client, x: float, y: float, expected: float):
    """Test the multiply tool with various inputs."""
    result = await client.call_tool("multiply", {"x": x, "y": y})
    assert abs(result.structuredContent["result"] - expected) < 1e-10  # Floating point comparison


@pytest.mark.parametrize("dividend,divisor,expected", [
    (10.0, 2.0, 5.0),
    (0.0, 5.0, 0.0),
    (-10.0, 2.0, -5.0),
    (15.0, 3.0, 5.0)
])
@pytest.mark.anyio
async def test_divide_parametrized(client: Client, dividend: float, divisor: float, expected: float):
    """Test the divide tool with various inputs."""
    result = await client.call_tool("divide", {"dividend": dividend, "divisor": divisor})
    assert abs(result.structuredContent["result"] - expected) < 1e-10


@pytest.mark.parametrize("operation,expected", [
    ("sum", 15.0),
    ("average", 3.0),
    ("max", 5.0),
    ("min", 1.0)
])
@pytest.mark.anyio
async def test_process_numbers_parametrized(client: Client, operation: str, expected: float):
    """Test the process_numbers tool with different operations."""
    result = await client.call_tool("process_numbers", {
        "numbers": [1.0, 2.0, 3.0, 4.0, 5.0],
        "operation": operation
    })
    assert abs(result.structuredContent["result"] - expected) < 1e-10
```

### Testing Error Handling

```python
import logging


@pytest.mark.anyio
async def test_tool_with_validation_error(client: Client):
    """Test that tools properly validate input parameters."""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        await client.call_tool("divide", {"dividend": 10.0, "divisor": 0.0})


@pytest.mark.anyio
async def test_tool_with_invalid_operation(client: Client):
    """Test that tools handle invalid operations correctly."""
    with pytest.raises(ValueError, match="Unsupported operation"):
        await client.call_tool("process_numbers", {
            "numbers": [1.0, 2.0],
            "operation": "invalid_operation"
        })


@pytest.mark.anyio
async def test_nonexistent_tool(client: Client):
    """Test calling a non-existent tool raises appropriate error."""
    with pytest.raises(Exception):  # Exact exception type depends on implementation
        await client.call_tool("nonexistent_tool", {"param": "value"})


@pytest.mark.anyio
async def test_resource_not_found(client: Client):
    """Test reading a non-existent resource raises appropriate error."""
    with pytest.raises(Exception):  # Exact exception type depends on implementation
        await client.read_resource("greeting://NonExistentUser")


@pytest.mark.anyio
async def test_prompt_with_invalid_params(client: Client):
    """Test calling a prompt with invalid parameters."""
    with pytest.raises(Exception):  # Exact exception type depends on implementation
        await client.call_prompt("greet_user", {"invalid_param": "value"})
```

## Comprehensive Test Suite

### Complete Test Suite Example

```python
import pytest
from mcp import Client
from typing import List, Dict, Any


class TestCalculatorTools:
    """Comprehensive test suite for calculator tools."""

    @pytest.mark.parametrize("a,b,expected", [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
        (100, 200, 300),
        (-5, -10, -15)
    ])
    @pytest.mark.anyio
    async def test_add_parametrized(self, client: Client, a: int, b: int, expected: int):
        """Test the add tool with various inputs."""
        result = await client.call_tool("add", {"a": a, "b": b})
        assert result.structuredContent["result"] == expected

    @pytest.mark.parametrize("x,y,expected", [
        (2.0, 3.0, 6.0),
        (0.0, 5.0, 0.0),
        (-2.0, 4.0, -8.0),
        (1.5, 2.5, 3.75),
        (10.0, 0.5, 5.0)
    ])
    @pytest.mark.anyio
    async def test_multiply_parametrized(self, client: Client, x: float, y: float, expected: float):
        """Test the multiply tool with various inputs."""
        result = await client.call_tool("multiply", {"x": x, "y": y})
        assert abs(result.structuredContent["result"] - expected) < 1e-10

    @pytest.mark.parametrize("dividend,divisor,expected", [
        (10.0, 2.0, 5.0),
        (0.0, 5.0, 0.0),
        (-10.0, 2.0, -5.0),
        (15.0, 3.0, 5.0)
    ])
    @pytest.mark.anyio
    async def test_divide_parametrized(self, client: Client, dividend: float, divisor: float, expected: float):
        """Test the divide tool with various inputs."""
        result = await client.call_tool("divide", {"dividend": dividend, "divisor": divisor})
        assert abs(result.structuredContent["result"] - expected) < 1e-10

    @pytest.mark.anyio
    async def test_division_by_zero_raises_error(self, client: Client):
        """Test that division by zero raises the correct error."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            await client.call_tool("divide", {"dividend": 10.0, "divisor": 0.0})

    @pytest.mark.parametrize("operation,expected", [
        ("sum", 15.0),
        ("average", 3.0),
        ("max", 5.0),
        ("min", 1.0)
    ])
    @pytest.mark.anyio
    async def test_process_numbers_parametrized(self, client: Client, operation: str, expected: float):
        """Test the process_numbers tool with different operations."""
        result = await client.call_tool("process_numbers", {
            "numbers": [1.0, 2.0, 3.0, 4.0, 5.0],
            "operation": operation
        })
        assert abs(result.structuredContent["result"] - expected) < 1e-10


class TestResources:
    """Test suite for resource operations."""

    @pytest.mark.parametrize("name,expected_greeting", [
        ("World", "Hello, World!"),
        ("Alice", "Hello, Alice!"),
        ("Bob", "Hello, Bob!"),
        ("", "Hello, !")
    ])
    @pytest.mark.anyio
    async def test_greeting_resource_parametrized(self, client: Client, name: str, expected_greeting: str):
        """Test the greeting resource with various names."""
        result = await client.read_resource(f"greeting://{name}")
        assert result == expected_greeting


class TestPrompts:
    """Test suite for prompt operations."""

    @pytest.mark.parametrize("name,style,expected_elements", [
        ("Alice", "friendly", ["friendly", "alice"]),
        ("Bob", "professional", ["professional", "bob"]),
        ("Charlie", "casual", ["casual", "charlie"])
    ])
    @pytest.mark.anyio
    async def test_greet_user_prompt_parametrized(self, client: Client, name: str, style: str, expected_elements: List[str]):
        """Test the greet_user prompt with various inputs."""
        result = await client.call_prompt("greet_user", {"name": name, "style": style})

        for element in expected_elements:
            assert element.lower() in result.lower()


class TestServerMetadata:
    """Test server metadata and capabilities."""

    def test_server_has_expected_tools(self):
        """Test that server has the expected tools registered."""
        tool_names = [tool.name for tool in mcp._tools]
        expected_tools = ["add", "multiply", "divide", "process_numbers", "analyze_text"]
        for tool in expected_tools:
            assert tool in tool_names

    def test_server_has_expected_resources(self):
        """Test that server has the expected resources registered."""
        resource_names = [resource.name for resource in mcp._resources]
        expected_resources = ["get_greeting"]  # This would be the function name
        for resource in expected_resources:
            assert resource in resource_names

    def test_server_has_expected_prompts(self):
        """Test that server has the expected prompts registered."""
        prompt_names = [prompt.name for prompt in mcp._prompts]
        expected_prompts = ["greet_user"]  # This would be the function name
        for prompt in expected_prompts:
            assert prompt in prompt_names


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    @pytest.mark.anyio
    async def test_very_large_numbers_add(self, client: Client):
        """Test addition with very large numbers."""
        large_num = 2**50
        result = await client.call_tool("add", {"a": large_num, "b": large_num})
        assert result.structuredContent["result"] == 2 * large_num

    @pytest.mark.anyio
    async def test_very_small_numbers_multiply(self, client: Client):
        """Test multiplication with very small numbers."""
        small_num = 1e-10
        result = await client.call_tool("multiply", {"x": small_num, "y": small_num})
        expected = small_num * small_num
        assert abs(result.structuredContent["result"] - expected) < 1e-20

    @pytest.mark.anyio
    async def test_empty_list_process_numbers(self, client: Client):
        """Test process_numbers with empty list."""
        result = await client.call_tool("process_numbers", {"numbers": [], "operation": "sum"})
        assert result.structuredContent["result"] == 0
        assert result.structuredContent["count"] == 0

    @pytest.mark.anyio
    async def test_empty_string_analyze_text(self, client: Client):
        """Test analyze_text with empty string."""
        result = await client.call_tool("analyze_text", {"text": ""})

        assert result.structuredContent["word_count"] == 0
        assert result.structuredContent["character_count"] == 0
        assert result.structuredContent["sentence_count"] == 0
        assert result.structuredContent["paragraph_count"] == 0
        assert result.structuredContent["average_word_length"] == 0
        assert result.structuredContent["has_questions"] is False
        assert result.structuredContent["has_exclamations"] is False


class TestConcurrentOperations:
    """Test concurrent operations to ensure thread safety."""

    @pytest.mark.anyio
    async def test_concurrent_add_operations(self, client: Client):
        """Test multiple concurrent add operations."""
        import asyncio

        # Make multiple concurrent calls
        tasks = [
            client.call_tool("add", {"a": i, "b": i+1})
            for i in range(10)
        ]

        results = await asyncio.gather(*tasks)

        # Verify all results
        expected_results = [2*i + 1 for i in range(10)]  # 1, 3, 5, 7, 9, 11, 13, 15, 17, 19
        actual_results = [r.structuredContent["result"] for r in results]
        assert actual_results == expected_results

    @pytest.mark.anyio
    async def test_concurrent_different_tools(self, client: Client):
        """Test concurrent calls to different tools."""
        import asyncio

        # Make concurrent calls to different tools
        tasks = [
            client.call_tool("add", {"a": 5, "b": 3}),
            client.call_tool("multiply", {"x": 4.0, "y": 2.0}),
            client.call_tool("process_numbers", {"numbers": [1.0, 2.0, 3.0], "operation": "sum"}),
            client.call_tool("analyze_text", {"text": "Hello world."})
        ]

        results = await asyncio.gather(*tasks)

        # Verify each result
        assert results[0].structuredContent["result"] == 8      # add: 5+3
        assert results[1].structuredContent["result"] == 8.0    # multiply: 4*2
        assert results[2].structuredContent["result"] == 6.0    # process_numbers: sum of [1,2,3]
        assert results[3].structuredContent["word_count"] == 2  # analyze_text: "Hello world."


class TestErrorHandling:
    """Test error handling and edge cases."""

    @pytest.mark.anyio
    async def test_missing_required_parameter(self, client: Client):
        """Test calling a tool without required parameters."""
        # This should raise an error because 'a' and 'b' are required for 'add'
        with pytest.raises(Exception):  # Could be TypeError, ValidationError, etc.
            await client.call_tool("add", {})

    @pytest.mark.anyio
    async def test_invalid_parameter_type(self, client: Client):
        """Test calling a tool with wrong parameter types."""
        with pytest.raises((TypeError, ValueError)):
            await client.call_tool("add", {"a": "not_a_number", "b": 5})

    @pytest.mark.anyio
    async def test_extra_unexpected_parameter(self, client: Client):
        """Test calling a tool with extra parameters."""
        # This should work fine - extra parameters might be ignored
        result = await client.call_tool("add", {"a": 1, "b": 2, "extra": "ignored"})
        assert result.structuredContent["result"] == 3

    @pytest.mark.anyio
    async def test_tool_not_found(self, client: Client):
        """Test calling a non-existent tool."""
        with pytest.raises(Exception):  # Exact exception depends on implementation
            await client.call_tool("non_existent_tool", {})

    @pytest.mark.anyio
    async def test_resource_not_found(self, client: Client):
        """Test reading a non-existent resource."""
        with pytest.raises(Exception):  # Exact exception depends on implementation
            await client.read_resource("greeting://NonExistentUser")

    @pytest.mark.anyio
    async def test_prompt_not_found(self, client: Client):
        """Test calling a non-existent prompt."""
        with pytest.raises(Exception):  # Exact exception depends on implementation
            await client.call_prompt("non_existent_prompt", {})
```

## Mocking and Testing External Dependencies

### Mocking External Services

```python
from unittest.mock import AsyncMock, patch
import pytest


# Example server that calls external APIs
@mcp.tool()
async def get_weather(city: str) -> Dict[str, any]:
    """Get weather for a city by calling external API."""
    import aiohttp

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.weather.com/v1/weather?city={city}") as response:
            return await response.json()


@pytest.mark.anyio
async def test_get_weather_with_mocked_api():
    """Test weather tool with mocked API."""
    # Create a mock response
    mock_response = AsyncMock()
    mock_response.json.return_value = {
        "city": "New York",
        "temperature": 22,
        "condition": "sunny"
    }

    # Create a mock session context manager
    mock_session = AsyncMock()
    mock_session.__aenter__.return_value = mock_session
    mock_session.get.return_value.__aenter__.return_value = mock_response

    # Patch the aiohttp.ClientSession
    with patch('aiohttp.ClientSession', return_value=mock_session):
        async with Client(mcp, raise_exceptions=True) as client:
            result = await client.call_tool("get_weather", {"city": "New York"})

            # Verify the API was called with correct parameters
            mock_session.get.assert_called_once()
            call_args = mock_session.get.call_args[0][0]  # Get the first positional argument
            assert "New York" in call_args

            # Verify the result contains expected data
            assert result.structuredContent["result"]["temperature"] == 22
            assert result.structuredContent["result"]["condition"] == "sunny"


# Example server that interacts with databases
@mcp.tool()
def get_user_info(user_id: str) -> Dict[str, any]:
    """Get user information from database."""
    # In a real implementation, this would connect to a database
    # For this example, we'll simulate a database lookup
    database = {
        "1": {"id": "1", "name": "Alice", "email": "alice@example.com", "age": 30},
        "2": {"id": "2", "name": "Bob", "email": "bob@example.com", "age": 25},
        "3": {"id": "3", "name": "Charlie", "email": "charlie@example.com", "age": 35}
    }

    if user_id not in database:
        raise ValueError(f"User with ID {user_id} not found")

    return database[user_id]


@pytest.mark.anyio
async def test_get_user_info_success():
    """Test successful user info retrieval."""
    async with Client(mcp, raise_exceptions=True) as client:
        result = await client.call_tool("get_user_info", {"user_id": "1"})

        expected_user = {"id": "1", "name": "Alice", "email": "alice@example.com", "age": 30}
        assert result.structuredContent["result"] == expected_user


@pytest.mark.anyio
async def test_get_user_info_not_found():
    """Test error handling when user is not found."""
    async with Client(mcp, raise_exceptions=True) as client:
        with pytest.raises(ValueError, match="User with ID 999 not found"):
            await client.call_tool("get_user_info", {"user_id": "999"})


# Example with patching a database connection
@pytest.mark.anyio
async def test_get_user_info_with_mocked_database():
    """Test user info tool with mocked database."""
    # This example shows how you might mock a real database connection
    # For this example, we'll patch the function that performs the database lookup

    # Since our example function is in the same module, we need to patch differently
    # In a real scenario, you'd patch the actual database connection function
    pass  # This would be implemented based on your actual database implementation
```

## Performance and Stress Testing

### Performance Testing Patterns

```python
import time
import asyncio
import pytest


class TestPerformance:
    """Performance and stress tests for the server."""

    @pytest.mark.timeout(5)  # This test should complete within 5 seconds
    @pytest.mark.anyio
    async def test_many_operations_performance(self, client: Client):
        """Test performance with many operations."""
        start_time = time.time()

        # Perform many operations
        for i in range(100):
            await client.call_tool("add", {"a": i, "b": i+1})

        elapsed = time.time() - start_time
        assert elapsed < 2.0, f"Operations took too long: {elapsed}s"

    @pytest.mark.anyio
    async def test_concurrent_throughput(self, client: Client):
        """Test concurrent request throughput."""
        import asyncio

        async def single_request(i):
            start = time.time()
            result = await client.call_tool("add", {"a": i, "b": i+1})
            end = time.time()
            return end - start, result

        # Send many concurrent requests
        start_total = time.time()
        tasks = [single_request(i) for i in range(50)]
        results = await asyncio.gather(*tasks)
        end_total = time.time()

        total_time = end_total - start_total
        requests_per_second = len(results) / total_time

        print(f"Throughput: {requests_per_second:.2f} requests/second")

        # Assert reasonable throughput
        assert requests_per_second > 10, f"Throughput too low: {requests_per_second} req/s"

    @pytest.mark.anyio
    async def test_large_payload_handling(self, client: Client):
        """Test handling of large payloads."""
        # Create a large input
        large_text = "This is a large text. " * 1000  # 20KB of text

        start_time = time.time()
        result = await client.call_tool("analyze_text", {"text": large_text})
        elapsed = time.time() - start_time

        # Verify the operation completed successfully
        assert result.structuredContent["word_count"] == 3000  # 3 words per sentence * 1000
        assert result.structuredContent["character_count"] == len(large_text)

        # Verify it didn't take too long
        assert elapsed < 5.0, f"Large payload took too long: {elapsed}s"

    @pytest.mark.anyio
    async def test_memory_usage_stability(self, client: Client):
        """Test that memory usage doesn't grow unexpectedly."""
        import psutil
        import os

        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        # Perform many operations that might cause memory accumulation
        for i in range(100):
            # Call various tools
            await client.call_tool("add", {"a": i, "b": i+1})
            await client.call_tool("multiply", {"x": float(i), "y": 2.0})
            await client.call_tool("analyze_text", {"text": f"Sample text {i}"})

        # Force garbage collection
        import gc
        gc.collect()

        # Get final memory usage
        final_memory = process.memory_info().rss
        memory_growth = final_memory - initial_memory

        # Memory should not grow more than 10MB during this test
        assert memory_growth < 10 * 1024 * 1024, f"Memory grew too much: {memory_growth} bytes"

    @pytest.mark.anyio
    async def test_response_time_consistency(self, client: Client):
        """Test that response times remain consistent."""
        response_times = []

        # Measure response time for multiple identical requests
        for _ in range(20):
            start = time.time()
            await client.call_tool("add", {"a": 1, "b": 2})
            elapsed = time.time() - start
            response_times.append(elapsed)

        # Calculate average and standard deviation
        avg_time = sum(response_times) / len(response_times)
        variance = sum((x - avg_time) ** 2 for x in response_times) / len(response_times)
        std_dev = variance ** 0.5

        # Response times should be consistent (std dev should be low)
        assert std_dev < avg_time * 0.5, f"Response times inconsistent: avg={avg_time:.4f}s, std_dev={std_dev:.4f}s"
        assert avg_time < 0.1, f"Average response time too high: {avg_time:.4f}s"


class TestStress:
    """Stress tests for the server."""

    @pytest.mark.anyio
    async def test_high_concurrency(self, client: Client):
        """Test server under high concurrent load."""
        import asyncio

        # Create many concurrent requests
        async def worker(worker_id):
            results = []
            for i in range(10):  # Each worker makes 10 requests
                result = await client.call_tool("add", {"a": worker_id, "b": i})
                results.append(result.structuredContent["result"])
            return results

        # Create 20 workers making requests concurrently
        workers = [worker(i) for i in range(20)]
        all_results = await asyncio.gather(*workers)

        # Verify all workers completed successfully
        assert len(all_results) == 20
        for worker_results in all_results:
            assert len(worker_results) == 10  # Each worker returned 10 results

    @pytest.mark.anyio
    async def test_long_running_operations(self, client: Client):
        """Test server behavior with long-running operations."""
        # This test would be for operations that take longer to complete
        # For now, we'll simulate with sleep operations
        pass  # Implementation would depend on your specific long-running operations
```

## Integration Testing Patterns

### Testing with Real Transport (Advanced)

```python
import subprocess
import time
import asyncio
from contextlib import asynccontextmanager


@asynccontextmanager
async def real_server_context():
    """Context manager for running a real server instance for integration tests."""
    # Start a real server in a subprocess
    # This would typically run your server with streamable-http transport
    process = subprocess.Popen([
        "python", "-c", """
import sys
sys.path.insert(0, '.')
from calculator_server import mcp
mcp.run(transport='streamable-http', host='127.0.0.1', port=8081)
"""
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for server to start
    await asyncio.sleep(2)

    try:
        # Test connection to the real server
        # This would involve creating an actual HTTP client
        yield "http://127.0.0.1:8081"
    finally:
        # Terminate the server process
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


@pytest.mark.integration
@pytest.mark.asyncio
async def test_with_real_transport():
    """Integration test using real HTTP transport."""
    async with real_server_context() as server_url:
        # Test using HTTP client or MCP client connecting to real server
        # Implementation would depend on your specific server configuration
        pass  # This is a placeholder for the actual integration test
```

## Test Organization and Structure

### Organizing Tests by Feature

```python
# Recommended test directory structure:
"""
tests/
├── conftest.py                 # Shared fixtures
├── test_calculator.py          # Specific tool tests
├── test_resources.py           # Resource tests
├── test_prompts.py             # Prompt tests
├── test_error_handling.py      # Error handling tests
├── test_performance.py         # Performance tests
├── test_concurrency.py         # Concurrency tests
├── test_integration.py         # Integration tests
└── __snapshots__/              # Snapshot files for inline-snapshot
"""

# Example conftest.py
"""
import pytest
from mcp import Client
from calculator_server import mcp


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    async with Client(mcp, raise_exceptions=True) as c:
        yield c


@pytest.fixture
def sample_data():
    return {
        "small_numbers": [1, 2, 3],
        "large_numbers": [1000, 2000, 3000],
        "negative_numbers": [-1, -2, -3],
        "mixed_numbers": [1, -2, 3, -4, 5],
        "sample_text": "This is a sample text for testing.",
        "long_text": "This is a long text. " * 1000
    }
"""
```

## Test Configuration

### pytest.ini Configuration

```ini
[tool:pytest]
asyncio_mode = auto
asyncio_default_fixture_loop_scope = function
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -ra
    --strict-markers
    --strict-config
    --tb=short
    --maxfail=1
    --durations=10
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    performance: marks tests as performance tests
filterwarnings =
    error
    ignore::DeprecationWarning
    ignore::UserWarning
```

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_calculator.py

# Run tests with specific marker
pytest -m "performance"

# Run tests with coverage
pytest --cov=calculator_server --cov-report=html

# Run tests in parallel (install pytest-xdist first)
pytest -n auto

# Run tests with timeout (install pytest-timeout first)
pytest --timeout=30
```

## Common Testing Scenarios

### Testing Different Transport Modes

```python
# While the in-memory transport is ideal for unit tests,
# you might want to test different transport configurations:

@pytest.mark.anyio
async def test_tool_with_different_inputs(client: Client):
    """Test tool behavior with different types of inputs."""

    # Test with integers
    result = await client.call_tool("add", {"a": 1, "b": 2})
    assert result.structuredContent["result"] == 3

    # Test with floats treated as ints
    result = await client.call_tool("add", {"a": 1.0, "b": 2.0})
    assert result.structuredContent["result"] == 3  # Should convert to int

    # Test with string numbers (this might fail depending on type conversion)
    with pytest.raises(Exception):
        await client.call_tool("add", {"a": "1", "b": "2"})
```

### Testing Context Integration

```python
# If your tools use MCP context for advanced features:
from mcp_use.server import Context

# Example tool that uses context
@mcp.tool()
async def contextual_tool(data: str, ctx: Context) -> str:
    """Tool that uses MCP context for advanced features."""
    # Log progress to client
    await ctx.log('info', f'Processing data: {data[:20]}...')

    # Perform operation
    result = data.upper()

    # Return result
    return result

@pytest.mark.anyio
async def test_contextual_tool(client: Client):
    """Test tool that uses context."""
    result = await client.call_tool("contextual_tool", {"data": "hello world"})
    assert result.structuredContent["result"] == "HELLO WORLD"
```

These testing patterns provide a comprehensive framework for testing MCP servers, ensuring reliability, correctness, and performance across various scenarios and edge cases.