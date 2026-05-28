---
name: api-documentation
description: Generate comprehensive API documentation following OpenAPI 3.0 and REST standards when creating or documenting APIs, endpoints, or web services
---

# API Documentation Skill

Generate professional API documentation following industry standards.

## OpenAPI 3.0 Format

```yaml
openapi: 3.0.0
info:
  title: Your API Name
  version: 1.0.0
  description: Clear API description

servers:
  - url: https://api.example.com/v1

paths:
  /users:
    get:
      summary: List all users
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'

components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
      properties:
        id:
          type: string
        email:
          type: string
```

## Documentation Checklist

- [ ] Endpoint path and HTTP method
- [ ] Clear summary (1 line)
- [ ] Detailed description (2-3 sentences)
- [ ] All query/path/header parameters documented
- [ ] Request body schema (if applicable)
- [ ] All response status codes
- [ ] Response schemas
- [ ] Authentication requirements
- [ ] Rate limiting information
- [ ] Example requests and responses

---

## Credits

**Author:** [Michel Abboud](https://github.com/michelabboud)
**AI Assistance:** Created with the help of Claude Code (Anthropic)
**License:** Apache-2.0

💡 **Want more?** Explore [claude-code-helper](https://github.com/michelabboud/claude-code-helper) for 30+ agents, 13+ skills, 9 MCP servers, and comprehensive guides.
