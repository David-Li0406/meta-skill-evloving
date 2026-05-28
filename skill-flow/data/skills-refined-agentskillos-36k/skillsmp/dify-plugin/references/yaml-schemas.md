# YAML Schema Reference

Common patterns for Dify plugin YAML configurations.

## Credential Types

```yaml
credentials_for_provider:
  # Secret input (encrypted)
  api_key:
    type: secret-input
    required: true
    label:
      en_US: API Key
    placeholder:
      en_US: Enter your API key
    help:
      en_US: Get from settings page
    url: https://example.com/settings

  # Text input
  endpoint:
    type: text-input
    required: false
    default: https://api.example.com
    label:
      en_US: API Endpoint

  # Select
  region:
    type: select
    required: true
    default: us-east-1
    options:
      - value: us-east-1
        label:
          en_US: US East
      - value: eu-west-1
        label:
          en_US: EU West

  # Boolean
  debug_mode:
    type: boolean
    required: false
    default: false
    label:
      en_US: Debug Mode
```

## Parameter Types

```yaml
parameters:
  # String with LLM form (filled by AI)
  - name: query
    type: string
    required: true
    form: llm
    label:
      en_US: Query
    llm_description: The search query

  # Number with user form
  - name: limit
    type: number
    required: false
    form: form
    default: 10
    min: 1
    max: 100
    label:
      en_US: Limit

  # Select with options
  - name: format
    type: select
    required: true
    form: form
    options:
      - value: json
        label:
          en_US: JSON
      - value: text
        label:
          en_US: Text

  # File input
  - name: document
    type: file
    required: true
    form: form
    label:
      en_US: Document
```

## I18n Object Pattern

All labels support multi-language:

```yaml
label:
  en_US: English Label
  zh_Hans: 中文标签
  ja_JP: 日本語ラベル
```

## Identity Block

```yaml
identity:
  author: your-name
  name: unique_identifier
  label:
    en_US: Display Name
  description:
    en_US: Description text
  icon: icon.svg
  tags:
    - search
    - utility
```

## Extra Python Source

Link YAML to Python implementation:

```yaml
extra:
  python:
    source: path/to/file.py
```
