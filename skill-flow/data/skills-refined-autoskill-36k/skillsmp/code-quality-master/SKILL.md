---
name: code-quality-master
description: Maestro de calidad de código - refactoring, code smells, arquitectura limpia y mejores prácticas
---

# Code Quality Master Skill

Skill especializado en mantener y mejorar la calidad del código a través de detección de code smells, refactoring automático, y aplicación de principios de arquitectura limpia.

## Principios de Calidad

### SOLID Principles
```
S - Single Responsibility: Una clase, una razón para cambiar
O - Open/Closed: Abierto para extensión, cerrado para modificación
L - Liskov Substitution: Subtipos sustituibles por tipos base
I - Interface Segregation: Interfaces específicas > interfaces grandes
D - Dependency Inversion: Depender de abstracciones, no de concretos
```

### Clean Code Guidelines
```python
# 1. Nombres significativos
# MALO
def calc(d, u):
    return (u / d) * 100

# BUENO
def calculate_usage_rate(granted_days: float, used_days: float) -> float:
    return (used_days / granted_days) * 100

# 2. Funciones pequeñas (< 20 líneas)
# 3. Un nivel de abstracción por función
# 4. Comentarios solo cuando el código no puede explicarse
# 5. Manejo de errores separado de lógica de negocio
```

## Detección de Code Smells

### Catálogo de Smells

#### 1. Long Method (> 50 líneas)
```python
# Detección
def detect_long_methods(file_content: str, threshold: int = 50) -> list:
    """Detecta métodos con más de N líneas."""
    issues = []
    for func in extract_functions(file_content):
        if func['line_count'] > threshold:
            issues.append({
                'type': 'LONG_METHOD',
                'name': func['name'],
                'lines': func['line_count'],
                'suggestion': 'Extract smaller methods with single responsibility'
            })
    return issues

# Refactoring: Extract Method
# ANTES
def process_employees(employees):
    # 100 líneas de código
    pass

# DESPUÉS
def process_employees(employees):
    validated = validate_employees(employees)
    enriched = enrich_with_metadata(validated)
    return save_to_database(enriched)
```

#### 2. God Class (> 20 métodos o > 500 líneas)
```python
# ANTES: App class con 50+ métodos
class App:
    def init_data(self): ...
    def fetch_employees(self): ...
    def render_table(self): ...
    def render_charts(self): ...
    def handle_click(self): ...
    # ... 45 métodos más

# DESPUÉS: Separar en clases especializadas
class DataService:
    def fetch_employees(self): ...
    def sync_data(self): ...

class UIManager:
    def render_table(self): ...
    def render_charts(self): ...

class EventHandler:
    def handle_click(self): ...
```

#### 3. Feature Envy
```python
# MALO: Método que usa más datos de otra clase
def calculate_employee_stats(employee):
    return {
        'usage_rate': (employee.used / employee.granted) * 100,
        'is_compliant': employee.used >= 5,
        'days_remaining': employee.granted - employee.used
    }

# BUENO: Mover lógica a la clase Employee
class Employee:
    def get_usage_rate(self) -> float:
        return (self.used / self.granted) * 100

    def is_compliant(self) -> bool:
        return self.used >= 5

    @property
    def days_remaining(self) -> float:
        return self.granted - self.used
```

#### 4. Data Clumps
```python
# MALO: Grupos de datos que siempre van juntos
def create_employee(name, employee_num, hire_date, department, factory):
    ...

def update_employee(employee_id, name, employee_num, hire_date, department, factory):
    ...

# BUENO: Agrupar en objetos
@dataclass
class EmployeeInfo:
    name: str
    employee_num: str
    hire_date: date
    department: str
    factory: str

def create_employee(info: EmployeeInfo):
    ...
```

#### 5. Primitive Obsession
```python
# MALO: Usar primitivos para conceptos de dominio
def process_leave_request(employee_num: str, days: float, leave_type: str):
    if leave_type not in ['full', 'half_am', 'half_pm', 'hourly']:
        raise ValueError("Invalid leave type")

# BUENO: Usar tipos específicos
from enum import Enum

class LeaveType(Enum):
    FULL = 'full'
    HALF_AM = 'half_am'
    HALF_PM = 'half_pm'
    HOURLY = 'hourly'

@dataclass
class LeaveRequest:
    employee_num: str
    days: float
    leave_type: LeaveType
```

### Matriz de Severidad

| Smell | Severidad | Impacto en Mantenibilidad |
|-------|-----------|---------------------------|
| Long Method | 🟠 MEDIUM | -20% readability |
| God Class | 🔴 HIGH | -40% maintainability |
| Feature Envy | 🟡 LOW | -10% cohesion |
| Data Clumps | 🟠 MEDIUM | -15% clarity |
| Primitive Obsession | 🟡 LOW | -10% type safety |
| Duplicate Code | 🔴 HIGH | -50% DRY |
| Dead Code | 🟠 MEDIUM | -25% clarity |
| Magic Numbers | 🟡 LOW | -15% clarity |

## Refactoring Patterns

### 1. Extract Class
```python
# ANTES
class Employee:
    def __init__(self):
        self.name = ""
        self.birth_date = ""
        self.address = ""
        self.city = ""
        self.postal_code = ""
        self.hire_date = ""
        self.granted_days = 0
        self.used_days = 0

    def get_full_address(self):
        return f"{self.address}, {self.city} {self.postal_code}"

    def get_balance(self):
        return self.granted_days - self.used_days

# DESPUÉS
@dataclass
class Address:
    street: str
    city: str
    postal_code: str

    def __str__(self):
        return f"{self.street}, {self.city} {self.postal_code}"

@dataclass
class VacationBalance:
    granted: float
    used: float

    @property
    def remaining(self) -> float:
        return self.granted - self.used

@dataclass
class Employee:
    name: str
    birth_date: date
    hire_date: date
    address: Address
    vacation: VacationBalance
```

### 2. Replace Conditional with Polymorphism
```python
# ANTES
def calculate_days(employee_type: str, seniority: float) -> int:
    if employee_type == 'fulltime':
        return get_fulltime_days(seniority)
    elif employee_type == 'parttime':
        return get_parttime_days(seniority)
    elif employee_type == 'contract':
        return get_contract_days(seniority)

# DESPUÉS
from abc import ABC, abstractmethod

class EmployeeType(ABC):
    @abstractmethod
    def calculate_days(self, seniority: float) -> int:
        pass

class FullTimeEmployee(EmployeeType):
    def calculate_days(self, seniority: float) -> int:
        return get_fulltime_days(seniority)

class PartTimeEmployee(EmployeeType):
    def calculate_days(self, seniority: float) -> int:
        return get_parttime_days(seniority)
```

### 3. Introduce Parameter Object
```python
# ANTES
def search_employees(
    name: str = None,
    department: str = None,
    factory: str = None,
    year: int = None,
    min_balance: float = None,
    max_balance: float = None,
    is_compliant: bool = None,
    sort_by: str = None,
    sort_order: str = None,
    page: int = 1,
    page_size: int = 50
):
    pass

# DESPUÉS
@dataclass
class EmployeeSearchCriteria:
    name: str = None
    department: str = None
    factory: str = None
    year: int = None
    min_balance: float = None
    max_balance: float = None
    is_compliant: bool = None

@dataclass
class PaginationOptions:
    page: int = 1
    page_size: int = 50
    sort_by: str = None
    sort_order: str = 'asc'

def search_employees(
    criteria: EmployeeSearchCriteria,
    pagination: PaginationOptions = None
):
    pass
```

## Métricas de Calidad

### Complejidad Ciclomática
```python
def calculate_cyclomatic_complexity(func_ast) -> int:
    """
    CC = 1 + número de puntos de decisión

    Puntos de decisión:
    - if, elif, else
    - for, while
    - try, except
    - and, or
    - case (match)
    """
    complexity = 1
    for node in ast.walk(func_ast):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
            complexity += 1
        elif isinstance(node, ast.BoolOp):
            complexity += len(node.values) - 1
    return complexity

# Thresholds
COMPLEXITY_THRESHOLDS = {
    'GOOD': (1, 10),
    'MODERATE': (11, 20),
    'HIGH': (21, 50),
    'VERY_HIGH': (51, float('inf'))
}
```

### Maintainability Index
```python
def calculate_maintainability_index(
    halstead_volume: float,
    cyclomatic_complexity: int,
    loc: int
) -> float:
    """
    MI = 171 - 5.2 * ln(V) - 0.23 * G - 16.2 * ln(LOC)

    Where:
    - V = Halstead Volume
    - G = Cyclomatic Complexity
    - LOC = Lines of Code

    Score interpretation:
    - 85+: Highly maintainable
    - 65-84: Moderately maintainable
    - <65: Difficult to maintain
    """
    import math
    mi = 171 - 5.2 * math.log(halstead_volume) \
             - 0.23 * cyclomatic_complexity \
             - 16.2 * math.log(loc)
    return max(0, min(100, mi))
```

### Code Coverage Quality
```python
COVERAGE_QUALITY_RULES = {
    'line_coverage': {
        'min': 70,
        'good': 80,
        'excellent': 90
    },
    'branch_coverage': {
        'min': 60,
        'good': 75,
        'excellent': 85
    },
    'function_coverage': {
        'min': 80,
        'good': 90,
        'excellent': 95
    }
}
```

## Análisis Automático

### Output de Análisis
```json
{
    "file": "main.py",
    "metrics": {
        "loc": 5058,
        "functions": 145,
        "classes": 8,
        "avg_complexity": 4.2,
        "max_complexity": 32,
        "maintainability_index": 72
    },
    "code_smells": [
        {
            "type": "LONG_METHOD",
            "location": "main.py:234-350",
            "name": "sync_all_data",
            "lines": 116,
            "suggestion": "Extract into smaller methods: parse_excel, validate_data, save_to_db"
        },
        {
            "type": "DUPLICATE_CODE",
            "locations": ["main.py:400-420", "main.py:500-520"],
            "similarity": 0.92,
            "suggestion": "Extract common logic to shared function"
        }
    ],
    "refactoring_opportunities": [
        {
            "pattern": "EXTRACT_METHOD",
            "function": "get_employees_by_type",
            "benefit": "Reduce complexity from 15 to 5",
            "risk": "LOW"
        }
    ],
    "quality_score": "B",
    "recommendations": [
        "Split main.py into multiple modules (routes/, services/)",
        "Add type hints to 45 functions missing them",
        "Remove 12 unused imports"
    ]
}
```

## Integración con YuKyuDATA

### Refactorings Prioritarios

#### 1. Modularizar main.py
```python
# Estructura propuesta
app/
├── main.py              # Solo setup de FastAPI
├── routes/
│   ├── employees.py     # Endpoints de empleados
│   ├── leave_requests.py # Endpoints de solicitudes
│   ├── compliance.py    # Endpoints de compliance
│   └── analytics.py     # Endpoints de analytics
├── services/
│   ├── employee_service.py
│   ├── leave_service.py
│   └── compliance_service.py
├── models/
│   ├── employee.py
│   ├── leave_request.py
│   └── compliance.py
└── utils/
    ├── validators.py
    └── formatters.py
```

#### 2. Aplicar Domain Objects
```python
# Antes: Diccionarios por todos lados
employee = {
    'employee_num': '001',
    'name': 'Tanaka',
    'granted': 10,
    'used': 5,
    'year': 2025
}

# Después: Domain models
from pydantic import BaseModel

class Employee(BaseModel):
    employee_num: str
    name: str
    granted: float
    used: float
    year: int

    @property
    def balance(self) -> float:
        return self.granted - self.used

    @property
    def usage_rate(self) -> float:
        if self.granted == 0:
            return 0
        return (self.used / self.granted) * 100

    def is_compliant_with_5day_rule(self) -> bool:
        return self.granted < 10 or self.used >= 5
```

## Comandos de Análisis

```bash
# Python
# Complexity analysis
pip install radon
radon cc main.py -a -s  # Cyclomatic complexity
radon mi main.py -s     # Maintainability index
radon hal main.py       # Halstead metrics

# Linting
pip install pylint flake8 mypy
pylint main.py --output-format=json
flake8 main.py --format=json
mypy main.py --json

# JavaScript
# ESLint with complexity
npx eslint static/js/app.js --format=json

# Code duplication
pip install pylint
pylint --disable=all --enable=duplicate-code *.py

# Dead code
pip install vulture
vulture . --min-confidence 80
```

---

**Principio Guía:** "El código limpio es código que otros desarrolladores pueden leer, entender y modificar con confianza."
