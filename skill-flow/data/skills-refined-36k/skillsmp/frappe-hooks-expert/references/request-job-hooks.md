# Request and Job Hooks

Request and job hooks intercept HTTP requests and background job execution.

## Request Hooks

### before_request

Runs before processing HTTP request.

```python
before_request = [
    "my_app.middleware.before_request"
]
```

**Use for:**
- Request logging
- Custom authentication
- Rate limiting
- Request validation

```python
def before_request():
    import frappe
    
    # Log request
    frappe.logger().debug(f"Request: {frappe.request.method} {frappe.request.path}")
    
    # Custom authentication
    api_key = frappe.get_request_header("X-API-Key")
    if api_key:
        validate_api_key(api_key)
    
    # Rate limiting
    check_rate_limit(frappe.session.user)
```

### after_request

Runs after processing HTTP request.

```python
after_request = [
    "my_app.middleware.after_request"
]
```

**Use for:**
- Response modification
- Logging response
- Adding custom headers

```python
def after_request():
    import frappe
    
    # Add custom header
    frappe.local.response['http_headers'] = {
        'X-Custom-Header': 'value'
    }
    
    # Log response
    if frappe.local.response:
        status = frappe.local.response.get('http_status_code', 200)
        frappe.logger().debug(f"Response: {status}")
```

## Job Hooks

### before_job

Runs before background job executes.

```python
before_job = [
    "my_app.jobs.before_job"
]
```

**Use for:**
- Job initialization
- Context setup
- Logging job start

```python
def before_job():
    import frappe
    
    # Log job start
    job_name = frappe.local.job_name
    frappe.logger().info(f"Job started: {job_name}")
    
    # Setup context
    frappe.flags.in_background_job = True
```

### after_job

Runs after background job completes.

```python
after_job = [
    "my_app.jobs.after_job"
]
```

**Use for:**
- Cleanup
- Logging completion
- Releasing resources

```python
def after_job():
    import frappe
    
    # Log completion
    job_name = frappe.local.job_name
    frappe.logger().info(f"Job completed: {job_name}")
    
    # Cleanup
    cleanup_temp_files()
```

## Boot Info Hook

### extend_bootinfo

Add data to initial page load.

```python
extend_bootinfo = [
    "my_app.boot.extend_bootinfo"
]
```

**Function signature:**
```python
def extend_bootinfo(bootinfo):
    """
    Args:
        bootinfo: Dict containing boot data
    """
    import frappe
    
    # Add custom data
    bootinfo['custom_settings'] = frappe.db.get_single_value("My Settings", "value")
    bootinfo['user_preferences'] = get_user_preferences()
```

**Access in JavaScript:**
```javascript
// Access boot info
let custom_settings = frappe.boot.custom_settings;
```

## Examples

### API Key Authentication

```python
# hooks.py
before_request = ["my_app.auth.validate_api_request"]

# auth.py
def validate_api_request():
    import frappe
    
    # Check if API request
    if frappe.request.path.startswith("/api/"):
        api_key = frappe.get_request_header("X-API-Key")
        
        if not api_key:
            frappe.throw("API Key required", frappe.AuthenticationError)
        
        # Validate API key
        user = frappe.db.get_value("User API Key", 
            {"api_key": api_key}, 
            "user"
        )
        
        if not user:
            frappe.throw("Invalid API Key", frappe.AuthenticationError)
        
        # Set user session
        frappe.set_user(user)
```

### Request Logging

```python
def before_request():
    import frappe
    from frappe.utils import now_datetime
    
    # Log request details
    frappe.local.request_start_time = now_datetime()
    frappe.logger().info({
        "method": frappe.request.method,
        "path": frappe.request.path,
        "user": frappe.session.user,
        "ip": frappe.local.request_ip
    })

def after_request():
    import frappe
    from frappe.utils import now_datetime, time_diff_in_seconds
    
    if hasattr(frappe.local, 'request_start_time'):
        duration = time_diff_in_seconds(
            now_datetime(), 
            frappe.local.request_start_time
        )
        frappe.logger().info(f"Request took {duration}s")
```

### CORS Headers

```python
def after_request():
    import frappe
    
    # Add CORS headers
    frappe.local.response.setdefault('http_headers', {})
    frappe.local.response['http_headers'].update({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    })
```

### Job Monitoring

```python
def before_job():
    import frappe
    
    # Create job log entry
    frappe.get_doc({
        "doctype": "Job Log",
        "job_name": frappe.local.job_name,
        "status": "Running",
        "start_time": frappe.utils.now()
    }).insert(ignore_permissions=True)

def after_job():
    import frappe
    
    # Update job log
    job_name = frappe.local.job_name
    frappe.db.set_value("Job Log", 
        {"job_name": job_name, "status": "Running"},
        {
            "status": "Completed",
            "end_time": frappe.utils.now()
        }
    )
```

### Custom Boot Data

```python
def extend_bootinfo(bootinfo):
    import frappe
    
    # Add user's default values
    bootinfo['default_company'] = frappe.db.get_value("User", 
        frappe.session.user, 
        "default_company"
    )
    
    # Add system settings
    bootinfo['app_settings'] = {
        "currency": frappe.db.get_single_value("System Settings", "currency"),
        "date_format": frappe.db.get_single_value("System Settings", "date_format")
    }
    
    # Add cached data
    bootinfo['countries'] = frappe.get_all("Country", 
        fields=["name", "code"],
        limit=250
    )
```

## Best Practices

1. **Performance**: Keep hooks fast, they run on every request/job
2. **Error Handling**: Don't break requests with hook failures
3. **Logging**: Use appropriate log levels
4. **Security**: Validate and sanitize inputs
5. **Context**: Be aware of request/job context

### Safe Hook Implementation

```python
def before_request():
    try:
        # Your logic
        custom_logic()
    except Exception as e:
        # Log but don't break request
        frappe.log_error(f"Hook failed: {str(e)}")
```

## Notes

- Request hooks run for ALL HTTP requests
- Job hooks run for background jobs and scheduler tasks
- Hooks run in order of registration
- Errors in hooks can break requests/jobs
- Use `frappe.local` for request-specific data
- Changes require bench restart
