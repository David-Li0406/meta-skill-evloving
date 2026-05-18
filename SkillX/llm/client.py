"""LLM client for SkillX."""

import asyncio
import os
import re
import logging
from typing import Optional, Callable, Any, List, Tuple, Union

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

logger = logging.getLogger(__name__)


MessageType = Tuple[str, str]  # (role, content)
Messages = List[Union[MessageType, HumanMessage, SystemMessage, AIMessage]]


class LLM:
    """
    Unified LLM client with retry logic and error handling.

    Supports async invocation with regex validation/extraction.
    Automatically handles rate limits and token limits.
    """

    def __init__(
        self,
        model: str = "gpt-4.1-2025-04-14",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        max_tokens: int = 10240,
        temperature: float = 0.9,
        max_retries: int = 10,
        retry_delay: int = 3,
        timeout: int = 60,
        **kwargs
    ):
        """
        Initialize LLM client.

        Args:
            model: Model name
            api_key: API key (defaults to OPENAI_API_KEY env var)
            base_url: Base URL for API (defaults to OPENAI_BASE_URL env var)
            max_tokens: Maximum tokens for response
            temperature: Sampling temperature
            max_retries: Maximum retry attempts
            retry_delay: Delay between retries in seconds
            timeout: Request timeout in seconds
            **kwargs: Additional ChatOpenAI parameters
        """
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or ""
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL") or ""
        self.initial_max_tokens = max_tokens
        self.current_max_tokens = max_tokens
        self.temperature = temperature
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.timeout = timeout
        self.kwargs = kwargs

        self._init_client()

    def _init_client(self) -> None:
        """Initialize ChatOpenAI client."""
        self.client = ChatOpenAI(
            model=self.model,
            api_key=self.api_key,
            base_url=self.base_url if self.base_url else None,
            max_tokens=self.current_max_tokens,
            temperature=self.temperature,
            timeout=self.timeout,
            extra_body={"chat_template_kwargs": {"enable_thinking": False}},
            **self.kwargs
        )

    def _update_max_tokens(self, new_max_tokens: int) -> None:
        """Update max_tokens and reinitialize client."""
        self.current_max_tokens = new_max_tokens
        logger.info(f"Reducing max_tokens to {self.current_max_tokens}")
        self._init_client()

    def _reset_max_tokens(self) -> None:
        """Reset max_tokens to initial value."""
        if self.current_max_tokens != self.initial_max_tokens:
            self.current_max_tokens = self.initial_max_tokens
            self._init_client()

    def _convert_messages(self, messages: Messages) -> List:
        """Convert message tuples to LangChain message objects."""
        converted = []
        for msg in messages:
            if isinstance(msg, tuple):
                role, content = msg
                if role == "system":
                    converted.append(SystemMessage(content=content))
                elif role == "human" or role == "user":
                    converted.append(HumanMessage(content=content))
                elif role == "assistant" or role == "ai":
                    converted.append(AIMessage(content=content))
                else:
                    converted.append(HumanMessage(content=content))
            else:
                converted.append(msg)
        return converted

    async def ainvoke(
        self,
        messages: Messages,
        regex_pattern: Optional[str] = None,
        regex_extractor: Optional[Callable[[str], Any]] = None,
        **kwargs
    ) -> str:
        """
        Async invoke LLM with retry logic.

        Args:
            messages: List of message tuples (role, content) or LangChain messages
            regex_pattern: Optional regex pattern to validate output
            regex_extractor: Optional function to extract/validate output.
                            Should return None if extraction fails (triggers retry).
            **kwargs: Additional invocation parameters

        Returns:
            LLM response text

        Raises:
            Exception: If all retries fail
        """
        retry_count = 0
        converted_messages = self._convert_messages(messages)

        # Small delay to prevent burst traffic
        await asyncio.sleep(0.3)

        while retry_count < self.max_retries:
            try:
                response = await self.client.ainvoke(
                    converted_messages,
                    extra_body={"chat_template_kwargs": {"enable_thinking": False}}
                )
                response_text = response.content

                logger.debug(f"LLM Response (attempt {retry_count + 1})")

                # Validate with regex extractor function
                if regex_extractor:
                    extracted = regex_extractor(response_text)
                    if extracted is None:
                        logger.warning(
                            f"Regex extraction failed, retrying... "
                            f"(attempt {retry_count + 1})"
                        )
                        retry_count += 1
                        await asyncio.sleep(self.retry_delay)
                        continue
                    logger.debug("Regex extraction successful")

                # Validate with regex pattern (legacy support)
                elif regex_pattern:
                    if not re.search(regex_pattern, response_text):
                        logger.warning(
                            f"Regex pattern not found, retrying... "
                            f"(attempt {retry_count + 1})"
                        )
                        retry_count += 1
                        await asyncio.sleep(self.retry_delay)
                        continue

                # Success - reset tokens and return
                self._reset_max_tokens()
                return response_text

            except Exception as e:
                error_message = str(e).lower()
                logger.error(f"Error on attempt {retry_count + 1}: {e}")

                # Handle token limit errors
                if any(keyword in error_message for keyword in [
                    'maximum context length',
                    'max_tokens',
                    'token limit',
                    'context_length_exceeded'
                ]):
                    new_max_tokens = max(self.current_max_tokens // 2, 100)
                    if new_max_tokens < 100:
                        logger.error("max_tokens too small, cannot retry")
                        raise

                    self._update_max_tokens(new_max_tokens)
                    retry_count += 1
                    await asyncio.sleep(self.retry_delay)
                    continue

                # Handle rate limit errors (exponential backoff)
                elif any(keyword in error_message for keyword in [
                    'rate limit',
                    'rate_limit_exceeded',
                    'too many requests',
                    '429'
                ]):
                    # Exponential backoff: 3, 6, 12, 24, 48...
                    sleep_time = self.retry_delay * (2 ** retry_count)
                    # Cap at 60 seconds max
                    sleep_time = min(sleep_time, 60)
                    logger.warning(
                        f"Rate limit hit, sleeping for {sleep_time} seconds..."
                    )
                    await asyncio.sleep(sleep_time)
                    retry_count += 1
                    continue

                # Handle other errors
                else:
                    retry_count += 1
                    if retry_count >= self.max_retries:
                        logger.error(
                            f"Max retries ({self.max_retries}) reached, giving up"
                        )
                        raise

                    logger.info(f"Retrying in {self.retry_delay} seconds...")
                    await asyncio.sleep(self.retry_delay)

        raise Exception(f"Failed after {self.max_retries} retries")

    def invoke(
        self,
        messages: Messages,
        regex_pattern: Optional[str] = None,
        regex_extractor: Optional[Callable[[str], Any]] = None,
        **kwargs
    ) -> str:
        """
        Synchronous invoke wrapper.

        Args:
            Same as ainvoke

        Returns:
            LLM response text
        """
        return asyncio.run(
            self.ainvoke(messages, regex_pattern, regex_extractor, **kwargs)
        )
