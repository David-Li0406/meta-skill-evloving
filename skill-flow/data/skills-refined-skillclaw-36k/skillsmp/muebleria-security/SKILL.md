---
name: muebleria-security
description: >
  Authentication, authorization, and security patterns for MuebleriaIris ERP.
  Trigger: When implementing authentication, JWT, sessions, RBAC, or security features.
license: Apache-2.0
metadata:
  author: muebleria-iris
  version: "1.0"
  scope: [root]
  auto_invoke:
    - "Implementing authentication"
    - "Working with JWT tokens"
    - "Setting up authorization/RBAC"
    - "Securing API endpoints"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## When to Use

Use this skill when:

- Implementing user authentication (login/logout)
- Working with JWT tokens
- Setting up role-based access control (RBAC)
- Securing API endpoints
- Hashing passwords
- Managing user sessions

---

## Tech Stack

```
Backend: Flask + Flask-JWT-Extended + bcrypt
Frontend: JWT storage + Axios interceptors
Database: Users table + Roles table (already exists)
```

---

## Critical Patterns

### Pattern 1: Password Hashing (Backend)

```python
# backend/app/auth.py
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password: str) -> str:
    """Hash password with bcrypt"""
    return generate_password_hash(password, method='pbkrypt2:sha256')

def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash"""
    return check_password_hash(password_hash, password)

# NEVER store plain text passwords
# ALWAYS hash before saving to database
```

### Pattern 2: JWT Authentication

```python
# backend/app/__init__.py
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    
    jwt.init_app(app)
    return app

# backend/app/routes.py
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

@main.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # Find user
    user = Usuario.query.filter_by(email_us=email).first()
    
    if not user or not verify_password(password, user.password_hash):
        return jsonify({'error': 'Credenciales inválidas'}), 401
    
    # Create JWT token
    access_token = create_access_token(identity=user.id_usuarios)
    
    return jsonify({
        'token': access_token,
        'user': user.to_dict()
    }), 200

@main.route('/api/productos', methods=['POST'])
@jwt_required()  # Protected endpoint
def create_producto():
    current_user_id = get_jwt_identity()
    # ... rest of logic
```

### Pattern 3: Role-Based Access Control (RBAC)

```python
# backend/app/decorators.py
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify

def role_required(required_role: str):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = Usuario.query.get(user_id)
            
            if not user or user.rol.nombre_rol != required_role:
                return jsonify({'error': 'Acceso denegado'}), 403
            
            return f(*args, **kwargs)
        return wrapper
    return decorator

# Usage
@main.route('/api/admin/usuarios', methods=['GET'])
@role_required('Admin')
def get_usuarios():
    # Only Admin role can access
    pass
```

---

## Frontend Authentication

### Pattern 4: JWT Storage

```typescript
// src/lib/auth.ts
const TOKEN_KEY = 'muebleria_token';

export const authService = {
  setToken(token: string) {
    localStorage.setItem(TOKEN_KEY, token);
  },
  
  getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY);
  },
  
  removeToken() {
    localStorage.removeItem(TOKEN_KEY);
  },
  
  isAuthenticated(): boolean {
    return this.getToken() !== null;
  }
};
```

### Pattern 5: Protected API Calls

```typescript
// src/lib/api.ts
import { authService } from './auth';

export async function apiCall(url: string, options: RequestInit = {}) {
  const token = authService.getToken();
  
  const headers = {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` }),
    ...options.headers
  };
  
  const response = await fetch(url, { ...options, headers });
  
  if (response.status === 401) {
    // Token expired or invalid
    authService.removeToken();
    window.location.href = '/login';
  }
  
  return response;
}

// Usage
const productos = await apiCall('http://localhost:5000/api/productos')
  .then(r => r.json());
```

---

## Login Component Example

```tsx
// src/components/ui/LoginForm.tsx
"use client";
import { useState } from 'react';
import { authService } from '@/lib/auth';

export function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    try {
      const response = await fetch('http://localhost:5000/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      
      if (!response.ok) {
        const data = await response.json();
        setError(data.error || 'Error de autenticación');
        return;
      }
      
      const { token, user } = await response.json();
      authService.setToken(token);
      
      // Redirect to dashboard
      window.location.href = '/dashboard';
      
    } catch (err) {
      setError('Error de conexión');
    }
  };
  
  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto p-6">
      {error && (
        <div className="bg-red-100 text-red-700 p-3 rounded mb-4">
          {error}
        </div>
      )}
      
      <input
        type="email"
        value={email}
        onChange={e => setEmail(e.target.value)}
        placeholder="Email"
        required
        className="w-full p-2 border rounded mb-4"
      />
      
      <input
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        placeholder="Contraseña"
        required
        className="w-full p-2 border rounded mb-4"
      />
      
      <button
        type="submit"
        className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700"
      >
        Iniciar Sesión
      </button>
    </form>
  );
}
```

---

## Security Best Practices

### ALWAYS:
- Hash passwords with bcrypt/pbkrypt2
- Use HTTPS in production
- Set JWT expiration times
- Validate JWT on every protected endpoint
- Sanitize user inputs
- Use environment variables for secrets
- Implement rate limiting for login attempts
- Use secure, httpOnly cookies for tokens (alternative to localStorage)

### NEVER:
- Store passwords in plain text
- Expose JWT secret key
- Trust client-side validation only
- Store sensitive data in JWT payload
- Use GET for authentication endpoints
- Log passwords or tokens
- Hardcode credentials

---

## Environment Variables

```bash
# backend/.env
JWT_SECRET_KEY=your-super-secret-key-change-this
JWT_ACCESS_TOKEN_EXPIRES=3600  # 1 hour in seconds
SECRET_KEY=flask-secret-key-change-this
```

---

## User Registration Example

```python
@main.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate required fields
    required = ['nombre', 'apellido', 'email', 'password', 'id_rol']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Campo {field} requerido'}), 400
    
    # Check if email already exists
    if Usuario.query.filter_by(email_us=data['email']).first():
        return jsonify({'error': 'Email ya registrado'}), 409
    
    # Validate password strength
    if len(data['password']) < 8:
        return jsonify({'error': 'Contraseña debe tener mínimo 8 caracteres'}), 400
    
    # Create user
    nuevo = Usuario(
        nombre_us=data['nombre'],
        apellido_us=data['apellido'],
        email_us=data['email'],
        password_hash=hash_password(data['password']),
        id_rol=data['id_rol']
    )
    
    try:
        db.session.add(nuevo)
        db.session.commit()
        
        # Auto-login
        token = create_access_token(identity=nuevo.id_usuarios)
        
        return jsonify({
            'mensaje': 'Usuario registrado exitosamente',
            'token': token,
            'user': nuevo.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
```

---

## Protected Route (Frontend)

```astro
---
// src/pages/admin/index.astro
import Layout from '@/layouts/Layout.astro';

// Check authentication server-side
const token = Astro.cookies.get('token')?.value;

if (!token) {
  return Astro.redirect('/login');
}

// Optionally verify token with backend
---

<Layout title="Admin Dashboard">
  <h1>Panel de Administración</h1>
  <!-- Admin content -->
</Layout>
```

---

## Commands

```bash
# Install dependencies
pip install flask-jwt-extended bcrypt

# Generate secret key
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## QA Checklist

- [ ] Passwords are hashed (never plain text)
- [ ] JWT secret is in environment variables
- [ ] Protected endpoints use @jwt_required()
- [ ] RBAC implemented for admin routes
- [ ] Tokens expire after reasonable time
- [ ] Login attempts are rate-limited
- [ ] User inputs are validated and sanitized
- [ ] HTTPS used in production

---

## Resources

- **Flask-JWT-Extended**: https://flask-jwt-extended.readthedocs.io
- **OWASP Security**: https://owasp.org/www-project-top-ten/
