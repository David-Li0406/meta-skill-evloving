# GitHub Copilot Setup Documentation

This document describes the GitHub Copilot configuration for the MCP-B repository, following [GitHub's best practices for Copilot coding agent](https://docs.github.com/en/copilot/tutorials/coding-agent/get-the-best-results).

## Overview

The MCP-B repository is configured with comprehensive GitHub Copilot instructions to help the coding agent understand the project structure, coding standards, and workflows. This setup includes:

1. **Repository-wide instructions** - General guidelines for all Copilot interactions
2. **Path-specific instructions** - Specialized guidelines for different file types
3. **Custom agents** - Specialized agents for ML/AI pipeline tasks
4. **Setup automation** - Pre-configured development environment

## File Structure

```
.github/
├── copilot-instructions.md              # Repository-wide instructions
├── instructions/                         # Path-specific instructions
│   ├── python-code.instructions.md      # Python file guidelines
│   └── test-files.instructions.md       # Test file guidelines
├── agents/                               # Custom specialized agents
│   ├── data-collector.agent.md          # Data collection agent
│   ├── data-prep.agent.md               # Data preparation agent
│   ├── model-trainer.agent.md           # Model training agent
│   ├── results-analyst.agent.md         # Results analysis agent
│   ├── visualization.agent.md           # Visualization agent
│   └── publisher.agent.md               # Documentation publishing agent
└── workflows/
    └── copilot-setup-steps.yml          # Environment setup for Copilot
```

## Repository-Wide Instructions

Located at `.github/copilot-instructions.md`, this file provides:

- **Project Overview**: What MCP-B is and its core components (MCP-B Protocol, AMUM, QCI, ETHIC)
- **Code Style Guidelines**: PEP 8, type hints, docstrings, line length (100 chars)
- **Project Structure**: File organization and module purposes
- **Key Concepts**: INQC commands, binary state flags
- **Testing Guidelines**: How to run tests, test patterns to follow
- **Dependencies**: Core and dev dependencies
- **Workflow Commands**: Verified commands for development, testing, and deployment

### Key Features

1. **Verified Commands**: All commands have been tested to ensure they work correctly
2. **MCP Server Integration**: Instructions for using Serena (#serena) for code analysis and Context7 (#context7) for documentation
3. **Pre-commit Checklist**: Clear steps to run before creating pull requests

## Path-Specific Instructions

### Python Code Instructions (`.github/instructions/python-code.instructions.md`)

Applies to: `**/*.py`

Provides detailed guidelines for Python development including:
- Type hints requirements and examples
- Docstring formatting
- Import organization
- F-string usage
- Error handling patterns
- Project-specific conventions (binary flags, INQC commands)
- Testing patterns

### Test File Instructions (`.github/instructions/test-files.instructions.md`)

Applies to: `**/test_*.py`

Specialized guidelines for test files:
- Test naming conventions
- Test structure and organization
- Fixture usage
- Edge case testing
- Performance testing
- Mocking and patching
- Test quality checklist

## Custom Agents

Six specialized agents are defined for ML/AI pipeline tasks:

| Agent | File | Purpose |
|-------|------|---------|
| 🔬 Data Collector | `data-collector.agent.md` | Gathering and ingesting data |
| 🧹 Data Prep | `data-prep.agent.md` | Cleaning and transforming data |
| 🤖 Model Trainer | `model-trainer.agent.md` | Training and optimizing models |
| 📊 Results Analyst | `results-analyst.agent.md` | Analyzing model performance |
| 🎨 Visualization | `visualization.agent.md` | Creating charts and visualizations |
| 📝 Publisher | `publisher.agent.md` | Generating and publishing documentation |

Each agent has:
- YAML frontmatter with metadata (name, description, tools, emoji, team)
- Role description and responsibilities
- Tool usage guidelines
- Code patterns to follow
- Best practices specific to their domain

## Environment Setup Workflow

The `copilot-setup-steps.yml` workflow pre-configures the development environment for Copilot coding agent:

### What It Does

1. Checks out the repository
2. Sets up Python 3.11
3. Installs all dependencies (dev + core)
4. Verifies installation
5. Runs smoke tests
6. Provides setup summary

### Benefits

- **Faster Agent Response**: Dependencies are pre-installed, so Copilot can start working immediately
- **Reliable Environment**: Consistent setup across all Copilot sessions
- **Quick Validation**: Smoke tests ensure everything is configured correctly

## How Copilot Uses These Instructions

### Order of Precedence

1. **Path-specific instructions** (`.github/instructions/*.instructions.md`) - Applied first based on file glob patterns
2. **Repository-wide instructions** (`.github/copilot-instructions.md`) - Applied to all files
3. **Custom agent instructions** (`.github/agents/*.agent.md`) - Used when specific agent is invoked

### Best Practices Followed

✅ **Clear and Concise**: Instructions are direct and actionable  
✅ **Example-Driven**: Code examples demonstrate correct patterns  
✅ **Logically Divided**: Repository-wide vs. path-specific vs. agent-specific  
✅ **Verified Commands**: All commands have been tested  
✅ **Security Focused**: No secrets in instructions  
✅ **Automated Setup**: Pre-configured environment reduces errors  

## For Developers

### Using the Instructions

When working with Copilot:

1. **For general coding**: Copilot automatically uses repository-wide instructions
2. **For Python files**: Python-specific instructions apply automatically
3. **For test files**: Test-specific instructions apply automatically
4. **For specialized tasks**: Invoke custom agents with `@agent-name`

### Updating Instructions

When updating instructions:

1. Keep them concise (< 1000 lines per file)
2. Test all commands before documenting them
3. Use examples to clarify guidelines
4. Update related instructions if necessary
5. Run `pytest -v` to ensure changes don't break tests

### Running Pre-commit Checks

Before creating a pull request:

```bash
# Format code
black src/

# Fix linting issues
ruff check --fix src/

# Run tests
pytest -v

# Or run all at once
black src/ && ruff check --fix src/ && pytest -v
```

## Maintenance

### Regular Updates

- Review instructions quarterly or when major changes occur
- Update examples when APIs change
- Add new path-specific instructions for new file types
- Update custom agents when workflows change

### Metrics to Monitor

- Copilot PR success rate
- Time to merge Copilot-generated PRs
- Number of review iterations needed
- Developer satisfaction with Copilot suggestions

## References

- [GitHub Copilot Best Practices](https://docs.github.com/en/copilot/tutorials/coding-agent/get-the-best-results)
- [Custom Instructions Documentation](https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot)
- [Creating Custom Agents](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/create-custom-agents)
- [Customizing Development Environment](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/coding-agent/customize-the-agent-environment)

## Questions or Issues?

If you encounter issues with Copilot instructions or have suggestions for improvements:

1. Open an issue in the repository
2. Tag with `copilot-instructions` label
3. Describe the problem or suggestion clearly
4. Include examples if applicable
