---
name: muebleria-db
description: >
  PostgreSQL database schema for MuebleriaIris ERP system.
  Trigger: When working with database migrations, schema design, or SQL operations.
license: Apache-2.0
metadata:
  author: muebleria-iris
  version: "1.0"
  scope: [root]
  auto_invoke:
    - "Modifying database schema"
    - "Creating migrations"
    - "Writing SQL queries"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## When to Use

Use this skill when:

- Designing or modifying database schema
- Creating database migrations
- Writing raw SQL queries
- Optimizing database performance
- Setting up PostgreSQL

---

## Database Schema (8 Tables)

### Catálogo
- `categoria` - Product categories
- `productos` - Furniture products
- `imagenes_productos` - Product images

### Logística
- `proovedores` - Suppliers
- `inventario` - Stock management

### Comercial
- `clientes` - Customers
- `ordenes` - Sales orders
- `detalles_orden` - Order line items
- `pagos` - MercadoPago payments

### Administración
- `roles` - User roles (Admin, Vendedor)
- `usuarios` - System users

---

## Critical Patterns

### Pattern 1: Foreign Keys

```sql
ALTER TABLE productos 
ADD CONSTRAINT fk_categoria 
FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria);

ALTER TABLE inventario 
ADD CONSTRAINT fk_producto 
FOREIGN KEY (id_producto) REFERENCES productos(id_producto);
```

### Pattern 2: Indexes for Performance

```sql
CREATE INDEX idx_productos_categoria ON productos(id_categoria);
CREATE INDEX idx_ordenes_cliente ON ordenes(id_cliente);
CREATE INDEX idx_ordenes_fecha ON ordenes(fecha_creacion DESC);
CREATE INDEX idx_productos_sku ON productos(sku);
```

### Pattern 3: Check Constraints

```sql
ALTER TABLE productos 
ADD CONSTRAINT check_precio_positive CHECK (precio > 0);

ALTER TABLE inventario 
ADD CONSTRAINT check_stock_non_negative CHECK (cantidad_stock >= 0);
```

---

## Schema Design Decisions

### IDs Convention
- Primary keys: `id_{table_singular}` (e.g., `id_producto`)
- Auto-increment integers
- Never expose to API (use SKU or UUID for external references)

### Relationships
```
categoria 1 ----< * productos
productos 1 ----< * imagenes_productos
productos 1 ---- 1 inventario
productos 1 ----< * detalles_orden
clientes 1 ----< * ordenes
ordenes 1 ----< * detalles_orden
ordenes 1 ----< * pagos
usuarios * ----< 1 roles
```

---

## Migration Examples

### Add Column

```sql
-- Add new field to productos
ALTER TABLE productos ADD COLUMN peso_kg NUMERIC(5,2);
```

### Modify Column

```sql
-- Change string length
ALTER TABLE productos ALTER COLUMN material TYPE VARCHAR(150);
```

### Drop Column (Safe)

```sql
-- Check dependencies first
SELECT * FROM information_schema.table_constraints 
WHERE constraint_schema = 'public' AND table_name = 'productos';

-- Then drop
ALTER TABLE productos DROP COLUMN campo_obsoleto;
```

---

## Commands

```bash
# Connect to database
psql -U muebleria_user -d muebleria_erp

# Backup database
pg_dump -U muebleria_user muebleria_erp > backup.sql

# Restore database
psql -U muebleria_user muebleria_erp < backup.sql

# Create database
createdb -U postgres muebleria_erp

# Drop database
dropdb -U postgres muebleria_erp
```

---

## Useful Queries

### Check Stock Alerts

```sql
SELECT p.nombre, i.cantidad_stock, i.stock_minimo
FROM inventario i
JOIN productos p ON i.id_producto = p.id_producto
WHERE i.cantidad_stock <= i.stock_minimo;
```

### Top Selling Products

```sql
SELECT p.nombre, SUM(d.cantidad) as total_vendido
FROM detalles_orden d
JOIN productos p ON d.id_producto = p.id_producto
GROUP BY p.id_producto, p.nombre
ORDER BY total_vendido DESC
LIMIT 10;
```

### Orders by Status

```sql
SELECT estado, COUNT(*) as cantidad, SUM(monto_total) as total
FROM ordenes
GROUP BY estado;
```

---

## QA Checklist

- [ ] All foreign keys have indexes
- [ ] Check constraints for business rules
- [ ] Timestamps use `timezone.utc`
- [ ] Backup strategy in place
- [ ] No sensitive data in plain text
- [ ] Cascading deletes configured correctly

---

## Resources

- **Models Reference**: `backend/app/models.py`
- **Config**: `backend/config.py`
