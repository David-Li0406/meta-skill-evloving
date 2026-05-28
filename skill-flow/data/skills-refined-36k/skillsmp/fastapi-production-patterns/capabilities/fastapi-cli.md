# FastAPI CLI

## Overview
The FastAPI CLI (introduced in FastAPI 0.100+) provides a streamlined way to run FastAPI applications in development and production, replacing manual uvicorn commands with a more intuitive interface.

## Installation

The FastAPI CLI is included when you install FastAPI with the `standard` extras:

```bash
uv add "fastapi[standard]"
```

This includes:
- `fastapi` - The core framework
- `uvicorn[standard]` - The ASGI server with high-performance dependencies
- `fastapi-cli[standard]` - The CLI tool (including fastapi-cloud-cli for deployment)
- `httpx` - For testing
- `jinja2` - For templates
- `python-multipart` - For form data parsing

## CLI Commands

### Development: `fastapi dev`

Run your application in development mode with auto-reload:

```bash
fastapi dev main.py
```

**Features:**
- Auto-reload on file changes
- Detailed error messages
- Debug mode enabled
- Runs on http://127.0.0.1:8000 by default

**Example output:**
```
 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/user/code/awesomeapp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2248755] using WatchFiles
INFO:     Started server process [2248757]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Custom host and port:**
```bash
fastapi dev main.py --host 0.0.0.0 --port 8080
```

### Production: `fastapi run`

Run your application in production mode:

```bash
fastapi run main.py
```

**Features:**
- No auto-reload (better performance)
- Optimized for production
- Runs on http://127.0.0.1:8000 by default

**Custom host and port:**
```bash
fastapi run main.py --host 0.0.0.0 --port 8080
```

**Number of workers:**
```bash
fastapi run main.py --workers 4
```

## Comparison: Old vs New

| Old Method (Uvicorn) | New Method (FastAPI CLI) |
|---------------------|-------------------------|
| `uvicorn main:app --reload` | `fastapi dev main.py` |
| `uvicorn main:app` | `fastapi run main.py` |
| `uvicorn main:app --host 0.0.0.0 --port 8080` | `fastapi dev main.py --host 0.0.0.0 --port 8080` |
| Manual dependency management | `uv add "fastapi[standard]"` |

## Quick Reference

| Command | Purpose | Mode |
|---------|---------|------|
| `fastapi dev main.py` | Development server with auto-reload | Development |
| `fastapi run main.py` | Production server | Production |
| `fastapi dev main.py --port 8080` | Custom port | Development |
| `fastapi run main.py --workers 4` | Multiple workers | Production |

## FastAPI Cloud (Optional)

FastAPI Cloud is a deployment service built by the FastAPI team for one-command deployment.

**Login:**
```bash
fastapi login
```

**Deploy:**
```bash
fastapi deploy
```

This deploys your application to FastAPI Cloud and provides a public URL.

> **Note:** FastAPI Cloud is optional. You can deploy FastAPI apps to any cloud provider (AWS, GCP, Azure, Railway, Render, etc.) using traditional deployment methods.

## Common Patterns

### Development Workflow

1. **Install dependencies:**
   ```bash
   uv add "fastapi[standard]"
   ```

2. **Create your app** (main.py):
   ```python
   from fastapi import FastAPI

   app = FastAPI()

   @app.get("/")
   async def root():
       return {"message": "Hello World"}
   ```

3. **Run in development:**
   ```bash
   fastapi dev main.py
   ```

4. **Test at http://127.0.0.1:8000/docs**

### Production Deployment

**Option 1: Using the CLI directly**
```bash
fastapi run main.py --host 0.0.0.0 --port 8000 --workers 4
```

**Option 2: Using gunicorn with uvicorn workers** (recommended for production)
```bash
uv add gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

**Option 3: FastAPI Cloud**
```bash
fastapi login
fastapi deploy
```

## Best Practices

1. **Use `fastapi dev` for development** - Auto-reload saves time
2. **Use `fastapi run` for simple production deployments** - Good for small apps
3. **Use gunicorn + uvicorn workers for production** - Better process management
4. **Set appropriate worker counts** - Typically 2-4 workers per CPU core
5. **Use environment variables** - Don't hardcode hosts and ports

## Troubleshooting

**"fastapi: command not found"**
- Ensure you installed with `uv add "fastapi[standard]"`
- Check your virtual environment is activated

**Port already in use**
- Use `--port` flag to specify a different port
- Check what's using the port: `lsof -i :8000` (macOS/Linux)

**Auto-reload not working**
- Ensure you're using `fastapi dev`, not `fastapi run`
- Check file permissions

**Workers not spawning**
- Ensure you're using `fastapi run`, not `fastapi dev`
- Check system resources

## See Also

- [Async Testing Capability](async-testing.md)
- [Database Lifecycle Management](database-lifecycle-management.md)
- [Integration Guide](../integration.md)
