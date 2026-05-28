# Atlas Guardrails Integration Specification

This document defines the technical integration contract for using Atlas Guardrails within LLM CLI environments (Claude Code, Gemini CLI, Cursor, etc.) via the Model Context Protocol (MCP).

## 1. Tool Integration Mechanism

Atlas exposes its capabilities via a **stdio-based MCP Server**.

*   **Executable**: `atlas` (or `node dist/index.js`)
*   **Argument**: `mcp`
*   **Transport**: Standard Input/Output (JSON-RPC 2.0 over lines)

### Registration

**Claude Desktop / Code (`claude_desktop_config.json`):**
```json
{
  "mcpServers": {
    "atlas": {
      "command": "atlas",
      "args": ["mcp"]
    }
  }
}
```

**Generic MCP Client:**
Spawn the process `atlas mcp` and communicate via stdin/stdout.

## 2. API Schema (Tool Definitions)

The server exposes the following tools. Parameters follow JSON Schema Draft 7.

### `atlas_index`
Scans the repository, builds the symbol graph, and updates manifests.
*   **Parameters**: None
*   **Returns**: `TextContent` ("Indexing complete")
*   **Side Effects**: writes to `.atlas/` directory.

### `atlas_pack`
Retrieves a token-optimized context pack for a specific task.
*   **Parameters**:
    *   `task` (string, required): Description of the coding task (e.g., "fix bug in auth login").
    *   `budget` (number, optional): Character budget for the pack. Default: 50000.
*   **Returns**: `TextContent` (JSON string of the pack).
    *   **JSON Structure**:
        ```json
        {
          "task": "...",
          "files": [
            { "path": "src/auth.ts", "reason": "...", "content": "..." }
          ]
        }
        ```

### `atlas_find_duplicates`
Searches for existing symbols that match an intent to prevent duplication.
*   **Parameters**:
    *   `intent` (string, required): Description of the functionality or symbol name (e.g., "UuidGenerator").
*   **Returns**: `TextContent` (JSON string of candidates).

## 3. Execution Context

*   **Working Directory (CWD)**: The MCP server **MUST** be spawned with the CWD set to the **root of the target repository**. Atlas relies on `process.cwd()` to locate files and `.atlas` artifacts.
*   **Environment Variables**:
    *   `NODE_ENV`: `production` (recommended).
    *   `PATH`: Must include `node`.

## 4. Error Handling

*   **Protocol Errors**: Standard MCP JSON-RPC errors (Parse Error, Invalid Request).
*   **Tool Errors**: Tools return a successful MCP response content containing the error details if the logic fails (soft failure), or throw an MCP `ToolExecutionError` for fatal issues.
    *   **Format**: `isError: true` flag in MCP response (if supported) or text content starting with `Error:`.

## 5. Security Protocols

*   **File Access**: The tool reads all files in CWD (respecting `.gitignore`). It only writes to:
    *   `.atlas/` (Index artifacts)
    *   `pack.json` (Context pack output)
    *   `.ralphy/` (Config generation)
*   **Input Sanitization**: Inputs (`task`, `intent`) are treated as literal strings for search/matching. No shell command injection risks exist as arguments are not passed to a shell.
*   **Authentication**: None required. Security relies on the host CLI ensuring `atlas` is only run in trusted repositories.

## 6. Observability

*   **Logs**: The MCP server writes operational logs (progress, warnings) to **stderr**.
*   **Events**:
    *   `[INFO] Starting indexing...`
    *   `[WARN] Skipping file...`
*   **Format**: Plain text lines on stderr. Host CLIs should capture stderr for debugging but NOT parse it as protocol messages.

## 7. Testing Strategy

To verify integration:

1.  **Install**: `npm install -g atlas-guardrails`
2.  **Mock Client**: Use an MCP inspector (e.g., `@modelcontextprotocol/inspector`).
3.  **Test Cases**:
    *   **Case A (Index)**: Call `atlas_index`. Verify `.atlas/symbols.sqlite` is created in CWD.
    *   **Case B (Pack)**: Call `atlas_pack` with `task="test"`. Verify JSON return contains file contents.
    *   **Case C (Search)**: Call `atlas_find_duplicates`. Verify JSON return.
