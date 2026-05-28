---
name: fable-dsl-extension
description: Comprehensive skill for extending the FableDSL language with new commands, directives, and features. Use when adding new DSL syntax, creating custom animation commands, implementing new visual agents (buttons, images, text), adding control flow (if statements, loops), or extending the parser with new language constructs. This skill handles the complete workflow from grammar updates to runtime implementation and editor integration.
---

# FableDSL Extension Skill

This skill provides comprehensive guidance for extending the FableDSL language with new commands, directives, and features.

## When to Use This Skill

Activate this skill when:
- Adding new DSL commands or directives
- Creating custom animation commands
- Implementing new visual agents (buttons, images, text)
- Adding control flow constructs (if statements, loops)
- Extending parser grammar with new syntax
- Updating editor support (syntax highlighting, validation)
- Creating new runtime components or engines

## DSL Extension Workflow

Follow this systematic approach when extending FableDSL:

### 1. Grammar Structure Analysis

First, understand the current grammar structure:

**File**: `packages/parser/src/grammar/fable.ohm-bundle.d.ts`
- Contains the language syntax and parsing rules
- Defines how DSL commands are structured
- Shows existing command patterns and syntax

**Action**: Read the grammar file to understand current syntax patterns before adding new constructs.

### 2. Type Definition Updates

Add new types for your feature:

**File**: `packages/parser/src/types.d.ts`

```typescript
// Example: Adding a new animation command
interface BounceAnimation extends Animation {
  type: 'bounce';
  duration?: number;
  intensity?: 'gentle' | 'medium' | 'intense';
  repeat?: number;
}
```

**Action**: Define proper TypeScript interfaces for new language constructs.

### 3. Parser Semantics Implementation

Update parser semantics to convert AST nodes:

**File**: `packages/parser/src/grammar/fable.ohm-bundle.d.ts`

**Action**: Add semantic actions that transform parsed syntax into proper AST nodes.

### 4. Runtime Logic Implementation

Implement the actual runtime behavior:

**File**: `packages/runtime/src/`

**Components to create/modify**:
- New animation components (`FableBounce.tsx`)
- Engine updates for new commands
- Control flow handlers
- Visual agent renderers

**Action**: Build the runtime logic that executes your DSL commands.

### 5. Editor Integration Updates

Add editor support for the new syntax:

**File**: `packages/editor/src/`

**Features to implement**:
- Syntax highlighting rules
- Autocompletion suggestions
- Real-time validation
- Error reporting

**Action**: Update Monaco editor integration to recognize new syntax.

### 6. Comprehensive Testing

Create test suites for the new functionality:

**Files**: `packages/*/tests/`

**Test types**:
- Unit tests for parser logic
- Integration tests for runtime execution
- Editor tests for syntax support
- End-to-end tests for complete workflows

**Action**: Ensure all functionality works correctly across the entire system.

### 7. Documentation and Examples

Update project documentation:

**Files to update**:
- `apps/web/src/constants/default-dsl.ts` - Add usage examples
- `AGENTS.md` - Document new features
- Code comments and JSDoc

**Action**: Document the new feature for future developers.

## Quick Command Creation

For simple command additions, use this streamlined process:

```bash
# Use the fable-dsl-extension skill
use skill fable-dsl-extension

# Create a new command with properties
create dsl command "bounce" for "animations" with properties:
- duration: number (default: 500ms)
- intensity: "gentle" | "medium" | "intense" (default: "medium")
- repeat: number (default: 1)
```

This will automatically generate:
- TypeScript type definitions
- Parser grammar updates
- Runtime animation component
- Editor syntax highlighting
- Test templates
- Documentation updates

## Common Extension Patterns

### Animation Commands
```dsl
bounce duration 1000ms intensity intense repeat 3
fade_in duration 500ms
slide_left distance 100px
```

### Visual Agents
```dsl
button #my-btn "Click Me" at [100, 200] size [150, 50]
image #logo "logo.png" at [50, 50] scale 0.8
text #title "Hello World" at [200, 100] size 24
```

### Control Flow
```dsl
if user_score > 80 then
  show_success
else
  show_retry
end

for each item in items do
  display_item item
end
```

## Best Practices

### Grammar Design
- Follow existing naming conventions
- Use descriptive, readable syntax
- Maintain backward compatibility
- Document all new syntax elements

### Type Safety
- Define comprehensive TypeScript interfaces
- Use discriminated unions for variant types
- Include proper JSDoc comments
- Validate inputs at runtime

### Performance
- Optimize runtime execution
- Minimize bundle size impact
- Cache expensive operations
- Profile animation performance

### Testing
- Test edge cases and error conditions
- Validate cross-browser compatibility
- Test editor integration thoroughly
- Include performance benchmarks

## Troubleshooting

### Common Issues
- **Parser errors**: Check grammar syntax and semantic actions
- **Runtime failures**: Verify type definitions and component props
- **Editor issues**: Update syntax highlighting rules
- **Performance problems**: Profile and optimize animation loops

### Debug Steps
1. Validate DSL syntax with parser tests
2. Check runtime component rendering
3. Test editor autocompletion
4. Verify end-to-end functionality
5. Profile performance metrics

## Resources

- [DSL Grammar Reference](references/grammar.md)
- [Runtime API Docs](references/runtime-api.md)
- [Editor Integration Guide](references/editor-integration.md)
- [Testing Patterns](references/testing.md)