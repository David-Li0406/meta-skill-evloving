# Django

**Category**: web-frameworks/backend
**Description**: The web framework for perfectionists with deadlines - High-level Python web framework with batteries included
**Homepage**: https://www.djangoproject.com

## Package Detection

### PYPI
*Core Django package*

- `Django`

### PIP
*Install via pip*

- `Django`

### POETRY
*Install via Poetry*

- `Django`

### Related Packages
- `djangorestframework`
- `django-cors-headers`
- `django-filter`
- `celery`
- `django-celery-beat`
- `django-redis`
- `psycopg2`
- `mysqlclient`
- `gunicorn`
- `django-environ`
- `django-extensions`
- `django-debug-toolbar`

## Import Detection

### Python
File extensions: .py

**Pattern**: `^from django\.`
- Django module import
- Example: `from django.db import models`

**Pattern**: `^import django`
- Direct Django import
- Example: `import django`

**Pattern**: `from django\.conf import settings`
- Django settings import
- Example: `from django.conf import settings`

**Pattern**: `from django\.urls import path`
- Django URL patterns
- Example: `from django.urls import path, include`

### Common Imports
- `django.db.models`
- `django.views`
- `django.urls`
- `django.conf.settings`

## Configuration Files

- `manage.py`
- `settings.py`
- `urls.py`
- `wsgi.py`
- `asgi.py`

## Detection Notes

- Check for Django in requirements.txt, setup.py, or pyproject.toml
- Look for manage.py file (Django management script)
- Check for django imports in Python files
- Look for settings.py or settings/ directory
- Django REST Framework is very common for APIs

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 60% (MEDIUM)
