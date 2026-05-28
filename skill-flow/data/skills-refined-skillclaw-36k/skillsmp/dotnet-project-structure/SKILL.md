---
name: dotnet-project-structure
description: .NET 10 project structure and scaffolding templates for migrated PHP applications. Use when creating new .NET projects, setting up folder structure, or generating boilerplate code for ASP.NET Core MVC or Minimal APIs.
---

# .NET 10 Project Structure Guide

Use this skill when setting up the .NET 10 project structure for migrated PHP applications.

## Recommended Project Structure

### ASP.NET Core MVC (from Laravel/Symfony)

```
src/ProjectName.Web/
├── Controllers/              # MVC Controllers
│   ├── HomeController.cs
│   └── Api/                  # API Controllers
├── Models/
│   ├── Entities/             # EF Core entities (from Eloquent models)
│   ├── DTOs/                 # Data Transfer Objects
│   └── ViewModels/           # View-specific models
├── Services/
│   ├── Interfaces/           # Service contracts
│   └── Implementations/      # Service implementations
├── Data/
│   ├── ApplicationDbContext.cs
│   └── Migrations/           # EF Core migrations
├── Views/                    # Razor views (from Blade/Twig)
│   ├── Shared/
│   │   ├── _Layout.cshtml
│   │   └── _Partial.cshtml
│   └── Home/
├── Infrastructure/
│   ├── Extensions/           # DI and service extensions
│   └── Middleware/           # Custom middleware
├── wwwroot/                  # Static files
│   ├── css/
│   ├── js/
│   └── images/
├── appsettings.json          # Configuration
├── appsettings.Development.json
└── Program.cs                # Entry point
```

### ASP.NET Core Minimal APIs (from Slim/Lumen)

```
src/ProjectName.Api/
├── Endpoints/                # Minimal API endpoint groups
│   ├── ProductEndpoints.cs
│   └── UserEndpoints.cs
├── Models/
│   ├── Entities/
│   └── DTOs/
├── Services/
│   ├── Interfaces/
│   └── Implementations/
├── Data/
│   └── ApplicationDbContext.cs
├── Infrastructure/
│   ├── Extensions/
│   └── Middleware/
├── appsettings.json
└── Program.cs
```

## Template Files

See the [templates](./templates/) directory for starter files:
- [Program.cs](./templates/Program.cs) - Entry point with DI setup
- [ApplicationDbContext.cs](./templates/ApplicationDbContext.cs) - EF Core DbContext
- [BaseController.cs](./templates/BaseController.cs) - Base controller with common functionality
- [ServiceCollectionExtensions.cs](./templates/ServiceCollectionExtensions.cs) - DI registration

## PHP to .NET Structure Mapping

| PHP (Laravel) | .NET 10 |
|---------------|---------|
| `app/Http/Controllers/` | `Controllers/` |
| `app/Models/` | `Models/Entities/` |
| `app/Services/` | `Services/Implementations/` |
| `app/Repositories/` | `Data/` (or keep as Repositories) |
| `resources/views/` | `Views/` |
| `resources/views/layouts/` | `Views/Shared/` |
| `public/` | `wwwroot/` |
| `routes/web.php` | `Program.cs` or `Controllers/` |
| `routes/api.php` | `Controllers/Api/` or `Endpoints/` |
| `config/` | `appsettings.json` |
| `database/migrations/` | `Data/Migrations/` |
| `app/Http/Middleware/` | `Infrastructure/Middleware/` |
| `app/Providers/` | `Infrastructure/Extensions/` |

## Naming Conventions

| Concept | PHP | .NET |
|---------|-----|------|
| Files | `snake_case.php` | `PascalCase.cs` |
| Classes | `PascalCase` | `PascalCase` |
| Methods | `camelCase` | `PascalCase` |
| Variables | `$camelCase` | `camelCase` |
| Properties | `$snake_case` or `$camelCase` | `PascalCase` |
| Constants | `UPPER_SNAKE_CASE` | `PascalCase` |
| Interfaces | `Interface` suffix | `I` prefix (`IService`) |

## Best Practices

1. **One class per file** - Each `.cs` file contains one class
2. **Interface-first** - Create `IService` interfaces for all services
3. **DTOs for boundaries** - Use DTOs between layers, not entities
4. **Extension methods for DI** - Group related service registrations
5. **Async everywhere** - Use `async/await` for I/O operations
6. **Nullable reference types** - Enable and handle nullability properly
