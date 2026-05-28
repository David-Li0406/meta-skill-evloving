# MCP Resources and Prompts

## Table of Contents

- [🚨 MANDATORY: Read BEFORE Creating Resources/Prompts](#mandatory-read-before-creating-resourcesprompts)
- [Resources Overview](#resources-overview)
- [Resource Types](#resource-types)
- [Resource Patterns](#resource-patterns)
- [Prompts Overview](#prompts-overview)
- [Prompt Examples](#prompt-examples)
- [Resource Implementation](#resource-implementation)
- [Prompt Implementation](#prompt-implementation)
- [Use Cases](#use-cases)
- [Best Practices](#best-practices)
- [When to Use Resources vs Tools](#when-to-use-resources-vs-tools)

Create and configure MCP resources for data access and prompts for predefined workflows.

## 🚨 MANDATORY: Read BEFORE Creating Resources/Prompts

**CRITICAL**: You MUST read and understand these URLs:

### Primary Documentation (MUST READ)
- **[MUST READ] MCP Specification**: https://modelcontextprotocol.io/
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **When to Read**: Before any MCP resource or prompt creation
  - **Content**: Resources, prompts, schemas, protocol requirements
  - **Cache**: 15 minutes minimum

- **[MUST READ] Official MCP Guide**: https://code.claude.com/docs/en/mcp
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **When to Read**: Before MCP integration
  - **Content**: Integration patterns, best practices
  - **Cache**: 15 minutes minimum

### ⚠️ BLOCKING RULES
- **DO NOT proceed** without understanding MCP primitives
- **MUST validate** resource schemas before implementation
- **REQUIRED** to understand when to use resources vs tools

## Resources Overview

### What Are Resources?
Read-only data accessible via MCP servers with:
- URI-based identification
- Content retrieval on demand
- Can be text or binary
- Cached by Claude Code

### Resource Structure
```json
{
  "uri": "resource://identifier",
  "name": "Human-readable name",
  "description": "What this resource contains"
}
```

## Resource Types

### 1. File Resources
Access file system files.

```json
{
  "uri": "file:///path/to/document",
  "name": "Project Documentation",
  "description": "Main project documentation"
}
```

**Implementation**:
```typescript
@server.get_resource()
async function handleGetResource(uri) {
  if (uri.startsWith('file://')) {
    const filePath = uri.replace('file://', '');
    const content = await fs.readFile(filePath);
    return {
      contents: [{
        uri,
        mimeType: 'text/markdown',
        text: content
      }]
    };
  }
}
```

### 2. Database Resources
Access database tables or views.

```json
{
  "uri": "table://users",
  "name": "User Table",
  "description": "User account information"
}
```

**Implementation**:
```typescript
@server.get_resource()
async function handleGetResource(uri) {
  if (uri.startsWith('table://')) {
    const tableName = uri.replace('table://', '');
    const data = await db.query(`SELECT * FROM ${tableName}`);

    return {
      contents: [{
        uri,
        mimeType: 'application/json',
        text: JSON.stringify(data)
      }]
    };
  }
}
```

### 3. API Resources
Access API endpoints.

```json
{
  "uri": "api://github/repos",
  "name": "GitHub Repositories",
  "description": "List of repositories"
}
```

**Implementation**:
```typescript
@server.get_resource()
async function handleGetResource(uri) {
  if (uri.startsWith('api://')) {
    const endpoint = uri.replace('api://', '');
    const data = await fetch(`https://api.example.com/${endpoint}`);

    return {
      contents: [{
        uri,
        mimeType: 'application/json',
        text: await data.text()
      }]
    };
  }
}
```

## Resource Patterns

### Pattern 1: List Resources
Provide a list of available resources.

```typescript
@server.list_resources()
async function handleListResources() {
  return [
    {
      uri: "file:///docs/readme.md",
      name: "README",
      description: "Project documentation"
    },
    {
      uri: "table://users",
      name: "Users",
      description: "User database table"
    }
  ];
}
```

### Pattern 2: Dynamic Resources
Generate resources on-demand.

```typescript
@server.get_resource()
async function handleGetResource(uri) {
  const resource = await generateResource(uri);

  return {
    contents: [{
      uri,
      mimeType: resource.mimeType,
      text: resource.content
    }]
  };
}
```

### Pattern 3: Resource Caching
Cache frequently accessed resources.

```typescript
const resourceCache = new Map();

@server.get_resource()
async function handleGetResource(uri) {
  if (resourceCache.has(uri)) {
    return resourceCache.get(uri);
  }

  const resource = await fetchResource(uri);
  resourceCache.set(uri, resource);

  return resource;
}
```

## Prompts Overview

### What Are Prompts?
Predefined workflows from MCP servers:
- Reusable prompt templates
- Parameterized workflows
- Shared across sessions
- Can include tools and resources

### Prompt Structure
```json
{
  "name": "prompt_name",
  "description": "What this prompt does",
  "arguments": [
    {
      "name": "argument_name",
      "description": "Argument description"
    }
  ]
}
```

## Prompt Examples

### 1. Code Review Prompt
```json
{
  "name": "code_review",
  "description": "Comprehensive code review workflow",
  "arguments": [
    {
      "name": "file_path",
      "description": "Path to file to review"
    },
    {
      "name": "focus_area",
      "description": "Area to focus on (security, performance, style)"
    }
  ]
}
```

**Implementation**:
```typescript
@server.list_prompts()
async function handleListPrompts() {
  return [
    {
      name: "code_review",
      description: "Comprehensive code review workflow",
      arguments: [
        {
          name: "file_path",
          description: "Path to file to review"
        },
        {
          name: "focus_area",
          description: "Area to focus on (security, performance, style)"
        }
      ]
    }
  ];
}

@server.get_prompt()
async function handleGetPrompt(name, arguments) {
  if (name === "code_review") {
    return {
      description: "Code review focusing on " + arguments.focus_area,
      messages: [
        {
          role: "user",
          content: {
            type: "text",
            text: `Review the file at ${arguments.file_path} for ${arguments.focus_area} issues.`
          }
        }
      ]
    };
  }
}
```

### 2. API Documentation Prompt
```json
{
  "name": "document_api",
  "description": "Generate API documentation",
  "arguments": [
    {
      "name": "endpoint",
      "description": "API endpoint to document"
    }
  ]
}
```

### 3. Test Generation Prompt
```json
{
  "name": "generate_tests",
  "description": "Generate unit tests for code",
  "arguments": [
    {
      "name": "code",
      "description": "Code to generate tests for"
    },
    {
      "name": "framework",
      "description": "Testing framework (jest, pytest, etc.)"
    }
  ]
}
```

## Resource Implementation

### Python Implementation
```python
@server.list_resources()
async def handle_list_resources():
    return [
        {
            "uri": "file:///docs/readme.md",
            "name": "README",
            "description": "Project documentation"
        }
    ]

@server.get_resource()
async def handle_get_resource(uri):
    if uri.startswith("file://"):
        file_path = uri.replace("file://", "")
        content = await read_file(file_path)

        return {
            "contents": [{
                "uri": uri,
                "mimeType": "text/markdown",
                "text": content
            }]
        }
```

### TypeScript Implementation
```typescript
server.setRequestHandler('resources/list', async () => ({
  resources: [
    {
      uri: 'file:///docs/readme.md',
      name: 'README',
      description: 'Project documentation'
    }
  ]
}));

server.setRequestHandler('resources/read', async (request) => {
  const { uri } = request.params;

  if (uri.startsWith('file://')) {
    const filePath = uri.replace('file://', '');
    const content = await fs.readFile(filePath);

    return {
      contents: [{
        uri,
        mimeType: 'text/markdown',
        text: content
      }]
    };
  }
});
```

## Prompt Implementation

### Python Implementation
```python
@server.list_prompts()
async def handle_list_prompts():
    return [
        {
            "name": "code_review",
            "description": "Comprehensive code review workflow",
            "arguments": [
                {
                    "name": "file_path",
                    "description": "Path to file to review"
                }
            ]
        }
    ]

@server.get_prompt()
async def handle_get_prompt(name, arguments):
    if name == "code_review":
        return {
            "description": f"Review {arguments['file_path']}",
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"Review the file at {arguments['file_path']}"
                    }
                }
            ]
        }
```

### TypeScript Implementation
```typescript
server.setRequestHandler('prompts/list', async () => ({
  prompts: [
    {
      name: 'code_review',
      description: 'Comprehensive code review workflow',
      arguments: [
        {
          name: 'file_path',
          description: 'Path to file to review'
        }
      ]
    }
  ]
}));

server.setRequestHandler('prompts/get', async (request) => {
  const { name, arguments } = request.params;

  if (name === 'code_review') {
    return {
      description: `Review ${arguments.file_path}`,
      messages: [
        {
          role: 'user',
          content: {
            type: 'text',
            text: `Review the file at ${arguments.file_path}`
          }
        }
      ]
    };
  }
});
```

## Use Cases

### Resources
- Database tables and views
- Configuration files
- API responses
- Document repositories
- Data caches
- Generated reports

### Prompts
- Code review workflows
- Documentation generation
- Test creation
- Analysis workflows
- Best practice templates
- Review checklists

## Best Practices

### Resources
- Use descriptive URIs
- Implement proper caching
- Handle errors gracefully
- Document resource structure
- Consider pagination for large datasets

### Prompts
- Make prompts reusable
- Use clear parameter names
- Provide helpful descriptions
- Include examples
- Validate arguments

## When to Use Resources vs Tools

### Use Resources For
- Read-only data access
- File system access
- Database queries (read)
- API GET requests
- Cached data

### Use Tools For
- Write operations
- API POST/PUT/DELETE
- Complex computations
- Multi-step workflows
- Side effects

See **[servers.md](servers.md)** and **[tools.md](tools.md)** for related information.
