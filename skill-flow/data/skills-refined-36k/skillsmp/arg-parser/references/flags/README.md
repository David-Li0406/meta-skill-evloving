# Flag Definitions

## IFlag Interface

```typescript
interface IFlag {
  name: string;
  options: string[];
  type?: TParsedArgsTypeFromFlagDef;
  description?: string | string[];
  valueHint?: string;
  defaultValue?: any;
  mandatory?: boolean | ((parsedArgs: TParsedArgs) => boolean);
  allowMultiple?: boolean;
  allowLigature?: boolean;
  flagOnly?: boolean;
  validate?: (value, parsedArgs?) => boolean | string | void;
  enum?: any[];
  env?: string | string[];
  dxtOptions?: IDxtOptions;
  dynamicRegister?: DynamicRegisterFn;
  setWorkingDirectory?: boolean;
  positional?: number;
}
```

## Flag Types

| Type         | Description       | Example                    |
| ------------ | ----------------- | -------------------------- |
| `String`     | String value      | `type: String`             |
| `Number`     | Numeric value     | `type: Number`             |
| `Boolean`    | True/false        | `type: Boolean`            |
| `Array`      | Array of strings  | `type: Array`              |
| `Object`     | Key-value pairs   | `type: Object`             |
| `"string"`   | String literal    | `type: "string"`           |
| `"number"`   | Number literal    | `type: "number"`           |
| `"boolean"`  | Boolean literal   | `type: "boolean"`          |
| `"array"`    | Array literal     | `type: "array"`            |
| `"object"`   | Object literal    | `type: "object"`           |
| `Zod schema` | Custom validation | `type: z.object({...})`    |
| `function`   | Custom parser     | `type: (v) => parseInt(v)` |

## Flag Options

```typescript
// Short and long options
{ name: "input", options: ["--input", "-i"], ... }

// Multiple long options
{ name: "verbose", options: ["--verbose", "--debug", "-v"], ... }
```

## Flag Examples

### String flag with default

```typescript
{ name: "output", options: ["--output", "-o"], type: String, defaultValue: "output.txt" }
```

### Number flag with validation

```typescript
{
  name: "port",
  options: ["--port", "-p"],
  type: Number,
  validate: (value) => value > 0 && value <= 65535 ? true : "Port must be 1-65535"
}
```

### Enum flag

```typescript
{
  name: "level",
  options: ["--level", "-l"],
  type: String,
  enum: ["debug", "info", "warn", "error"]
}
```

### Mandatory flag with conditional

```typescript
{
  name: "config",
  options: ["--config", "-c"],
  type: String,
  mandatory: (args) => !args.useDefault
}
```

### Array flag (multiple values)

```typescript
{
  name: "files",
  options: ["--files", "-f"],
  type: String,
  allowMultiple: true
}
// Usage: -f file1.txt -f file2.txt -> ["file1.txt", "file2.txt"]
```

### Flag-only (presence)

```typescript
{
  name: "verbose",
  options: ["--verbose", "-v"],
  type: Boolean,
  flagOnly: true
}
// Any value after -v is NOT consumed
```

### Zod schema for structured input

```typescript
{
  name: "config",
  options: ["--config"],
  type: z.object({
    host: z.string(),
    port: z.number(),
    ssl: z.boolean().optional()
  })
}
```

### Environment variable fallback

```typescript
{
  name: "token",
  options: ["--token", "-t"],
  type: String,
  env: "API_TOKEN"
}
// Priority: CLI flag > env var > default
```

### Dynamic flag registration

```typescript
{
  name: "mode",
  options: ["--mode", "-m"],
  type: String,
  dynamicRegister: async (ctx) => {
    if (ctx.value === "advanced") {
      return [
        { name: "debug", options: ["--debug"], type: Boolean },
        { name: "trace", options: ["--trace"], type: Boolean }
      ]
    }
    return []
  }
}
```

### Positional argument capture

```typescript
{
  name: "file",
  options: ["--file", "-f"],
  type: String,
  positional: 1
}
// Captures first positional after flags
// Usage: cmd --file input.txt other.txt -> file = "input.txt"
```

### Set working directory

```typescript
{
  name: "workspace",
  options: ["--workspace", "-w"],
  type: String,
  setWorkingDirectory: true
}
// Changes cwd for file operations in this flag's handler
```

## Flag Inheritance

```typescript
import { FlagInheritance } from "@alcyone-labs/arg-parser";

FlagInheritance.NONE; // No inheritance
FlagInheritance.DirectParentOnly; // Direct parent only
FlagInheritance.AllParents; // All parent flags
```

Usage: `new ArgParser(params, flags, FlagInheritance.AllParents)`
