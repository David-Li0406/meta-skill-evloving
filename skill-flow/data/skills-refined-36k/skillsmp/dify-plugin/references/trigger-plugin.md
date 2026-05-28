# Trigger Plugin Development

Trigger plugins receive external webhooks to start Dify workflows.

## File Structure

```
my-trigger/
├── manifest.yaml                    # Plugin manifest
├── main.py                          # Entry point
├── pyproject.toml                   # Dependencies (uv)
├── README.md                        # Documentation
├── _assets/
│   └── icon.svg                     # Plugin icon
├── provider/
│   ├── {provider_name}.yaml         # Provider config (subscription schema)
│   └── {provider_name}.py           # Provider implementation (Start/Destroy/OnEvent)
└── events/
    ├── {event_name}_event.yaml      # Event definition
    └── {event_name}_event.py        # Event implementation
```

## manifest.yaml

```yaml
version: 0.0.1
type: plugin
author: your-name
name: my_trigger
label:
  en_US: My Trigger
  zh_Hans: 我的触发器
description:
  en_US: Webhook trigger for external events
icon: icon.svg

meta:
  version: 0.0.1
  arch: [amd64, arm64]
  runner:
    language: python
    version: "3.12"
    entrypoint: main
  minimum_dify_version: "1.10.0"

plugins:
  triggers:                    # Note: triggers, not tools
    - provider/my_trigger.yaml

resource:
  memory: 1048576
  permission:
    tool:
      enabled: true
    model:
      enabled: true
      llm: true

tags:
  - trigger
```

## provider.yaml

Note: `identity` section should be at the **bottom** of the file.

```yaml
# User fills when creating subscription
subscription_schema:
  - name: webhook_secret
    type: secret-input
    required: false
    label:
      en_US: Webhook Secret
      zh_Hans: Webhook 密钥
    help:
      en_US: Secret for validating webhook signatures

# Parameters for creating subscription
subscription_constructor:
  parameters:
    - name: repository
      type: dynamic-select      # Fetches options via _fetch_parameter_options
      required: true
      label:
        en_US: Repository
      placeholder:
        en_US: "owner/repo"
      description:
        en_US: "GitHub repository in format owner/repo"

    - name: events
      type: checkbox
      required: true
      multiple: true
      default:
        - push
        - issues
      options:
        - value: push
          label:
            en_US: Push
            zh_Hans: 推送
        - value: issues
          label:
            en_US: Issues
            zh_Hans: 议题
        - value: pull_request
          label:
            en_US: Pull Request

  credentials_schema:
    access_token:
      type: secret-input
      required: true
      label:
        en_US: Access Token
      help:
        en_US: Personal access token with webhook permissions
      url: https://github.com/settings/tokens

  # Optional: OAuth support
  oauth_schema:
    client_schema:
      - name: client_id
        type: secret-input
        required: true
        url: https://github.com/settings/applications/new
        label:
          en_US: Client ID
      - name: client_secret
        type: secret-input
        required: true
        label:
          en_US: Client Secret
      - name: scope
        type: text-input
        default: "read:user admin:repo_hook"
        label:
          en_US: OAuth Scope
    credentials_schema:
      - name: access_tokens
        type: secret-input
        label:
          en_US: Access Token

events:
  - events/push/push.yaml
  - events/issues/issues.yaml
  - events/pull_request/pull_request.yaml

# identity section at the bottom
identity:
  author: your-name
  name: my_trigger
  label:
    en_US: My Trigger
    zh_Hans: 我的触发器
  description:
    en_US: Receives webhook events from external service
  icon: icon.svg

extra:
  python:
    source: provider/my_trigger.py
```

## Event Definition (events/issues/issues.yaml)

```yaml
identity:
  name: issues
  author: your-name
  label:
    en_US: Issues Event
    zh_Hans: 议题事件

description:
  en_US: Triggered when issue is created, updated, or closed

# Event filter parameters
parameters:
  - name: actions
    type: select
    multiple: true
    default: [opened, edited, closed]
    options:
      - value: opened
        label:
          en_US: Opened
      - value: edited
        label:
          en_US: Edited
      - value: closed
        label:
          en_US: Closed
    description:
      en_US: Filter by issue action

  - name: labels
    type: string
    required: false
    description:
      en_US: Comma-separated labels to filter

# Output schema for workflow variables
output_schema:
  type: object
  properties:
    action:
      type: string
      description: Event action (opened, edited, closed)
    issue:
      type: object
      properties:
        id:
          type: integer
        number:
          type: integer
        title:
          type: string
        body:
          type: [string, "null"]
        state:
          type: string
        user:
          type: object
          properties:
            id:
              type: integer
            login:
              type: string
      required: [id, number, title, state]
    repository:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        full_name:
          type: string
    sender:
      type: object
      properties:
        id:
          type: integer
        login:
          type: string
  required: [action, issue, repository, sender]

extra:
  python:
    source: events/issues/issues.py
```

## Trigger Implementation

```python
import hmac
import hashlib
from typing import Any, Mapping
from werkzeug import Request, Response
from dify_plugin.interfaces.trigger import Trigger
from dify_plugin.entities.trigger import EventDispatch, Subscription
from dify_plugin.errors.trigger import TriggerDispatchError, TriggerValidationError

class MyTrigger(Trigger):
    def _dispatch_event(
        self, subscription: Subscription, request: Request
    ) -> EventDispatch:
        """Dispatch incoming webhook to appropriate events"""
        # Validate signature (optional)
        webhook_secret = subscription.properties.get("webhook_secret")
        if webhook_secret:
            self._validate_signature(request, webhook_secret)

        # Get event type from header
        event_type = request.headers.get("X-Event-Type")
        if not event_type:
            raise TriggerDispatchError("Missing event type header")

        # Parse payload
        try:
            payload = request.get_json(force=True)
        except Exception as e:
            raise TriggerDispatchError(f"Invalid JSON payload: {e}")

        # Extract user ID for tracking
        user_id = str(payload.get("sender", {}).get("id", "unknown"))

        # Determine which events to trigger
        events = self._resolve_events(event_type, payload)

        # Create response
        response = Response(
            response='{"status": "ok"}',
            status=200,
            mimetype="application/json"
        )

        return EventDispatch(
            user_id=user_id,
            events=events,
            response=response
        )

    def _validate_signature(self, request: Request, secret: str) -> None:
        """Validate webhook signature"""
        signature = request.headers.get("X-Signature-256")
        if not signature:
            raise TriggerValidationError("Missing signature header")

        body = request.get_data()
        expected = "sha256=" + hmac.new(
            secret.encode(), body, hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected):
            raise TriggerValidationError("Invalid signature")

    def _resolve_events(self, event_type: str, payload: dict) -> list[str]:
        """Map webhook event type to internal event names"""
        event_type = event_type.lower()

        # Simple mapping
        if event_type in {"push", "issues", "pull_request"}:
            return [event_type]

        # Events with action suffix
        action = payload.get("action")
        if action:
            return [f"{event_type}_{action}"]

        return [event_type]
```

## SubscriptionConstructor Implementation

```python
from collections.abc import Mapping
from typing import Any
import httpx
from dify_plugin.entities.provider_config import CredentialType
from dify_plugin.entities.trigger import Subscription, UnsubscribeResult
from dify_plugin.errors.trigger import (
    SubscriptionError,
    TriggerProviderCredentialValidationError,
)
from dify_plugin.interfaces.trigger import TriggerSubscriptionConstructor

class MySubscriptionConstructor(TriggerSubscriptionConstructor):
    def _validate_api_key(self, credentials: Mapping[str, Any]) -> None:
        """Validate API credentials"""
        token = credentials.get("access_token")
        if not token:
            raise TriggerProviderCredentialValidationError("Access token required")

        # Test API access
        try:
            response = httpx.get(
                "https://api.example.com/user",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10
            )
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise TriggerProviderCredentialValidationError(f"Invalid token: {e}")

    def _create_subscription(
        self,
        endpoint: str,                    # Dify's webhook URL
        parameters: Mapping[str, Any],    # User's subscription params
        credentials: Mapping[str, Any],
        credential_type: CredentialType,
    ) -> Subscription:
        """Create webhook subscription on external service"""
        token = credentials.get("access_token")
        repository = parameters.get("repository")
        events = parameters.get("events", [])

        # Generate webhook secret
        import secrets
        webhook_secret = secrets.token_hex(32)

        # Create webhook on external service
        try:
            response = httpx.post(
                f"https://api.example.com/repos/{repository}/hooks",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "config": {
                        "url": endpoint,
                        "content_type": "json",
                        "secret": webhook_secret,
                    },
                    "events": events,
                    "active": True,
                },
                timeout=30
            )
            response.raise_for_status()
            hook_data = response.json()
        except httpx.HTTPError as e:
            raise SubscriptionError(f"Failed to create webhook: {e}")

        return Subscription(
            endpoint=endpoint,
            parameters=parameters,
            properties={
                "hook_id": str(hook_data["id"]),
                "webhook_secret": webhook_secret,
            },
        )

    def _delete_subscription(
        self,
        subscription: Subscription,
        credentials: Mapping[str, Any],
        credential_type: CredentialType
    ) -> UnsubscribeResult:
        """Delete webhook from external service"""
        token = credentials.get("access_token")
        repository = subscription.parameters.get("repository")
        hook_id = subscription.properties.get("hook_id")

        try:
            response = httpx.delete(
                f"https://api.example.com/repos/{repository}/hooks/{hook_id}",
                headers={"Authorization": f"Bearer {token}"},
                timeout=30
            )
            response.raise_for_status()
            return UnsubscribeResult(success=True, message="Webhook deleted")
        except httpx.HTTPError as e:
            return UnsubscribeResult(success=False, message=str(e))

    def _refresh_subscription(
        self,
        subscription: Subscription,
        credentials: Mapping[str, Any],
        credential_type: CredentialType
    ) -> Subscription:
        """Refresh subscription expiration (called periodically)"""
        import time
        WEBHOOK_TTL = 30 * 24 * 60 * 60  # 30 days
        return Subscription(
            expires_at=int(time.time()) + WEBHOOK_TTL,
            endpoint=subscription.endpoint,
            parameters=subscription.parameters,
            properties=subscription.properties,
        )

    def _fetch_parameter_options(
        self,
        parameter: str,
        credentials: Mapping[str, Any],
        credential_type: CredentialType
    ) -> list:
        """Fetch dynamic options for parameters (e.g., repository list)"""
        from dify_plugin.entities import I18nObject, ParameterOption

        if parameter != "repository":
            return []

        token = credentials.get("access_token")
        # Fetch repositories from API
        response = httpx.get(
            "https://api.example.com/user/repos",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10
        )
        repos = response.json()

        return [
            ParameterOption(
                value=repo["full_name"],
                label=I18nObject(en_US=repo["full_name"]),
                icon=repo.get("owner", {}).get("avatar_url")
            )
            for repo in repos
        ]
```

## Event Handler Implementation

```python
from typing import Any, Mapping
from werkzeug import Request
from dify_plugin.entities.trigger import Variables
from dify_plugin.errors.trigger import EventIgnoreError
from dify_plugin.interfaces.trigger import Event

class IssuesEvent(Event):
    def _on_event(
        self,
        request: Request,
        parameters: Mapping[str, Any],   # Event filter params from YAML
        payload: Mapping[str, Any]        # Webhook payload
    ) -> Variables:
        """Process event and return workflow variables"""
        # Apply filters
        allowed_actions = parameters.get("actions", [])
        action = payload.get("action")

        if allowed_actions and action not in allowed_actions:
            raise EventIgnoreError(f"Action '{action}' not in filter")

        # Filter by labels
        labels_filter = parameters.get("labels", "")
        if labels_filter:
            required_labels = {s.strip() for s in labels_filter.split(",")}
            issue_labels = {
                label["name"]
                for label in payload.get("issue", {}).get("labels", [])
            }
            if not required_labels.issubset(issue_labels):
                raise EventIgnoreError("Required labels not present")

        # Return variables for workflow
        return Variables(variables=payload)
```

## Event Parameter Types

| Type | Description |
|------|-------------|
| `string` | Text input |
| `number` | Numeric value |
| `boolean` | True/false toggle |
| `select` | Dropdown selection |
| `file` | Single file input |
| `files` | Multiple files |
| `model-selector` | Model picker |
| `app-selector` | Dify app picker |
| `object` | Nested object |
| `array` | Array of values |
| `dynamic-select` | Fetches options dynamically |
| `checkbox` | Multiple selection |

## Error Types

```python
from dify_plugin.errors.trigger import (
    SubscriptionError,                         # Subscription creation failed
    TriggerDispatchError,                      # Event dispatch failed
    TriggerProviderCredentialValidationError,  # Invalid credentials
    TriggerProviderOAuthError,                 # OAuth flow error
    TriggerValidationError,                    # Validation failed (e.g., signature)
    EventIgnoreError,                          # Skip this event (not an error)
)
```

## Workflow

1. **User creates subscription** → `_create_subscription()` called
2. **External service sends webhook** → `_dispatch_event()` called
3. **Event matched** → `_on_event()` called for each matching event
4. **Variables returned** → Workflow starts with these variables
5. **User deletes subscription** → `_delete_subscription()` called

## Best Practices

1. **Validate signatures** - Always verify webhook authenticity
2. **Store hook metadata** - Save hook_id in properties for cleanup
3. **Generate secrets** - Create unique secrets per subscription
4. **Handle cleanup** - Implement proper `_delete_subscription`
5. **Use EventIgnoreError** - Skip irrelevant events gracefully
6. **Define output_schema** - Document expected workflow variables
