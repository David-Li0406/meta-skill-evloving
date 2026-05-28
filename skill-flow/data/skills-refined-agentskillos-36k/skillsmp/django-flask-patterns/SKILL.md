---
name: django-flask-patterns
description: Models/views/templates (Django), blueprints (Flask), migrations.
---

# Django / Flask Patterns

## When to use this skill
- Maintaining Django or Flask applications.
- Writing migrations.
- Working with templates (Jinja2/DTL).

## 1. Django
- **Models**: Fat models, thin views. Put business logic in Model methods or Managers.
- **CBV vs FBV**: Context dependent, but stick to one style per project. Function-Based Views often cleaner for simple logic.
- **ORM**: Use `select_related` (FK) and `prefetch_related` (M2M) to avoid N+1 queries.

## 2. Flask
- **Blueprints**: Always use Blueprints to organize routes.
- **Application Factory**: Use the `create_app()` pattern for better testing and config management.
- **Extensions**: Initialize extensions (`db.init_app(app)`) inside the factory.
