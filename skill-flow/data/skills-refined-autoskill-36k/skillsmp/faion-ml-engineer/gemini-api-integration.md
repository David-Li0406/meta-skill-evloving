---
id: gemini-api-integration
name: "Gemini API Integration"
domain: ML
skill: faion-ml-engineer
category: "ml-engineering"
---

# Gemini API Integration

## Overview

Google's Gemini API provides access to multimodal AI models capable of understanding text, images, audio, and video. Gemini 1.5 Pro offers a 1M token context window, making it ideal for processing entire codebases, long documents, or video content.

## When to Use

- Processing very long documents (1M token context)
- Multimodal tasks (text + images + audio + video)
- Applications requiring Google Cloud integration
- When cost-effectiveness at scale matters
- YouTube video analysis
- Code understanding across large repositories

## Key Concepts

### Model Hierarchy

| Model | Context | Best For | Cost |
|-------|---------|----------|------|
| gemini-1.5-pro | 1M | Complex multimodal, long context | Medium |
| gemini-1.5-flash | 1M | Fast, cost-effective | Low |
| gemini-1.0-pro | 32K | Text-only, legacy | Low |
| gemini-1.0-pro-vision | 16K | Vision, legacy | Medium |

### Unique Features

- **1M Token Context**: Process entire books, codebases, or video
- **Native Multimodal**: Single model handles text, image, audio, video
- **Grounding**: Connect to Google Search for real-time information
- **Code Execution**: Run Python code within the model

## Implementation

### Basic Setup

```python
import google.generativeai as genai
import os

# Configure API key
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# Initialize model
model = genai.GenerativeModel("gemini-1.5-pro")

# Simple completion
response = model.generate_content("Explain quantum entanglement simply.")
print(response.text)
```

### Chat Conversations

```python
def create_chat():
    """Multi-turn chat conversation."""
    model = genai.GenerativeModel("gemini-1.5-pro")
    chat = model.start_chat(history=[])

    # First message
    response = chat.send_message("What is machine learning?")
    print(f"Gemini: {response.text}")

    # Follow-up (maintains context)
    response = chat.send_message("How does it differ from deep learning?")
    print(f"Gemini: {response.text}")

    # Access conversation history
    for message in chat.history:
        print(f"{message.role}: {message.parts[0].text[:100]}...")

    return chat
```

### Streaming Responses

```python
def stream_response(prompt: str) -> str:
    """Stream response for real-time output."""
    model = genai.GenerativeModel("gemini-1.5-pro")

    response = model.generate_content(prompt, stream=True)

    full_text = ""
    for chunk in response:
        if chunk.text:
            print(chunk.text, end="", flush=True)
            full_text += chunk.text

    return full_text
```

### Image Analysis

```python
import PIL.Image

def analyze_image(image_path: str, question: str) -> str:
    """Analyze image with Gemini Vision."""
    model = genai.GenerativeModel("gemini-1.5-pro")

    # Load image
    image = PIL.Image.open(image_path)

    # Send image with text prompt
    response = model.generate_content([question, image])

    return response.text

def analyze_image_url(image_url: str, question: str) -> str:
    """Analyze image from URL."""
    import httpx

    model = genai.GenerativeModel("gemini-1.5-pro")

    # Download image
    image_data = httpx.get(image_url).content

    response = model.generate_content([
        question,
        {"mime_type": "image/jpeg", "data": image_data}
    ])

    return response.text
```

### Video Analysis

```python
def analyze_video(video_path: str, question: str) -> str:
    """Analyze video content with Gemini."""
    model = genai.GenerativeModel("gemini-1.5-pro")

    # Upload video file
    video_file = genai.upload_file(video_path)

    # Wait for processing
    import time
    while video_file.state.name == "PROCESSING":
        time.sleep(5)
        video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        raise ValueError("Video processing failed")

    # Analyze
    response = model.generate_content([video_file, question])

    return response.text

def analyze_youtube(youtube_url: str, question: str) -> str:
    """Analyze YouTube video (requires video download first)."""
    # Note: Gemini doesn't directly accept YouTube URLs
    # You need to download the video first using yt-dlp or similar
    pass
```

### Audio Analysis

```python
def transcribe_audio(audio_path: str) -> str:
    """Transcribe and analyze audio."""
    model = genai.GenerativeModel("gemini-1.5-pro")

    # Upload audio file
    audio_file = genai.upload_file(audio_path)

    response = model.generate_content([
        audio_file,
        "Transcribe this audio and summarize the key points."
    ])

    return response.text
```

### Function Calling

```python
def get_weather(location: str, unit: str = "celsius") -> dict:
    """Mock weather function."""
    return {"location": location, "temperature": 22, "unit": unit}

# Define function for Gemini
weather_tool = genai.protos.Tool(
    function_declarations=[
        genai.protos.FunctionDeclaration(
            name="get_weather",
            description="Get current weather for a location",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "location": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        description="City name"
                    ),
                    "unit": genai.protos.Schema(
                        type=genai.protos.Type.STRING,
                        enum=["celsius", "fahrenheit"]
                    )
                },
                required=["location"]
            )
        )
    ]
)

def chat_with_functions(user_message: str):
    """Gemini with function calling."""
    model = genai.GenerativeModel(
        "gemini-1.5-pro",
        tools=[weather_tool]
    )

    chat = model.start_chat()
    response = chat.send_message(user_message)

    # Check for function calls
    for part in response.parts:
        if hasattr(part, "function_call"):
            fn = part.function_call

            # Execute function
            if fn.name == "get_weather":
                result = get_weather(**dict(fn.args))

                # Send result back
                response = chat.send_message(
                    genai.protos.Content(
                        parts=[genai.protos.Part(
                            function_response=genai.protos.FunctionResponse(
                                name=fn.name,
                                response={"result": result}
                            )
                        )]
                    )
                )

    return response.text
```

### System Instructions

```python
def create_specialized_model():
    """Create model with system instructions."""
    model = genai.GenerativeModel(
        "gemini-1.5-pro",
        system_instruction="""You are a senior Python developer.
        - Always provide code examples
        - Explain trade-offs
        - Follow PEP 8 style
        - Include error handling
        """
    )

    return model
```

### Safety Settings

```python
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def create_safe_model():
    """Model with custom safety settings."""
    model = genai.GenerativeModel(
        "gemini-1.5-pro",
        safety_settings={
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }
    )
    return model
```

### Long Context Processing

```python
def process_large_document(file_path: str, question: str) -> str:
    """Process documents using Gemini's 1M context."""
    model = genai.GenerativeModel("gemini-1.5-pro")

    # Read entire file
    with open(file_path, "r") as f:
        content = f.read()

    # Gemini can handle very long documents
    response = model.generate_content([
        f"Document:\n{content}\n\nQuestion: {question}"
    ])

    return response.text

def analyze_codebase(directory: str, question: str) -> str:
    """Analyze entire codebase."""
    import glob

    model = genai.GenerativeModel("gemini-1.5-pro")

    # Collect all Python files
    code_content = []
    for filepath in glob.glob(f"{directory}/**/*.py", recursive=True):
        with open(filepath, "r") as f:
            code_content.append(f"# File: {filepath}\n{f.read()}")

    full_code = "\n\n".join(code_content)

    response = model.generate_content([
        f"Codebase:\n{full_code}\n\nQuestion: {question}"
    ])

    return response.text
```

### Production Service Class

```python
from dataclasses import dataclass
from typing import Optional, List, Any
import logging

@dataclass
class GeminiConfig:
    model: str = "gemini-1.5-pro"
    temperature: float = 0.7
    top_p: float = 0.95
    top_k: int = 40
    max_output_tokens: int = 8192

class GeminiService:
    """Production-ready Gemini service."""

    def __init__(self, api_key: Optional[str] = None):
        genai.configure(api_key=api_key or os.environ.get("GOOGLE_API_KEY"))
        self.logger = logging.getLogger(__name__)

    def complete(
        self,
        prompt: str,
        config: Optional[GeminiConfig] = None
    ) -> dict:
        """Execute completion."""
        config = config or GeminiConfig()

        model = genai.GenerativeModel(config.model)

        generation_config = genai.GenerationConfig(
            temperature=config.temperature,
            top_p=config.top_p,
            top_k=config.top_k,
            max_output_tokens=config.max_output_tokens
        )

        try:
            response = model.generate_content(
                prompt,
                generation_config=generation_config
            )

            return {
                "content": response.text,
                "usage": {
                    "prompt_tokens": response.usage_metadata.prompt_token_count,
                    "output_tokens": response.usage_metadata.candidates_token_count
                },
                "finish_reason": response.candidates[0].finish_reason.name
            }
        except Exception as e:
            self.logger.error(f"Gemini API error: {e}")
            raise
```

## Best Practices

1. **Leverage Long Context**
   - Use 1M context for entire documents/codebases
   - Chunk strategically if content exceeds limit
   - Consider cost vs. summarization approaches

2. **Multimodal Integration**
   - Combine text, images, audio in single request
   - Upload large files before referencing
   - Monitor file processing status

3. **Safety Configuration**
   - Adjust safety settings for your use case
   - Handle blocked responses gracefully
   - Log and review blocked content patterns

4. **Cost Optimization**
   - Use gemini-1.5-flash for simple tasks
   - Cache responses when appropriate
   - Batch similar requests

5. **Error Handling**
   - Handle quota limits with backoff
   - Check for blocked content
   - Verify file upload completion

## Common Pitfalls

1. **File Processing Time** - Not waiting for video/audio upload completion
2. **Safety Blocks** - Response blocked without error handling
3. **Token Limits** - Even 1M has limits with rich media
4. **Rate Limits** - Different limits for different operations
5. **Missing Regions** - Some features region-restricted
6. **Grounding Costs** - Google Search grounding adds significant cost

## References

- [Google AI Studio](https://makersuite.google.com/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Google AI Python SDK](https://github.com/google/generative-ai-python)
- [Gemini Cookbook](https://github.com/google-gemini/cookbook)
