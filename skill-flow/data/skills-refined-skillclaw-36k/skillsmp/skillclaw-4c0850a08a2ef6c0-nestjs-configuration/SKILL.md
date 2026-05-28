---
name: nestjs-configuration
description: Use this skill when you need to set up and validate environment variables in a NestJS application.
---

# NestJS Configuration Standards

## Setup

1. **Library**: Use `@nestjs/config`.
2. **Initialization**: Import `ConfigModule.forRoot({ isGlobal: true })` in `AppModule`.

## Validation

- **Mandatory**: Validate environment variables at startup.
- **Tool**: Use `joi` or a custom validation class.
- **Effect**: The app **must crash** immediately if a required env var (e.g., `DB_URL`) is missing.

```typescript
// app.module.ts
ConfigModule.forRoot({
  validationSchema: Joi.object({
    NODE_ENV: Joi.string()
      .valid('development', 'production')
      .default('development'),
    PORT: Joi.number().default(3000),
    DATABASE_URL: Joi.string().required(),
  }),
});
```

## Usage

- **Injection**: Inject `ConfigService` to access values.
- **Typing**: Avoid magic strings. Use a type-safe getter helper or a dedicated configuration object/interface.
- **Secrets**: Never commit `.env` files. Add `.env*` to `.gitignore`.