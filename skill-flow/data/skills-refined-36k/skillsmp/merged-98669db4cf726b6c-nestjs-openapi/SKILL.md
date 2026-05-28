---
name: nestjs-openapi
description: Use this skill for automating Swagger documentation and managing OpenAPI standards in NestJS applications.
---

# OpenAPI & Documentation

## Swagger (OpenAPI)

- **Automation**: **ALWAYS** use the Nest CLI Plugin (`@nestjs/swagger/plugin`).
  - **Benefit**: Auto-generates `@ApiProperty` for DTOs and response types, reducing boilerplate by 50%.
  - **Config**: Update `nest-cli.json` to include `"plugins": ["@nestjs/swagger"]`.
- **Versioning**: Maintain separate Swagger docs for `v1`, `v2` if breaking changes occur.

## Response Documentation

- **Strictness**: Every controller method must have `@ApiResponse({ status: 200, type: UserDto })`.
- **Generic Wrappers**: Define `ApiPaginatedResponse<T>` decorators to document generic `PageDto<T>` returns properly.
  - **Technique**: Use `ApiExtraModels` + `getSchemaPath()` in the custom decorator to handle the generic `T` reference.

## Advanced Patterns

- **Polymorphism**: Use `@ApiExtraModels` and `getSchemaPath` for `oneOf`/`anyOf` union types.
- **File Uploads**: Document `multipart/form-data` explicitly.
  - **Decorator**: `@ApiConsumes('multipart/form-data')`.
  - **Body**: `@ApiBody({ schema: { type: 'object', properties: { file: { type: 'string', format: 'binary' } } } })`.
- **Authentication**: Specify granular security schemes per route/controller.
  - **Types**: Use `@ApiBearerAuth()` or `@ApiSecurity('api-key')`, ensuring they match `DocumentBuilder().addBearerAuth()`.
- **Enums**: Force named enums for reusable schema references.
  - **Code**: `@ApiProperty({ enum: MyEnum, enumName: 'MyEnum' })`.

## Operation Grouping

- **Tags**: Mandatory `@ApiTags('domains')` on every Controller to group endpoints logically.
- **Multiple Docs**: Generate separate docs for different audiences (e.g., Public vs Internal).

  ```typescript
  SwaggerModule.createDocument(app, config, { include: [PublicModule] }); // /api/docs
  SwaggerModule.createDocument(app, adminConfig, { include: [AdminModule] }); // /admin/docs
  ```

## Self-Documentation

- **Compodoc**: Use `@compodoc/compodoc` to generate static documentation of the module graph, services, and dependencies.
  - **Use Case**: Useful for new developer onboarding and architectural review.