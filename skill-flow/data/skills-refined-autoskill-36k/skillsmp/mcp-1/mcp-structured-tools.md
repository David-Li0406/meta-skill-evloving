---
name: mcp-structured-tools
description: "MCP structured tools with JSON Schema validation. Use when asking 'structured tools', 'JSON schema', 'tool validation', 'mcp parameters', or 'tool input validation'."
---

# MCP Structured Tools

Define MCP tools with JSON Schema validation for reliable parameter handling.

> **Skill Metadata**
> Category: `mcp`
> Priority: `MEDIUM`
> SDK Version: `0.9.25+`
> Related Skills: [`mcp-integration-guide`](../../01-core-sdk/mcp-integration-guide.md), [`mcp-resources`](mcp-resources.md)
> Related Subagents: `mcp-specialist` (complex schemas, validation logic)

## Quick Reference

- **JSON Schema**: Define tool input/output contracts
- **Validation**: Automatic parameter validation before tool execution
- **Type Safety**: Strongly-typed tool parameters
- **Documentation**: Self-documenting tool interfaces

## Basic Structured Tool

```python
from kailash.workflow.builder import WorkflowBuilder
from kailash.runtime import LocalRuntime

workflow = WorkflowBuilder()

# MCP server with structured tools
workflow.add_node("IterativeLLMAgentNode", "agent", {
    "provider": "openai",
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Get weather for NYC and London"}],
    "mcp_servers": [{
        "name": "weather",
        "transport": "stdio",
        "command": "python",
        "args": ["-m", "weather_mcp_server"],
        "tools": [
            {
                "name": "get_weather",
                "description": "Get current weather for a city",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "City name"
                        },
                        "units": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "default": "celsius"
                        }
                    },
                    "required": ["city"]
                }
            }
        ]
    }],
    "auto_discover_tools": True,
    "auto_execute_tools": True
})

runtime = LocalRuntime()
results, run_id = runtime.execute(workflow.build())
```

## Advanced Schema Patterns

### Complex Type Validation

```python
workflow.add_node("IterativeLLMAgentNode", "agent", {
    "provider": "openai",
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Search documents"}],
    "mcp_servers": [{
        "name": "search",
        "transport": "http",
        "url": "https://api.company.com/mcp",
        "tools": [
            {
                "name": "search_documents",
                "description": "Search documents with filters",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "minLength": 1,
                            "maxLength": 500
                        },
                        "filters": {
                            "type": "object",
                            "properties": {
                                "date_range": {
                                    "type": "object",
                                    "properties": {
                                        "start": {"type": "string", "format": "date"},
                                        "end": {"type": "string", "format": "date"}
                                    }
                                },
                                "categories": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "minItems": 1
                                }
                            }
                        },
                        "limit": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 100,
                            "default": 10
                        }
                    },
                    "required": ["query"]
                }
            }
        ]
    }]
})
```

### Nested Objects and Arrays

```python
workflow.add_node("IterativeLLMAgentNode", "agent", {
    "mcp_servers": [{
        "name": "crm",
        "transport": "http",
        "url": "https://crm-api.com/mcp",
        "tools": [
            {
                "name": "create_contact",
                "description": "Create a new contact",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "email": {
                            "type": "string",
                            "format": "email"
                        },
                        "phones": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "type": {
                                        "type": "string",
                                        "enum": ["mobile", "work", "home"]
                                    },
                                    "number": {"type": "string", "pattern": "^\\+?[0-9]{10,15}$"}
                                },
                                "required": ["type", "number"]
                            }
                        },
                        "address": {
                            "type": "object",
                            "properties": {
                                "street": {"type": "string"},
                                "city": {"type": "string"},
                                "zip": {"type": "string", "pattern": "^[0-9]{5}$"}
                            }
                        }
                    },
                    "required": ["name", "email"]
                }
            }
        ]
    }]
})
```

## Output Schema Validation

```python
workflow.add_node("IterativeLLMAgentNode", "agent", {
    "mcp_servers": [{
        "name": "analytics",
        "transport": "http",
        "url": "https://analytics-api.com/mcp",
        "tools": [
            {
                "name": "get_report",
                "description": "Generate analytics report",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "report_type": {
                            "type": "string",
                            "enum": ["sales", "traffic", "conversion"]
                        },
                        "period": {"type": "string"}
                    },
                    "required": ["report_type"]
                },
                "output_schema": {
                    "type": "object",
                    "properties": {
                        "metrics": {
                            "type": "object",
                            "properties": {
                                "total": {"type": "number"},
                                "average": {"type": "number"},
                                "trend": {"type": "string", "enum": ["up", "down", "stable"]}
                            },
                            "required": ["total", "average"]
                        },
                        "timestamp": {"type": "string", "format": "date-time"}
                    },
                    "required": ["metrics", "timestamp"]
                }
            }
        ]
    }]
})
```

## Conditional Schemas

```python
workflow.add_node("IterativeLLMAgentNode", "agent", {
    "mcp_servers": [{
        "name": "payment",
        "transport": "http",
        "url": "https://payment-api.com/mcp",
        "tools": [
            {
                "name": "process_payment",
                "description": "Process payment with different methods",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "amount": {"type": "number", "minimum": 0.01},
                        "currency": {"type": "string", "enum": ["USD", "EUR", "GBP"]},
                        "method": {
                            "type": "string",
                            "enum": ["card", "bank_transfer", "paypal"]
                        }
                    },
                    "required": ["amount", "currency", "method"],
                    "allOf": [
                        {
                            "if": {"properties": {"method": {"const": "card"}}},
                            "then": {
                                "properties": {
                                    "card_number": {"type": "string", "pattern": "^[0-9]{16}$"},
                                    "cvv": {"type": "string", "pattern": "^[0-9]{3,4}$"}
                                },
                                "required": ["card_number", "cvv"]
                            }
                        },
                        {
                            "if": {"properties": {"method": {"const": "bank_transfer"}}},
                            "then": {
                                "properties": {
                                    "account_number": {"type": "string"},
                                    "routing_number": {"type": "string"}
                                },
                                "required": ["account_number", "routing_number"]
                            }
                        }
                    ]
                }
            }
        ]
    }]
})
```

## Schema Reuse with Definitions

```python
workflow.add_node("IterativeLLMAgentNode", "agent", {
    "mcp_servers": [{
        "name": "inventory",
        "transport": "http",
        "url": "https://inventory-api.com/mcp",
        "schema_definitions": {
            "address": {
                "type": "object",
                "properties": {
                    "street": {"type": "string"},
                    "city": {"type": "string"},
                    "zip": {"type": "string"}
                },
                "required": ["street", "city", "zip"]
            }
        },
        "tools": [
            {
                "name": "create_warehouse",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "address": {"$ref": "#/definitions/address"}
                    }
                }
            },
            {
                "name": "update_supplier",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "supplier_id": {"type": "string"},
                        "billing_address": {"$ref": "#/definitions/address"},
                        "shipping_address": {"$ref": "#/definitions/address"}
                    }
                }
            }
        ]
    }]
})
```

## Best Practices

### 1. Descriptive Properties

```python
{
    "name": "search_products",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query (e.g., 'laptop 15 inch')",
                "minLength": 1
            },
            "price_range": {
                "type": "object",
                "description": "Optional price filter",
                "properties": {
                    "min": {"type": "number", "description": "Minimum price in USD"},
                    "max": {"type": "number", "description": "Maximum price in USD"}
                }
            }
        },
        "required": ["query"]
    }
}
```

### 2. Default Values

```python
{
    "name": "get_data",
    "input_schema": {
        "type": "object",
        "properties": {
            "page": {"type": "integer", "default": 1, "minimum": 1},
            "page_size": {"type": "integer", "default": 20, "minimum": 1, "maximum": 100},
            "sort_order": {"type": "string", "enum": ["asc", "desc"], "default": "asc"}
        }
    }
}
```

### 3. Validation Constraints

```python
{
    "name": "create_user",
    "input_schema": {
        "type": "object",
        "properties": {
            "username": {
                "type": "string",
                "minLength": 3,
                "maxLength": 20,
                "pattern": "^[a-zA-Z0-9_]+$"
            },
            "email": {
                "type": "string",
                "format": "email"
            },
            "age": {
                "type": "integer",
                "minimum": 18,
                "maximum": 120
            }
        },
        "required": ["username", "email"]
    }
}
```

## Error Handling

```python
# IterativeLLMAgentNode automatically validates inputs
# If validation fails, it includes error in response

workflow.add_node("IterativeLLMAgentNode", "agent", {
    "provider": "openai",
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Search with invalid params"}],
    "mcp_servers": [{
        "name": "search",
        "transport": "http",
        "url": "https://api.com/mcp",
        "tools": [
            {
                "name": "search",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "minLength": 1}
                    },
                    "required": ["query"]
                }
            }
        ]
    }]
})

# Agent will report: "Validation failed: 'query' is required"
```

## Related Patterns

- **MCP Integration**: [`mcp-integration-guide`](../../01-core-sdk/mcp-integration-guide.md)
- **MCP Resources**: [`mcp-resources`](mcp-resources.md)

## When to Escalate to Subagent

Use `mcp-specialist` subagent when:
- Implementing complex conditional schemas (oneOf, anyOf, allOf)
- Creating reusable schema libraries
- Building schema validation middleware
- Troubleshooting validation failures

## Quick Tips

- Always include descriptions for better LLM understanding
- Use enums to constrain valid values
- Set reasonable min/max constraints
- Provide default values when possible
- Use format validators (email, date, uri)

<!-- Trigger Keywords: structured tools, JSON schema, tool validation, mcp parameters, tool input validation, schema validation, mcp types, parameter types -->
