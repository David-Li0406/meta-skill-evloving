# Multi-Modal Common Pitfalls

Common mistakes from kaizen-specialist lines 301-373.

## Pitfall 1: OllamaVisionProvider Initialization

```python
# ❌ WRONG - TypeError
provider = OllamaVisionProvider(model="bakllava")

# ✅ CORRECT
config = OllamaVisionConfig(model="bakllava")
provider = OllamaVisionProvider(config=config)
```

## Pitfall 2: VisionAgent Parameter Names

```python
# ❌ WRONG - TypeError
result = agent.analyze(image="...", prompt="What do you see?")

# ✅ CORRECT
result = agent.analyze(image="...", question="What do you see?")
```

## Pitfall 3: Image Path Handling

```python
# ❌ WRONG - Ollama doesn't accept data URLs
img = ImageField()
img.load("/path/to/image.png")
provider.analyze_image(image=img.to_base64(), ...)

# ✅ CORRECT - Pass file path or ImageField
provider.analyze_image(image="/path/to/image.png", ...)
```

## Pitfall 4: Response Format Differences

```python
# OllamaVisionProvider → 'response' key
result = provider.analyze_image(...)
text = result['response']

# VisionAgent → 'answer' key
result = agent.analyze(...)
text = result['answer']
```

## Pitfall 5: Integration Testing

Always validate with real models, not just mocks.

## References
- **Specialist**: `.claude/agents/frameworks/kaizen-specialist.md` lines 300-373
