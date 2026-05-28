---
name: validation
description: Schema validation patterns for Zod and class-validator in NestJS. Detect which library the project uses and follow its patterns. Use for DTO validation, request/response validation, custom validators, and TypeScript type inference.
---

# Validation Skill

> **Load this skill** before implementing input validation, DTOs, or schema definitions.

## Library Detection (CRITICAL)

**ALWAYS detect and use the project's existing validation library. NEVER mix validation libraries in the same project.**

| Detection Method | Library |
|------------------|---------|
| `zod` or `nestjs-zod` in package.json | **Zod** |
| `class-validator` + `class-transformer` in package.json | **class-validator** |

```bash
# Quick detection commands
grep -E "\"zod\"|\"nestjs-zod\"" package.json     # Zod
grep -E "\"class-validator\"" package.json        # class-validator
```

**If no validation library exists yet:**
- For new NestJS projects: Recommend `class-validator` (native NestJS support)
- For schema-first or non-NestJS: Recommend `zod` (better type inference)
- If using NestJS with Zod: Use `nestjs-zod` for seamless integration

---

## Quick Comparison

| Feature | Zod | class-validator |
|---------|-----|-----------------|
| **Approach** | Schema-first, functional | Decorator-based, class-first |
| **Type Inference** | Excellent (`z.infer<typeof schema>`) | Requires separate interface |
| **NestJS Integration** | Via `nestjs-zod` | Native `ValidationPipe` |
| **Bundle Size** | ~12kb | ~40kb (with class-transformer) |
| **Custom Validation** | `.refine()`, `.superRefine()` | `@Validate()`, `registerDecorator` |
| **Composability** | Excellent (schemas are values) | Limited (class inheritance) |
| **Error Messages** | Customizable per field | Customizable per decorator |
| **Async Validation** | `.refineAsync()` | Built-in async support |

### When to Choose

| Use Case | Recommended |
|----------|-------------|
| Standard NestJS API | class-validator |
| Schema-first design | Zod |
| Heavy type inference needs | Zod |
| Existing NestJS codebase | Match existing |
| OpenAPI/Swagger integration | class-validator (better decorators) |
| Shared frontend/backend schemas | Zod |

---

## Zod Patterns

### Installation

```bash
# Basic Zod
bun add zod

# For NestJS integration
bun add zod nestjs-zod
```

### Schema Definitions

```typescript
import { z } from 'zod';

// Primitives
const stringSchema = z.string();
const numberSchema = z.number();
const booleanSchema = z.boolean();
const dateSchema = z.date();

// String validations
const emailSchema = z.string().email();
const urlSchema = z.string().url();
const uuidSchema = z.string().uuid();
const minMaxSchema = z.string().min(3).max(100);
const regexSchema = z.string().regex(/^[A-Z]/);

// Number validations
const positiveSchema = z.number().positive();
const intSchema = z.number().int();
const rangeSchema = z.number().min(0).max(100);

// Enums
const statusSchema = z.enum(['pending', 'active', 'completed']);
// Or from TypeScript enum
enum Status { Pending, Active, Completed }
const nativeEnumSchema = z.nativeEnum(Status);

// Arrays
const tagsSchema = z.array(z.string()).min(1).max(10);
const uniqueSchema = z.array(z.string()).refine(
  (items) => new Set(items).size === items.length,
  { message: 'Array must contain unique items' }
);

// Objects
const userSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().positive().optional(),
  role: z.enum(['user', 'admin']).default('user'),
  tags: z.array(z.string()).default([]),
  metadata: z.record(z.string(), z.unknown()).optional(),
});

// Type inference - ALWAYS use this pattern
type User = z.infer<typeof userSchema>;
// Result: { id: string; email: string; name: string; age?: number; role: 'user' | 'admin'; tags: string[]; metadata?: Record<string, unknown> }
```

### Parse vs SafeParse

```typescript
// parse() - throws ZodError on failure
try {
  const user = userSchema.parse(unknownData);
  // user is fully typed
} catch (error) {
  if (error instanceof z.ZodError) {
    console.error(error.errors);
  }
}

// safeParse() - returns result object (PREFERRED for user input)
const result = userSchema.safeParse(unknownData);
if (result.success) {
  const user = result.data; // fully typed
} else {
  const errors = result.error.errors; // ZodIssue[]
}

// parseAsync() / safeParseAsync() for async refinements
const asyncResult = await asyncSchema.safeParseAsync(data);
```

### Refinements and Transforms

```typescript
// refine() - custom validation
const passwordSchema = z.string()
  .min(8)
  .refine(
    (val) => /[A-Z]/.test(val),
    { message: 'Must contain uppercase letter' }
  )
  .refine(
    (val) => /[0-9]/.test(val),
    { message: 'Must contain number' }
  );

// superRefine() - access context, add multiple issues
const confirmPasswordSchema = z.object({
  password: z.string().min(8),
  confirmPassword: z.string(),
}).superRefine((data, ctx) => {
  if (data.password !== data.confirmPassword) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      message: 'Passwords must match',
      path: ['confirmPassword'],
    });
  }
});

// transform() - modify data after validation
const lowercaseEmailSchema = z.string()
  .email()
  .transform((val) => val.toLowerCase());

const dateStringSchema = z.string()
  .transform((val) => new Date(val))
  .refine((date) => !isNaN(date.getTime()), { message: 'Invalid date' });

// pipe() - chain schemas
const stringToNumber = z.string()
  .transform((val) => parseInt(val, 10))
  .pipe(z.number().positive());
```

### Schema Composition

```typescript
// Extend objects
const baseUserSchema = z.object({
  email: z.string().email(),
  name: z.string(),
});

const createUserSchema = baseUserSchema.extend({
  password: z.string().min(8),
});

const updateUserSchema = baseUserSchema.partial(); // All fields optional

// Pick and omit
const userResponseSchema = userSchema.omit({ password: true });
const userSummarySchema = userSchema.pick({ id: true, name: true });

// Merge schemas
const withTimestamps = z.object({
  createdAt: z.date(),
  updatedAt: z.date(),
});
const fullUserSchema = userSchema.merge(withTimestamps);

// Union types
const idSchema = z.union([z.string().uuid(), z.number().int().positive()]);
// Shorthand
const idShortSchema = z.string().uuid().or(z.number().int().positive());

// Discriminated unions (better error messages)
const eventSchema = z.discriminatedUnion('type', [
  z.object({ type: z.literal('click'), x: z.number(), y: z.number() }),
  z.object({ type: z.literal('scroll'), delta: z.number() }),
  z.object({ type: z.literal('keypress'), key: z.string() }),
]);
```

### NestJS Integration with nestjs-zod

```typescript
// Install: bun add nestjs-zod

// main.ts - Global setup
import { ZodValidationPipe } from 'nestjs-zod';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalPipes(new ZodValidationPipe());
  await app.listen(3000);
}

// create-user.dto.ts
import { createZodDto } from 'nestjs-zod';
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  name: z.string().min(1).max(100),
});

// DTO class extends from schema - gets type inference automatically
export class CreateUserDto extends createZodDto(CreateUserSchema) {}

// user.controller.ts
@Controller('users')
export class UserController {
  @Post()
  async create(@Body() dto: CreateUserDto) {
    // dto is fully typed and validated
    return this.userService.create(dto);
  }
}
```

### Error Formatting

```typescript
// Custom error formatter
function formatZodError(error: z.ZodError): Record<string, string[]> {
  const formatted: Record<string, string[]> = {};
  
  for (const issue of error.errors) {
    const path = issue.path.join('.') || '_root';
    if (!formatted[path]) {
      formatted[path] = [];
    }
    formatted[path].push(issue.message);
  }
  
  return formatted;
}

// Usage
const result = schema.safeParse(data);
if (!result.success) {
  const errors = formatZodError(result.error);
  // { "email": ["Invalid email"], "password": ["Too short"] }
}

// Or use built-in flatten
const flattened = result.error.flatten();
// { formErrors: [], fieldErrors: { email: ["Invalid email"] } }
```

---

## class-validator Patterns

### Installation

```bash
bun add class-validator class-transformer
```

### Common Decorators

```typescript
import {
  IsString,
  IsEmail,
  IsNumber,
  IsInt,
  IsPositive,
  IsBoolean,
  IsDate,
  IsEnum,
  IsArray,
  IsOptional,
  IsNotEmpty,
  IsUUID,
  IsUrl,
  Min,
  Max,
  MinLength,
  MaxLength,
  Matches,
  ArrayMinSize,
  ArrayMaxSize,
  ValidateNested,
} from 'class-validator';
import { Type, Transform } from 'class-transformer';

// Basic DTO
export class CreateUserDto {
  @IsEmail()
  @Transform(({ value }) => value?.toLowerCase())
  email: string;

  @IsString()
  @MinLength(8)
  @MaxLength(100)
  @Matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, {
    message: 'Password must contain uppercase, lowercase, and number',
  })
  password: string;

  @IsString()
  @IsNotEmpty()
  @MaxLength(100)
  name: string;

  @IsOptional()
  @IsInt()
  @IsPositive()
  @Max(150)
  age?: number;

  @IsOptional()
  @IsEnum(UserRole)
  role?: UserRole;

  @IsOptional()
  @IsArray()
  @IsString({ each: true })
  @ArrayMinSize(0)
  @ArrayMaxSize(10)
  tags?: string[];
}

enum UserRole {
  User = 'user',
  Admin = 'admin',
}
```

### Nested Validation

```typescript
// address.dto.ts
export class AddressDto {
  @IsString()
  @IsNotEmpty()
  street: string;

  @IsString()
  @IsNotEmpty()
  city: string;

  @IsString()
  @MinLength(2)
  @MaxLength(2)
  country: string;

  @IsOptional()
  @IsString()
  postalCode?: string;
}

// user.dto.ts
export class CreateUserWithAddressDto {
  @IsEmail()
  email: string;

  @IsString()
  name: string;

  // CRITICAL: Both decorators required for nested objects
  @ValidateNested()
  @Type(() => AddressDto)
  address: AddressDto;

  // For arrays of nested objects
  @IsOptional()
  @IsArray()
  @ValidateNested({ each: true })
  @Type(() => AddressDto)
  additionalAddresses?: AddressDto[];
}
```

### Custom Validators

```typescript
import {
  registerDecorator,
  ValidationOptions,
  ValidationArguments,
  ValidatorConstraint,
  ValidatorConstraintInterface,
} from 'class-validator';

// Simple custom decorator
export function IsStrongPassword(validationOptions?: ValidationOptions) {
  return function (object: object, propertyName: string) {
    registerDecorator({
      name: 'isStrongPassword',
      target: object.constructor,
      propertyName: propertyName,
      options: validationOptions,
      validator: {
        validate(value: unknown) {
          if (typeof value !== 'string') return false;
          return (
            value.length >= 8 &&
            /[A-Z]/.test(value) &&
            /[a-z]/.test(value) &&
            /[0-9]/.test(value)
          );
        },
        defaultMessage() {
          return 'Password must be 8+ chars with uppercase, lowercase, and number';
        },
      },
    });
  };
}

// Usage
export class RegisterDto {
  @IsStrongPassword()
  password: string;
}

// Complex validator with constraints (for async or cross-field validation)
@ValidatorConstraint({ name: 'isEmailUnique', async: true })
export class IsEmailUniqueConstraint implements ValidatorConstraintInterface {
  constructor(private readonly userService: UserService) {}

  async validate(email: string): Promise<boolean> {
    const user = await this.userService.findByEmail(email);
    return !user; // Valid if no user found
  }

  defaultMessage(): string {
    return 'Email already exists';
  }
}

// Register as decorator
export function IsEmailUnique(validationOptions?: ValidationOptions) {
  return function (object: object, propertyName: string) {
    registerDecorator({
      target: object.constructor,
      propertyName: propertyName,
      options: validationOptions,
      constraints: [],
      validator: IsEmailUniqueConstraint,
    });
  };
}

// Cross-field validation
export function Match(property: string, validationOptions?: ValidationOptions) {
  return function (object: object, propertyName: string) {
    registerDecorator({
      name: 'match',
      target: object.constructor,
      propertyName: propertyName,
      constraints: [property],
      options: validationOptions,
      validator: {
        validate(value: unknown, args: ValidationArguments) {
          const [relatedPropertyName] = args.constraints;
          const relatedValue = (args.object as Record<string, unknown>)[relatedPropertyName];
          return value === relatedValue;
        },
        defaultMessage(args: ValidationArguments) {
          const [relatedPropertyName] = args.constraints;
          return `${args.property} must match ${relatedPropertyName}`;
        },
      },
    });
  };
}

// Usage
export class ChangePasswordDto {
  @IsString()
  @MinLength(8)
  password: string;

  @IsString()
  @Match('password')
  confirmPassword: string;
}
```

### Validation Groups

```typescript
export class UpdateUserDto {
  @IsEmail({ groups: ['create', 'update'] })
  email: string;

  @IsString()
  @MinLength(8)
  @IsNotEmpty({ groups: ['create'] }) // Required only on create
  @IsOptional({ groups: ['update'] })  // Optional on update
  password?: string;

  @IsString()
  name: string;
}

// In controller
@Post()
async create(@Body(new ValidationPipe({ groups: ['create'] })) dto: UpdateUserDto) {}

@Patch(':id')
async update(@Body(new ValidationPipe({ groups: ['update'] })) dto: UpdateUserDto) {}
```

### Conditional Validation

```typescript
import { ValidateIf } from 'class-validator';

export class PaymentDto {
  @IsEnum(PaymentMethod)
  method: PaymentMethod;

  // Only validate if method is 'card'
  @ValidateIf((o) => o.method === PaymentMethod.Card)
  @IsString()
  @Matches(/^\d{16}$/)
  cardNumber?: string;

  @ValidateIf((o) => o.method === PaymentMethod.Card)
  @IsString()
  @Matches(/^\d{3,4}$/)
  cvv?: string;

  // Only validate if method is 'bank'
  @ValidateIf((o) => o.method === PaymentMethod.Bank)
  @IsString()
  @IsNotEmpty()
  accountNumber?: string;
}

enum PaymentMethod {
  Card = 'card',
  Bank = 'bank',
  Crypto = 'crypto',
}
```

### NestJS ValidationPipe Configuration

```typescript
// main.ts - Global setup
import { ValidationPipe } from '@nestjs/common';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  app.useGlobalPipes(new ValidationPipe({
    whitelist: true,              // Strip non-decorated properties
    forbidNonWhitelisted: true,   // Throw if non-decorated properties present
    transform: true,              // Transform payloads to DTO instances
    transformOptions: {
      enableImplicitConversion: true, // Convert query params to proper types
    },
    exceptionFactory: (errors) => {
      // Custom error format
      const messages = errors.map((error) => ({
        field: error.property,
        errors: Object.values(error.constraints || {}),
      }));
      return new BadRequestException({ message: 'Validation failed', errors: messages });
    },
  }));
  
  await app.listen(3000);
}

// Or configure per-module in app.module.ts
@Module({
  providers: [
    {
      provide: APP_PIPE,
      useValue: new ValidationPipe({
        whitelist: true,
        forbidNonWhitelisted: true,
        transform: true,
      }),
    },
  ],
})
export class AppModule {}
```

### Whitelist Mode (CRITICAL for Security)

```typescript
// ❌ WITHOUT whitelist - attacker can inject fields
// POST /users { "email": "...", "role": "admin", "isVerified": true }
// These extra fields pass through!

// ✅ WITH whitelist: true - only decorated properties allowed
export class CreateUserDto {
  @IsEmail()
  email: string;  // Only this gets through

  @IsString()
  name: string;   // And this
  
  // role and isVerified are stripped!
}

// ✅ WITH forbidNonWhitelisted: true - throws on extra fields
// Returns 400 Bad Request if any non-decorated properties present
```

---

## NestJS Integration Summary

### class-validator (Native)

```typescript
// main.ts
app.useGlobalPipes(new ValidationPipe({
  whitelist: true,
  forbidNonWhitelisted: true,
  transform: true,
}));

// dto.ts
export class CreateUserDto {
  @IsEmail()
  email: string;
}

// controller.ts
@Post()
create(@Body() dto: CreateUserDto) {} // Validated automatically
```

### Zod (via nestjs-zod)

```typescript
// main.ts
import { ZodValidationPipe } from 'nestjs-zod';
app.useGlobalPipes(new ZodValidationPipe());

// dto.ts
import { createZodDto } from 'nestjs-zod';
const schema = z.object({ email: z.string().email() });
export class CreateUserDto extends createZodDto(schema) {}

// controller.ts
@Post()
create(@Body() dto: CreateUserDto) {} // Validated automatically
```

### Error Response Format (Both)

```json
{
  "statusCode": 400,
  "message": "Validation failed",
  "errors": [
    {
      "field": "email",
      "errors": ["email must be a valid email address"]
    },
    {
      "field": "password",
      "errors": ["password must be at least 8 characters"]
    }
  ]
}
```

---

## Best Practices

### 1. Define Once, Infer Types

```typescript
// ✅ Zod - schema is the source of truth
const userSchema = z.object({ email: z.string().email() });
type User = z.infer<typeof userSchema>;

// ✅ class-validator - DTO is the source of truth
export class UserDto {
  @IsEmail()
  email: string;
}
// Type is the class itself
```

### 2. Always Validate at API Boundaries

```typescript
// ✅ Validate incoming requests
@Post()
create(@Body() dto: CreateUserDto) {}

// ✅ Validate query parameters
@Get()
findAll(@Query() query: PaginationDto) {}

// ✅ Validate path parameters
@Get(':id')
findOne(@Param('id', ParseUUIDPipe) id: string) {}
```

### 3. Use SafeParse for User Input (Zod)

```typescript
// ✅ Handle validation errors gracefully
const result = schema.safeParse(userInput);
if (!result.success) {
  return { errors: formatZodError(result.error) };
}
// Use result.data

// ❌ Don't let parse() throw in request handlers
const data = schema.parse(userInput); // May throw!
```

### 4. Whitelist Mode in NestJS (class-validator)

```typescript
// ✅ ALWAYS enable for security
new ValidationPipe({
  whitelist: true,           // Strip unknown properties
  forbidNonWhitelisted: true, // Or throw on unknown
});
```

### 5. Compose Schemas/DTOs for Reuse

```typescript
// ✅ Zod - compose with extend/merge
const baseSchema = z.object({ id: z.string() });
const createSchema = baseSchema.omit({ id: true });
const updateSchema = baseSchema.partial();

// ✅ class-validator - use inheritance or mapped types
export class UpdateUserDto extends PartialType(CreateUserDto) {}
export class UserResponseDto extends OmitType(UserDto, ['password']) {}
```

---

## Quick Checklist

Before shipping validation code:

- [ ] Using project's existing validation library (not mixing)
- [ ] All user input validated at API boundaries
- [ ] Types inferred from schemas (Zod) or DTOs (class-validator)
- [ ] Whitelist mode enabled in NestJS
- [ ] Custom error messages are user-friendly
- [ ] Nested objects use proper validation (`@ValidateNested` + `@Type` or nested Zod schemas)
- [ ] Sensitive fields (passwords) have proper constraints
- [ ] Async validators used for database checks (unique email, etc.)

## When to Use This Skill

Load this skill when:
- Implementing input validation for APIs
- Creating DTOs for NestJS endpoints
- Building schema definitions for data parsing
- Adding custom validation rules
- Setting up global validation pipes
- Debugging validation errors
- Choosing between Zod and class-validator
