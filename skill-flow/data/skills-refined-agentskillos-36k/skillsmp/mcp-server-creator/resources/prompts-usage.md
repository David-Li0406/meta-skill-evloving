# MCP Prompts Usage Guide

This document provides detailed information about using the `@mcp.prompt()` decorator to define prompts in your MCP server.

## Overview

Prompts are templates that generate prompts for LLMs. They return structured messages that can be used by LLMs to perform tasks or generate content.

## Basic Prompt Definition

### Simple Prompt
```python
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt."""
    return f"Write a {style} greeting for someone named {name}."
```

## Message Structure

### Prompt Returning Message List
```python
@mcp.prompt()
def analyze_table(table_name: str) -> list[dict]:
    """Generate a prompt to analyze a database table."""
    schema = get_table_schema(table_name)  # This would fetch actual schema
    return [
        {
            "role": "user",
            "content": f"Analyze this table schema:\n{schema}\n\nIdentify potential issues and optimization opportunities."
        }
    ]
```

### Prompt with Rich Content
```python
@mcp.prompt()
def analyze_document(path: str) -> list[dict]:
    """Generate a prompt to analyze a document."""
    content = read_file_content(path)

    return [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Please analyze the following document and provide a summary:\n\n{content[:1000]}..."
                }
            ]
        }
    ]
```

### Multi-Message Prompt
```python
@mcp.prompt()
def conduct_interview(candidate_name: str, position: str) -> list[dict]:
    """Generate a multi-part interview prompt."""
    return [
        {
            "role": "system",
            "content": "You are conducting an interview for a technical position."
        },
        {
            "role": "user",
            "content": f"You are interviewing {candidate_name} for the position of {position}."
        },
        {
            "role": "user",
            "content": "Please prepare a series of technical questions related to this position."
        }
    ]
```

## Asynchronous Prompts

### Async Prompt
```python
@mcp.prompt()
async def generate_report_async(data_source: str) -> list[dict]:
    """Asynchronously generate a report prompt."""
    data = await fetch_data_from_source(data_source)

    return [
        {
            "role": "user",
            "content": f"Generate a comprehensive report based on this data:\n\n{data}"
        }
    ]
```

## Prompt Parameters

### Prompt Decorator Parameters
```python
@mcp.prompt(
    name="custom-prompt-name",     # Optional custom name (defaults to function name)
    title="Custom Prompt Title",   # Optional human-readable title
    description="Description of what this prompt does",  # Optional description
    icons=[{"type": "image/png", "uri": "icon.png"}]     # Optional icons
)
def custom_prompt(parameter: str) -> str:
    """Prompt with custom parameters."""
    return f"Custom prompt with parameter: {parameter}"
```

## Advanced Prompt Patterns

### Prompt with Validation
```python
@mcp.prompt()
def validate_input(user_input: str, criteria: str) -> str:
    """Generate a prompt for input validation."""
    if not user_input.strip():
        raise ValueError("Input cannot be empty")

    if len(user_input) > 10000:  # 10k character limit
        raise ValueError("Input too long, maximum 10,000 characters allowed")

    return f"Review the following input against these criteria: '{criteria}'\n\nInput: {user_input}"
```

## Integration with Tools and Resources

### Prompt Using Tool Results
```python
@mcp.tool()
def get_current_weather(location: str) -> dict:
    """Get current weather data."""
    # This would typically call a weather API
    return {"location": location, "temperature": "22°C", "conditions": "Sunny"}

@mcp.prompt()
def weather_report_prompt(location: str) -> str:
    """Generate a weather report prompt using tool results."""
    weather_data = get_current_weather(location)  # Call the tool
    return f"Write a detailed weather report for {location} where the temperature is {weather_data['temperature']} and conditions are {weather_data['conditions']}."
```

### Prompt Using Resource Data
```python
@mcp.resource("company://{name}/info")
def get_company_info(name: str) -> dict:
    """Get company information."""
    return {"name": name, "industry": "Technology", "founded": "2020"}

@mcp.prompt()
def company_analysis_prompt(company_name: str) -> str:
    """Generate a company analysis prompt using resource data."""
    company_info = get_company_info(company_name)  # Access the resource
    return f"Analyze {company_info['name']}, a {company_info['industry']} company founded in {company_info['founded']}. Discuss market position and growth potential."
```

## Security Considerations

### Safe Prompt Generation
```python
import re

def sanitize_for_prompt(text: str) -> str:
    """Sanitize text before including in prompt."""
    # Remove potentially harmful patterns
    sanitized = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'vbscript:', '', sanitized, flags=re.IGNORECASE)
    return sanitized.strip()

@mcp.prompt()
def safe_analysis_prompt(content: str) -> str:
    """Generate a prompt with sanitized content."""
    sanitized_content = sanitize_for_prompt(content)
    return f"Analyze the following content: {sanitized_content}"
```

## Performance Optimization

### Cached Prompt Generation
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def _generate_static_prompt(template: str, **kwargs) -> str:
    """Internal cached function for static prompt generation."""
    # Simulate expensive template processing
    import time
    time.sleep(0.01)  # Simulate processing

    prompt = template
    for key, value in kwargs.items():
        prompt = prompt.replace(f"{{{key}}}", str(value))

    return prompt

@mcp.prompt()
def cached_template_prompt(template_name: str, **kwargs) -> str:
    """Prompt with caching for repeated templates."""
    templates = {
        "email": "Write a {tone} email about {subject} to {recipient}",
        "report": "Generate a {type} report on {topic} with {sections} sections",
        "summary": "Summarize {content} in {length} format"
    }

    template = templates.get(template_name)
    if not template:
        raise ValueError(f"Unknown template: {template_name}")

    return _generate_static_prompt(template, **kwargs)
```
