---
name: documentation-generator
description: Use this skill to generate comprehensive documentation from code, APIs, and specifications, including API documentation, developer guides, architecture docs, and user manuals.
---

# Body of the merged SKILL.md

## Identity
Documentation Generator Skill - Generates comprehensive documentation from code, APIs, and specifications including API docs, developer guides, architecture documentation, and user manuals.

## Capabilities
- Generating API documentation
- Creating developer guides
- Documenting architecture
- Creating user manuals
- Generating OpenAPI/Swagger specs
- Updating existing documentation

## Instructions
### Execution Process

#### Step 1: Identify Documentation Type
Determine documentation type:
- **API Documentation**: Endpoint references
- **Developer Guide**: Setup and usage
- **Architecture Docs**: System overview
- **User Manual**: Feature guides

#### Step 2: Extract Information
Gather documentation content:
- Read code and comments
- Analyze API endpoints
- Extract examples
- Understand architecture

#### Step 3: Generate Documentation
Create documentation:
- Follow documentation templates
- Include examples
- Add troubleshooting
- Create clear structure

#### Step 4: Validate Documentation
Validate quality:
- Check completeness
- Verify examples work
- Ensure clarity
- Validate links

## Integration
**Integration with Technical Writer Agent**:
- Uses this skill for documentation generation
- Ensures documentation quality
- Validates completeness

**Integration with Developer Agent**:
- Generates API documentation
- Creates inline documentation
- Updates docs with code changes

## Best Practices
1. **Extract from Code**: Use code as source of truth
2. **Include Examples**: Provide working examples
3. **Keep Updated**: Sync docs with code
4. **Clear Structure**: Organize logically
5. **User-Focused**: Write for users, not system

## Examples
### Formatting Examples
**API Documentation**
````markdown
# Users API

## Endpoints

### GET /api/users
List all users with pagination.

**Query Parameters:**
- `page` (number): Page number (default: 1)
- `limit` (number): Items per page (default: 10)

**Response:**
```json
{
  "data": [
    {
      "id": "uuid",
      "email": "user@example.com",
      "name": "User Name"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 100
  }
}
```
````

**Example:**
```bash
curl -X GET "http://localhost:3000/api/users?page=1&limit=10"
```

**Developer Guide**
```markdown
# Developer Guide

## Getting Started

### Prerequisites
- Node.js 18+
- pnpm 8+

### Installation
```bash
pnpm install
```

### Development
```bash
pnpm dev
```

## Architecture
[Architecture overview]

## Development Workflow
[Development process]
```

### Usage Examples
**Example Commands**:
```
# Generate API documentation
Generate API documentation for app/api/users

# Generate developer guide
Generate developer guide for this project

# Generate architecture docs
Generate architecture documentation

# Generate OpenAPI spec
Generate OpenAPI specification from API routes
```