---
name: backend-controller-pattern-me
description: Provides NestJS Controller patterns for User-facing (Me) endpoints. This skill should be used when building endpoints for authenticated users to interact with their own resources.
---

# User (Me) Controller Pattern (NestJS)

This skill outlines the patterns for **User-facing** controllers in `erify_api`. These endpoints are for authenticated users interacting with *their own* resources.

## Core Principles

1.  **Standard Controller**: Standard NestJS controller (no specific base class required, though consistent patterns apply).
2.  **Context**: ALWAYS use `@CurrentUser()` to scope operations to the authenticated user.
3.  **Path Structure**: Routes typically start with `me/` or implied user context.

## Implementation Pattern

```typescript
import { Controller, Get, Post, Body } from '@nestjs/common';
import { CurrentUser } from '@eridu/auth-sdk/adapters/nestjs/current-user.decorator';
import { AuthenticatedUser } from '@/lib/auth/jwt-auth.guard';
import { ZodResponse } from '@/lib/decorators/zod-response.decorator';

@Controller('me/profile')
export class ProfileController {
  constructor(private readonly userService: UserService) {}

  @Get()
  @ZodResponse(ProfileResponseDto)
  async getProfile(@CurrentUser() user: AuthenticatedUser) {
    // Validate user context
    return this.userService.getUserById(user.id);
  }

  @Post()
  @ZodResponse(ProfileResponseDto)
  async updateProfile(
    @CurrentUser() user: AuthenticatedUser,
    @Body() body: UpdateProfileDto
  ) {
    // ALWAYS use user.id from token, never from body/params for 'me' routes
    return this.userService.updateUser(user.id, body);
  }
}
```

## Checklist

- [ ] Route starts with `me/` or is user-scoped.
- [ ] Uses `@CurrentUser()` to get user ID.
- [ ] NEVER trusts user ID from request body/params for self-operations.
- [ ] Uses `@ZodResponse` or `@ZodPaginatedResponse`.
