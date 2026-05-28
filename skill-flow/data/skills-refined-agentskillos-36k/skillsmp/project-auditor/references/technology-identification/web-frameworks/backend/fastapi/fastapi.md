# FastAPI

**Category**: web-frameworks/backend
**Description**: Modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints
**Homepage**: https://fastapi.tiangolo.com

## Package Detection

### PYPI
*Core FastAPI package*

- `fastapi`

### PIP
*Install via pip*

- `fastapi`

### Related Packages
- `uvicorn`
- `starlette`
- `pydantic`
- `sqlalchemy`
- `alembic`
- `python-multipart`
- `python-jose`
- `passlib`

## Import Detection

### Python
File extensions: .py

**Pattern**: `^from fastapi import`
- FastAPI import
- Example: `from fastapi import FastAPI, APIRouter`

**Pattern**: `^import fastapi`
- Direct FastAPI import
- Example: `import fastapi`

**Pattern**: `from pydantic import BaseModel`
- Pydantic models (used with FastAPI)
- Example: `from pydantic import BaseModel, Field`

### Common Imports
- `fastapi.FastAPI`
- `fastapi.APIRouter`
- `fastapi.Depends`
- `pydantic.BaseModel`

## Environment Variables

*Common FastAPI environment variables*

- `DATABASE_URL`
- `SECRET_KEY`
- `API_KEY`

## Configuration Files

- `main.py`
- `app.py`
- `*/routers/*.py`
- `*/api/*.py`

## Detection Notes

- FastAPI requires uvicorn or hypercorn for ASGI server
- Uses Pydantic for data validation
- Built on top of Starlette
- Check for 'from fastapi import FastAPI'
- Automatic OpenAPI documentation generation

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 60% (MEDIUM)
- **API Endpoint Detection**: 70% (MEDIUM)
