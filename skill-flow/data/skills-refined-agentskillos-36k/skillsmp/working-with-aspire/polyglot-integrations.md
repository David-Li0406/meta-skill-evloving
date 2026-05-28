# Polyglot Integrations Reference

## Quick Reference

| Language/Runtime | Package | Add Method |
|-----------------|---------|------------|
| JavaScript (Generic) | `Aspire.Hosting.JavaScript` | `AddJavaScriptApp()` |
| Node.js | `Aspire.Hosting.JavaScript` | `AddNodeApp()` |
| Vite | `Aspire.Hosting.JavaScript` | `AddViteApp()` |
| Angular | `Aspire.Hosting.JavaScript` | `AddAngularApp()` |
| Python | `Aspire.Hosting.Python` | `AddPythonProject()` |
| Uvicorn | `Aspire.Hosting.Python` | `AddUvicornApp()` |
| Go | `CommunityToolkit.Aspire.Hosting.Golang` | `AddGolangApp()` |
| Rust | `CommunityToolkit.Aspire.Hosting.Rust` | `AddRustApp()` |
| Java/Spring | `CommunityToolkit.Aspire.Hosting.Java` | `AddSpringApp()` |
| Deno | `CommunityToolkit.Aspire.Hosting.Deno` | `AddDenoApp()` |

## JavaScript/Node.js (13.0+)

### Package
```bash
# Aspire 13.0 renamed NodeJs to JavaScript
dotnet add package Aspire.Hosting.JavaScript
```

### AddJavaScriptApp (Recommended)

The foundational method for all JavaScript applications:

```csharp
var builder = DistributedApplication.CreateBuilder(args);

var api = builder.AddProject<Projects.Api>("api");

// Basic usage - runs "npm run dev" by default
var frontend = builder.AddJavaScriptApp("frontend", "./frontend")
    .WithHttpEndpoint(port: 3000, env: "PORT")
    .WithReference(api);

builder.Build().Run();
```

**Default behavior:**
- Uses npm as package manager (detects from `package.json`)
- Runs "dev" script during local development
- Runs "build" script when publishing
- Automatically generates Dockerfiles for production

### Package Manager Configuration

```csharp
// npm (default)
var app = builder.AddJavaScriptApp("app", "./app");

// npm with custom flags
var npmApp = builder.AddJavaScriptApp("app", "./app")
    .WithNpm(installCommand: "ci", installArgs: ["--legacy-peer-deps"]);

// Yarn
var yarnApp = builder.AddJavaScriptApp("app", "./app")
    .WithYarn();

// Yarn with flags
var yarnCustom = builder.AddJavaScriptApp("app", "./app")
    .WithYarn(installArgs: ["--immutable"]);

// pnpm
var pnpmApp = builder.AddJavaScriptApp("app", "./app")
    .WithPnpm();

// pnpm with flags
var pnpmCustom = builder.AddJavaScriptApp("app", "./app")
    .WithPnpm(installArgs: ["--frozen-lockfile"]);
```

**Production lockfile behavior:**
- **npm**: Uses `npm ci` if `package-lock.json` exists
- **yarn v2+**: Uses `yarn install --immutable` if `yarn.lock` exists
- **yarn v1**: Uses `yarn install --frozen-lockfile`
- **pnpm**: Uses `pnpm install --frozen-lockfile` if `pnpm-lock.yaml` exists

### Script Configuration

```csharp
// Customize scripts
var app = builder.AddJavaScriptApp("app", "./app")
    .WithRunScript("start")      // Run "npm run start" during dev (default: "dev")
    .WithBuildScript("prod");    // Run "npm run prod" when publishing (default: "build")
```

### Passing Arguments to Scripts

**Option 1: WithArgs**
```csharp
builder.AddJavaScriptApp("frontend", "./frontend")
    .WithRunScript("dev")
    .WithArgs("--port", "3000", "--host");
```

**Option 2: package.json custom scripts**
```json
{
  "scripts": {
    "dev": "vite",
    "dev:custom": "vite --port 3000 --host"
  }
}
```

```csharp
builder.AddJavaScriptApp("frontend", "./frontend")
    .WithRunScript("dev:custom");
```

### AddViteApp (Vite Projects)

Optimized for Vite-based applications (React, Vue, Svelte):

```csharp
var frontend = builder.AddViteApp("frontend", "./frontend")
    .WithHttpEndpoint(env: "PORT")
    .WithExternalHttpEndpoints()
    .WithReference(api);
```

**Vite-specific features:**
- Automatic browser opening support
- Hot module replacement (HMR) configuration
- Vite environment variable injection
- Development/production mode detection

### AddNodeApp (Node.js Scripts)

Run a Node.js script directly:

```csharp
builder.AddNodeApp("api", "../node-app", "index.js")
    .WithHttpEndpoint(port: 3000, env: "PORT")
    .WithExternalHttpEndpoints();
```

### AddAngularApp

```csharp
builder.AddAngularApp("frontend", "../angular-app")
    .WithHttpEndpoint(env: "PORT")
    .WithExternalHttpEndpoints();
```

### Dynamic Dockerfile Generation

JavaScript apps automatically generate production Dockerfiles:

```csharp
var app = builder.AddJavaScriptApp("app", "./app");
// Dockerfile generated automatically when publishing
```

**Generated Dockerfile features:**
- Detects Node.js version from `.nvmrc`, `.node-version`, `package.json`, or `.tool-versions`
- Uses multi-stage builds for smaller images
- Installs dependencies in separate layer for caching
- Runs build script to create production assets
- Defaults to `node:22-slim` if no version specified

### Environment Variables in JavaScript

```javascript
// Access Aspire-injected variables
const apiUrl = process.env.services__api__http__0;
const dbConn = process.env.ConnectionStrings__db;
const port = process.env.PORT || 3000;

app.listen(port, () => {
    console.log(`Listening on port ${port}`);
});
```

## Python

### Package
```bash
dotnet add package Aspire.Hosting.Python
```

### Which Method to Use?

| Framework | Method | Why |
|-----------|--------|-----|
| **FastAPI** | `AddUvicornApp` | FastAPI is ASGI, needs Uvicorn |
| **Starlette** | `AddUvicornApp` | ASGI framework |
| **Flask** | `AddUvicornApp` | Modern deployment uses Uvicorn |
| **Scripts (no web)** | `AddPythonProject` | Standalone Python scripts |
| **CLI tools** | `AddPythonProject` | Non-web Python apps |

> **IMPORTANT:** The method is `AddUvicornApp`, NOT `AddPythonUvicornApp`. There is no `AddPythonUvicornApp` method.

### AddUvicornApp (FastAPI, Starlette, Flask)
```csharp
// For ASGI/WSGI web apps - THIS IS THE CORRECT METHOD
builder.AddUvicornApp("api", "../fastapi-app", "main:app")
    .WithHttpEndpoint(port: 8000, env: "PORT")
    .WithExternalHttpEndpoints();
```

### AddPythonProject (Scripts, CLI tools)
```csharp
// ONLY for non-web Python scripts
builder.AddPythonProject("worker", "../python-worker", "main.py")
    .WithEnvironment("SOME_VAR", "value");
```

### Package Management

```csharp
// Use existing venv
builder.AddPythonProject("api", "../python-api", "main.py")
    .WithVirtualEnvironment("../python-api/.venv");

// Or create venv and install requirements
builder.AddPythonProject("api", "../python-api", "main.py")
    .WithPipPackageInstallation();
```

**Supported package managers:**
- `pip` (default)
- `uv` (faster alternative)
- `venv`

### Automatic Dockerfile Generation

Python apps also generate production-ready Dockerfiles:

```csharp
var api = builder.AddUvicornApp("api", "../api", "main:app");
// Dockerfile generated with uvicorn configuration
```

### Environment Variables in Python
```python
import os

# Access Aspire-injected variables
api_url = os.getenv("services__api__http__0")
db_conn = os.getenv("ConnectionStrings__db")
port = int(os.getenv("PORT", "8000"))
```

### Python Debugging (VS Code)

Python resources support debugging automatically:
- Set breakpoints in VS Code
- Run with Aspire debugger
- Breakpoints hit in Python code

## Go

### Package (Community Toolkit)
```bash
dotnet add package CommunityToolkit.Aspire.Hosting.Golang
```

### Go App
```csharp
builder.AddGolangApp("api", "../go-app")
    .WithHttpEndpoint(port: 8080, env: "PORT")
    .WithExternalHttpEndpoints();
```

### Go Code
```go
package main

import (
    "fmt"
    "net/http"
    "os"
)

func main() {
    port := os.Getenv("PORT")
    if port == "" {
        port = "8080"
    }

    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "Hello from Go!")
    })

    http.ListenAndServe(":"+port, nil)
}
```

## Rust

### Package (Community Toolkit)
```bash
dotnet add package CommunityToolkit.Aspire.Hosting.Rust
```

### Rust App
```csharp
builder.AddRustApp("api", "../rust-app", "my-crate")
    .WithHttpEndpoint(port: 8080, env: "PORT")
    .WithExternalHttpEndpoints();
```

## Java/Spring Boot

### Package (Community Toolkit)
```bash
dotnet add package CommunityToolkit.Aspire.Hosting.Java
```

### Spring Boot App
```csharp
// Requires OpenTelemetry Java agent
builder.AddSpringApp("api", "../spring-app",
    "../agents/opentelemetry-javaagent.jar")
    .WithHttpEndpoint(port: 8080)
    .WithExternalHttpEndpoints();
```

## Deno

### Package (Community Toolkit)
```bash
dotnet add package CommunityToolkit.Aspire.Hosting.Deno
```

### Deno App
```csharp
builder.AddDenoApp("api", "../deno-app", "main.ts",
    ["--allow-net", "--allow-env"])
    .WithHttpEndpoint(port: 8000, env: "PORT")
    .WithExternalHttpEndpoints();
```

## Containers (Any Language)

### Generic Container
```csharp
builder.AddContainer("api", "my-image:latest")
    .WithHttpEndpoint(port: 8080, targetPort: 80)
    .WithEnvironment("CONFIG_KEY", "value");
```

### Dockerfile Build
```csharp
builder.AddDockerfile("api", "../app")
    .WithHttpEndpoint(port: 8080, targetPort: 80)
    .WithBuildArg("BUILD_ENV", "production");
```

## Common Patterns

### Reference Backend from Frontend
```csharp
var api = builder.AddProject<Projects.Api>("api");

builder.AddViteApp("frontend", "../frontend")
    .WithReference(api)  // Injects API URL as env var
    .WithExternalHttpEndpoints();
```

### Pass Database to Polyglot App
```csharp
var db = builder.AddPostgres("db").AddDatabase("mydb");

builder.AddPythonProject("api", "../python-api", "main.py")
    .WithReference(db)  // Injects ConnectionStrings__mydb
    .WaitFor(db);
```

### External HTTP Endpoints
```csharp
// Required for dashboard to show clickable URLs
builder.AddNodeApp("api", "../app", "index.js")
    .WithExternalHttpEndpoints();
```

### Port Configuration
```csharp
// Random port (recommended for services)
.WithHttpEndpoint(env: "PORT")

// Fixed port (for frontends)
.WithHttpEndpoint(port: 3000, env: "PORT")

// Container port mapping
.WithHttpEndpoint(port: 8080, targetPort: 80)
```

## Service Discovery

Aspire injects service URLs as environment variables:

| Pattern | Variable |
|---------|----------|
| `services__<name>__<scheme>__<index>` | Full URL |
| `ConnectionStrings__<name>` | Connection string |

Example for frontend referencing API:
```javascript
// In Node.js/JavaScript
const apiUrl = process.env.services__api__http__0;
// Result: "http://localhost:5001"
```

```python
# In Python
api_url = os.getenv("services__api__http__0")
# Result: "http://localhost:5001"
```

## Certificate Trust (13.0+)

Polyglot apps automatically trust development certificates:

```csharp
// Automatic - no configuration needed
var pythonApi = builder.AddUvicornApp("api", "./api", "main:app");
var nodeApi = builder.AddJavaScriptApp("frontend", "./frontend");
```

See `certificate-config.md` for advanced certificate configuration.

## Migration from AddNpmApp (9.x)

```csharp
// Before (9.x) - REMOVED
builder.AddNpmApp("frontend", "../app", "dev", args: ["--no-open"]);

// After (13.0)
builder.AddJavaScriptApp("frontend", "../app")
    .WithRunScript("dev")
    .WithArgs("--no-open");
```
