# Testing Patterns

## Commands

```bash
python manage.py test                           # All tests
python manage.py test characters                # App-specific
python manage.py test characters.tests.TestClass.test_method  # Specific
python manage.py test --verbosity=2             # Verbose
```

## File Location Pattern

Test structure mirrors source code:

| Source | Test |
|--------|------|
| `characters/models/vampire/vampire.py` | `characters/tests/models/vampire/test_vampire.py` |
| `items/views/mage/wonder.py` | `items/tests/views/mage/test_wonder.py` |

## Directory Structure

```
app/
├── models/gameline/model.py
├── views/gameline/view.py
└── tests/
    ├── models/gameline/test_model.py
    └── views/gameline/test_view.py
```

## Model Test Pattern

```python
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class CharacterModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_character_creation(self):
        pass
    
    def test_get_absolute_url(self):
        pass
```

## View Test Pattern

```python
from django.test import TestCase, Client
from django.urls import reverse

class CharacterViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(...)
        self.character = Character.objects.create(owner=self.user, ...)
    
    def test_detail_view_permission(self):
        response = self.client.get(
            reverse('characters:gameline:detail:character', kwargs={'pk': self.character.pk})
        )
        self.assertEqual(response.status_code, 200)
    
    def test_update_view_requires_login(self):
        response = self.client.get(
            reverse('characters:gameline:update:character', kwargs={'pk': self.character.pk})
        )
        self.assertRedirects(response, '/accounts/login/...')
```

## Migration Test Pattern

```python
from django.test import TransactionTestCase
from django.core.management import call_command

class MigrationTestCase(TransactionTestCase):
    def test_migration_forward_backward(self):
        call_command('migrate', 'characters', '0041')
        call_command('migrate', 'characters', '0042')
        call_command('migrate', 'characters', '0041')  # Rollback
```
