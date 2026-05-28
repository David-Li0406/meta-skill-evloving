import os
import argparse

def create_instruction(name, description, apply_to):
    if not name.endswith('.instructions.md'):
        name += '.instructions.md'
    
    path = os.path.join('instructions', name)
    
    if os.path.exists(path):
        print(f"Error: File {path} already exists.")
        return

    content = f"""---
description: '{description}'
applyTo: '{apply_to}'
---

# {name.replace('.instructions.md', '').replace('-', ' ').title()}

## Overview
Brief introduction and context.

## Workflow
1. Step 1: Analyze the input.
2. Step 2: Execute the [Skill Name](skills/<skill-name>/SKILL.md).
3. Step 3: Verify the output.

## Rules & Constraints
- Rule 1
- Rule 2

## Best Practices
- Specific practice 1

## Code Standards
### Naming Conventions
- Rule 1

## Common Patterns
### Pattern 1
Description and example

```language
code example
```

## Validation
- Build command: `npm run build`
"""
    
    os.makedirs('instructions', exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    
    print(f"Created {path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Initialize a new instruction file.')
    parser.add_argument('name', help='Name of the instruction file (e.g., react-best-practices)')
    parser.add_argument('--description', default='Brief description of purpose', help='Description for frontmatter')
    parser.add_argument('--applyTo', default='**', help='Glob pattern for applyTo')
    
    args = parser.parse_args()
    create_instruction(args.name, args.description, args.applyTo)
