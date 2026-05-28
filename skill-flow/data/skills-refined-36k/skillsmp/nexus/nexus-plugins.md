---
skill: nexus-plugins
description: Plugin development and extending Nexus with custom functionality
priority: LOW
tags: [nexus, plugins, extensibility, custom, development]
---

# Nexus Plugins

Extend Nexus with custom plugins and integrations.

## Plugin System Overview (v1.1.0)

Nexus provides a plugin system for extending functionality without modifying core code.

**v1.1.0 Validation Improvements:**
- ✅ Plugin validation now checks for `name` and `apply` method
- ✅ Specific error handling for TypeError (missing constructor args)
- ✅ Improved logging for plugin failures
- ✅ Validates plugin name is non-empty string

**Plugin Interface:**
```python
from nexus.plugins import NexusPlugin

class MyPlugin(NexusPlugin):
    @property
    def name(self) -> str:
        return "my_plugin"  # Required: non-empty string

    @property
    def description(self) -> str:
        return "Description"  # Required

    def apply(self, nexus_instance) -> None:
        # Required: must be callable
        pass

    def validate(self) -> bool:
        # Optional: custom validation
        return super().validate()
```

## Built-in Plugins

### Auth Plugin

```python
from nexus.plugins import AuthPlugin

auth_plugin = AuthPlugin()
auth_plugin.strategy = "oauth2"
auth_plugin.provider = "google"

app.add_plugin(auth_plugin)
```

### Monitoring Plugin

```python
from nexus.plugins import MonitoringPlugin

monitoring_plugin = MonitoringPlugin()
monitoring_plugin.backend = "prometheus"
monitoring_plugin.interval = 30

app.add_plugin(monitoring_plugin)
```

### Rate Limit Plugin

```python
from nexus.plugins import RateLimitPlugin

rate_limit_plugin = RateLimitPlugin()
rate_limit_plugin.limit = 1000  # per minute
rate_limit_plugin.burst = 100

app.add_plugin(rate_limit_plugin)
```

## Creating Custom Plugins

### Plugin Base Class

```python
from nexus.plugins import NexusPlugin

class MyCustomPlugin(NexusPlugin):
    @property
    def name(self):
        return "my_custom_plugin"

    @property
    def description(self):
        return "My custom Nexus plugin"

    @property
    def version(self):
        return "1.0.0"

    def setup(self, nexus_app):
        """Called when plugin is added to Nexus"""
        self.app = nexus_app
        print(f"Setting up {self.name}")

    def teardown(self):
        """Called when Nexus is stopped"""
        print(f"Tearing down {self.name}")

# Use plugin
plugin = MyCustomPlugin()
app.add_plugin(plugin)
```

## Plugin Examples

### Request Logger Plugin

```python
class RequestLoggerPlugin(NexusPlugin):
    @property
    def name(self):
        return "request_logger"

    def setup(self, nexus_app):
        self.app = nexus_app

        # Hook into request lifecycle
        @nexus_app.on_workflow_started
        def log_request(event):
            self.log_request(event)

        @nexus_app.on_workflow_completed
        def log_response(event):
            self.log_response(event)

    def log_request(self, event):
        print(f"[REQUEST] {event.workflow_name} - {event.channel}")
        print(f"  Inputs: {event.inputs}")

    def log_response(self, event):
        print(f"[RESPONSE] {event.workflow_name}")
        print(f"  Duration: {event.duration}s")
        print(f"  Success: {event.result is not None}")

# Use plugin
app.add_plugin(RequestLoggerPlugin())
```

### Metrics Collection Plugin

```python
class MetricsPlugin(NexusPlugin):
    @property
    def name(self):
        return "metrics"

    def setup(self, nexus_app):
        self.app = nexus_app
        self.metrics = {
            "requests_total": 0,
            "requests_success": 0,
            "requests_failed": 0,
            "total_duration": 0
        }

        @nexus_app.on_workflow_started
        def count_request(event):
            self.metrics["requests_total"] += 1

        @nexus_app.on_workflow_completed
        def count_success(event):
            self.metrics["requests_success"] += 1
            self.metrics["total_duration"] += event.duration

        @nexus_app.on_workflow_failed
        def count_failure(event):
            self.metrics["requests_failed"] += 1

    def get_metrics(self):
        avg_duration = (
            self.metrics["total_duration"] / self.metrics["requests_success"]
            if self.metrics["requests_success"] > 0
            else 0
        )

        return {
            **self.metrics,
            "avg_duration": avg_duration,
            "success_rate": (
                self.metrics["requests_success"] / self.metrics["requests_total"]
                if self.metrics["requests_total"] > 0
                else 0
            )
        }

# Use plugin
metrics_plugin = MetricsPlugin()
app.add_plugin(metrics_plugin)

# Access metrics
print(metrics_plugin.get_metrics())
```

### Webhook Integration Plugin

```python
import requests

class WebhookPlugin(NexusPlugin):
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    @property
    def name(self):
        return "webhook"

    def setup(self, nexus_app):
        self.app = nexus_app

        @nexus_app.on_workflow_completed
        def send_webhook(event):
            self.send_notification(event)

    def send_notification(self, event):
        payload = {
            "workflow": event.workflow_name,
            "status": "completed",
            "duration": event.duration,
            "timestamp": event.timestamp
        }

        try:
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
        except Exception as e:
            print(f"Webhook error: {e}")

# Use plugin
webhook_plugin = WebhookPlugin("https://example.com/webhook")
app.add_plugin(webhook_plugin)
```

### Caching Plugin

```python
import hashlib
import json

class CachingPlugin(NexusPlugin):
    def __init__(self, ttl=300):
        self.ttl = ttl
        self.cache = {}

    @property
    def name(self):
        return "caching"

    def setup(self, nexus_app):
        self.app = nexus_app
        self._wrap_execute()

    def _wrap_execute(self):
        original_execute = self.app.execute_workflow

        def cached_execute(workflow_name, inputs, **kwargs):
            # Generate cache key
            cache_key = self._generate_key(workflow_name, inputs)

            # Check cache
            cached = self.cache.get(cache_key)
            if cached and time.time() - cached["timestamp"] < self.ttl:
                print(f"Cache hit for {workflow_name}")
                return cached["result"]

            # Execute workflow
            result = original_execute(workflow_name, inputs, **kwargs)

            # Cache result
            self.cache[cache_key] = {
                "result": result,
                "timestamp": time.time()
            }

            return result

        self.app.execute_workflow = cached_execute

    def _generate_key(self, workflow_name, inputs):
        data = json.dumps({"workflow": workflow_name, "inputs": inputs}, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()

    def clear_cache(self):
        self.cache = {}

# Use plugin
caching_plugin = CachingPlugin(ttl=600)
app.add_plugin(caching_plugin)
```

### Database Integration Plugin

```python
import psycopg2

class DatabasePlugin(NexusPlugin):
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.conn = None

    @property
    def name(self):
        return "database"

    def setup(self, nexus_app):
        self.app = nexus_app
        self.conn = psycopg2.connect(self.connection_string)

        @nexus_app.on_workflow_started
        def log_start(event):
            self.log_execution_start(event)

        @nexus_app.on_workflow_completed
        def log_complete(event):
            self.log_execution_complete(event)

    def log_execution_start(self, event):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO workflow_executions (
                workflow_id, workflow_name, session_id, channel, started_at
            ) VALUES (%s, %s, %s, %s, NOW())
        """, (event.workflow_id, event.workflow_name, event.session_id, event.channel))
        self.conn.commit()

    def log_execution_complete(self, event):
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE workflow_executions
            SET completed_at = NOW(),
                duration = %s,
                status = 'completed'
            WHERE workflow_id = %s
        """, (event.duration, event.workflow_id))
        self.conn.commit()

    def teardown(self):
        if self.conn:
            self.conn.close()

# Use plugin
db_plugin = DatabasePlugin("postgresql://localhost/nexus")
app.add_plugin(db_plugin)
```

## Plugin Lifecycle

```python
class PluginLifecycle(NexusPlugin):
    @property
    def name(self):
        return "lifecycle_demo"

    def __init__(self):
        print("1. Plugin instantiated")

    def setup(self, nexus_app):
        print("2. Plugin setup called")
        self.app = nexus_app

        # Register hooks
        @nexus_app.on_startup
        def on_startup():
            print("3. Nexus started, plugin running")

        @nexus_app.on_shutdown
        def on_shutdown():
            print("5. Nexus shutting down")

    def teardown(self):
        print("6. Plugin teardown called")
```

## Plugin Configuration

```python
class ConfigurablePlugin(NexusPlugin):
    def __init__(self, config=None):
        self.config = config or {}

    @property
    def name(self):
        return "configurable"

    def setup(self, nexus_app):
        self.app = nexus_app

        # Use configuration
        enabled = self.config.get("enabled", True)
        log_level = self.config.get("log_level", "INFO")
        max_retries = self.config.get("max_retries", 3)

        if enabled:
            print(f"Plugin enabled with log_level={log_level}")

# Use with config
plugin = ConfigurablePlugin({
    "enabled": True,
    "log_level": "DEBUG",
    "max_retries": 5
})
app.add_plugin(plugin)
```

## Plugin Manager

```python
class PluginManager:
    def __init__(self, nexus_app):
        self.app = nexus_app
        self.plugins = {}

    def register(self, plugin):
        """Register and setup plugin"""
        if plugin.name in self.plugins:
            raise ValueError(f"Plugin {plugin.name} already registered")

        self.plugins[plugin.name] = plugin
        plugin.setup(self.app)
        print(f"Plugin registered: {plugin.name} v{plugin.version}")

    def unregister(self, plugin_name):
        """Unregister and teardown plugin"""
        if plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]
            plugin.teardown()
            del self.plugins[plugin_name]
            print(f"Plugin unregistered: {plugin_name}")

    def get(self, plugin_name):
        """Get plugin by name"""
        return self.plugins.get(plugin_name)

    def list(self):
        """List all registered plugins"""
        return list(self.plugins.keys())

# Use plugin manager
pm = PluginManager(app)
pm.register(MyCustomPlugin())
pm.register(MetricsPlugin())
print(f"Active plugins: {pm.list()}")
```

## Best Practices

1. **Keep Plugins Focused** - One responsibility per plugin
2. **Handle Errors Gracefully** - Don't crash the app
3. **Clean Up Resources** - Implement teardown properly
4. **Make Plugins Configurable** - Accept configuration
5. **Document Plugin Usage** - Clear documentation
6. **Test Plugins Independently** - Unit test plugins
7. **Version Plugins** - Track version numbers
8. **Use Dependency Injection** - Don't access globals

## Key Takeaways

- Plugins extend Nexus without modifying core
- Inherit from NexusPlugin base class
- Hook into lifecycle events
- Clean up in teardown method
- Use PluginManager for organization
- Configure via constructor parameters
- Test plugins independently

## Related Skills

- [nexus-architecture](#) - Understand plugin system
- [nexus-event-system](#) - Use events in plugins
- [nexus-enterprise-features](#) - Built-in plugins
