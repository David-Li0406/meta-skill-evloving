# Jules API Examples

## Quick Start

### 1. Setup Authentication

```bash
# Get your API key from https://jules.google.com/settings#api
# Then export it as an environment variable
export JULES_API_KEY="your-api-key-here"

# Verify it's set
echo $JULES_API_KEY
```

### 2. Create Your First Session

**Using curl**:
```bash
curl -X POST https://jules.googleapis.com/v1alpha/sessions \
  -H "X-Goog-Api-Key: $JULES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Add logging to all API endpoints",
    "sourceContext": {
      "githubRepository": {
        "owner": "myusername",
        "name": "myrepo",
        "branch": "main"
      }
    }
  }'
```

**Using the Python client**:
```bash
python .claude/skills/jules-api/jules_client.py create \
  "Add logging to all API endpoints" \
  myusername \
  myrepo \
  main
```

**Using Python code**:
```python
from repo_client import JulesClient

client = JulesClient()
session = client.create_session(
    prompt="Add logging to all API endpoints",
    owner="myusername",
    repo="myrepo",
    branch="main"
)
print(f"Session ID: {session['id']}")
print(f"Status: {session['state']}")
```

### 3. Check Session Status

```bash
# Using curl
SESSION_ID="your-session-id"
curl https://jules.googleapis.com/v1alpha/sessions/$SESSION_ID \
  -H "X-Goog-Api-Key: $JULES_API_KEY"

# Using Python client
python .claude/skills/jules-api/jules_client.py get $SESSION_ID
```

## Common Use Cases

### Use Case 1: Simple Automated Task

Create a session and let Jules complete it automatically:

```python
from repo_client import JulesClient
import time

client = JulesClient()

# Create session
session = client.create_session(
    prompt="Fix all TypeScript type errors in the src/ directory",
    owner="myorg",
    repo="myproject",
    branch="develop"
)

session_id = session['id']
print(f"Created session: {session_id}")

# Poll until complete
while True:
    session = client.get_session(session_id)
    state = session['state']
    print(f"Current state: {state}")

    if state == 'COMPLETED':
        print("Task completed successfully!")
        if 'outputs' in session:
            for output in session['outputs']:
                print(f"Pull Request: {output.get('url')}")
        break
    elif state == 'FAILED':
        print("Task failed!")
        break

    time.sleep(10)  # Wait 10 seconds before checking again
```

### Use Case 2: Task with Manual Plan Approval

Review and approve Jules' plan before execution:

```python
from repo_client import JulesClient
import time

client = JulesClient()

# Create session with plan approval required
session = client.create_session(
    prompt="Refactor the authentication module to use JWT tokens",
    owner="myorg",
    repo="myproject",
    require_plan_approval=True
)

session_id = session['id']

# Wait for plan
while True:
    session = client.get_session(session_id)
    state = session['state']

    if state == 'AWAITING_PLAN_APPROVAL':
        print("Plan ready for approval!")

        # Get activities to see the plan
        activities = client.get_activities(session_id)
        print("\nProposed plan:")
        print(activities)

        # Approve the plan
        approval = input("\nApprove this plan? (yes/no): ")
        if approval.lower() == 'yes':
            client.approve_plan(session_id)
            print("Plan approved! Execution starting...")
        break

    time.sleep(5)

# Continue monitoring...
while True:
    session = client.get_session(session_id)
    state = session['state']

    if state in ['COMPLETED', 'FAILED']:
        print(f"Final state: {state}")
        break

    time.sleep(10)
```

### Use Case 3: Interactive Session with Feedback

Provide feedback during execution:

```python
from repo_client import JulesClient
import time

client = JulesClient()

session = client.create_session(
    prompt="Add comprehensive unit tests for the payment processing module",
    owner="myorg",
    repo="myproject"
)

session_id = session['id']

# Monitor and interact
while True:
    session = client.get_session(session_id)
    state = session['state']
    print(f"State: {state}")

    if state == 'AWAITING_USER_FEEDBACK':
        print("\nJules is waiting for feedback!")

        # Get recent activities
        activities = client.get_activities(session_id)
        print("Recent activity:")
        print(activities)

        # Send feedback
        feedback = input("\nYour feedback: ")
        client.send_message(session_id, feedback)
        print("Feedback sent!")

    elif state == 'COMPLETED':
        print("Task completed!")
        break
    elif state == 'FAILED':
        print("Task failed!")
        break

    time.sleep(10)
```

### Use Case 4: List All Sessions

View all your active and completed sessions:

```python
from repo_client import JulesClient

client = JulesClient()
sessions = client.list_sessions()

print("Your Jules sessions:")
print("-" * 80)

for session in sessions.get('sessions', []):
    print(f"ID: {session['id']}")
    print(f"Title: {session.get('title', 'Untitled')}")
    print(f"State: {session['state']}")
    print(f"Created: {session['createTime']}")
    print("-" * 80)
```

## Bash Script Examples

### Monitor Session Script

Save as `monitor_repo.sh`:

```bash
#!/bin/bash

SESSION_ID=$1

if [ -z "$SESSION_ID" ]; then
    echo "Usage: ./monitor_repo.sh <session_id>"
    exit 1
fi

while true; do
    echo "Checking session status..."

    RESPONSE=$(curl -s https://jules.googleapis.com/v1alpha/sessions/$SESSION_ID \
        -H "X-Goog-Api-Key: $JULES_API_KEY")

    STATE=$(echo $RESPONSE | jq -r '.state')

    echo "Current state: $STATE"

    if [ "$STATE" = "COMPLETED" ] || [ "$STATE" = "FAILED" ]; then
        echo "Session finished!"
        echo $RESPONSE | jq .
        break
    fi

    sleep 10
done
```

### Bulk Session Creation

Create multiple related sessions:

```bash
#!/bin/bash

OWNER="myorg"
REPO="myproject"

declare -a TASKS=(
    "Add error handling to authentication module"
    "Update dependencies to latest versions"
    "Fix linting errors in src/ directory"
    "Add JSDoc comments to public API functions"
)

for TASK in "${TASKS[@]}"; do
    echo "Creating session for: $TASK"

    curl -X POST https://jules.googleapis.com/v1alpha/sessions \
        -H "X-Goog-Api-Key: $JULES_API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
            \"prompt\": \"$TASK\",
            \"sourceContext\": {
                \"githubRepository\": {
                    \"owner\": \"$OWNER\",
                    \"name\": \"$REPO\",
                    \"branch\": \"main\"
                }
            }
        }" | jq .

    echo "---"
done
```

## Error Handling Examples

### Robust Error Handling

```python
from repo_client import JulesClient
import requests

def create_session_with_retry(client, prompt, owner, repo, max_retries=3):
    """Create a session with automatic retry logic."""
    for attempt in range(max_retries):
        try:
            session = client.create_session(prompt, owner, repo)
            return session
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                print("Authentication failed. Re-authenticating...")
                client.access_token = None  # Force token refresh
            elif e.response.status_code == 429:
                print(f"Rate limited. Waiting before retry {attempt + 1}/{max_retries}...")
                time.sleep(60)
            else:
                print(f"HTTP error {e.response.status_code}: {e.response.text}")
                if attempt == max_retries - 1:
                    raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            if attempt == max_retries - 1:
                raise

    return None

# Usage
client = JulesClient()
session = create_session_with_retry(
    client,
    prompt="Update README with API documentation",
    owner="myorg",
    repo="myproject"
)
```

## Integration Examples

### CI/CD Integration

Use Jules in your CI/CD pipeline:

```yaml
# .github/workflows/jules-code-review.yml
name: Jules Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  jules-review:
    runs-on: ubuntu-latest
    steps:
      - name: Setup gcloud
        uses: google-github-actions/setup-gcloud@v1
        with:
          service_account_key: ${{ secrets.GCP_SA_KEY }}

      - name: Create Jules Review Session
        run: |
          SESSION_ID=$(curl -X POST https://jules.googleapis.com/v1alpha/sessions \
            -H "X-Goog-Api-Key: $JULES_API_KEY" \
            -H "Content-Type: application/json" \
            -d "{
              \"prompt\": \"Review PR #${{ github.event.pull_request.number }} and suggest improvements\",
              \"sourceContext\": {
                \"githubRepository\": {
                  \"owner\": \"${{ github.repository_owner }}\",
                  \"name\": \"${{ github.event.repository.name }}\",
                  \"branch\": \"${{ github.head_ref }}\"
                }
              }
            }" | jq -r '.id')

          echo "Created Jules session: $SESSION_ID"
```

These examples should help you get started with the Jules API!
