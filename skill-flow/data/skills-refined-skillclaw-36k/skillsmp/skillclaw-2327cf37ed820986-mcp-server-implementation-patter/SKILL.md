---
name: mcp-server-implementation-patterns
description: Use this skill when building Model Context Protocol (MCP) servers to extend AI capabilities with custom tools, resources, and prompt templates using either Spring AI or LangChain4j.
---

# MCP Server Implementation Patterns

Implement Model Context Protocol (MCP) servers to extend AI capabilities with standardized tools, resources, and prompt templates. This skill covers both Spring AI and LangChain4j implementations.

## When to Use

Use this skill when building:
- AI applications requiring external tool integration
- Enterprise MCP servers with multi-domain support (e.g., GitHub, databases, APIs)
- Function calling servers with declarative patterns
- Dynamic tool providers with context-aware filtering
- Resource-based data access systems for AI models
- Prompt template servers for standardized AI interactions
- Scalable AI agents with resilient tool execution
- Spring Boot applications with native MCP integration
- Production-ready MCP servers with security and monitoring
- Microservices that expose AI capabilities via MCP protocol

## Quick Start

### Basic MCP Server with Spring AI

Create a simple MCP server with function calling:

```java
@SpringBootApplication
@EnableMcpServer
public class WeatherMcpApplication {

    public static void main(String[] args) {
        SpringApplication.run(WeatherMcpApplication.class, args);
    }
}

@Component
public class WeatherTools {

    @Tool(description = "Get current weather for a city")
    public WeatherData getWeather(@ToolParam("City name") String city) {
        // Implementation
        return new WeatherData(city, "Sunny", 22.5);
    }
}
```

### Basic MCP Server with LangChain4j

Create a simple MCP server with one tool:

```java
MCPServer server = MCPServer.builder()
    .server(new StdioServer.Builder())
    .addToolProvider(new SimpleWeatherToolProvider())
    .build();

server.start();
```

### Function Calling Setup (Spring AI)

Configure function calling in `application.properties`:

```properties
spring.ai.openai.api-key=${OPENAI_API_KEY}
spring.ai.mcp.enabled=true
spring.ai.mcp.transport=stdio
```

### Spring Boot Integration (LangChain4j)

Configure MCP server in Spring Boot:

```java
@Bean
public MCPSpringConfig mcpServer(List<ToolProvider> tools) {
    return MCPSpringConfig.builder()
        .tools(tools)
        .server(new StdioServer.Builder())
        .build();
}
```

## Core Concepts

### MCP Architecture

MCP standardizes AI application connections:
- **Tools**: Executable functions (database queries, API calls)
- **Resources**: Data sources (files, schemas, documentation)
- **Prompts**: Pre-configured templates for tasks
- **Transport**: Communication layer (stdio, HTTP, WebSocket)

```
AI Application ←→ MCP Client ←→ Transport ←→ MCP Server ←→ External Service
```

### Key Components

- **MCPServer**: Main server instance with configuration
- **ToolProvider**: Tool specification and execution interface
- **ResourceListProvider/ResourceReadHandler**: Resource access
- **PromptListProvider/PromptGetHandler**: Template management
- **Transport**: Communication mechanisms (stdio, HTTP)