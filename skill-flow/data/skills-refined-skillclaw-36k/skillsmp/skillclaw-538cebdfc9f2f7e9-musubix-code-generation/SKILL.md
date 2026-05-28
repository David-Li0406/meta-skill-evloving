---
name: musubix-code-generation
description: Use this skill when asked to generate code, implement features, or create components following design documents using the MUSUBIX methodology.
---

# MUSUBIX Code Generation Skill

This skill guides you through generating code from design specifications following the MUSUBIX methodology.

## Prerequisites

Before generating code:

1. Verify the design document exists (`DES-*`)
2. Verify requirements are traceable (`REQ-*`)
3. Check `steering/tech.ja.md` for the technology stack

## Supported Languages

| Language     | Extension | Features                          |
|--------------|-----------|-----------------------------------|
| TypeScript   | `.ts`     | Full support with types           |
| JavaScript   | `.js`     | ES6+ modules                      |
| Python       | `.py`     | Type hints support                |
| Java         | `.java`   | Interface/Class generation        |
| Go           | `.go`     | Struct/Interface generation       |
| Rust         | `.rs`     | Trait/Struct generation           |
| C#           | `.cs`     | Interface/Class generation        |

## Code Generation Workflow

### Step 1: Read Design Document

```bash
# Generate code from design
npx musubix codegen generate <design-file>
```

### Step 2: Generate with Traceability

Always include requirement references:

```typescript
/**
 * UserService - Handles user operations
 * 
 * @see REQ-INT-001 - Neuro-Symbolic Integration
 * @see DES-INT-001 - Integration Layer Design
 */
export class UserService {
  // Implementation
}
```

### Step 3: Follow Test-First (Article III)

1. **Write test first**:
```typescript
describe('UserService', () => {
  it('should create user', async () => {
    const service = new UserService();
    const user = await service.create({ name: 'Test' });
    expect(user.id).toBeDefined();
  });
});
```

2. **Implement minimal code**:
```typescript
export class UserService {
  async create(data: CreateUserDto): Promise<User> {
    return { id: generateId(), ...data };
  }
}
```

3. **Refactor**

## Design Pattern Templates

### Singleton Pattern
```typescript
/**
 * @see REQ-DES-001 - Pattern Detection
 * @pattern Singleton
 */
export class ConfigManager {
  private static instance: ConfigManager;
  
  private constructor() {}
  
  static getInstance(): ConfigManager {
    if (!ConfigManager.instance) {
      ConfigManager.instance = new ConfigManager();
    }
    return ConfigManager.instance;
  }
}
```

### Factory Pattern
```typescript
/**
 * @see REQ-DES-001 - Pattern Detection
 * @pattern Factory
 */
export interface ServiceFactory {
  create(type: string): Service;
}
```