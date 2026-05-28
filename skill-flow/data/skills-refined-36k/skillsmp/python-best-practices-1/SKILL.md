---
name: python-best-practices
description: Python best practices e styleguide
triggers: [python, pep8, black, flake8, mypy, type hints]
sources:
  - https://github.com/kennethreitz/python-guide
  - https://github.com/wemake-services/wemake-python-styleguide
  - https://github.com/vinta/awesome-python
---

# Python Best Practices

**Convenções e styleguide para código Python.**

---

## Type Hints

**SEMPRE usar type hints em todas as assinaturas de função:**

```python
from typing import Optional, List, Dict, Any

def process_data(
    user_id: int,
    data: Dict[str, Any],
    optional_param: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Processa dados do usuário."""
    return []
```

---

## Estrutura de Módulos

### Regra de Múltiplas Classes

**Quando um módulo tem mais de uma classe, cada classe deve estar em um arquivo separado:**

```
# ❌ ERRADO
utils/validators.py:
  - EmailValidator
  - PhoneValidator
  - URLValidator

# ✅ CORRETO
utils/validators/
  ├── __init__.py
  ├── email.py
  ├── phone.py
  └── url.py
```

---

## Code Style

### Black (Formatação)

```bash
black .
```

### isort (Imports)

```bash
isort .
```

### flake8 (Linting)

```bash
flake8 .
```

### mypy (Type Checking)

```bash
mypy src/
```

---

## Estrutura de Projeto

```
project/
├── src/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── modules/
│   └── tests/
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
└── pyproject.toml
```

---

## Checklist

- [ ] Type hints em todas as funções
- [ ] Múltiplas classes em módulos separados
- [ ] Black para formatação
- [ ] isort para organização de imports
- [ ] flake8 para linting
- [ ] mypy para type checking

