# Extension Plugin Development

Extension plugins add custom HTTP endpoints to Dify for OAuth callbacks, webhooks, and APIs.

## File Structure

```
my-extension/
├── manifest.yaml                # Plugin manifest
├── main.py                      # Entry point
├── pyproject.toml               # Dependencies (uv)
├── README.md                    # Documentation
├── _assets/
│   └── icon.svg                 # Plugin icon
├── group/
│   └── {group_name}.yaml        # Endpoint group config (settings)
└── endpoints/
    ├── {endpoint_name}.yaml     # Endpoint definition (path, method)
    └── {endpoint_name}.py       # Endpoint implementation (HTTP handler)
```

## manifest.yaml

```yaml
version: 0.0.1
type: plugin
author: your-name
name: my_extension
label:
  en_US: My Extension
  zh_Hans: 我的扩展
description:
  en_US: Custom HTTP endpoints
icon: icon.svg

meta:
  version: 0.0.1
  arch: [amd64, arm64]
  runner:
    language: python
    version: "3.12"
    entrypoint: main

plugins:
  endpoints:                   # Note: endpoints, not tools
    - group/my_group.yaml

resource:
  memory: 1048576
  permission:
    tool:
      enabled: false
    model:
      enabled: false
    endpoint:
      enabled: true            # Required for extensions
    app:
      enabled: true            # Enable to invoke Dify apps
    storage:
      enabled: true            # Enable for persistent storage
      size: 1048576
```

## group.yaml

Note: No root-level `name` or `label` fields in group.yaml.

```yaml
# Optional: Settings schema for endpoint configuration
settings:
  - name: api_key
    type: secret-input
    required: true
    label:
      en_US: API Key
    help:
      en_US: API key for authentication

  - name: app
    type: app-selector          # Special type: select a Dify app
    scope: chat                  # Options: chat, completion, workflow, agent
    required: false
    label:
      en_US: Dify App
    help:
      en_US: Select a Dify app to invoke from this endpoint

endpoints:
  - endpoints/webhook.yaml
  - endpoints/callback.yaml
```

## endpoint.yaml

Note: Official implementations use minimal endpoint.yaml without `label` or `description`.

```yaml
path: "/webhook"
method: "POST"

extra:
  python:
    source: endpoints/webhook.py
```

## Endpoint Implementation

```python
import json
from werkzeug import Request, Response
from dify_plugin.interfaces.endpoint import Endpoint

class WebhookEndpoint(Endpoint):
    def _invoke(
        self,
        request: Request,
        values: dict,           # URL path parameters
        settings: dict          # Endpoint settings from group.yaml
    ) -> Response:
        """Handle incoming request"""
        # Access settings
        api_key = settings.get("api_key")

        # Validate request
        auth_header = request.headers.get("Authorization")
        if auth_header != f"Bearer {api_key}":
            return Response(
                response=json.dumps({"error": "Unauthorized"}),
                status=401,
                mimetype="application/json"
            )

        # Parse request body
        try:
            data = request.get_json(force=True)
        except Exception:
            return Response(
                response=json.dumps({"error": "Invalid JSON"}),
                status=400,
                mimetype="application/json"
            )

        # Process request
        result = self._process_webhook(data)

        return Response(
            response=json.dumps(result),
            status=200,
            mimetype="application/json"
        )

    def _process_webhook(self, data: dict) -> dict:
        """Process webhook payload"""
        return {
            "status": "received",
            "event": data.get("event"),
            "timestamp": data.get("timestamp")
        }
```

## OAuth Callback Example

```yaml
# endpoints/oauth_callback.yaml
path: "/oauth/callback"
method: "GET"
label:
  en_US: OAuth Callback
description:
  en_US: Handles OAuth authorization callback

extra:
  python:
    source: endpoints/oauth_callback.py
```

```python
# endpoints/oauth_callback.py
import httpx
from urllib.parse import urlencode
from werkzeug import Request, Response
from dify_plugin.interfaces.endpoint import Endpoint

class OAuthCallbackEndpoint(Endpoint):
    def _invoke(
        self,
        request: Request,
        values: dict,
        settings: dict
    ) -> Response:
        """Handle OAuth callback"""
        code = request.args.get("code")
        state = request.args.get("state")
        error = request.args.get("error")

        if error:
            return self._error_response(f"OAuth error: {error}")

        if not code:
            return self._error_response("Missing authorization code")

        # Exchange code for token
        try:
            token_data = self._exchange_code(code, settings)
        except Exception as e:
            return self._error_response(f"Token exchange failed: {e}")

        # Success page
        return Response(
            response=self._success_html(token_data),
            status=200,
            mimetype="text/html"
        )

    def _exchange_code(self, code: str, settings: dict) -> dict:
        """Exchange authorization code for access token"""
        response = httpx.post(
            "https://oauth.example.com/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": settings.get("client_id"),
                "client_secret": settings.get("client_secret"),
                "redirect_uri": settings.get("redirect_uri"),
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()

    def _error_response(self, message: str) -> Response:
        return Response(
            response=f"<html><body><h1>Error</h1><p>{message}</p></body></html>",
            status=400,
            mimetype="text/html"
        )

    def _success_html(self, token_data: dict) -> str:
        return """
        <html>
        <body>
            <h1>Authorization Successful</h1>
            <p>You can close this window.</p>
            <script>window.close();</script>
        </body>
        </html>
        """
```

## File Upload Example

```yaml
# endpoints/upload.yaml
path: "/upload"
method: "POST"
label:
  en_US: File Upload
description:
  en_US: Handles file uploads

extra:
  python:
    source: endpoints/upload.py
```

```python
# endpoints/upload.py
import json
from werkzeug import Request, Response
from dify_plugin.interfaces.endpoint import Endpoint

class UploadEndpoint(Endpoint):
    def _invoke(
        self,
        request: Request,
        values: dict,
        settings: dict
    ) -> Response:
        """Handle file upload"""
        if "file" not in request.files:
            return Response(
                response=json.dumps({"error": "No file provided"}),
                status=400,
                mimetype="application/json"
            )

        file = request.files["file"]
        filename = file.filename
        content = file.read()

        # Process file
        result = self._process_file(filename, content)

        return Response(
            response=json.dumps(result),
            status=200,
            mimetype="application/json"
        )

    def _process_file(self, filename: str, content: bytes) -> dict:
        return {
            "filename": filename,
            "size": len(content),
            "status": "uploaded"
        }
```

## Path Parameters

```yaml
# endpoints/item.yaml
path: "/items/<item_id>"
method: "GET"
label:
  en_US: Get Item

extra:
  python:
    source: endpoints/item.py
```

```python
# endpoints/item.py
class ItemEndpoint(Endpoint):
    def _invoke(self, request: Request, values: dict, settings: dict) -> Response:
        item_id = values.get("item_id")  # From URL path
        # ...
```

## HTTP Methods

| Method | Use Case |
|--------|----------|
| `HEAD` | Check resource existence |
| `GET` | Retrieve data, OAuth callbacks |
| `POST` | Webhooks, file uploads, create resources |
| `PUT` | Update resources |
| `DELETE` | Delete resources |
| `OPTIONS` | CORS preflight requests |

**Note**: `PATCH` is not in the official supported methods list.

## Response Helpers

```python
import json
from werkzeug import Response

# JSON response
Response(
    response=json.dumps({"key": "value"}),
    status=200,
    mimetype="application/json"
)

# HTML response
Response(
    response="<html><body>Hello</body></html>",
    status=200,
    mimetype="text/html"
)

# Redirect
Response(
    response="",
    status=302,
    headers={"Location": "https://example.com"}
)

# File download
Response(
    response=file_bytes,
    status=200,
    mimetype="application/octet-stream",
    headers={"Content-Disposition": "attachment; filename=file.pdf"}
)
```

## Invoking Dify Apps

Extensions can invoke Dify apps (chat, completion, workflow) when `permission.app.enabled: true`:

```python
from collections.abc import Generator
from werkzeug import Request, Response
from dify_plugin.interfaces.endpoint import Endpoint
import json

class ChatEndpoint(Endpoint):
    def _invoke(
        self,
        request: Request,
        values: dict,
        settings: dict
    ) -> Response:
        # Get app ID from settings (app-selector type)
        app_id = settings.get("app", {}).get("app_id")
        if not app_id:
            return Response(
                response=json.dumps({"error": "No app configured"}),
                status=400,
                mimetype="application/json"
            )

        data = request.get_json(force=True)
        query = data.get("query", "")

        # Invoke Dify chat app
        response_text = ""
        for chunk in self.session.app.chat.invoke(
            app_id=app_id,
            query=query,
            inputs={},                    # Optional workflow inputs
            conversation_id="",           # Empty for new conversation
        ):
            # chunk is a generator yielding response pieces
            response_text += chunk.get("answer", "")

        return Response(
            response=json.dumps({"answer": response_text}),
            status=200,
            mimetype="application/json"
        )
```

Available app invocation methods:
- `self.session.app.chat.invoke()` - Chat apps
- `self.session.app.completion.invoke()` - Completion apps
- `self.session.app.workflow.invoke()` - Workflow apps

## Use Cases

| Use Case | Path | Method | Description |
|----------|------|--------|-------------|
| OAuth callback | `/oauth/callback` | GET | Handle OAuth authorization |
| Webhook receiver | `/webhook` | POST | Receive external events |
| File upload | `/upload` | POST | Handle file uploads |
| API proxy | `/api/<path>` | ANY | Proxy requests to external API |
| Health check | `/health` | GET | Service status endpoint |
| Chat gateway | `/chat` | POST | Invoke Dify app from endpoint |

## Best Practices

1. **Validate requests** - Check auth headers and payload format
2. **Handle errors** - Return appropriate HTTP status codes
3. **Use settings** - Store secrets in group settings, not code
4. **Set CORS** - Add CORS headers if accessed from browsers
5. **Log requests** - Use logging for debugging
