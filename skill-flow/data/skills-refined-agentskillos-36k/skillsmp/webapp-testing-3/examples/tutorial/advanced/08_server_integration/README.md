# Server Integration Testing

This example demonstrates how to test full-stack applications (frontend + backend) using Playwright with the `with_server.py` helper script.

## Overview

Testing applications with backend servers requires:
1. Starting the server before tests run
2. Waiting for the server to be ready
3. Running your tests
4. Stopping the server after tests complete

The `with_server.py` helper automates this entire lifecycle!

## Files

- `flask_app.py` - Simple Flask web server with HTML page and API
- `test_with_server.py` - Playwright tests for the Flask application
- `README.md` - This file

## Prerequisites

Install Flask:

```bash
pip install flask
```

Playwright should already be installed from the tutorial prerequisites.

## Running the Tests

### Option 1: Using the with_server.py Helper (Recommended)

The helper script automatically starts the server, waits for it to be ready, runs your tests, and stops the server:

```bash
# From this directory
python ../../../../scripts/with_server.py \
  --server "python flask_app.py" \
  --port 5000 \
  -- python test_with_server.py
```

That's it! The helper handles everything.

### Option 2: Manual Server Start

If you prefer to manually control the server:

**Terminal 1** - Start the server:
```bash
python flask_app.py
```

**Terminal 2** - Run the tests:
```bash
python test_with_server.py
```

Press `Ctrl+C` in Terminal 1 to stop the server when done.

## What Gets Tested

1. **Server Connectivity** - Verify the server is running and accessible
2. **Page Content** - Check that HTML is served correctly
3. **API Endpoints** - Test direct API calls (GET /api/status, GET /api/data)
4. **Frontend-Backend Integration** - Click button → API call → DOM update
5. **Console Monitoring** - Capture browser console logs during testing

## Understanding with_server.py

The helper script usage:

```bash
python scripts/with_server.py \
  --server "command to start server" \
  --port port_number \
  -- your_test_command
```

### Arguments:

- `--server`: Command to start your server (can be used multiple times for multiple servers)
- `--port`: Port number to poll for server readiness (can be used multiple times)
- `--`: Everything after this is your test command

### Multiple Servers Example:

```bash
python scripts/with_server.py \
  --server "cd backend && python api_server.py" --port 5000 \
  --server "cd frontend && npm run dev" --port 3000 \
  -- python test_integration.py
```

## How It Works

1. **with_server.py** starts the server process(es)
2. Polls the specified port(s) until the server responds (default 30s timeout)
3. Once ready, executes your test command
4. When tests finish, automatically terminates all server processes

## Troubleshooting

### Port Already in Use

```
Error: Address already in use
```

**Solution:** Stop any existing Flask servers:
```bash
# macOS/Linux
lsof -ti:5000 | xargs kill

# Windows
netstat -ano | findstr :5000
taskkill /PID <pid> /F
```

### Server Not Ready

```
Error: Server did not become ready within timeout
```

**Solutions:**
- Increase timeout: The helper has a 30s default timeout
- Check server logs for startup errors
- Verify the port number is correct
- Ensure Flask is installed: `pip install flask`

### Connection Refused

```
Error: Could not connect to server
```

**Solutions:**
- Make sure the server is running (check the other terminal)
- Verify you're using the correct port (5000)
- Check firewall settings

## Next Steps

After mastering this example:

1. **Try with your own backend** - Replace Flask with Django, FastAPI, Express, etc.
2. **Test multiple endpoints** - Add more API routes and test them
3. **Test authentication** - Add login flows and session management
4. **Test database operations** - Verify CRUD operations work correctly
5. **Test error handling** - Trigger errors and verify proper error messages

## Related Examples

- **05_dynamic_content** - Learn proper wait strategies for async operations
- **09_comprehensive** - See a complete test suite for a complex application

---

**Pro Tip:** In CI/CD environments, always use the `with_server.py` pattern to ensure clean server startup and shutdown. This prevents port conflicts and zombie processes!
