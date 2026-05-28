---
name: generate-schema
description: Use when generating JSON schema from LandDefinitions or generating TypeScript client SDK from schema
---

# Generate Schema and Codegen

## Overview

Generate JSON schema from LandDefinitions and TypeScript client SDK from schema for Swift StateTree project.

**Announce at start:** "I'm using the generate-schema skill to generate schema and client SDK."

## When to Use

- After modifying LandDefinitions
- Before updating client code
- When schema needs to be regenerated
- When TypeScript types need to be updated

## The Process

### Step 1: Generate JSON Schema

**Command:**
```bash
cd Examples/HummingbirdDemo && swift run SchemaGen --output schema.json
```

**What it does:**
- Generates JSON schema from LandDefinitions
- Extracts types using `@StateNodeBuilder` and `@Payload` macro metadata
- Outputs to `schema.json` (or specified path)

**Output location:** `Examples/HummingbirdDemo/schema.json`

**How it works:**
- Uses macro metadata to extract type information
- Automatically detects `@Sync` fields
- Includes action and event definitions
- Generates path hashes and event hashes

### Step 2: Generate TypeScript Client SDK

**Command:**
```bash
cd Examples/HummingbirdDemo/WebClient && npm run codegen
```

**What it does:**
- Generates TypeScript client code from `schema.json`
- Creates type definitions for actions, events, and state
- Updates client SDK with latest schema

**Output location:** `Examples/HummingbirdDemo/WebClient/src/generated/`

**Generated files:**
- Type definitions for Land types
- Action and event payload types
- State type definitions
- Path hash mappings
- Event hash mappings

### Step 3: Verify Generated Files

**Check generated files:**
```bash
ls -la Examples/HummingbirdDemo/WebClient/src/generated/
```

**Verify schema is valid:**
```bash
cat Examples/HummingbirdDemo/schema.json | jq .
```

### Step 4: Commit Generated Files

**Important:** Generated files should be committed to version control.

```bash
git add Examples/HummingbirdDemo/schema.json
git add Examples/HummingbirdDemo/WebClient/src/generated/
git commit -m "chore: regenerate schema and client SDK"
```

## Schema Generation Details

### What Gets Extracted

- **StateNode types**: All types marked with `@StateNodeBuilder`
- **Action types**: All types marked with `@Payload` and conforming to `ActionPayload`
- **Event types**: All types marked with `@Payload` and conforming to `EventPayload`
- **Sync fields**: Fields marked with `@Sync` and their policies
- **Path hashes**: Computed hashes for state paths
- **Event hashes**: Computed hashes for event types

### Schema Structure

```json
{
  "version": "1.0.0",
  "defs": {
    "CounterState": { ... },
    "IncrementAction": { ... }
  },
  "lands": {
    "counter": {
      "stateType": "CounterState",
      "pathHashes": { ... },
      "eventHashes": { ... },
      "actions": { ... },
      "events": { ... }
    }
  }
}
```

## Codegen Details

### TypeScript SDK Generation

The codegen process:
1. Reads `schema.json`
2. Generates TypeScript interfaces for all types
3. Creates action/event payload types
4. Generates path hash reverse lookup tables
5. Creates event hash reverse lookup tables
6. Updates SDK runtime with new types

### Generated Type Structure

```typescript
export interface CounterState {
  count: number;
}

export interface IncrementAction {
  type: 'increment';
}

export interface IncrementResponse {
  newCount: number;
}
```

## Common Issues

### Schema Generation Fails

**Symptoms:** `swift run SchemaGen` fails with errors

**Solutions:**
- Check that all LandDefinitions are properly marked with `@StateNodeBuilder`
- Verify `@Payload` macros are correctly applied
- Check for compilation errors: `swift build`
- Ensure all dependencies are resolved: `swift package resolve`

### Codegen Fails

**Symptoms:** `npm run codegen` fails

**Solutions:**
- Verify `schema.json` exists and is valid JSON
- Check that schema file path is correct
- Ensure npm dependencies are installed: `npm install`
- Check codegen script configuration

### Generated Types Don't Match

**Symptoms:** TypeScript types don't match Swift types

**Solutions:**
- Regenerate schema from latest Swift code
- Clear generated files and regenerate
- Check for schema version mismatches
- Verify macro metadata is correct

## Integration with Development Workflow

### Before PR Submission

1. Regenerate schema if LandDefinitions changed
2. Regenerate client SDK
3. Commit generated files
4. Verify tests pass with new schema

### After Merging Changes

1. Pull latest changes
2. Regenerate schema if needed
3. Regenerate client SDK
4. Update client code to use new types

## Best Practices

- **Always commit generated files**: They're part of the codebase
- **Regenerate after LandDefinition changes**: Keep schema in sync
- **Verify schema validity**: Use `jq` to check JSON structure
- **Test with generated SDK**: Ensure client code works with new types
- **Document schema changes**: Note breaking changes in PR description
