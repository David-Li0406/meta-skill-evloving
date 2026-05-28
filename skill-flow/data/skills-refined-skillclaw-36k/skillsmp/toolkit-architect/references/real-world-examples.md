# Real-World Examples

## Table of Contents

- [Example 1: multi-agent-swarm Plugin](#example-1-multi-agent-swarm-plugin)
- [Requirements](#requirements)
- [Success Criteria](#success-criteria)
- [Example 2: ralph-wiggum Plugin](#example-2-ralph-wiggum-plugin)
- [Current Status](#current-status)
- [Example 3: Security Scanner Plugin](#example-3-security-scanner-plugin)
- [Example 4: Deployment Orchestrator](#example-4-deployment-orchestrator)
- [Example 5: Database Migration Manager](#example-5-database-migration-manager)
- [Common Patterns Summary](#common-patterns-summary)
- [Best Practices from Examples](#best-practices-from-examples)
- [Testing Configurations](#testing-configurations)

## Example 1: multi-agent-swarm Plugin

### Overview

The multi-agent-swarm plugin uses `.local.md` files to coordinate multiple agents across different sessions, manage task assignments, and track progress.

### Configuration File

**.claude/multi-agent-swarm.local.md:**

```markdown
---
agent_name: auth-implementation
task_number: 3.5
pr_number: 1234
coordinator_session: team-leader
enabled: true
dependencies: ["Task 3.4"]
additional_instructions: Use JWT tokens, not sessions
---

# Task: Implement Authentication

Build JWT-based authentication for the REST API.
Coordinate with auth-agent on shared types.

## Requirements
- JWT token-based authentication
- Refresh token support
- Proper error handling
- API documentation

## Success Criteria
- [ ] Authentication endpoints created
- [ ] Tests passing
- [ ] PR created and CI green
```

### Hook Implementation

**Hook: agent-stop-notification.sh**

```bash
#!/bin/bash
set -euo pipefail

# Configuration
STATE_FILE=".claude/multi-agent-swarm.local.md"
LOG_FILE=".claude/agent-activity.log"

# Quick exit if not configured
if [[ ! -f "$STATE_FILE" ]]; then
    exit 0
fi

# Parse configuration using Python
python3 <<'PYTHON_SCRIPT'
import yaml
import sys
import json
from datetime import datetime

try:
    with open(sys.argv[1], 'r') as f:
        content = f.read()

    if not content.startswith('---'):
        sys.exit(0)

    _, frontmatter, body = content.split('---', 2)
    config = yaml.safe_load(frontmatter) or {}

    # Check if enabled
    if not config.get('enabled', False):
        sys.exit(0)

    # Extract fields
    agent_name = config.get('agent_name', 'unknown')
    task_number = config.get('task_number', 'unknown')
    pr_number = config.get('pr_number', 'unknown')
    coordinator = config.get('coordinator_session', 'team-leader')
    dependencies = config.get('dependencies', [])

    # Log activity
    timestamp = datetime.now().isoformat()
    log_entry = {
        'timestamp': timestamp,
        'agent': agent_name,
        'task': task_number,
        'event': 'completed'
    }

    with open(sys.argv[2], 'a') as log:
        log.write(json.dumps(log_entry) + '\n')

    # Send notification to coordinator
    message = f"🤖 Agent {agent_name} completed Task {task_number}"
    if pr_number != 'unknown':
        message += f" (PR #{pr_number})"

    print(f"NOTIFY:{coordinator}:{message}")

except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
PYTHON_SCRIPT

STATE_FILE="$STATE_FILE"
LOG_FILE="$LOG_FILE"

# Check notification from Python
NOTIFICATION=$(python3 -c "
import subprocess
result = subprocess.run(['python3', '-c', '''
import yaml
import sys
try:
    with open(\"$STATE_FILE\", \"r\") as f:
        content = f.read()
    if content.startswith(\"---\"):
        _, frontmatter, _ = content.split(\"---\", 2)
        config = yaml.safe_load(frontmatter) or {}
        if config.get('enabled', False):
            print(f\"NOTIFY:{config.get('coordinator_session', 'team-leader')}:Agent {config.get('agent_name', 'unknown')} completed\")
'''], capture_output=True, text=True)
print(result.stdout.strip())
")

# Send notification if present
if [[ "$NOTIFICATION" == NOTIFY:* ]]; then
    # Extract coordinator and message
    COORDINATOR=$(echo "$NOTIFICATION" | cut -d':' -f2)
    MESSAGE=$(echo "$NOTIFICATION" | cut -d':' -f3-)
    
    # Send to tmux session (if available)
    if command -v tmux &> /dev/null; then
        tmux send-keys -t "$COORDINATOR" "$MESSAGE" Enter 2>/dev/null || true
    fi
    
    echo "✅ Notification sent to $COORDINATOR: $MESSAGE"
fi
```

### Key Patterns Used

1. **Quick Exit**: Check if file exists before parsing
2. **Python Parsing**: Robust YAML parsing with error handling
3. **Event Logging**: Structured logging for debugging
4. **Cross-Session Communication**: Using tmux sessions
5. **Conditional Execution**: Only run if enabled=true

### Configuration Variations

**Task Assignment:**
```markdown
---
agent_name: db-migration
task_number: 2.1
enabled: true
dependencies: ["Task 2.0"]
---

# Database Migration

Migrate user table to new schema.
```

**Completion Tracking:**
```markdown
---
agent_name: test-coverage
task_number: 4.2
pr_number: 1289
enabled: true
completion_promise: "All tests passing and coverage > 80%"
---

# Increase Test Coverage

Add unit tests for uncovered modules.
```

## Example 2: ralph-wiggum Plugin

### Overview

The ralph-wiggum plugin implements iterative refinement using `.local.md` files to track iterations, completion criteria, and prompts.

### Configuration File

**.claude/ralph-loop.local.md:**

```markdown
---
iteration: 1
max_iterations: 10
completion_promise: "All tests passing and build successful"
enabled: true
---

Fix all the linting errors in the project.
Make sure tests pass after each fix.

## Current Status
- Iteration: 1
- Focus: Import sorting
```

### Hook Implementation

**Hook: stop-hook.sh**

```bash
#!/bin/bash
set -euo pipefail

STATE_FILE=".claude/ralph-loop.local.md"

# Quick exit if not active
if [[ ! -f "$STATE_FILE" ]]; then
    exit 0
fi

# Parse and increment iteration
python3 <<'PYTHON_SCRIPT'
import yaml
import sys
import os

STATE_FILE = sys.argv[1]

try:
    with open(STATE_FILE, 'r') as f:
        content = f.read()

    if not content.startswith('---'):
        print("Invalid format: missing frontmatter")
        sys.exit(1)

    _, frontmatter, body = content.split('---', 2)
    config = yaml.safe_load(frontmatter) or {}

    # Check if enabled
    if not config.get('enabled', False):
        sys.exit(0)

    # Get current iteration
    current_iter = config.get('iteration', 0)
    max_iter = config.get('max_iterations', 10)
    completion_promise = config.get('completion_promise', '')

    # Increment iteration
    new_iter = current_iter + 1

    # Check completion criteria
    if new_iter > max_iter:
        print(f"❌ Max iterations ({max_iter}) reached")
        sys.exit(0)

    # Update configuration
    config['iteration'] = new_iter

    # Write back to file
    new_frontmatter = yaml.dump(config, default_flow_style=False)

    with open(STATE_FILE, 'w') as f:
        f.write('---\n')
        f.write(new_frontmatter)
        f.write('---\n')
        f.write(body)

    # Output for shell
    print(f"ITERATION:{new_iter}")
    print(f"PROMISE:{completion_promise}")
    print(f"BODY:{body}")

except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
PYTHON_SCRIPT

STATE_FILE="$STATE_FILE"

# Read output from Python
PYTHON_OUTPUT=$(python3 -c "
import subprocess
result = subprocess.run(['python3', '-c', '''
import yaml
import sys

STATE_FILE = \"$STATE_FILE\"

try:
    with open(STATE_FILE, \"r\") as f:
        content = f.read()

    if content.startswith(\"---\"):
        _, frontmatter, body = content.split(\"---\", 2)
        config = yaml.safe_load(frontmatter) or {}

        if config.get('enabled', False):
            current_iter = config.get('iteration', 0)
            max_iter = config.get('max_iterations', 10)
            completion_promise = config.get('completion_promise', '')

            if current_iter < max_iter:
                print(f\"CONTINUE:{current_iter + 1}\")
                print(f\"PROMISE:{completion_promise}\")
                print(f\"BODY:{body}\")
            else:
                print(\"COMPLETE:max_iterations_reached\")
'''], capture_output=True, text=True)
echo "$PYTHON_OUTPUT"
")

# Check if should continue
if [[ "$PYTHON_OUTPUT" == CONTINUE:* ]]; then
    ITERATION=$(echo "$PYTHON_OUTPUT" | grep "^CONTINUE:" | cut -d':' -f2)
    PROMISE=$(echo "$PYTHON_OUTPUT" | grep "^PROMISE:" | cut -d':' -f2-)
    BODY=$(echo "$PYTHON_OUTPUT" | grep "^BODY:" | cut -d':' -f2-)
    
    echo "🔄 Iteration $ITERATION"
    echo "📋 Task: $BODY"
    echo "✅ Success: $PROMISE"
    
    # Send task back to Claude
    echo "$BODY"
    
elif [[ "$PYTHON_OUTPUT" == COMPLETE:* ]]; then
    echo "✅ Loop complete"
    exit 0
fi
```

### Key Patterns Used

1. **State Persistence**: Iteration count stored in file
2. **Loop Control**: max_iterations prevents infinite loops
3. **Dynamic Prompts**: Body content becomes next prompt
4. **Completion Tracking**: completion_promise defines success criteria

### Configuration Variations

**Simple Loop:**
```markdown
---
iteration: 1
max_iterations: 5
enabled: true
---

Review and improve code quality.
```

**Conditional Loop:**
```markdown
---
iteration: 1
max_iterations: 20
completion_promise: "Zero linting errors and all tests green"
enabled: true
---

Iteratively fix linting issues.
Stop when code is clean.
```

## Example 3: Security Scanner Plugin

### Configuration File

**.claude/security-scan.local.md:**

```markdown
---
enabled: true
scan_level: strict
excluded_paths: ["node_modules", ".git", "dist"]
max_file_size: 1000000
notification_level: warning
rules:
  - "no-secrets"
  - "validate-inputs"
  - "secure-auth"
environment: production
cooldown_seconds: 300
---

# Security Scanning Configuration

Strict mode enabled for production.
All file writes validated.
```

### Hook Implementation

**Hook: pre-tool-use-scan.sh**

```bash
#!/bin/bash
set -euo pipefail

STATE_FILE=".claude/security-scan.local.md"

# Quick exit if disabled
if [[ ! -f "$STATE_FILE" ]]; then
    exit 0
fi

# Parse configuration
ENABLED=$(yq eval '.enabled' "$STATE_FILE" 2>/dev/null || echo "false")

if [[ "$ENABLED" != "true" ]]; then
    exit 0
fi

# Get scan parameters
SCAN_LEVEL=$(yq eval '.scan_level // "standard"' "$STATE_FILE")
MAX_SIZE=$(yq eval '.max_file_size // 1000000' "$STATE_FILE")
NOTIFICATION_LEVEL=$(yq eval '.notification_level // "info"' "$STATE_FILE")

# Read excluded paths
IFS=$'\n' read -rd '' -a EXCLUDED_PATHS <<< "$(yq eval -r '.excluded_paths[]' "$STATE_FILE" 2>/dev/null || echo "")"

# Check cooldown
COOLDOWN_FILE=".claude/.scan-cooldown"
if [[ -f "$COOLDOWN_FILE" ]]; then
    LAST_SCAN=$(cat "$COOLDOWN_FILE")
    NOW=$(date +%s)
    COOLDOWN_SECONDS=$(yq eval '.cooldown_seconds // 300' "$STATE_FILE")
    
    ELAPSED=$((NOW - LAST_SCAN))
    if [[ $ELAPSED -lt $COOLDOWN_SECONDS ]]; then
        REMAINING=$((COOLDOWN_SECONDS - ELAPSED))
        echo "⏱️ Scanning cooldown: ${REMAINING}s remaining"
        exit 0
    fi
fi

# Perform scan
echo "🔍 Running security scan (level: $SCAN_LEVEL)"

# Update cooldown
date +%s > "$COOLDOWN_FILE"

# Run scan logic here
# (Scan files, check for security issues, etc.)

echo "✅ Security scan complete"
```

### Key Patterns Used

1. **Conditional Activation**: Enabled/disabled via config
2. **Rate Limiting**: Cooldown prevents excessive scanning
3. **Complex Configuration**: Nested objects and arrays
4. **Performance Optimization**: File size limits, path exclusions

## Example 4: Deployment Orchestrator

### Configuration File

**.claude/deploy-orchestrator.local.md:**

```markdown
---
version: "2.0.0"
enabled: true
environment: staging
deployment_strategy: blue-green
notification_channels:
  - slack
  - email
rollback_on_failure: true
health_check_path: /health
timeout_seconds: 300
secrets:
  encrypted: true
approval_required: false
---

# Deployment Configuration

Staging environment deployment.
Blue-green strategy enabled.
```

### Command Implementation

**Command: deploy-app.md**

```markdown
---
name: deploy-app
description: "Deploy application using configured strategy"
allowed-tools: ["Read", "Bash", "Write"]
---

# Deploy Application

Deploy the application using the configuration in `.claude/deploy-orchestrator.local.md`.

Steps:
1. Read deployment configuration
2. Validate environment and secrets
3. Execute deployment strategy (blue-green/rolling/canary)
4. Run health checks
5. Send notifications
6. Confirm deployment success

Configuration is read from `.claude/deploy-orchestrator.local.md`
```

### Command Script

```bash
#!/bin/bash
set -euo pipefail

STATE_FILE=".claude/deploy-orchestrator.local.md"

# Check if configured
if [[ ! -f "$STATE_FILE" ]]; then
    echo "❌ No deployment configuration found"
    echo "Create .claude/deploy-orchestrator.local.md"
    exit 1
fi

# Parse configuration
ENVIRONMENT=$(yq eval '.environment' "$STATE_FILE")
STRATEGY=$(yq eval '.deployment_strategy' "$STATE_FILE")
TIMEOUT=$(yq eval '.timeout_seconds // 300' "$STATE_FILE")
ROLLBACK=$(yq eval '.rollback_on_failure' "$STATE_FILE")

# Read notification channels
IFS=$'\n' read -rd '' -a NOTIFICATIONS <<< "$(yq eval -r '.notification_channels[]' "$STATE_FILE")"

echo "🚀 Starting deployment"
echo "Environment: $ENVIRONMENT"
echo "Strategy: $STRATEGY"
echo "Timeout: ${TIMEOUT}s"
echo "Rollback on failure: $ROLLBACK"

# Validate configuration
if [[ "$ENVIRONMENT" == "production" ]] && [[ "$(yq eval '.approval_required // false' "$STATE_FILE")" == "true" ]]; then
    echo "⚠️ Production deployment requires approval"
    # Check for approval...
fi

# Execute deployment
case "$STRATEGY" in
    blue-green)
        echo "Executing blue-green deployment..."
        # Blue-green logic
        ;;
    rolling)
        echo "Executing rolling deployment..."
        # Rolling logic
        ;;
    canary)
        echo "Executing canary deployment..."
        # Canary logic
        ;;
    *)
        echo "❌ Unknown deployment strategy: $STRATEGY"
        exit 1
        ;;
esac

# Health check
HEALTH_PATH=$(yq eval '.health_check_path // "/health"' "$STATE_FILE")
echo "🔍 Running health check: $HEALTH_PATH"

# Send notifications
for channel in "${NOTIFICATIONS[@]}"; do
    echo "📢 Notifying via $channel"
    # Send notification
done

echo "✅ Deployment complete"
```

### Key Patterns Used

1. **Complex Configuration**: Multiple nested settings
2. **Strategy Pattern**: Different deployment methods
3. **Validation**: Pre-deployment checks
4. **Notifications**: Multi-channel alerting
5. **Approval Workflows**: Production safeguards

## Example 5: Database Migration Manager

### Configuration File

**.claude/db-migration.local.md:**

```markdown
---
version: "2.0.0"
enabled: true
database_url: "${DATABASE_URL}"
migration_dir: "./migrations"
backup_before_migration: true
backup_retention_days: 30
transaction_mode: true
max_execution_time: 600
validation_query: "SELECT 1"
rollback_sql_directory: "./rollback"
notification_on_success: true
notification_on_failure: true
---

# Database Migration Configuration

Automated migration management with rollback support.
```

### Migration Hook

**Hook: pre-migration.sh**

```bash
#!/bin/bash
set -euo pipefail

STATE_FILE=".claude/db-migration.local.md"

# Check if enabled
if [[ ! -f "$STATE_FILE" ]] || [[ "$(yq eval '.enabled' "$STATE_FILE")" != "true" ]]; then
    exit 0
fi

# Parse configuration
DB_URL=$(yq eval '.database_url' "$STATE_FILE")
MIGRATION_DIR=$(yq eval '.migration_dir // "./migrations"' "$STATE_FILE")
BACKUP_BEFORE=$(yq eval '.backup_before_migration' "$STATE_FILE")
TRANSACTION_MODE=$(yq eval '.transaction_mode' "$STATE_FILE")
MAX_TIME=$(yq eval '.max_execution_time // 600' "$STATE_FILE")

if [[ -z "$DB_URL" ]]; then
    echo "❌ Database URL not configured"
    exit 1
fi

echo "🔄 Preparing for migration"
echo "Database: ${DB_URL:0:20}..."
echo "Migration directory: $MIGRATION_DIR"
echo "Backup enabled: $BACKUP_BEFORE"
echo "Transaction mode: $TRANSACTION_MODE"

# Create backup if enabled
if [[ "$BACKUP_BEFORE" == "true" ]]; then
    echo "💾 Creating backup..."
    BACKUP_FILE=".claude/db-backup-$(date +%Y%m%d-%H%M%S).sql"
    
    if command -v pg_dump &> /dev/null; then
        pg_dump "$DB_URL" > "$BACKUP_FILE"
        echo "✅ Backup created: $BACKUP_FILE"
    elif command -v mysqldump &> /dev/null; then
        mysqldump "$DB_URL" > "$BACKUP_FILE"
        echo "✅ Backup created: $BACKUP_FILE"
    else
        echo "⚠️ No database dump tool found"
    fi
fi

# Validate database connection
VALIDATION_QUERY=$(yq eval '.validation_query // "SELECT 1"' "$STATE_FILE")

if command -v psql &> /dev/null; then
    psql "$DB_URL" -c "$VALIDATION_QUERY" > /dev/null
elif command -v mysql &> /dev/null; then
    mysql "$DB_URL" -e "$VALIDATION_QUERY" > /dev/null
fi

echo "✅ Database connection validated"
echo "🚀 Ready for migration"
```

### Key Patterns Used

1. **Environment Variables**: Using ${DATABASE_URL}
2. **Tool Detection**: pg_dump vs mysqldump
3. **Validation**: Database connectivity check
4. **Backup Strategy**: Automatic backup creation
5. **Timeout Handling**: Execution time limits

## Common Patterns Summary

### 1. Quick Exit Pattern
```bash
if [[ ! -f "$STATE_FILE" ]]; then
    exit 0  # Not configured, skip
fi
```

### 2. Enabled/Disabled Toggle
```bash
ENABLED=$(yq eval '.enabled' "$STATE_FILE")
if [[ "$ENABLED" != "true" ]]; then
    exit 0  # Disabled
fi
```

### 3. Python YAML Parsing
```python
with open(STATE_FILE, 'r') as f:
    content = f.read()

_, frontmatter, body = content.split('---', 2)
config = yaml.safe_load(frontmatter)
```

### 4. Nested Value Access
```bash
# yq
VALUE=$(yq eval '.settings.database.host' "$STATE_FILE")

# Python
HOST=config.get('settings', {}).get('database', {}).get('host', 'localhost')
```

### 5. Array Parsing
```bash
IFS=$'\n' read -rd '' -a ARRAY <<< "$(yq eval -r '.items[]' "$STATE_FILE")"
for item in "${ARRAY[@]}"; do
    echo "$item"
done
```

### 6. Error Handling
```bash
python3 <<'PYTHON_SCRIPT'
try:
    # Parse YAML
    config = yaml.safe_load(frontmatter)
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
PYTHON_SCRIPT
```

### 7. Default Values
```bash
# yq with defaults
VALUE=$(yq eval '.field // "default_value"' "$STATE_FILE")

# Python
VALUE=config.get('field', 'default_value')
```

### 8. Type Validation
```python
if not isinstance(config.get('enabled'), bool):
    print("Field 'enabled' must be boolean", file=sys.stderr)
    sys.exit(1)
```

### 9. State Updates
```python
config['iteration'] = config.get('iteration', 0) + 1
with open(STATE_FILE, 'w') as f:
    f.write('---\n')
    f.write(yaml.dump(config))
    f.write('---\n')
    f.write(body)
```

### 10. Cross-Component Communication
```bash
# Write to log file
echo "$LOG_ENTRY" >> ".claude/activity.log"

# tmux notification
tmux send-keys -t "$SESSION" "$MESSAGE" Enter
```

## Best Practices from Examples

1. **Always check if file exists** before parsing
2. **Provide defaults** for all optional fields
3. **Use Python for complex parsing** and validation
4. **Handle errors gracefully** with clear messages
5. **Log important events** for debugging
6. **Validate inputs** before using them
7. **Support enable/disable** via configuration
8. **Use appropriate tools** (yq, Python, bash) for the task
9. **Test edge cases** (missing fields, invalid values)
10. **Document configuration** in README files

## Testing Configurations

### Test Script Template

```bash
#!/bin/bash
test_config() {
    local test_file="$1"
    local expected_enabled="$2"
    
    echo "Testing: $test_file"
    
    if [[ ! -f "$test_file" ]]; then
        echo "  ❌ File not found"
        return 1
    fi
    
    local enabled
    enabled=$(yq eval '.enabled' "$test_file")
    
    if [[ "$enabled" == "$expected_enabled" ]]; then
        echo "  ✅ Enabled: $enabled"
    else
        echo "  ❌ Expected: $expected_enabled, Got: $enabled"
        return 1
    fi
    
    # Add more tests...
}

# Run tests
test_config ".claude/test1.local.md" "true"
test_config ".claude/test2.local.md" "false"
```

These examples demonstrate real-world usage of `.local.md` configuration files across different plugin types and use cases.
