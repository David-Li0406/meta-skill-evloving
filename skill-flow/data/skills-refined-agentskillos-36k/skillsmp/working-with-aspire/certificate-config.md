# Certificate Configuration Reference

## Overview

Aspire 13.0 automatically configures HTTPS endpoints and certificate trust for resources, enabling secure communication during local development without manual certificate setup.

## Automatic Certificate Trust (13.0+)

Aspire automatically configures ASP.NET Development Certificate trust for Python, Node.js, and containerized applications:

```csharp
// No configuration needed - certificate trust is automatic
var pythonApi = builder.AddUvicornApp("api", "./api", "main:app");
var nodeApi = builder.AddJavaScriptApp("frontend", "./frontend");
var container = builder.AddContainer("service", "myimage");
```

**Automatic configuration by language:**

| Language | Environment Variables Set |
|----------|--------------------------|
| Python | `SSL_CERT_FILE`, `REQUESTS_CA_BUNDLE` |
| Node.js | `NODE_EXTRA_CA_CERTS` |
| Containers | Certificate bundles mounted, OpenSSL vars configured |

## Certificate Trust APIs

### Enable/Disable Per Resource

```csharp
var builder = DistributedApplication.CreateBuilder(args);

// Explicitly enable development certificate trust
var nodeApp = builder.AddNpmApp("frontend", "../frontend")
    .WithDeveloperCertificateTrust(trust: true);

// Disable development certificate trust
var pythonApp = builder.AddPythonApp("api", "../api", "main.py")
    .WithDeveloperCertificateTrust(trust: false);

builder.Build().Run();
```

### Global Configuration

Configure default behavior in `appsettings.json`:

```json
{
  "Aspire": {
    "Hosting": {
      "DeveloperCertificateTrust": {
        "Enabled": true
      }
    }
  }
}
```

Or in AppHost:

```csharp
builder.Configuration["Aspire:Hosting:DeveloperCertificateTrust:Enabled"] = "false";
```

## Custom Certificate Bundles

### Create Certificate Collection

```csharp
var builder = DistributedApplication.CreateBuilder(args);

// Create certificate bundle with custom certificates
var certs = builder.AddCertificateAuthorityCollection("custom-certs")
    .WithCertificatesFromFile("./certs/my-ca.pem")
    .WithCertificatesFromFile("./certs/another-ca.pem");

// Apply to resources
var api = builder.AddNodeApp("api", "../api", "index.js")
    .WithCertificateAuthorityCollection(certs);

builder.Build().Run();
```

### Apply to Resources

```csharp
var gateway = builder.AddYarp("gateway")
    .WithCertificateAuthorityCollection(certs)
    .WithDeveloperCertificateTrust(trust: true);
```

## Certificate Trust Scopes

Control how custom certificates interact with default trusted certificates:

### Available Scopes

| Scope | Behavior |
|-------|----------|
| `Append` | Add custom certs to default trusted certs |
| `Override` | Replace defaults with only custom certs |
| `System` | Combine custom + system root certs (default for Python) |
| `None` | Disable custom certificate trust |

### Configure Scope

```csharp
// Append mode - adds to existing trusted certs
builder.AddNodeApp("api", "../api", "index.js")
    .WithCertificateTrustScope(CertificateTrustScope.Append);

// Override mode - replaces all trusted certs
builder.AddContainer("service", "myimage")
    .WithCertificateTrustScope(CertificateTrustScope.Override);

// System mode - combines with system root certs (Python default)
builder.AddPythonApp("api", "../api", "main.py")
    .WithCertificateTrustScope(CertificateTrustScope.System);

// None mode - disable all custom trust
builder.AddProject<Projects.Api>("api")
    .WithCertificateTrustScope(CertificateTrustScope.None);
```

## HTTPS Endpoint Configuration

### Development Certificate for HTTPS

```csharp
// Configure HTTPS with development certificate
var api = builder.AddViteApp("frontend", "../frontend")
    .WithHttpsDeveloperCertificate();
```

### Custom Certificate Callback

```csharp
builder.AddContainer("api", "myimage")
    .WithCertificateTrustConfiguration(context =>
    {
        // Add custom environment variables
        context.EnvironmentVariables["MY_CERT_PATH"] = context.CertificateBundlePath;

        // Add command line arguments
        context.Arguments.Add("--ca-cert");
        context.Arguments.Add(context.CertificateBundlePath);
    });
```

### Callback Context Properties

| Property | Description |
|----------|-------------|
| `Scope` | The `CertificateTrustScope` for the resource |
| `Arguments` | Command line arguments list |
| `EnvironmentVariables` | Environment variables dictionary |
| `CertificateBundlePath` | Path to certificate bundle file |
| `CertificateDirectoriesPath` | Paths containing individual certs |

## Common Scenarios

### Service with HTTPS + Dashboard Telemetry

```csharp
var api = builder.AddUvicornApp("api", "../api", "main:app")
    .WithHttpsEndpoint(port: 8001, env: "HTTPS_PORT")
    .WithDeveloperCertificateTrust(trust: true);
```

### Container with Custom CA

```csharp
var certs = builder.AddCertificateAuthorityCollection("corporate-ca")
    .WithCertificatesFromFile("./certs/corporate-root.pem");

var service = builder.AddContainer("internal-service", "internal/service")
    .WithCertificateAuthorityCollection(certs)
    .WithCertificateTrustScope(CertificateTrustScope.System);
```

### Disable Certificate Config for Self-Managed Resource

```csharp
var legacy = builder.AddContainer("legacy", "legacy-service")
    .WithDeveloperCertificateTrust(trust: false)
    .WithCertificateTrustScope(CertificateTrustScope.None);
```

## Container HTTPS (13.1+)

Containers like YARP, Redis, Keycloak, and Uvicorn can serve HTTPS directly:

```csharp
// YARP with HTTPS
var gateway = builder.AddYarp("gateway")
    .WithHttpsDeveloperCertificate();

// Uvicorn with HTTPS
var api = builder.AddUvicornApp("api", "../api", "main:app")
    .WithHttpsDeveloperCertificate();
```

## Limitations

- Certificate configuration only supported in **run mode** (not publish mode)
- Not all languages support all trust scope modes
- Python doesn't support `Append` mode natively (uses `System` by default)
- .NET on Windows uses `None` by default (no way to change system store)
- HTTPS endpoint APIs are experimental (`ASPIRECERTIFICATES001`)

## Troubleshooting

### Python SSL Errors

Python uses `System` scope by default. If SSL errors occur:

```csharp
// Explicitly configure Python certificate trust
builder.AddPythonApp("api", "../api", "main.py")
    .WithCertificateTrustScope(CertificateTrustScope.System)
    .WithDeveloperCertificateTrust(trust: true);
```

### Container SSL Errors

Check that certificate bundle is mounted correctly:

```csharp
builder.AddContainer("service", "myimage")
    .WithCertificateTrustConfiguration(context =>
    {
        // Log what's being configured
        Console.WriteLine($"Bundle: {context.CertificateBundlePath}");
        foreach (var env in context.EnvironmentVariables)
        {
            Console.WriteLine($"{env.Key}={env.Value}");
        }
    });
```

### Node.js Certificate Issues

Ensure `NODE_EXTRA_CA_CERTS` is being set:

```csharp
builder.AddJavaScriptApp("frontend", "../frontend")
    .WithDeveloperCertificateTrust(trust: true)
    .WithEnvironment(ctx =>
    {
        // Verify NODE_EXTRA_CA_CERTS is set
        if (ctx.EnvironmentVariables.TryGetValue("NODE_EXTRA_CA_CERTS", out var path))
        {
            Console.WriteLine($"Node CA certs: {path}");
        }
    });
```
