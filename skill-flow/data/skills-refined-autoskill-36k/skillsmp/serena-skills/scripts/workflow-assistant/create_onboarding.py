#!/usr/bin/env python3
"""
Create project onboarding documentation
"""
import argparse
import os
import sys
from pathlib import Path


ONBOARDING_TEMPLATE = """# Project Onboarding

## Overview

[Brief description of the project and its purpose]

## Architecture

[System architecture, design patterns, and technical approach]

## Key Components

[Main modules, services, or packages and their responsibilities]

## Development Setup

### Prerequisites
- [List required tools and dependencies]

### Installation
```bash
# [Setup commands]
```

## Code Structure

```
project/
├── [key directories and their purposes]
```

## Common Tasks

### Running the Application
```bash
# [Commands to run]
```

### Testing
```bash
# [Test commands]
```

### Building
```bash
# [Build commands]
```

## Important Files

- `[file]` - [description]

## Coding Standards

[Project conventions and style guidelines]

## References

- [Links to external documentation]
- [Related resources]

---
Last Updated: [auto-generated on creation]
"""


def create_onboarding(project_root: str):
    """Create onboarding documentation"""
    
    serena_dir = Path(project_root) / ".tmp" / ".serena-skills"
    serena_dir.mkdir(parents=True, exist_ok=True)
    
    onboarding_file = serena_dir / "onboarding.md"
    
    if onboarding_file.exists():
        return f"Onboarding already exists: {onboarding_file}"
    
    # Add timestamp
    from datetime import datetime
    content = ONBOARDING_TEMPLATE.replace(
        "[auto-generated on creation]",
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    
    onboarding_file.write_text(content, encoding='utf-8')
    
    return f"Onboarding created: {onboarding_file}"


def main():
    parser = argparse.ArgumentParser(description="Create project onboarding")
    parser.add_argument("--project-root", required=True, help="Absolute path to project root")
    
    args = parser.parse_args()
    
    try:
        result = create_onboarding(args.project_root)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
