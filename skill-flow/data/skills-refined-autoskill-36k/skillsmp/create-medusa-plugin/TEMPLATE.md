# MedusaJS Plugin Template Examples

This document provides quick-reference templates for common MedusaJS plugin components.

## Quick Start Template

### Minimal Plugin Structure

```
packages/medusa-plugin-{service}/
├── package.json
├── tsconfig.json
├── .gitignore
└── src/
    ├── models/
    │   └── {service}-config.ts
    └── modules/
        └── {service}/
            ├── index.ts
            └── service.ts
```

## Model Template

### Basic Config Entity

```typescript
import { Entity, PrimaryKey, Property, JsonType } from "@mikro-orm/core";

export type {Service}Preferences = {
  enabled: boolean;
  // Add your preferences
};

@Entity({ tableName: "{service}_config" })
export class {Service}Config {
  @PrimaryKey({ type: "string", columnType: "text" })
  id: string = "{service}_config";

  @Property({ nullable: true, columnType: "text", fieldName: "api_key" })
  apiKey: string | null = null;

  @Property({ nullable: true, type: JsonType, fieldName: "preferences" })
  preferences: {Service}Preferences | null = null;
}
```

### Entity with Timestamps

```typescript
import { Entity, PrimaryKey, Property, BeforeCreate, BeforeUpdate } from "@mikro-orm/core";

@Entity({ tableName: "{service}_data" })
export class {Service}Data {
  @PrimaryKey({ type: "string", columnType: "text" })
  id!: string;

  @Property({ columnType: "text" })
  name!: string;

  @Property({ columnType: "timestamptz", fieldName: "created_at" })
  createdAt!: Date;

  @Property({ columnType: "timestamptz", fieldName: "updated_at" })
  updatedAt!: Date;

  @BeforeCreate()
  setCreatedAt() {
    this.createdAt = new Date();
    this.updatedAt = new Date();
  }

  @BeforeUpdate()
  setUpdatedAt() {
    this.updatedAt = new Date();
  }
}
```

## Module Service Template

### Basic Service

```typescript
import { MedusaService } from "@medusajs/framework/utils";
import { Logger } from "@medusajs/types";
import { EntityManager, EntityRepository } from "@mikro-orm/core";
import { {Service}Config } from "../../models/{service}-config.js";

type InjectedDependencies = {
  manager: EntityManager;
  logger: Logger;
};

class {Service}ModuleService extends MedusaService({
  {Service}Config,
}) {
  protected readonly logger_: Logger;
  protected readonly configRepository_: EntityRepository<{Service}Config>;

  constructor(deps: InjectedDependencies) {
    super(arguments[0]);
    this.logger_ = deps.logger;
    this.configRepository_ = deps.manager.getRepository({Service}Config);
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
}

export default {Service}ModuleService;
```

### Service with HTTP Client

```typescript
import axios, { AxiosInstance } from "axios";

class {Service}ModuleService extends MedusaService({
  {Service}Config,
}) {
  protected readonly apiBaseUrl: string;

  constructor(deps: InjectedDependencies, options: { apiBaseUrl?: string } = {}) {
    super(arguments[0]);
    this.logger_ = deps.logger;
    this.configRepository_ = deps.manager.getRepository({Service}Config);
    this.apiBaseUrl = options.apiBaseUrl || "https://api.{service}.com";
  }

  async createClient(): Promise<AxiosInstance> {
    const config = await this.getConfig();
    if (!config?.apiKey) {
      throw new Error("API key not configured");
    }

    return axios.create({
      baseURL: this.apiBaseUrl,
      headers: {
        "Authorization": `Bearer ${config.apiKey}`,
        "Content-Type": "application/json",
      },
    });
  }

  async fetchData(params: Record<string, any> = {}) {
    const client = await this.createClient();
    const response = await client.get("/data", { params });
    return response.data;
  }
}
```

## API Route Templates

### GET Route with Query Params

```typescript
import { z } from "zod";
import { {SERVICE}_MODULE } from "../../../../modules/{service}/index.js";
import type {Service}ModuleService from "../../../../modules/{service}/service.js";
import type { MedusaRequest, MedusaResponse } from "@medusajs/framework/http";

const querySchema = z.object({
  limit: z.coerce.number().optional().default(10),
  offset: z.coerce.number().optional().default(0),
});

export const GET = async (req: MedusaRequest, res: MedusaResponse) => {
  const { limit, offset } = querySchema.parse(req.query);
  const service: {Service}ModuleService = req.scope.resolve({SERVICE}_MODULE);

  try {
    const data = await service.fetchData({ limit, offset });
    res.json({ data });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    res.status(500).json({ error: message });
  }
};
```

### POST Route with Body Validation

```typescript
const bodySchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  preferences: z.object({
    enabled: z.boolean(),
  }).optional(),
});

export const POST = async (req: MedusaRequest, res: MedusaResponse) => {
  const validated = bodySchema.parse(req.body);
  const service: {Service}ModuleService = req.scope.resolve({SERVICE}_MODULE);

  try {
    const result = await service.createItem(validated);
    res.status(201).json({ data: result });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    res.status(400).json({ error: message });
  }
};
```

### Dynamic Route with Path Params

```typescript
// File: src/api/admin/{service}/items/[id]/route.ts

export const GET = async (req: MedusaRequest, res: MedusaResponse) => {
  const { id } = req.params;
  const service: {Service}ModuleService = req.scope.resolve({SERVICE}_MODULE);

  try {
    const item = await service.getItemById(id);
    if (!item) {
      return res.status(404).json({ error: "Item not found" });
    }
    res.json({ data: item });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    res.status(500).json({ error: message });
  }
};

export const DELETE = async (req: MedusaRequest, res: MedusaResponse) => {
  const { id } = req.params;
  const service: {Service}ModuleService = req.scope.resolve({SERVICE}_MODULE);

  try {
    await service.deleteItem(id);
    res.status(204).send();
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    res.status(500).json({ error: message });
  }
};
```

## Workflow Templates

### Simple Workflow

```typescript
import { createWorkflow, WorkflowResponse } from "@medusajs/framework/workflows-sdk";
import { processDataStep } from "./steps/process-data-step.js";

export const process{Entity}Workflow = createWorkflow(
  "process-{entity}",
  () => {
    const result = processDataStep();
    return new WorkflowResponse(result);
  }
);
```

### Multi-Step Workflow

```typescript
import { createWorkflow, WorkflowResponse } from "@medusajs/framework/workflows-sdk";
import { fetchDataStep } from "./steps/fetch-data-step.js";
import { transformDataStep } from "./steps/transform-data-step.js";
import { saveDataStep } from "./steps/save-data-step.js";

export const sync{Entity}Workflow = createWorkflow(
  "sync-{entity}",
  () => {
    // Step 1: Fetch
    const rawData = fetchDataStep();

    // Step 2: Transform
    const transformedData = transformDataStep({ data: rawData });

    // Step 3: Save
    const result = saveDataStep({ data: transformedData });

    return new WorkflowResponse({
      items_processed: result,
    });
  }
);
```

### Workflow Step Template

```typescript
import { createStep, StepResponse } from "@medusajs/framework/workflows-sdk";
import { {SERVICE}_MODULE } from "../../modules/{service}/index.js";
import type {Service}ModuleService from "../../modules/{service}/service.js";

type StepInput = {
  param1: string;
  param2?: number;
};

export const process{Entity}Step = createStep(
  "process-{entity}",
  async (input: StepInput, { container }) => {
    const service: {Service}ModuleService = container.resolve({SERVICE}_MODULE);

    const result = await service.processEntity(input);

    return new StepResponse(result);
  }
);
```

### Compensatable Step (with Rollback)

```typescript
import { createStep, StepResponse } from "@medusajs/framework/workflows-sdk";

type StepInput = {
  entityId: string;
};

export const updateEntityStep = createStep(
  "update-entity",
  async (input: StepInput, { container }) => {
    const service = container.resolve({SERVICE}_MODULE);

    // Store original state for rollback
    const originalState = await service.getEntity(input.entityId);
    
    // Perform update
    const updated = await service.updateEntity(input.entityId, { status: "processed" });

    return new StepResponse(updated, {
      entityId: input.entityId,
      originalState,
    });
  },
  async (rollbackData, { container }) => {
    if (!rollbackData) return;

    const service = container.resolve({SERVICE}_MODULE);
    
    // Restore original state
    await service.updateEntity(
      rollbackData.entityId,
      rollbackData.originalState
    );
  }
);
```

## OAuth Integration Template

### OAuth Service Methods

```typescript
class {Service}ModuleService extends MedusaService({
  {Service}Config,
}) {
  async getAuthorizationUrl(redirectUri: string): Promise<string> {
    const config = await this.getConfig();
    if (!config?.clientId) {
      throw new Error("Client ID not configured");
    }

    const params = new URLSearchParams({
      client_id: config.clientId,
      redirect_uri: redirectUri,
      response_type: "code",
      scope: "read write",
    });

    return `https://oauth.{service}.com/authorize?${params}`;
  }

  async handleOAuthCallback(code: string): Promise<{ success: boolean }> {
    const config = await this.getConfig();
    if (!config?.clientId || !config?.clientSecret) {
      throw new Error("OAuth credentials not configured");
    }

    const response = await axios.post("https://oauth.{service}.com/token", {
      grant_type: "authorization_code",
      code,
      client_id: config.clientId,
      client_secret: config.clientSecret,
    });

    await this.saveConfig({
      accessToken: response.data.access_token,
      refreshToken: response.data.refresh_token,
      expiresIn: response.data.expires_in,
      tokenUpdatedAt: new Date(),
    });

    return { success: true };
  }

  async refreshAccessToken(): Promise<string> {
    const config = await this.getConfig();
    if (!config?.refreshToken) {
      throw new Error("No refresh token available");
    }

    const response = await axios.post("https://oauth.{service}.com/token", {
      grant_type: "refresh_token",
      refresh_token: config.refreshToken,
      client_id: config.clientId,
      client_secret: config.clientSecret,
    });

    await this.saveConfig({
      accessToken: response.data.access_token,
      refreshToken: response.data.refresh_token,
      expiresIn: response.data.expires_in,
      tokenUpdatedAt: new Date(),
    });

    return response.data.access_token;
  }

  async getAccessToken(): Promise<string> {
    const config = await this.getConfig();
    if (!config?.accessToken) {
      throw new Error("Not authenticated");
    }

    // Check if token is expired
    if (config.tokenUpdatedAt && config.expiresIn) {
      const expiresAt = new Date(config.tokenUpdatedAt);
      expiresAt.setSeconds(expiresAt.getSeconds() + config.expiresIn);

      if (new Date() >= expiresAt) {
        return await this.refreshAccessToken();
      }
    }

    return config.accessToken;
  }
}
```

### OAuth Routes

```typescript
// src/api/admin/{service}/authorize/route.ts
import { z } from "zod";

const schema = z.object({
  redirect_uri: z.string().url(),
});

export const GET = async (req: MedusaRequest, res: MedusaResponse) => {
  const { redirect_uri } = schema.parse(req.query);
  const service: {Service}ModuleService = req.scope.resolve({SERVICE}_MODULE);

  try {
    const url = await service.getAuthorizationUrl(redirect_uri);
    res.json({ url });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    res.status(400).json({ error: message });
  }
};
```

```typescript
// src/api/admin/{service}/oauth/callback/route.ts
import { z } from "zod";

const schema = z.object({
  code: z.string(),
});

export const POST = async (req: MedusaRequest, res: MedusaResponse) => {
  const { code } = schema.parse(req.body);
  const service: {Service}ModuleService = req.scope.resolve({SERVICE}_MODULE);

  try {
    const result = await service.handleOAuthCallback(code);
    res.json(result);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    res.status(400).json({ error: message });
  }
};
```

## Utility Templates

### Data Mapper

```typescript
// src/modules/{service}/utils/mapper.ts

import type { Product } from "@medusajs/types";

export type External{Entity} = {
  id: string;
  name: string;
  price: number;
};

export function mapExternalToMedusa(
  external: External{Entity}
): Partial<Product> {
  return {
    title: external.name,
    handle: external.id.toLowerCase(),
    // Map other fields
  };
}

export function mapMedusaToExternal(
  medusa: Product
): External{Entity} {
  return {
    id: medusa.handle || medusa.id,
    name: medusa.title,
    price: 0, // Calculate from variants
  };
}
```

### Validation Utility

```typescript
// src/modules/{service}/utils/validation.ts

export function validateEmail(email: string): boolean {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

export function validatePhone(phone: string): boolean {
  const cleaned = phone.replace(/\D/g, "");
  return cleaned.length >= 10 && cleaned.length <= 15;
}
```

## Testing Templates

### Service Test

```typescript
import { describe, it, expect, beforeEach, vi } from "vitest";
import {Service}ModuleService from "../service.js";

describe("{Service}ModuleService", () => {
  let service: {Service}ModuleService;
  let mockLogger: any;
  let mockRepository: any;

  beforeEach(() => {
    mockLogger = {
      info: vi.fn(),
      error: vi.fn(),
    };

    mockRepository = {
      findOne: vi.fn(),
      create: vi.fn(),
      flush: vi.fn(),
    };

    service = new {Service}ModuleService({
      logger: mockLogger,
      manager: {
        getRepository: () => mockRepository,
      } as any,
    });
  });

  it("should get config", async () => {
    const mockConfig = { id: "{service}_config", apiKey: "test" };
    mockRepository.findOne.mockResolvedValue(mockConfig);

    const result = await service.getConfig();

    expect(result).toEqual(mockConfig);
    expect(mockRepository.findOne).toHaveBeenCalledWith({ id: "{service}_config" });
  });
});
```

### Mapper Test

```typescript
import { describe, it, expect } from "vitest";
import { mapExternalToMedusa } from "../utils/mapper.js";

describe("{Service} Mapper", () => {
  it("should map external entity to Medusa format", () => {
    const external = {
      id: "EXT123",
      name: "Test Product",
      price: 99.99,
    };

    const result = mapExternalToMedusa(external);

    expect(result.title).toBe("Test Product");
    expect(result.handle).toBe("ext123");
  });
});
```
