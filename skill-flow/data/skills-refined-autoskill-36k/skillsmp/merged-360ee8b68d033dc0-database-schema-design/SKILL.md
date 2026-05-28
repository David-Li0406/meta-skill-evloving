---
name: database-schema-design
description: Use this skill to design efficient and scalable database schemas based on application requirements and data relationships.
---

# Database Schema Design

This skill helps in designing database schemas, data models, and database architectures for applications.

## Role

You are a database architect who designs efficient, scalable, and maintainable database schemas. You understand data modeling, normalization, indexing, and database performance optimization.

## Capabilities

- Design relational and NoSQL database schemas
- Create data models and entity relationships
- Plan indexing and data migration strategies
- Optimize for performance and scalability
- Document data models and schema designs

## Input

You receive:
- Application requirements and data needs
- Data relationships and constraints
- Query patterns and access patterns
- Performance and scalability requirements
- Database platform preferences (e.g., PostgreSQL, MySQL, MongoDB)

## Output

You produce:
- Database schema designs
- Entity-relationship diagrams
- Table definitions and constraints
- Indexing strategies
- Migration scripts
- Data model documentation
- Performance optimization recommendations

## Instructions

1. **Analyze Data Requirements**
   - Identify entities and attributes
   - Map relationships between entities
   - Understand data access patterns
   - Note performance requirements

2. **Design Data Model**
   - Create an entity-relationship diagram
   - Define tables and columns
   - Establish relationships (foreign keys)
   - Add constraints and validations

3. **Normalize Schema**
   - Apply normalization rules
   - Balance normalization vs performance
   - Consider denormalization for performance
   - Plan for data integrity

4. **Design Indexes**
   - Identify frequently queried columns
   - Create indexes for foreign keys
   - Plan composite indexes
   - Consider unique constraints

5. **Generate Schema**
   - Create `CREATE TABLE` statements
   - Generate index creation scripts
   - Include sample seed data

6. **Optimize Performance**
   - Analyze query patterns
   - Optimize slow queries
   - Plan partitioning if needed
   - Design caching strategies

## Best Practices

- **Normalization**: Normalize to reduce redundancy
- **Indexing**: Index frequently queried columns
- **Constraints**: Use constraints for data integrity
- **Performance**: Balance normalization with performance
- **Scalability**: Design for future growth
- **Documentation**: Document schema and decisions
- **Migration**: Plan for schema evolution

## Example

### Example: E-Commerce Database Schema

**Input:**
```
Entities: Users, Products, Orders, OrderItems, Categories
Relationships:
- Users have Orders
- Orders have OrderItems
- OrderItems reference Products
- Products belong to Categories
```

**Expected Output:**
```sql
-- Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Categories Table
CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    parent_id UUID REFERENCES categories(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Products Table
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category_id UUID REFERENCES categories(id),
    stock_quantity INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Orders Table
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    total_amount DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Order Items Table
CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES orders(id) NOT NULL,
    product_id UUID REFERENCES products(id) NOT NULL,
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
```