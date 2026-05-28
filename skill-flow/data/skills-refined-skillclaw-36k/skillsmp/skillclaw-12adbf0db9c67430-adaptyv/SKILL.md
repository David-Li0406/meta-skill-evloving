---
name: adaptyv
description: Use this skill when designing proteins and needing experimental validation, including binding assays, expression testing, thermostability measurements, enzyme activity assays, or protein sequence optimization.
---

# Adaptyv

Adaptyv is a cloud laboratory platform that provides automated protein testing and validation services. Submit protein sequences via API or web interface and receive experimental results in approximately 21 days.

## Quick Start

### Authentication Setup

Adaptyv requires API authentication. Set up your credentials:

1. Contact support@adaptyvbio.com to request API access (platform is in alpha/beta).
2. Receive your API access token.
3. Set environment variable:

```bash
export ADAPTYV_API_KEY="your_api_key_here"
```

Or create a `.env` file:

```
ADAPTYV_API_KEY=your_api_key_here
```

### Installation

Install the required package using uv:

```bash
uv pip install requests python-dotenv
```

### Basic Usage

Submit protein sequences for testing:

```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ADAPTYV_API_KEY")
base_url = "https://kq5jp7qj7wdqklhsxmovkzn4l40obksv.lambda-url.eu-central-1.on.aws"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Submit experiment
response = requests.post(
    f"{base_url}/experiments",
    headers=headers,
    json={
        "sequences": ">protein1\nMKVLWALLGLLGAA...",
        "experiment_type": "binding",
        "webhook_url": "https://your-webhook.com/callback"
    }
)

experiment_id = response.json()["experiment_id"]
```

## Available Experiment Types

Adaptyv supports multiple assay types:

- **Binding assays** - Test protein-target interactions using biolayer interferometry.
- **Expression testing** - Measure protein expression levels.
- **Thermostability** - Characterize protein thermal stability.
- **Enzyme activity** - Assess enzymatic function.

## Protein Sequence Optimization

Before submitting sequences, optimize them for better expression using computational tools (NetSolP, SoluProt, SolubleMPNN, ESM).