# Types

## IHandlerContext

```typescript
interface IHandlerContext<TCurrentCommandArgs = any, TParentCommandArgs = any> {
  args: TCurrentCommandArgs;
  parentArgs?: TParentCommandArgs;
  commandChain: string[];
  parser: ArgParserInstance;
  parentParser?: ArgParserInstance;
  isMcp?: boolean;
  getFlag?: (name: string) => any;
  displayHelp: () => void;
  rootPath?: string;
  logger: any;
}
```

## TParsedArgs

```typescript
type TParsedArgs<TFlags extends readonly ProcessedFlag[]> = {
  [K in TFlags[number]["name"]]: ExtractFlagType<
    Extract<TFlags[number], { name: K }>
  >;
};
```

## IFlagCore (Input)

```typescript
interface IFlagCore {
  name: string;
  options: string[];
  type?: TParsedArgsTypeFromFlagDef;
  description?: string | string[];
  valueHint?: string;
  defaultValue?: any;
  mandatory?: boolean | ((parsedArgs: any) => boolean);
  allowMultiple?: boolean;
  allowLigature?: boolean;
  flagOnly?: boolean;
  validate?: (value?, parsedArgs?) => boolean | string | void;
  enum?: any[];
  env?: string | string[];
  dxtOptions?: IDxtOptions;
  dynamicRegister?: DynamicRegisterFn;
  setWorkingDirectory?: boolean;
  positional?: number;
  default?: any; // Alias for defaultValue
  required?: boolean | ((parsedArgs: any) => boolean); // Alias for mandatory
  env?: string | string[];
}
```

## ProcessedFlag

```typescript
interface ProcessedFlag {
  name: string;
  options: string[];
  type: TParsedArgsTypeFromFlagDef;
  description?: string | string[];
  valueHint?: string;
  defaultValue?: any;
  mandatory?: boolean | ((parsedArgs: TParsedArgs) => boolean);
  allowMultiple?: boolean;
  allowLigature?: boolean;
  flagOnly?: boolean;
  validate?: (value?, parsedArgs?) => boolean | string | void;
  enum?: any[];
  env?: string | string[];
  dxtOptions?: IDxtOptions;
  dynamicRegister?: DynamicRegisterFn;
  setWorkingDirectory?: boolean;
  positional?: number;
}
```

## TParsedArgsTypeFromFlagDef

```typescript
type TParsedArgsTypeFromFlagDef =
  | StringConstructor
  | NumberConstructor
  | BooleanConstructor
  | ArrayConstructor
  | ObjectConstructor
  | ((value: string) => any)
  | ((value: string) => Promise<any>)
  | ZodTypeAny
  | "string"
  | "number"
  | "boolean"
  | "array"
  | "object";
```

## ISubCommand

```typescript
interface ISubCommand<
  TSubCommandFlags extends FlagsArray = FlagsArray,
  TParentCommandFlags extends FlagsArray = FlagsArray,
  THandlerReturn = any,
> {
  name: string;
  description?: string;
  parser: ArgParserInstance;
  handler?: (
    ctx: IHandlerContext<
      TParsedArgs<TSubCommandFlags>,
      TParsedArgs<TParentCommandFlags>
    >,
  ) => THandlerReturn | Promise<THandlerReturn>;
  isMcp?: boolean;
  mcpServerInfo?: { name: string; version: string; description?: string };
  mcpToolOptions?: any;
}
```

## ParseResult

```typescript
interface ParseResult<T = any> {
  success: boolean;
  exitCode: number;
  data?: T;
  message?: string;
  shouldExit?: boolean;
  type?: "success" | "error" | "help" | "version" | "debug";
}
```

## ToolConfig

```typescript
interface ToolConfig {
  name: string;
  description?: string;
  flags: readonly IFlag[];
  handler: (ctx: IHandlerContext) => Promise<any> | any;
  outputSchema?: OutputSchemaConfig;
}
```

## OutputSchemaConfig

```typescript
type OutputSchemaConfig =
  | OutputSchemaPatternName // "successError" | "successWithData" | etc.
  | z.ZodTypeAny // Zod schema object
  | Record<string, z.ZodTypeAny>; // Schema definition object
```

## McpTransportConfig

```typescript
interface McpTransportConfig {
  type: "stdio" | "sse" | "streamable-http";
  port?: number;
  host?: string;
  path?: string;
  sessionIdGenerator?: () => string;
  cors?: CorsOptions;
  auth?: AuthOptions;
}
```

## CorsOptions

```typescript
interface CorsOptions {
  origins?: "*" | string | RegExp | Array<string | RegExp>;
  methods?: string[];
  headers?: string[];
  exposedHeaders?: string[];
  credentials?: boolean;
  maxAge?: number;
}
```

## AuthOptions

```typescript
interface AuthOptions {
  required?: boolean;
  scheme?: "bearer" | "jwt";
  allowedTokens?: string[];
  validator?: (req, token) => boolean | Promise<boolean>;
  jwt?: JwtVerifyOptions;
  publicPaths?: string[];
  protectedPaths?: string[];
  customMiddleware?: (req, res, next) => any;
}
```

## JwtVerifyOptions

```typescript
interface JwtVerifyOptions {
  algorithms?: ("HS256" | "RS256")[];
  secret?: string;
  publicKey?: string;
  getPublicKey?: (header, payload) => string | Promise<string>;
  audience?: string | string[];
  issuer?: string | string[];
  clockToleranceSec?: number;
}
```

## LogPath

```typescript
type LogPath =
  | string
  | { path: string; relativeTo?: "entry" | "cwd" | "absolute" };
```

## IDxtOptions

```typescript
interface IDxtOptions {
  sensitive?: boolean;
  localDefault?: string;
  type?: "string" | "directory" | "file" | "boolean" | "number";
  multiple?: boolean;
  min?: number;
  max?: number;
  default?: any;
  title?: string;
}
```

## FlagInheritance

```typescript
const FlagInheritance = {
  NONE: "none",
  DirectParentOnly: "direct-parent-only",
  AllParents: "all-parents",
} as const;

type TFlagInheritance = "none" | "direct-parent-only" | "all-parents" | boolean;
```
