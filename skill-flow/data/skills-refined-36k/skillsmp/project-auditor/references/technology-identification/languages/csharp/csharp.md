# C#

**Category**: languages
**Description**: C# programming language - modern, object-oriented language developed by Microsoft for .NET platform
**Homepage**: https://docs.microsoft.com/en-us/dotnet/csharp/

## Package Detection

### NUGET
- `Microsoft.NET.Sdk`
- `Microsoft.NETCore.App`
- `Microsoft.AspNetCore.App`

## Configuration Files

- `*.csproj`
- `*.sln`
- `*.fsproj` (F#)
- `*.vbproj` (VB.NET)
- `nuget.config`
- `NuGet.Config`
- `packages.config`
- `global.json`
- `Directory.Build.props`
- `Directory.Build.targets`
- `*.props`
- `*.targets`
- `app.config`
- `web.config`
- `appsettings.json`
- `appsettings.*.json`

## File Extensions

- `.cs`
- `.csx` (C# script)
- `.razor` (Razor components)
- `.cshtml` (Razor views)

## Import Detection

### CSharp
**Pattern**: `^using\s+[\w.]+;`
- Using directive
- Example: `using System.Collections.Generic;`

**Pattern**: `^namespace\s+[\w.]+`
- Namespace declaration
- Example: `namespace MyApp.Services {}`

**Pattern**: `(public|private|internal)\s+(class|interface|struct|enum|record)\s+\w+`
- Type declaration
- Example: `public class UserService {}`

**Pattern**: `static\s+void\s+Main\(`
- Main method
- Example: `static void Main(string[] args) {}`

**Pattern**: `async\s+Task`
- Async method
- Example: `public async Task<User> GetUserAsync() {}`

## Environment Variables

- `DOTNET_ROOT`
- `DOTNET_CLI_HOME`
- `NUGET_PACKAGES`
- `ASPNETCORE_ENVIRONMENT`
- `DOTNET_ENVIRONMENT`
- `MSBuildSDKsPath`

## Version Indicators

- .NET 8 (current LTS)
- .NET 7 (STS)
- .NET 6 LTS (widely used)
- .NET Core 3.1 (legacy LTS)
- .NET Framework 4.8 (legacy)

## Detection Notes

- Look for `.cs` files in repository
- `.csproj` file is the primary indicator
- `.sln` file indicates Visual Studio solution
- Check TargetFramework in .csproj for version
- global.json pins SDK version

## Detection Confidence

- **File Extension Detection**: 95% (HIGH)
- **.csproj Detection**: 95% (HIGH)
- **Package Detection**: 90% (HIGH)
