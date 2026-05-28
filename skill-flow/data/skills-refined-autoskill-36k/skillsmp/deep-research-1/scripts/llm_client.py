#!/usr/bin/env python3
"""
LLM Client Module - Unified interface for Gemini/OpenAI

Enhanced module for deep-research skill with improved error handling
and integration with the new environment management system.
"""

import os
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Import new modules
try:
    from .env_manager import get_env_manager
    from .error_handler import get_error_handler, ErrorType
except ImportError:
    # Fallback for direct execution
    from env_manager import get_env_manager
    from error_handler import get_error_handler, ErrorType

# Optional imports
_gemini_available = False
_openai_available = False

try:
    from google import genai
    _gemini_available = True
except ImportError:
    genai = None

try:
    from openai import OpenAI
    _openai_available = True
except ImportError:
    OpenAI = None


def gemini_complete(prompt: str, model: str = "gemini-2.0-flash") -> str:
    """Call Gemini API with enhanced error handling.

    Args:
        prompt: The prompt to send.
        model: Model name to use.

    Returns:
        Response text or mock response if API unavailable.
    """
    env_manager = get_env_manager()
    error_handler = get_error_handler()
    
    # Get API key from environment manager
    api_keys = env_manager.load_api_keys()
    api_key = api_keys.get("GEMINI_API_KEY")

    if not api_key:
        logger.warning("GEMINI_API_KEY not found, using mock response")
        return mock_response(prompt)

    if not _gemini_available or genai is None:
        logger.warning("google-generativeai not installed, using mock response")
        return mock_response(prompt)

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model=model, contents=prompt)
        return response.text or ""
    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        # Use error handler for better user experience
        if error_handler.should_fallback(e):
            logger.info("Falling back to mock response due to API error")
            return mock_response(prompt)
        return f"Error: {e}"


def openai_complete(prompt: str, model: str = "gpt-4o") -> str:
    """Call OpenAI API with enhanced error handling.

    Args:
        prompt: The prompt to send.
        model: Model name to use.

    Returns:
        Response text or mock response if API unavailable.
    """
    env_manager = get_env_manager()
    error_handler = get_error_handler()
    
    # Get API key from environment manager
    api_keys = env_manager.load_api_keys()
    api_key = api_keys.get("OPENAI_API_KEY")

    if not api_key:
        logger.warning("OPENAI_API_KEY not found, using mock response")
        return mock_response(prompt)

    if not _openai_available or OpenAI is None:
        logger.warning("openai not installed, using mock response")
        return mock_response(prompt)

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        # Use error handler for better user experience
        if error_handler.should_fallback(e):
            logger.info("Falling back to mock response due to API error")
            return mock_response(prompt)
        return f"Error: {e}"


def llm_complete(
    prompt: str, provider: Optional[str] = None, model: Optional[str] = None
) -> str:
    """Unified LLM interface with enhanced provider selection.

    Priority:
    1. Explicit provider argument
    2. LLM_PROVIDER env var
    3. Default to preferred provider from EnvManager
    4. Fall back to available provider
    5. Mock response

    Args:
        prompt: The prompt to send.
        provider: Optional provider override ('gemini' or 'openai').
        model: Optional model name override.

    Returns:
        Response text.
    """
    env_manager = get_env_manager()
    
    if not provider:
        provider = env_manager.get_preferred_provider()

    # Check if chosen provider is available
    api_keys = env_manager.load_api_keys()
    
    if provider == "openai" and "OPENAI_API_KEY" not in api_keys:
        logger.warning("OpenAI provider requested but no API key available, falling back")
        provider = "gemini" if "GEMINI_API_KEY" in api_keys else "mock"
    elif provider == "gemini" and "GEMINI_API_KEY" not in api_keys:
        logger.warning("Gemini provider requested but no API key available, falling back")
        provider = "openai" if "OPENAI_API_KEY" in api_keys else "mock"

    if provider == "openai":
        return openai_complete(prompt, model=model or "gpt-4o")
    elif provider == "gemini":
        return gemini_complete(prompt, model=model or "gemini-2.0-flash")
    else:
        logger.info("Using mock response (no valid provider available)")
        return mock_response(prompt)


def mock_response(prompt: str) -> str:
    """Fallback mock response when no API is available."""
    if "json" in prompt.lower():
        return json.dumps(
            {
                "steps": [
                    {"query": "topic overview", "rationale": "General information"},
                    {"query": "topic news", "rationale": "Recent updates"},
                    {"query": "topic analysis", "rationale": "Deep dive"},
                ]
            }
        )

    return """# Deep Research Report (Mock Mode)

⚠️ **API Key Missing - Using Mock Response**

This is a placeholder because no API key was found.

## To Enable Real LLM Responses:

```bash
# Option 1: Gemini (Recommended)
export GEMINI_API_KEY="your-key-here"

# Option 2: OpenAI
export OPENAI_API_KEY="your-key-here"

# Then run:
source scripts/load_env.sh
```

## Mock Summary

The research would normally contain:
- Executive Summary
- Key Findings
- Detailed Analysis
- Conclusions

---"""
