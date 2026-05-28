# MCP Resources Usage Guide

This document provides detailed information about using the `@mcp.resource()` decorator to define resources in your MCP server.

## Overview

Resources are named pieces of data that can be retrieved by clients. They represent static or dynamic data that can be accessed by URI.

## Basic Resource Definition

### Simple Resource
```python
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting."""
    return f"Hello, {name}!"
```

### Resource with Complex Data
```python
@mcp.resource("config://{env}/{key}")
def get_config_value(env: str, key: str) -> str:
    """Get configuration value for environment."""
    configs = {
        "prod": {"db_host": "prod-db.example.com", "api_key": "prod-key"},
        "dev": {"db_host": "dev-db.example.com", "api_key": "dev-key"}
    }

    env_config = configs.get(env, {})
    return env_config.get(key, "")
```

## Asynchronous Resources

### Async Resource
```python
@mcp.resource("file://{path}")
async def read_file(path: str) -> str:
    """Asynchronously read a file."""
    import aiofiles

    async with aiofiles.open(path, 'r') as f:
        return await f.read()
```

### Async Resource with External API
```python
@mcp.resource("api://{endpoint}")
async def fetch_api_data(endpoint: str) -> dict:
    """Fetch data from an external API."""
    import aiohttp

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.example.com/{endpoint}") as response:
            return await response.json()
```

## Resource Parameters

### Resource Decorator Parameters
```python
@mcp.resource(
    "my-resource://{identifier}",  # URI pattern
    name="custom-resource-name",   # Optional custom name
    title="Custom Resource Title", # Optional human-readable title
    description="Description of what this resource provides",  # Optional description
    icons=[{"type": "image/png", "uri": "icon.png"}]  # Optional icons
)
def my_resource(identifier: str) -> str:
    """Resource with custom parameters."""
    return f"Data for {identifier}"
```

## Advanced Resource Patterns

### Resource with Caching
```python
from functools import lru_cache
import time

@lru_cache(maxsize=128)
def _cached_resource_data(resource_id: str) -> str:
    """Internal function with caching."""
    # Simulate expensive operation
    time.sleep(0.1)
    return f"Cached data for {resource_id}"

@mcp.resource("cached://{resource_id}")
def get_cached_resource(resource_id: str) -> str:
    """Resource with caching."""
    return _cached_resource_data(resource_id)
```

## URI Pattern Guidelines

### Valid URI Patterns
```python
# Good: Simple parameter
@mcp.resource("user://{id}")
def get_user(id: str) -> dict: ...

# Good: Multiple parameters
@mcp.resource("organization://{org_id}/user://{user_id}")
def get_org_user(org_id: str, user_id: str) -> dict: ...

# Good: With file extension
@mcp.resource("document://{doc_id}.{extension}")
def get_document(doc_id: str, extension: str) -> str: ...
```

### Path-like Resources
```python
@mcp.resource("path://{path:path}")
def get_path_content(path: str) -> str:
    """Resource that accepts path-like parameters."""
    # The ':path' suffix allows slashes in the parameter
    return f"Content of path: {path}"
```

## Resource Return Types

### String Content
```python
@mcp.resource("text://{name}")
def get_text(name: str) -> str:
    """Return string content."""
    return f"This is the text content for {name}"
```

### JSON Data
```python
@mcp.resource("data://{dataset}")
def get_dataset(dataset: str) -> dict:
    """Return structured data."""
    return {
        "name": dataset,
        "data": [1, 2, 3, 4, 5],
        "metadata": {"created": "2024-01-01"}
    }
```

### Binary Content (represented as base64 or similar)
```python
import base64

@mcp.resource("image://{name}")
def get_image(name: str) -> str:
    """Return image as base64 encoded string."""
    # This would typically read an actual image file
    image_data = f"fake-image-data-for-{name}".encode()
    return base64.b64encode(image_data).decode()
```

## Integration with Tools

### Resource Called from Tool
```python
@mcp.resource("product://{product_id}")
def get_product(product_id: str) -> dict:
    """Get product information."""
    return {"id": product_id, "name": f"Product {product_id}", "price": 100}

@mcp.tool()
def recommend_product(user_id: str) -> dict:
    """Recommend a product by calling the resource internally."""
    # Get a default product recommendation
    product = get_product("recommended")
    return {
        "user_id": user_id,
        "recommended_product": product,
        "message": f"We recommend {product['name']} for user {user_id}"
    }
```
