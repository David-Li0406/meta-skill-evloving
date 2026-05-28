# Dify Plugin Manifest.yaml Complete Reference Guide

This document provides complete field rules, validation constraints, and examples for manifest.yaml to help developers correctly write plugin manifest files.

## Table of Contents

1. [Basic Structure](#1-basic-structure)
2. [Field Validation Rules](#2-field-validation-rules)
3. [Plugin Type Declarations](#3-plugin-type-declarations)
4. [Complete Examples](#4-complete-examples)
5. [Common Errors and Solutions](#5-common-errors-and-solutions)

---

## 1. Basic Structure

### 1.1 manifest.yaml Top-Level Structure

```yaml
# Basic Information (Required)
version: "0.0.1"              # Semantic version
type: plugin                   # Fixed value
author: your-name              # Author name
name: plugin-name              # Plugin name
label:                         # Multi-language labels
  en_US: "Plugin Name"
  zh_Hans: "插件名称"
description:                   # Multi-language descriptions
  en_US: "Plugin description"
  zh_Hans: "插件描述"
icon: icon.svg                 # Icon path
created_at: 2024-01-01T00:00:00Z  # Creation time

# Runtime Metadata (Required)
meta:
  version: "0.0.1"
  arch:
    - amd64
    - arm64
  runner:
    language: python
    version: "3.12"
    entrypoint: main

# Resource Requirements (Required)
resource:
  memory: 268435456            # Memory limit (bytes)
  permission:                  # Permission configuration (optional)
    tool:
      enabled: true
    model:
      enabled: true
    storage:
      enabled: true
      size: 1048576            # 1MB

# Plugin Component Declarations (Required, at least one)
plugins:
  tools:
    - provider/tools/my_tool.yaml
  models: []
  endpoints: []
  agent_strategies: []
  datasources: []
  triggers: []

# Optional Fields
icon_dark: icon_dark.svg       # Dark theme icon
tags:                          # Category tags
  - productivity
  - utilities
privacy: "https://example.com/privacy"   # Privacy policy URL
repo: "https://github.com/user/repo"     # Repository URL

# Provider Declarations (choose based on plugin type)
tool: ...                      # Tool plugin declaration
model: ...                     # Model plugin declaration
agent_strategy: ...            # Agent Strategy plugin declaration
datasource: ...                # Datasource plugin declaration
trigger: ...                   # Trigger plugin declaration
endpoint: ...                  # Endpoint plugin declaration
```

---

## 2. Field Validation Rules

### 2.1 Version (version)

**Pattern**: `^\d{1,4}(\.\d{1,4}){2}(-\w{1,16})?$`

| Example | Valid | Description |
|---------|-------|-------------|
| `0.0.1` | ✅ | Standard semantic version |
| `1.2.3` | ✅ | Standard semantic version |
| `1.0.0-beta` | ✅ | With pre-release identifier |
| `1.0.0-alpha1` | ✅ | With pre-release identifier |
| `1` | ❌ | Missing minor and patch version |
| `1.0` | ❌ | Missing patch version |
| `1.0.0.0.0` | ❌ | Too many version segments |
| `v1.0.0` | ❌ | Cannot have "v" prefix |

### 2.2 Type (type)

**Rule**: Must equal `plugin`

```yaml
type: plugin  # Only valid value
```

### 2.3 Author Name (author)

**Pattern**: `^[a-z0-9_-]{1,64}$`

| Example | Valid | Description |
|---------|-------|-------------|
| `langgenius` | ✅ | Lowercase letters |
| `my-company` | ✅ | With hyphen |
| `user_123` | ✅ | With underscore and numbers |
| `MyCompany` | ❌ | No uppercase letters allowed |
| `my company` | ❌ | No spaces allowed |
| `a` | ✅ | Minimum 1 character |
| `a...64chars...` | ✅ | Maximum 64 characters |

### 2.4 Plugin Name (name)

**Pattern**: `^[a-z0-9_-]{1,128}$`

| Example | Valid | Description |
|---------|-------|-------------|
| `my-plugin` | ✅ | With hyphen |
| `my_tool_v2` | ✅ | With underscore and numbers |
| `MyPlugin` | ❌ | No uppercase letters allowed |
| `my plugin` | ❌ | No spaces allowed |

### 2.5 Internationalization Object (I18nObject)

```yaml
label:
  en_US: "English Label"      # Required, 1-1023 characters
  zh_Hans: "中文标签"          # Optional, max 1023 characters
  ja_JP: "日本語ラベル"        # Optional, max 1023 characters
  pt_BR: "Rótulo em Português" # Optional, max 1023 characters
```

**Rules**:
- `en_US`: **Required**, 1-1023 characters
- `zh_Hans`, `ja_JP`, `pt_BR`: Optional, max 1023 characters

### 2.6 Icon (icon)

**Rule**: Required, max 128 characters

```yaml
icon: icon.svg                 # Path relative to plugin root
icon_dark: icon_dark.svg       # Optional, dark theme icon
```

### 2.7 Runtime Metadata (meta)

```yaml
meta:
  version: "0.0.1"             # Required, semantic version
  arch:                        # Required, supported architectures
    - amd64                    # x86_64 architecture
    - arm64                    # ARM64 architecture
  runner:                      # Required, runtime configuration
    language: python           # Required, currently only "python" supported
    version: "3.12"            # Required, Python version, max 128 characters
    entrypoint: main           # Required, entry module, max 256 characters
  minimum_dify_version: "0.8.0" # Optional, minimum Dify version
```

**Supported Architectures**:
- `amd64` - x86_64 architecture
- `arm64` - ARM64 architecture

**Supported Languages**:
- `python` - Currently the only supported language

### 2.8 Resource Requirements (resource)

```yaml
resource:
  memory: 268435456            # Required, memory limit (bytes)
  permission:                  # Optional, permission configuration
    tool:
      enabled: true            # Enable tool invocation permission
    model:
      enabled: true            # Enable model invocation permission
      llm: true                # LLM invocation
      text_embedding: true     # Text embedding
      rerank: true             # Reranking
      tts: true                # Text-to-speech
      speech2text: true        # Speech-to-text
      moderation: true         # Content moderation
    node:
      enabled: true            # Enable node invocation permission
    endpoint:
      enabled: true            # Enable endpoint registration permission
    app:
      enabled: true            # Enable app invocation permission
    storage:
      enabled: true            # Enable storage permission
      size: 1048576            # Storage size limit (bytes)
```

**Storage Size Limits**:
- Minimum: 1024 bytes (1 KB)
- Maximum: 1073741824 bytes (1 GB)

### 2.9 Plugin Component Declarations (plugins)

```yaml
plugins:
  tools:                       # Tool definition file list
    - provider/tools/tool1.yaml
    - provider/tools/tool2.yaml
  models:                      # Model definition file list
    - provider/models/model1.yaml
  endpoints:                   # Endpoint definition file list
    - provider/endpoints/endpoint1.yaml
  agent_strategies:            # Agent strategy definition file list
    - provider/agent_strategies/strategy1.yaml
  datasources:                 # Datasource definition file list
    - provider/datasources/ds1.yaml
  triggers:                    # Trigger definition file list
    - provider/triggers/trigger1.yaml
```

**Rule**: Each path max 128 characters

### 2.10 Tags (tags)

**Valid Tag Values**:
```yaml
tags:
  - search           # Search
  - image            # Image
  - videos           # Videos
  - weather          # Weather
  - finance          # Finance
  - design           # Design
  - travel           # Travel
  - social           # Social
  - news             # News
  - medical          # Medical
  - productivity     # Productivity
  - education        # Education
  - business         # Business
  - entertainment    # Entertainment
  - utilities        # Utilities
  - agent            # Agent
  - rag              # RAG
  - other            # Other
  - trigger          # Trigger
```

### 2.11 Plugin Type Mutual Exclusion Rules

| Declared Type | Can Combine With | Cannot Combine With |
|---------------|------------------|---------------------|
| `tool` | `endpoint` | `model`, `agent_strategy`, `datasource`, `trigger` |
| `model` | None | All other types |
| `agent_strategy` | None | All other types |
| `datasource` | None | All other types |
| `trigger` | None | All other types |
| `endpoint` | `tool` | `model`, `agent_strategy`, `datasource`, `trigger` |

---

## 3. Plugin Type Declarations

### 3.1 Tool Plugin Declaration

```yaml
tool:
  identity:
    author: your-name            # Required
    name: tool-provider-name     # Required, pattern: ^[a-zA-Z0-9_-]+$
    description:                 # Optional
      en_US: "Provider description"
      zh_Hans: "提供者描述"
    icon: icon.svg               # Required
    icon_dark: icon_dark.svg     # Optional
    label:                       # Required
      en_US: "Provider Label"
      zh_Hans: "提供者标签"
    tags:                        # Optional
      - productivity

  credentials_schema:            # Optional, credential configuration
    - name: api_key              # Field name, 1-1023 characters
      type: secret-input         # Type (see below)
      required: true             # Whether required
      default: ""                # Default value
      label:
        en_US: "API Key"
        zh_Hans: "API 密钥"
      help:                      # Help text
        en_US: "Enter your API key"
      placeholder:               # Placeholder
        en_US: "sk-..."
      url: "https://example.com/api-keys"  # Help link

  oauth_schema:                  # Optional, OAuth configuration
    client_schema:
      - name: client_id
        type: text-input
        required: true
        label:
          en_US: "Client ID"
    credentials_schema:
      - name: access_token
        type: secret-input
        required: true
        label:
          en_US: "Access Token"

  tools:                         # Required, tool list
    - identity:
        author: your-name        # Required
        name: tool-name          # Required, pattern: ^[a-zA-Z0-9_-]+$
        label:
          en_US: "Tool Label"
          zh_Hans: "工具标签"
      description:               # Required
        human:
          en_US: "Human-readable description"
          zh_Hans: "人类可读描述"
        llm: "LLM-readable description for tool selection"
      parameters:                # Tool parameters
        - name: query            # Parameter name, 1-1023 characters
          type: string           # Parameter type (see below)
          label:
            en_US: "Query"
            zh_Hans: "查询"
          human_description:     # Required
            en_US: "Search query"
            zh_Hans: "搜索查询"
          llm_description: "The search query string"  # LLM description
          form: llm              # Form type: schema | form | llm
          required: true         # Whether required
          default: ""            # Default value
          min: 0                 # Minimum value (numeric types)
          max: 100               # Maximum value (numeric types)
          precision: 2           # Precision (numeric types)
          options:               # Options (select type)
            - value: option1
              label:
                en_US: "Option 1"
          scope: "all"           # Scope (specific types)
      output_schema:             # Optional, output JSON Schema
        type: object
        properties:
          result:
            type: string
      has_runtime_parameters: false  # Whether has runtime parameters
```

#### Credential/Configuration Types (credentials_schema.type)

| Type | Description |
|------|-------------|
| `secret-input` | Sensitive input (e.g., API key) |
| `text-input` | Plain text input |
| `select` | Dropdown selection |
| `boolean` | Boolean switch |
| `model-selector` | Model selector |
| `app-selector` | App selector |
| `array[tools]` | Tool array selector |
| `any` | Any type |

#### Tool Parameter Types (parameters.type)

| Type | Description |
|------|-------------|
| `string` | String |
| `number` | Number |
| `boolean` | Boolean |
| `select` | Dropdown selection |
| `secret-input` | Sensitive input |
| `file` | Single file |
| `files` | Multiple files |
| `app-selector` | App selector |
| `model-selector` | Model selector |
| `any` | Any type |
| `dynamic-select` | Dynamic dropdown selection |
| `array` | Array |
| `object` | Object |
| `checkbox` | Checkbox |

#### Parameter Form Types (parameters.form)

| Type | Description |
|------|-------------|
| `schema` | Defined in Schema |
| `form` | User form input |
| `llm` | LLM auto-fill |

#### Scope Configuration

**model-selector Scope**:
```yaml
scope: "llm"                    # Single
scope: "llm&text-embedding"     # Combined using & separator
```
Valid values: `all`, `llm`, `text-embedding`, `rerank`, `tts`, `speech2text`, `moderation`, `vision`, `document`, `tool-call`

**app-selector Scope**:
```yaml
scope: "all"                    # All apps
scope: "chat&workflow"          # Combined
```
Valid values: `all`, `chat`, `workflow`, `completion`

**any Scope**:
```yaml
scope: "string"                 # String
scope: "string&number&object"   # Combined
```
Valid values: `string`, `number`, `object`, `array[number]`, `array[string]`, `array[object]`, `array[file]`

---

### 3.2 Model Plugin Declaration

```yaml
model:
  provider: provider-name        # Required, max 255 characters
  label:                         # Required
    en_US: "Provider Name"
    zh_Hans: "提供者名称"
  description:                   # Optional
    en_US: "Provider description"
  icon_small:                    # Optional, small icon
    en_US: icon_small.svg
  icon_large:                    # Optional, large icon
    en_US: icon_large.svg
  background: "#FFFFFF"          # Optional, background color
  help:                          # Optional, help information
    title:
      en_US: "Help Title"
    url:
      en_US: "https://help.example.com"

  supported_model_types:         # Required, supported model types
    - llm
    - text-embedding
    - rerank
    - speech2text
    - moderation
    - tts
    - text2img
    - multimodal-embedding
    - multimodal-rerank

  configurate_methods:           # Required, configuration methods
    - predefined-model           # Predefined model
    - customizable-model         # Customizable model

  provider_credential_schema:    # Optional, provider credentials
    credential_form_schemas:
      - variable: api_key        # Variable name, max 255 characters
        label:
          en_US: "API Key"
        type: secret-input       # text-input | secret-input | select | radio | switch
        required: true
        default: ""              # Max 255 characters
        placeholder:
          en_US: "Enter API key"
        max_length: 256
        options:                 # For select/radio types
          - label:
              en_US: "Option 1"
            value: option1       # Max 255 characters
            show_on:             # Conditional display
              - variable: other_field
                value: some_value
        show_on:                 # Conditional display
          - variable: provider_type
            value: custom

  model_credential_schema:       # Optional, model credentials
    model:
      label:
        en_US: "Model Name"
      placeholder:
        en_US: "Enter model name"
    credential_form_schemas:
      - variable: model_id
        label:
          en_US: "Model ID"
        type: text-input
        required: true

  models:                        # Optional, predefined model list
    - model: gpt-4               # Required, model identifier, max 255 characters
      label:
        en_US: "GPT-4"
      model_type: llm            # Required
      features:                  # Optional, feature list
        - vision
        - tool-use
      fetch_from: predefined-model  # predefined-model | customizable-model
      model_properties:          # Optional, model properties
        context_size: 128000
        max_tokens: 4096
      deprecated: false          # Whether deprecated
      parameter_rules:           # Parameter rules, max 128 entries
        - name: temperature      # Required, max 255 characters
          use_template: temperature  # Use predefined template
        - name: max_tokens
          label:
            en_US: "Max Tokens"
          type: int              # float | int | string | boolean | text
          required: false
          default: 4096
          min: 1
          max: 128000
          help:
            en_US: "Maximum output tokens"
      pricing:                   # Optional, pricing information
        input: 0.00003
        output: 0.00006
        unit: 0.001
        currency: USD
```

#### Model Types (model_type)

| Type | Description |
|------|-------------|
| `llm` | Language model |
| `text-embedding` | Text embedding |
| `rerank` | Reranking |
| `speech2text` | Speech-to-text |
| `moderation` | Content moderation |
| `tts` | Text-to-speech |
| `text2img` | Text-to-image |
| `multimodal-embedding` | Multimodal embedding |
| `multimodal-rerank` | Multimodal reranking |

#### Parameter Templates (use_template)

Predefined parameter templates that can be directly referenced:
- `temperature` - Temperature parameter
- `top_p` - Top-P sampling
- `top_k` - Top-K sampling
- `presence_penalty` - Presence penalty
- `frequency_penalty` - Frequency penalty
- `max_tokens` - Maximum tokens
- `response_format` - Response format
- `json_schema` - JSON Schema

---

### 3.3 Agent Strategy Plugin Declaration

```yaml
agent_strategy:
  identity:
    author: your-name           # Required
    name: strategy-provider     # Required, pattern: ^[a-zA-Z0-9_-]+$
    description:
      en_US: "Strategy provider description"
    icon: icon.svg              # Required
    label:
      en_US: "Strategy Provider"
    tags:
      - agent

  strategies:                   # Required
    - identity:
        author: your-name       # Required
        name: my-strategy       # Required, pattern: ^[a-zA-Z0-9_-]+$
        label:
          en_US: "My Strategy"
      description:              # Required
        en_US: "Strategy description"
      parameters:
        - name: model
          type: model-selector  # Special: array[tools] (tool selector)
          scope: "llm"
          required: true
          label:
            en_US: "Model"
          human_description:
            en_US: "Select a model"
          form: form
        - name: tools
          type: array[tools]    # Agent-specific type
          required: true
          label:
            en_US: "Tools"
          human_description:
            en_US: "Select tools"
          form: form
      output_schema:            # Optional
        type: object
        properties:
          result:
            type: string
      features:                 # Optional, feature list
        - streaming
```

#### Agent Parameter Types

In addition to common types, Agent Strategy has:
- `array[tools]` - Tool selector, allows selecting available tools

---

### 3.4 Datasource Plugin Declaration

```yaml
datasource:
  identity:
    author: your-name           # Required
    name: datasource-provider   # Required
    description:                # Required
      en_US: "Datasource provider"
    icon: icon.svg              # Required
    label:                      # Required
      en_US: "Datasource Provider"
    tags:
      - productivity

  credentials_schema:           # Optional
    - name: api_key
      type: secret-input
      required: true
      label:
        en_US: "API Key"

  oauth_schema:                 # Optional
    client_schema: []
    credentials_schema: []

  provider_type: website_crawl  # Required, datasource type
  # Valid values: website_crawl | online_document | online_drive

  datasources:                  # Required
    - identity:
        author: your-name       # Required
        name: crawler           # Required
        label:
          en_US: "Web Crawler"
      parameters:               # Required, at least one
        - name: url
          type: string          # string | number | boolean | select | secret-input
          required: true
          label:
            en_US: "URL"
          description:
            en_US: "URL to crawl"
      description:              # Required
        en_US: "Crawl a website"
      output_schema:            # Optional
        type: object
        properties:
          content:
            type: string
```

#### Datasource Types (provider_type)

| Type | Description |
|------|-------------|
| `website_crawl` | Website crawling |
| `online_document` | Online document |
| `online_drive` | Cloud storage |

---

### 3.5 Trigger Plugin Declaration

```yaml
trigger:
  identity:
    author: your-name           # Required
    name: trigger-provider      # Required, pattern: ^[a-zA-Z0-9_-]+$
    description:
      en_US: "Trigger provider"
    icon: icon.svg              # Required
    icon_dark: icon_dark.svg    # Optional
    label:                      # Required
      en_US: "Trigger Provider"
    tags:
      - trigger

  subscription_schema:          # Required, subscription parameters
    - name: webhook_url
      type: text-input
      required: true
      label:
        en_US: "Webhook URL"

  subscription_constructor:     # Optional, subscription constructor
    parameters:
      - name: event_type
        type: select
        required: true
        label:
          en_US: "Event Type"
        options:
          - value: push
            label:
              en_US: "Push"
    credentials_schema:
      - name: secret
        type: secret-input
        required: true
        label:
          en_US: "Secret"
    oauth_schema:               # Optional
      client_schema: []
      credentials_schema: []

  events:                       # Optional, event list
    - identity:
        author: your-name       # Required
        name: on-push           # Required, pattern: ^[a-zA-Z0-9_-]+$
        label:
          en_US: "On Push"
      parameters:
        - name: branch
          type: string          # string | number | boolean | select | file | files | model-selector | app-selector | object | array | dynamic-select | checkbox
          required: false
          label:
            en_US: "Branch"
      description:              # Required
        en_US: "Triggered on push event"
      output_schema:            # Optional
        type: object
        properties:
          commit_id:
            type: string
```

---

### 3.6 Endpoint Plugin Declaration

```yaml
endpoint:
  settings:                     # Optional, endpoint configuration
    - name: base_path
      type: text-input
      required: false
      label:
        en_US: "Base Path"

  endpoints:                    # Endpoint list
    - path: /api/webhook        # Required
      method: POST              # Required: HEAD | GET | POST | PUT | DELETE | OPTIONS
      hidden: false             # Optional, whether hidden
    - path: /api/status
      method: GET

  endpoint_files:               # Optional, endpoint definition files
    - endpoints/webhook.yaml
```

---

## 4. Complete Examples

### 4.1 Tool Plugin Complete Example

```yaml
version: "1.0.0"
type: plugin
author: langgenius
name: web-search
label:
  en_US: "Web Search"
  zh_Hans: "网页搜索"
description:
  en_US: "Search the web using various search engines"
  zh_Hans: "使用多种搜索引擎搜索网页"
icon: icon.svg
icon_dark: icon_dark.svg
created_at: 2024-01-01T00:00:00Z

meta:
  version: "1.0.0"
  arch:
    - amd64
    - arm64
  runner:
    language: python
    version: "3.12"
    entrypoint: main
  minimum_dify_version: "0.8.0"

resource:
  memory: 268435456
  permission:
    tool:
      enabled: true
    storage:
      enabled: true
      size: 10485760

plugins:
  tools:
    - provider/tools/search.yaml

tags:
  - search
  - productivity

tool:
  identity:
    author: langgenius
    name: web-search
    description:
      en_US: "Web search provider"
      zh_Hans: "网页搜索提供者"
    icon: icon.svg
    label:
      en_US: "Web Search"
      zh_Hans: "网页搜索"
    tags:
      - search

  credentials_schema:
    - name: api_key
      type: secret-input
      required: true
      label:
        en_US: "API Key"
        zh_Hans: "API 密钥"
      help:
        en_US: "Get your API key from the dashboard"
        zh_Hans: "从控制台获取 API 密钥"
      placeholder:
        en_US: "Enter your API key"
        zh_Hans: "输入您的 API 密钥"
    - name: search_engine
      type: select
      required: true
      default: google
      label:
        en_US: "Search Engine"
        zh_Hans: "搜索引擎"
      options:
        - value: google
          label:
            en_US: "Google"
        - value: bing
          label:
            en_US: "Bing"

  tools:
    - identity:
        author: langgenius
        name: search
        label:
          en_US: "Search"
          zh_Hans: "搜索"
      description:
        human:
          en_US: "Search the web for information"
          zh_Hans: "搜索网页获取信息"
        llm: "Search the web using the specified query and return relevant results"
      parameters:
        - name: query
          type: string
          label:
            en_US: "Query"
            zh_Hans: "查询"
          human_description:
            en_US: "The search query"
            zh_Hans: "搜索查询"
          llm_description: "The search query string"
          form: llm
          required: true
        - name: max_results
          type: number
          label:
            en_US: "Max Results"
            zh_Hans: "最大结果数"
          human_description:
            en_US: "Maximum number of results to return"
            zh_Hans: "返回的最大结果数"
          form: form
          required: false
          default: 10
          min: 1
          max: 100
      output_schema:
        type: object
        properties:
          results:
            type: array
            items:
              type: object
              properties:
                title:
                  type: string
                url:
                  type: string
                snippet:
                  type: string
```

### 4.2 Model Plugin Complete Example

```yaml
version: "1.0.0"
type: plugin
author: langgenius
name: openai-compatible
label:
  en_US: "OpenAI Compatible"
  zh_Hans: "OpenAI 兼容"
description:
  en_US: "OpenAI API compatible model provider"
  zh_Hans: "OpenAI API 兼容模型提供者"
icon: icon.svg
created_at: 2024-01-01T00:00:00Z

meta:
  version: "1.0.0"
  arch:
    - amd64
    - arm64
  runner:
    language: python
    version: "3.12"
    entrypoint: main

resource:
  memory: 536870912
  permission:
    model:
      enabled: true
      llm: true
      text_embedding: true

plugins:
  models:
    - provider/models/llm.yaml
    - provider/models/embedding.yaml

tags:
  - utilities

model:
  provider: openai-compatible
  label:
    en_US: "OpenAI Compatible"
    zh_Hans: "OpenAI 兼容"
  description:
    en_US: "Connect to any OpenAI API compatible endpoint"
    zh_Hans: "连接任何 OpenAI API 兼容端点"
  icon_small:
    en_US: icon_small.svg
  icon_large:
    en_US: icon_large.svg

  supported_model_types:
    - llm
    - text-embedding

  configurate_methods:
    - customizable-model

  provider_credential_schema:
    credential_form_schemas:
      - variable: api_key
        label:
          en_US: "API Key"
          zh_Hans: "API 密钥"
        type: secret-input
        required: true
        placeholder:
          en_US: "Enter your API key"
      - variable: api_base
        label:
          en_US: "API Base URL"
          zh_Hans: "API 基础 URL"
        type: text-input
        required: true
        default: "https://api.openai.com/v1"
        placeholder:
          en_US: "https://api.openai.com/v1"

  model_credential_schema:
    model:
      label:
        en_US: "Model Name"
        zh_Hans: "模型名称"
      placeholder:
        en_US: "e.g., gpt-4"
    credential_form_schemas:
      - variable: context_size
        label:
          en_US: "Context Size"
          zh_Hans: "上下文大小"
        type: text-input
        required: false
        default: "4096"
```

---

## 5. Common Errors and Solutions

### 5.1 Version Number Error

```
❌ Error: version: "1"
   Message: Field validation for 'Version' failed on the 'version' tag

✅ Correct: version: "1.0.0"
```

### 5.2 Name Format Error

```
❌ Error: name: "My Plugin"
   Message: plugin name not match regex pattern

✅ Correct: name: "my-plugin"
```

### 5.3 Missing Required Field

```
❌ Error: label: {}
   Message: Field validation for 'EnUS' failed on the 'required' tag

✅ Correct:
   label:
     en_US: "Label"
```

### 5.4 Storage Size Out of Range

```
❌ Error: size: 500  # Less than 1024
   Message: Field validation for 'Size' failed on the 'min' tag

❌ Error: size: 2147483648  # Greater than 1GB
   Message: Field validation for 'Size' failed on the 'max' tag

✅ Correct: size: 1048576  # 1MB
```

### 5.5 Type Mutual Exclusion Error

```
❌ Error: Declaring both model and tool
   Message: model and tool cannot be provided at the same time

✅ Correct: Declare only one exclusive type, or use allowed combinations (tool + endpoint)
```

### 5.6 Invalid Parameter Type

```
❌ Error: type: "invalid-type"
   Message: Field validation for 'Type' failed on the 'tool_parameter_type' tag

✅ Correct: type: "string"
```

### 5.7 Invalid Tag

```
❌ Error: tags: ["invalid-tag"]
   Message: Field validation for 'Tags[0]' failed on the 'plugin_tag' tag

✅ Correct: tags: ["productivity", "utilities"]
```

### 5.8 Scope Configuration Error

```
❌ Error:
   type: app-selector
   scope: "invalid"
   Message: Field validation for 'Scope' failed on the 'is_scope' tag

✅ Correct:
   type: app-selector
   scope: "all"  # Or "chat", "workflow", "completion"
```

---

## Appendix: Validator Registry

All custom validators list (defined in `pkg/validators/`):

| Validator Name | Purpose |
|----------------|---------|
| `version` | Semantic version validation |
| `plugin_tag` | Plugin tag validation |
| `is_available_language` | Programming language validation |
| `is_available_arch` | CPU architecture validation |
| `tool_identity_name` | Tool name validation |
| `tool_parameter_type` | Tool parameter type validation |
| `tool_parameter_form` | Parameter form type validation |
| `tool_provider_identity_name` | Tool provider name validation |
| `parameter_auto_generate_type` | Parameter auto-generate type validation |
| `is_basic_type` | Basic type validation |
| `model_type` | Model type validation |
| `model_provider_configurate_method` | Model configuration method validation |
| `model_provider_form_type` | Model form type validation |
| `model_parameter_type` | Model parameter type validation |
| `parameter_rule` | Parameter rule validation |
| `is_available_endpoint_method` | HTTP method validation |
| `event_parameter_type` | Event parameter type validation |
| `event_identity_name` | Event name validation |
| `trigger_provider_identity_name` | Trigger provider name validation |
| `agent_strategy_parameter_type` | Agent strategy parameter type validation |
| `datasource_provider_type` | Datasource type validation |
| `datasource_parameter_type` | Datasource parameter type validation |
| `credential_type` | Credential type validation |
| `is_scope` | Scope validation |
| `is_app_selector_scope` | App selector scope validation |
| `is_model_config_scope` | Model config scope validation |
| `is_tool_selector_scope` | Tool selector scope validation |
| `plugin_unique_identifier` | Plugin unique identifier validation |
