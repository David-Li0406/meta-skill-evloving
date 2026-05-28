---
name: spec:design
description: Create Design Document - generates a technical design document based on the requirements document
---

# Create Design Document

Creates a design document based on the requirements document. This command reads the requirements from `.specs/<spec-name>/requirements.md` and generates a technical design.

## When to use

Use this skill when the user needs to:
- Create a technical design document from existing requirements
- Generate architecture diagrams and component specifications
- Plan implementation details before coding

## Instructions

### Step 1: Locate Requirements

1. If `<args>` contains a spec name, look for requirements at `.specs/<spec-name>/requirements.md`
2. If no spec name provided, list available specs in `.specs/` and ask user to choose
3. Read and analyze the requirements document

### Step 2: Analyze the Codebase

Before writing the design:
1. Explore the existing architecture and patterns in the codebase
2. Identify components that will be created or modified
3. Understand existing services, interfaces, and data models
4. Note integration points with other parts of the system

### Step 3: Create the Design Document

Create the document at `.specs/<spec-name>/design.md` with this structure:

```markdown
# Design Document: [Feature Name]

## Overview

[Brief description of what will be implemented and the key changes]

### Key Changes

1. [Major change 1]
2. [Major change 2]
3. [Major change 3]

## Architecture

### Component Diagram

\`\`\`mermaid
graph TB
    subgraph "Module Name"
        A[Component A]
        B[Component B]
    end

    subgraph "External"
        C[External Service]
    end

    A --> B
    B --> C
\`\`\`

### Data Flow

\`\`\`mermaid
sequenceDiagram
    participant U as User
    participant C as Component
    participant S as Service
    participant E as External

    U->>C: Action
    C->>S: Request
    S->>E: API Call
    E-->>S: Response
    S-->>C: Result
    C-->>U: Display
\`\`\`

## Components and Interfaces

### [Component/Service Name]

[Description of the component]

\`\`\`typescript
// Path: src/path/to/file.ts

interface InterfaceName {
  property: Type;
  method(param: Type): ReturnType;
}

class ClassName {
  constructor(config: ConfigType);

  methodName(param: Type): ReturnType;
}
\`\`\`

[Continue with additional components]

## Data Models

### [Model Name]

\`\`\`typescript
interface ModelName {
  // Properties with comments
  field1: string;  // Description
  field2: number;  // Description
}
\`\`\`

## Error Handling

### Error Types and Handling

| Error | User Message |
|-------|-------------|
| Network error | "Could not connect to server." |
| Invalid input | "Please check your input." |

## Testing Strategy

### Approach

[Describe the testing approach - unit tests, integration tests, etc.]

### Unit Tests

\`\`\`typescript
describe('ComponentName', () => {
  it('should [expected behavior]', () => {
    // Test example
  });
});
\`\`\`

### Edge Cases

1. [Edge case 1] - [Expected handling]
2. [Edge case 2] - [Expected handling]
```

### Writing Guidelines

1. **Include diagrams** - Use Mermaid for architecture and flow diagrams
2. **Show TypeScript interfaces** - Define all new interfaces and types
3. **Reference file paths** - Indicate where code will be located
4. **Map to requirements** - Ensure design covers all requirements
5. **Consider error cases** - Document error handling strategy
6. **Include test examples** - Show how components will be tested

### Step 4: Confirm with User

After creating the document, show the user:
1. The location of the created file
2. A summary of the design decisions
3. Ask if they want to make any changes

## Arguments

- `<args>` - The spec name (e.g., "user-auth", "payment-flow")

If not provided, list available specs and ask the user to choose.
