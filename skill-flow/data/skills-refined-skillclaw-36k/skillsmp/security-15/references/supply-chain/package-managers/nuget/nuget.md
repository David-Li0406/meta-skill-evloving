# NuGet Package Manager

**Ecosystem**: .NET (C#, F#, VB.NET)
**Package Registry**: https://api.nuget.org/v3/index.json
**Documentation**: https://docs.microsoft.com/nuget/

---

## TIER 1: Manifest Detection

### Manifest Files

| File | Required | Description |
|------|----------|-------------|
| `*.csproj` | Yes* | C# project file |
| `*.fsproj` | Yes* | F# project file |
| `*.vbproj` | Yes* | VB.NET project file |
| `packages.config` | Legacy | Legacy package references |
| `nuget.config` | No | NuGet configuration |
| `Directory.Packages.props` | No | Central Package Management |

*One project file is required

### Project File Detection

**Pattern**: `\.(cs|fs|vb)proj$`
**Confidence**: 98% (HIGH)

### SDK-Style Project (Modern)

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Newtonsoft.Json" Version="13.0.3" />
    <PackageReference Include="Microsoft.Extensions.Logging" Version="8.0.0" />
  </ItemGroup>

  <ItemGroup Condition="'$(Configuration)' == 'Debug'">
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
  </ItemGroup>
</Project>
```

### Legacy packages.config

```xml
<?xml version="1.0" encoding="utf-8"?>
<packages>
  <package id="Newtonsoft.Json" version="13.0.3" targetFramework="net48" />
  <package id="log4net" version="2.0.15" targetFramework="net48" />
</packages>
```

### Dependency Types

| Element | Included in SBOM | Notes |
|---------|------------------|-------|
| `PackageReference` | Yes (always) | Direct dependencies |
| `ProjectReference` | Metadata | Project references |
| Transitive | Yes | Resolved transitively |
| `PrivateAssets="all"` | Configurable | Development-only |

---

## TIER 2: Lock File Detection

### Lock Files

| File | Format | Version |
|------|--------|---------|
| `packages.lock.json` | JSON | NuGet 4.9+ |

**Pattern**: `packages\.lock\.json$`
**Confidence**: 98% (HIGH)

### Enabling Lock Files

```xml
<!-- In .csproj or Directory.Build.props -->
<PropertyGroup>
  <RestorePackagesWithLockFile>true</RestorePackagesWithLockFile>
  <RestoreLockedMode>true</RestoreLockedMode>
</PropertyGroup>
```

### Lock File Structure

```json
{
  "version": 1,
  "dependencies": {
    "net8.0": {
      "Newtonsoft.Json": {
        "type": "Direct",
        "requested": "[13.0.3, )",
        "resolved": "13.0.3",
        "contentHash": "HrC5BXdl00IP9zeV+0Z848QWPAoCr9P3bDEZguI+gkLcBKAOxix/tLEAAHC+UvDNPv4a2d18lOReHMOagPa+zQ=="
      },
      "Microsoft.CSharp": {
        "type": "Transitive",
        "resolved": "4.7.0",
        "contentHash": "pTj+D3uJWyN3My70i2Hqo+OXixq3Os2D1nJ2x92FFo6sk8fYS1m1WLNTs0Dc1uPaViH0YvEEwvzddQ7y4rhXmA=="
      }
    }
  }
}
```

### Key Lock File Fields

| Field | SBOM Use |
|-------|----------|
| `resolved` | Exact version |
| `contentHash` | SHA-512 hash |
| `type` | Direct or Transitive |
| `requested` | Version constraint |
| `dependencies` | Package dependencies |

---

## TIER 3: Configuration Extraction

### Registry Configuration

**File**: `nuget.config`

**Locations**:
- Project: `./nuget.config`
- User: `%APPDATA%\NuGet\NuGet.Config` (Windows)
- User: `~/.nuget/NuGet/NuGet.Config` (Linux/macOS)
- Machine: `%ProgramFiles(x86)%\NuGet\Config\` (Windows)

**Pattern**: `<add key="[^"]+" value="([^"]+)"`

### Common Configuration

```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <packageSources>
    <clear />
    <add key="nuget.org" value="https://api.nuget.org/v3/index.json" protocolVersion="3" />
    <add key="MyCompany" value="https://nuget.mycompany.com/v3/index.json" />
  </packageSources>

  <packageSourceCredentials>
    <MyCompany>
      <add key="Username" value="user" />
      <add key="ClearTextPassword" value="%NUGET_PASSWORD%" />
    </MyCompany>
  </packageSourceCredentials>

  <packageSourceMapping>
    <packageSource key="nuget.org">
      <package pattern="*" />
    </packageSource>
    <packageSource key="MyCompany">
      <package pattern="MyCompany.*" />
    </packageSource>
  </packageSourceMapping>
</configuration>
```

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `NUGET_PACKAGES` | Global packages folder |
| `NUGET_HTTP_CACHE_PATH` | HTTP cache path |
| `NUGET_PLUGIN_PATHS` | Plugin directories |
| `NUGET_CREDENTIAL_PROVIDER_*` | Credential providers |

---

## SBOM Generation

### Using CycloneDX .NET Tool

```bash
# Install globally
dotnet tool install --global CycloneDX

# Generate SBOM
dotnet CycloneDX <path-to-project-or-solution> -o sbom.json

# Exclude dev dependencies
dotnet CycloneDX <path> -o sbom.json --exclude-dev

# Specific format
dotnet CycloneDX <path> -o sbom.json -j -sv 1.5
```

### Using cdxgen

```bash
# Install cdxgen
npm install -g @cyclonedx/cdxgen

# Generate SBOM
cdxgen -o sbom.json

# Specify project type
cdxgen --project-type dotnet -o sbom.json
```

### Using cdxgen (alternative)

```bash
# Generate from directory
cdxgen -o sbom.json

# Specify type
cdxgen -t dotnet -o sbom.json
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `-j, --json` | Output as JSON | XML |
| `-sv, --schema-version` | CycloneDX version | 1.5 |
| `-exc, --exclude-dev` | Exclude dev dependencies | Include |
| `-rs, --recursive` | Recursive scan | false |

---

## Cache Locations

| Platform | Path |
|----------|------|
| Windows | `%USERPROFILE%\.nuget\packages\` |
| Linux/macOS | `~/.nuget/packages/` |
| HTTP Cache | `%LOCALAPPDATA%\NuGet\v3-cache` |

```bash
# Find packages folder
dotnet nuget locals global-packages --list

# Clear all caches
dotnet nuget locals all --clear

# Show all cache locations
dotnet nuget locals all --list
```

---

## Best Practices

1. **Enable lock files** with `RestorePackagesWithLockFile`
2. **Use Central Package Management** for large solutions
3. **Use `--locked-mode`** in CI/CD
4. **Configure package source mapping** for security
5. **Run `dotnet list package --vulnerable`** for vulnerability scanning
6. **Sign packages** with NuGet package signing

### Central Package Management

```xml
<!-- Directory.Packages.props -->
<Project>
  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
  </PropertyGroup>

  <ItemGroup>
    <PackageVersion Include="Newtonsoft.Json" Version="13.0.3" />
    <PackageVersion Include="Microsoft.Extensions.Logging" Version="8.0.0" />
  </ItemGroup>
</Project>
```

```xml
<!-- In .csproj - no version needed -->
<ItemGroup>
  <PackageReference Include="Newtonsoft.Json" />
</ItemGroup>
```

### Locked Mode in CI/CD

```bash
# Restore with locked mode
dotnet restore --locked-mode

# If lock file is stale, regenerate
dotnet restore --force-evaluate
```

---

## Troubleshooting

### Missing Lock File
```bash
# Generate lock file
dotnet restore --use-lock-file
```

### Lock File Out of Sync
```bash
# Force regenerate
dotnet restore --force-evaluate

# Or delete and regenerate
rm packages.lock.json
dotnet restore --use-lock-file
```

### Version Conflicts
```bash
# Show dependency graph
dotnet list package --include-transitive

# Show outdated packages
dotnet list package --outdated

# Show vulnerable packages
dotnet list package --vulnerable
```

### Private Feed Issues
```xml
<!-- nuget.config -->
<packageSourceCredentials>
  <MyFeed>
    <add key="Username" value="user" />
    <add key="ClearTextPassword" value="password" />
  </MyFeed>
</packageSourceCredentials>
```

### Package Source Mapping

```xml
<!-- Prevent dependency confusion attacks -->
<packageSourceMapping>
  <packageSource key="nuget.org">
    <package pattern="*" />
  </packageSource>
  <packageSource key="private">
    <package pattern="MyCompany.*" />
  </packageSource>
</packageSourceMapping>
```

---

## Security Scanning

### Built-in Vulnerability Check

```bash
# Check for vulnerable packages
dotnet list package --vulnerable

# Include transitive dependencies
dotnet list package --vulnerable --include-transitive

# Specific frameworks
dotnet list package --vulnerable --framework net8.0
```

### NuGet Package Signing

```bash
# Sign a package
dotnet nuget sign MyPackage.1.0.0.nupkg --certificate-path cert.pfx

# Verify signatures
dotnet nuget verify MyPackage.1.0.0.nupkg
```

---

## Solution-Level Patterns

For solutions with multiple projects:

```
MySolution/
├── MySolution.sln
├── Directory.Build.props          # Shared properties
├── Directory.Packages.props       # Central package versions
├── nuget.config                   # NuGet configuration
├── src/
│   ├── Project1/
│   │   ├── Project1.csproj
│   │   └── packages.lock.json
│   └── Project2/
│       ├── Project2.csproj
│       └── packages.lock.json
```

**SBOM Options**:
- Generate for entire solution
- Generate per project
- Aggregate multiple SBOMs

```bash
# Solution-level SBOM
dotnet CycloneDX MySolution.sln -o sbom.json

# Project-level SBOM
dotnet CycloneDX src/Project1/Project1.csproj -o project1-sbom.json
```

---

## Best Practices Detection

### NuGet Lock File Present
**Pattern**: `packages\.lock\.json`
**Type**: regex
**Severity**: info
**Languages**: [json]
**Context**: lock file
- Lock file ensures reproducible builds
- Enables deterministic restore

### Central Package Management
**Pattern**: `Directory\.Packages\.props`
**Type**: regex
**Severity**: info
**Languages**: [xml]
**Context**: solution root
- Centralized version management
- Modern .NET best practice

### Target Framework Specified
**Pattern**: `<TargetFramework>net[0-9]+\.[0-9]+</TargetFramework>`
**Type**: regex
**Severity**: info
**Languages**: [xml]
**Context**: .csproj
- Target framework explicitly set
- Best practice for compatibility

### RestorePackagesWithLockFile Enabled
**Pattern**: `<RestorePackagesWithLockFile>true</RestorePackagesWithLockFile>`
**Type**: regex
**Severity**: info
**Languages**: [xml]
**Context**: .csproj
- Lock file generation enabled
- Reproducible builds

---

## Anti-Patterns Detection

### HTTP Package Source
**Pattern**: `<add\s+key=['\"][^'\"]+['\"]\s+value=['\"]http://(?!localhost)`
**Type**: regex
**Severity**: critical
**Languages**: [xml]
**Context**: nuget.config
- Non-HTTPS package source
- CWE-319: Cleartext Transmission

### Floating Version (Asterisk)
**Pattern**: `Version=['\"][0-9]*\.\*['\"]`
**Type**: regex
**Severity**: high
**Languages**: [xml]
**Context**: .csproj
- Floating version constraint
- CWE-829: Non-deterministic dependency

### Latest Version Reference
**Pattern**: `Version=['\"]latest['\"]`
**Type**: regex
**Severity**: high
**Languages**: [xml]
**Context**: .csproj
- Latest version reference
- CWE-829: Unpinned dependency

### Legacy packages.config
**Pattern**: `packages\.config`
**Type**: regex
**Severity**: medium
**Languages**: [xml]
**Context**: project directory
- Legacy package reference format
- Should migrate to PackageReference

### Missing Package Version
**Pattern**: `<PackageReference\s+Include=['\"][^'\"]+['\"]\s*/>`
**Type**: regex
**Severity**: medium
**Languages**: [xml]
**Context**: .csproj
- PackageReference without version
- CWE-829: Version not specified

### Disabled Package Restore
**Pattern**: `<RestorePackages>false</RestorePackages>`
**Type**: regex
**Severity**: medium
**Languages**: [xml]
**Context**: .csproj
- Package restore disabled
- May cause build inconsistencies

---

## References

- [NuGet Documentation](https://docs.microsoft.com/nuget/)
- [PackageReference Format](https://docs.microsoft.com/nuget/consume-packages/package-references-in-project-files)
- [NuGet Lock Files](https://docs.microsoft.com/nuget/consume-packages/package-references-in-project-files#locking-dependencies)
- [CycloneDX .NET](https://github.com/CycloneDX/cyclonedx-dotnet)
- [Central Package Management](https://docs.microsoft.com/nuget/consume-packages/central-package-management)
