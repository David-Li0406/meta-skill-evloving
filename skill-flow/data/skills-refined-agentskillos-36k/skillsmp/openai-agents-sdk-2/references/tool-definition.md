# Function Tool Definition Guide

This guide covers advanced patterns and best practices for defining function tools with the OpenAI Agents SDK.

## Basic Tool Definition

### Simple Function Tool

```python
from agents import function_tool

@function_tool
def get_weather(city: str) -> str:
    """Get weather information for a city."""
    return f"The weather in {city} is sunny."
```

### With Type Hints and Annotations

```python
from typing import Annotated
from agents import function_tool

@function_tool
def calculate_area(
    length: Annotated[float, "Length of the rectangle"],
    width: Annotated[float, "Width of the rectangle"],
    unit: Annotated[str, "Unit of measurement (meters, feet, inches)"]
) -> float:
    """
    Calculate area of a rectangle.

    Args:
        length: Length measurement
        width: Width measurement
        unit: Unit of measurement

    Returns:
        Area in square units
    """
    area = length * width
    return area
```

## Structured Output Tools

### Using Pydantic Models

```python
from typing import Annotated
from pydantic import BaseModel, Field
from agents import function_tool

class WeatherData(BaseModel):
    city: str = Field(description="Name of the city")
    temperature: float = Field(description="Temperature in Celsius")
    conditions: str = Field(description="Weather conditions")
    humidity: float = Field(description="Humidity percentage")
    wind_speed: float = Field(description="Wind speed in km/h")

@function_tool
def get_detailed_weather(
    city: Annotated[str, "City to get weather for"],
    include_forecast: Annotated[bool, "Include 3-day forecast"] = False
) -> WeatherData:
    """Get detailed weather information with structured response."""
    # In production, this would call a weather API
    return WeatherData(
        city=city,
        temperature=22.5,
        conditions="Partly cloudy",
        humidity=65.0,
        wind_speed=15.0
    )
```

### Nested Structured Responses

```python
from typing import List, Dict
from pydantic import BaseModel, Field
from agents import function_tool

class ForecastDay(BaseModel):
    date: str = Field(description="Date of forecast")
    high_temp: float = Field(description="High temperature")
    low_temp: float = Field(description="Low temperature")
    conditions: str = Field(description="Weather conditions")
    precipitation_chance: float = Field(description="Chance of precipitation")

class ExtendedWeatherData(BaseModel):
    current: WeatherData = Field(description="Current weather")
    forecast: List[ForecastDay] = Field(description="3-day forecast")
    alerts: List[str] = Field(description="Weather alerts")

@function_tool
def get_extended_weather(city: str) -> ExtendedWeatherData:
    """Get extended weather information with forecast."""
    return ExtendedWeatherData(
        current=WeatherData(
            city=city,
            temperature=22.5,
            conditions="Partly cloudy",
            humidity=65.0,
            wind_speed=15.0
        ),
        forecast=[
            ForecastDay(
                date="2024-01-22",
                high_temp=24.0,
                low_temp=18.0,
                conditions="Sunny",
                precipitation_chance=0.1
            ),
            # ... more forecast days
        ],
        alerts=["High UV index expected"]
    )
```

## Advanced Tool Patterns

### Tool with Side Effects

```python
import sqlite3
from typing import Annotated
from contextlib import closing
from agents import function_tool

@function_tool
def add_todo_item(
    title: Annotated[str, "Title of the todo item"],
    description: Annotated[str, "Description of the todo item"],
    priority: Annotated[str, "Priority (high, medium, low)"] = "medium"
) -> dict:
    """
    Add a new todo item to the database.

    This tool has side effects - it modifies the database.
    """
    try:
        with closing(sqlite3.connect("todos.db")) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO todos (title, description, priority) VALUES (?, ?, ?)",
                (title, description, priority)
            )
            conn.commit()

            return {
                "success": True,
                "message": f"Todo '{title}' added successfully",
                "id": cursor.lastrowid
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to add todo item"
        }
```

### Tool with External API Calls

```python
import aiohttp
import asyncio
from typing import Annotated, Dict, Any
from agents import function_tool

@function_tool
async def fetch_stock_price(
    symbol: Annotated[str, "Stock symbol (e.g., AAPL, GOOGL)"],
    include_history: Annotated[bool, "Include historical data"] = False
) -> Dict[str, Any]:
    """Fetch current stock price from external API."""
    try:
        async with aiohttp.ClientSession() as session:
            # Example API call
            url = f"https://api.example.com/stocks/{symbol}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()

                    result = {
                        "symbol": symbol,
                        "price": data["price"],
                        "currency": data["currency"],
                        "last_updated": data["timestamp"]
                    }

                    if include_history:
                        result["history"] = data.get("history", [])

                    return result
                else:
                    return {
                        "error": f"API request failed with status {response.status}",
                        "symbol": symbol
                    }
    except Exception as e:
        return {
            "error": str(e),
            "symbol": symbol
        }
```

### Tool with Authentication

```python
import os
from typing import Annotated, Dict, Any
from agents import function_tool

class AuthenticatedTool:
    """Base class for tools requiring authentication."""

    def __init__(self):
        self.api_key = os.getenv("EXTERNAL_API_KEY")
        if not self.api_key:
            raise ValueError("EXTERNAL_API_KEY environment variable not set")

    def get_headers(self) -> Dict[str, str]:
        """Get authentication headers."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

@function_tool
def search_products(
    query: Annotated[str, "Search query for products"],
    category: Annotated[str, "Product category"] = "all",
    max_results: Annotated[int, "Maximum number of results"] = 10
) -> Dict[str, Any]:
    """Search products using authenticated API."""
    tool = AuthenticatedTool()
    headers = tool.get_headers()

    # Make authenticated API call
    # ... implementation details

    return {
        "query": query,
        "results": [
            {"id": 1, "name": "Product 1", "price": 29.99},
            {"id": 2, "name": "Product 2", "price": 49.99}
        ],
        "total": 2
    }
```

## Tool Composition

### Chaining Tools

```python
from typing import Annotated
from agents import function_tool

@function_tool
def parse_user_query(query: str) -> dict:
    """Parse natural language query into structured format."""
    # Simple parsing logic
    if "weather" in query.lower():
        return {"type": "weather", "location": query.split()[-1]}
    elif "calculate" in query.lower():
        return {"type": "calculation", "expression": query}
    else:
        return {"type": "general", "query": query}

@function_tool
def execute_parsed_query(parsed: dict) -> str:
    """Execute query based on parsed type."""
    if parsed["type"] == "weather":
        return get_weather(parsed["location"])
    elif parsed["type"] == "calculation":
        return evaluate_expression(parsed["expression"])
    else:
        return f"Processing general query: {parsed['query']}"

@function_tool
def process_query_with_chain(query: str) -> str:
    """Process query through a chain of tools."""
    parsed = parse_user_query(query)
    result = execute_parsed_query(parsed)
    return result
```

### Tool Pipelines

```python
from typing import List, Callable
from agents import function_tool

class ToolPipeline:
    """Execute a sequence of tools in order."""

    def __init__(self, tools: List[Callable]):
        self.tools = tools

    @function_tool
    def execute_pipeline(self, initial_input: str) -> str:
        """Execute all tools in sequence."""
        current_result = initial_input

        for tool in self.tools:
            # Each tool should accept and return a string
            current_result = tool(current_result)

        return current_result

# Usage
def clean_text(text: str) -> str:
    return text.strip().lower()

def extract_keywords(text: str) -> str:
    keywords = ["weather", "calculate", "help"]
    found = [kw for kw in keywords if kw in text]
    return f"Keywords found: {', '.join(found)}"

pipeline = ToolPipeline([clean_text, extract_keywords])
```

## Error Handling in Tools

### Graceful Error Handling

```python
from typing import Annotated, Optional
from agents import function_tool

@function_tool
def safe_division(
    numerator: Annotated[float, "Numerator"],
    denominator: Annotated[float, "Denominator"]
) -> dict:
    """Perform division with comprehensive error handling."""
    try:
        if denominator == 0:
            return {
                "success": False,
                "error": "Division by zero",
                "message": "Cannot divide by zero"
            }

        result = numerator / denominator

        return {
            "success": True,
            "result": result,
            "operation": f"{numerator} / {denominator}",
            "message": "Division completed successfully"
        }

    except TypeError as e:
        return {
            "success": False,
            "error": "Type error",
            "message": f"Invalid input types: {e}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": "Unexpected error",
            "message": str(e)
        }
```

### Retry Logic in Tools

```python
import asyncio
from typing import Annotated
from agents import function_tool

@function_tool
async def resilient_api_call(
    endpoint: Annotated[str, "API endpoint URL"],
    max_retries: Annotated[int, "Maximum retry attempts"] = 3
) -> dict:
    """Make API call with retry logic."""
    import aiohttp

    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            "success": True,
                            "data": data,
                            "attempts": attempt + 1
                        }
                    else:
                        print(f"Attempt {attempt + 1} failed with status {response.status}")

        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")

        # Wait before retry
        if attempt < max_retries - 1:
            wait_time = (attempt + 1) * 2  # Exponential backoff
            await asyncio.sleep(wait_time)

    return {
        "success": False,
        "error": f"Failed after {max_retries} attempts",
        "attempts": max_retries
    }
```

## Tool Validation

### Input Validation

```python
from typing import Annotated
from pydantic import BaseModel, validator
from agents import function_tool

class UserInput(BaseModel):
    email: str
    age: int
    country: str

    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email address')
        return v

    @validator('age')
    def validate_age(cls, v):
        if v < 0 or v > 150:
            raise ValueError('Age must be between 0 and 150')
        return v

@function_tool
def register_user(
    email: Annotated[str, "User email address"],
    age: Annotated[int, "User age"],
    country: Annotated[str, "Country of residence"]
) -> dict:
    """Register user with input validation."""
    try:
        # Validate input using Pydantic
        user_input = UserInput(email=email, age=age, country=country)

        # Process registration
        return {
            "success": True,
            "message": f"User {email} registered successfully",
            "data": user_input.dict()
        }
    except ValueError as e:
        return {
            "success": False,
            "error": "Validation failed",
            "message": str(e)
        }
```

### Business Logic Validation

```python
from typing import Annotated
from datetime import datetime
from agents import function_tool

@function_tool
def schedule_meeting(
    title: Annotated[str, "Meeting title"],
    start_time: Annotated[str, "Start time (YYYY-MM-DD HH:MM)"],
    duration_minutes: Annotated[int, "Meeting duration in minutes"],
    participants: Annotated[list, "List of participant emails"]
) -> dict:
    """Schedule a meeting with business logic validation."""
    errors = []

    # Validate start time
    try:
        start_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
        if start_datetime < datetime.now():
            errors.append("Start time cannot be in the past")
    except ValueError:
        errors.append("Invalid date format. Use YYYY-MM-DD HH:MM")

    # Validate duration
    if duration_minutes < 15:
        errors.append("Meeting must be at least 15 minutes")
    elif duration_minutes > 240:
        errors.append("Meeting cannot exceed 4 hours")

    # Validate participants
    if not participants:
        errors.append("At least one participant is required")
    elif len(participants) > 20:
        errors.append("Maximum 20 participants allowed")

    if errors:
        return {
            "success": False,
            "errors": errors,
            "message": "Validation failed"
        }

    # Schedule meeting
    return {
        "success": True,
        "meeting_id": "meeting_123",
        "title": title,
        "start_time": start_time,
        "duration": duration_minutes,
        "participants": participants,
        "message": "Meeting scheduled successfully"
    }
```

## Performance Optimization

### Caching in Tools

```python
from functools import lru_cache
from typing import Annotated
from agents import function_tool

class CachedCalculator:
    """Calculator with caching for expensive operations."""

    def __init__(self):
        self.cache = {}

    @lru_cache(maxsize=100)
    def fibonacci(self, n: int) -> int:
        """Calculate Fibonacci number with caching."""
        if n <= 1:
            return n
        return self.fibonacci(n-1) + self.fibonacci(n-2)

    @lru_cache(maxsize=100)
    def factorial(self, n: int) -> int:
        """Calculate factorial with caching."""
        if n == 0:
            return 1
        return n * self.factorial(n-1)

calculator = CachedCalculator()

@function_tool
def calculate_math_operation(
    operation: Annotated[str, "Operation (fibonacci, factorial)"],
    n: Annotated[int, "Input number"]
) -> dict:
    """Calculate mathematical operations with caching."""
    if operation == "fibonacci":
        result = calculator.fibonacci(n)
    elif operation == "factorial":
        result = calculator.factorial(n)
    else:
        return {
            "success": False,
            "error": f"Unknown operation: {operation}"
        }

    return {
        "success": True,
        "operation": operation,
        "input": n,
        "result": result,
        "cache_hit": calculator.fibonacci.cache_info().hits > 0
    }
```

### Batch Processing Tools

```python
from typing import Annotated, List
from agents import function_tool

@function_tool
def batch_process_items(
    items: Annotated[List[str], "List of items to process"],
    operation: Annotated[str, "Operation to perform"]
) -> dict:
    """Process multiple items in batch."""
    results = []

    for item in items:
        if operation == "uppercase":
            results.append(item.upper())
        elif operation == "lowercase":
            results.append(item.lower())
        elif operation == "reverse":
            results.append(item[::-1])
        else:
            results.append(f"Unknown operation on: {item}")

    return {
        "success": True,
        "operation": operation,
        "input_count": len(items),
        "results": results,
        "summary": f"Processed {len(items)} items with {operation}"
    }
```

## Testing Tools

### Unit Testing Framework

```python
import unittest
from agents import function_tool

@function_tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

class TestFunctionTools(unittest.TestCase):
    """Test cases for function tools."""

    def test_add_numbers(self):
        """Test basic addition."""
        result = add_numbers(2, 3)
        self.assertEqual(result, 5)

    def test_add_negative_numbers(self):
        """Test addition with negative numbers."""
        result = add_numbers(-5, 10)
        self.assertEqual(result, 5)

    def test_add_zero(self):
        """Test addition with zero."""
        result = add_numbers(0, 42)
        self.assertEqual(result, 42)

if __name__ == "__main__":
    unittest.main()
```

### Integration Testing

```python
import asyncio
from agents import Agent, Runner, function_tool

@function_tool
def mock_weather_api(city: str) -> str:
    """Mock weather API for testing."""
    return f"Weather in {city}: Sunny, 22°C"

async def test_agent_with_tools():
    """Integration test for agent with tools."""
    agent = Agent(
        name="Test Agent",
        instructions="You are a test agent.",
        model="gpt-4o",
        tools=[mock_weather_api]
    )

    result = await Runner.run(agent, "What's the weather in Tokyo?")

    assert "Tokyo" in result.final_output
    assert "Sunny" in result.final_output or "22" in result.final_output

    return result.final_output

# Run test
if __name__ == "__main__":
    result = asyncio.run(test_agent_with_tools())
    print(f"Test passed! Result: {result}")
```

## Best Practices

### 1. Documentation
- Include comprehensive docstrings
- Document parameters and return types
- Provide examples when possible

### 2. Error Handling
- Always handle exceptions gracefully
- Return structured error responses
- Log errors for debugging

### 3. Performance
- Implement caching for expensive operations
- Consider batch processing for multiple items
- Monitor tool execution times

### 4. Security
- Validate all inputs
- Sanitize user-provided data
- Use environment variables for secrets

### 5. Testing
- Write unit tests for individual tools
- Test tool integration with agents
- Monitor tool behavior in production

### 6. Maintenance
- Keep tools focused and single-purpose
- Document tool dependencies
- Version tools when making breaking changes

## Example Tool Library

See the `scripts/` directory for complete working examples:
- `scripts/basic_agent.py` - Basic tool usage patterns
- `scripts/openrouter_config.py` - Tools with external API integration
- `scripts/multi_agent_workflow.py` - Complex tool interactions