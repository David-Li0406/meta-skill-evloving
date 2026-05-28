---
id: local-llm-ollama
name: "Local LLM (Ollama)"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Local LLM (Ollama)

## Overview

Ollama enables running large language models locally, providing privacy, cost savings, and offline capability. It supports models like Llama 3, Mistral, CodeLlama, Phi-3, and many others with a simple interface similar to Docker.

## When to Use

- Data privacy requirements (no external API calls)
- Offline or air-gapped environments
- Cost elimination for high-volume tasks
- Development and testing without API costs
- Custom fine-tuned model deployment
- Edge computing and embedded systems

## Key Concepts

### Popular Models

| Model | Size | Best For | RAM Required |
|-------|------|----------|--------------|
| llama3.1:8b | 4.7GB | General purpose | 8GB |
| llama3.1:70b | 40GB | Complex reasoning | 48GB |
| mistral:7b | 4.1GB | Fast, efficient | 8GB |
| codellama:13b | 7.4GB | Code generation | 16GB |
| phi3:mini | 2.3GB | Lightweight, fast | 4GB |
| deepseek-coder:6.7b | 3.8GB | Code, instruction | 8GB |
| mixtral:8x7b | 26GB | Mixture of experts | 32GB |

### Architecture

```
┌─────────────────┐
│   Your App      │
└────────┬────────┘
         │ HTTP API (port 11434)
┌────────▼────────┐
│  Ollama Server  │
├─────────────────┤
│  Model Runtime  │
├─────────────────┤
│  GPU/CPU Layer  │
└─────────────────┘
```

## Implementation

### Installation and Setup

```bash
# Install Ollama (Linux)
curl -fsSL https://ollama.com/install.sh | sh

# Install Ollama (macOS)
brew install ollama

# Start server
ollama serve

# Pull a model
ollama pull llama3.1:8b

# List models
ollama list

# Run interactive chat
ollama run llama3.1:8b
```

### Basic Python Integration

```python
import requests
import json

OLLAMA_URL = "http://localhost:11434"

def generate(prompt: str, model: str = "llama3.1:8b") -> str:
    """Simple generation with Ollama."""
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]

def chat(messages: list, model: str = "llama3.1:8b") -> str:
    """Chat completion with message history."""
    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": model,
            "messages": messages,
            "stream": False
        }
    )
    return response.json()["message"]["content"]

# Usage
result = generate("Explain Docker in one paragraph")
print(result)

messages = [
    {"role": "system", "content": "You are a Python expert."},
    {"role": "user", "content": "What's the best way to handle exceptions?"}
]
result = chat(messages)
print(result)
```

### Streaming Responses

```python
def stream_generate(prompt: str, model: str = "llama3.1:8b"):
    """Stream response tokens in real-time."""
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": True
        },
        stream=True
    )

    full_response = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line)
            token = data.get("response", "")
            print(token, end="", flush=True)
            full_response += token

            if data.get("done"):
                break

    return full_response
```

### Using Official Python Library

```python
import ollama

# Simple generation
response = ollama.generate(
    model="llama3.1:8b",
    prompt="Write a haiku about programming"
)
print(response["response"])

# Chat with history
response = ollama.chat(
    model="llama3.1:8b",
    messages=[
        {"role": "user", "content": "Why is the sky blue?"}
    ]
)
print(response["message"]["content"])

# Streaming
stream = ollama.chat(
    model="llama3.1:8b",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)
```

### Embeddings

```python
def get_embedding(text: str, model: str = "nomic-embed-text") -> list:
    """Generate embeddings locally."""
    response = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={
            "model": model,
            "prompt": text
        }
    )
    return response.json()["embedding"]

# Using ollama library
response = ollama.embeddings(
    model="nomic-embed-text",
    prompt="Hello world"
)
embedding = response["embedding"]
print(f"Embedding dimension: {len(embedding)}")
```

### Custom Model Configuration

```python
def create_model_with_config():
    """Create custom model with specific parameters."""
    modelfile = """
FROM llama3.1:8b
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER num_ctx 4096
SYSTEM You are a helpful coding assistant specializing in Python.
"""

    response = requests.post(
        f"{OLLAMA_URL}/api/create",
        json={
            "name": "python-assistant",
            "modelfile": modelfile
        }
    )
    return response.json()
```

### Modelfile Examples

```dockerfile
# Modelfile.coding
FROM codellama:13b
PARAMETER temperature 0.2
PARAMETER num_ctx 8192
SYSTEM """You are an expert programmer.
- Write clean, documented code
- Explain your reasoning
- Include error handling
- Follow best practices"""

# Modelfile.creative
FROM llama3.1:8b
PARAMETER temperature 1.0
PARAMETER top_p 0.95
PARAMETER top_k 100
SYSTEM "You are a creative writer with vivid imagination."
```

```bash
# Build custom model
ollama create python-coder -f Modelfile.coding
```

### OpenAI-Compatible API

```python
from openai import OpenAI

# Ollama exposes OpenAI-compatible endpoint
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Not required but needed for client
)

response = client.chat.completions.create(
    model="llama3.1:8b",
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
    ]
)
print(response.choices[0].message.content)
```

### Async Implementation

```python
import aiohttp
import asyncio

async def async_generate(prompt: str, model: str = "llama3.1:8b") -> str:
    """Async generation for concurrent requests."""
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False}
        ) as response:
            data = await response.json()
            return data["response"]

async def batch_generate(prompts: list[str]) -> list[str]:
    """Process multiple prompts concurrently."""
    tasks = [async_generate(p) for p in prompts]
    return await asyncio.gather(*tasks)
```

### Production Service Class

```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import logging

@dataclass
class OllamaConfig:
    model: str = "llama3.1:8b"
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 40
    num_ctx: int = 4096
    base_url: str = "http://localhost:11434"

class OllamaService:
    """Production-ready Ollama service."""

    def __init__(self, config: Optional[OllamaConfig] = None):
        self.config = config or OllamaConfig()
        self.logger = logging.getLogger(__name__)

    def is_available(self) -> bool:
        """Check if Ollama server is running."""
        try:
            response = requests.get(f"{self.config.base_url}/api/tags")
            return response.status_code == 200
        except:
            return False

    def list_models(self) -> List[str]:
        """Get available models."""
        response = requests.get(f"{self.config.base_url}/api/tags")
        return [m["name"] for m in response.json()["models"]]

    def generate(
        self,
        prompt: str,
        system: str = "",
        **kwargs
    ) -> Dict[str, Any]:
        """Generate completion."""
        options = {
            "temperature": kwargs.get("temperature", self.config.temperature),
            "top_p": kwargs.get("top_p", self.config.top_p),
            "top_k": kwargs.get("top_k", self.config.top_k),
            "num_ctx": kwargs.get("num_ctx", self.config.num_ctx)
        }

        try:
            response = requests.post(
                f"{self.config.base_url}/api/generate",
                json={
                    "model": kwargs.get("model", self.config.model),
                    "prompt": prompt,
                    "system": system,
                    "stream": False,
                    "options": options
                },
                timeout=120
            )

            data = response.json()

            return {
                "content": data["response"],
                "model": data["model"],
                "done": data["done"],
                "total_duration": data.get("total_duration"),
                "eval_count": data.get("eval_count")
            }

        except Exception as e:
            self.logger.error(f"Ollama error: {e}")
            raise

    def pull_model(self, model: str) -> bool:
        """Pull a model from Ollama library."""
        response = requests.post(
            f"{self.config.base_url}/api/pull",
            json={"name": model},
            stream=True
        )

        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                self.logger.info(f"Pulling {model}: {data.get('status')}")
                if data.get("status") == "success":
                    return True

        return False
```

### GPU Configuration

```bash
# Check GPU usage
nvidia-smi

# Ollama automatically uses GPU if available
# For multi-GPU:
CUDA_VISIBLE_DEVICES=0,1 ollama serve

# Limit VRAM usage (in Modelfile)
# PARAMETER num_gpu 1

# Force CPU only
OLLAMA_NO_GPU=1 ollama serve
```

### Docker Deployment

```yaml
# docker-compose.yml
version: '3.8'
services:
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]

volumes:
  ollama_data:
```

```bash
# Run with Docker
docker run -d --gpus all -v ollama:/root/.ollama -p 11434:11434 ollama/ollama

# Pull model in container
docker exec -it <container_id> ollama pull llama3.1:8b
```

## Best Practices

1. **Model Selection**
   - Match model size to available RAM/VRAM
   - Use quantized versions (Q4, Q5) for memory savings
   - Test multiple models for your use case

2. **Performance Optimization**
   - Keep models loaded in memory between requests
   - Use appropriate context window size
   - Consider model quantization trade-offs

3. **Resource Management**
   - Monitor GPU/CPU usage
   - Set appropriate timeouts
   - Implement request queuing for high load

4. **Deployment**
   - Use Docker for reproducible deployments
   - Set up health checks
   - Configure automatic restarts

5. **Development Workflow**
   - Test with local models before cloud APIs
   - Create custom Modelfiles for specific tasks
   - Version control your Modelfiles

## Common Pitfalls

1. **Insufficient RAM** - Model won't load or runs extremely slow
2. **Wrong Context Size** - Truncated outputs or OOM errors
3. **No GPU Detection** - Falling back to slow CPU inference
4. **Server Not Running** - Forgetting to start `ollama serve`
5. **Model Not Pulled** - Trying to use unpulled models
6. **Timeout Too Short** - Large models need more time

## References

- [Ollama Official Site](https://ollama.com/)
- [Ollama GitHub](https://github.com/ollama/ollama)
- [Ollama Model Library](https://ollama.com/library)
- [Ollama Python Library](https://github.com/ollama/ollama-python)
