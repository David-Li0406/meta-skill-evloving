---
name: slack-bot-builder
description: Use this skill when you want to build Slack apps using the Bolt framework across Python, JavaScript, and Java, focusing on best practices for production-ready integrations.
---

# Skill body

## Overview

The Bolt framework is Slack's recommended approach for building apps. It simplifies authentication, event routing, request verification, and HTTP request processing, allowing you to focus on app logic.

### Key Benefits
- Event handling in a few lines of code
- Built-in security checks and payload validation
- Organized and consistent patterns
- Suitable for both experiments and production

### When to Use
- Starting any new Slack app
- Migrating from legacy Slack APIs
- Building production Slack integrations

## Supported Languages
- Python
- JavaScript (Node.js)
- Java

## Example: Python Bolt App

```python
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os

# Initialize with tokens from environment
app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"]
)

# Handle messages containing "hello"
@app.message("hello")
def handle_hello(message, say):
    """Respond to messages containing 'hello'."""
    user = message["user"]
    say(f"Hey there <@{user}>!")

# Handle slash command
@app.command("/ticket")
def handle_ticket_command(ack, body, client):
    """Handle /ticket slash command."""
    # Acknowledge immediately (within 3 seconds)
    ack()

    # Open a modal for ticket creation
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "ticket_modal",
            "title": {"type": "plain_text", "text": "Create Ticket"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "title_block",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "title_input"
                    },
                    "label": {"type": "plain_text", "text": "Title"}
                },
                {
                    "type": "input",
                    "block_id": "description_block",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "description_input"
                    },
                    "label": {"type": "plain_text", "text": "Description"}
                }
            ]
        }
    )
```

## Additional Resources
- Refer to the [Slack API documentation](https://api.slack.com/) for more details on building Slack apps.
- Consult the [Bolt documentation](https://slack.dev/bolt) for specific patterns and best practices.