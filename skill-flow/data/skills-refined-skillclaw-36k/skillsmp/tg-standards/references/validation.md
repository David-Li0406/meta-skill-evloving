# Data Validation Patterns

## Priority Guidelines

| Priority | What to Validate | Pattern |
|----------|-----------------|---------|
| CRITICAL | XP/freebie operations | `@transaction.atomic` + `select_for_update()` |
| HIGH | Numeric ranges (1-10, 0-5) | `CheckConstraint` + Field validators |
| MEDIUM | Cross-field rules | `clean()` method |
| LOW | JSON structure | JSON schema validation |

## Transaction Pattern (XP/Freebie Operations)

```python
from django.db import transaction
from django.core.exceptions import ValidationError

class Character(Model):
    @transaction.atomic
    def spend_xp(self, trait_name, cost, category):
        # Lock row for concurrent access
        char = Character.objects.select_for_update().get(pk=self.pk)
        
        if char.xp < cost:
            raise ValidationError(f"Insufficient XP: need {cost}, have {char.xp}")
        
        char.xp -= cost
        char.spent_xp.append({...})
        char.save(update_fields=['xp', 'spent_xp'])
```

## Database Constraint Pattern

```python
from django.db.models import CheckConstraint, Q

class Character(Model):
    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(xp__gte=0),
                name='%(app_label)s_%(class)s_xp_non_negative',
                violation_error_message="XP cannot be negative"
            ),
        ]
```

## Model Validation Pattern

```python
class Human(Character):
    def clean(self):
        super().clean()
        if self.temporary_willpower > self.willpower:
            raise ValidationError({
                'temporary_willpower': f"Cannot exceed permanent willpower ({self.willpower})"
            })
```

## Field Validator Pattern

```python
from django.core.validators import MinValueValidator, MaxValueValidator

class AttributeBlock(models.Model):
    strength = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
```

## Status State Machine

```python
STATUS_TRANSITIONS = {
    'Un': ['Sub', 'Ret'],      # Unfinished -> Submitted or Retired
    'Sub': ['Un', 'App', 'Ret'],  # Submitted -> back, Approved, or Retired
    'App': ['Ret', 'Dec'],     # Approved -> Retired or Deceased
    'Ret': ['App'],            # Retired -> back to Approved
    'Dec': [],                 # Deceased -> no transitions
}

def clean(self):
    if self.pk:
        old = Character.objects.get(pk=self.pk)
        if old.status != self.status:
            if self.status not in self.STATUS_TRANSITIONS.get(old.status, []):
                raise ValidationError({'status': f"Cannot transition from {old.status} to {self.status}"})
```

## Testing Validation

```python
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

class TestCharacterValidation(TestCase):
    def test_xp_cannot_be_negative_db_constraint(self):
        character.xp = -100
        with self.assertRaises(IntegrityError):
            character.save()

    def test_xp_cannot_be_negative_model_validation(self):
        character.xp = -100
        with self.assertRaises(ValidationError):
            character.full_clean()
```
