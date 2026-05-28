#!/usr/bin/env python3
"""
통합 LLM 클라이언트
여러 LLM 프로바이더(OpenAI, Gemini, Ollama 등)를 하나의 인터페이스로 제공합니다.
"""

import os
import json
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Generator
import requests


@dataclass
class LLMResponse:
    """LLM 응답 데이터 클래스"""
    content: str
    model: str
    provider: str
    usage: dict = field(default_factory=dict)
    latency: float = 0.0
    raw_response: dict = field(default_factory=dict)


@dataclass
class Message:
    """채팅 메시지"""
    role: str  # "system", "user", "assistant"
    content: str


class BaseLLMClient(ABC):
    """LLM 클라이언트 기본 클래스"""

    def __init__(self, model: str, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.model = model
        self.api_key = api_key
        self.base_url = base_url

    @abstractmethod
    def chat(self, messages: list[Message], **kwargs) -> LLMResponse:
        """채팅 완성 요청"""
        pass

    @abstractmethod
    def stream(self, messages: list[Message], **kwargs) -> Generator[str, None, None]:
        """스트리밍 응답"""
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass


class OpenAIClient(BaseLLMClient):
    """OpenAI API 클라이언트"""

    def __init__(self, model: str = "gpt-4o", api_key: Optional[str] = None, base_url: Optional[str] = None):
        super().__init__(model, api_key or os.getenv("OPENAI_API_KEY"), base_url or "https://api.openai.com/v1")

    @property
    def provider_name(self) -> str:
        return "openai"

    def chat(self, messages: list[Message], **kwargs) -> LLMResponse:
        start_time = time.time()
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            **kwargs
        }

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", 120)
        )
        response.raise_for_status()
        data = response.json()

        return LLMResponse(
            content=data["choices"][0]["message"]["content"],
            model=self.model,
            provider=self.provider_name,
            usage=data.get("usage", {}),
            latency=time.time() - start_time,
            raw_response=data
        )

    def stream(self, messages: list[Message], **kwargs) -> Generator[str, None, None]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "stream": True,
            **kwargs
        }

        with requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            stream=True,
            timeout=kwargs.get("timeout", 120)
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: ") and line != "data: [DONE]":
                        data = json.loads(line[6:])
                        if data["choices"][0].get("delta", {}).get("content"):
                            yield data["choices"][0]["delta"]["content"]


class GeminiClient(BaseLLMClient):
    """Google Gemini API 클라이언트"""

    def __init__(self, model: str = "gemini-2.0-flash", api_key: Optional[str] = None, base_url: Optional[str] = None):
        super().__init__(model, api_key or os.getenv("GOOGLE_API_KEY"), base_url or "https://generativelanguage.googleapis.com/v1beta")

    @property
    def provider_name(self) -> str:
        return "gemini"

    def _convert_messages(self, messages: list[Message]) -> tuple[Optional[str], list[dict]]:
        """OpenAI 형식 메시지를 Gemini 형식으로 변환"""
        system_instruction = None
        contents = []

        for msg in messages:
            if msg.role == "system":
                system_instruction = msg.content
            else:
                role = "user" if msg.role == "user" else "model"
                contents.append({"role": role, "parts": [{"text": msg.content}]})

        return system_instruction, contents

    def chat(self, messages: list[Message], **kwargs) -> LLMResponse:
        start_time = time.time()
        system_instruction, contents = self._convert_messages(messages)

        payload = {"contents": contents}
        if system_instruction:
            payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

        generation_config = {}
        if "temperature" in kwargs:
            generation_config["temperature"] = kwargs["temperature"]
        if "max_tokens" in kwargs:
            generation_config["maxOutputTokens"] = kwargs["max_tokens"]
        if generation_config:
            payload["generationConfig"] = generation_config

        response = requests.post(
            f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=kwargs.get("timeout", 120)
        )
        response.raise_for_status()
        data = response.json()

        content = data["candidates"][0]["content"]["parts"][0]["text"]
        usage = {}
        if "usageMetadata" in data:
            usage = {
                "prompt_tokens": data["usageMetadata"].get("promptTokenCount", 0),
                "completion_tokens": data["usageMetadata"].get("candidatesTokenCount", 0),
                "total_tokens": data["usageMetadata"].get("totalTokenCount", 0)
            }

        return LLMResponse(
            content=content,
            model=self.model,
            provider=self.provider_name,
            usage=usage,
            latency=time.time() - start_time,
            raw_response=data
        )

    def stream(self, messages: list[Message], **kwargs) -> Generator[str, None, None]:
        system_instruction, contents = self._convert_messages(messages)

        payload = {"contents": contents}
        if system_instruction:
            payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

        with requests.post(
            f"{self.base_url}/models/{self.model}:streamGenerateContent?key={self.api_key}&alt=sse",
            headers={"Content-Type": "application/json"},
            json=payload,
            stream=True,
            timeout=kwargs.get("timeout", 120)
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        data = json.loads(line[6:])
                        if "candidates" in data:
                            parts = data["candidates"][0].get("content", {}).get("parts", [])
                            if parts and "text" in parts[0]:
                                yield parts[0]["text"]


class OllamaClient(BaseLLMClient):
    """Ollama 로컬 LLM 클라이언트"""

    def __init__(self, model: str = "llama3.2", api_key: Optional[str] = None, base_url: Optional[str] = None):
        super().__init__(model, api_key, base_url or os.getenv("OLLAMA_HOST", "http://localhost:11434"))

    @property
    def provider_name(self) -> str:
        return "ollama"

    def chat(self, messages: list[Message], **kwargs) -> LLMResponse:
        start_time = time.time()
        payload = {
            "model": self.model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "stream": False,
            "options": {}
        }

        if "temperature" in kwargs:
            payload["options"]["temperature"] = kwargs["temperature"]

        response = requests.post(
            f"{self.base_url}/api/chat",
            json=payload,
            timeout=kwargs.get("timeout", 120)
        )
        response.raise_for_status()
        data = response.json()

        return LLMResponse(
            content=data["message"]["content"],
            model=self.model,
            provider=self.provider_name,
            usage={
                "prompt_tokens": data.get("prompt_eval_count", 0),
                "completion_tokens": data.get("eval_count", 0),
                "total_tokens": data.get("prompt_eval_count", 0) + data.get("eval_count", 0)
            },
            latency=time.time() - start_time,
            raw_response=data
        )

    def stream(self, messages: list[Message], **kwargs) -> Generator[str, None, None]:
        payload = {
            "model": self.model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "stream": True
        }

        with requests.post(
            f"{self.base_url}/api/chat",
            json=payload,
            stream=True,
            timeout=kwargs.get("timeout", 120)
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if "message" in data and "content" in data["message"]:
                        yield data["message"]["content"]


class AnthropicClient(BaseLLMClient):
    """Anthropic Claude API 클라이언트"""

    def __init__(self, model: str = "claude-sonnet-4-20250514", api_key: Optional[str] = None, base_url: Optional[str] = None):
        super().__init__(model, api_key or os.getenv("ANTHROPIC_API_KEY"), base_url or "https://api.anthropic.com/v1")

    @property
    def provider_name(self) -> str:
        return "anthropic"

    def chat(self, messages: list[Message], **kwargs) -> LLMResponse:
        start_time = time.time()

        system_content = None
        chat_messages = []
        for msg in messages:
            if msg.role == "system":
                system_content = msg.content
            else:
                chat_messages.append({"role": msg.role, "content": msg.content})

        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        payload = {
            "model": self.model,
            "messages": chat_messages,
            "max_tokens": kwargs.get("max_tokens", 4096)
        }
        if system_content:
            payload["system"] = system_content
        if "temperature" in kwargs:
            payload["temperature"] = kwargs["temperature"]

        response = requests.post(
            f"{self.base_url}/messages",
            headers=headers,
            json=payload,
            timeout=kwargs.get("timeout", 120)
        )
        response.raise_for_status()
        data = response.json()

        return LLMResponse(
            content=data["content"][0]["text"],
            model=self.model,
            provider=self.provider_name,
            usage={
                "prompt_tokens": data.get("usage", {}).get("input_tokens", 0),
                "completion_tokens": data.get("usage", {}).get("output_tokens", 0),
                "total_tokens": data.get("usage", {}).get("input_tokens", 0) + data.get("usage", {}).get("output_tokens", 0)
            },
            latency=time.time() - start_time,
            raw_response=data
        )

    def stream(self, messages: list[Message], **kwargs) -> Generator[str, None, None]:
        system_content = None
        chat_messages = []
        for msg in messages:
            if msg.role == "system":
                system_content = msg.content
            else:
                chat_messages.append({"role": msg.role, "content": msg.content})

        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        payload = {
            "model": self.model,
            "messages": chat_messages,
            "max_tokens": kwargs.get("max_tokens", 4096),
            "stream": True
        }
        if system_content:
            payload["system"] = system_content

        with requests.post(
            f"{self.base_url}/messages",
            headers=headers,
            json=payload,
            stream=True,
            timeout=kwargs.get("timeout", 120)
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        data = json.loads(line[6:])
                        if data.get("type") == "content_block_delta":
                            yield data.get("delta", {}).get("text", "")


class LLMClientFactory:
    """LLM 클라이언트 팩토리"""

    PROVIDERS = {
        "openai": OpenAIClient,
        "gemini": GeminiClient,
        "google": GeminiClient,
        "ollama": OllamaClient,
        "anthropic": AnthropicClient,
        "claude": AnthropicClient
    }

    @classmethod
    def create(cls, provider: str, model: Optional[str] = None, **kwargs) -> BaseLLMClient:
        """프로바이더에 맞는 LLM 클라이언트 생성"""
        provider = provider.lower()
        if provider not in cls.PROVIDERS:
            raise ValueError(f"Unknown provider: {provider}. Available: {list(cls.PROVIDERS.keys())}")

        client_class = cls.PROVIDERS[provider]
        if model:
            return client_class(model=model, **kwargs)
        return client_class(**kwargs)

    @classmethod
    def available_providers(cls) -> list[str]:
        return list(cls.PROVIDERS.keys())


def main():
    """테스트 및 CLI 사용"""
    import argparse

    parser = argparse.ArgumentParser(description="LLM 클라이언트 테스트")
    parser.add_argument("--provider", default="openai", help="LLM 프로바이더")
    parser.add_argument("--model", help="모델명")
    parser.add_argument("--prompt", default="Hello, who are you?", help="테스트 프롬프트")
    parser.add_argument("--system", help="시스템 프롬프트")
    parser.add_argument("--stream", action="store_true", help="스트리밍 모드")

    args = parser.parse_args()

    client = LLMClientFactory.create(args.provider, args.model)
    messages = []
    if args.system:
        messages.append(Message(role="system", content=args.system))
    messages.append(Message(role="user", content=args.prompt))

    print(f"Provider: {client.provider_name}")
    print(f"Model: {client.model}")
    print("-" * 50)

    if args.stream:
        print("Response (streaming):")
        for chunk in client.stream(messages):
            print(chunk, end="", flush=True)
        print()
    else:
        response = client.chat(messages)
        print(f"Response: {response.content}")
        print(f"Latency: {response.latency:.2f}s")
        print(f"Usage: {response.usage}")


if __name__ == "__main__":
    main()
