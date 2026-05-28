---
name: documentation-writing
description: Best practices for creating clear, comprehensive, and maintainable documentation for code, APIs, and systems
---

# Documentation Writing

This skill covers best practices for creating effective documentation that developers actually want to read and maintain.

## Core Philosophy

Great documentation is:
- **Clear**: Easy to understand on first reading
- **Complete**: Answers the questions users actually have
- **Current**: Kept in sync with code changes
- **Concise**: No unnecessary fluff
- **Scannable**: Easy to find what you need
- **Practical**: Focuses on how-to, not just what

## Types of Documentation

### 1. README Files

The front door to your project:

```markdown
# Project Name

Brief description (1-2 sentences) of what this does.

## Features

- Key feature 1
- Key feature 2
- Key feature 3

## Quick Start

\`\`\`bash
npm install
npm run dev
\`\`\`

Visit http://localhost:3000

## Project Structure

\`\`\`
src/
  routes/        # Remix routes
  lib/           # Shared utilities
  components/    # React components
\`\`\`

## Documentation

- [Setup Guide](docs/setup.md)
- [Architecture](docs/architecture.md)
- [API Reference](docs/api.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT
```

**Key elements:**
- What it does (immediately)
- How to get started (quickly)
- Where to find more information
- How to contribute

### 2. Code Comments

Use sparingly and wisely:

✅ **Do explain WHY:**
```typescript
// We batch writes to avoid hitting DynamoDB's 25-item transaction limit
const batches = chunk(items, 25);

// Disable cache for this endpoint because user data changes frequently
// and stale data causes support tickets. See issue #123
export const loader = async () => {
  // ...
};
```

✅ **Do document complex algorithms:**
```typescript
/**
 * Implements the Luhn algorithm for credit card validation.
 * https://en.wikipedia.org/wiki/Luhn_algorithm
 */
function validateCardNumber(cardNumber: string): boolean {
  // Double every second digit from right to left
  // If doubling results in two digits, add them together
  // ...
}
```

❌ **Don't state the obvious:**
```typescript
// Get the user
const user = await getUser(id);

// Check if user exists
if (!user) {
  // Return error
  return error("Not found");
}
```

### 3. API Documentation

Document public APIs thoroughly:

```typescript
/**
 * Creates a new user account and sends a welcome email.
 *
 * @param email - User's email address (must be unique)
 * @param password - Plain text password (will be hashed)
 * @param name - User's display name
 * @returns The created user object (without password)
 * @throws {ValidationError} If email is invalid or already exists
 * @throws {EmailError} If welcome email fails to send
 *
 * @example
 * ```typescript
 * const user = await createUser({
 *   email: "user@example.com",
 *   password: "secure123",
 *   name: "John Doe"
 * });
 * ```
 */
export async function createUser(
  email: string,
  password: string,
  name: string
): Promise<User> {
  // Implementation
}
```

### 4. Architecture Documentation

Explain the big picture:

```markdown
# Architecture Overview

## System Components

### Frontend (Remix)
- Server-side rendering for initial load
- Progressive enhancement for interactivity
- Nested routes for UI composition

### Backend (SST)
- Lambda functions for API endpoints
- DynamoDB for data storage (single table design)
- S3 for file uploads
- SES for email sending

### Data Flow

1. User submits form → Remix action
2. Action validates data
3. Action calls business logic in `src/lib/`
4. Business logic updates DynamoDB
5. Action redirects or returns errors
6. Loader refetches data
7. Component renders updated state

## Key Design Decisions

### Why Single Table DynamoDB?
We use single table design because:
- Lower costs (one table vs many)
- Better performance (no joins needed)
- Atomic transactions across entities
- Aligns with serverless architecture

See: docs/dynamodb-design.md

### Why SST over CDK?
- Type-safe resource bindings
- Better developer experience
- Simpler infrastructure code
- Great local development story
```

### 5. Setup Documentation

Make it easy for new developers:

```markdown
# Setup Guide

## Prerequisites

- Node.js 20+
- AWS account with CLI configured
- GitHub account (for deployment)

## Installation

1. Clone the repository:
   \`\`\`bash
   git clone https://github.com/your-org/project
   cd project
   \`\`\`

2. Install dependencies:
   \`\`\`bash
   npm install
   \`\`\`

3. Set up environment:
   \`\`\`bash
   cp .env.example .env
   # Edit .env and add your values
   \`\`\`

4. Start SST:
   \`\`\`bash
   npm run sst:dev
   \`\`\`

5. In another terminal, start Remix:
   \`\`\`bash
   npm run dev
   \`\`\`

6. Visit http://localhost:3000

## Troubleshooting

### "Cannot find module 'sst'"
Run `npm install` again. SST might not have installed correctly.

### Port 3000 already in use
Kill the process using port 3000 or change the port in package.json.
```

### 6. ADR (Architecture Decision Records)

Document important decisions:

```markdown
# ADR 001: Use Single Table Design for DynamoDB

## Status
Accepted

## Context
We need to store users, posts, comments, and relationships between them.
Traditional approach would be separate tables, but we're building a serverless app.

## Decision
We will use single table design with generic pk/sk keys.

## Consequences

### Positive
- Lower costs (one table vs many)
- Better query performance (no joins)
- Atomic transactions across entity types
- Simpler infrastructure

### Negative
- Higher initial learning curve
- Requires understanding access patterns upfront
- More complex to query during development

## Alternatives Considered
- Multiple tables (rejected: higher costs, no cross-table transactions)
- Relational DB (rejected: doesn't fit serverless model well)
```

## Documentation Patterns

### Pattern 1: Tutorial-Style Guides

Walk through a complete example:

```markdown
# Building Your First Feature

Let's build a simple blog post feature together.

## Step 1: Create the Database Schema

First, we'll define how posts are stored in DynamoDB.

A post has:
- ID (unique identifier)
- Author (user who created it)
- Title
- Content
- Created date

In single table design, we'll store this as:

\`\`\`typescript
{
  pk: "POST#<postId>",
  sk: "METADATA",
  authorId: "<userId>",
  title: "My First Post",
  content: "Hello, world!",
  createdAt: "2025-01-02T10:00:00Z"
}
\`\`\`

## Step 2: Create the Route

Create a new file: `app/routes/posts.new.tsx`

\`\`\`typescript
// ... code here
\`\`\`

## Step 3: Add the Form
// ... continue the tutorial
```

### Pattern 2: Reference Documentation

Quick lookup for APIs:

```markdown
# Database API Reference

## `createPost()`

Creates a new blog post.

**Signature:**
\`\`\`typescript
createPost(authorId: string, data: PostData): Promise<Post>
\`\`\`

**Parameters:**
- `authorId` - ID of the user creating the post
- `data.title` - Post title (required, max 200 chars)
- `data.content` - Post content (required, max 50000 chars)

**Returns:**
- Promise resolving to created Post object

**Throws:**
- `ValidationError` - If data is invalid
- `DatabaseError` - If write fails

**Example:**
\`\`\`typescript
const post = await createPost("user123", {
  title: "Hello World",
  content: "My first post!"
});
\`\`\`
```

### Pattern 3: Troubleshooting Guides

Help users solve common problems:

```markdown
# Troubleshooting Guide

## Common Issues

### SST Deploy Fails with "Resource already exists"

**Symptoms:**
\`\`\`
Error: Resource MyFunction already exists
\`\`\`

**Cause:**
A previous deployment failed partway through.

**Solution:**
1. Delete the CloudFormation stack manually:
   \`\`\`bash
   aws cloudformation delete-stack --stack-name my-app-dev
   \`\`\`
2. Wait for deletion to complete
3. Deploy again: `npm run deploy`

### DynamoDB Query Returns No Results

**Symptoms:**
Query runs without errors but returns empty array.

**Common Causes:**
1. **Wrong key format** - Check your pk/sk format matches
2. **Using scan instead of query** - Use Query for single partition
3. **GSI not ready** - Wait a few seconds after creating items

**Debug Steps:**
1. Log the query parameters
2. Check item in DynamoDB console
3. Verify key format matches exactly
```

## Best Practices

### 1. Keep Docs Close to Code

```
src/
  lib/
    email/
      send.ts
      README.md       # Email system docs
      examples.md     # Usage examples
```

### 2. Use Markdown Formatting

```markdown
# Headers for sections
## Subheaders for subsections

**Bold** for emphasis
*Italic* for terms

`code` for inline code
\`\`\`typescript
// code blocks
\`\`\`

> Blockquotes for notes

- Bullet lists
- For multiple items

1. Numbered lists
2. For sequential steps
```

### 3. Include Code Examples

Always show working code:

```markdown
## Creating a User

\`\`\`typescript
import { createUser } from "./lib/users";

const user = await createUser({
  email: "user@example.com",
  password: "secure123",
  name: "John Doe"
});

console.log(`Created user: ${user.id}`);
\`\`\`
```

### 4. Link Related Documentation

```markdown
See also:
- [Authentication Guide](./auth.md)
- [Database Schema](./database.md)
- [API Reference](./api.md)
```

### 5. Keep It Current

```markdown
<!-- Add a "Last Updated" note -->
> Last Updated: 2025-01-02
> Version: 2.0.0
```

## Documentation Tools

### JSDoc for TypeScript

```typescript
/**
 * Represents a blog post.
 */
export interface Post {
  /** Unique identifier */
  id: string;
  
  /** Post title (max 200 characters) */
  title: string;
  
  /** Post content in Markdown format */
  content: string;
  
  /** ISO 8601 timestamp of creation */
  createdAt: string;
  
  /** ID of the author */
  authorId: string;
}
```

### README Badges

```markdown
![Build Status](https://github.com/org/repo/workflows/test/badge.svg)
![Coverage](https://codecov.io/gh/org/repo/branch/main/graph/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
```

### Diagrams with Mermaid

```markdown
\`\`\`mermaid
graph TD
    A[User submits form] --> B[Remix action]
    B --> C{Valid data?}
    C -->|Yes| D[Save to DB]
    C -->|No| E[Return errors]
    D --> F[Redirect to success]
    E --> G[Show form with errors]
\`\`\`
```

## Documentation Checklist

When documenting a new feature:

- [ ] Update README if user-facing
- [ ] Add JSDoc comments to public APIs
- [ ] Create usage examples
- [ ] Document configuration options
- [ ] Explain error messages
- [ ] Add troubleshooting tips
- [ ] Link to related docs
- [ ] Update architecture diagrams
- [ ] Review for clarity
- [ ] Test all code examples

## Common Mistakes to Avoid

❌ **Don't:**
- Write docs that are out of date
- Use jargon without explanation
- Skip error handling in examples
- Document internal implementation details
- Write novels (keep it concise)
- Assume prior knowledge

✅ **Do:**
- Update docs with code changes
- Define terms on first use
- Show how to handle errors
- Document public APIs and behavior
- Be clear and direct
- Provide context and examples

## Documentation as Code

Treat docs like code:

```typescript
// docs/examples/create-user.test.ts
// This file is both docs and tests!

import { createUser } from "../src/lib/users";

test("creating a user", async () => {
  // This example appears in docs
  const user = await createUser({
    email: "user@example.com",
    password: "secure123",
    name: "John Doe"
  });
  
  expect(user.email).toBe("user@example.com");
  expect(user.name).toBe("John Doe");
});
```

## Further Reading

- Write The Docs: https://www.writethedocs.org/
- MDN Writing Guidelines: https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines
- Google Developer Documentation Style Guide: https://developers.google.com/style
