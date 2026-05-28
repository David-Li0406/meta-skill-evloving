---
name: backend
description: Perigon ASP.NET Core + EF Core + Aspire conventions
---
## When to use
- Backend work across src/Definition, src/Modules, src/Services, and src/AppHost (entities, DTOs, managers, controllers, EF, hosting).

## Usage
- Architecture: Definition (entities/EF/Share/ServiceDefaults) -> Modules (Managers + DTOs) -> Services (controllers). Use Code First with <Nullable>enable.
- Project configuration: enable <Nullable> and follow RESTful naming conventions in controllers (AddAsync/UpdateAsync/DeleteAsync/GetDetailAsync/FilterAsync).
- Entities: inherit EntityBase (Id, CreatedAt, UpdatedAt, IsDeleted); Id uses Guid v7 client-generated. Strings need max length; decimals set precision (10,2 or 18,6); enums require [Description]; prefer DateTimeOffset/DateOnly/TimeOnly.
- Database: prefer SQL Server (commercial) or PostgreSQL; use foreign keys within a domain; avoid string-delimited lists (use arrays/JSON). Use SQL Server 2025+ / PostgreSQL 18+ for new projects. Migrations via scripts/EFMigrations.ps1; files under Definition/EntityFramework/Migrations.
- Data access: DbContexts live in Definition/EntityFramework/AppDbContext; default TenantDbFactory/UniversalDbFactory for creation. Prefer Queryable with Select projections; AsNoTracking by default; use EFCore.BulkExtensions for bulk ops.
- Managers: place in src/Modules/{Mod}/Managers; inherit ManagerBase (generic when tied to entity) for DI. Do not return ActionResult or touch HttpContext; avoid manager-to-manager refs. Use base ops (FindAsync, ExistAsync, ListAsync, PageListAsync, InsertAsync, UpdateAsync, DeleteAsync, BulkInsertAsync, ExecuteInTransactionAsync). Throw BusinessException for business errors; keep third-party calls/helpers in Share/Services. Avoid defining Manager interfaces unless multiple implementations are required.
- DTOs: store under src/Modules/{Mod}/Models/{Entity}Dtos with Detail/Add/Update/Item/Filter shapes; map via Mapster.
- Controllers: under src/Services/*/Controllers; inherit RestControllerBase. Use HTTP verb attributes and method names AddAsync/UpdateAsync/DeleteAsync/GetDetailAsync/FilterAsync. Return ActionResult<T>; use Problem/NotFound for errors; avoid ApiResponse wrappers; keep business logic in Manager; handle auth/permission/validation here. Controllers handle routing, validation, permission checks, and error mapping; they should not implement business logic or data access.
- Aspire/AppHost: AppHost orchestrates infra/services; ensure Docker/Podman running. Configure via appsettings*.json. Avoid build/run commands unless requested; check editor diagnostics after changes.
- C#/.NET conventions:
	- Prefer file-scoped namespaces, primary constructors, and collection expressions where appropriate (C# 14).
	- Async all the way: use async/await, pass CancellationToken from controllers to managers/data access.
	- Validate inputs at the API boundary; keep business rules in Managers.
	- Use DI via constructor injection; avoid service locator patterns.
- ASP.NET Core API conventions:
	- Keep controllers thin; avoid DbContext usage outside Managers.
	- Use explicit [FromBody]/[FromQuery]/[FromRoute] when ambiguous.
	- Prefer HTTP verb attributes over [Route] for action routing.
	- Use pagination for list endpoints and avoid returning large unbounded sets.
	- Return ActionResult<T> (or model directly) on success; use Problem() / NotFound() for errors.
- Response standards:
	- Use HTTP status codes: 200 OK, 201 Created, 401 Unauthorized, 403 Forbidden, 404 NotFound, 409 Conflict, 500 Server/Business error.
	- Error responses follow ProblemDetails (title/status/detail/traceId). Business errors should throw BusinessException in Manager and be mapped by middleware.
