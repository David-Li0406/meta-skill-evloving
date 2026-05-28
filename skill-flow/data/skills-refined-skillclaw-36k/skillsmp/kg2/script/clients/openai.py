"""OpenAI API client."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

from ..constants import (
    DEFAULT_EMBEDDING_MODEL,
    DEFAULT_OPENAI_MODEL,
    OPENAI_API_URL,
    OPENAI_TIMEOUT_SECONDS,
)


class OpenAIClient:
    """OpenAI API client with Structured Outputs and Embeddings support."""

    BASE_URL = OPENAI_API_URL
    EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"

    def __init__(self, api_key: str, model: str = DEFAULT_OPENAI_MODEL,
                 embedding_model: str = DEFAULT_EMBEDDING_MODEL):
        self.api_key = api_key
        self.model = model
        self.embedding_model = embedding_model

    def structured_completion(
        self,
        messages: list[dict[str, str]],
        schema: dict[str, Any],
        schema_name: str = "response",
    ) -> dict[str, Any]:
        """Get structured completion using JSON Schema.

        Args:
            messages: Chat messages
            schema: JSON Schema for the response
            schema_name: Name for the schema

        Returns:
            Parsed JSON response matching the schema
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": schema_name,
                    "strict": True,
                    "schema": schema,
                }
            }
        }

        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(self.BASE_URL, data=data, method='POST')
        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', f'Bearer {self.api_key}')

        try:
            with urllib.request.urlopen(req, timeout=OPENAI_TIMEOUT_SECONDS) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                content = result['choices'][0]['message']['content']
                return json.loads(content)
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8') if e.fp else str(e)
            raise RuntimeError(f"OpenAI API error ({e.code}): {body}") from e

    def embed(self, text: str) -> list[float]:
        """Get embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector
        """
        return self.embed_batch([text])[0]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Get embeddings for multiple texts.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors (same order as input)
        """
        if not texts:
            return []

        payload = {
            "model": self.embedding_model,
            "input": texts,
        }

        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(self.EMBEDDINGS_URL, data=data, method='POST')
        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', f'Bearer {self.api_key}')

        try:
            with urllib.request.urlopen(req, timeout=OPENAI_TIMEOUT_SECONDS) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                # Sort by index to ensure correct order
                embeddings_data = sorted(result['data'], key=lambda x: x['index'])
                return [item['embedding'] for item in embeddings_data]
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8') if e.fp else str(e)
            raise RuntimeError(f"OpenAI Embeddings API error ({e.code}): {body}") from e

    def embed_paper(self, title: str, abstract: str | None) -> list[float]:
        """Get embedding for a paper using title and abstract.

        Args:
            title: Paper title
            abstract: Paper abstract (optional)

        Returns:
            Embedding vector
        """
        if abstract:
            text = f"{title}\n\n{abstract}"
        else:
            text = title
        return self.embed(text)
