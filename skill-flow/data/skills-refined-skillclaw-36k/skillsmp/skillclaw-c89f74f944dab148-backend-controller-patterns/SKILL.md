---
name: backend-controller-patterns
description: Use this skill when building NestJS controllers for both user-facing and admin-facing endpoints, ensuring proper authentication and authorization practices.
---

# Backend Controller Patterns (NestJS)

This skill outlines the patterns for building both **User-facing** and **Admin-facing** controllers in a NestJS application. It provides guidelines for structuring endpoints, handling authentication, and ensuring proper authorization.

## Core Principles

1. **Controller Structure**:
   - User controllers should use `@CurrentUser()` to scope operations to the authenticated user.
   - Admin controllers must extend a base class (`BaseAdminController`) that handles role-based authorization.

2. **Path Structure**:
   - User routes typically start with `me/` to indicate user-specific actions.
   - Admin routes must start with `admin/` to indicate administrative actions.

3. **Response Handling**:
   - User controllers should use `@ZodResponse()` for response validation.
   - Admin controllers should use `@AdminResponse()` and `@AdminPaginatedResponse()` for response handling.

## Implementation Patterns

### User Controller Example

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
    return this.userService.getUserById(user.id);
  }

  @Post()
  @ZodResponse(ProfileResponseDto)
  async updateProfile(
    @CurrentUser() user: AuthenticatedUser,
    @Body() body: UpdateProfileDto
  ) {
    return this.userService.updateUser(user.id, body);
  }
}
```

### Admin Controller Example

```typescript
import { Body, Controller, Delete, Get, HttpStatus, Param, Post, Query } from '@nestjs/common';
import { BaseAdminController } from '@/admin/base-admin.controller';
import { AdminResponse, AdminPaginatedResponse } from '@/admin/decorators/admin-response.decorator';
import { PaginationQueryDto } from '@/lib/pagination/pagination.schema';
import { UidValidationPipe } from '@/lib/pipes/uid-validation.pipe';

@Controller('admin/users')
export class AdminUserController extends BaseAdminController {
  constructor(private readonly userService: UserService) {
    super();
  }

  @Get()
  @AdminPaginatedResponse(UserDto, 'List users with pagination')
  async listUsers(@Query() query: PaginationQueryDto) {
    const [data, total] = await Promise.all([
      this.userService.listUsers(query),
      this.userService.countUsers(),
    ]);
    return this.createPaginatedResponse(data, total, query);
  }

  @Get(':id')
  @AdminResponse(UserDto, HttpStatus.OK, 'Get user details')
  async getUser(
    @Param('id', new UidValidationPipe(UserService.UID_PREFIX, 'User'))
    id: string,
  ) {
    const user = await this.userService.getUserById(id);
    this.ensureResourceExists(user, 'User', id);
    return user;
  }

  @Post()
  @AdminResponse(UserDto, HttpStatus.CREATED, 'Create user')
  async createUser(@Body() body: CreateUserDto) {
    return this.userService.createUser(body);
  }

  @Delete(':id')
  @AdminResponse(UserDto, HttpStatus.NO_CONTENT, 'Delete user')
  async deleteUser(@Param('id') id: string) {
    await this.userService.deleteUser(id);
  }
}
```

## Checklist

- [ ] User routes start with `me/` and use `@CurrentUser()` for user context.
- [ ] Admin routes start with `admin/` and extend `BaseAdminController`.
- [ ] Use appropriate response decorators for user and admin controllers.