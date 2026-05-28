---
name: benchling-integration
description: Use this skill when you need to integrate with the Benchling R&D platform to manage biological data, automate lab workflows, and access various registry entities via API.
---

# Benchling Integration

## Overview

Benchling is a cloud platform for life sciences R&D. This skill allows you to access registry entities (DNA, proteins), manage inventory, create electronic lab notebook entries, and automate workflows programmatically via the Python SDK and REST API.

## When to Use This Skill

This skill should be used when:
- Working with Benchling's Python SDK or REST API
- Managing biological sequences (DNA, RNA, proteins) and registry entities
- Automating inventory operations (samples, containers, locations, transfers)
- Creating or querying electronic lab notebook entries
- Building workflow automations or Benchling Apps
- Syncing data between Benchling and external systems
- Querying the Benchling Data Warehouse for analytics
- Setting up event-driven integrations with AWS EventBridge

## Core Capabilities

### 1. Authentication & Setup

**Python SDK Installation:**
```bash
# Stable release
pip install benchling-sdk
# or with Poetry
poetry add benchling-sdk
```

**Authentication Methods:**

**API Key Authentication (recommended for scripts):**
```python
from benchling_sdk.benchling import Benchling
from benchling_sdk.auth.api_key_auth import ApiKeyAuth

benchling = Benchling(
    url="https://your-tenant.benchling.com",
    auth_method=ApiKeyAuth("your_api_key")
)
```

**OAuth Client Credentials (for apps):**
```python
from benchling_sdk.auth.client_credentials_oauth2 import ClientCredentialsOAuth2

auth_method = ClientCredentialsOAuth2(
    client_id="your_client_id",
    client_secret="your_client_secret"
)
benchling = Benchling(
    url="https://your-tenant.benchling.com",
    auth_method=auth_method
)
```

**Key Points:**
- API keys are obtained from Profile Settings in Benchling.
- Store credentials securely (use environment variables or password managers).
- All API requests require HTTPS.
- Authentication permissions mirror user permissions in the UI.

### 2. Registry & Entity Management

Registry entities include DNA sequences, RNA sequences, AA sequences, custom entities, and mixtures. The SDK provides typed classes for creating and managing these entities.

**Creating DNA Sequences:**
```python
from benchling_sdk.models import DnaSequence

dna_sequence = DnaSequence(
    name="Example DNA",
    sequence="ATCGATCGATCG"
)
```

### 3. Inventory Management

Automate inventory operations such as adding, updating, and querying samples and containers.

### 4. Electronic Lab Notebook (ELN)

Create and manage entries in the electronic lab notebook programmatically.

### 5. Workflow Automation

Build and manage workflows to automate lab processes and integrate with other systems.

### 6. Data Warehouse Queries

Query the Benchling Data Warehouse for analytics and reporting purposes.

### 7. Event-Driven Integrations

Set up integrations with AWS EventBridge for event-driven architecture.

For detailed information on each capability, refer to the Benchling API documentation.