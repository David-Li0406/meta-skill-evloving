# Flask

**Category**: web-frameworks/backend
**Description**: Lightweight WSGI web application framework - Python microframework for building web applications
**Homepage**: https://flask.palletsprojects.com

## Package Detection

### PYPI
*Core Flask package*

- `Flask`

### PIP
*Install via pip*

- `Flask`

### Related Packages
- `flask-restful`
- `flask-sqlalchemy`
- `flask-migrate`
- `flask-login`
- `flask-wtf`
- `flask-cors`
- `gunicorn`
- `werkzeug`

## Import Detection

### Python
File extensions: .py

**Pattern**: `^import\s+Flask`
- Direct import
- Example: `import Flask`

**Pattern**: `^from\s+Flask\s+import`
- From import
- Example: `from Flask import something`

## Detection Notes

- Look for Flask in requirements.txt
- Check for 'from flask import Flask' in Python files
- app.py or main.py typically contains Flask app
- Much simpler structure than Django

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 85% (HIGH)
- **Environment Variable Detection**: 60% (MEDIUM)
