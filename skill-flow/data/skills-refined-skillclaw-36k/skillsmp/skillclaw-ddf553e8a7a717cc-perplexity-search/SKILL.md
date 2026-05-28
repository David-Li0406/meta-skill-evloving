---
name: perplexity-search
description: Use this skill when you need to perform AI-powered web searches for current information, recent scientific literature, or grounded answers with source citations beyond the model's knowledge cutoff.
---

# Perplexity Search

## Overview

Perform AI-powered web searches using Perplexity models through LiteLLM and OpenRouter. This skill provides real-time, web-grounded answers with source citations, making it ideal for finding current information, recent scientific literature, and facts beyond the model's training data cutoff. Access all Perplexity models through OpenRouter with a single API key (no separate Perplexity account needed).

## When to Use This Skill

Use this skill when:
- Searching for current information or recent developments (2024 and beyond)
- Finding the latest scientific publications and research
- Getting real-time answers grounded in web sources
- Verifying facts with source citations
- Conducting literature searches across multiple domains
- Accessing information beyond the model's knowledge cutoff
- Performing domain-specific research (biomedical, technical, clinical)
- Comparing current approaches or technologies

**Do not use** for:
- Simple calculations or logic problems (use directly)
- Tasks requiring code execution (use standard tools)
- Questions well within the model's training data (unless verification needed)

## Quick Start

### Setup (One-time)

1. **Get OpenRouter API key**:
   - Visit https://openrouter.ai/keys
   - Create an account and generate an API key
   - Add credits to your account (minimum $5 recommended)

2. **Configure environment**:
   ```bash
   # Set API key
   export OPENROUTER_API_KEY='sk-or-v1-your-key-here'

   # Or use setup script
   python scripts/setup_env.py --api-key sk-or-v1-your-key-here
   ```

3. **Install dependencies**:
   ```bash
   pip install litellm
   ```

4. **Verify setup**:
   ```bash
   python scripts/perplexity_search.py --check-setup
   ```

### Basic Usage

**Simple search:**
```bash
python scripts/perplexity_search.py --query "latest research on AI"
```