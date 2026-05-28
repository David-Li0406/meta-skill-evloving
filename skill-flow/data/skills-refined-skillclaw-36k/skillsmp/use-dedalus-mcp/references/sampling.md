# Sampling Reference

Make nested LLM calls from within MCP tools.

## Basic Sampling

Use `ctx.sample()` to call an LLM from within a tool:

```python
from dedalus_mcp import tool, get_context

@tool(description="Review code for issues")
async def review_code(code: str, language: str) -> str:
    ctx = get_context()
    
    response = await ctx.sample(
        f"Review this {language} code for bugs and improvements:\n\n```{language}\n{code}\n```",
        system_prompt="You are an expert code reviewer. Be concise and actionable.",
        temperature=0.2,
    )
    
    return response.text
```

## Sample Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt` | `str` | User message to send |
| `system_prompt` | `str` | System instructions |
| `temperature` | `float` | Sampling temperature (0-1) |
| `max_tokens` | `int` | Maximum response tokens |

## Using Types

For structured sampling with MCP types:

```python
from dedalus_mcp import get_context, tool, types

@tool(description="Review code in the repo")
async def review_code(code: str, language: str) -> str:
    ctx = get_context()
    
    params = types.CreateMessageRequestParams(
        messages=[
            types.SamplingMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=f"Review this {language} code:\n\n```{language}\n{code}\n```",
                ),
            )
        ],
        systemPrompt="You are an expert code reviewer. Be concise and actionable.",
        temperature=0.2,
        maxTokens=500,
    )
    
    result = await ctx.server.request_sampling(params)
    return result.content.text
```

## Use Cases

### Content Generation

```python
@tool(description="Generate blog post outline")
async def generate_outline(topic: str) -> str:
    ctx = get_context()
    
    response = await ctx.sample(
        f"Create a detailed outline for a blog post about: {topic}",
        system_prompt="You are a content strategist. Create clear, engaging outlines.",
        temperature=0.7,
    )
    
    return response.text
```

### Analysis

```python
@tool(description="Analyze sentiment")
async def analyze_sentiment(text: str) -> dict:
    ctx = get_context()
    
    response = await ctx.sample(
        f"Analyze the sentiment of this text and respond with JSON:\n\n{text}",
        system_prompt="Respond only with JSON: {\"sentiment\": \"positive|negative|neutral\", \"confidence\": 0.0-1.0}",
        temperature=0.0,
    )
    
    return json.loads(response.text)
```

### Translation

```python
@tool(description="Translate text")
async def translate(text: str, target_language: str) -> str:
    ctx = get_context()
    
    response = await ctx.sample(
        f"Translate to {target_language}:\n\n{text}",
        system_prompt="You are a professional translator. Preserve meaning and tone.",
        temperature=0.3,
    )
    
    return response.text
```

## Chaining Samples

```python
@tool(description="Research and summarize topic")
async def research_and_summarize(topic: str) -> str:
    ctx = get_context()
    
    # Step 1: Research
    research = await ctx.sample(
        f"List 5 key facts about: {topic}",
        temperature=0.5,
    )
    
    # Step 2: Summarize
    summary = await ctx.sample(
        f"Summarize these facts into a single paragraph:\n\n{research.text}",
        temperature=0.3,
    )
    
    return summary.text
```

## Best Practices

1. **Set appropriate temperature** - Lower for factual, higher for creative
2. **Use system prompts** - Guide the model's behavior
3. **Limit max_tokens** - Prevent runaway responses
4. **Handle errors** - Sampling can fail; wrap in try/except
5. **Chain thoughtfully** - Each sample adds latency
