---
name: django-best-practices
description: Django best practices baseadas em cookiecutter-django e produção real
triggers: [django, djangorestframework, drf, model, view, serializer, migration]
source: https://github.com/cookiecutter/cookiecutter-django
---

# Django Best Practices

**Convenções baseadas em cookiecutter-django e experiência de produção.**

---

## Estrutura de Projeto

### Organização Recomendada

```
project/
├── config/              # Settings (base, local, production, test)
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   ├── production.py
│   │   └── test.py
│   ├── urls.py
│   └── wsgi.py
├── apps/                # Aplicações Django
│   ├── users/
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── user.py
│   │   ├── views/
│   │   ├── serializers/
│   │   └── admin.py
│   └── core/
├── static/
├── media/
├── templates/
├── locale/
├── requirements/
│   ├── base.txt
│   ├── local.txt
│   └── production.txt
└── manage.py
```

### Regra de Múltiplas Classes

**Quando um módulo tem mais de uma classe, cada classe deve estar em um arquivo separado:**

```
# ❌ ERRADO
apps/users/models.py:
  - User
  - Profile
  - Role

# ✅ CORRETO
apps/users/models/
  ├── __init__.py      # Exporta todas
  ├── user.py          # class User
  ├── profile.py       # class Profile
  └── role.py          # class Role
```

---

## Settings

### 12-Factor App

Usar `django-environ` para configuração via variáveis de ambiente:

```python
import environ

env = environ.Env()

DEBUG = env.bool("DEBUG", default=False)
SECRET_KEY = env("SECRET_KEY")
DATABASES = {
    "default": env.db("DATABASE_URL")
}
```

### Separação por Ambiente

- `base.py` - Configurações comuns
- `local.py` - Desenvolvimento local
- `production.py` - Produção
- `test.py` - Testes

---

## Models

### Custom User Model

**SEMPRE usar custom user model desde o início:**

```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    # Campos customizados aqui
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
```

### Soft Delete

```python
class SoftDeleteModel(models.Model):
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True
    
    def soft_delete(self):
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()
```

---

## Migrations

### PROIBIÇÃO CRÍTICA

**TODO E QUALQUER AGENTE ESTÁ PROIBIDO DE MEXER EM MIGRATIONS JÁ APLICADAS:**

- ❌ **NUNCA** alterar migrations já commitadas e aplicadas
- ❌ **NUNCA** editar arquivos de migration existentes
- ❌ **NUNCA** deletar migrations antigas
- ✅ **SEMPRE** criar nova migration para alterações
- ✅ **SEMPRE** testar migrations em desenvolvimento primeiro

---

## Django REST Framework

### Serializers

```python
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username"]
        read_only_fields = ["id"]
```

### ViewSets

```python
from rest_framework import viewsets

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
```

---

## SQL Puro

**Para queries complexas, usar SQL puro com proteção:**

**Referência obrigatória (template/snippet do cursor-multiagent-system):**
- `core/templates/database/django-sql-snippets.py` - Funções genéricas para SQL puro (Django) com proteção contra SQL injection

```python
from core.templates.database.django_sql_snippets import sql_to_dict, sql_to_list, query_value, exec_sql

# Exemplo: Obter resultados como lista de dicionários
results = sql_to_dict(
    "SELECT * FROM users WHERE email = %s",
    param=("user@example.com",)
)

# Exemplo: Obter valor único
count = query_value("SELECT COUNT(*) FROM users")

# Exemplo: Executar update/insert
exec_sql(
    "UPDATE users SET status = 'active' WHERE id = %s",
    param=(user_id,)
)
```

---

## Cache System

**Para consultas repetitivas, usar cache Redis:**

**Referência obrigatória (template/snippet do cursor-multiagent-system):**
- `core/templates/cache/redis-cache-snippet.py` - Sistema de cache Redis genérico (Django e standalone)

```python
from core.templates.cache.redis_cache_snippet import CacheSystem
from django.conf import settings

# Configurar cache (exemplo com Django settings)
cache = CacheSystem(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=getattr(settings, 'REDIS_PASSWORD', None),
    db=0
)

def get_user_profile(user_id):
    cache_key = f"user_profile:{user_id}"
    cached = cache.read(cache_key)
    if cached:
        return cached
    
    profile = User.objects.get(id=user_id)
    cache.save(cache_key, profile_data, expiration=3600)
    return profile
```

---

## Checklist

- [ ] Custom user model implementado
- [ ] Settings separados por ambiente
- [ ] Múltiplas classes em módulos separados
- [ ] Migrations nunca alteradas após aplicadas
- [ ] SQL puro com proteção contra injection (quando necessário)
- [ ] Cache system para consultas repetitivas (quando necessário)

