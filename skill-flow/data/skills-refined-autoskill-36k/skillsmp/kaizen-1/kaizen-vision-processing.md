# Vision Processing

VisionAgent, OllamaVisionProvider, image analysis with Ollama/OpenAI.

## Basic Vision Agent

```python
from kaizen.agents import VisionAgent, VisionAgentConfig

config = VisionAgentConfig(llm_provider="ollama", model="bakllava")
agent = VisionAgent(config=config)

result = agent.analyze(
    image="/path/to/image.png",  # File path, NOT base64
    question="What is the total amount?"  # 'question', NOT 'prompt'
)
print(result['answer'])  # Key is 'answer', NOT 'response'
```

## OllamaVisionProvider

```python
from kaizen.providers.ollama_vision_provider import OllamaVisionProvider, OllamaVisionConfig

config = OllamaVisionConfig(model="bakllava")
provider = OllamaVisionProvider(config=config)

result = provider.analyze_image(
    image="/path/to/image.png",
    prompt="Extract invoice number"
)
print(result['response'])  # Key is 'response', NOT 'answer'
```

## Model Selection
- **bakllava**: 4.7GB, 2-4s, 40-60% accuracy, free
- **llava:13b**: 7GB, 4-8s, 80-90% accuracy, free
- **GPT-4V**: API, 1-2s, 95%+ accuracy, ~$0.01/img

## References
- **Specialist**: `.claude/agents/frameworks/kaizen-specialist.md` lines 167-214
- **API Reference**: `sdk-users/apps/kaizen/docs/reference/multi-modal-api-reference.md`
