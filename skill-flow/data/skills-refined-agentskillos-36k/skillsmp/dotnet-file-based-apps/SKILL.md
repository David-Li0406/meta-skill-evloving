---
name: dotnet-file-based-apps
description: Creates .NET file-based apps from single C# files. Use when building scripts, utilities, or small applications without project files.
---

# .NET File-Based Apps

File-based apps let you build, run, and publish .NET applications from a single C# file without a `.csproj`. Requires .NET 10 SDK or later.

## Quick Start

Create a single `.cs` file with directives at the top:

```csharp
#:package Spectre.Console@*

using Spectre.Console;

AnsiConsole.MarkupLine("[green]Hello, World![/]");
```

Run it:

```bash
dotnet run file.cs
# or shorthand:
dotnet file.cs
```

## Directives

Place at the top of your C# file, prefixed with `#:`:

| Directive | Purpose | Example |
|-----------|---------|---------|
| `#:package` | Add NuGet package | `#:package Newtonsoft.Json@13.0.3` |
| `#:project` | Reference another project | `#:project ../Shared/Shared.csproj` |
| `#:property` | Set MSBuild property | `#:property TargetFramework=net10.0` |
| `#:sdk` | Specify SDK (default: `Microsoft.NET.Sdk`) | `#:sdk Microsoft.NET.Sdk.Web` |

**Package versions**: Always specify version (`@3.1.1`) or use `@*` for latest. Omitting version only works with central package management.

## CLI Commands

```bash
dotnet run file.cs              # Run
dotnet run file.cs -- arg1 arg2 # Run with arguments
dotnet build file.cs            # Build
dotnet publish file.cs          # Publish (AOT by default)
dotnet pack file.cs             # Package as .NET tool
dotnet clean file.cs            # Clean build outputs
dotnet restore file.cs          # Restore packages
dotnet project convert file.cs  # Convert to traditional project
```

## Native AOT

**Enabled by default.** File-based apps produce optimized, self-contained executables with native AOT. This means:

- Faster startup and smaller memory footprint
- All code must be AOT-compatible (no reflection-based serialization, etc.)
- Use source generators for JSON serialization (see examples below)

To disable:

```csharp
#:property PublishAot=false
```

## Shell Execution (Unix)

Add shebang and make executable:

```csharp
#!/usr/bin/env dotnet
#:package Spectre.Console@*

using Spectre.Console;
AnsiConsole.MarkupLine("[green]Hello![/]");
```

```bash
chmod +x file.cs
./file.cs
```

## Launch Profiles

Create `[filename].run.json` alongside your `.cs` file:

```json
{
  "profiles": {
    "dev": {
      "commandName": "Project",
      "environmentVariables": {
        "ASPNETCORE_ENVIRONMENT": "Development"
      }
    }
  }
}
```

Run with profile: `dotnet run app.cs --launch-profile dev`

## User Secrets

```bash
dotnet user-secrets set "ApiKey" "secret-value" --project file.cs
```

## Pipe from stdin

```bash
echo 'Console.WriteLine("Hello");' | dotnet run -
```

## Folder Layout

**Avoid** placing file-based apps inside traditional project directories:

```
# ❌ Bad - inside project cone
MyProject/
├── MyProject.csproj
└── scripts/
    └── utility.cs

# ✅ Good - separate directory
MyProject/
├── MyProject.csproj
└── Program.cs
scripts/
└── utility.cs
```

## Implicit Build Files

These files in parent directories affect file-based apps:

- `Directory.Build.props` - MSBuild properties
- `Directory.Build.targets` - Build targets
- `Directory.Packages.props` - Central package management
- `nuget.config` - Package sources
- `global.json` - SDK version

Create isolated `Directory.Build.props` in script directories if needed.

## Workflow

- [ ] Create `.cs` file with directives at top
- [ ] Add package references with explicit versions
- [ ] Test with `dotnet run file.cs`
- [ ] Publish with `dotnet publish file.cs`

## Common Examples

### Web API

```csharp
#:sdk Microsoft.NET.Sdk.Web

var app = WebApplication.Create();
app.MapGet("/", () => "Hello!");
app.Run();
```

### CLI with Arguments

```csharp
#:package System.CommandLine@*

using System.CommandLine;

var nameOption = new Option<string>("--name", "Your name");
var rootCommand = new RootCommand { nameOption };
rootCommand.SetHandler(name => Console.WriteLine($"Hello, {name}!"), nameOption);
return await rootCommand.InvokeAsync(args);
```

### JSON Processing

Always use System.Text.Json for JSON operations.

```csharp
using System.Text.Json;
using System.Text.Json.Serialization;

var data = new { Name = "Test", Value = 42 };
Console.WriteLine(JsonSerializer.Serialize(data, AppJsonContext.Default.Object));

// Source generator for AOT compatibility
[JsonSerializable(typeof(object))]
partial class AppJsonContext : JsonSerializerContext { }
```

### Run Shell Commands

Use the CliWrap package to easily run shell commands.

```csharp
#:package CliWrap@*

using CliWrap;
using CliWrap.Buffered;

var result = await Cli.Wrap("git")
    .WithArguments(["status", "--short"])
    .WithWorkingDirectory(Environment.CurrentDirectory)
    .ExecuteBufferedAsync();

Console.WriteLine(result.StandardOutput);
```
