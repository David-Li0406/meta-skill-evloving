# Manual Review Guide

Checks that require human judgment or runtime testing.

## Security Checks

### Authentication (Remote Servers Only)
- [ ] Uses OAuth 2.0 with certificates from recognized authorities
- [ ] No hardcoded API keys or secrets in code
- [ ] Secrets loaded from environment variables
- [ ] No sensitive data in error messages

### Input Validation
- [ ] All inputs are validated before use
- [ ] SQL injection prevention (parameterized queries)
- [ ] Path traversal prevention (no `../` in file paths)
- [ ] Command injection prevention (no shell=True with user input)

```python
# BAD - command injection
os.system(f"ffmpeg {user_input}")

# GOOD - safe subprocess
subprocess.run(["ffmpeg", "-i", validated_path], check=True)
```

## Functionality Verification

### Description Accuracy Test
For each tool:
1. Read the description
2. Call the tool with valid inputs
3. Verify the result matches what the description promised

### Edge Case Testing
| Test Type | What to Check |
|-----------|---------------|
| Empty input | Does it handle `""`, `[]`, `{}`? |
| Invalid types | Wrong type for parameter? |
| Boundary values | Max int, very long strings? |
| Missing optional params | All optional params truly optional? |
| Concurrent calls | Thread-safe? |

## Performance Checks

### Response Time
- [ ] Tools respond in <2 seconds for typical operations
- [ ] Long operations show progress or are documented as slow

### Token Usage Analysis
Run this check:
```python
import json

async def measure_response_size(client, tool_name, args):
    result = await client.call_tool(tool_name, args)
    size = len(json.dumps(result.data))
    print(f"{tool_name}: {size} bytes")
    return size
```

Acceptable sizes:
- Simple status: <500 bytes
- List (paginated): <5KB
- Detailed item: <2KB

## Compatibility Checks

### Tool Name Conflicts
- [ ] No tool names that conflict with common MCP servers
- [ ] No generic names like `search`, `get`, `list` without prefix

### Protocol Compliance
- [ ] Supports Streamable HTTP transport (SSE being deprecated)
- [ ] Uses current dependency versions
- [ ] No deprecated MCP features

## User Experience

### Error Message Quality
Rate each error message:
| Rating | Criteria |
|--------|----------|
| 5 | Explains problem + suggests fix |
| 4 | Explains problem clearly |
| 3 | Identifies the error type |
| 2 | Generic but informative |
| 1 | "Error occurred" or similar |

### Tool Discoverability
- [ ] Tool names are intuitive
- [ ] Related tools are grouped logically
- [ ] No duplicate functionality across tools

## Final Verification

Before publishing to MCP Directory:

1. **Run Full Test Suite**
   ```bash
   pytest --cov=your_mcp_server
   ```

2. **Test with MCP Inspector**
   ```bash
   npx @anthropic-ai/mcp-inspector
   ```

3. **Test with Real LLM**
   - Can Claude use the tools correctly?
   - Are tool descriptions clear enough for the LLM?

4. **Documentation Review**
   - Are 3 working examples provided?
   - Is troubleshooting info available?
