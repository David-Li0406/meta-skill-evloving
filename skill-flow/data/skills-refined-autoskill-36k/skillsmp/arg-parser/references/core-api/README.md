# Core API

## ArgParser class

```typescript
class ArgParser<THandlerReturn = any> extends ArgParserBase
```

### Constructor

```typescript
new ArgParser(params: IArgParserParams<THandlerReturn>, flags?: readonly IFlag[], flagInheritance?: TFlagInheritance)
```

**IArgParserParams:**

```typescript
{
  appName: string
  appCommandName?: string
  description?: string
  handler?: MainHandler
  autoExit?: boolean
  handleErrors?: boolean
}
```

### Flag Methods

| Method                              | Description          |
| ----------------------------------- | -------------------- |
| `addFlag(flag: IFlag)`              | Add single flag      |
| `addFlags(flags: readonly IFlag[])` | Add multiple flags   |
| `hasFlag(name: string)`             | Check if flag exists |
| `getFlagDefinition(name: string)`   | Get processed flag   |

### Subcommand Methods

| Method                               | Description         |
| ------------------------------------ | ------------------- |
| `addSubCommand(config: ISubCommand)` | Register subcommand |
| `getSubCommand(name: string)`        | Get subcommand      |
| `getSubCommands()`                   | Get all subcommands |

### Parsing

```typescript
parse(processArgs?: string[], options?: IParseOptions): Promise<ParseResult>
```

**IParseOptions:**

```typescript
{
  skipHandlerExecution?: boolean
  isMcp?: boolean
}
```

### MCP Methods

| Method                                                 | Description                    |
| ------------------------------------------------------ | ------------------------------ |
| `withMcp(options: WithMcpOptions)`                     | Configure MCP server           |
| `addTool(config: ToolConfig)`                          | Add unified CLI/MCP tool       |
| `addMcpTool(config: McpToolConfig)`                    | Add MCP-only tool (deprecated) |
| `toMcpTools(options?)`                                 | Generate MCP tool structures   |
| `createMcpServer(serverInfo?, toolOptions?, logPath?)` | Create MCP server instance     |
| `startMcpServerWithTransport(...)`                     | Start with single transport    |
| `startMcpServerWithMultipleTransports(...)`            | Start with multiple transports |

### Utility Methods

| Method                | Description        |
| --------------------- | ------------------ |
| `getAppName()`        | Get app name       |
| `getAppCommandName()` | Get command name   |
| `getDescription()`    | Get description    |
| `helpText()`          | Generate help text |
| `printAll(filePath?)` | Print help to file |

## ArgParserBase class

Base class with core parsing functionality. Use `ArgParser` for full features.

## Exit Codes

| Code | Meaning                |
| ---- | ---------------------- |
| 0    | Success                |
| 1    | General error          |
| 2    | Invalid arguments      |
| 3    | Missing mandatory flag |
| 4    | Validation failed      |
