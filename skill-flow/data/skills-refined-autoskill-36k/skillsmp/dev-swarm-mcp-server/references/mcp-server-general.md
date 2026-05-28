# MCP Server Configuration - General Guidance

**Transport Types:**
- **stdio**: Standard input/output (most common for local servers)
- **HTTP**: HTTP-based communication
- **SSE**: Server-Sent Events

## Best Practices

1. **Always verify installation**: Use `<cli> mcp list` to confirm the server is configured.
2. **Restart required**: Exit and restart the CLI after making configuration changes.
3. **Project vs user scope**:
   - Use **project scope** for team-shared configs (only when no secrets are involved).
   - Use **user/global scope** for personal tools and API keys.
   - For **stdio** in user scope, use absolute paths so the server is reachable from any working directory.
   - For **stdio** in project scope, use paths relative to the project root to reduce external dependencies.
4. **Environment variables**: Store sensitive data in env vars, never commit secrets to VCS.
5. **Test connectivity**: Verify the server appears in list output and responds to basic requests.
6. **Timeouts**: Set startup timeouts for servers that take longer to initialize.
7. **Server availability**: Check whether a server exists before attempting to add it.
