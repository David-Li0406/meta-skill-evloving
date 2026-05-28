---
name: React Code Optimizer
description: Comprehensive code quality analysis and optimization for React/TypeScript projects. Identifies performance bottlenecks, suggests architectural improvements, and generates detailed optimization plans.
---

# React Code Optimizer Skill

This skill performs a comprehensive code quality analysis for React/TypeScript projects and generates a detailed optimization plan.

## Overview

The React Code Optimizer analyzes your React project to identify:
- Performance bottlenecks (missing React.memo, large components, inefficient re-renders)
- Code organization issues (large files, code duplication, unclear responsibilities)
- Architecture problems (state management, data flow, error handling)
- Type safety issues
- Best practices violations

It then generates a prioritized optimization plan with specific implementation steps.

## Usage

Invoke this skill when you want to optimize a React project:

```
Use the react-code-optimizer skill to analyze my project
```

Or for a specific directory:

```
Analyze the code in src/components using react-code-optimizer
```

## What This Skill Does

### 1. Project Structure Analysis
- Examines package.json for dependencies and versions
- Maps out component hierarchy
- Identifies large files (>500 lines) that may need refactoring

### 2. Performance Analysis
- **React.memo Usage**: Checks if components use React.memo to prevent unnecessary re-renders
- **Hook Optimization**: Verifies proper use of useMemo, useCallback
- **Context Performance**: Analyzes Context providers for performance issues
- **Component Size**: Flags components over 300 lines for potential splitting
- **Lazy Loading**: Checks for code splitting and lazy loading

### 3. Code Quality Analysis
- **Code Duplication**: Identifies repeated patterns that could be extracted
- **Component Responsibilities**: Checks if components do too much
- **Type Safety**: Reviews TypeScript usage and identifies any type issues
- **Error Handling**: Verifies error boundaries and error handling patterns

### 4. Architecture Review
- **State Management**: Analyzes state management patterns (Context, Redux, etc.)
- **Data Flow**: Reviews how data flows through the application
- **Side Effects**: Checks useEffect usage and cleanup
- **API Integration**: Reviews data fetching patterns

### 5. Generate Optimization Plan
Creates a detailed, phased implementation plan including:
- Specific files to modify
- Code examples for improvements
- Priority ranking (High/Medium/Low)
- Verification steps

## Output Artifacts

The skill generates these artifacts in `.gemini/antigravity/brain/<conversation-id>/`:

1. **task.md** - Checklist of optimization tasks
2. **implementation_plan.md** - Detailed optimization plan with:
   - Problem descriptions
   - Specific solutions
   - File-by-file changes
   - Verification plan
   - Expected benefits

## Analysis Steps

### Step 1: Initial Scan
```typescript
// Scans for these patterns:
- List all .tsx/.ts files
- Identify files >500 lines
- Check package.json dependencies
```

### Step 2: Component Analysis
```typescript
// For each component:
- Check for React.memo usage
- Count lines of code
- Identify useEffect/useCallback/useMemo usage
- Check prop types/interfaces
```

### Step 3: Context Analysis
```typescript
// For Context files:
- Check useMemo dependencies in context value
- Identify unnecessary re-renders
- Verify proper Provider structure
```

### Step 4: Pattern Detection
```typescript
// Identifies:
- Repeated code blocks
- Large switch statements
- Complex nested components
- Hardcoded values
```

### Step 5: Report Generation
Generates a comprehensive report with:
- Executive summary
- Detailed findings by category
- Prioritized recommendations
- Implementation roadmap

## Configuration Options

You can customize the analysis by specifying:

```markdown
Analyze my React project with these focus areas:
- Performance optimization only
- Focus on components in src/pages
- Prioritize memory leaks
```

## Best Practices Checked

### Performance
- ✅ React.memo for expensive components
- ✅ useCallback for event handlers
- ✅ useMemo for computed values
- ✅ Code splitting with React.lazy
- ✅ Virtualization for long lists

### Code Organization
- ✅ Single Responsibility Principle
- ✅ Component size <300 lines
- ✅ Extract custom hooks
- ✅ Proper file structure

### Architecture
- ✅ Proper state management
- ✅ Error boundaries
- ✅ Consistent data fetching
- ✅ Type safety

### React Patterns
- ✅ Proper useEffect cleanup
- ✅ Correct dependency arrays
- ✅ Avoid inline object/array creation
- ✅ Proper key usage in lists

## Example Output

Given a React project, the skill generates:

**Problems Found:**
- ❌ `ComponentPanel.tsx` (847 lines) - too large
- ❌ Missing React.memo on `CanvasItem` component
- ❌ Context re-renders too frequently (52 dependencies)
- ❌ No error boundaries in key areas

**Optimization Plan:**
1. **Phase 1 (High Priority)**
   - Add React.memo to 5 main components
   - Split ComponentPanel into 3 files
   - Optimize Context with separate providers

2. **Phase 2 (Medium Priority)**
   - Extract 3 custom hooks
   - Add error boundaries
   - Optimize re-renders

3. **Phase 3 (Low Priority)**
   - Improve type safety
   - Add code documentation
   - Enhance error messages

## Tips for Best Results

1. **Run on stable code** - Best used on code that's working but needs optimization
2. **Focus areas** - Specify if you want to focus on specific directories
3. **Follow phases** - Implement optimizations in the suggested order
4. **Verify between phases** - Test after each optimization phase

## Common Optimization Patterns

### Pattern 1: Memoize Components
```typescript
// Before
export default function MyComponent({ data }) { ... }

// After
export default React.memo(MyComponent, (prev, next) => {
  return prev.data.id === next.data.id;
});
```

### Pattern 2: Split Large Components
```typescript
// Before: 800 line component

// After: Split into:
- MyComponent.tsx (150 lines)
- renderers/DataRenderer.tsx (200 lines)
- renderers/UIRenderer.tsx (200 lines)
- hooks/useMyData.ts (100 lines)
```

### Pattern 3: Optimize Context
```typescript
// Before: Single context with many values
const value = { state, dispatch, helper1, helper2, ... }

// After: Split concerns
<StateContext.Provider value={state}>
  <ActionsContext.Provider value={actions}>
    <HelpersContext.Provider value={helpers}>
```

## Limitations

This skill:
- Does NOT automatically apply changes (generates plans only)
- Focuses on React/TypeScript projects
- May need manual review for complex architectures
- Best suited for projects with 50-5000 components

## Related Skills

- **Component Generator** - Create new optimized components
- **Hook Extractor** - Extract logic into custom hooks
- **Type Generator** - Generate TypeScript types

## Support

For issues or improvements to this skill, refer to the skill documentation or create an issue in your skill repository.
