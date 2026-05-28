"""
BAML Python Usage Examples

This file demonstrates common patterns for calling BAML functions from Python.
Assumes you have run `baml-cli generate` and have a baml_client/ directory.
"""

import asyncio
from typing import List

# =============================================================================
# IMPORTS
# =============================================================================

# Sync client
from baml_client import b

# Async client (same interface, just async)
from baml_client.async_client import b as b_async

# Types (generated from your BAML classes/enums)
from baml_client.types import Resume, Message, EmailClassification

# Multimodal inputs
from baml_py import Image, Audio, Pdf

# Error handling
from baml_py.errors import (
    BamlError,
    BamlValidationError,
    BamlClientError,
    BamlClientHttpError,
)
from baml_py import BamlAbortError, AbortController


# =============================================================================
# BASIC CALLS
# =============================================================================

def basic_sync_call():
    """Simple synchronous function call."""
    resume = b.ExtractResume("John Doe, Python developer at Acme Corp...")
    print(f"Name: {resume.name}")
    print(f"Skills: {resume.skills}")


async def basic_async_call():
    """Simple asynchronous function call."""
    resume = await b_async.ExtractResume("John Doe, Python developer...")
    return resume


# =============================================================================
# STREAMING
# =============================================================================

def streaming_sync():
    """Stream results synchronously."""
    stream = b.stream.ExtractResume("John Doe, Python developer...")

    for partial in stream:
        # partial is a Resume with fields populated as they arrive
        print(f"Name so far: {partial.name}")
        print(f"Skills so far: {partial.skills}")

    # Get the complete result
    final = stream.get_final_response()
    print(f"Final result: {final}")


async def streaming_async():
    """Stream results asynchronously."""
    stream = b_async.stream.ExtractResume("John Doe, Python developer...")

    async for partial in stream:
        print(f"Partial: {partial}")

    final = await stream.get_final_response()
    return final


# =============================================================================
# ERROR HANDLING
# =============================================================================

def handle_errors():
    """Demonstrate error handling patterns."""
    try:
        result = b.ExtractResume("some text")
    except BamlValidationError as e:
        # LLM returned something that couldn't be parsed
        print(f"Parse error: {e.message}")
        print(f"Raw LLM output: {e.raw_output}")
        print(f"Original prompt: {e.prompt}")
    except BamlClientHttpError as e:
        # HTTP error from the LLM provider
        print(f"HTTP {e.status_code}: {e.message}")
    except BamlClientError as e:
        # Other client errors
        print(f"Client error: {e.message}")
    except BamlError as e:
        # Catch-all for BAML errors
        print(f"BAML error: {e}")


# =============================================================================
# MULTIMODAL INPUTS
# =============================================================================

async def multimodal_examples():
    """Working with images, audio, and PDFs."""

    # Image from URL
    result = await b_async.AnalyzeImage(
        img=Image.from_url("https://example.com/image.png")
    )

    # Image from file
    result = await b_async.AnalyzeImage(
        img=Image.from_file("./screenshot.png")
    )

    # Image from base64
    import base64
    with open("image.png", "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    result = await b_async.AnalyzeImage(
        img=Image.from_base64("image/png", b64)
    )

    # PDF (base64 only for most providers)
    with open("document.pdf", "rb") as f:
        pdf_b64 = base64.b64encode(f.read()).decode()
    result = await b_async.SummarizePdf(
        doc=Pdf.from_base64("application/pdf", pdf_b64)
    )


# =============================================================================
# CONCURRENT CALLS
# =============================================================================

async def parallel_calls():
    """Run multiple BAML calls in parallel."""
    texts = [
        "First email content...",
        "Second email content...",
        "Third email content...",
    ]

    # Run all classifications in parallel
    results = await asyncio.gather(*[
        b_async.ClassifyEmail(text) for text in texts
    ])

    for text, result in zip(texts, results):
        print(f"{text[:20]}... -> {result.category}")


# =============================================================================
# CANCELLATION
# =============================================================================

async def cancellation_example():
    """Cancel a long-running request."""
    controller = AbortController()

    # Start the request
    task = asyncio.create_task(
        b_async.ExtractResume(
            "Very long resume text...",
            baml_options={"abort_controller": controller}
        )
    )

    # Cancel after 5 seconds
    await asyncio.sleep(5)
    controller.abort()

    try:
        result = await task
    except BamlAbortError:
        print("Request was cancelled")


async def timeout_with_controller():
    """Timeout using AbortController."""
    controller = AbortController(timeout_ms=5000)  # 5 second timeout

    try:
        result = await b_async.ExtractResume(
            "Resume text...",
            baml_options={"abort_controller": controller}
        )
    except BamlAbortError:
        print("Request timed out")


# =============================================================================
# CHAT / MULTI-TURN
# =============================================================================

async def chat_example():
    """Multi-turn conversation with message history."""
    messages: List[Message] = []

    # First turn
    messages.append(Message(role="user", content="What is Python?"))
    response = await b_async.Chat(messages)
    messages.append(Message(role="assistant", content=response))

    # Second turn
    messages.append(Message(role="user", content="How do I install it?"))
    response = await b_async.Chat(messages)

    return response


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    # Run sync examples
    basic_sync_call()
    streaming_sync()
    handle_errors()

    # Run async examples
    asyncio.run(basic_async_call())
    asyncio.run(streaming_async())
    asyncio.run(parallel_calls())
    asyncio.run(chat_example())
