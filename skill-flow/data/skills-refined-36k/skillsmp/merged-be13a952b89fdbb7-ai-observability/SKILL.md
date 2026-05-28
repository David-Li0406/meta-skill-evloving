---
name: ai-observability
description: Use this skill when debugging, evaluating, and monitoring LLM applications with detailed traces and systematic evaluations.
---

# AI Observability Platform

A comprehensive platform for tracing, evaluating, and monitoring language models and AI applications.

## When to use this skill

**Use this skill when:**
- Debugging LLM application issues with detailed traces
- Evaluating model outputs systematically against datasets
- Monitoring production LLM systems in real-time
- Building regression testing and experiment pipelines for AI features
- Analyzing latency, token usage, and costs

## Key features
- **Tracing**: Capture inputs, outputs, and latency for all LLM calls using OpenTelemetry-based trace collection.
- **Evaluation**: Systematic testing with built-in and custom evaluators for quality assessment.
- **Datasets**: Create and version test sets from production traces or manually for regression testing.
- **Monitoring**: Track metrics, errors, and costs in production with real-time insights.
- **Integrations**: Works with various frameworks including OpenAI, Anthropic, LangChain, and LlamaIndex.

## Quick start

### Installation

```bash
pip install langsmith arize-phoenix

# Set environment variables
export LANGSMITH_API_KEY="your-api-key"
export LANGSMITH_TRACING=true
export PHOENIX_SQL_DATABASE_URL="postgresql://user:pass@host/db"
```

### Basic tracing

```python
from langsmith import traceable
from openai import OpenAI

client = OpenAI()

@traceable
def generate_response(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Automatically traced to LangSmith
result = generate_response("What is machine learning?")
```

### OpenAI instrumentation

```python
from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor

# Configure OpenTelemetry with Phoenix
tracer_provider = register(
    project_name="my-llm-app",
    endpoint="http://localhost:6006/v1/traces"
)

# Instrument OpenAI SDK
OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)

# All OpenAI calls are now traced
client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Core concepts

### Runs and traces

A **run** is a single execution unit (LLM call, chain, tool). Runs form hierarchical **traces** showing the full execution flow.

### Projects

Projects organize related runs and traces. Set via environment or code:

```python
import os
os.environ["LANGSMITH_PROJECT"] = "my-project"
os.environ["PHOENIX_PROJECT_NAME"] = "production-chatbot"
```

## Evaluation framework

### Built-in evaluators

```python
from phoenix.evals import OpenAIModel, HallucinationEvaluator

# Setup model for evaluation
eval_model = OpenAIModel(model="gpt-4o")

# Evaluate hallucination
hallucination_eval = HallucinationEvaluator(eval_model)
results = hallucination_eval.evaluate(
    input="What is the capital of France?",
    output="The capital of France is Paris.",
    reference="Paris is the capital of France."
)
```

### Run evaluations on dataset

```python
from phoenix import Client
from phoenix.evals import run_evals

client = Client()

# Get spans to evaluate
spans_df = client.get_spans_dataframe(
    project_name="my-app",
    filter_condition="span_kind == 'LLM'"
)

# Run evaluations
eval_results = run_evals(
    dataframe=spans_df,
    evaluators=[HallucinationEvaluator(eval_model)],
    provide_explanation=True
)

# Log results back to Phoenix
client.log_evaluations(eval_results)
```

## Best practices

1. **Structured naming** - Use consistent project/run naming conventions.
2. **Add metadata** - Include version, environment, user info.
3. **Evaluate regularly** - Run automated evaluations in CI/CD pipelines.
4. **Monitor costs** - Track token usage and latency trends.

## Common issues

**Traces not appearing:**
```python
import os
# Ensure tracing is enabled
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "your-key"
```

**High latency from tracing:**
```python
# Enable background batching (default)
from langsmith import Client
client = Client(auto_batch_tracing=True)
```

## References

- **Documentation**: https://docs.smith.langchain.com
- **Repository**: https://github.com/langchain-ai/langsmith-sdk
- **Docker Hub**: https://hub.docker.com/r/arizephoenix/phoenix
- **Version**: 0.2.0+ for LangSmith, 12.0.0+ for Phoenix
- **License**: MIT for LangSmith, Apache 2.0 for Phoenix