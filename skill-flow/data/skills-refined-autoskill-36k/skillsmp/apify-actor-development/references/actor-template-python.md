# Python Actor Template Reference

This document describes the complete Python actor template structure that serves as the starting point for all Python-based Apify actors.

## Template Overview

The Python empty template provides a minimal, production-ready structure for building Apify actors in Python. It includes:

- Basic Actor skeleton with async/await support
- Proper project structure with src/ directory
- Docker configuration optimized for Python
- Dependency management with requirements.txt
- Actor configuration files

## Complete File Structure

```
python-empty/
├── .actor/
│   └── actor.json                    # Actor metadata and configuration
├── src/
│   ├── __init__.py                   # Package initialization (empty)
│   ├── __main__.py                   # Entry point for execution
│   ├── main.py                       # Main actor logic
│   └── py.typed                      # PEP 561 type marker
├── .dockerignore                     # Docker build exclusions
├── .gitignore                        # Git exclusions
├── Dockerfile                        # Container image definition
├── requirements.txt                  # Python dependencies
├── README.md                         # Project documentation
└── AGENTS.md                         # Agent-specific documentation
```

## File-by-File Reference

### `.actor/actor.json`

Actor metadata and platform configuration.

```json
{
    "actorSpecification": 1,
    "name": "python-empty",
    "title": "Empty Python project",
    "description": "Empty project in Python.",
    "version": "0.0",
    "buildTag": "latest",
    "meta": {
        "templateId": "python-empty-from-agent",
        "generatedBy": "<FILL-IN-MODEL>"
    },
    "dockerfile": "../Dockerfile"
}
```

**Key fields:**
- `actorSpecification`: Always `1` (current spec version)
- `name`: Actor identifier (lowercase, hyphens)
- `title`: Human-readable name shown in UI
- `description`: Short description for marketplace
- `version`: Semantic version (e.g., "1.0.0")
- `buildTag`: Docker tag for builds (usually "latest")
- `meta.templateId`: Template identifier (use `"python-empty-from-agent"` for agent-generated actors)
- `meta.generatedBy`: **CRITICAL** - Must be filled with model name (e.g., "claude-sonnet-4-5-20250929")
- `dockerfile`: Path to Dockerfile (relative to .actor/)

**Important:**
- Always update `generatedBy` with the current model name
- Use `"python-empty-from-agent"` as templateId for agent-created actors
- Use semantic versioning for `version`
- `name` must be URL-safe (lowercase, hyphens only)

### `src/main.py`

Main actor logic with async entry point.

```python
"""Module defines the main entry point for the Apify Actor.

Feel free to modify this file to suit your specific needs.

To build Apify Actors, utilize the Apify SDK toolkit, read more at the official documentation:
https://docs.apify.com/sdk/python
"""

from __future__ import annotations

from apify import Actor


async def main() -> None:
    """Define a main entry point for the Apify Actor.

    This coroutine is executed using `asyncio.run()`, so it must remain an asynchronous function for proper execution.
    Asynchronous execution is required for communication with Apify platform, and it also enhances performance in
    the field of web scraping significantly.
    """
    async with Actor:
        Actor.log.info('Hello from the Actor!')
        # Write your code here
```

**Key points:**
- Always use `async def main()` - asynchronous execution is required
- Use `async with Actor:` context manager for proper initialization/cleanup
- `Actor.log` automatically censors sensitive data (API keys, tokens)
- Code goes inside the `async with Actor:` block

**Common patterns:**

```python
async def main() -> None:
    async with Actor:
        # 1. Get input
        actor_input = await Actor.get_input() or {}
        start_urls = actor_input.get('startUrls', [])

        # 2. Process data
        results = []
        for url_obj in start_urls:
            # Scraping logic here
            results.append({'url': url_obj['url']})

        # 3. Save output
        await Actor.push_data(results)

        Actor.log.info(f'Processed {len(results)} items')
```

### `src/__main__.py`

Entry point that executes the main coroutine.

```python
import asyncio

from .main import main

# Execute the Actor entry point.
asyncio.run(main())
```

**Key points:**
- This file should rarely be modified
- Uses `asyncio.run()` to execute the async `main()` function
- Imports `main` from the same package
- Enables running the actor as a module: `python -m src`

### `src/__init__.py`

Package initialization file (empty by default).

```python
# Empty file marking src/ as a Python package
```

**Key points:**
- Makes `src/` a proper Python package
- Usually left empty
- Can be used to expose package-level imports if needed

### `src/py.typed`

PEP 561 marker file indicating type hints are available.

```
# Empty marker file for PEP 561
```

**Key points:**
- Empty file indicating the package supports type checking
- Enables type checkers (mypy, pyright) to check your code
- Should always be present in typed packages

### `Dockerfile`

Container image definition optimized for Python actors.

```dockerfile
# First, specify the base Docker image.
# You can see the Docker images from Apify at https://hub.docker.com/r/apify/.
# You can also use any other image from Docker Hub.
FROM apify/actor-python:3.13

USER myuser

# Second, copy just requirements.txt into the Actor image,
# since it should be the only file that affects the dependency install in the next step,
# in order to speed up the build
COPY --chown=myuser:myuser requirements.txt ./

# Install the packages specified in requirements.txt,
# Print the installed Python version, pip version
# and all installed packages with their versions for debugging
RUN echo "Python version:" \
 && python --version \
 && echo "Pip version:" \
 && pip --version \
 && echo "Installing dependencies:" \
 && pip install -r requirements.txt \
 && echo "All installed Python packages:" \
 && pip freeze

# Next, copy the remaining files and directories with the source code.
# Since we do this after installing the dependencies, quick build will be really fast
# for most source file changes.
COPY --chown=myuser:myuser . ./

# Use compileall to ensure the runnability of the Actor Python code.
RUN python3 -m compileall -q src/

# Specify how to launch the source code of your Actor.
# By default, the "python3 -m ." command is run
CMD ["python3", "-m", "src"]
```

**Key points:**
- Uses official Apify Python base image (Python 3.13)
- Runs as non-root user (`myuser`) for security
- Optimized layer caching: requirements.txt copied separately
- Validates code with `compileall` before runtime
- Executes actor with `python3 -m src` (runs `src/__main__.py`)

**Available Python versions:**
- `apify/actor-python:3.13` (recommended)
- `apify/actor-python:3.12`
- `apify/actor-python:3.11`

**Build optimization:**
- Copy `requirements.txt` first for layer caching
- Dependencies are cached unless `requirements.txt` changes
- Source code changes don't trigger dependency reinstall

### `requirements.txt`

Python dependency specification.

```
# Feel free to add your Python dependencies below. For formatting guidelines, see:
# https://pip.pypa.io/en/latest/reference/requirements-file-format/

apify < 4.0.0
```

**Key points:**
- List one dependency per line
- Use version constraints for stability
- `apify` SDK is the core dependency
- Pin major versions to avoid breaking changes

**Common dependencies:**

```
apify < 4.0.0
beautifulsoup4 ~= 4.12.0
httpx ~= 0.27.0
playwright ~= 1.40.0
selenium ~= 4.16.0
lxml ~= 5.1.0
```

**Version constraint examples:**
- `apify < 4.0.0` - Any version below 4.0.0
- `httpx ~= 0.27.0` - Compatible release (>= 0.27.0, < 0.28.0)
- `playwright == 1.40.0` - Exact version
- `beautifulsoup4 >= 4.12.0` - Minimum version

### `.dockerignore`

Files to exclude from Docker builds (reduces image size and build time).

```
.git/
.github/
.venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.pytest_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/
storage/
apify_storage/
.DS_Store
*.log
```

**Key points:**
- Excludes version control (`.git/`)
- Excludes virtual environments (`.venv/`)
- Excludes Python cache files (`__pycache__/`, `*.pyc`)
- Excludes local storage directories
- Reduces Docker image size significantly

### `.gitignore`

Files to exclude from version control.

```
.venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.pytest_cache/
.coverage
htmlcov/
dist/
build/
*.egg-info/
storage/
apify_storage/
.DS_Store
*.log
.env
```

**Key points:**
- Similar to `.dockerignore` but for git
- Includes `.env` to prevent committing secrets
- Excludes local Apify storage directories
- Excludes Python build artifacts

### `README.md`

Development documentation for the project.

**Purpose:**
- Documents local development setup
- Explains how to run and test the actor
- Lists included features and resources
- Not shown in marketplace (use `.actor/ACTOR.md` for that)

**Key sections:**
- Project overview
- How to run locally
- How to deploy
- Available resources and documentation links

## Using the Template

### Step 1: Copy Template Files

```bash
# Create new actor directory
mkdir my-new-actor
cd my-new-actor

# Copy all template files including hidden ones
cp -r /path/to/python-empty/* .
cp -r /path/to/python-empty/.* .
```

### Step 2: Update Actor Configuration

Edit `.actor/actor.json`:

```json
{
    "actorSpecification": 1,
    "name": "my-scraper",
    "title": "My Product Scraper",
    "description": "Scrapes products from e-commerce sites.",
    "version": "1.0.0",
    "buildTag": "latest",
    "meta": {
        "templateId": "python-empty-from-agent",
        "generatedBy": "claude-sonnet-4-5-20250929"  // Update with current model
    },
    "dockerfile": "../Dockerfile"
}
```

### Step 3: Add Dependencies

Edit `requirements.txt`:

```
apify < 4.0.0
beautifulsoup4 ~= 4.12.0
httpx ~= 0.27.0
```

### Step 4: Implement Logic

Edit `src/main.py`:

```python
from __future__ import annotations

from apify import Actor
import httpx
from bs4 import BeautifulSoup


async def main() -> None:
    async with Actor:
        # Get input
        actor_input = await Actor.get_input() or {}
        start_urls = actor_input.get('startUrls', [])

        # Scrape data
        async with httpx.AsyncClient() as client:
            for url_obj in start_urls:
                response = await client.get(url_obj['url'])
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extract data
                title = soup.find('h1')
                await Actor.push_data({
                    'url': url_obj['url'],
                    'title': title.text if title else None
                })

        Actor.log.info('Scraping completed')
```

### Step 5: Test Locally

```bash
# Install Apify CLI if not installed
npm install -g apify-cli

# Run locally
apify run
```

### Step 6: Deploy

```bash
# Login to Apify
apify login

# Push to Apify platform
apify push
```

## Common Modifications

### Adding Input Schema

Create `.actor/input_schema.json`:

```json
{
    "title": "My Scraper Input",
    "type": "object",
    "schemaVersion": 1,
    "properties": {
        "startUrls": {
            "title": "Start URLs",
            "type": "array",
            "description": "URLs to scrape",
            "editor": "requestListSources",
            "default": [{"url": "https://example.com"}]
        },
        "maxItems": {
            "title": "Max Items",
            "type": "integer",
            "description": "Maximum number of items to scrape",
            "default": 100,
            "minimum": 1
        }
    },
    "required": ["startUrls"]
}
```

### Adding Output Schema

Create `.actor/output_schema.json`:

```json
{
    "actorOutputSchemaVersion": 1,
    "title": "Scraper Output",
    "properties": {
        "dataset": {
            "type": "string",
            "title": "📊 Dataset",
            "description": "Scraped items",
            "template": "{{links.apiDefaultDatasetUrl}}/items"
        }
    }
}
```

### Adding Browser Automation

Update `requirements.txt`:

```
apify < 4.0.0
playwright ~= 1.40.0
```

Update `src/main.py`:

```python
from playwright.async_api import async_playwright

async def main() -> None:
    async with Actor:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            await page.goto('https://example.com')
            title = await page.title()

            await Actor.push_data({'title': title})
            await browser.close()
```

## Best Practices

### Code Quality
- Use type hints: `async def main() -> None:`
- Add docstrings to functions
- Use `Actor.log` instead of `print()`
- Handle errors gracefully with try/except

### Performance
- Use `async with` for proper resource cleanup
- Batch data pushes: `await Actor.push_data(items)` instead of individual pushes
- Use `httpx.AsyncClient` for HTTP requests
- Set reasonable timeouts

### Security
- Never hardcode secrets in source code
- Use environment variables or actor input
- Run as non-root user (already configured in Dockerfile)
- Validate all input data

### Dependency Management
- Pin major versions: `apify < 4.0.0`
- Use compatible releases: `httpx ~= 0.27.0`
- Test after dependency updates
- Document version requirements

## Troubleshooting

### Import Errors

```python
# Wrong
from main import main

# Correct
from .main import main
```

### Module Not Found

Ensure `src/__init__.py` exists and `py.typed` is present.

### Docker Build Fails

Check that `requirements.txt` is properly formatted and all dependencies are available on PyPI.

### Actor Won't Start

Verify:
- `src/__main__.py` imports correctly
- `main()` is an async function
- `async with Actor:` context manager is used

## Additional Resources

- [Apify Python SDK Documentation](https://docs.apify.com/sdk/python)
- [Python Actor Tutorial](https://docs.apify.com/academy/python)
- [Actor Input Schema Guide](https://docs.apify.com/platform/actors/development/input-schema)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
