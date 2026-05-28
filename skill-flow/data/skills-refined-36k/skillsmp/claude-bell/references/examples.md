# Workflow Examples

Common patterns for using claude-bell in Claude Code workflows.

## Simple Alerts

### Task Completion

```bash
# Basic completion notification
cb -t "Build Complete" -m "Project compiled successfully"

# With sound
cb -t "Tests Passed" -m "All 142 tests passed" --sound Glass

# With subtitle for context
cb -t "Deploy Done" -s "production" -m "v1.2.3 deployed to prod"
```

### Error Notifications

```bash
# Build failure
cb -t "Build Failed" -m "TypeScript compilation error in src/app.ts" --sound Basso

# Test failure with details
cb -t "Tests Failed" -m "3 tests failed in auth.spec.ts" --sound Sosumi
```

## Interactive Confirmations

### Yes/No Confirmation

```bash
# Destructive operation confirmation
RESPONSE=$(cb -t "Confirm Delete" -m "Delete all .log files?" -a "Delete,Cancel" --default "Cancel")
if [ "$RESPONSE" = "Delete" ]; then
    rm -f *.log
fi

# Deploy confirmation
RESPONSE=$(cb -t "Deploy to Production?" -m "This will deploy v1.2.3" -a "Deploy,Cancel" --default "Cancel")
```

### Multiple Choice

```bash
# Branch selection
BRANCH=$(cb -t "Select Branch" -m "Which branch to deploy?" -a "main,staging,develop,Cancel" --default "Cancel")
case "$BRANCH" in
    main) deploy_prod ;;
    staging) deploy_staging ;;
    develop) deploy_dev ;;
    *) echo "Cancelled" ;;
esac

# Error recovery options
ACTION=$(cb -t "Test Failure" -m "What would you like to do?" -a "Retry,Skip,Abort" --default "Abort")
```

### With Timeout

```bash
# Auto-proceed after timeout
RESPONSE=$(cb -t "Continue?" -m "Proceeding in 30 seconds..." -a "Continue,Cancel" --default "Continue" --timeout 30s)

# Non-blocking confirmation
RESPONSE=$(cb -t "Optimization Complete" -m "Run additional analysis?" -a "Yes,No" --default "No" --timeout 5m)
```

## Text Input

### Commit Messages

```bash
# Request commit message
MESSAGE=$(cb -t "Commit Message" -r "Enter commit message..." --timeout 5m --default "")
if [ -n "$MESSAGE" ]; then
    git commit -m "$MESSAGE"
fi
```

### Release Notes

```bash
# Collect release notes
NOTES=$(cb -t "Release Notes" -s "v1.2.3" -r "Enter release notes..." --timeout 10m)
echo "$NOTES" >> CHANGELOG.md
```

### User Input with Validation

```bash
# Loop until valid input or cancel
while true; do
    VERSION=$(cb -t "Version Number" -r "Enter version (e.g., 1.2.3)..." --default "")
    if [[ -z "$VERSION" ]]; then
        echo "Cancelled"
        break
    elif [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo "Valid version: $VERSION"
        break
    else
        cb -t "Invalid Format" -m "Version must be in X.Y.Z format"
    fi
done
```

## Using Templates

### Define a Template

First, create a template using `cb template create` or add to templates.json:

```json
{
  "name": "build-done",
  "title": "Build Complete",
  "subtitle": "{{ project }}",
  "message": "Built in {{ duration | default('unknown time') }}",
  "sound": "Glass",
  "defaults": {
    "project": "unnamed"
  }
}
```

### Use the Template

```bash
# With all variables
cb --template build-done --var 'project:my-app' --var 'duration:45s'

# With defaults
cb --template build-done --var 'project:my-app'

# Override multiple variables
cb --template build-done --var 'project:backend,duration:2m30s'
```

## Exit Code Handling

### Comprehensive Exit Code Handling

```bash
cb -t "Deploy?" -a "Yes,No" --default "No" --timeout 60s
EXIT_CODE=$?
RESPONSE=$(cb -t "Deploy?" -a "Yes,No" --default "No" --timeout 60s)

case $EXIT_CODE in
    0)  # Success - user responded
        if [ "$RESPONSE" = "Yes" ]; then
            deploy
        fi
        ;;
    1)  # Timeout - use default
        echo "Timed out, using default: No"
        ;;
    2)  # Dismissed - use default
        echo "Dismissed, using default: No"
        ;;
    3)  # User error
        echo "Invalid arguments"
        ;;
    4)  # System error
        echo "Notification system error - run 'cb doctor'"
        ;;
    5)  # App error
        echo "Bug in claude-bell - please report"
        ;;
esac
```

### Simplified Pattern

```bash
# For most cases, just check if response equals expected value
RESPONSE=$(cb -t "Continue?" -a "Yes,No" --default "No")
if [ "$RESPONSE" = "Yes" ]; then
    proceed
else
    cancel
fi
```

## Long-Running Operations

### Progress Updates

```bash
# Start notification
cb -t "Building" -m "Starting build..."

# ... build runs ...

# Completion notification
cb -t "Build Complete" -m "Finished in 2m 34s" --sound Glass
```

### With User Interrupt Option

```bash
# Offer to stop
RESPONSE=$(cb -t "Long Operation Running" -m "Press Stop to cancel" -a "Stop,Continue" --default "Continue" --timeout 30s)
if [ "$RESPONSE" = "Stop" ]; then
    kill $BUILD_PID
fi
```

## JSON Output

### Capture Full Response

```bash
# Get JSON response
RESULT=$(cb -t "Choice" -a "A,B,C" --json stdout)
echo "$RESULT"
# {"action":"clicked","value":"B","exit_code":0}

# Pretty printed
cb -t "Choice" -a "A,B,C" --json stdout --pretty
```

### Parse with jq

```bash
RESULT=$(cb -t "Choice" -a "A,B,C" --json stdout)
ACTION=$(echo "$RESULT" | jq -r '.action')
VALUE=$(echo "$RESULT" | jq -r '.value')
```

## Batch Operations

### Multiple Notifications

```bash
# Send multiple notifications from file
cat <<EOF | cb --batch
{"title": "Step 1", "message": "Downloading dependencies"}
{"title": "Step 2", "message": "Compiling source"}
{"title": "Step 3", "message": "Running tests"}
EOF
```

## Best Practices

### Do

```bash
# Provide defaults for interactive notifications
cb -t "Continue?" -a "Yes,No" --default "No"

# Use timeouts for non-critical prompts
cb -t "Run optional step?" -a "Yes,Skip" --default "Skip" --timeout 60s

# Be specific in messages
cb -t "Deploy to production?" -m "This will deploy commit abc123 to prod-us-east"
```

### Don't

```bash
# DON'T: No default for interactive notification
cb -t "Continue?" -a "Yes,No"  # Bad - what happens on timeout?

# DON'T: Spam notifications
for file in *.ts; do
    cb -t "Processing" -m "$file"  # Bad - too many notifications
done

# DON'T: Vague messages
cb -t "Error" -m "Something went wrong"  # Bad - not helpful
```
