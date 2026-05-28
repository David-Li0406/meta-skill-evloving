---
name: backend-controller-pattern-backdoor
description: Provides NestJS Controller patterns for Backdoor (Service-to-Service) endpoints. This skill should be used when building endpoints that require API Key authentication for internal communication.
---

# Backdoor Controller Pattern (NestJS)

This skill outlines the patterns for **Backdoor** controllers in `erify_api`. These endpoints are designed for service-to-service communication or internal tools that bypass standard JWT authentication in favor of API Key authentication.

## Core Principles

1.  **Inheritance**: All backdoor controllers MUST extend `BaseBackdoorController`.
2.  **Authentication**: Automatically authenticated via API Key using the `@Backdoor()` decorator (from base class).
3.  **Path Structure**: All routes must start with `backdoor/`.

## Base Controller

`BaseBackdoorController` provides:
*   `@Backdoor()` decorator application (skips JWT guard, applies API Key guard).

## Implementation Pattern

```typescript
import { Controller, Get, Param, UseGuards } from '@nestjs/common';
import { BaseBackdoorController } from '@/backdoor/base-backdoor.controller';
import { ZodResponse } from '@/lib/decorators/zod-response.decorator';

@Controller('backdoor/users')
export class BackdoorUserController extends BaseBackdoorController {
  constructor(private readonly userService: UserService) {
    super();
  }

  @Get(':ext_id')
  @ZodResponse(UserDto)
  async getUserByExtId(@Param('ext_id') extId: string) {
    return this.userService.getUserByExtId(extId);
  }
}
```

## Checklist

- [ ] Controller extends `BaseBackdoorController`.
- [ ] Route prefix is `backdoor/<resource>`.
- [ ] Uses `@ZodResponse` for serialization.
- [ ] NO `@CurrentUser` decorator (concept doesn't exist for API keys).
