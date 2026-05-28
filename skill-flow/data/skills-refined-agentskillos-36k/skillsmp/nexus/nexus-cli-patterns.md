---
skill: nexus-cli-patterns
description: CLI command patterns, arguments, execution, and automation for Nexus workflows
priority: HIGH
tags: [nexus, cli, command-line, automation, scripting]
---

# Nexus CLI Patterns

Master command-line interface patterns for Nexus workflows.

## Basic Commands

```bash
# Execute workflow
nexus run workflow-name

# Execute with parameters
nexus run workflow-name --param1 value1 --param2 value2

# List available workflows
nexus list

# Get workflow information
nexus info workflow-name

# Help
nexus --help
nexus run --help
```

## Workflow Execution

```bash
# Simple execution
nexus run data-processor

# With parameters
nexus run data-processor --input-file data.csv --output-format json

# With JSON parameters
nexus run data-processor --params '{"input": "data.csv", "limit": 100}'

# With session
nexus run data-processor --session session-123 --step 2
```

## Parameter Formats

```bash
# String parameters
nexus run workflow --name "John Doe"

# Integer parameters
nexus run workflow --count 100 --limit 50

# Boolean parameters
nexus run workflow --verbose true --debug false

# Array parameters
nexus run workflow --items "[1,2,3,4,5]"

# JSON object parameters
nexus run workflow --config '{"key": "value", "nested": {"a": 1}}'
```

## CLI Configuration

```python
from nexus import Nexus

app = Nexus()

# Configure CLI behavior
app.cli.interactive = True          # Enable interactive prompts
app.cli.auto_complete = True        # Tab completion
app.cli.progress_bars = True        # Progress indicators
app.cli.colored_output = True       # Colorized output
app.cli.streaming_output = True     # Stream output
app.cli.command_history = True      # Command history
```

## Interactive Mode

```bash
# Start interactive shell
nexus shell

# Interactive prompt
nexus> run data-processor --input data.csv
nexus> info data-processor
nexus> list
nexus> exit
```

## Scripting and Automation

```bash
#!/bin/bash
# automation.sh

# Run multiple workflows in sequence
nexus run extract-data --source database
nexus run transform-data --format json
nexus run load-data --destination warehouse

# Check exit codes
if [ $? -eq 0 ]; then
    echo "Pipeline completed successfully"
else
    echo "Pipeline failed"
    exit 1
fi
```

## Output Formatting

```bash
# JSON output
nexus run workflow --output json

# YAML output
nexus run workflow --output yaml

# Table output
nexus run workflow --output table

# Raw output
nexus run workflow --output raw
```

## Error Handling

```bash
# Verbose error messages
nexus run workflow --verbose

# Debug mode
nexus run workflow --debug

# Capture errors
nexus run workflow 2> errors.log

# Continue on error
nexus run workflow --continue-on-error
```

## Session Management

```bash
# Create session
nexus session create --name my-session

# List sessions
nexus session list

# Use session
nexus run workflow --session my-session

# Continue session
nexus continue my-session --step 2

# End session
nexus session end my-session
```

## Configuration Files

```bash
# Use config file
nexus run workflow --config workflow.yaml

# Example workflow.yaml
# workflow: data-processor
# parameters:
#   input: data.csv
#   limit: 100
#   output_format: json
```

## Logging

```bash
# Enable logging
nexus run workflow --log-level INFO

# Log to file
nexus run workflow --log-file workflow.log

# Structured logging
nexus run workflow --log-format json
```

## Best Practices

1. **Use JSON for Complex Parameters**
2. **Capture Exit Codes** for automation
3. **Use Config Files** for repeated executions
4. **Enable Logging** for production scripts
5. **Use Sessions** for multi-step processes
6. **Test Scripts** in development environment

## Key Takeaways

- Automatic CLI commands for all workflows
- Multiple parameter formats supported
- Interactive and scripting modes
- Session management built-in
- Configurable output formats

## Related Skills

- [nexus-multi-channel](#) - CLI, API, MCP overview
- [nexus-sessions](#) - Session management
- [nexus-troubleshooting](#) - Fix CLI issues
