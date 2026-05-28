---
name: backend-controller-patterns
description: Use this skill when building NestJS controllers for both user-facing and admin-facing endpoints, ensuring proper authentication and authorization patterns.
---

# Backend Controller Patterns (NestJS)

This skill outlines the patterns for building both **User-facing** and **Admin** controllers in `erify_api`. 

## User (Me) Controller Pattern

These endpoints are for authenticated users interacting with *their own* resources.

### Core Principles

1. **Standard Controller**: Use a standard NestJS controller without a specific base class, but follow consistent patterns.
2. **Context**: Always use `@CurrentUser()` to scope operations to the authenticated user.
3. **Path Structure**: Routes typically start with `me/` or imply user context.

### Implementation Pattern

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

### Checklist

- [ ] Route starts with `me/` or is user-scoped.
- [ ] Uses `@CurrentUser()` to get user ID.
- [ ] Never trusts user ID from request body/params for self-operations.
- [ ] Uses `@ZodResponse` or `@ZodPaginatedResponse`.

## Admin Controller Pattern

These controllers are protected by authentication and role-based authorization (System Admin).

### Core Principles

1. **Inheritance**: All admin controllers must extend `BaseAdminController`.
2. **Authorization**: Automatically protected by `@AdminProtected()` via the base class.
3. **Response Wrapper**: Use `@AdminResponse()` and `@AdminPaginatedResponse()` instead of generic Zod decorators.
4. **Path Structure**: All routes must start with `admin/`.

### Base Controller

`BaseAdminController` provides:
* `@AdminProtected()` decorator application.
* `createPaginatedResponse()` helper.
* `ensureResourceExists()` and `ensureFieldExists()` helpers.

### Implementation Pattern

```typescript
import { Body, Controller, Delete, Get, HttpStatus, Param, Patch, Post, Query } from '@nestjs/common';
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
  @AdminResponse(undefined, HttpStatus.NO_CONTENT, 'Delete user')
  async deleteUser(
    @Param('id', new UidValidationPipe(UserService.UID_PREFIX, 'User'))
    id: string,
  ) {
    await this.userService.deleteUser(id);
  }
}
```

### Checklist

- [ ] Controller extends `BaseAdminController`.
- [ ] Route prefix is `admin/<resource>`.
- [ ] Uses `@AdminResponse` / `@AdminPaginatedResponse`.
- [ ] Uses `UidValidationPipe` for ID parameters.
- [ ] Uses `ensureResourceExists` for 404 checks.