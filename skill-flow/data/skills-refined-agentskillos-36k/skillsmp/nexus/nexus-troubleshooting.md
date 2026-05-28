---
skill: nexus-troubleshooting
description: Common issues, debugging strategies, and solutions for Nexus platform
priority: HIGH
tags: [nexus, troubleshooting, debugging, errors, solutions]
---

# Nexus Troubleshooting

Common issues and solutions for Nexus platform.

## Common Issues

### 1. Port Already in Use

**Error**: `Address already in use`

**Solution**:
```python
# Use custom ports
app = Nexus(api_port=8001, mcp_port=3002)
```

**Check port usage**:
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### 2. Workflow Not Found

**Error**: `Workflow 'my-workflow' not registered`

**Solution**:
```python
# Ensure .build() is called
workflow = WorkflowBuilder()
workflow.add_node("PythonCodeNode", "test", {"code": "result = {'ok': True}"})
app.register("my-workflow", workflow.build())  # Don't forget .build()

# Check registered workflows
print(list(app.workflows.keys()))
```

### 3. Auto-Discovery Blocking (with DataFlow)

**Error**: Nexus hangs during initialization

**Solution**:
```python
# Disable auto_discovery when using DataFlow
app = Nexus(auto_discovery=False)

# Also configure DataFlow optimally
db = DataFlow(
    enable_model_persistence=False  # Skip model registry for fast startup
)
```

### 4. Import Errors

**Error**: `ModuleNotFoundError: No module named 'nexus'`

**Solution**:
```bash
# Install Nexus
pip install kailash-nexus

# Verify installation
python -c "from nexus import Nexus; print('OK')"
```

### 5. Authentication Errors

**Error**: `Unauthorized` or `401`

**Solution**:
```python
# Configure authentication
app = Nexus(enable_auth=True)

# For API requests, include auth header
curl -X POST http://localhost:8000/workflows/test/execute \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"inputs": {}}'
```

### 6. Parameter Validation Errors

**Error**: `Invalid parameter type`

**Solution**:
```python
# Check parameter types match node requirements
# Use proper JSON types in API calls

# Correct
{"inputs": {"limit": 10}}  # Integer

# Wrong
{"inputs": {"limit": "10"}}  # String instead of integer
```

### 7. Session Not Found

**Error**: `Session 'session-123' not found or expired`

**Solution**:
```python
# Create session before use
session_id = app.create_session(channel="api")

# Or extend timeout
app.session_manager.extend_timeout(session_id, 600)

# Check session exists
if not app.session_manager.exists(session_id):
    print("Session expired or invalid")
```

### 8. Slow Startup

**Problem**: Nexus takes 10-30 seconds to start

**Solution**:
```python
# With DataFlow, use optimized settings
app = Nexus(auto_discovery=False)
db = DataFlow(
    enable_model_persistence=False,  # Skip model registry for fast startup
    auto_migrate=False,
    skip_migration=True
)

# Should now start in <2 seconds
```

### 9. API Inputs Not Reaching Node

**Problem**: Node doesn't receive API parameters

**Solution**:
```python
# Use try/except pattern in PythonCodeNode
workflow.add_node("PythonCodeNode", "process", {
    "code": """
try:
    param = my_param  # From API inputs
except NameError:
    param = None  # Not provided

result = {'param': param}
"""
})

# API request
curl -X POST http://localhost:8000/workflows/process/execute \
  -d '{"inputs": {"my_param": "value"}}'
```

### 10. Connection Errors Between Nodes

**Problem**: Data not flowing between nodes

**Solution**:
```python
# Use explicit connections with correct paths
workflow.add_connection(
    "node1", "result.data",  # Full path to output
    "node2", "input"         # Input parameter name
)

# Check node outputs match connection source
# Check node inputs match connection target
```

## Debugging Strategies

### 1. Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Or in Nexus
app = Nexus(log_level="DEBUG")
```

### 2. Add Debug Nodes

```python
# Insert debug node to inspect data
workflow.add_node("PythonCodeNode", "debug", {
    "code": """
import json
print(f"Debug data: {json.dumps(data, indent=2)}")
result = data  # Pass through
"""
})
```

### 3. Check Health Status

```bash
# Check overall health
curl http://localhost:8000/health

# Check detailed status
curl http://localhost:8000/health/detailed
```

### 4. Verify Workflow Registration

```python
# List registered workflows
print("Registered workflows:", list(app.workflows.keys()))

# Get workflow details
workflow_info = app.get_workflow_info("my-workflow")
print(workflow_info)
```

### 5. Test Individual Nodes

```python
# Test node in isolation
from kailash.runtime import LocalRuntime

runtime = LocalRuntime()

# Create simple workflow with problem node
test_workflow = WorkflowBuilder()
test_workflow.add_node("ProblemNode", "test", {"param": "value"})

# Execute and check result
result, run_id = runtime.execute(test_workflow.build())
print(f"Result: {result}")
```

### 6. Check API Request Format

```bash
# Use -v for verbose output
curl -v -X POST http://localhost:8000/workflows/test/execute \
  -H "Content-Type: application/json" \
  -d '{"inputs": {"param": "value"}}'

# Check request is sent correctly
# Check response headers and body
```

### 7. Monitor Logs

```bash
# Tail logs in real-time
tail -f nexus.log

# Search for errors
grep ERROR nexus.log

# Search for specific workflow
grep "my-workflow" nexus.log
```

## Common Error Messages

### "Workflow 'X' not registered"
- Forgot to call `.build()`
- Wrong workflow name
- Registration failed (check logs)

### "Invalid parameter type"
- API request has wrong type
- Node expects different type
- Check API schema

### "Session expired"
- Session timeout reached
- Session manually ended
- Session never created

### "Port already in use"
- Another Nexus instance running
- Different service using port
- Change port in config

### "Auto-discovery blocking"
- Using DataFlow with auto_discovery=True
- Set auto_discovery=False

## Performance Issues

### Slow API Responses
```python
# Check workflow execution time
metrics = app.get_workflow_metrics("workflow-name")
print(f"Avg execution time: {metrics['avg_execution_time']}s")

# Optimize workflow
# - Remove unnecessary nodes
# - Optimize PythonCodeNode code
# - Add caching
# - Use async operations
```

### High Memory Usage
```python
# Check session cleanup
app.session_manager.cleanup_expired()

# Configure session limits
app = Nexus(
    session_max_age=1800,  # 30 minutes
    session_cleanup_interval=300  # 5 minutes
)
```

### High CPU Usage
```python
# Check concurrent requests
metrics = app.get_metrics()
print(f"Concurrent requests: {metrics['concurrent_requests']}")

# Limit concurrency
app.api.max_concurrent_requests = 50
```

## Getting Help

### 1. Check Documentation
- [Nexus README](../../sdk-users/apps/nexus/README.md)
- [User Guides](../../sdk-users/apps/nexus/docs/user-guides/)
- [Technical Docs](../../sdk-users/apps/nexus/docs/technical/)

### 2. Enable Verbose Logging
```python
app = Nexus(log_level="DEBUG", log_format="json")
```

### 3. Check GitHub Issues
Search for similar issues in the repository.

### 4. Create Minimal Reproduction
```python
# Minimal example to reproduce issue
from nexus import Nexus
from kailash.workflow.builder import WorkflowBuilder

app = Nexus()

workflow = WorkflowBuilder()
workflow.add_node("PythonCodeNode", "test", {
    "code": "result = {'test': True}"
})

app.register("test", workflow.build())
app.start()
```

## Key Takeaways

- Most issues have simple solutions
- Enable debug logging early
- Check health endpoints regularly
- Use minimal examples to isolate issues
- Verify configuration settings
- Monitor logs and metrics

## Related Skills

- [nexus-quickstart](#) - Basic setup
- [nexus-api-input-mapping](#) - Fix parameter issues
- [nexus-dataflow-integration](#) - Fix integration issues
- [nexus-health-monitoring](#) - Monitor for issues
