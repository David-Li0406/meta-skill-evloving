---
name: create-feature
description: 'Scaffold a new feature with all required files and structure'
targets: ["*"]
claudecode:
  allowed-tools:
    - "Bash"
    - "Read"
    - "Write"
    - "Glob"
    - "Grep"
---

# Create Feature Skill

This skill scaffolds a complete feature following ContractSpec architecture.

## Usage

Invoke when user wants to create a new feature, module, or capability.

## Process

### Step 1: Gather Requirements

Ask for:
- Feature name (kebab-case)
- Feature domain (studio, lifecycle, integrations, evolution, etc.)
- Feature type (UI component, service, full-stack)
- Brief description

### Step 2: Determine Package Location

Based on architecture rules:
- **Pure domain logic**: `packages/libs/`
- **Business feature**: `packages/bundles/contractspec-studio/src/modules/<domain>/`
- **UI components**: `packages/bundles/contractspec-studio/src/presentation/<domain>/`
- **Platform-specific**: `packages/apps/<app>/`

### Step 3: Create File Structure

For a full-stack feature in bundles:

```
modules/<feature>/
├── index.ts              # Public exports
├── types.ts              # Type definitions
├── <feature>.service.ts  # Business logic
├── <feature>.test.ts     # Tests
└── README.md             # Feature documentation
```

For a UI feature:

```
presentation/<domain>/<feature>/
├── index.ts              # Public exports
├── types.ts              # Type definitions
├── <Feature>.tsx         # UI component
├── use<Feature>.ts       # Logic hook
└── <Feature>.test.tsx    # Tests
```

### Step 4: Generate Files

Create each file with:
- Proper TypeScript types
- JSDoc comments
- Basic implementation skeleton
- Test file with basic structure
- Exports in index.ts

### Step 5: Update Imports

- Add exports to parent module index.ts
- Verify no circular dependencies

### Step 6: Verification

- Run TypeScript check
- Run lint
- Verify structure matches architecture rules

## Templates

### Service Template

```typescript
/**
 * <Feature description>
 *
 * @module <feature>
 */

import type { <FeatureInput>, <FeatureOutput> } from './types';

/**
 * <Description of what this service does>
 */
export class <Feature>Service {
  /**
   * <Method description>
   */
  async execute(input: <FeatureInput>): Promise<<FeatureOutput>> {
    // TODO: Implement
    throw new Error('Not implemented');
  }
}
```

### Component Template

```tsx
/**
 * <Component description>
 */

import { use<Feature> } from './use<Feature>';
import type { <Feature>Props } from './types';

export const <Feature> = (props: <Feature>Props) => {
  const { /* state, handlers */ } = use<Feature>(props);

  return (
    // TODO: Implement using design system components
    null
  );
};
```

### Test Template

```typescript
import { describe, it, expect } from 'vitest';
import { <Feature>Service } from './<feature>.service';

describe('<Feature>Service', () => {
  describe('execute', () => {
    it('should <expected behavior>', async () => {
      // Arrange
      const service = new <Feature>Service();
      const input = {};

      // Act
      const result = await service.execute(input);

      // Assert
      expect(result).toBeDefined();
    });
  });
});
```

## Output

After completion, report:
- Files created
- Next steps for implementation
- Related docs to update