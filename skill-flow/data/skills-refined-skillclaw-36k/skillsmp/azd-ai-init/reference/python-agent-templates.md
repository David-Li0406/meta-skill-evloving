# Python Agent Code Templates

This file contains Python code templates for Azure AI Foundry hosted agents.

## Basic Agent Template

```python
import asyncio
import os
import logging
from typing import Annotated

from azure.identity.aio import DefaultAzureCredential
from agent_framework.azure import AzureAIAgentClient
from azure.ai.agentserver.agentframework import from_agent_framework
from azure.monitor.opentelemetry import configure_azure_monitor
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)

logger = logging.getLogger(__name__)

# Configure Azure Monitor if connection string is available
if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
    configure_azure_monitor(enable_live_metrics=True, logger_name="__main__")

# Foundry Configuration
ENDPOINT = os.getenv("FOUNDRY_PROJECT_ENDPOINT", "")
MODEL_DEPLOYMENT_NAME = os.getenv("FOUNDRY_MODEL_DEPLOYMENT_NAME", "")


# ============================================
# Define your tools here
# ============================================

def example_tool(
    param1: Annotated[str, "Description of the first parameter"],
    param2: Annotated[int, "Description of the second parameter"]
) -> str:
    """Brief description of what this tool does.

    Args:
        param1: More detailed description if needed
        param2: More detailed description if needed
    
    Returns:
        Description of the return value
    """
    # Your implementation here
    return f"Result: {param1} - {param2}"


# Collect all tools in a list
tools = [example_tool]


# ============================================
# Agent Server
# ============================================

async def run_server():
    """Run the agent as an HTTP server."""
    credential = DefaultAzureCredential()
    
    try:
        # Create the Azure AI Agent client
        client = AzureAIAgentClient(
            project_endpoint=ENDPOINT,
            model_deployment_name=MODEL_DEPLOYMENT_NAME,
            credential=credential,
        )
        
        # Create the agent with tools
        agent = client.create_agent(
            name="{{AGENT_NAME}}",
            model=MODEL_DEPLOYMENT_NAME,
            instructions="""{{AGENT_INSTRUCTIONS}}""",
            tools=tools,
        )
        
        logger.info("Starting Agent HTTP Server...")
        print("Starting Agent HTTP Server...")
        
        # Run as hosted agent
        await from_agent_framework(agent).run_async()
    finally:
        await credential.close()


def main():
    """Main entry point for the hosted agent server."""
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
```

## Agent with Multiple Tools

```python
import asyncio
import os
import logging
from typing import Annotated, List, Optional

from azure.identity.aio import DefaultAzureCredential
from agent_framework.azure import AzureAIAgentClient
from azure.ai.agentserver.agentframework import from_agent_framework
from azure.monitor.opentelemetry import configure_azure_monitor
from dotenv import load_dotenv

load_dotenv(override=True)

logger = logging.getLogger(__name__)

if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
    configure_azure_monitor(enable_live_metrics=True, logger_name="__main__")

ENDPOINT = os.getenv("FOUNDRY_PROJECT_ENDPOINT", "")
MODEL_DEPLOYMENT_NAME = os.getenv("FOUNDRY_MODEL_DEPLOYMENT_NAME", "")


# ============================================
# Calculator Tools
# ============================================

def add(
    a: Annotated[float, "The first number to add"],
    b: Annotated[float, "The second number to add"]
) -> float:
    """Add two numbers together.

    Args:
        a: First number
        b: Second number
    """
    return a + b


def subtract(
    a: Annotated[float, "The number to subtract from"],
    b: Annotated[float, "The number to subtract"]
) -> float:
    """Subtract b from a.

    Args:
        a: The minuend
        b: The subtrahend
    """
    return a - b


def multiply(
    a: Annotated[float, "The first number to multiply"],
    b: Annotated[float, "The second number to multiply"]
) -> float:
    """Multiply two numbers.

    Args:
        a: First factor
        b: Second factor
    """
    return a * b


def divide(
    a: Annotated[float, "The dividend (numerator)"],
    b: Annotated[float, "The divisor (denominator)"]
) -> float:
    """Divide a by b.

    Args:
        a: Dividend
        b: Divisor (must not be zero)
    
    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


# ============================================
# String Tools
# ============================================

def reverse_string(
    text: Annotated[str, "The text to reverse"]
) -> str:
    """Reverse a string.

    Args:
        text: Input text to reverse
    """
    return text[::-1]


def count_words(
    text: Annotated[str, "The text to count words in"]
) -> int:
    """Count the number of words in text.

    Args:
        text: Input text
    """
    return len(text.split())


# All tools
tools = [add, subtract, multiply, divide, reverse_string, count_words]


async def run_server():
    """Run the agent as an HTTP server."""
    credential = DefaultAzureCredential()
    
    try:
        client = AzureAIAgentClient(
            project_endpoint=ENDPOINT,
            model_deployment_name=MODEL_DEPLOYMENT_NAME,
            credential=credential,
        )
        
        agent = client.create_agent(
            name="MultiToolAgent",
            model=MODEL_DEPLOYMENT_NAME,
            instructions="""You are a helpful assistant with access to multiple tools.
            
You can:
- Perform arithmetic operations (add, subtract, multiply, divide)
- Manipulate strings (reverse text, count words)

Always use the appropriate tool for the task. Show your work when doing calculations.""",
            tools=tools,
        )
        
        logger.info("Starting Multi-Tool Agent...")
        await from_agent_framework(agent).run_async()
    finally:
        await credential.close()


def main():
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
```

## Agent with External API Calls

```python
import asyncio
import os
import logging
import httpx
from typing import Annotated, Optional

from azure.identity.aio import DefaultAzureCredential
from agent_framework.azure import AzureAIAgentClient
from azure.ai.agentserver.agentframework import from_agent_framework
from azure.monitor.opentelemetry import configure_azure_monitor
from dotenv import load_dotenv

load_dotenv(override=True)

logger = logging.getLogger(__name__)

if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
    configure_azure_monitor(enable_live_metrics=True, logger_name="__main__")

ENDPOINT = os.getenv("FOUNDRY_PROJECT_ENDPOINT", "")
MODEL_DEPLOYMENT_NAME = os.getenv("FOUNDRY_MODEL_DEPLOYMENT_NAME", "")
EXTERNAL_API_KEY = os.getenv("EXTERNAL_API_KEY", "")


# ============================================
# HTTP Client Tools
# ============================================

async def fetch_data(
    url: Annotated[str, "The URL to fetch data from"],
    method: Annotated[str, "HTTP method (GET, POST)"] = "GET"
) -> str:
    """Fetch data from an external URL.

    Args:
        url: The endpoint URL
        method: HTTP method to use
    """
    async with httpx.AsyncClient() as client:
        try:
            if method.upper() == "GET":
                response = await client.get(url, timeout=30.0)
            else:
                response = await client.post(url, timeout=30.0)
            
            response.raise_for_status()
            return response.text
        except httpx.HTTPError as e:
            return f"Error fetching data: {str(e)}"


def search_api(
    query: Annotated[str, "The search query"],
    max_results: Annotated[int, "Maximum number of results to return"] = 5
) -> str:
    """Search using an external API.

    Args:
        query: Search terms
        max_results: Limit on results
    """
    # Example implementation - replace with actual API
    import httpx
    
    try:
        with httpx.Client() as client:
            response = client.get(
                "https://api.example.com/search",
                params={"q": query, "limit": max_results},
                headers={"Authorization": f"Bearer {EXTERNAL_API_KEY}"},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except Exception as e:
        return f"Search error: {str(e)}"


tools = [fetch_data, search_api]


async def run_server():
    credential = DefaultAzureCredential()
    
    try:
        client = AzureAIAgentClient(
            project_endpoint=ENDPOINT,
            model_deployment_name=MODEL_DEPLOYMENT_NAME,
            credential=credential,
        )
        
        agent = client.create_agent(
            name="APIAgent",
            model=MODEL_DEPLOYMENT_NAME,
            instructions="""You are an assistant that can fetch data from external APIs.
            
Use the provided tools to retrieve information as needed.""",
            tools=tools,
        )
        
        logger.info("Starting API Agent...")
        await from_agent_framework(agent).run_async()
    finally:
        await credential.close()


def main():
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
```

## Requirements.txt Template

```
# Core agent packages
agent-framework-azure-ai
agent-framework-core
azure-ai-agentserver-agentframework

# Web server (required by agent server)
uvicorn
fastapi

# Azure identity
azure-identity

# Environment
python-dotenv

# Monitoring
azure-monitor-opentelemetry

# Optional: HTTP client for external APIs
httpx

# Optional: For async operations
aiohttp
```

## Dockerfile Template

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY ./ user_agent/

WORKDIR /app/user_agent

RUN if [ -f requirements.txt ]; then \
        pip install --no-cache-dir -r requirements.txt; \
    else \
        echo "No requirements.txt found"; \
    fi

# Expose the agent port
EXPOSE 8088

# Set environment variables
ENV PORT=8088
ENV PYTHONUNBUFFERED=1

# Run the agent
CMD ["python", "main.py"]
```
