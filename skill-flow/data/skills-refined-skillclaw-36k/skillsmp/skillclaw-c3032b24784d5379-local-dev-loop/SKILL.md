---
name: local-dev-loop
description: Use this skill when setting up a local development environment with hot reload and testing for either Replit or Instantly.
---

# Local Dev Loop

## Overview
Set up a fast, reproducible local development workflow for Replit or Instantly.

## Prerequisites
- Completed installation and authentication setup for Replit or Instantly
- Node.js 18+ with npm/pnpm
- Code editor with TypeScript support
- Git for version control

## Instructions

### Step 1: Create Project Structure
```
my-project/
├── src/
│   ├── client/
│   │   ├── client.ts       # Client wrapper
│   │   ├── config.ts       # Configuration management
│   │   └── utils.ts        # Helper functions
│   └── index.ts
├── tests/
│   └── client.test.ts
├── .env.local              # Local secrets (git-ignored)
├── .env.example            # Template for team
└── package.json
```

### Step 2: Configure Environment
```bash
# Copy environment template
cp .env.example .env.local

# Install dependencies
npm install

# Start development server
npm run dev
```

### Step 3: Setup Hot Reload
```json
{
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "test": "vitest",
    "test:watch": "vitest --watch"
  }
}
```

### Step 4: Configure Testing
```typescript
import { describe, it, expect, vi } from 'vitest';
import { Client } from '../src/client/client';

describe('Client', () => {
  it('should initialize with API key', () => {
    const client = new Client({ apiKey: 'test-key' });
    expect(client).toBeDefined();
  });
});
```

## Output
- Working development environment with hot reload
- Configured test suite with mocking
- Environment variable management
- Fast iteration cycle for development

## Error Handling
| Error | Cause | Solution |
|-------|-------|----------|
| Module not found | Missing dependency | Run `npm install` |
| Port in use | Another process | Kill process or change port |
| Env not loaded | Missing .env.local | Copy from .env.example |
| Test timeout | Slow network | Increase test timeout |

## Examples

### Mock Responses
```typescript
vi.mock('@sdk', () => ({
  Client: vi.fn()
}));
```