---
name: create-spec
description: 'Create a new ContractSpec specification (command, query, or event)'
targets: ["*"]
claudecode:
  allowed-tools:
    - "Bash"
    - "Read"
    - "Write"
    - "Glob"
    - "Grep"
---

# Create Spec Skill

This skill creates ContractSpec specifications following the spec-first approach.

## Usage

Invoke when user wants to create a new API operation, event, or contract.

## Process

### Step 1: Determine Spec Type

- **Command**: Mutates state (create, update, delete)
- **Query**: Reads state without mutation
- **Event**: Represents something that happened

### Step 2: Gather Requirements

For Commands/Queries:
- Operation name (e.g., `createUser`, `getUserById`)
- Input schema (fields, types, validation)
- Output schema (response structure)
- Error cases
- Business rules

For Events:
- Event name (past tense, e.g., `UserCreated`)
- Payload schema
- When it's emitted

### Step 3: Create the Spec

Location: `packages/libs/contracts/src/specs/<domain>/`

```typescript
// packages/libs/contracts/src/specs/users/createUser.ts

import { z } from 'zod';
import { defineCommand } from '../../core/defineCommand';

/**
 * Creates a new user in the system.
 *
 * @domain users
 * @visibility public
 */
export const createUserCommand = defineCommand({
  name: 'createUser',
  description: 'Creates a new user account',
  input: z.object({
    email: z.string().email('Invalid email format'),
    name: z.string().min(1, 'Name is required'),
    role: z.enum(['admin', 'user', 'viewer']).default('user'),
  }),
  output: z.object({
    id: z.string().uuid(),
    email: z.string(),
    name: z.string(),
    role: z.enum(['admin', 'user', 'viewer']),
    createdAt: z.date(),
  }),
  errors: {
    EMAIL_EXISTS: 'A user with this email already exists',
    INVALID_ROLE: 'The specified role is not valid',
  },
});

// Export type helpers
export type CreateUserInput = z.infer<typeof createUserCommand.input>;
export type CreateUserOutput = z.infer<typeof createUserCommand.output>;
```

### Step 4: Register the Spec

Add to the domain's index:

```typescript
// packages/libs/contracts/src/specs/users/index.ts
export * from './createUser';
export * from './getUserById';
// ...
```

### Step 5: Create DocBlock

```typescript
// packages/libs/contracts/src/specs/users/createUser.docblock.ts

import { registerDocBlock } from '@contractspec/lib.docs';

export const createUserDoc = registerDocBlock({
  id: 'spec-create-user',
  title: 'Create User Command',
  body: `
## Overview

Creates a new user account in the system.

## Input

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | User's email address |
| name | string | Yes | User's display name |
| role | enum | No | User's role (default: user) |

## Output

Returns the created user object with generated ID and timestamp.

## Errors

- \`EMAIL_EXISTS\`: When email is already registered
- \`INVALID_ROLE\`: When role value is not recognized

## Example

\`\`\`typescript
const user = await execute(createUserCommand, {
  email: 'user@example.com',
  name: 'John Doe',
});
\`\`\`
  `,
  kind: 'reference',
  route: '/docs/specs/users/create-user',
  visibility: 'public',
});
```

### Step 6: Verification

- Run TypeScript check
- Verify schema validates correctly
- Check spec is exported

## Templates

### Command Template
```typescript
export const <name>Command = defineCommand({
  name: '<name>',
  description: '<description>',
  input: z.object({
    // Define input fields
  }),
  output: z.object({
    // Define output fields
  }),
  errors: {
    // Define error codes
  },
});
```

### Query Template
```typescript
export const <name>Query = defineQuery({
  name: '<name>',
  description: '<description>',
  input: z.object({
    // Define input fields
  }),
  output: z.object({
    // Define output fields
  }),
});
```

### Event Template
```typescript
export const <name>Event = defineEvent({
  name: '<name>',
  description: '<description>',
  payload: z.object({
    // Define event payload
  }),
});
```

## Output

After completion, report:
- Spec file created
- Types exported
- DocBlock created
- Next steps (implement handler, add tests)