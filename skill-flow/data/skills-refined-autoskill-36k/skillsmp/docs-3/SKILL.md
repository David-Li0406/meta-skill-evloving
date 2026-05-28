---
name: docs
description: Generate documentation, API docs, README files, and code comments. Use for creating or improving project documentation.
allowed-tools: Read, Write, Grep, Glob
---

# Documentation Generation Skill

Create comprehensive documentation for projects.

## 1. README Templates

**Basic README:**
```markdown
# Project Name

Brief description of what this project does.

## Installation

\`\`\`bash
npm install
# or
pip install -r requirements.txt
\`\`\`

## Usage

\`\`\`bash
npm start
# or
python app.py
\`\`\`

## Features

- Feature 1
- Feature 2
- Feature 3

## Configuration

Environment variables:
- `API_KEY` - Your API key
- `DATABASE_URL` - Database connection string

## Contributing

Pull requests are welcome.

## License

MIT
```

## 2. API Documentation

**OpenAPI/Swagger:**
```yaml
openapi: 3.0.0
info:
  title: My API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      responses:
        '200':
          description: Success
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
      properties:
        id:
          type: integer
        name:
          type: string
        email:
          type: string
```

## 3. Code Comments

**Python Docstrings:**
```python
def calculate_total(items, tax_rate=0.08):
    """
    Calculate total price including tax.

    Args:
        items (list): List of items with price and quantity
        tax_rate (float, optional): Tax rate. Defaults to 0.08.

    Returns:
        float: Total price including tax

    Raises:
        ValueError: If items is empty or tax_rate is negative

    Example:
        >>> items = [{'price': 10, 'qty': 2}]
        >>> calculate_total(items)
        21.6
    """
    if not items:
        raise ValueError("Items cannot be empty")
    if tax_rate < 0:
        raise ValueError("Tax rate cannot be negative")

    subtotal = sum(item['price'] * item['qty'] for item in items)
    return subtotal * (1 + tax_rate)
```

**JavaScript JSDoc:**
```javascript
/**
 * Calculate total price including tax
 * @param {Array<{price: number, qty: number}>} items - Items to calculate
 * @param {number} [taxRate=0.08] - Tax rate
 * @returns {number} Total price including tax
 * @throws {Error} If items is empty
 * @example
 * const items = [{price: 10, qty: 2}];
 * calculateTotal(items); // 21.6
 */
function calculateTotal(items, taxRate = 0.08) {
    if (!items.length) {
        throw new Error("Items cannot be empty");
    }
    const subtotal = items.reduce((sum, item) =>
        sum + item.price * item.qty, 0);
    return subtotal * (1 + taxRate);
}
```

## 4. Architecture Documentation

```markdown
# Architecture

## Overview

System consists of three main components:
- Frontend (React)
- Backend API (Node.js)
- Database (PostgreSQL)

## Components

### Frontend
- React SPA
- Redux for state management
- Material-UI components

### Backend
- Express.js REST API
- JWT authentication
- PostgreSQL database

### Database Schema

\`\`\`sql
users (id, email, password_hash, created_at)
orders (id, user_id, total, status, created_at)
\`\`\`

## Data Flow

1. User makes request
2. Frontend sends API call
3. Backend validates and processes
4. Database updated
5. Response returned to frontend
```

## 5. Generate Docs from Code

**Python (Sphinx):**
```bash
# Install
pip install sphinx

# Initialize
sphinx-quickstart docs

# Generate
cd docs
make html
```

**JavaScript (JSDoc):**
```bash
# Install
npm install -g jsdoc

# Generate
jsdoc src/ -d docs/
```

## 6. Changelog

```markdown
# Changelog

## [1.2.0] - 2026-01-22

### Added
- New user authentication feature
- CSV export functionality

### Changed
- Improved performance of search
- Updated UI design

### Fixed
- Bug in payment processing
- XSS vulnerability in comments

### Removed
- Deprecated API endpoint /old-users
```

## When to Use This Skill

Use `/docs` for generating documentation, API specs, README files, and code comments.
