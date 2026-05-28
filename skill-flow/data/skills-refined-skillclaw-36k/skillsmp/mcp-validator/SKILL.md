---
name: "mcp-validator"
description: "Valida endpoints MCP contra especificación 2024-11-05"
version: "1.0.0"
author: "MEMORY_P Team"
tags: ["mcp", "protocol", "validation", "json-rpc"]
---

# MCP Protocol Validator Skill

## Descripción
Valida que endpoints MCP cumplan con especificación 2024-11-05 y JSON-RPC 2.0.

## Cuándo Usar
- Implementar nuevo endpoint MCP
- Modificar handler existente
- Depurar problemas de compatibilidad
- Antes de release

## Checklist de Validación

### Request Validation
- [ ] `jsonrpc` es "2.0"
- [ ] `method` está presente
- [ ] `id` está presente (puede ser null)
- [ ] `params` cumple con schema del tool

### Response Validation
- [ ] `jsonrpc` es "2.0"
- [ ] `id` coincide con request
- [ ] Tiene `result` XOR `error`
- [ ] Error tiene `code` y `message`

### Tools Validation
- [ ] `name` es único
- [ ] `description` es clara
- [ ] `inputSchema` es JSON Schema válido
- [ ] `required` fields están en `properties`

## Test Request Template
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "analyze",
    "arguments": {
      "path": "./src",
      "pattern": "**/*.rs"
    }
  }
}
```

## Test con curl
```bash
curl -X POST http://localhost:4040/mcp \
  -H "Content-Type: application/json" \
  -d @test_request.json | jq
```

## Errores Comunes

### 1. ID Mismatch
```rust
// ❌ MAL: id diferente en response
JsonRpcResponse {
    id: json!(999), // Debe ser el mismo del request
    // ...
}
```

### 2. Result y Error Simultáneos
```rust
// ❌ MAL: ambos presentes
JsonRpcResponse {
    result: Some(json!({"ok": true})),
    error: Some(json!({"code": -32603})), // Solo uno debe estar
    // ...
}
```

### 3. Schema Inválido
```json
// ❌ MAL: required no está en properties
{
  "inputSchema": {
    "properties": {
      "path": {"type": "string"}
    },
    "required": ["path", "format"]
  }
}
```

## Comandos de Validación
```bash
# Verificar que servidor responde
curl -I http://localhost:4040/

# Test initialize
./scripts/test_mcp_initialize.sh

# Test tools/list
./scripts/test_mcp_tools_list.sh

# Test tools/call
./scripts/test_mcp_tools_call.sh
```

---

## 📚 Ver También

- [SKILLS.md](../../../SKILLS.md) - Documentación completa de Skills
- [AGENTS.md](../../../AGENTS.md) - Guía de Agents
- [Agent memory-p-mcp-expert](../../agents/memory-p-mcp-expert.agent.md) - Implementación MCP
- [Documentación MCP](../../../docs/REFERENCE_TOOLS.md) - Referencia de herramientas
- [MCP Specification](https://spec.modelcontextprotocol.io) - Especificación oficial

**Última actualización**: Enero 2026 (Post-merge PR #4)  
**Compatibilidad**: GitHub Copilot, Cursor, Windsurf, Claude Desktop
