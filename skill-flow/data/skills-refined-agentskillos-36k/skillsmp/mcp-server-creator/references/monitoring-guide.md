# MCP Server Monitoring and Observability Guide

This document provides guidance on monitoring and observing your production MCP server.

## Health Checks

### Basic Health Endpoint
```python
import time
import psutil
from datetime import datetime

from starlette.responses import JSONResponse
from starlette.requests import Request

@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request):
    """Basic health check endpoint."""
    return JSONResponse({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "my-server",
        "version": "1.0.0",
        "uptime": time.time(),
    })
```

### Comprehensive Health Check
```python
import time
import psutil
from datetime import datetime
from starlette.responses import JSONResponse
from starlette.requests import Request

@mcp.custom_route("/health", methods=["GET"])
async def comprehensive_health_check(request: Request):
    """Comprehensive health check with system metrics."""
    # Check system resources
    memory_percent = psutil.virtual_memory().percent
    cpu_percent = psutil.cpu_percent(interval=1)

    # Check critical dependencies (customize based on your server)
    checks = {}

    # Example: Check database connection
    try:
        # db_ping_result = await database.ping()
        # checks["database"] = "healthy" if db_ping_result else "unhealthy"
        checks["database"] = "healthy"  # Placeholder
    except Exception as e:
        checks["database"] = f"unhealthy: {str(e)}"

    # Example: Check external API
    try:
        # external_check = await check_external_service()
        # checks["external_api"] = "healthy" if external_check else "unhealthy"
        checks["external_api"] = "healthy"  # Placeholder
    except Exception as e:
        checks["external_api"] = f"unhealthy: {str(e)}"

    # Determine overall status
    all_healthy = all(status == "healthy" for status in checks.values())
    overall_status = "healthy" if all_healthy else "degraded"

    # If system resources are critically low, mark as unhealthy
    if memory_percent > 90 or cpu_percent > 95:
        overall_status = "unhealthy"

    return JSONResponse({
        "status": overall_status,
        "timestamp": datetime.now().isoformat(),
        "service": "my-server",
        "version": "1.0.0",
        "uptime": time.process_time(),
        "system": {
            "memory_usage_percent": memory_percent,
            "cpu_usage_percent": cpu_percent,
            "disk_usage_percent": psutil.disk_usage('/').percent
        },
        "checks": checks
    })
```

## Metrics Collection

### Basic Metrics Middleware
```python
from collections import Counter, defaultdict
import time
from typing import Dict, Any

class MetricsCollector:
    def __init__(self):
        self.request_counts = Counter()
        self.error_counts = Counter()
        self.request_durations = defaultdict(list)
        self.start_times = {}

    def start_timer(self, request_id: str):
        """Start timing a request."""
        self.start_times[request_id] = time.time()

    def record_request(self, tool_name: str, status: str):
        """Record a completed request."""
        self.request_counts[(tool_name, status)] += 1

    def record_error(self, tool_name: str, error_type: str):
        """Record an error."""
        self.error_counts[(tool_name, error_type)] += 1

    def record_duration(self, request_id: str, tool_name: str):
        """Record request duration."""
        if request_id in self.start_times:
            duration = time.time() - self.start_times.pop(request_id)
            self.request_durations[tool_name].append(duration)

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics snapshot."""
        # Calculate averages
        avg_durations = {}
        for tool, durations in self.request_durations.items():
            if durations:
                avg_durations[tool] = sum(durations) / len(durations)

        return {
            "request_counts": dict(self.request_counts),
            "error_counts": dict(self.error_counts),
            "average_durations": avg_durations,
            "total_requests": sum(self.request_counts.values()),
            "total_errors": sum(self.error_counts.values())
        }

metrics = MetricsCollector()
```

### Tool Instrumentation
```python
import uuid

def instrumented_tool(tool_func):
    """Decorator to add metrics instrumentation to tools."""
    async def wrapper(*args, **kwargs):
        request_id = str(uuid.uuid4())
        tool_name = tool_func.__name__

        # Start timing
        metrics.start_timer(request_id)

        try:
            result = await tool_func(*args, **kwargs)
            # Record successful request
            metrics.record_request(tool_name, "success")
            return result
        except Exception as e:
            # Record error
            metrics.record_error(tool_name, type(e).__name__)
            metrics.record_request(tool_name, "error")
            raise
        finally:
            # Record duration
            metrics.record_duration(request_id, tool_name)

    return wrapper

# Example usage:
@mcp.tool()
@instrumented_tool
async def instrumented_example_tool(data: str) -> str:
    """Example tool with instrumentation."""
    return f"Processed: {data}"
```

### Prometheus Metrics Endpoint
```python
from starlette.responses import PlainTextResponse
from starlette.requests import Request


@mcp.custom_route("/metrics", methods=["GET"])
async def prometheus_metrics(request: Request):
    """Prometheus-compatible metrics endpoint."""
    metrics_data = metrics.get_metrics()

    output_lines = []

    # Request counts
    for (tool, status), count in metrics_data["request_counts"].items():
        output_lines.append(f'mcp_requests_total{{tool="{tool}", status="{status}"}} {count}')

    # Error counts
    for (tool, error_type), count in metrics_data["error_counts"].items():
        output_lines.append(f'mcp_errors_total{{tool="{tool}", error_type="{error_type}"}} {count}')

    # Average durations
    for tool, avg_duration in metrics_data["average_durations"].items():
        output_lines.append(f'mcp_request_duration_seconds_avg{{tool="{tool}"}} {avg_duration:.4f}')

    # Total requests
    output_lines.append(f'mcp_requests_total_all {metrics_data["total_requests"]}')
    output_lines.append(f'mcp_errors_total_all {metrics_data["total_errors"]}')

    return PlainTextResponse("\n".join(output_lines))
```

## Logging Patterns

### Structured Logging
```python
import logging
import json
from datetime import datetime

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Create handler
        handler = logging.StreamHandler()

        # Create formatter
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

    def log(self, level: str, message: str, **kwargs):
        """Log a structured message."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level.upper(),
            "message": message,
            **kwargs
        }

        getattr(self.logger, level.lower())(json.dumps(log_entry))

structured_logger = StructuredLogger("mcp-server")

@mcp.tool()
async def logged_tool(data: str, ctx=None) -> str:
    """Tool with structured logging."""
    # Log the start of the operation
    structured_logger.log(
        "info",
        "Starting tool execution",
        tool="logged_tool",
        data_length=len(data),
        client=getattr(ctx, 'client_id', 'unknown') if ctx else 'unknown'
    )

    try:
        result = await process_data_async(data)

        # Log successful completion
        structured_logger.log(
            "info",
            "Tool execution completed successfully",
            tool="logged_tool",
            result_length=len(result) if isinstance(result, (str, list, dict)) else "N/A"
        )

        return result
    except Exception as e:
        # Log error
        structured_logger.log(
            "error",
            "Tool execution failed",
            tool="logged_tool",
            error=str(e),
            error_type=type(e).__name__
        )

        raise
```

### Context-Aware Logging
```python
@mcp.tool()
async def context_aware_tool(query: str, ctx) -> str:
    """Tool that uses MCP context for logging."""
    # Log to the client via MCP context
    await ctx.log('info', f'Received query: {query[:50]}...', 'context_aware_tool')

    try:
        result = await complex_operation(query)

        # Log progress
        await ctx.log('info', 'Operation completed successfully', 'context_aware_tool')

        return result
    except Exception as e:
        # Log error to client
        await ctx.log('error', f'Operation failed: {str(e)}', 'context_aware_tool')
        raise
```

## Alerting and Notification

### Alert Conditions
```python
from typing import List, Dict

class AlertManager:
    def __init__(self):
        self.alert_conditions = []
        self.active_alerts = set()

    def add_condition(self, name: str, condition_func, severity: str = "warning"):
        """Add an alert condition."""
        self.alert_conditions.append({
            "name": name,
            "condition": condition_func,
            "severity": severity
        })

    def check_alerts(self) -> List[Dict]:
        """Check all alert conditions."""
        triggered_alerts = []

        for condition in self.alert_conditions:
            try:
                if condition["condition"]():
                    alert = {
                        "name": condition["name"],
                        "severity": condition["severity"],
                        "timestamp": datetime.now().isoformat()
                    }
                    triggered_alerts.append(alert)

                    # Track active alerts to avoid spam
                    alert_key = condition["name"]
                    if alert_key not in self.active_alerts:
                        self.active_alerts.add(alert_key)
                        self.send_notification(alert)
                else:
                    # Remove from active alerts if condition is no longer met
                    self.active_alerts.discard(condition["name"])
            except Exception as e:
                # Don't let alert condition errors break the system
                structured_logger.log(
                    "error",
                    f"Alert condition check failed: {str(e)}",
                    condition=condition["name"]
                )

        return triggered_alerts

    def send_notification(self, alert: Dict):
        """Send notification about alert (implementation depends on your system)."""
        # This would integrate with your notification system
        structured_logger.log(
            "warning",
            "Alert triggered",
            **alert
        )

alert_manager = AlertManager()

# Example alert conditions
alert_manager.add_condition(
    "high_error_rate",
    lambda: (metrics.get_metrics()["total_errors"] / max(metrics.get_metrics()["total_requests"], 1)) > 0.1,
    "critical"
)

alert_manager.add_condition(
    "high_memory_usage",
    lambda: psutil.virtual_memory().percent > 85,
    "warning"
)
```

## Performance Monitoring

### Response Time Tracking
```python
import statistics

class ResponseTimeTracker:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.response_times = defaultdict(list)

    def add_response_time(self, tool_name: str, duration: float):
        """Add a response time measurement."""
        times = self.response_times[tool_name]
        times.append(duration)

        # Keep only the last window_size measurements
        if len(times) > self.window_size:
            times.pop(0)

    def get_stats(self, tool_name: str) -> Dict[str, float]:
        """Get response time statistics for a tool."""
        times = self.response_times[tool_name]
        if not times:
            return {}

        return {
            "avg": statistics.mean(times),
            "median": statistics.median(times),
            "p95": float(sorted(times)[int(0.95 * len(times))]) if times else 0,
            "p99": float(sorted(times)[int(0.99 * len(times))]) if times else 0,
            "min": min(times),
            "max": max(times),
            "count": len(times)
        }

response_tracker = ResponseTimeTracker()

# Integration with metrics collector
original_record_duration = metrics.record_duration

def enhanced_record_duration(request_id: str, tool_name: str):
    """Enhanced duration recording that also tracks response times."""
    if request_id in metrics.start_times:
        duration = time.time() - metrics.start_times.pop(request_id)
        metrics.request_durations[tool_name].append(duration)
        response_tracker.add_response_time(tool_name, duration)

metrics.record_duration = enhanced_record_duration
```

## Dashboard Metrics

### Summary Metrics Endpoint
```python
from starlette.responses import JSONResponse
from starlette.requests import Request

@mcp.custom_route("/dashboard", methods=["GET"])
async def dashboard_metrics(request: Request):
    """Endpoint with metrics suitable for dashboards."""
    metrics_data = metrics.get_metrics()
    response_stats = {}

    # Gather response time statistics for all tools
    for tool_name in metrics_data["average_durations"].keys():
        response_stats[tool_name] = response_tracker.get_stats(tool_name)

    return JSONResponse({
        "summary": {
            "total_requests": metrics_data["total_requests"],
            "total_errors": metrics_data["total_errors"],
            "error_rate": (
                metrics_data["total_errors"] / metrics_data["total_requests"]
                if metrics_data["total_requests"] > 0 else 0
            ),
            "uptime_minutes": time.process_time() / 60
        },
        "by_tool": {
            tool: {
                "requests": sum(1 for t, s in metrics_data["request_counts"] if t == tool),
                "errors": sum(count for (t, e), count in metrics_data["error_counts"].items() if t == tool),
                "avg_duration": metrics_data["average_durations"].get(tool, 0),
                "response_stats": response_stats.get(tool, {})
            }
            for tool in set(t for t, _ in metrics_data["request_counts"])
        },
        "system": {
            "memory_percent": psutil.virtual_memory().percent,
            "cpu_percent": psutil.cpu_percent(interval=1),
            "disk_percent": psutil.disk_usage('/').percent
        },
        "timestamp": datetime.now().isoformat()
    })
```

## Log Aggregation

### Log Rotation and Archiving
```python
import logging.handlers
import os

def setup_rotating_logs(log_file_path: str = "mcp-server.log"):
    """Set up rotating log files."""
    logger = logging.getLogger("mcp-server")
    logger.setLevel(logging.INFO)

    # Create rotating file handler (10MB per file, keep 5 backups)
    handler = logging.handlers.RotatingFileHandler(
        log_file_path,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

# Use in your server initialization
log_file_path = os.getenv("LOG_FILE_PATH", "mcp-server.log")
setup_rotating_logs(log_file_path)
```

These monitoring patterns will help you maintain visibility into your production MCP server's health, performance, and behavior.
