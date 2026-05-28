---
name: dependency-analyzer
description: Analyzes NuGet packages and project dependencies for security and updates
trigger: "dependency check OR update packages OR security scan OR check vulnerabilities"
allowed-tools:
  - Bash(dotnet list)
  - Bash(dotnet restore)
  - Bash(dotnet nuget)
  - Read
  - Glob
  - Grep
---

# Dependency Analyzer

Analyzes project dependencies for security vulnerabilities, updates, and conflicts.

## Trigger Conditions

- User says "check dependencies"
- User says "update packages"
- User says "security scan"
- User says "check vulnerabilities"
- Before major releases

## Analysis Categories

### 1. Security Vulnerability Scan

**Commands:**
```bash
# Check for vulnerable packages (including transitive)
dotnet list package --vulnerable --include-transitive

# Output vulnerable packages in all projects
dotnet list Merge.sln package --vulnerable

# Check specific project
dotnet list Merge.API package --vulnerable
```

**Common Vulnerabilities:**
```
Package                    CVE             Severity  Fix Version
─────────────────────────────────────────────────────────────────
System.Text.Json           CVE-2024-xxxx   High      8.0.1
Newtonsoft.Json           CVE-2024-yyyy   Medium    13.0.3
Microsoft.Data.SqlClient  CVE-2024-zzzz   Critical  5.1.4
```

**Auto-Fix:**
```bash
# Update vulnerable package to safe version
dotnet add package System.Text.Json --version 8.0.1

# Update all packages in solution
dotnet outdated --upgrade
```

### 2. Outdated Package Analysis

**Commands:**
```bash
# List outdated packages
dotnet list package --outdated

# Include prerelease versions
dotnet list package --outdated --include-prerelease

# Check specific framework
dotnet list package --outdated --framework net9.0
```

**Output Format:**
```
Project: Merge.API

Package                           Current   Latest    Type
─────────────────────────────────────────────────────────────
MediatR                          11.1.0    12.2.0    Major
AutoMapper                       12.0.1    13.0.1    Major
FluentValidation                 11.8.0    11.9.0    Minor
Microsoft.EntityFrameworkCore    8.0.0     9.0.0     Major
Serilog.AspNetCore              7.0.0     8.0.1     Major
```

**Update Strategy:**
- **Patch** (x.x.1 → x.x.2): Safe to update immediately
- **Minor** (x.1.x → x.2.x): Review changelog, usually safe
- **Major** (1.x.x → 2.x.x): Review breaking changes, test thoroughly

### 3. Version Conflict Detection

**Detection:**
```bash
# Check for version conflicts
dotnet list package --include-transitive | grep -E "^\s+>" | sort | uniq -d

# Find packages with multiple versions
dotnet restore --verbosity detailed 2>&1 | grep "Detected package version"
```

**Common Conflicts:**
```csharp
// ❌ Conflict: Different projects reference different versions
Merge.API          → Newtonsoft.Json 13.0.1
Merge.Application  → Newtonsoft.Json 12.0.3 (transitive from OtherPackage)

// ✅ Resolution: Add explicit package reference
<PackageReference Include="Newtonsoft.Json" Version="13.0.1" />
```

**Resolution Strategies:**
1. **Direct Reference**: Add explicit package reference with desired version
2. **Central Package Management**: Use Directory.Packages.props
3. **Binding Redirects**: For .NET Framework compatibility

### 4. Unused Package Detection

**Detection:**
```bash
# Find packages not referenced in code
# Check if namespace is used
for pkg in $(dotnet list package --format json | jq -r '.projects[].frameworks[].topLevelPackages[].id'); do
    if ! grep -r "using.*${pkg//.*/}" --include="*.cs" >/dev/null 2>&1; then
        echo "Potentially unused: $pkg"
    fi
done
```

**Common Unused Packages:**
- Development tools left in production
- Removed feature dependencies
- Transitive dependencies made explicit

### 5. License Compliance

**Check Licenses:**
```bash
# Using dotnet-project-licenses tool
dotnet tool install --global dotnet-project-licenses
dotnet-project-licenses -i Merge.sln

# Common license types
# MIT, Apache-2.0: Generally permissive, OK for commercial
# GPL: Copyleft, requires source disclosure
# BSD: Permissive with attribution
```

**License Report:**
```
Package                    License      Risk
─────────────────────────────────────────────
MediatR                   Apache-2.0   Low
AutoMapper                MIT          Low
Newtonsoft.Json           MIT          Low
SomePackage               GPL-3.0      High (copyleft)
```

### 6. Transitive Dependency Analysis

**Commands:**
```bash
# List all transitive dependencies
dotnet list package --include-transitive

# Find deep dependency chains
dotnet list package --include-transitive --format json | \
  jq '.projects[].frameworks[].transitivePackages[] | "\(.id) <- \(.resolvedVersion)"'
```

**Risk Assessment:**
- **Deep chains**: More points of failure
- **Abandoned packages**: No updates, potential vulnerabilities
- **Heavy dependencies**: Large bundle size

## Package Update Workflow

### Step 1: Analyze Current State
```bash
# Full dependency report
dotnet list package --include-transitive > deps-before.txt

# Check vulnerabilities
dotnet list package --vulnerable > vulnerabilities.txt

# Check outdated
dotnet list package --outdated > outdated.txt
```

### Step 2: Plan Updates
```markdown
## Update Plan

### Critical (Security)
1. System.Text.Json: 8.0.0 → 8.0.1 (CVE-2024-xxxx)

### High Priority (Major versions with benefits)
1. MediatR: 11.1.0 → 12.2.0 (Performance improvements)

### Medium Priority (Minor updates)
1. FluentValidation: 11.8.0 → 11.9.0 (Bug fixes)

### Low Priority (Patch updates)
1. Serilog: 3.1.0 → 3.1.1 (Minor fixes)
```

### Step 3: Update Packages
```bash
# Update specific package
dotnet add Merge.API package MediatR --version 12.2.0

# Update all packages (use with caution)
dotnet outdated --upgrade

# Restore and verify
dotnet restore
dotnet build
```

### Step 4: Verify Changes
```bash
# Run tests
dotnet test

# Compare dependencies
diff deps-before.txt <(dotnet list package --include-transitive)

# Check for new vulnerabilities
dotnet list package --vulnerable
```

## Central Package Management

**Directory.Packages.props:**
```xml
<Project>
  <PropertyGroup>
    <ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>
  </PropertyGroup>
  <ItemGroup>
    <!-- Core -->
    <PackageVersion Include="MediatR" Version="12.2.0" />
    <PackageVersion Include="AutoMapper" Version="13.0.1" />
    <PackageVersion Include="FluentValidation" Version="11.9.0" />

    <!-- EF Core -->
    <PackageVersion Include="Microsoft.EntityFrameworkCore" Version="9.0.0" />
    <PackageVersion Include="Npgsql.EntityFrameworkCore.PostgreSQL" Version="9.0.0" />

    <!-- Testing -->
    <PackageVersion Include="xunit" Version="2.6.6" />
    <PackageVersion Include="FluentAssertions" Version="6.12.0" />
    <PackageVersion Include="NSubstitute" Version="5.1.0" />
  </ItemGroup>
</Project>
```

**Project File (simplified):**
```xml
<ItemGroup>
  <PackageReference Include="MediatR" />
  <PackageReference Include="AutoMapper" />
  <PackageReference Include="FluentValidation" />
</ItemGroup>
```

## Output Format

```markdown
# Dependency Analysis Report

**Date:** 2024-01-15
**Solution:** Merge E-Commerce Backend

## Summary

| Category | Count | Status |
|----------|-------|--------|
| Total Packages | 45 | - |
| Vulnerable | 2 | 🔴 Action Required |
| Outdated (Major) | 5 | 🟡 Review Needed |
| Outdated (Minor) | 8 | 🔵 Optional |
| Unused | 3 | ⚠️ Consider Removal |

## Security Issues

### Critical
| Package | Current | Fixed | CVE |
|---------|---------|-------|-----|
| System.Text.Json | 8.0.0 | 8.0.1 | CVE-2024-xxxx |

### High
| Package | Current | Fixed | CVE |
|---------|---------|-------|-----|
| Microsoft.Data.SqlClient | 5.1.0 | 5.1.4 | CVE-2024-yyyy |

## Recommended Updates

### Immediate (Security)
```bash
dotnet add package System.Text.Json --version 8.0.1
dotnet add package Microsoft.Data.SqlClient --version 5.1.4
```

### This Sprint (Major versions)
```bash
dotnet add package MediatR --version 12.2.0
dotnet add package AutoMapper --version 13.0.1
```

## Unused Packages (Consider Removal)
- Swashbuckle.AspNetCore.Annotations (not used)
- Microsoft.Extensions.Caching.Memory (redundant with Redis)

## License Summary
- MIT: 35 packages ✅
- Apache-2.0: 8 packages ✅
- BSD: 2 packages ✅
- Unknown: 0 packages ✅
```

## Automation

**GitHub Action for Dependency Check:**
```yaml
name: Dependency Audit
on:
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday
  workflow_dispatch:

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-dotnet@v4
        with:
          dotnet-version: '9.0.x'
      - name: Check vulnerabilities
        run: dotnet list package --vulnerable --include-transitive
      - name: Check outdated
        run: dotnet list package --outdated
```
