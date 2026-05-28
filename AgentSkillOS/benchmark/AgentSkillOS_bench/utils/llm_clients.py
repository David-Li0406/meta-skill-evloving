"""
LLM client utilities.

Two backends:
- "openai": OpenAI-compatible API (OpenAI, vLLM, Ollama, etc.)
- "claude_code": Claude Code SDK (same agent as the runner)

Usage:
    # Use default backend (claude_code)
    text = await query_llm(prompt="...", system="...")

    # Override backend
    text = await query_llm(prompt="...", system="...", backend="openai")

    # Change global default
    set_llm_backend("openai")
"""
import base64
from typing import Optional, List


def _detect_image_mime(data: bytes) -> str:
    """Detect image MIME type from file header magic bytes.

    Falls back to ``image/png`` if the format is unrecognised.
    """
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return "image/png"
    if data[:3] == b"\xff\xd8\xff":
        return "image/jpeg"
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return "image/gif"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "image/webp"
    if data[:2] == b"BM":
        return "image/bmp"
    return "image/png"

# ---------- Global default backend ----------
_default_backend: str = "claude_code"

# ---------- Global default OpenAI params ----------
_openai_defaults: dict = {}

# ---------- Global default Claude Code params ----------
_claude_code_defaults: dict = {}


def set_llm_backend(backend: str) -> None:
    """Set the global default LLM backend.

    Args:
        backend: "claude_code" or "openai"
    """
    global _default_backend
    if backend not in ("claude_code", "openai"):
        raise ValueError(f"Unknown backend: {backend!r}. Must be 'claude_code' or 'openai'.")
    _default_backend = backend


def get_llm_backend() -> str:
    """Get the current global default LLM backend."""
    return _default_backend


def set_openai_defaults(**kwargs) -> None:
    """Set global default parameters for the OpenAI backend.

    Accepted keys: model, base_url, api_key.
    These are used as fallbacks when query_openai() is called without
    explicit values (e.g., from llm_judge evaluators).
    """
    global _openai_defaults
    _openai_defaults = {k: v for k, v in kwargs.items() if v is not None}


def get_openai_defaults() -> dict:
    """Get the current global default OpenAI parameters."""
    return dict(_openai_defaults)


def set_claude_code_defaults(**kwargs) -> None:
    """Set global default parameters for the Claude Code backend.

    Accepted keys: model.
    These are used as fallbacks when query_claude_code() is called without
    explicit values (e.g., from llm_judge evaluators).
    """
    global _claude_code_defaults
    _claude_code_defaults = {k: v for k, v in kwargs.items() if v is not None}


def get_claude_code_defaults() -> dict:
    """Get the current global default Claude Code parameters."""
    return dict(_claude_code_defaults)


# ---------- Unified entry ----------

async def query_llm(
    prompt: str,
    system: str = "",
    backend: Optional[str] = None,
    **kwargs,
) -> str:
    """
    Query an LLM using the specified (or default) backend.

    Args:
        prompt: User message / task prompt
        system: System message (ignored by claude_code backend)
        backend: "openai" or "claude_code" (default: global setting)
        **kwargs: Backend-specific arguments, forwarded as-is

    Returns:
        Response text
    """
    backend = backend or _default_backend

    if backend == "openai":
        return await query_openai(prompt=prompt, system=system, **kwargs)
    elif backend == "claude_code":
        return await query_claude_code(prompt=prompt, system=system, **kwargs)
    else:
        raise ValueError(f"Unknown backend: {backend!r}")


# ---------- Backend: OpenAI-compatible ----------

async def query_openai(
    prompt: str,
    system: str = "",
    model: str = "gpt-5.2",
    max_tokens: int = 512,
    temperature: float = 0.0,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    images: Optional[List[bytes]] = None,
    **kwargs,
) -> str:
    """
    Query an OpenAI-compatible API.

    Compatible with OpenAI, Anthropic (via proxy), vLLM, Ollama, etc.
    Falls back to global defaults set via set_openai_defaults().

    Args:
        images: Optional list of PNG image bytes to include as vision input.
    """
    from openai import AsyncOpenAI

    # Apply global defaults for params not explicitly provided
    defaults = _openai_defaults
    if model == "gpt-5.2" and "model" in defaults:
        model = defaults["model"]
    if base_url is None:
        base_url = defaults.get("base_url")
    if api_key is None:
        api_key = defaults.get("api_key")

    client_kwargs = {}
    if base_url:
        client_kwargs["base_url"] = base_url
    if api_key:
        client_kwargs["api_key"] = api_key

    client = AsyncOpenAI(**client_kwargs)

    messages = []
    if system:
        messages.append({"role": "system", "content": system})

    if images:
        # Multipart content: text + images (OpenAI Vision format)
        content = [{"type": "text", "text": prompt}]
        for img_bytes in images:
            b64 = base64.b64encode(img_bytes).decode()
            mime = _detect_image_mime(img_bytes)
            content.append({
                "type": "image_url",
                "image_url": {"url": f"data:{mime};base64,{b64}"},
            })
        messages.append({"role": "user", "content": content})
    else:
        messages.append({"role": "user", "content": prompt})

    response = await client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    return response.choices[0].message.content


# ---------- Backend: Claude Code SDK ----------

async def query_claude_code(
    prompt: str,
    system: str = "",
    cwd: Optional[str] = None,
    model: Optional[str] = None,
    max_turns: int = 50,
    **kwargs,
) -> str:
    """
    Query using Claude Code SDK (claude_agent_sdk).

    The agent can read files, run code, and use tools — making it a
    more powerful judge that can verify claims against actual code.
    """
    from claude_agent_sdk import (
        query, ClaudeAgentOptions,
        AssistantMessage, ResultMessage, TextBlock,
    )

    # Prepend system instructions into the prompt (SDK has no separate system param)
    full_prompt = f"{system}\n\n{prompt}" if system else prompt
    full_prompt = full_prompt.replace("\x00", "")  # Remove null bytes that break SDK calls

    # Apply global defaults for params not explicitly provided
    defaults = _claude_code_defaults
    if model is None and "model" in defaults:
        model = defaults["model"]

    options = ClaudeAgentOptions(
        permission_mode="bypassPermissions",
        max_turns=max_turns,
        max_buffer_size=10 * 1024 * 1024,  # 10MB, default 1MB is too small for large files
    )
    if cwd:
        options.cwd = cwd
    if model:
        options.model = model

    text_parts = []
    result_text = ""
    try:
        async for message in query(prompt=full_prompt, options=options):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        text_parts.append(block.text)
            elif isinstance(message, ResultMessage):
                if message.result:
                    result_text = message.result
    except Exception as e:
        # Try to extract stderr details from the exception chain
        stderr_info = ""
        cur = e
        while cur is not None:
            if hasattr(cur, "stderr"):
                stderr_info = f" | stderr: {cur.stderr}"
                break
            cur = cur.__cause__ if cur.__cause__ else cur.__context__
            if cur is e:
                break
        raise RuntimeError(
            f"{e} (prompt length: {len(full_prompt)} chars){stderr_info}"
        ) from e

    # Prefer ResultMessage.result (final answer); fall back to collected TextBlocks
    return result_text or "\n".join(text_parts)
