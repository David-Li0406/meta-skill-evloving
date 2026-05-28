# Permission System

## Quick Reference

| Use Case | Method |
|----------|--------|
| Object-level access (detail/update views) | View mixins (`ViewPermissionMixin`, `EditPermissionMixin`) |
| Role-based checks (forms, templates) | `is_st()` |
| Owner editing restrictions | Limited forms |

## View Mixins

```python
from core.mixins import (
    ViewPermissionMixin,      # VIEW_FULL permission
    EditPermissionMixin,      # EDIT_FULL permission
    SpendXPPermissionMixin,   # XP spending
    SpendFreebiesPermissionMixin,  # Freebie spending
    VisibilityFilterMixin,    # Filter queryset by visibility
    OwnerRequiredMixin,       # Must be object owner
    STRequiredMixin,          # Must be storyteller
)
```

## is_st() - Role-Based Checks

For general storyteller checks not tied to specific objects:

```python
# In views - form selection
def get_form_class(self):
    if self.request.user.profile.is_st() or self.request.user.is_staff:
        return CharacterForm  # Full form
    return LimitedCharacterEditForm

# In templates
{% if user.profile.is_st %}
    <!-- ST-only controls -->
{% endif %}
```

## PermissionManager (Object-Level)

```python
from core.permissions import PermissionManager, Permission

pm = PermissionManager()
if pm.check_permission(user, character, Permission.EDIT_FULL):
    # Allow editing
```

## Roles

- `OWNER` - Object owner
- `ADMIN` - Superuser/staff
- `CHRONICLE_HEAD_ST` - Head ST of object's chronicle
- `GAME_ST` - Game ST (read-only)
- `PLAYER` - Player in same chronicle
- `OBSERVER` - Granted observer access

## Limited Forms for Owners

Owners can only edit descriptive fields:
```python
fields = ["notes", "description", "public_info", "image", "history", "goals"]
```

Never allow owners to edit: stats, XP, status, mechanical fields.

## Query Optimization

```python
# Always prefetch for permission checks
characters = Character.objects.select_related(
    'owner', 'chronicle'
).prefetch_related(
    'chronicle__storytellers',
    'observers'
)
```

## User + Profile Pattern

```python
# Access pattern
request.user.profile.is_st()
request.user.profile.preferred_heading
request.user.profile.my_characters()

# Always prefetch profile
users = User.objects.select_related('profile').all()
```
