---
name: muebleria-errors
description: >
  Error handling and logging patterns for MuebleriaIris.
  Trigger: When implementing error handling, logging, or debugging features.
license: Apache-2.0
metadata:
  author: muebleria-iris
  version: "1.0"
  scope: [root]
  auto_invoke:
    - "Implementing error handling"
    - "Setting up logging"
    - "Creating error boundaries"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## When to Use

Use this skill when:

- Implementing error handling
- Setting up logging systems
- Creating React error boundaries
- Debugging issues
- Monitoring errors in production

---

## Critical Patterns

### Pattern 1: Backend Error Handling

```python
# backend/app/errors.py
from flask import jsonify
from werkzeug.exceptions import HTTPException
import logging

logger = logging.getLogger(__name__)

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        logger.warning(f'404: {request.url}')
        return jsonify({'error': 'Recurso no encontrado'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f'500: {str(error)}', exc_info=True)
        db.session.rollback()
        return jsonify({'error': 'Error interno del servidor'}), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        # Log all unhandled exceptions
        logger.error(f'Unhandled exception: {str(error)}', exc_info=True)
        
        if isinstance(error, HTTPException):
            return jsonify({'error': error.description}), error.code
        
        return jsonify({'error': 'Error inesperado'}), 500

# backend/app/__init__.py
from .errors import register_error_handlers

def create_app():
    app = Flask(__name__)
    register_error_handlers(app)
    return app
```

### Pattern 2: Logging Configuration

```python
# backend/app/logging_config.py
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # File handler
    file_handler = RotatingFileHandler(
        'logs/muebleria.log',
        maxBytes=10240000,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if app.debug else logging.INFO)
    app.logger.addHandler(console_handler)
    
    app.logger.setLevel(logging.INFO)
    app.logger.info('MuebleriaIris startup')
```

### Pattern 3: Try-Except Patterns

```python
# backend/app/routes.py
@main.route('/api/productos', methods=['POST'])
def create_producto():
    try:
        data = request.get_json()
        
        # Validation
        if not data.get('nombre'):
            return jsonify({'error': 'Nombre requerido'}), 400
        
        # Business logic
        nuevo = Producto(**data)
        db.session.add(nuevo)
        db.session.commit()
        
        app.logger.info(f'Producto creado: {nuevo.id_producto}')
        return jsonify({'producto': nuevo.to_dict()}), 201
        
    except ValueError as e:
        # Expected errors (validation)
        app.logger.warning(f'Validation error: {str(e)}')
        return jsonify({'error': str(e)}), 400
        
    except KeyError as e:
        # Missing required field
        app.logger.warning(f'Missing field: {str(e)}')
        return jsonify({'error': f'Campo requerido: {str(e)}'}), 400
        
    except Exception as e:
        # Unexpected errors
        app.logger.error(f'Error creating producto: {str(e)}', exc_info=True)
        db.session.rollback()
        return jsonify({'error': 'Error al crear producto'}), 500
```

---

## Frontend Error Handling

### Pattern 4: Error Boundary (React)

```tsx
// src/components/ErrorBoundary.tsx
import { Component, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }
  
  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }
  
  componentDidCatch(error: Error, errorInfo: any) {
    console.error('ErrorBoundary caught:', error, errorInfo);
    // Send to logging service
  }
  
  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="p-4 bg-red-100 text-red-700 rounded">
          <h2 className="font-bold">Algo salió mal</h2>
          <p>{this.state.error?.message}</p>
          <button
            onClick={() => this.setState({ hasError: false })}
            className="mt-2 px-4 py-2 bg-red-600 text-white rounded"
          >
            Reintentar
          </button>
        </div>
      );
    }
    
    return this.props.children;
  }
}

// Usage
<ErrorBoundary>
  <ProductList />
</ErrorBoundary>
```

### Pattern 5: API Error Handling

```typescript
// src/lib/apiClient.ts
export class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public data?: any
  ) {
    super(message);
    this.name = 'APIError';
  }
}

export async function apiRequest<T>(
  url: string,
  options?: RequestInit
): Promise<T> {
  try {
    const response = await fetch(url, options);
    
    if (!response.ok) {
      const data = await response.json().catch(() => ({}));
      throw new APIError(
        data.error || 'Error en la petición',
        response.status,
        data
      );
    }
    
    return await response.json();
    
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    
    // Network error
    throw new APIError('Error de conexión', 0);
  }
}

// Usage
try {
  const productos = await apiRequest<Producto[]>('http://localhost:5000/api/productos');
} catch (error) {
  if (error instanceof APIError) {
    if (error.status === 404) {
      console.log('No encontrado');
    } else if (error.status === 500) {
      console.log('Error del servidor');
    } else {
      console.log('Error de red');
    }
  }
}
```

---

## Logging Patterns

```python
# backend/app/routes.py
import logging

logger = logging.getLogger(__name__)

# Log levels
logger.debug('Debugging info')     # Development only
logger.info('User logged in')      # Important events
logger.warning('Stock bajo')       # Warnings
logger.error('DB error', exc_info=True)  # Errors
logger.critical('System down')     # Critical errors

# Structured logging
logger.info(f'Order created: {order_id}, customer: {customer_id}, total: {total}')

# Log with context
try:
    # ...
except Exception as e:
    logger.error(f'Failed to process order {order_id}', exc_info=True)
```

---

## User-Friendly Error Messages

```python
# ❌ DON'T: Expose internal errors
return jsonify({'error': str(e)}), 500  # Shows stack trace

# ✅ DO: Generic messages for unexpected errors
return jsonify({'error': 'Error al procesar la solicitud'}), 500

# ✅ DO: Specific messages for expected errors
if stock < cantidad:
    return jsonify({'error': 'Stock insuficiente. Disponible: ' + str(stock)}), 400
```

---

## Toast Notifications (Frontend)

```tsx
// src/lib/toast.ts
type ToastType = 'success' | 'error' | 'warning' | 'info';

export const toast = {
  success(message: string) {
    // Show success toast
    console.log('✅', message);
  },
  
  error(message: string) {
    // Show error toast
    console.error('❌', message);
  },
  
  warning(message: string) {
    console.warn('⚠️', message);
  }
};

// Usage
try {
  await createProduct(data);
  toast.success('Producto creado exitosamente');
} catch (error) {
  toast.error(error.message || 'Error al crear producto');
}
```

---

## Best Practices

### DO:
- Log all errors with context
- Use appropriate log levels
- Sanitize error messages for users
- Implement error boundaries
- Handle network errors
- Rollback DB transactions on error
- Monitor production errors

### DON'T:
- Expose stack traces to users
- Log sensitive data (passwords, tokens)
- Ignore exceptions
- Show technical errors to users
- Let app crash without boundaries
- Forget to rollback DB on error

---

## Commands

```bash
# View logs
tail -f backend/logs/muebleria.log

# Search errors
grep "ERROR" backend/logs/muebleria.log

# Monitor in real-time
watch -n 1 'tail -20 backend/logs/muebleria.log'
```

---

## QA Checklist

- [ ] All API endpoints have try-except
- [ ] DB transactions rollback on error
- [ ] User-friendly error messages
- [ ] Errors logged with context
- [ ] React error boundaries in place
- [ ] Network errors handled
- [ ] No sensitive data in logs
- [ ] Log rotation configured

---

## Resources

- **Python Logging**: https://docs.python.org/3/library/logging.html
- **React Error Boundaries**: https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary
