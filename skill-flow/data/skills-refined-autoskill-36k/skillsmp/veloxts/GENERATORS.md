# VeloxTS Generators Guide

## AI Agent Recommended Workflow

When creating new entities, the **recommended approach** is:

1. **Design and add the Prisma model** directly to `prisma/schema.prisma`
2. **Run `velox make namespace EntityName`** to generate procedures

This ensures complete, production-ready code because the AI can design the full schema based on requirements.

```bash
# Example: Creating a Post entity

# Step 1: AI adds model to prisma/schema.prisma
model Post {
  id        String   @id @default(uuid())
  title     String
  content   String
  published Boolean  @default(false)
  authorId  String
  author    User     @relation(fields: [authorId], references: [id])
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  @@map("posts")
}

# Step 2: Generate procedures for the existing model
velox make namespace Post --example
```

## Decision Tree: Which Generator?

```
Do you need a new database entity?
├── YES (AI workflow) → 1. Design Prisma model in schema.prisma
│                       2. velox make namespace EntityName --example
│                       Creates: Schema + Procedures for existing model
│
├── YES (Interactive) → velox make resource EntityName -i
│                       Prompts for fields, creates everything
│
└── NO → What do you need?
         ├── Single API endpoint → velox make procedure
         ├── Validation schema only → velox make schema
         ├── Database model only → velox make model
         ├── Background job → velox make job
         ├── Email template → velox make mail
         ├── Auth guard → velox make guard
         ├── Auth policy → velox make policy
         ├── Middleware → velox make middleware
         ├── Service class → velox make service
         ├── Custom exception → velox make exception
         └── Scheduled task → velox make task
```

## Generator Comparison

| Generator | Creates | Use When |
|-----------|---------|----------|
| `namespace` | Schema + Procedures + Tests | **AI agents** or existing Prisma model |
| `resource -i` | Prisma + Schema + Procedures + Tests | **Human interactive** field definition |
| `resource` | Scaffolds with TODOs | Quick start (fields needed manually) |
| `procedure` | Procedures (inline schemas) | Single endpoint, quick prototype |
| `schema` | Zod schema file | Standalone validation |
| `model` | Prisma model | Database-only change |

## Namespace Generator [AI RECOMMENDED]

Best choice for AI agents. Works with models you've already defined.

```bash
# After adding model to schema.prisma:
velox make namespace Post --example

# With tests
velox make namespace Order --example --with-tests

# Short form
velox m ns Product -e -t
```

### What It Creates

```
src/
├── procedures/
│   ├── posts.ts              # CRUD procedures
│   └── __tests__/
│       └── posts.test.ts     # Unit tests
└── schemas/
    └── post.ts               # Zod validation
```

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--example` | `-e` | Include example CRUD procedures |
| `--with-tests` | `-t` | Generate test file (default: true) |
| `--skip-registration` | `-S` | Don't auto-register in router |

## Resource Generator [HUMAN INTERACTIVE]

Best for humans defining fields interactively via `-i` flag.

**Important:** Without `-i`, creates scaffolds with TODO placeholders that require manual completion.

```bash
# RECOMMENDED: Interactive mode (prompts for fields)
velox make resource Product -i

# Without -i: Creates TODOs (not recommended)
velox make resource Post

# With all features
velox make resource Order -i --soft-delete --auto-migrate

# Preview without writing
velox make resource Post --dry-run
```

### What It Creates

```
src/
├── procedures/
│   ├── posts.ts              # CRUD procedures
│   └── __tests__/
│       └── posts.test.ts     # Unit tests
├── schemas/
│   └── post.schema.ts        # Zod validation
└── models/
    └── post.prisma           # Injected into schema.prisma
```

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--interactive` | `-i` | **Define fields interactively (recommended)** |
| `--crud` | `-c` | Generate full CRUD operations |
| `--paginated` | `-P` | Include pagination for list |
| `--soft-delete` | `-s` | Add soft delete support |
| `--timestamps` | `-t` | Include timestamps (default: true) |
| `--with-tests` | `-W` | Generate tests (default: true) |
| `--skip-registration` | | Don't auto-register in router |
| `--auto-migrate` | | Run migration automatically |
| `--dry-run` | `-d` | Preview changes only |
| `--force` | `-f` | Overwrite existing files |

## Procedure Generator

For single procedures or quick prototypes.

```bash
# Simple single procedure
velox make procedure health

# CRUD with inline schemas
velox make procedure users --crud

# With pagination
velox make procedure posts --crud --paginated
```

### What It Creates

```
src/
└── procedures/
    └── users.ts              # Procedures with inline schemas
```

### When to Use

- Adding a single endpoint (health check, webhook)
- Quick prototyping
- Self-contained procedure with inline schemas

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--crud` | `-c` | Generate full CRUD operations |
| `--paginated` | `-P` | Include pagination |
| `--skip-registration` | `-S` | Don't auto-register |

## Other Generators

### Schema Generator

```bash
velox make schema User
velox make schema Post --crud    # With input schemas
```

### Model Generator

```bash
velox make model User
velox make model Post --timestamps
```

### Job Generator (Background Tasks)

```bash
velox make job SendWelcomeEmail
velox make job ProcessOrder --queue
```

### Mail Generator

```bash
velox make mail WelcomeEmail
velox make mail OrderConfirmation --react   # React Email template
```

### Guard Generator (Authentication)

```bash
velox make guard admin           # Role-based
velox make guard verified        # Custom logic
```

### Policy Generator (Authorization)

```bash
velox make policy PostPolicy
velox make policy CommentPolicy --crud
```

### Middleware Generator

```bash
velox make middleware logging
velox make middleware rate-limit
```

### Service Generator

```bash
velox make service PaymentService
velox make service EmailService --injectable
```

### Exception Generator

```bash
velox make exception PaymentFailed
velox make exception ValidationFailed --http
```

### Task Generator (Scheduled)

```bash
velox make task CleanupExpiredSessions
velox make task SendDailyDigest --cron="0 9 * * *"
```

## Common Workflows

### New Feature: Blog Posts (AI Agent)

```bash
# 1. Design Prisma model directly in schema.prisma
model Post {
  id        String   @id @default(uuid())
  title     String
  slug      String   @unique
  content   String
  excerpt   String?
  published Boolean  @default(false)
  authorId  String
  author    User     @relation(fields: [authorId], references: [id])
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  @@map("posts")
}

# 2. Generate procedures for the model
velox make namespace Post --example

# 3. Push database changes
pnpm db:push

# 4. (Optional) Seed sample data
velox make seeder PostSeeder
```

### New Feature: Blog Posts (Human Interactive)

```bash
# 1. Interactive field definition
velox make resource Post -i --auto-migrate

# 2. Follow prompts to define fields
# 3. Migration runs automatically
```

### Adding Procedures for Existing Model

```bash
# Model already exists in Prisma
velox make namespace Order --example

# Or just add schema
velox make schema Order --crud
```

### Quick Utility Endpoint

```bash
# Health check
velox make procedure health

# Then customize the generated file
```

### Background Processing

```bash
# Create job
velox make job SendWelcomeEmail

# Create mail template
velox make mail WelcomeEmail --react

# Use in procedure
createUser: procedure()
  .input(CreateUserSchema)
  .mutation(async ({ ctx, input }) => {
    const user = await ctx.db.user.create({ data: input });
    await dispatch(SendWelcomeEmail, { userId: user.id });
    return user;
  }),
```

## Generator Aliases

| Full Command | Alias |
|--------------|-------|
| `velox make resource` | `velox m r` |
| `velox make namespace` | `velox m ns` |
| `velox make procedure` | `velox m p` |
| `velox make schema` | `velox m s` |
| `velox make model` | `velox m mod` |
| `velox make job` | `velox m j` |
| `velox make mail` | `velox m em` |
| `velox make guard` | `velox m g` |
| `velox make policy` | `velox m pol` |
| `velox make middleware` | `velox m mw` |
| `velox make service` | `velox m svc` |
| `velox make exception` | `velox m ex` |
| `velox make task` | `velox m task` |