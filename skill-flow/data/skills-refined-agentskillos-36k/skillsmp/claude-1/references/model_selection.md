# Model Selection Guide

## Available Models

### Claude 3.5 Haiku (`claude-3-5-haiku-20241022`)

**Best for:** High-volume, low-latency tasks that don't require deep reasoning.

**Strengths:**
- Fastest response times
- Lowest cost per token
- Good for simple, well-defined tasks

**Ideal use cases:**
- Data extraction and parsing
- Simple classification
- Formatting and transformation
- High-throughput processing pipelines
- Quick Q&A with clear answers
- Text summarization (straightforward documents)

**When to avoid:**
- Complex multi-step reasoning
- Nuanced analysis requiring judgment
- Creative writing with specific style requirements
- Tasks where quality is critical

---

### Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`)

**Best for:** General-purpose tasks requiring good balance of speed, cost, and quality.

**Strengths:**
- Excellent code generation and analysis
- Strong reasoning capabilities
- Good balance of speed and quality
- Handles most professional tasks well

**Ideal use cases:**
- Code generation and debugging
- Document analysis and summarization
- Multi-step reasoning tasks
- Technical writing and documentation
- Complex data extraction
- Most business automation tasks

**When to avoid:**
- Simple extraction where Haiku suffices
- Maximum quality creative writing
- Extremely complex analysis (use Opus)

---

### Claude Opus 4.5 (`claude-opus-4-5-20251101`)

**Best for:** Maximum quality output where cost and latency are secondary concerns.

**Strengths:**
- Highest intelligence and reasoning capability
- Best creative writing quality
- Most nuanced understanding
- Excellent at complex, ambiguous tasks

**Ideal use cases:**
- Complex strategic analysis
- High-stakes content creation
- Nuanced decision-making
- Research and synthesis
- Creative writing with specific voice/style
- Tasks requiring exceptional judgment
- Multi-faceted problems with trade-offs

**When to avoid:**
- High-volume processing (cost prohibitive)
- Simple, well-defined tasks
- Latency-sensitive applications

---

## Decision Matrix

| Task Complexity | Volume | Latency Requirement | Recommended Model |
|-----------------|--------|---------------------|-------------------|
| Simple | High | Low | Haiku |
| Simple | Low | Any | Haiku |
| Medium | Any | Medium | Sonnet |
| Complex | Low | Any | Sonnet or Opus |
| Complex | Low | Not critical | Opus |
| Very Complex | Any | Not critical | Opus |

## Cost Considerations

Models are priced per million tokens:
- **Haiku**: Lowest cost (~$0.25/M input, ~$1.25/M output)
- **Sonnet**: Medium cost (~$3/M input, ~$15/M output)
- **Opus**: Highest cost (~$15/M input, ~$75/M output)

**Cost optimization strategies:**
1. Use Haiku for preprocessing and validation
2. Use Sonnet for main processing
3. Reserve Opus for final quality checks or complex decisions
4. Batch similar requests to maximize context reuse

## Extended Thinking

For tasks requiring deep reasoning, enable extended thinking on Sonnet or Opus:

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000
    },
    messages=[...]
)
```

**When to use extended thinking:**
- Mathematical or logical problems
- Complex code architecture decisions
- Multi-step analysis
- Problems requiring exploration of alternatives

**Budget guidelines:**
- Start with 4000-8000 tokens for most tasks
- Increase to 10000-16000 for complex problems
- Use 32000+ for extremely difficult reasoning (batch processing recommended)

## Model Selection by Use Case

### Natural Language Processing
| Use Case | Model | Notes |
|----------|-------|-------|
| Simple text classification | Haiku | Fast, cheap |
| Sentiment analysis | Haiku/Sonnet | Haiku for basic, Sonnet for nuanced |
| Named entity extraction | Haiku | Well-defined task |
| Summarization | Sonnet | Better quality |
| Translation | Sonnet | Handles nuance well |

### Data Extraction
| Use Case | Model | Notes |
|----------|-------|-------|
| Structured form data | Haiku | Simple extraction |
| Semi-structured documents | Sonnet | Handles variation |
| Complex unstructured text | Sonnet/Opus | Depends on complexity |
| Legal/medical documents | Opus | Accuracy critical |

### Content Generation
| Use Case | Model | Notes |
|----------|-------|-------|
| Templates/boilerplate | Haiku | Simple generation |
| Documentation | Sonnet | Good quality/cost balance |
| Marketing copy | Sonnet | Professional quality |
| Creative writing | Opus | Best voice/style |
| Technical articles | Sonnet | Strong technical capability |

### Code & Technical
| Use Case | Model | Notes |
|----------|-------|-------|
| Code formatting | Haiku | Mechanical task |
| Bug fixes | Sonnet | Strong reasoning |
| New feature implementation | Sonnet | Good balance |
| Architecture design | Opus + thinking | Complex decisions |
| Code review | Sonnet | Catches most issues |

### Image Analysis
| Use Case | Model | Notes |
|----------|-------|-------|
| Simple description | Haiku | Basic analysis |
| OCR/text extraction | Sonnet | Better accuracy |
| Chart/graph analysis | Sonnet | Understands context |
| Complex scene analysis | Sonnet/Opus | Depends on detail needed |
| Document image processing | Sonnet | Good balance |
