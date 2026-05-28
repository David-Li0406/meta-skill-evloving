# ASP.NET Core

**Category**: web-frameworks/backend
**Description**: Cross-platform, high-performance framework for building modern, cloud-enabled, Internet-connected apps

## Package Detection

### NUGET
- `Microsoft.AspNetCore.App`
- `Microsoft.AspNetCore.Mvc`
- `Microsoft.AspNetCore`

### Related Packages
- `Microsoft.EntityFrameworkCore`
- `Microsoft.AspNetCore.Authentication.JwtBearer`
- `Microsoft.AspNetCore.Identity`
- `Swashbuckle.AspNetCore`

## Import Detection

### Csharp
File extensions: .cs

**Pattern**: `using Microsoft\.AspNetCore`
- ASP.NET Core namespace imports
- Example: `using Microsoft.AspNetCore.Mvc;`

**Pattern**: `\[ApiController\]|\[Controller\]`
- ASP.NET Core controller attributes
- Example: `[ApiController] public class UsersController : ControllerBase {...}`

**Pattern**: `\[HttpGet\]|\[HttpPost\]|\[HttpPut\]|\[HttpDelete\]`
- HTTP method attributes
- Example: `[HttpGet] public ActionResult<User> GetUser(int id) {...}`

**Pattern**: `WebApplication\.CreateBuilder|builder\.Build\(\)`
- ASP.NET Core 6+ minimal API pattern
- Example: `var builder = WebApplication.CreateBuilder(args);`

### Common Imports
- `Microsoft.AspNetCore.Mvc`
- `Microsoft.AspNetCore.Builder`
- `Microsoft.AspNetCore.Hosting`

## Environment Variables

*ASP.NET Core environment variables*

- `ASPNETCORE_ENVIRONMENT`
- `ASPNETCORE_URLS`
- `DOTNET_ENVIRONMENT`
- `ConnectionStrings__DefaultConnection`

## Configuration Files

- `*.csproj`
- `appsettings.json`
- `appsettings.Development.json`
- `Program.cs`
- `Startup.cs`

## Detection Notes

- ASP.NET Core is C#/.NET-based
- Uses NuGet for package management
- Cross-platform (Windows, Linux, macOS)

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 70% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
