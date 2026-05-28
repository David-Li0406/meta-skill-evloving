---
name: perigon
description: Pointers for Copilot/agents to apply Perigon conventions
---
## When to use
- Need project rules, locations, or docs before generating code.

## Usage
- Start with .github/copilot-instructions.md (global rules: accuracy first, no builds unless asked, check diagnostics).
- Repository layout (from README):
	- docs: project documents
	- scripts: project scripts
	- src: project code
	- test: test projects
	- .config: configuration files
- Backend map: definitions in src/Definition/{Entity,EntityFramework,Share,ServiceDefaults}; managers/DTOs in src/Modules/{Mod}/{Managers,Models}; controllers in src/Services/*/Controllers; host in src/AppHost.
- Frontend map: Angular app in src/ClientApp/WebApp (routes app/app.routes.ts, services app/services, shared components app/share/components, i18n assets/i18n).
- src layout highlights:
	- src/Perigon/Perigon.AspNetCore: base libraries and helpers
	- src/Definition/ServiceDefaults: shared service registrations
	- src/Definition/Entity: entities organized by module
	- src/Definition/EntityFramework: EF Core DbContext and migrations
	- src/Modules/{Mod}/Managers: business logic
	- src/Modules/{Mod}/Models: DTOs by entity
	- src/Services/ApiService: public Web API
	- src/Services/AdminService: admin Web API
- Key docs: Development-Conventions, Constants-Definition, Database, Manager-Business-Logic, Controller-APIs at https://dusi.dev/docs/Perigon/en-US/10.0/Best-Practices/…
- Behavior defaults: RESTful APIs; ManagerBase pattern; Code First EF; Guid v7 IDs; BusinessException/Problem for errors; select projections over heavy Include; avoid manager cross-calls; no ApiResponse wrappers.
- When unclear: ask for entity/DTO details and target module/service; do not assume; avoid auto-running builds/migrations.
- Constants:
  - Shared constants live in src/Definition/Share/Constants; module-specific constants stay in their module/service.
  - Extend AppConst via extension methods in Share/Constants (e.g., AppExtensions) rather than modifying base constants.
- Migrations/runtime:
  - AppHost startup applies latest migrations via MigrationService.
  - For new DbContext: add under Definition/EntityFramework/AppDbContext and register in Definition/ServiceDefaults/FrameworkExtensions, then resolve via UniversalDbFactory.
- MCP (perigon CLI MCP server):
	- Prefer MCP generation tools over manual scaffolding when creating modules/entities/DTOs/managers/controllers.
	- Available MCP tools to use:
		- create module: mcp_perigon_create_module
		- new entity model: mcp_perigon_new_entity
		- generate DTO: mcp_perigon_generate_dto
		- generate manager: mcp_perigon_generate_manager
		- generate controller API: mcp_perigon_generate_controller
		- create/verify razor template: mcp_perigon_create_razor_template / mcp_perigon_verify_razor_template
		- execute generate task: mcp_perigon_execute_generate_task
	- MCP server config lives in [.mcp.json](.mcp.json) and [.vscode/mcp.json](.vscode/mcp.json); use configured endpoints when invoking tools.
