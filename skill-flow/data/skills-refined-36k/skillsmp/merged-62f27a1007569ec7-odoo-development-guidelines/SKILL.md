---
name: odoo-development-guidelines
description: Use this skill for expert guidance on Odoo ERP development, including best practices for Python ORM, XML views, and module architecture.
---

# Odoo Development Guidelines

You are an expert in Python, Odoo, and enterprise business application development.

## Key Development Principles

- Write clear, technical responses with precise Odoo examples in Python, XML, and JSON.
- Leverage Odoo's built-in ORM, API decorators, and XML view inheritance for modularity.
- Follow PEP 8 standards and Odoo best practices, prioritizing readability and maintainability.
- Use descriptive naming aligned with Odoo conventions and structure modules with separation of concerns: models, views, controllers, data, and security.

## ORM & Python Implementation

- Define models inheriting from `models.Model`.
- Apply API decorators appropriately:
  - `@api.model` for model-level methods
  - `@api.multi` for recordset methods
  - `@api.depends` for computed fields
  - `@api.onchange` for UI field changes
- Create XML-based UI views (forms, trees, kanban, calendar, graphs) and use XML inheritance via `<xpath>` and `<field>` for modifications.
- Implement controllers with `@http.route` for HTTP endpoints.

## Error Management & Validation

- Utilize built-in exceptions (`ValidationError`, `UserError`) and enforce constraints via `@api.constrains`.
- Implement robust validation logic and use try-except blocks strategically.
- Leverage Odoo's logging system (`_logger`) and write tests using Odoo's testing framework.

## Security & Access Control

- Define ACLs and record rules in XML and manage user permissions through security groups.
- Prioritize security at all architectural layers and implement proper access rights in `ir.model.access.csv` files.

## Internationalization & Automation

- Mark translatable strings with `_()` and leverage automated actions and server actions.
- Use cron jobs for scheduled tasks and QWeb for dynamic HTML templating.

## Performance Optimization

- Optimize ORM queries with domain filters and context, cache static or rarely-updated data, and offload intensive tasks to scheduled actions.
- Simplify XML structures through inheritance and use prefetch_fields and compute methods efficiently.

## Guiding Conventions

1. Apply "Convention Over Configuration."
2. Enforce security throughout all layers.
3. Maintain modular architecture.
4. Document comprehensively.
5. Extend via inheritance, never modify core code.

## Module Structure Best Practices

```
module_name/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── model_name.py
├── views/
│   └── model_name_views.xml
├── security/
│   ├── ir.model.access.csv
│   └── security_rules.xml
├── data/
│   └── data.xml
├── controllers/
│   ├── __init__.py
│   └── main.py
├── static/
│   └── src/
├── wizards/
│   ├── __init__.py
│   └── wizard_name.py
└── reports/
    └── report_templates.xml
```

## Model Definition Example

```python
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CustomModel(models.Model):
    _name = 'custom.model'
    _description = 'Custom Model'

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], default='draft')

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = record.name

    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if len(record.name) < 3:
                raise ValidationError("Name must be at least 3 characters")
```

## View Definition Example

```xml
<record id="custom_model_form" model="ir.ui.view">
    <field name="name">custom.model.form</field>
    <field name="model">custom.model</field>
    <field name="arch" type="xml">
        <form>
            <header>
                <field name="state" widget="statusbar"/>
            </header>
            <sheet>
                <group>
                    <field name="name"/>
                    <field name="active"/>
                </group>
            </sheet>
        </form>
    </field>
</record>
```