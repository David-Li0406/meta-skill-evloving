---
name: full-stack-architect
description: Arquitecto full-stack - diseño de sistemas, decisiones de arquitectura, patrones y escalabilidad
---

# Full Stack Architect Skill

Skill especializado en diseño de arquitectura de sistemas, toma de decisiones técnicas, patrones de diseño y estrategias de escalabilidad para aplicaciones full-stack.

## Principios Arquitectónicos

### 1. Separation of Concerns
```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  UI Components, Views, Templates, Client-side Logic         │
└─────────────────────────────────────────────────────────────┘
                              ↓ HTTP/WebSocket
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│  Controllers, Routes, API Endpoints, Request/Response        │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    DOMAIN/SERVICE LAYER                      │
│  Business Logic, Use Cases, Domain Models, Validations       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    DATA ACCESS LAYER                         │
│  Repositories, DAOs, ORM, Query Builders                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE LAYER                      │
│  Database, Cache, Message Queue, External Services           │
└─────────────────────────────────────────────────────────────┘
```

### 2. Domain-Driven Design (DDD)
```python
# Bounded Contexts para YuKyuDATA
BOUNDED_CONTEXTS = {
    'Vacation Management': {
        'aggregates': ['Employee', 'LeaveRequest', 'VacationBalance'],
        'services': ['ComplianceService', 'BalanceCalculator'],
        'events': ['LeaveApproved', 'BalanceUpdated', 'ComplianceAlertRaised']
    },
    'Employee Registry': {
        'aggregates': ['GenzaiEmployee', 'UkeoiEmployee', 'StaffMember'],
        'services': ['EmployeeSync', 'ExcelParser'],
        'events': ['EmployeeCreated', 'EmployeeUpdated']
    },
    'Analytics': {
        'aggregates': ['UsageReport', 'TrendAnalysis'],
        'services': ['ReportGenerator', 'DashboardService'],
        'events': ['ReportGenerated']
    }
}
```

### 3. CQRS (Command Query Responsibility Segregation)
```python
# Commands (Write)
class CreateLeaveRequestCommand:
    employee_num: str
    start_date: date
    end_date: date
    leave_type: LeaveType

class ApproveLeaveRequestCommand:
    request_id: int
    approved_by: str

# Queries (Read)
class GetEmployeeVacationBalanceQuery:
    employee_num: str
    year: int

class GetComplianceReportQuery:
    year: int
    department: str = None

# Separate handlers
class CommandHandler:
    def handle_create_leave_request(self, cmd: CreateLeaveRequestCommand):
        # Validate, create, emit event
        pass

class QueryHandler:
    def handle_get_balance(self, query: GetEmployeeVacationBalanceQuery):
        # Read from optimized read model
        pass
```

## Patrones de Arquitectura

### 1. Repository Pattern
```python
from abc import ABC, abstractmethod
from typing import List, Optional

class EmployeeRepository(ABC):
    """Abstract repository for employee data access."""

    @abstractmethod
    def get_by_id(self, employee_num: str, year: int) -> Optional[Employee]:
        pass

    @abstractmethod
    def get_all(self, year: int = None) -> List[Employee]:
        pass

    @abstractmethod
    def save(self, employee: Employee) -> None:
        pass

    @abstractmethod
    def delete(self, employee_num: str, year: int) -> bool:
        pass

class SQLiteEmployeeRepository(EmployeeRepository):
    """SQLite implementation of EmployeeRepository."""

    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_by_id(self, employee_num: str, year: int) -> Optional[Employee]:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM employees WHERE employee_num = ? AND year = ?",
                (employee_num, year)
            )
            row = cursor.fetchone()
            return Employee(**dict(row)) if row else None
```

### 2. Service Layer Pattern
```python
class LeaveRequestService:
    """Service for managing leave requests."""

    def __init__(
        self,
        leave_repo: LeaveRequestRepository,
        employee_repo: EmployeeRepository,
        balance_calculator: BalanceCalculator,
        event_bus: EventBus
    ):
        self.leave_repo = leave_repo
        self.employee_repo = employee_repo
        self.balance_calculator = balance_calculator
        self.event_bus = event_bus

    def create_request(self, cmd: CreateLeaveRequestCommand) -> LeaveRequest:
        # 1. Validate employee exists
        employee = self.employee_repo.get_by_id(cmd.employee_num, get_current_year())
        if not employee:
            raise EmployeeNotFoundError(cmd.employee_num)

        # 2. Check balance
        if not self.balance_calculator.has_sufficient_balance(employee, cmd.days):
            raise InsufficientBalanceError(employee.balance, cmd.days)

        # 3. Create request
        request = LeaveRequest(
            employee_num=cmd.employee_num,
            start_date=cmd.start_date,
            end_date=cmd.end_date,
            leave_type=cmd.leave_type,
            status=LeaveStatus.PENDING
        )

        # 4. Save
        self.leave_repo.save(request)

        # 5. Emit event
        self.event_bus.publish(LeaveRequestCreated(request))

        return request
```

### 3. Event-Driven Architecture
```python
from typing import Callable, Dict, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DomainEvent:
    event_id: str
    timestamp: datetime
    aggregate_id: str

@dataclass
class LeaveApprovedEvent(DomainEvent):
    request_id: int
    employee_num: str
    days_approved: float
    approved_by: str

class EventBus:
    def __init__(self):
        self._handlers: Dict[type, List[Callable]] = {}

    def subscribe(self, event_type: type, handler: Callable):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def publish(self, event: DomainEvent):
        handlers = self._handlers.get(type(event), [])
        for handler in handlers:
            handler(event)

# Usage
event_bus = EventBus()

# Subscribe handlers
event_bus.subscribe(LeaveApprovedEvent, update_employee_balance)
event_bus.subscribe(LeaveApprovedEvent, send_notification)
event_bus.subscribe(LeaveApprovedEvent, log_audit_trail)
```

## Decisiones de Arquitectura

### ADR (Architecture Decision Record) Template
```markdown
# ADR-001: Usar SQLite como base de datos principal

## Estado
Aceptado

## Contexto
Necesitamos una base de datos para almacenar datos de empleados y vacaciones.
Opciones consideradas: SQLite, PostgreSQL, MySQL.

## Decisión
Usar SQLite con opción de migrar a PostgreSQL.

## Consecuencias

### Positivas
- Zero configuration
- Portable (archivo único)
- Suficiente para ~1000 empleados
- Backup simple (copiar archivo)

### Negativas
- No soporta concurrencia de escritura
- Sin full-text search nativo (requiere FTS5)
- Sin replicación

### Mitigaciones
- Implementar wrapper de base de datos para permitir cambio
- Usar PostgreSQL en producción si se requiere
```

### Tabla de Trade-offs
```
┌─────────────────────┬─────────────────────┬─────────────────────┐
│     Decisión        │     Beneficios      │     Trade-offs      │
├─────────────────────┼─────────────────────┼─────────────────────┤
│ SQLite default      │ Simplicidad, portable│ Concurrencia limitada│
│ FastAPI vs Flask    │ Async, typing, docs │ Learning curve       │
│ Vanilla JS vs React │ No build, simple    │ State management     │
│ JWT vs Sessions     │ Stateless, escalable│ No revocación fácil  │
│ Monolith vs Micro   │ Desarrollo rápido   │ Refactoring futuro   │
└─────────────────────┴─────────────────────┴─────────────────────┘
```

## Estrategias de Escalabilidad

### Horizontal Scaling
```
                    ┌──────────────┐
                    │ Load Balancer│
                    │   (nginx)    │
                    └──────┬───────┘
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
    │  FastAPI    │ │  FastAPI    │ │  FastAPI    │
    │  Instance 1 │ │  Instance 2 │ │  Instance 3 │
    └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
           │               │               │
           └───────────────┼───────────────┘
                           ▼
                    ┌──────────────┐
                    │  PostgreSQL  │
                    │   (Primary)  │
                    └──────────────┘
```

### Caching Strategy
```python
CACHING_LAYERS = {
    'L1': {
        'type': 'In-Memory (Python dict)',
        'ttl': 60,  # 1 minuto
        'use_cases': ['User session', 'Config']
    },
    'L2': {
        'type': 'Redis',
        'ttl': 300,  # 5 minutos
        'use_cases': ['API responses', 'Computed stats']
    },
    'L3': {
        'type': 'CDN (Static assets)',
        'ttl': 86400,  # 1 día
        'use_cases': ['CSS', 'JS', 'Images']
    }
}

# Implementation
from functools import lru_cache
from services.caching import cache

# L1: In-memory
@lru_cache(maxsize=100)
def get_grant_table():
    return {...}

# L2: Redis
@cache(ttl=300)
def get_compliance_stats(year: int):
    return calculate_compliance(year)
```

### Database Optimization
```python
# Read replicas for queries
class DatabaseRouter:
    def get_connection(self, operation: str):
        if operation in ['SELECT', 'READ']:
            return self.read_replica
        else:
            return self.primary

# Query optimization
QUERY_OPTIMIZATIONS = {
    'pagination': 'SELECT * FROM employees LIMIT ? OFFSET ?',
    'covering_index': 'CREATE INDEX idx_emp_year ON employees(year, employee_num, name)',
    'partial_index': 'CREATE INDEX idx_active ON genzai(employee_num) WHERE status != "退社"',
}
```

## Patrones de API Design

### RESTful Conventions
```python
# Resource naming
GET    /api/employees              # List all
GET    /api/employees/{id}         # Get one
POST   /api/employees              # Create
PUT    /api/employees/{id}         # Update (full)
PATCH  /api/employees/{id}         # Update (partial)
DELETE /api/employees/{id}         # Delete

# Nested resources
GET    /api/employees/{id}/leave-requests
POST   /api/employees/{id}/leave-requests

# Filtering, sorting, pagination
GET    /api/employees?year=2025&status=active&sort=-created_at&page=1&per_page=50

# Actions (non-CRUD)
POST   /api/leave-requests/{id}/approve
POST   /api/leave-requests/{id}/reject
POST   /api/data/sync
```

### API Versioning
```python
# URL versioning (recommended for YuKyuDATA)
/api/v1/employees
/api/v2/employees

# Header versioning
Accept: application/vnd.yukyu.v1+json

# Migration strategy
@app.get("/api/employees")
async def get_employees_legacy():
    """Deprecated: Use /api/v1/employees"""
    return RedirectResponse("/api/v1/employees")

@app.get("/api/v1/employees")
async def get_employees_v1():
    return paginated_response(employees)
```

## Módulos Propuestos para YuKyuDATA

### Estructura Modular
```
yukyu/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app setup
│   ├── config.py               # Configuration
│   └── dependencies.py         # Dependency injection
│
├── api/
│   ├── __init__.py
│   ├── v1/
│   │   ├── routes/
│   │   │   ├── employees.py
│   │   │   ├── leave_requests.py
│   │   │   ├── compliance.py
│   │   │   └── analytics.py
│   │   └── schemas/
│   │       ├── employee.py
│   │       └── leave_request.py
│   └── middleware/
│       ├── auth.py
│       ├── rate_limit.py
│       └── logging.py
│
├── domain/
│   ├── __init__.py
│   ├── models/
│   │   ├── employee.py
│   │   ├── leave_request.py
│   │   └── vacation_balance.py
│   ├── services/
│   │   ├── compliance_service.py
│   │   ├── balance_calculator.py
│   │   └── leave_service.py
│   └── events/
│       ├── leave_events.py
│       └── event_bus.py
│
├── infrastructure/
│   ├── __init__.py
│   ├── database/
│   │   ├── connection.py
│   │   ├── migrations/
│   │   └── repositories/
│   │       ├── employee_repo.py
│   │       └── leave_repo.py
│   ├── external/
│   │   ├── excel_parser.py
│   │   └── email_service.py
│   └── caching/
│       └── redis_cache.py
│
├── static/
│   ├── css/
│   ├── js/
│   └── assets/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
└── scripts/
    ├── migrate.py
    └── seed.py
```

### Dependency Injection Setup
```python
# app/dependencies.py
from functools import lru_cache
from infrastructure.database.repositories import SQLiteEmployeeRepository
from domain.services import LeaveService, ComplianceService

@lru_cache()
def get_employee_repository():
    return SQLiteEmployeeRepository(settings.database_url)

@lru_cache()
def get_leave_service():
    return LeaveService(
        leave_repo=get_leave_repository(),
        employee_repo=get_employee_repository(),
        event_bus=get_event_bus()
    )

# Usage in routes
@app.post("/api/v1/leave-requests")
async def create_leave_request(
    request: LeaveRequestCreate,
    leave_service: LeaveService = Depends(get_leave_service)
):
    return leave_service.create_request(request)
```

## Checklist de Arquitectura

### Pre-Desarrollo
- [ ] ADRs documentados para decisiones clave
- [ ] Bounded contexts identificados
- [ ] API contracts definidos (OpenAPI)
- [ ] Modelo de datos diseñado
- [ ] Estrategia de autenticación definida

### Durante Desarrollo
- [ ] Separation of concerns respetada
- [ ] Dependency injection implementada
- [ ] Código testeable (interfaces, no implementaciones)
- [ ] Logging estructurado
- [ ] Error handling consistente

### Pre-Producción
- [ ] Performance benchmarks
- [ ] Security audit
- [ ] Load testing
- [ ] Backup/restore verificado
- [ ] Monitoring configurado

---

**Principio Guía:** "La arquitectura correcta es la que permite que el sistema evolucione sin reescribir. Diseña para el cambio, no para la eternidad."
