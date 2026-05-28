# Code Diff Templates by Fix Type

Reference for generating code diffs based on `fix.type` from AIP review findings.

## Quick Reference

| fix.type                | Auto-generate? | Complexity |
| ----------------------- | -------------- | ---------- |
| `rename-path-segment`   | Yes            | Low        |
| `rename-parameter`      | Yes            | Low        |
| `change-status-code`    | Yes            | Low        |
| `remove-request-body`   | Yes            | Low        |
| `add-parameter`         | Partial        | Medium     |
| `add-parameters`        | Partial        | Medium     |
| `set-schema-constraint` | Spec only      | Low        |
| `add-schema-property`   | Partial        | Medium     |
| `add-schema`            | No             | High       |
| `add-response`          | Partial        | Medium     |
| `add-operation`         | No             | High       |

---

## NestJS Templates

### rename-path-segment

**Scenario**: `/user/{id}` → `/users/{id}`

```diff
// Controller decorator
-@Controller('user')
+@Controller('users')
export class UsersController {
```

**If path is in method decorator:**

```diff
-@Get('user/:id')
+@Get('users/:id')
async getUser(@Param('id') id: string) {
```

### rename-parameter

**Scenario**: `userId` → `user_id`

```diff
-@Get(':userId')
-async getUser(@Param('userId') userId: string) {
+@Get(':user_id')
+async getUser(@Param('user_id') user_id: string) {
```

### change-status-code

**Scenario**: POST should return 201, not 200

```diff
@Post()
+@HttpCode(HttpStatus.CREATED)
async create(@Body() dto: CreateUserDto) {
```

**For 202 (Accepted):**

```diff
@Post()
+@HttpCode(HttpStatus.ACCEPTED)
async createAsync(@Body() dto: CreateUserDto) {
```

### remove-request-body

**Scenario**: GET endpoint has @Body() which should be removed

```diff
@Get(':id')
-async getUser(@Param('id') id: string, @Body() filters: FilterDto) {
+async getUser(@Param('id') id: string) {
```

### add-parameter (pagination)

**Scenario**: List endpoint needs page_size and page_token

```diff
@Get()
-async findAll() {
+async findAll(
+  @Query('page_size', new DefaultValuePipe(20), ParseIntPipe) pageSize: number,
+  @Query('page_token') pageToken?: string,
+) {
-  return this.service.findAll();
+  return this.service.findAll({ pageSize, pageToken });
}
```

**Required imports:**

```typescript
import { DefaultValuePipe, ParseIntPipe, Query } from '@nestjs/common';
```

### add-parameter (filter)

**Scenario**: List endpoint needs filter parameter

```diff
@Get()
async findAll(
  @Query('page_size') pageSize: number,
+  @Query('filter') filter?: string,
) {
-  return this.service.findAll({ pageSize });
+  return this.service.findAll({ pageSize, filter });
}
```

### add-parameter (idempotency-key)

**Scenario**: POST endpoint needs Idempotency-Key header

```diff
@Post()
async create(
  @Body() dto: CreateOrderDto,
+  @Headers('idempotency-key') idempotencyKey?: string,
) {
```

**Required imports:**

```typescript
import { Headers } from '@nestjs/common';
```

---

## Fastify Templates

### rename-path-segment

```diff
-fastify.get('/user/:id', async (request, reply) => {
+fastify.get('/users/:id', async (request, reply) => {
```

### change-status-code

```diff
fastify.post('/users', async (request, reply) => {
  const user = await createUser(request.body);
-  return user;
+  reply.code(201).send(user);
});
```

### add-parameter (pagination)

```diff
fastify.get('/users', {
  schema: {
    querystring: {
+      page_size: { type: 'integer', default: 20, maximum: 100 },
+      page_token: { type: 'string' },
    }
  }
}, async (request, reply) => {
-  const users = await getUsers();
+  const { page_size, page_token } = request.query;
+  const users = await getUsers({ pageSize: page_size, pageToken: page_token });
  return users;
});
```

---

## Express Templates

### rename-path-segment

```diff
-router.get('/user/:id', async (req, res) => {
+router.get('/users/:id', async (req, res) => {
```

### change-status-code

```diff
router.post('/users', async (req, res) => {
  const user = await createUser(req.body);
-  res.json(user);
+  res.status(201).json(user);
});
```

### add-parameter (pagination)

```diff
router.get('/users', async (req, res) => {
-  const users = await getUsers();
+  const pageSize = parseInt(req.query.page_size) || 20;
+  const pageToken = req.query.page_token;
+  const users = await getUsers({ pageSize, pageToken });
  res.json(users);
});
```

---

## When NOT to Generate Diffs

### add-schema

Too complex - requires:

- Creating new DTO/interface file
- Adding validation decorators
- Potentially creating nested types
- Understanding business logic

**Instead, provide template:**

```typescript
// src/common/dto/error.dto.ts (suggested location)
export class ErrorDto {
  // TODO: Implement based on AIP-193
  code: string;
  message: string;
  details?: unknown[];
  request_id?: string;
}
```

### add-operation

Too complex - requires:

- New controller method
- Service implementation
- DTOs for request/response
- Tests

**Instead, provide guidance:**

```markdown
New endpoint needed: GET /users/{id}/orders

- Add method to UsersController
- Add getOrdersByUserId to OrdersService
- Create response DTO
```

### Complex refactoring

If the fix requires understanding business logic or making architectural decisions, don't generate a diff. Instead, describe what needs to change and let the developer decide.

---

## Diff Quality Guidelines

1. **Be conservative** - Only generate diffs you're confident about
2. **Include imports** - Show required import changes
3. **Preserve formatting** - Match existing code style
4. **Show context** - Include surrounding lines for clarity
5. **Note side effects** - If change affects other files, mention it

## Example Usage in Correlation

```json
{
  "codeLocations": [
    {
      "file": "src/users/users.controller.ts",
      "line": 8,
      "type": "controller"
    }
  ],
  "finding": {
    "fix": {
      "specChanges": [
        { "from": "/user/{id}", "operation": "rename-key", "to": "/users/{id}" }
      ],
      "type": "rename-path-segment"
    },
    "ruleId": "naming/plural-resources"
  },
  "suggestedDiffs": {
    "codeDiffs": [
      {
        "description": "Rename controller path to plural form",
        "diff": "-@Controller('user')\n+@Controller('users')",
        "file": "src/users/users.controller.ts"
      }
    ],
    "specDiff": "..."
  }
}
```
