---
name: backend-controller-pattern-admin
description: Provides NestJS Controller patterns for Admin-facing endpoints. This skill should be used when building controllers protected by authentication and role-based authorization.
---

# Admin Controller Pattern (NestJS)

This skill outlines the specific patterns for building **Admin** controllers in `erify_api`. These controllers are protected by authentication AND role-based authorization (System Admin).

## Core Principles

1.  **Inheritance**: All admin controllers MUST extend `BaseAdminController`.
2.  **Authorization**: Automatically protected by `@AdminProtected()` via the base class.
3.  **Response Wrapper**: Use `@AdminResponse()` and `@AdminPaginatedResponse()` instead of generic Zod decorators.
4.  **Path Structure**: All routes must start with `admin/`.

## Base Controller

`BaseAdminController` provides:
*   `@AdminProtected()` decorator application.
*   `createPaginatedResponse()` helper.
*   `ensureResourceExists()` and `ensureFieldExists()` helpers.

## Implementation Pattern

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

## Checklist

- [ ] Controller extends `BaseAdminController`.
- [ ] Route prefix is `admin/<resource>`.
- [ ] Uses `@AdminResponse` / `@AdminPaginatedResponse`.
- [ ] Uses `UidValidationPipe` for ID parameters.
- [ ] Uses `ensureResourceExists` for 404 checks.
