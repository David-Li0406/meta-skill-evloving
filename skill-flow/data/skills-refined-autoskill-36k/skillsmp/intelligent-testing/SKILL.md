---
name: intelligent-testing
description: Testing inteligente con generación automática de tests, detección de flaky tests y análisis de cobertura
---

# Intelligent Testing Skill

Skill avanzado para testing automatizado que genera tests, detecta tests frágiles, analiza cobertura y sugiere mejoras basadas en análisis estático y patrones de código.

## Filosofía de Testing

### Pirámide de Tests
```
          /\
         /  \     E2E Tests (10%)
        /----\    - Playwright/Cypress
       /      \   - Critical user flows
      /--------\  Integration Tests (20%)
     /          \ - API endpoints
    /------------\- Database operations
   /              \ Unit Tests (70%)
  /----------------\- Pure functions
 /                  \- Business logic
/____________________\
```

### Principios FIRST
- **F**ast: Tests rápidos (< 100ms unitarios)
- **I**ndependent: Sin dependencias entre tests
- **R**epeatable: Mismo resultado siempre
- **S**elf-validating: Pass/fail automático
- **T**imely: Escritos junto al código

## Generación Automática de Tests

### 1. Tests Unitarios (Python)
```python
# Dado el código:
def calculate_granted_days(seniority_years: float) -> int:
    GRANT_TABLE = {0.5: 10, 1.5: 11, 2.5: 12, 3.5: 14, 4.5: 16, 5.5: 18, 6.5: 20}
    granted = 0
    for threshold, days in sorted(GRANT_TABLE.items()):
        if seniority_years >= threshold:
            granted = days
    return granted

# Tests generados automáticamente:
import pytest
from services.fiscal_year import calculate_granted_days

class TestCalculateGrantedDays:
    """Tests for calculate_granted_days function."""

    # Boundary tests
    @pytest.mark.parametrize("years,expected", [
        (0.0, 0),      # Bajo mínimo
        (0.5, 10),     # Exactamente 6 meses
        (0.49, 0),     # Justo bajo el límite
        (0.51, 10),    # Justo sobre el límite
        (6.5, 20),     # Máximo
        (10.0, 20),    # Sobre máximo
    ])
    def test_boundary_values(self, years, expected):
        assert calculate_granted_days(years) == expected

    # Edge cases
    def test_negative_years(self):
        assert calculate_granted_days(-1.0) == 0

    def test_float_precision(self):
        assert calculate_granted_days(1.4999999) == 10
        assert calculate_granted_days(1.5000001) == 11

    # Regression tests
    def test_known_values(self):
        assert calculate_granted_days(2.5) == 12
        assert calculate_granted_days(5.5) == 18
```

### 2. Tests de API (FastAPI)
```python
# Dado el endpoint:
@app.get("/api/employees")
async def get_employees(year: int = None):
    return database.get_employees(year=year)

# Tests generados:
from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

class TestGetEmployees:
    """API tests for /api/employees endpoint."""

    def test_get_all_employees_success(self):
        response = client.get("/api/employees")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_employees_by_year(self):
        response = client.get("/api/employees?year=2025")
        assert response.status_code == 200
        for emp in response.json():
            assert emp.get("year") == 2025

    def test_get_employees_invalid_year(self):
        response = client.get("/api/employees?year=invalid")
        assert response.status_code == 422  # Validation error

    def test_get_employees_empty_result(self):
        response = client.get("/api/employees?year=1900")
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.parametrize("year", [2020, 2021, 2022, 2023, 2024, 2025])
    def test_get_employees_multiple_years(self, year):
        response = client.get(f"/api/employees?year={year}")
        assert response.status_code == 200
```

### 3. Tests E2E (Playwright)
```javascript
// Dado el flujo de usuario:
// 1. Login → 2. Dashboard → 3. Submit Leave Request → 4. Verify

import { test, expect } from '@playwright/test';

test.describe('Leave Request Workflow', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('/');
        // Login
        await page.locator('[data-testid="login-btn"]').click();
        await page.locator('[data-testid="username"]').fill('admin');
        await page.locator('[data-testid="password"]').fill('password');
        await page.locator('[data-testid="submit-login"]').click();
        await expect(page).toHaveURL('/dashboard');
    });

    test('should submit leave request successfully', async ({ page }) => {
        // Navigate to requests
        await page.locator('[data-testid="nav-requests"]').click();

        // Fill form
        await page.locator('[data-testid="start-date"]').fill('2025-12-25');
        await page.locator('[data-testid="end-date"]').fill('2025-12-26');
        await page.locator('[data-testid="leave-type"]').selectOption('full');
        await page.locator('[data-testid="reason"]').fill('Christmas vacation');

        // Submit
        await page.locator('[data-testid="submit-request"]').click();

        // Verify
        await expect(page.locator('[data-testid="success-toast"]'))
            .toContainText('Request submitted');
        await expect(page.locator('[data-testid="pending-requests"]'))
            .toContainText('2025-12-25');
    });

    test('should reject invalid date range', async ({ page }) => {
        await page.locator('[data-testid="nav-requests"]').click();
        await page.locator('[data-testid="start-date"]').fill('2025-12-26');
        await page.locator('[data-testid="end-date"]').fill('2025-12-25');  // End before start
        await page.locator('[data-testid="submit-request"]').click();

        await expect(page.locator('[data-testid="error-message"]'))
            .toContainText('End date must be after start date');
    });
});
```

## Detección de Tests Frágiles

### Patrones Problemáticos
```python
FRAGILE_PATTERNS = {
    'time_dependent': {
        'pattern': r'datetime\.now\(\)|time\.time\(\)|Date\.now\(\)',
        'fix': 'Usar freezegun/timemachine para mockear tiempo',
        'example': '''
            # ANTES (frágil)
            def test_expiry():
                assert is_expired(datetime.now() - timedelta(days=1))

            # DESPUÉS (estable)
            @freeze_time("2025-01-09")
            def test_expiry():
                assert is_expired(datetime(2025, 1, 8))
        '''
    },
    'order_dependent': {
        'pattern': r'test_\d+_|test_a_|test_first_',
        'fix': 'Usar fixtures para setup/teardown independiente',
    },
    'sleep_wait': {
        'pattern': r'time\.sleep\(|await asyncio\.sleep\(|setTimeout\(',
        'fix': 'Usar polling/waitFor con timeout en lugar de sleep fijo',
        'example': '''
            # ANTES (frágil)
            await asyncio.sleep(2)
            assert result.ready

            # DESPUÉS (estable)
            await wait_for(lambda: result.ready, timeout=5)
        '''
    },
    'random_values': {
        'pattern': r'random\.\w+\(|uuid\.uuid4\(\)|faker\.',
        'fix': 'Fijar seed o usar valores determinísticos',
    },
    'external_dependency': {
        'pattern': r'requests\.get\(|fetch\(|\.connect\(',
        'fix': 'Mockear llamadas externas con responses/httpx-mock',
    }
}
```

### Análisis de Flakiness
```python
def analyze_test_stability(test_history: list) -> dict:
    """
    Analiza historial de ejecuciones para detectar tests flaky.

    Returns:
        {
            "test_name": {
                "pass_rate": 0.95,
                "flakiness_score": 0.05,
                "common_failure_patterns": ["timeout", "assertion"],
                "recommendation": "Add explicit wait for async operation"
            }
        }
    """
    results = {}
    for test in test_history:
        runs = test['runs']
        passes = sum(1 for r in runs if r['status'] == 'pass')
        pass_rate = passes / len(runs)

        if pass_rate < 1.0 and pass_rate > 0.0:
            results[test['name']] = {
                'pass_rate': pass_rate,
                'flakiness_score': 1 - pass_rate,
                'common_failure_patterns': extract_failure_patterns(runs),
                'recommendation': generate_fix_recommendation(runs)
            }

    return results
```

## Análisis de Cobertura

### Cobertura por Módulo
```python
COVERAGE_THRESHOLDS = {
    'critical': {
        'files': ['fiscal_year.py', 'auth.py', 'database.py'],
        'line_coverage': 90,
        'branch_coverage': 85,
    },
    'important': {
        'files': ['main.py', 'excel_service.py'],
        'line_coverage': 80,
        'branch_coverage': 70,
    },
    'standard': {
        'files': ['*'],
        'line_coverage': 70,
        'branch_coverage': 60,
    }
}
```

### Cobertura de Casos de Uso
```python
def analyze_use_case_coverage(code_path: str, tests_path: str) -> dict:
    """
    Analiza qué casos de uso están cubiertos por tests.

    Returns:
        {
            "5_day_compliance": {
                "covered": True,
                "tests": ["test_check_5day_compliance", "test_compliance_alert"],
                "missing_scenarios": []
            },
            "lifo_deduction": {
                "covered": False,
                "tests": [],
                "missing_scenarios": [
                    "Deduction spanning multiple years",
                    "Deduction with expired days"
                ]
            }
        }
    """
```

## Templates de Tests

### Fixture Factory
```python
import pytest
from datetime import date, timedelta

@pytest.fixture
def employee_factory():
    """Factory para crear empleados de test."""
    def _create(
        employee_num: str = "TEST001",
        name: str = "Test Employee",
        granted: float = 10.0,
        used: float = 0.0,
        year: int = 2025
    ):
        return {
            "id": f"{employee_num}_{year}",
            "employee_num": employee_num,
            "name": name,
            "granted": granted,
            "used": used,
            "balance": granted - used,
            "year": year
        }
    return _create

@pytest.fixture
def leave_request_factory():
    """Factory para crear solicitudes de test."""
    def _create(
        employee_num: str = "TEST001",
        days: float = 1.0,
        status: str = "PENDING",
        start_date: date = None
    ):
        start = start_date or date.today()
        return {
            "employee_num": employee_num,
            "days_requested": days,
            "status": status,
            "start_date": start.isoformat(),
            "end_date": (start + timedelta(days=int(days))).isoformat()
        }
    return _create
```

### Mocking Best Practices
```python
from unittest.mock import Mock, patch, MagicMock

# Mock de base de datos
@pytest.fixture
def mock_db():
    with patch('database.get_db') as mock:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock.__enter__ = Mock(return_value=mock_conn)
        mock.__exit__ = Mock(return_value=False)
        yield mock_cursor

# Mock de servicios externos
@pytest.fixture
def mock_excel_service():
    with patch('excel_service.parse_excel_file') as mock:
        mock.return_value = [
            {"employee_num": "001", "name": "Test", "granted": 10, "used": 5}
        ]
        yield mock
```

## Comandos de Testing

### Ejecución
```bash
# Backend
pytest tests/ -v                          # Todos los tests
pytest tests/ -v --cov=. --cov-report=html  # Con cobertura
pytest tests/ -v -x                       # Parar en primer fallo
pytest tests/ -v -k "compliance"          # Solo tests con "compliance"
pytest tests/ --tb=short                  # Traceback corto

# Frontend
npx jest                                  # Todos los tests
npx jest --coverage                       # Con cobertura
npx jest --watch                          # Watch mode
npx jest --testNamePattern="escapeHtml"   # Test específico

# E2E
npx playwright test                       # Todos
npx playwright test --headed              # Ver browser
npx playwright test --debug               # Debug mode
npx playwright show-report                # Ver reporte
```

### Generación de Reportes
```bash
# Cobertura combinada
pytest --cov=. --cov-report=xml
npx jest --coverage --coverageReporters=cobertura

# Mutation testing
pip install mutmut
mutmut run --paths-to-mutate=fiscal_year.py
mutmut results
```

## Integración con YuKyuDATA

### Tests Críticos Requeridos
```python
# 1. Compliance Tests
class TestFiveDayCompliance:
    def test_employee_with_10_days_using_4_is_non_compliant(self):
        pass
    def test_employee_with_10_days_using_5_is_compliant(self):
        pass
    def test_employee_with_9_days_exempt_from_rule(self):
        pass

# 2. LIFO Deduction Tests
class TestLIFODeduction:
    def test_deduct_from_current_year_first(self):
        pass
    def test_deduct_from_previous_year_when_current_exhausted(self):
        pass
    def test_expired_days_not_deductible(self):
        pass

# 3. Year-End Carryover Tests
class TestYearEndCarryover:
    def test_carryover_up_to_max_days(self):
        pass
    def test_expire_days_older_than_2_years(self):
        pass
    def test_preserve_balance_order(self):
        pass

# 4. Leave Request Workflow Tests
class TestLeaveRequestWorkflow:
    def test_create_pending_request(self):
        pass
    def test_approve_deducts_balance(self):
        pass
    def test_reject_preserves_balance(self):
        pass
    def test_revert_restores_balance(self):
        pass
```

### GitHub Actions CI
```yaml
name: Test Suite
on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest tests/ --cov=. --cov-report=xml
      - uses: codecov/codecov-action@v4

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx jest --coverage

  e2e-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test
```

---

**Principio Guía:** "Test what matters. Make tests reliable. Fast feedback > complete coverage."
