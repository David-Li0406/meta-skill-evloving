# Models Reference

## Choosing a Model

For most use cases, start with **Claude Sonnet 4.5**. It offers the best balance of intelligence, speed, and cost, with exceptional performance in coding and agentic tasks.

All current Claude models support text and image input, text output, multilingual capabilities, and vision.

---

## Latest Models

### Claude Sonnet 4.5

Smart model for complex agents and coding.

| Property | Value |
|----------|-------|
| **API ID** | `claude-sonnet-4-5-20250929` |
| **API Alias** | `claude-sonnet-4-5` |
| **AWS Bedrock** | `anthropic.claude-sonnet-4-5-20250929-v1:0` |
| **GCP Vertex AI** | `claude-sonnet-4-5@20250929` |
| **Pricing** | $3/MTok input, $15/MTok output |
| **Context Window** | 200K tokens (1M beta) |
| **Max Output** | 64K tokens |
| **Latency** | Fast |
| **Extended Thinking** | Yes |
| **Knowledge Cutoff** | Jan 2025 (reliable), Jul 2025 (training) |

### Claude Haiku 4.5

Fastest model with near-frontier intelligence.

| Property | Value |
|----------|-------|
| **API ID** | `claude-haiku-4-5-20251001` |
| **API Alias** | `claude-haiku-4-5` |
| **AWS Bedrock** | `anthropic.claude-haiku-4-5-20251001-v1:0` |
| **GCP Vertex AI** | `claude-haiku-4-5@20251001` |
| **Pricing** | $1/MTok input, $5/MTok output |
| **Context Window** | 200K tokens |
| **Max Output** | 64K tokens |
| **Latency** | Fastest |
| **Extended Thinking** | Yes |
| **Knowledge Cutoff** | Feb 2025 (reliable), Jul 2025 (training) |

### Claude Opus 4.5

Premium model combining maximum intelligence with practical performance.

| Property | Value |
|----------|-------|
| **API ID** | `claude-opus-4-5-20251101` |
| **API Alias** | `claude-opus-4-5` |
| **AWS Bedrock** | `anthropic.claude-opus-4-5-20251101-v1:0` |
| **GCP Vertex AI** | `claude-opus-4-5@20251101` |
| **Pricing** | $5/MTok input, $25/MTok output |
| **Context Window** | 200K tokens |
| **Max Output** | 64K tokens |
| **Latency** | Moderate |
| **Extended Thinking** | Yes |
| **Knowledge Cutoff** | May 2025 (reliable), Aug 2025 (training) |

---

## Legacy Models

These models are still available but we recommend migrating to current models.

### Claude Opus 4.1

| Property | Value |
|----------|-------|
| **API ID** | `claude-opus-4-1-20250805` |
| **API Alias** | `claude-opus-4-1` |
| **AWS Bedrock** | `anthropic.claude-opus-4-1-20250805-v1:0` |
| **GCP Vertex AI** | `claude-opus-4-1@20250805` |
| **Pricing** | $15/MTok input, $75/MTok output |
| **Context Window** | 200K tokens |
| **Max Output** | 32K tokens |
| **Extended Thinking** | Yes |

### Claude Sonnet 4

| Property | Value |
|----------|-------|
| **API ID** | `claude-sonnet-4-20250514` |
| **API Alias** | `claude-sonnet-4-0` |
| **AWS Bedrock** | `anthropic.claude-sonnet-4-20250514-v1:0` |
| **GCP Vertex AI** | `claude-sonnet-4@20250514` |
| **Pricing** | $3/MTok input, $15/MTok output |
| **Context Window** | 200K tokens (1M beta) |
| **Max Output** | 64K tokens |
| **Extended Thinking** | Yes |

### Claude Sonnet 3.7

| Property | Value |
|----------|-------|
| **API ID** | `claude-3-7-sonnet-20250219` |
| **API Alias** | `claude-3-7-sonnet-latest` |
| **AWS Bedrock** | `anthropic.claude-3-7-sonnet-20250219-v1:0` |
| **GCP Vertex AI** | `claude-3-7-sonnet@20250219` |
| **Pricing** | $3/MTok input, $15/MTok output |
| **Context Window** | 200K tokens |
| **Max Output** | 64K tokens (128K beta) |
| **Extended Thinking** | Yes |

### Claude Opus 4

| Property | Value |
|----------|-------|
| **API ID** | `claude-opus-4-20250514` |
| **API Alias** | `claude-opus-4-0` |
| **AWS Bedrock** | `anthropic.claude-opus-4-20250514-v1:0` |
| **GCP Vertex AI** | `claude-opus-4@20250514` |
| **Pricing** | $15/MTok input, $75/MTok output |
| **Context Window** | 200K tokens |
| **Max Output** | 32K tokens |
| **Extended Thinking** | Yes |

### Claude Haiku 3

| Property | Value |
|----------|-------|
| **API ID** | `claude-3-haiku-20240307` |
| **AWS Bedrock** | `anthropic.claude-3-haiku-20240307-v1:0` |
| **GCP Vertex AI** | `claude-3-haiku@20240307` |
| **Pricing** | $0.25/MTok input, $1.25/MTok output |
| **Context Window** | 200K tokens |
| **Max Output** | 4K tokens |
| **Extended Thinking** | No |

---

## Model Selection Guide

| Use Case | Recommended Model |
|----------|-------------------|
| Complex agents and coding | Claude Sonnet 4.5 |
| Fast, lightweight tasks | Claude Haiku 4.5 |
| Maximum intelligence | Claude Opus 4.5 |
| Cost-sensitive applications | Claude Haiku 4.5 |
| Long context (up to 1M tokens) | Claude Sonnet 4.5 (with beta header) |

---

## API Aliases

Aliases automatically point to the most recent model snapshot. When new snapshots are released, aliases migrate within a week.

**For production**: Use specific model versions (e.g., `claude-sonnet-4-5-20250929`) to ensure consistent behavior.

**For experimentation**: Aliases (e.g., `claude-sonnet-4-5`) are convenient for testing.

---

## Platform Availability

All models are available via:
- **Anthropic API** - Direct access
- **AWS Bedrock** - Global and regional endpoints
- **Google Vertex AI** - Global and regional endpoints

Starting with Claude 4.5, AWS Bedrock and Google Vertex AI offer:
- **Global endpoints**: Dynamic routing for maximum availability
- **Regional endpoints**: Guaranteed data routing through specific geographic regions

---

## 1M Token Context (Beta)

Claude Sonnet 4.5 and Claude Sonnet 4 support 1M token context with the beta header:

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    extra_headers={"anthropic-beta": "context-1m-2025-08-07"},
    messages=[{"role": "user", "content": very_long_content}]
)
```

Long context pricing applies to requests exceeding 200K tokens.

---

## 128K Output (Beta)

Claude Sonnet 3.7 supports 128K output tokens with the beta header:

```python
message = client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=128000,
    extra_headers={"anthropic-beta": "output-128k-2025-02-19"},
    messages=[{"role": "user", "content": "..."}]
)
```

Use streaming to avoid timeouts when generating longer outputs.
