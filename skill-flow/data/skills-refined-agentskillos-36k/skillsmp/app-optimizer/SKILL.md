---
name: app-optimizer
description: Optimizador integral de aplicaciones - combina performance, seguridad y mejores prácticas
---

# App Optimizer Skill

Skill especializado en optimización integral de aplicaciones web full-stack. Combina análisis de performance, seguridad y arquitectura para maximizar la calidad del código.

## Capacidades Principales

### 1. Análisis de Performance

#### Backend (Python/FastAPI)
```python
# Detección de N+1 Queries
PROBLEMATIC_PATTERNS = {
    'n_plus_1': [
        r'for\s+\w+\s+in\s+\w+:.*execute\(',   # Query en loop
        r'for\s+\w+\s+in\s+\w+:.*\.get\(',     # ORM get en loop
    ],
    'full_table_scan': [
        r'SELECT\s+\*\s+FROM',                  # SELECT * sin filtro
        r'execute\(["\']SELECT.*without.*WHERE' # Query sin WHERE
    ],
    'missing_index': [
        r'WHERE\s+\w+\s*=',                     # Columnas en WHERE sin índice
        r'ORDER BY\s+\w+',                      # Columnas en ORDER BY
    ]
}
```

#### Frontend (JavaScript)
```javascript
// Patrones de performance a detectar
const PERFORMANCE_ISSUES = {
    // DOM
    'layout_thrashing': /\.offset|\.client|\.scroll|getBoundingClientRect/,
    'forced_reflow': /\.style\.\w+\s*=.*\.offset/,

    // Memory
    'event_listener_leak': /addEventListener(?!.*removeEventListener)/,
    'closure_leak': /setInterval|setTimeout(?!.*clear)/,

    // Rendering
    'expensive_css': /box-shadow|filter|backdrop-filter|transform/,
    'large_paint': /position:\s*fixed|background-attachment:\s*fixed/
};
```

### 2. Optimizaciones Automáticas

#### Database Queries
```python
# ANTES (N+1)
for emp in employees:
    details = db.query(Details).filter_by(emp_id=emp.id).first()

# DESPUÉS (JOIN optimizado)
employees_with_details = db.query(Employee, Details)\
    .join(Details)\
    .all()
```

#### Bundle Size Reduction
```javascript
// Lazy loading de módulos
const ChartManager = await import('./modules/chart-manager.js');

// Tree shaking - importar solo lo necesario
import { debounce, throttle } from './utils.js';
// NO: import * as Utils from './utils.js';
```

#### Image Optimization
```html
<!-- Lazy loading nativo -->
<img src="image.jpg" loading="lazy" decoding="async">

<!-- Responsive images -->
<picture>
  <source srcset="image.webp" type="image/webp">
  <source srcset="image.jpg" type="image/jpeg">
  <img src="image.jpg" alt="Description">
</picture>
```

### 3. Análisis de Seguridad

#### OWASP Top 10 Detection
```python
SECURITY_PATTERNS = {
    'A01_BROKEN_ACCESS_CONTROL': {
        'missing_auth': r'@app\.(get|post|put|delete)\([^)]+\)\s*\n\s*async\s+def\s+\w+\([^)]*\):(?!.*Depends)',
        'hardcoded_secret': r'(password|secret|api_key)\s*=\s*["\'][^"\']+["\']',
    },
    'A03_INJECTION': {
        'sql_injection': r'execute\(f["\']|format\(.*\)|%\s*\(',
        'command_injection': r'os\.system\(|subprocess\.(call|run|Popen)\([^)]*\+',
        'xss': r'innerHTML\s*=|document\.write\(',
    },
    'A07_AUTH_FAILURES': {
        'weak_jwt': r'algorithm\s*=\s*["\']none["\']',
        'no_expiration': r'create.*token(?!.*exp)',
    }
}
```

#### Secret Scanning
```python
SECRET_PATTERNS = {
    'api_key': r'(?i)(api[_-]?key|apikey)\s*[:=]\s*["\']?[\w-]{20,}',
    'jwt_secret': r'(?i)(jwt[_-]?secret|secret[_-]?key)\s*[:=]\s*["\'][^"\']{10,}',
    'database_url': r'(?i)(database_url|db_url)\s*[:=]\s*["\']?[a-z]+:\/\/[^"\']+',
    'aws_key': r'AKIA[0-9A-Z]{16}',
    'private_key': r'-----BEGIN (RSA |EC )?PRIVATE KEY-----',
}
```

### 4. Métricas y Benchmarks

#### Core Web Vitals Targets
```javascript
const WEB_VITALS_TARGETS = {
    LCP: 2500,  // Largest Contentful Paint < 2.5s
    FID: 100,   // First Input Delay < 100ms
    CLS: 0.1,   // Cumulative Layout Shift < 0.1
    TTFB: 600,  // Time to First Byte < 600ms
    FCP: 1800,  // First Contentful Paint < 1.8s
};
```

#### Database Query Benchmarks
```python
QUERY_BENCHMARKS = {
    'simple_select': 10,    # < 10ms
    'join_2_tables': 50,    # < 50ms
    'join_3_tables': 100,   # < 100ms
    'aggregate': 200,       # < 200ms
    'full_text_search': 100 # < 100ms
}
```

## Comandos de Optimización

### Performance Audit
```bash
# Backend profiling
python -m cProfile -o profile.stats main.py
python -m pstats profile.stats

# Frontend bundle analysis
npx webpack-bundle-analyzer stats.json

# Database query analysis
sqlite3 yukyu.db "EXPLAIN QUERY PLAN SELECT ..."
```

### Security Audit
```bash
# Python security scan
pip install bandit
bandit -r . -f json -o security_report.json

# Dependency vulnerabilities
pip-audit
npm audit

# Secrets scanning
git secrets --scan
```

## Checklist de Optimización

### Pre-Deploy
- [ ] No hay console.log en producción
- [ ] Imágenes optimizadas (WebP, lazy loading)
- [ ] CSS/JS minificados
- [ ] Gzip/Brotli habilitado
- [ ] Cache headers configurados
- [ ] Security headers (CSP, HSTS, X-Frame-Options)

### Database
- [ ] Índices en columnas WHERE/ORDER BY
- [ ] No hay SELECT *
- [ ] Queries paginadas
- [ ] Connection pooling configurado
- [ ] Backups automáticos

### API
- [ ] Rate limiting activo
- [ ] Autenticación en endpoints sensibles
- [ ] Validación de input (Pydantic)
- [ ] Error handling sin leak de info
- [ ] CORS restringido

### Frontend
- [ ] Virtual scrolling para listas grandes
- [ ] Debounce en inputs
- [ ] Lazy loading de módulos
- [ ] Service Worker para offline
- [ ] Accesibilidad WCAG AA

## Integración con YuKyuDATA

### Optimizaciones Específicas
```python
# 1. Paginación server-side para /api/employees
@app.get("/api/v1/employees")
async def get_employees_paginated(
    year: int = None,
    page: int = 1,
    page_size: int = 50,
    sort_by: str = "name"
):
    offset = (page - 1) * page_size
    query = "SELECT * FROM employees WHERE year = ? LIMIT ? OFFSET ?"
    return {"data": results, "total": total, "page": page}

# 2. Cache de datos frecuentes
from services.caching import cache

@cache(ttl=300)  # 5 minutos
def get_yearly_stats(year: int):
    return calculate_stats(year)

# 3. Batch queries para dashboard
async def get_dashboard_data(year: int):
    # Una sola query con JOINs en lugar de múltiples
    query = """
        SELECT
            e.*, g.dispatch_name, u.contract_business
        FROM employees e
        LEFT JOIN genzai g ON e.employee_num = g.employee_num
        LEFT JOIN ukeoi u ON e.employee_num = u.employee_num
        WHERE e.year = ?
    """
```

## Output del Análisis

```json
{
    "performance": {
        "score": 85,
        "issues": [
            {"type": "N+1", "file": "main.py", "line": 234, "severity": "HIGH"},
            {"type": "BUNDLE_SIZE", "file": "app.js", "size_kb": 450, "severity": "MEDIUM"}
        ],
        "recommendations": [
            "Implementar paginación server-side",
            "Lazy load chart libraries"
        ]
    },
    "security": {
        "score": 72,
        "vulnerabilities": [
            {"type": "MISSING_AUTH", "endpoint": "/api/employees", "severity": "CRITICAL"},
            {"type": "CORS_PERMISSIVE", "severity": "MEDIUM"}
        ],
        "secrets_found": 0
    },
    "overall_grade": "B"
}
```

---

**Principio Guía:** "Optimiza lo que importa. Mide antes de optimizar. Seguridad nunca es opcional."
