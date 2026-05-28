# AMUM Alignment Workflow

## Overview

AMUM implements a progressive 3→6→9 human-AI alignment workflow.

## Phases

1. **Divergent (3)**: Generate 3 initial options
2. **Expand (6)**: Expand selected option to 6 variations
3. **Converge (9)**: Converge to 9 final options, select best

## Usage

### Quick Alignment

```python
from mcp_b import quick_alignment

result = quick_alignment(
    intent="Create AI agent",
    divergent_3=["Minimal", "Balanced", "Full"],
    select_1=1,
    expand_6=["Text", "Image", "Voice", "Multi", "Pro", "Suite"],
    select_2=4,
    converge_9=["GPT-4", "Claude", "Gemini", "Ollama", "Hybrid",
                "Edge", "ElevenLabs", "OpenAI", "Local"],
    select_3=6
)
print(result["final_intent"])  # "ElevenLabs"
```

### Session-Based

```python
from mcp_b import AMUM, AMUMSession

amum = AMUM()
session = amum.start("Build an API")

# Phase 1: Divergent
session.set_options(["REST", "GraphQL", "gRPC"])
session.select(1)  # Select REST

# Phase 2: Expand
session.set_options(["FastAPI", "Flask", "Django", "Starlette", "Falcon", "aiohttp"])
session.select(1)  # Select FastAPI

# Phase 3: Converge
session.set_options([
    "Basic CRUD", "Auth", "Pagination", "Rate Limit",
    "Caching", "Docs", "Tests", "Deploy", "Monitor"
])
session.select(6)  # Select Docs
```
