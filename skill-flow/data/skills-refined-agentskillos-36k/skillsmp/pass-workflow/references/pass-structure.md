# Pass Structure and Implementation Patterns

**Note:** Import paths assume pass is in `src/passes/`. Adjust if needed.

## Pass Anatomy

Every unmangleJS pass follows this structure:

```typescript
import * as t from "@babel/types";
import { NodePath } from "@babel/traverse";
import { Pass, UnmangleContext } from "../core/index.js";

export const passName: Pass = {
  name: "pass-name",
  description: "Human-readable description of what this pass does",

  pre(ctx: UnmangleContext) {
    // Setup phase - runs once before traversal
    ctx.stats.processed = 0;
    ctx.stats.transformed = 0;
  },

  visitor(ctx: UnmangleContext) {
    return {
      // Babel visitor methods
      NodeType(path: NodePath<t.NodeType>) {
        // Transformation logic
      },
    };
  },

  post(ctx: UnmangleContext) {
    // Cleanup phase - runs once after traversal
    const processed = ctx.stats.processed ?? 0;
    const transformed = ctx.stats.transformed ?? 0;
    ctx.log.info(`Pass: ${transformed} nodes transformed (processed ${processed})`);
  },
};
```

## Lifecycle Phases

### 1. Pre Phase

Runs once before traversal. Initialize counters and state.

```typescript
pre(ctx: UnmangleContext) {
  ctx.stats.processed = 0;
  ctx.stats.transformed = 0;
  // Use ctx.stats for counting, module-level vars for collections
}
```

### 2. Visitor Phase

Called for each matching node during traversal.

```typescript
visitor(ctx: UnmangleContext) {
  return {
    BinaryExpression(path) {
      ctx.stats.processed = (ctx.stats.processed ?? 0) + 1;

      if (shouldTransform(path)) {
        doTransform(path);
        ctx.stats.transformed = (ctx.stats.transformed ?? 0) + 1;
        ctx.markAstDirty();
      }
    }
  };
}
```

**Key principles:**

- Check before transforming: `if (!isTargetPattern(path)) return;`
- Mark dirty: `ctx.markAstDirty()` for nodes, `ctx.markScopeDirty()` for variable changes
- Use descriptive logging: `ctx.log.at(path).debug("message")`

### 3. Post Phase

Runs once after traversal. Report statistics and clean up.

```typescript
post(ctx: UnmangleContext) {
  const processed = ctx.stats.processed ?? 0;
  const transformed = ctx.stats.transformed ?? 0;
  ctx.log.info(`${transformed} of ${processed} nodes transformed`);
}
```

## Common Pass Patterns

### Pattern 1: Simple Node Replacement

Replace nodes matching a pattern.

```typescript
visitor(ctx: UnmangleContext) {
  return {
    UnaryExpression(path) {
      if (path.node.operator !== "!") {
        return;
      }

      const argPath = path.get("argument");
      const result = tryEvaluateConstant(argPath);

      if (result.ok && typeof result.value === "boolean") {
        const replacement = t.booleanLiteral(!result.value); // Negate the boolean
        path.replaceWith(replacement);
        ctx.markAstDirty();
        ctx.markScopeDirty();
        ctx.log.at(path).debug(`Folded !${result.value} to ${!result.value}`);
      }
    }
  };
}
```

### Pattern 2: Collection and Analysis

**⚠️ WARNING:** Transform immediately in visitor. Collecting paths for later transformation is risky (paths may become stale).

```typescript
let collectedNodes: t.Node[] = []; // Module-level

export const passName: Pass = {
  name: "pass-name",

  pre(ctx: UnmangleContext) {
    collectedNodes = [];
    ctx.stats.targetsFound = 0;
  },

  visitor(ctx: UnmangleContext) {
    return {
      Identifier(path) {
        if (isTarget(path)) {
          transform(path); // Transform immediately
          ctx.markAstDirty();
          ctx.markScopeDirty();
          ctx.stats.targetsFound = (ctx.stats.targetsFound ?? 0) + 1;
          collectedNodes.push(path.node); // Or collect for analysis only
        }
      },
    };
  },

  post(ctx: UnmangleContext) {
    ctx.log.info(`Found ${ctx.stats.targetsFound ?? 0} targets`);
    collectedNodes = [];
  },
};
```

### Pattern 3: State Tracking

Track state across visitor calls using module-level variables.

```typescript
const scopeData = new Map<string, { variables: string[] }>(); // Module-level

export const passName: Pass = {
  name: "pass-name",

  pre(ctx: UnmangleContext) {
    scopeData.clear();
    ctx.stats.scopesProcessed = 0;
  },

  visitor(ctx: UnmangleContext) {
    return {
      Scope(path) {
        scopeData.set(path.scope.uid, {
          variables: Object.keys(path.scope.getAllBindings()),
        });
        ctx.stats.scopesProcessed = (ctx.stats.scopesProcessed ?? 0) + 1;
      },

      Identifier(path) {
        const data = scopeData.get(path.scope.uid);
        if (data) {
          ctx.log.at(path).debug(`Scope has ${data.variables.length} variables`);
        }
      },
    };
  },

  post(ctx: UnmangleContext) {
    ctx.log.info(`Processed ${ctx.stats.scopesProcessed ?? 0} scopes`);
    scopeData.clear();
  },
};
```

### Pattern 4: Conditional Transformation

Transform based on complex conditions.

```typescript
visitor(ctx: UnmangleContext) {
  return {
    CallExpression(path) {
      // Check callee
      if (!path.get("callee").isIdentifier({ name: "parseInt" })) {
        return;
      }

      // Check arguments
      const args = path.get("arguments");
      if (args.length !== 1 && args.length !== 2) {
        return;
      }

      // Check if first arg is constant
      const firstArg = args[0];
      const result = tryEvaluateConstant(firstArg);
      if (!result.ok) {
        return;
      }

      // Safe to transform
      const value = parseInt(result.value as string, 10);
      path.replaceWith(t.numericLiteral(value));
      ctx.markAstDirty();
    }
  };
}
```

### Pattern 5: Nested Visitor

**⚠️ WARNING:** `path.traverse()` creates nested traversals with performance risks. Prefer `path.skip()` to prevent entering nodes.

```typescript
visitor(ctx: UnmangleContext) {
  return {
    FunctionDeclaration(path) {
      path.skip(); // Prevent entering this function

      // ❌ AVOID nested traversal unless absolutely necessary
      // path.traverse({ Identifier(innerPath) { ... } });
    }
  };
}
```

## Context Usage

### Statistics

```typescript
ctx.stats.processed = 0; // Initialize
ctx.stats.processed = (ctx.stats.processed ?? 0) + 1; // Increment
const count = ctx.stats.processed ?? 0; // Read
```

### Logging

```typescript
ctx.log.debug("message"); // General
ctx.log.at(path).debug("context"); // With code snippet
```

### Dirty Flags

```typescript
ctx.markAstDirty(); // Always call when modifying nodes
ctx.markScopeDirty(); // Call when variables/bindings change
```

## State Management

**`UnmangleContext` only supports `stats` for custom data. Use module-level variables for other state:**

```typescript
let passState = new Map(); // Module-level (outside pass)

export const passName: Pass = {
  pre(ctx) {
    passState.clear();
  },
  visitor(ctx) {
    return {
      Identifier(path) {
        passState.set(path.node.name, path.node);
      },
    };
  },
  post(ctx) {
    passState.clear();
  },
};

// ❌ WRONG: ctx.customState = new Map();
```

**Best practices:**

- Clear module-level state in `pre()` or `post()`
- Use descriptive variable names
- Consider `WeakMap` for node-keyed storage (auto-GC)

## Import Patterns

### Standard Imports

```typescript
import * as t from "@babel/types";
import { NodePath } from "@babel/traverse";
import { Pass, UnmangleContext } from "../core/index.js";

// Utils imports
import { tryEvaluateConstant, valueToExpression } from "../utils/index.js";
```

### Export Pattern

```typescript
export const passName: Pass = {
  // ... pass implementation
};

// For barrel exports (src/passes/index.ts)
export { passName };
```

## Common Visitor Targets

### Expression Visitors

```typescript
BinaryExpression; // x + y, a * b
UnaryExpression; // -x, !true
LogicalExpression; // a && b, c || d
ConditionalExpression; // a ? b : c
CallExpression; // foo()
MemberExpression; // obj.prop, obj[prop]
Identifier; // variableName
```

### Statement Visitors

```typescript
ExpressionStatement; // expr;
VariableDeclaration; // const x = 1;
IfStatement; // if (cond) {}
ForStatement; // for (;;){}
WhileStatement; // while (cond) {}
ReturnStatement; // return val;
```

### Declaration Visitors

```typescript
FunctionDeclaration; // function foo() {}
VariableDeclarator; // const x = 1
ClassDeclaration; // class Foo {}
```

## Error Handling

```typescript
// Safe guards
if (!path.node) return;
if (!t.isIdentifier(path.node.callee)) return;
if (path.node.arguments.length === 0) return;

// Graceful degradation
try {
  const result = evaluateMember(path);
  if (result.ok) {
    path.replaceWith(result.value);
    ctx.markAstDirty();
  }
} catch (error) {
  ctx.log.at(path).warn(`Transformation failed: ${error.message}`);
}
```

## Testing Your Pass

```typescript
import { describe, it, expect } from "vitest";
import { yourPass } from "../../src/passes";
import { unmangle } from "../unmangle";

describe("your-pass pass", () => {
  it("should transform pattern X", async () => {
    const input = "const x = <obfuscated code>;";
    const { code } = await unmangle(input, [yourPass]);
    expect(code).toContain("const x = <deobfuscated code>;");
  });

  it("should not touch non-matching code", async () => {
    const input = "const x = normalCode();";
    const { code } = await unmangle(input, [yourPass]);
    expect(code).toBe(input);
  });
});

// Usage options:
await unmangle(input, [yourPass]); // Single pass
await unmangle(input, [pass1, pass2, pass3]); // Multiple passes
```

## Performance Tips

```typescript
// Early returns - cheap checks first
if (path.node.name.length > 10) return;
if (!complexCondition(path)) return;

// Cache expensive computations
const cache = new Map(); // Module-level
pre(ctx) { cache.clear(); }
visitor(ctx) {
  return {
    Identifier(path) {
      const key = getCacheKey(path);
      if (cache.has(key)) return cache.get(key);
      const result = expensiveComputation(path);
      cache.set(key, result);
      return result;
    }
  };
}

// Use path methods
const leftPath = path.get("left");  // ✅ GOOD
const left = path.node.left;        // ❌ AVOID (loses path context)
```

## Registering Your Pass

```typescript
// src/passes/registry.ts
import { yourPass } from "./your-pass.js";
export const ALL_PASSES: Pass[] = [
  // ... existing passes
  yourPass,
];

// src/passes/index.ts
export { yourPass } from "./your-pass.js";
```

## Deep Dive References

For comprehensive Babel plugin development knowledge:

- **Fundamentals**: Read `docs/en/babel-plugin-handbook.md` for AST basics, traversal, Paths, Visitors, Scopes, and Bindings
- **Advanced Pitfalls**: Read `docs/en/babel-api-gotchas.md` for deep dives into binding.constant, referencePaths, scope.crawl(), and reference invalidation

## Documentation Requirements

Each pass requires five files (kept in sync):

1. `src/passes/<pass-name>.ts` - Implementation
2. `tests/passes/<pass-name>.test.ts` - Tests
3. `examples/<pass-name>.js` - Examples
4. `docs/en/passes/<pass-name>.md` - English docs
5. `docs/zh-CN/passes/<pass-name>.md` - Chinese docs
