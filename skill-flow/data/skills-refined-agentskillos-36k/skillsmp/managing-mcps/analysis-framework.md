# MCP Analysis Framework

Comprehensive evaluation criteria for assessing Model Context Protocol server implementations.

## Analysis Process

Follow this systematic approach when analyzing any MCP server.

### Phase 1: Discovery and Inventory

**Objective**: Understand what the MCP provides and how it's structured.

#### 1.1 File Discovery

Use Glob patterns to find:
- `**/package.json` - Node.js projects
- `**/pyproject.toml` or `**/setup.py` - Python projects
- `**/*server*.ts` or `**/*mcp*.ts` - TypeScript implementations
- `**/*server*.py` or `**/*mcp*.py` - Python implementations
- `**/config.json` - Configuration files

#### 1.2 Project Structure Analysis

Read and document:
- **Language/Runtime**: Node.js/TypeScript, Python, other
- **SDK Usage**: Which MCP SDK and version
- **Entry Point**: Main server file
- **Dependencies**: Required packages
- **Build System**: TypeScript, Python packaging, etc.

#### 1.3 Capability Inventory

Search for capability registrations:

**Tools:**
```typescript
server.setRequestHandler(ListToolsRequestSchema, ...)
server.setRequestHandler(CallToolRequestSchema, ...)
```
```python
@app.list_tools()
@app.call_tool()
```

**Resources:**
```typescript
server.setRequestHandler(ListResourcesRequestSchema, ...)
server.setRequestHandler(ReadResourceRequestSchema, ...)
```
```python
@app.list_resources()
@app.read_resource()
```

**Prompts:**
```typescript
server.setRequestHandler(ListPromptsRequestSchema, ...)
server.setRequestHandler(GetPromptRequestSchema, ...)
```
```python
@app.list_prompts()
@app.get_prompt()
```

Document each capability:
- Name
- Description
- Input schema
- Implementation location

### Phase 2: Protocol Compliance

**Objective**: Verify adherence to MCP specification 2025-06-18.

#### 2.1 Protocol Version

Check initialization:
- [ ] Declares protocol version "2025-06-18"
- [ ] Handles initialization request/response
- [ ] Sends initialized notification

Search for: `protocolVersion`, `initialize`, `notifications/initialized`

#### 2.2 Capability Declaration

Verify server declares capabilities correctly:
```typescript
{
  capabilities: {
    tools: {},           // If implements tools
    resources: {},       // If implements resources
    prompts: {}          // If implements prompts
  }
}
```

Check:
- [ ] Declares all implemented capabilities
- [ ] Does not declare unimplemented capabilities
- [ ] Uses correct capability structure

#### 2.3 Request Handlers

For each capability, verify:

**Tools:**
- [ ] ListToolsRequest returns valid tool array
- [ ] Each tool has name, description, inputSchema
- [ ] inputSchema is valid JSON Schema
- [ ] CallToolRequest handles all listed tools
- [ ] Returns ToolResult with content array
- [ ] Handles unknown tools with error

**Resources:**
- [ ] ListResourcesRequest returns resource array
- [ ] Each resource has uri, name, optional description/mimeType
- [ ] URIs follow valid format (scheme://path)
- [ ] ReadResourceRequest handles all listed resources
- [ ] Returns ResourceContents with uri, mimeType, content
- [ ] Handles unknown resources with error

**Prompts:**
- [ ] ListPromptsRequest returns prompt array
- [ ] Each prompt has name, optional description/arguments
- [ ] GetPromptRequest handles all listed prompts
- [ ] Returns messages array with role and content
- [ ] Handles unknown prompts with error

#### 2.4 Message Format

Check JSON-RPC compliance:
- [ ] All requests have jsonrpc: "2.0", id, method, params
- [ ] All responses have jsonrpc: "2.0", id, result OR error
- [ ] Notifications have jsonrpc: "2.0", method, params (no id)
- [ ] Error objects have code, message, optional data

#### 2.5 Transport Implementation

Verify transport layer:

**stdio:**
- [ ] Uses StdioServerTransport (TypeScript) or stdio_server (Python)
- [ ] Connects transport to server
- [ ] Handles process lifecycle correctly

**SSE:**
- [ ] Implements SSE endpoint
- [ ] Handles long-lived connections
- [ ] Sends proper SSE events

### Phase 3: Architecture Quality

**Objective**: Assess implementation quality and maintainability.

#### 3.1 Code Organization

Evaluate structure:
- [ ] Clear separation of concerns
- [ ] Tool implementations separated from protocol handling
- [ ] Configuration management isolated
- [ ] Reusable utility functions
- [ ] Type definitions (TypeScript) or type hints (Python)

**Rating:**
- **Excellent**: Modular, well-organized, clear responsibilities
- **Good**: Mostly organized with minor issues
- **Fair**: Some organization but could improve
- **Poor**: Monolithic, unclear structure

#### 3.2 Error Handling

Check error management:
- [ ] Try-catch around all tool implementations
- [ ] Proper error propagation
- [ ] Meaningful error messages
- [ ] Correct JSON-RPC error codes
- [ ] No unhandled promise rejections
- [ ] Graceful degradation on failures

**Critical Issues:**
- Unhandled errors causing crashes
- Generic error messages
- Wrong error codes
- Silent failures

#### 3.3 Input Validation

Verify validation practices:
- [ ] JSON Schema validation on tool inputs
- [ ] Type checking before use
- [ ] Range/format validation
- [ ] Sanitization of user inputs
- [ ] Path traversal prevention
- [ ] SQL injection prevention (if applicable)
- [ ] Command injection prevention (if applicable)

**Critical Issues:**
- Missing validation on security-sensitive inputs
- Direct use of user input in system calls
- SQL queries without parameterization
- File paths without sanitization

#### 3.4 SDK Usage

Assess SDK integration:
- [ ] Uses official MCP SDK
- [ ] SDK version is current (not deprecated)
- [ ] Follows SDK patterns correctly
- [ ] Uses provided types and schemas
- [ ] Leverages SDK utilities

**Issues:**
- Old SDK version with known issues
- Bypassing SDK for custom implementations
- Incorrect use of SDK APIs
- Missing SDK type definitions

#### 3.5 Async/Await Patterns

Evaluate async handling:
- [ ] Consistent async/await usage
- [ ] No blocking synchronous operations
- [ ] Proper promise chaining
- [ ] Error handling in async functions
- [ ] No race conditions

**Issues:**
- Blocking operations in async context
- Unhandled promise rejections
- Race conditions in concurrent operations

### Phase 4: Tool Design Quality

**Objective**: Evaluate tool effectiveness and usability.

#### 4.1 Tool Naming

Check naming conventions:
- [ ] Clear, descriptive names (verb-noun format)
- [ ] Consistent naming pattern across tools
- [ ] No ambiguous or generic names
- [ ] Follows domain conventions

**Good Examples:**
- `fetch-user-data`
- `calculate-statistics`
- `search-documents`

**Poor Examples:**
- `process` (too generic)
- `do-thing` (unclear)
- `tool1` (non-descriptive)

#### 4.2 Tool Descriptions

Evaluate descriptions:
- [ ] Clear purpose statement
- [ ] Explains what tool does (not how)
- [ ] Mentions key parameters
- [ ] Includes usage context
- [ ] Natural language, not technical jargon

**Rating:**
- **Excellent**: Complete, clear, contextual
- **Good**: Clear but could add context
- **Fair**: Basic but missing details
- **Poor**: Unclear or missing

#### 4.3 Schema Design

Assess input schemas:
- [ ] All parameters documented
- [ ] Correct JSON Schema types
- [ ] Required fields marked
- [ ] Optional fields have defaults or clear purpose
- [ ] Constraints specified (min/max, pattern, enum)
- [ ] Nested objects properly structured

**Issues:**
- Missing parameter descriptions
- Incorrect type specifications
- Missing required fields
- Unclear optional parameters
- No validation constraints

#### 4.4 Tool Atomicity

Evaluate tool scope:
- [ ] Each tool has single clear purpose
- [ ] Operations are atomic (succeed or fail together)
- [ ] No side effects beyond stated purpose
- [ ] Idempotent when appropriate
- [ ] Composable with other tools

**Issues:**
- Multi-purpose tools doing unrelated things
- Partial success scenarios
- Hidden side effects
- Non-idempotent operations that should be

#### 4.5 Result Format

Check result structure:
- [ ] Consistent result format across tools
- [ ] Appropriate content types (text, image, resource)
- [ ] Structured data when applicable
- [ ] Error results use isError flag
- [ ] Clear success indicators

**Issues:**
- Inconsistent result formats
- Unstructured text when JSON would be better
- Missing error indicators
- Ambiguous success/failure

### Phase 5: Resource Design Quality

**Objective**: Evaluate resource implementation (if applicable).

#### 5.1 URI Design

Check URI patterns:
- [ ] Follows URI format (scheme://path)
- [ ] Consistent scheme usage
- [ ] Hierarchical path structure
- [ ] Query parameters for variants
- [ ] No sensitive data in URIs

**Good Examples:**
- `db://users/123`
- `file:///documents/report.pdf`
- `api://service/v1/data?format=json`

**Issues:**
- Invalid URI format
- Inconsistent schemes
- Flat structure without hierarchy
- Credentials in URIs

#### 5.2 Resource Discovery

Evaluate listing:
- [ ] All resources discoverable via ListResources
- [ ] Resource templates for dynamic URIs
- [ ] Clear names and descriptions
- [ ] Appropriate mimeType declarations
- [ ] Logical grouping

#### 5.3 Resource Content

Check content handling:
- [ ] Correct mimeType
- [ ] Efficient content delivery
- [ ] Caching when appropriate
- [ ] Streaming for large resources
- [ ] Proper encoding

#### 5.4 Resource Updates

If subscriptions supported:
- [ ] Subscribe/unsubscribe implemented
- [ ] Notifications sent on changes
- [ ] Efficient change detection
- [ ] No unnecessary notifications

### Phase 6: Security Assessment

**Objective**: Identify security vulnerabilities and risks.

Load security-best-practices.md for detailed criteria.

#### 6.1 Authentication/Authorization

Check access controls:
- [ ] Authentication implemented if needed
- [ ] Authorization checks on sensitive operations
- [ ] Token/key validation
- [ ] Rate limiting on public operations
- [ ] Session management if stateful

**Critical Issues:**
- No auth on sensitive operations
- Hardcoded credentials
- Missing rate limiting
- No session timeout

#### 6.2 Input Sanitization

Verify input handling:
- [ ] All user inputs validated
- [ ] Path traversal prevention
- [ ] SQL injection prevention
- [ ] Command injection prevention
- [ ] XSS prevention (if generating HTML)
- [ ] JSON injection prevention

**Critical Issues:**
- Direct use of user input in system calls
- Unsanitized SQL queries
- File operations without path validation
- Eval or exec with user input

#### 6.3 Environment Variables

Check configuration security:
- [ ] Secrets via environment variables (not hardcoded)
- [ ] Validation of environment values
- [ ] Secure defaults
- [ ] Documentation of required variables
- [ ] No logging of sensitive values

**Issues:**
- Hardcoded API keys
- Secrets in config files
- Missing environment variable validation
- Logging sensitive data

#### 6.4 Error Information Disclosure

Evaluate error messages:
- [ ] No stack traces to client
- [ ] No internal paths exposed
- [ ] No sensitive data in errors
- [ ] Generic errors for security issues
- [ ] Detailed logs server-side only

**Issues:**
- Full stack traces returned
- Database schema in errors
- File paths exposed
- Credential hints in messages

### Phase 7: Configuration Assessment

**Objective**: Evaluate Claude Code integration setup.

Load configuration-guide.md for detailed patterns.

#### 7.1 Configuration Format

Check config.json structure:
- [ ] Correct mcpServers format
- [ ] Valid command/args for stdio
- [ ] Valid url for SSE
- [ ] Environment variables properly set
- [ ] No sensitive data directly in config

#### 7.2 Connection Parameters

Verify parameters:
- [ ] Correct path to server executable
- [ ] All required arguments included
- [ ] Environment variables available
- [ ] Working directory appropriate
- [ ] Timeout settings if needed

#### 7.3 Documentation

Check installation docs:
- [ ] Installation instructions clear
- [ ] Configuration example provided
- [ ] Environment variables documented
- [ ] Troubleshooting guide included
- [ ] Examples of usage

### Phase 8: Testing and Validation

**Objective**: Verify functionality through testing.

#### 8.1 MCP Inspector Testing

Test with Inspector:
- [ ] Server starts successfully
- [ ] Tools appear in list
- [ ] Tools execute without errors
- [ ] Resources accessible
- [ ] Prompts render correctly
- [ ] Error handling works

#### 8.2 Claude Code Integration

Test in Claude Code:
- [ ] Server connects successfully
- [ ] Tools appear in Claude's tool list
- [ ] Tools execute from Claude
- [ ] Results display correctly
- [ ] Errors handled gracefully

#### 8.3 Edge Cases

Test boundary conditions:
- [ ] Missing required parameters
- [ ] Invalid input types
- [ ] Large inputs
- [ ] Concurrent requests
- [ ] Network failures (if applicable)
- [ ] Resource exhaustion

### Phase 9: Documentation Quality

**Objective**: Assess documentation completeness.

#### 9.1 README

Check README.md:
- [ ] Purpose clearly stated
- [ ] Installation instructions
- [ ] Configuration steps
- [ ] Usage examples
- [ ] Environment variables documented
- [ ] Troubleshooting section

#### 9.2 Code Comments

Evaluate inline documentation:
- [ ] Complex logic explained
- [ ] Public APIs documented
- [ ] Security considerations noted
- [ ] Edge cases mentioned
- [ ] TODOs for incomplete features

#### 9.3 API Documentation

For tools/resources/prompts:
- [ ] All capabilities documented
- [ ] Parameter descriptions
- [ ] Return value formats
- [ ] Error conditions
- [ ] Usage examples

## Analysis Output Format

Structure findings as:

### Summary

**MCP Name**: [name]
**Version**: [version]
**Language**: [TypeScript/Python/Other]
**Capabilities**: [Tools, Resources, Prompts]

### Overall Assessment

**Quality Score**: [Excellent/Good/Fair/Poor]
**Protocol Compliance**: [Pass/Fail]
**Security Posture**: [Secure/Needs Attention/Vulnerable]
**Recommendation**: [Production Ready/Needs Improvements/Major Issues]

### Critical Issues

List show-stoppers:
1. [Issue with severity and impact]
2. ...

### Major Issues

List significant problems:
1. [Issue with explanation]
2. ...

### Minor Issues

List improvements:
1. [Suggestion]
2. ...

### Strengths

Highlight positive aspects:
- [What's done well]
- ...

### Recommendations

Specific actionable improvements:
1. **[Category]**: [What to change and why]
2. ...

### Priority Actions

Ordered list of what to fix first:
1. [Critical fix]
2. [Major improvement]
3. [Minor enhancement]

## Scoring Rubric

**Excellent (90-100%)**
- Full protocol compliance
- Comprehensive security
- Well-organized code
- Complete documentation
- Thorough testing

**Good (70-89%)**
- Protocol compliant
- Basic security measures
- Organized code
- Adequate documentation
- Some testing

**Fair (50-69%)**
- Mostly compliant with gaps
- Security concerns
- Disorganized code
- Incomplete documentation
- Limited testing

**Poor (<50%)**
- Protocol violations
- Security vulnerabilities
- Poor code quality
- Missing documentation
- No testing

## Common Anti-Patterns

Identify these during analysis:

**Protocol:**
- Custom implementations instead of SDK
- Non-standard message formats
- Missing capability declarations

**Architecture:**
- Monolithic tool implementations
- No error handling
- Synchronous blocking operations

**Security:**
- Hardcoded credentials
- No input validation
- Command injection vulnerabilities

**Tools:**
- Generic tool names
- Multi-purpose tools
- Missing schema descriptions

**Resources:**
- Non-standard URI formats
- No caching for expensive resources
- Missing mimeType declarations

## Analysis Checklist

Quick checklist for rapid assessment:

- [ ] SDK version current
- [ ] Protocol version correct
- [ ] All capabilities declared
- [ ] Tool schemas valid
- [ ] Input validation present
- [ ] Error handling comprehensive
- [ ] Security measures implemented
- [ ] Documentation complete
- [ ] Configuration example provided
- [ ] Tested with Inspector
- [ ] Claude Code integration works
