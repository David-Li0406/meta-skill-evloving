---
name: extract
description: Extract structured data from websites. Use when the user wants to scrape a webpage, extract data from a URL, or get structured information from a website.
allowed-tools: Read, Bash, Write, Glob, Grep, WebFetch
---

# Structured Data Extraction

Workflow guide for extracting structured web data using YAML configs and Python scripts.

## Core Architecture

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   YAML Config   │ ───▶ │  Python Script  │ ───▶ │     Output      │
│  (WHAT to get)  │      │ (HOW to get it) │      │  (JSON / CSV)   │
└─────────────────┘      └─────────────────┘      └─────────────────┘
```

### Separation of Concerns

| Component | Purpose | Location |
|-----------|---------|----------|
| **YAML Config** | Define WHAT to extract (selectors, fields, patterns, filters) | `configs/*.yaml` |
| **Python Script** | Execute HOW to extract (fetch pages, parse HTML, save output) | `scripts/*.py` |

**YAML Config** = Declarative rules (what data, which selectors, what transforms)
**Python Script** = Procedural execution (load config, fetch URL, extract, save)

---

## Project Structure

```
projects/<project_name>/
├── configs/          # YAML configs (WHAT to extract)
│   └── session_details.yaml
├── scripts/          # Python scripts (HOW to execute)
│   └── batch_extract.py
├── output/           # Extraction results
│   └── sessions.csv
└── docs/             # Project notes (optional)
```

---

## YAML Config: Define WHAT to Extract

Config files declare extraction rules without any execution logic.

### Basic Structure

```yaml
version: "1.0"
name: "my_extraction"
description: "What this config extracts"

source:
  url: "https://example.com/page"
  options:
    headless: true
    wait_for: "body"

output:
  format: [json, csv]
  path: "output/results"

# Standard extraction rules (for simple cases)
items:
  - name: product
    selector: "div.product"
    fields:
      title:
        selector: "h2"
        extract: text
      price:
        selector: ".price"
        extract: text
      url:
        selector: "a"
        extract: href

# Custom extraction rules (for complex cases)
custom:
  selectors:
    speakers:
      html: "span.p--medium"
    abstract:
      container: "div[style*='margin-bottom']"
      paragraphs: "p"
      min_length: 50
    topics:
      industry_pattern: 'Industry:\s*([^\n]+)'
  filters:
    exclude_patterns:
      - "|"              # Skip speaker paragraphs
    stop_markers:
      - "Prerequisite"   # Stop before prerequisites
      - "Certificate:"   # Stop before certificate info
      - "Important:"     # Stop before important notices
  technologies:
    html_selector:
      container: "div[style*='padding-bottom']"
      label: "NVIDIA Technology"
      value: "span"
```

### Config Sections

| Section | Purpose |
|---------|---------|
| `source` | URL and fetch options |
| `output` | Output format and path |
| `items` | Standard CSS selector extraction |
| `custom` | Complex extraction rules (selectors, filters, patterns) |
| `schema` | Field validation rules |

---

## Python Script: Execute the Extraction

Scripts read YAML configs and perform the actual extraction.

### Script Responsibilities

1. **Load config** - Read YAML file
2. **Fetch HTML** - Use Playwright for JS-rendered pages
3. **Parse & Extract** - Apply selectors and filters from config
4. **Transform** - Clean data (remove markers, normalize whitespace)
5. **Save output** - Write JSON/CSV

### Script Template Pattern

```python
#!/usr/bin/env python3
"""Extraction script that reads config and executes extraction."""

import yaml
from pathlib import Path
from playwright.sync_api import sync_playwright

def load_config(config_path):
    """Load extraction rules from YAML."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def extract_data(url, browser, config):
    """Extract data using rules from config."""
    custom = config.get('custom', {})
    selectors = custom.get('selectors', {})
    filters = custom.get('filters', {})

    # Use selectors from config
    speaker_selector = selectors['speakers']['html']
    # Apply filters from config
    stop_markers = filters.get('stop_markers', [])
    # ... extraction logic

def main():
    config = load_config('configs/extraction.yaml')
    # Execute extraction using config rules
    # Save to config['output']['path']

if __name__ == '__main__':
    main()
```

---

## Agent Workflow

### Phase 1: Analyze Page

1. Run `analyze_page.py` to identify page structure
2. Identify CSS selectors for target data
3. Note any special patterns (markers to filter, nested structures)

### Phase 2: Create YAML Config

1. Create `configs/<name>.yaml`
2. Define selectors for each field
3. Add filters for unwanted content (prerequisites, certificates, etc.)
4. Add stop markers if content has multiple sections

### Phase 3: Write/Adapt Script

1. Copy template or adapt existing script
2. Script reads config and applies rules
3. Script handles batch processing if needed

### Phase 4: Run & Iterate

```bash
.venv/bin/python scripts/extract.py --config configs/my_config.yaml
```

---

## Config Examples

### Simple List Extraction
See: `.claude/skills/extract/examples/configs/simple_list.yaml`

### Hierarchical Data
See: `.claude/skills/extract/examples/configs/hierarchical.yaml`

### Multiple Patterns
See: `.claude/skills/extract/examples/configs/multi_pattern.yaml`

---

## Real-World Example: GTC 2026

```
projects/gtc-2026/
├── configs/
│   ├── session_details_general.yaml      # Rules for session pages
│   └── session_details_training.yaml     # Rules for training labs
├── scripts/
│   ├── batch_extract.py                  # Generic batch extractor
│   └── batch_extract_training.py         # Training-specific extractor
└── output/
    ├── gtc-2026-talks-detailed.csv
    └── gtc-2026-training-detailed.csv
```

**Config defines**: selectors, filters (skip `|` paragraphs), stop markers (`Prerequisite`, `Certificate:`)
**Script executes**: loads config, fetches URLs, applies rules, saves CSV

---

## Script Templates

| Template | Use Case |
|----------|----------|
| `analyze_page.py` | Explore page structure before writing config |
| `extract_template.py` | Basic single-page extraction |
| `extract_with_debug.py` | Debug extraction with verbose output |

Location: `.claude/skills/extract/examples/scripts/`

---

## Important Rules

1. **Config = WHAT**: All extraction rules go in YAML
2. **Script = HOW**: Scripts read config, don't hardcode selectors
3. **Confirm schema**: Ask user for fields before creating config
4. **Use virtual env**: `.venv/bin/python`
5. **Don't modify skill**: `.claude/skills/extract/` is read-only
