# Debugging Skill

Systematic debugging workflows for frontend, backend, tests, devops, and web issues.

## Structure

```
debugging/
├── SKILL.md                    # Main entry point (router/coordinator)
├── README.md                   # This file
├── workflows/                  # Step-by-step debugging procedures
│   ├── debug-frontend.md       # Browser, React/Vue, CSS debugging
│   ├── debug-backend.md        # API, server, database debugging
│   ├── debug-tests.md          # Test failures, flaky tests
│   ├── debug-devops.md         # Container, deployment, infra issues
│   └── debug-web.md            # Network, CORS, SSL, performance
└── context/                    # Supporting knowledge
    ├── patterns/
    │   ├── isolation-strategies.md   # Binary search, bisect techniques
    │   └── common-errors.md          # Error patterns and solutions
    ├── checklists/
    │   ├── pre-debug.md              # Info to gather before debugging
    │   └── root-cause.md             # Root cause analysis checklist
    └── tools/
        ├── browser-tools.md          # DevTools reference
        └── cli-tools.md              # Command-line debugging tools
```

## Usage

The skill auto-routes based on the type of issue:

| Symptom | Workflow |
|---------|----------|
| UI bugs, JS errors, CSS issues | `debug-frontend` |
| API errors, server crashes | `debug-backend` |
| Failing tests, flaky tests | `debug-tests` |
| Deployment failures, container issues | `debug-devops` |
| CORS, network, performance | `debug-web` |

## Customization

**To modify the debugging steps for a domain:**

Edit the corresponding workflow file in `workflows/`. Each workflow contains:
- When to use this workflow
- Step-by-step debugging process
- Common patterns and fixes
- Quick reference tables

**To add new error patterns:**

Edit `context/patterns/common-errors.md`

**To update tool references:**

Edit files in `context/tools/`

## Key Principles

1. **Reproduce First** - Can't debug what you can't reproduce
2. **Isolate Aggressively** - Binary search to narrow scope
3. **Read the Error** - Error messages often tell you the answer
4. **One Change at a Time** - Never change multiple things at once
5. **Trust Nothing** - Verify all assumptions
