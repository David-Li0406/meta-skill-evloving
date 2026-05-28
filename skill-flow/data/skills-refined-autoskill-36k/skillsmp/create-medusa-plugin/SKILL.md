---
name: create-medusa-plugin
description: Creates custom MedusaJS v2 plugins following the established patterns from the Bling plugin. Guides through plugin structure creation including modules, models, API routes, workflows, and TypeScript configuration. Use when creating new MedusaJS integrations, third-party service plugins, or extending MedusaJS functionality with custom modules.
---

# Create MedusaJS Plugin

Creates custom MedusaJS v2 plugins for the learning-infra monorepo following established patterns, proper structure, and MedusaJS best practices.

This skill guides you through creating production-ready MedusaJS plugins with:
- Custom modules with dependency injection
- MikroORM entities for data persistence
- Admin and Store API routes
- Workflow orchestration with steps
- OAuth integration patterns
- TypeScript strict mode configuration

## Project Documentation References

For comprehensive project documentation and MedusaJS compatibility requirements, see:

- **[AGENTS.md](../../../AGENTS.md)** - Central reference for all project documentation
- **[@project-overview.md](../../rules/shared/project/project-overview.md)** - Project overview and tech stack
- **[@coding-standards.md](../../rules/shared/quality/coding-standards.md)** - Coding standards and guidelines

## MedusaJS Documentation

Use the `context7` MCP server to query MedusaJS v2 documentation:

```
Query: "How to create a custom module in MedusaJS v2"
Library: /medusajs/medusa
```

Key topics to reference:
- Custom modules and services
- MikroORM entities and repositories
- API route creation (admin and store)
- Workflow SDK and step creation
- Plugin configuration and exports

## Plugin Creation Workflow

Follow these steps to create a new MedusaJS plugin:

### 1. Determine Plugin Scope

**Questions to answer:**
- What third-party service are you integrating? (e.g., Bling ERP, Shopify, Stripe)
- What functionality does it provide? (e.g., product sync, order management, payments)
- Does it require OAuth authentication?
- What data needs to be persisted? (e.g., tokens, config, sync preferences)
- What API endpoints are needed? (admin only, store only, or both)

### 2. Create Plugin Structure

**Location:** `packages/medusa/plugins/medusa-plugin-{service-name}/`

**Required files:**
```
packages/medusa/plugins/medusa-plugin-{service-name}/
├── package.json
├── tsconfig.json
├── .gitignore
└── src/
    ├── models/           # MikroORM entities
    ├── modules/          # Custom modules
    │   └── {service}/
    │       ├── index.ts
    │       ├── service.ts
    │       ├── types/
    │       └── utils/
    ├── api/              # API routes
    │   ├── admin/
    │   └── store/
    └── workflows/        # Workflow orchestration
        └── steps/
```

### 3. Configure Package

**package.json pattern:**

```json
{
  "name": "@vendin/medusa-plugin-{service}",
  "version": "1.0.0",
  "description": "{Service} integration for MedusaJS v2",
  "private": true,
  "type": "module",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "require": "./dist/index.js",
      "types": "./dist/index.d.ts"
    },
    "./api/*": "./dist/api/*",
    "./modules/*": "./dist/modules/*",
    "./workflows/*": "./dist/workflows/*",
    "./package.json": "./package.json"
  },
  "scripts": {
    "build": "medusa plugin:build",
    "watch": "tsc --watch",
    "clean": "rm -rf dist .medusa",
    "test": "vitest",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "@medusajs/admin-sdk": "^2.13.0",
    "@medusajs/framework": "^2.13.0",
    "@medusajs/medusa": "^2.13.0",
    "@medusajs/types": "^2.13.0",
    "@medusajs/ui": "^4.1.0",
    "@medusajs/utils": "^2.13.0",
    "@mikro-orm/core": "^6.6.5",
    "axios": "^1.6.8",
    "zod": "^3.22.4"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0",
    "vitest": "^1.0.0",
    "@medusajs/cli": "^2.13.0"
  },
  "peerDependencies": {
    "@medusajs/framework": "^2.0.0"
  },
  "files": ["dist"]
}
```

**tsconfig.json pattern:**

```json
{
  "extends": "../config/tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src",
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true,
    "exactOptionalPropertyTypes": false
  },
  "include": ["src/**/*"]
}
```

**.gitignore:**

```
.medusa
.turbo
node_modules
dist
```

### 4. Create Models (Data Persistence)

**Pattern:** Use MikroORM entities for configuration and state

**Example:** `src/models/{service}-config.ts`

```typescript
import { Entity, PrimaryKey, Property, JsonType } from "@mikro-orm/core";

export type {Service}SyncPreferences = {
  // Define sync preferences structure
  products: {
    enabled: boolean;
    import_images: boolean;
    import_prices: boolean;
  };
  orders: {
    enabled: boolean;
    send_to_{service}: boolean;
  };
};

@Entity({ tableName: "{service}_config" })
export class {Service}Config {
  @PrimaryKey({ type: "string", columnType: "text" })
  id: string = "{service}_config";

  @Property({ nullable: true, columnType: "text", fieldName: "client_id" })
  clientId: string | null = null;

  @Property({ nullable: true, columnType: "text", fieldName: "client_secret" })
  clientSecret: string | null = null;

  @Property({ nullable: true, columnType: "text", fieldName: "access_token" })
  accessToken: string | null = null;

  @Property({ nullable: true, columnType: "text", fieldName: "refresh_token" })
  refreshToken: string | null = null;

  @Property({ nullable: true, columnType: "integer", fieldName: "expires_in" })
  expiresIn: number | null = null;

  @Property({ nullable: true, columnType: "timestamptz", fieldName: "token_updated_at" })
  tokenUpdatedAt: Date | null = null;

  @Property({ nullable: true, type: JsonType, fieldName: "sync_preferences" })
  syncPreferences: {Service}SyncPreferences | null = null;
}
```

**Key patterns:**
- Use `@Entity` decorator with explicit `tableName`
- Use `fieldName` for snake_case database columns
- Use `JsonType` for complex configuration objects
- Provide sensible defaults for nullable fields

### 5. Create Module Service

**Pattern:** Custom module with MedusaService base class

**Example:** `src/modules/{service}/index.ts`

```typescript
import {Service}ModuleService from "./service.js";

export const {SERVICE}_MODULE = "{service}";

export default {
  service: {Service}ModuleService,
};
```

**Example:** `src/modules/{service}/service.ts`

```typescript
import { MedusaService } from "@medusajs/framework/utils";
import { Logger } from "@medusajs/types";
import { EntityManager, EntityRepository } from "@mikro-orm/core";
import axios, { AxiosInstance } from "axios";
import { {Service}Config } from "../../models/{service}-config.js";

type {Service}ModuleOptions = {
  apiBaseUrl?: string;
  oauthBaseUrl?: string;
};

type InjectedDependencies = {
  manager: EntityManager;
  logger: Logger;
};

class {Service}ModuleService extends MedusaService({
  {Service}Config,
}) {
  protected readonly logger_: Logger;
  protected readonly configRepository_: EntityRepository<{Service}Config>;
  protected readonly apiBaseUrl: string;
  protected readonly oauthBaseUrl: string;

  constructor(
    deps: InjectedDependencies,
    options: {Service}ModuleOptions = {}
  ) {
    super(arguments[0]);
    this.logger_ = deps.logger;
    this.configRepository_ = deps.manager.getRepository({Service}Config);
    this.apiBaseUrl = options.apiBaseUrl || "https://api.{service}.com";
    this.oauthBaseUrl = options.oauthBaseUrl || "https://oauth.{service}.com";
  }

  async getConfig(): Promise<{Service}Config | null> {
    return await this.configRepository_.findOne({ id: "{service}_config" });
  }

  async saveConfig(data: Partial<{Service}Config>): Promise<{Service}Config> {
    let config = await this.getConfig();
    
    if (!config) {
      config = this.configRepository_.create({ id: "{service}_config", ...data });
    } else {
      this.configRepository_.assign(config, data);
    }
    
    await this.configRepository_.flush();
    return config;
  }

  // OAuth methods (if needed)
  async getAuthorizationUrl(redirectUri: string): Promise<string> {
    const config = await this.getConfig();
    if (!config?.clientId) {
      throw new Error("Client ID not configured");
    }

    const params = new URLSearchParams({
      client_id: config.clientId,
      redirect_uri: redirectUri,
      response_type: "code",
      scope: "required scopes here",
    });

    return `${this.oauthBaseUrl}/authorize?${params}`;
  }

  async handleOAuthCallback(code: string): Promise<{ success: boolean }> {
    // Implement OAuth token exchange
    const config = await this.getConfig();
    // ... exchange code for tokens
    await this.saveConfig({ accessToken: "...", refreshToken: "..." });
    return { success: true };
  }

  async getAccessToken(): Promise<string> {
    const config = await this.getConfig();
    if (!config?.accessToken) {
      throw new Error("Not authenticated");
    }
    
    // Check if token is expired and refresh if needed
    // ... token refresh logic
    
    return config.accessToken;
  }

  async createAuthorizedClient(): Promise<AxiosInstance> {
    const token = await this.getAccessToken();
    return axios.create({
      baseURL: this.apiBaseUrl,
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  // API methods
  async getProducts(params: Record<string, any> = {}) {
    const client = await this.createAuthorizedClient();
    const response = await client.get("/products", { params });
    return response.data;
  }

  async createOrder(payload: any) {
    const client = await this.createAuthorizedClient();
    const response = await client.post("/orders", payload);
    return response.data;
  }
}

export default {Service}ModuleService;
```

**Key patterns:**
- Extend `MedusaService` with entity models
- Inject `manager` and `logger` dependencies
- Use repository pattern for data access
- Implement OAuth flow if needed
- Create authorized HTTP clients for API calls
- Add error handling and logging

### 6. Create API Routes

**Admin routes pattern:** `src/api/admin/{service}/{action}/route.ts`

```typescript
import { z } from "zod";
import { {SERVICE}_MODULE } from "../../../../modules/{service}/index.js";
import type {Service}ModuleService from "../../../../modules/{service}/service.js";
import type { MedusaRequest, MedusaResponse } from "@medusajs/framework/http";

const schema = z.object({
  // Define request schema
});

export const GET = async (request: MedusaRequest, response: MedusaResponse) => {
  const validated = schema.parse(request.query);
  const {service}Service: {Service}ModuleService = request.scope.resolve({SERVICE}_MODULE);

  try {
    const result = await {service}Service.someMethod(validated);
    response.json(result);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Generic error";
    response.status(400).json({ message });
  }
};

export const POST = async (request: MedusaRequest, response: MedusaResponse) => {
  const validated = schema.parse(request.body);
  const {service}Service: {Service}ModuleService = request.scope.resolve({SERVICE}_MODULE);

  try {
    const result = await {service}Service.someMethod(validated);
    response.json(result);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Generic error";
    response.status(400).json({ message });
  }
};
```

**Store routes pattern:** `src/api/store/{service}/{action}/route.ts`

Similar structure but for customer-facing endpoints.

**Key patterns:**
- Use Zod for request validation
- Resolve module service from request scope
- Use proper HTTP methods (GET, POST, PUT, DELETE)
- Return consistent error responses
- Type request and response properly

### 7. Create Workflows

**Workflow pattern:** `src/workflows/sync-{entity}.ts`

```typescript
import { createWorkflow, WorkflowResponse } from "@medusajs/framework/workflows-sdk";
import { fetch{Entity}Step } from "./steps/fetch-{entity}-step.js";
import { upsert{Entity}Step } from "./steps/upsert-{entity}-step.js";

export const sync{Entity}From{Service}Workflow = createWorkflow(
  "sync-{entity}-from-{service}",
  () => {
    // 1. Fetch from external service
    const items = fetch{Entity}Step();

    // 2. Upsert into Medusa
    const result = upsert{Entity}Step({ items });

    return new WorkflowResponse({
      items_synced: result,
    });
  }
);
```

**Step pattern:** `src/workflows/steps/fetch-{entity}-step.ts`

```typescript
import { createStep, StepResponse } from "@medusajs/framework/workflows-sdk";
import { {SERVICE}_MODULE } from "../../modules/{service}/index.js";
import type {Service}ModuleService from "../../modules/{service}/service.js";

export const fetch{Entity}Step = createStep(
  "fetch-{entity}-from-{service}",
  async (input, { container }) => {
    const {service}Service: {Service}ModuleService = container.resolve({SERVICE}_MODULE);

    const items = await {service}Service.get{Entity}();

    return new StepResponse(items);
  }
);
```

**Key patterns:**
- Use `createWorkflow` for orchestration
- Use `createStep` for individual operations
- Resolve services from container
- Return `StepResponse` for compensatable steps
- Chain steps logically (fetch → transform → upsert)

### 8. Add Type Definitions

**Pattern:** `src/modules/{service}/types/index.ts`

```typescript
export type {Service}Product = {
  id: string;
  name: string;
  price: number;
  // ... other fields
};

export type {Service}Order = {
  id: string;
  customer: {
    name: string;
    email: string;
  };
  items: Array<{
    product_id: string;
    quantity: number;
  }>;
  // ... other fields
};

// Export all types
export * from "./api-types.js";
```

### 9. Add Utility Functions

**Pattern:** `src/modules/{service}/utils/{mapper}.ts`

```typescript
import type { Product } from "@medusajs/types";
import type { {Service}Product } from "../types/index.js";

export function map{Service}ProductToMedusa(
  {service}Product: {Service}Product
): Partial<Product> {
  return {
    title: {service}Product.name,
    handle: {service}Product.id.toLowerCase(),
    // ... map other fields
  };
}

export function mapMedusaProductTo{Service}(
  medusaProduct: Product
): {Service}Product {
  return {
    id: medusaProduct.handle || medusaProduct.id,
    name: medusaProduct.title,
    // ... map other fields
  };
}
```

## Reference Implementation

See the Bling plugin for a complete reference implementation:

- **[package.json](file:///C:/Users/yuri_/IdeaProjects/learning-infra/packages/medusa-plugin-bling/package.json)** - Package configuration
- **[src/models/](file:///C:/Users/yuri_/IdeaProjects/learning-infra/packages/medusa-plugin-bling/src/models)** - MikroORM entities
- **[src/modules/bling/](file:///C:/Users/yuri_/IdeaProjects/learning-infra/packages/medusa-plugin-bling/src/modules/bling)** - Module service
- **[src/api/](file:///C:/Users/yuri_/IdeaProjects/learning-infra/packages/medusa-plugin-bling/src/api)** - API routes
- **[src/workflows/](file:///C:/Users/yuri_/IdeaProjects/learning-infra/packages/medusa-plugin-bling/src/workflows)** - Workflows and steps

## Common Patterns

### OAuth Integration

1. Store client credentials in config entity
2. Implement authorization URL generation
3. Handle OAuth callback with code exchange
4. Store and refresh access tokens
5. Create authorized HTTP clients

### Data Synchronization

1. Create workflow for sync orchestration
2. Fetch data from external service
3. Map external data to Medusa format
4. Upsert entities using Medusa services
5. Handle errors and log results

### Configuration Management

1. Use MikroORM entity for persistence
2. Provide defaults for optional settings
3. Use JSON columns for complex preferences
4. Expose admin API for configuration updates

### Error Handling

1. Use try-catch in API routes
2. Return consistent error responses
3. Log errors with context
4. Provide helpful error messages

## Testing

Create tests following the project's testing strategy:

```typescript
import { describe, it, expect } from "vitest";
import { map{Service}ProductToMedusa } from "../utils/{mapper}.js";

describe("{Service} Product Mapper", () => {
  it("should map {service} product to Medusa format", () => {
    const {service}Product = {
      id: "123",
      name: "Test Product",
      price: 99.99,
    };

    const medusaProduct = map{Service}ProductToMedusa({service}Product);

    expect(medusaProduct.title).toBe("Test Product");
    expect(medusaProduct.handle).toBe("123");
  });
});
```

## Next Steps

After creating the plugin:

1. **Build the plugin:** `bun run build` in the plugin directory
2. **Add to tenant instance:** Update `apps/tenant-instance/medusa-config.ts`
3. **Run migrations:** The plugin will auto-create tables on first run
4. **Test API routes:** Use the admin dashboard or API client
5. **Verify workflows:** Trigger sync workflows and check logs
