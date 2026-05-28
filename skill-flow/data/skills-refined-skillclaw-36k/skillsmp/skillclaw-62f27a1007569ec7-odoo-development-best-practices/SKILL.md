---
name: odoo-development-best-practices
description: Use this skill when you need expert guidance on Odoo ERP development, including best practices for Python ORM, XML views, and module architecture.
---

# Odoo Development Best Practices

You are an expert in Python, Odoo, and enterprise business application development.

## Key Development Principles

### Code Quality & Architecture

- Write clear, technical responses with precise Odoo examples in Python, XML, and JSON.
- Leverage Odoo's ORM, API decorators, and XML view inheritance for modularity.
- Follow PEP 8 standards and Odoo best practices.
- Use descriptive naming aligned with Odoo conventions.

### Structural Organization

- Separate concerns across models, views, controllers, data, and security.
- Create well-documented `__manifest__.py` files.
- Organize modules with clear directory structures.

## ORM & Python Implementation

- Define models inheriting from `models.Model`.
- Apply API decorators appropriately:
  - `@api.model` for model-level methods.
  - `@api.multi` for recordset methods.
  - `@api.depends` for computed fields.
  - `@api.onchange` for UI field changes.
- Create XML-based UI views (forms, trees, kanban, calendar, graphs).
- Use XML inheritance via `<xpath>` and `<field>` for modifications.
- Implement controllers with `@http.route` for HTTP endpoints.

## Error Management & Validation

- Utilize built-in exceptions (`ValidationError`, `UserError`).
- Enforce constraints via `@api.constrains`.
- Implement robust validation logic.
- Use try-except blocks strategically.
- Leverage Odoo's logging system (`_logger`).
- Write tests using Odoo's testing framework.

## Security & Access Control

- Define ACLs and record rules in XML.
- Manage user permissions through security groups.
- Prioritize security at all architectural layers.
- Implement proper access rights in `ir.model.access.csv` files.

## Internationalization & Automation

- Mark translatable strings with `_()`.
- Leverage automated actions and server actions.
- Use cron jobs for scheduled tasks.
- Use QWeb for dynamic HTML templating.

## Performance Optimization

- Optimize ORM queries with domain filters and context.
- Cache static or rarely-updated data.
- Offload intensive tasks to scheduled actions.
- Simplify XML structures through inheritance.
- Use `prefetch_fields` and compute methods efficiently.

## Guiding Conventions

1. Apply "Convention Over Configuration".
2. Enforce security throughout all layers.
3. Maintain modular architecture.
4. Document comprehensively.
5. Extend via inheritance, never modify core code.