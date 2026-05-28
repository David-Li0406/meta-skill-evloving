---
name: muebleria-docs
description: >
  Documentation standards for MuebleriaIris project.
  Trigger: When writing or updating documentation, README files, or API docs.
license: Apache-2.0
metadata:
  author: muebleria-iris
  version: "1.0"
  scope: [root]
  auto_invoke:
    - "Writing documentation"
    - "Updating README files"
    - "Documenting API endpoints"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## When to Use

Use this skill when:

- Writing or updating README files
- Documenting API endpoints
- Creating developer guides
- Writing code comments
- Documenting database schema

---

## Documentation Types

```
README.md          → Project overview, setup instructions
API.md             → Endpoint documentation
ARCHITECTURE.md    → System design, tech stack
CONTRIBUTING.md    → Contribution guidelines
CHANGELOG.md       → Version history
```

---

## Critical Patterns

### Pattern 1: README Structure

```markdown
# Project Name

Brief description (1-2 sentences)

## Features

- Feature 1
- Feature 2

## Tech Stack

**Frontend:**
- Astro 5.16.4
- React 19.2.1
- TailwindCSS 4.1.17

**Backend:**
- Flask 3.0+
- PostgreSQL 15+
- SQLAlchemy 2.0+

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.9+
- PostgreSQL 15+

### Installation

\`\`\`bash
# Frontend
npm install
npm run dev

# Backend
pip install -r backend/requirements.txt
python backend/run.py
\`\`\`

## Project Structure

\`\`\`
project/
├── src/            # Frontend
├── backend/        # API
└── agents/         # AI agents
\`\`\`

## License

Apache-2.0
```

### Pattern 2: API Documentation

```markdown
## API Endpoints

### Products

#### Get All Products

\`\`\`http
GET /api/productos
\`\`\`

**Response (200):**
\`\`\`json
[
  {
    "id": 1,
    "sku": "SOF001",
    "nombre": "Sofá 3 Cuerpos",
    "precio": 1500,
    "material": "Tela"
  }
]
\`\`\`

#### Create Product

\`\`\`http
POST /api/productos
Content-Type: application/json
\`\`\`

**Request Body:**
\`\`\`json
{
  "sku": "SOF001",
  "nombre": "Sofá 3 Cuerpos",
  "precio": 1500,
  "material": "Tela",
  "id_categoria": 1
}
\`\`\`

**Response (201):**
\`\`\`json
{
  "mensaje": "Producto creado exitosamente",
  "producto": { ... }
}
\`\`\`

**Errors:**
- `400` - Missing required fields
- `409` - SKU already exists
- `500` - Server error
```

### Pattern 3: Code Comments

```python
# Python docstrings
def create_orden(data):
    """
    Crea una nueva orden de venta y descuenta inventario.
    
    Args:
        data (dict): Datos de la orden con id_cliente e items
        
    Returns:
        tuple: (response_json, status_code)
        
    Raises:
        ValueError: Si el stock es insuficiente
        
    Example:
        >>> create_orden({'id_cliente': 1, 'items': [...]})
        ({'mensaje': 'Éxito', ...}, 201)
    """
    pass
```

```typescript
// TypeScript JSDoc
/**
 * Displays a product card with image, name, and price.
 * 
 * @param props - Product card properties
 * @param props.nombre - Product name
 * @param props.precio - Product price
 * @returns A styled product card component
 * 
 * @example
 * <ProductCard nombre="Sofá" precio={1500} />
 */
export function ProductCard(props: ProductCardProps) {
  // ...
}
```

---

## Documentation Best Practices

### DO:
- Start with a clear, one-sentence description
- Include code examples for every pattern
- Show both request and response formats
- Document error cases
- Use tables for structured data
- Add diagrams for complex flows

### DON'T:
- Assume prior knowledge
- Use jargon without explanation
- Include outdated examples
- Leave endpoints undocumented
- Skip error handling docs

---

## Markdown Conventions

```markdown
# H1: Page title (one per document)
## H2: Major sections
### H3: Subsections

**Bold** for emphasis
*Italic* for technical terms
`inline code` for commands/variables
\`\`\`language for code blocks

[Link text](url)
![Alt text](image-url)

> Blockquotes for important notes

- Unordered lists
1. Ordered lists

| Table | Headers |
|-------|---------|
| Data  | Values  |
```

---

## Database Schema Documentation

```markdown
## Database Schema

### Productos Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id_producto | INTEGER | PRIMARY KEY | Auto-increment ID |
| sku | VARCHAR(50) | UNIQUE, NOT NULL | Product code |
| nombre | VARCHAR(100) | NOT NULL | Product name |
| precio | NUMERIC(10,2) | NOT NULL | Price in currency |
| id_categoria | INTEGER | FOREIGN KEY | References categoria.id_categoria |

**Relationships:**
- One-to-Many with `imagenes_productos`
- One-to-One with `inventario`
- Many-to-One with `categoria`
```

---

## Commands

```bash
# Generate API docs (if using tools)
# None currently (manual documentation)

# Preview markdown locally
npm install -g markdown-preview
markdown-preview README.md
```

---

## QA Checklist

- [ ] README has setup instructions
- [ ] All API endpoints documented
- [ ] Code examples are tested and working
- [ ] Error responses documented
- [ ] Database schema documented
- [ ] Links are not broken
- [ ] Consistent formatting throughout
- [ ] Images have alt text

---

## Resources

- **Markdown Guide**: https://www.markdownguide.org
- **API Documentation**: REST API best practices
