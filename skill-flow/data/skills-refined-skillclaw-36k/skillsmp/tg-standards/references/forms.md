# Form Patterns

## Creation Form

```python
from django import forms
from .models import MyCharacter

class MyCharacterCreationForm(forms.ModelForm):
    class Meta:
        model = MyCharacter
        fields = ["name", "nature", "demeanor", "concept", "chronicle", "faction", "image", "npc"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter character name", "class": "form-control"}),
            "concept": forms.TextInput(attrs={"placeholder": "Brief character concept", "class": "form-control"}),
            "chronicle": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["chronicle"].queryset = Chronicle.objects.filter(
                models.Q(allowed_users=user) | models.Q(storytellers=user)
            ).distinct()
```

## Limited Edit Form (for owners, non-ST users)

Owners can only edit descriptive fields:

```python
class LimitedMyCharacterEditForm(forms.ModelForm):
    class Meta:
        model = MyCharacter
        fields = ["notes", "description", "public_info", "image", "history", "goals"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "Physical description..."}),
            "history": forms.Textarea(attrs={"rows": 6, "placeholder": "Character history..."}),
            "notes": forms.Textarea(attrs={"rows": 4, "placeholder": "Private notes (ST only)..."}),
        }
```

**Only allow:** `notes`, `description`, `public_info`, `image`, `history`, `goals`
**Never allow owners to edit:** stats, XP, status, mechanical fields

## FormSet Pattern

```python
from django.forms import inlineformset_factory

class BaseMyRatingFormSet(forms.BaseInlineFormSet):
    def __init__(self, *args, character=None, **kwargs):
        self.character = character
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()
        # Custom validation here

MyRatingFormSet = inlineformset_factory(
    MyCharacter,
    MyRating,
    form=MyRatingForm,
    formset=BaseMyRatingFormSet,
    extra=3,
    can_delete=True,
)
```

## Freebies/XP Form

```python
class MyFreebiesForm(HumanFreebiesForm):
    CATEGORY_CHOICES = [
        ("attributes", "Attributes"),
        ("abilities", "Abilities"),
        ("backgrounds", "Backgrounds"),
        ("my_power", "My Power"),
        ("willpower", "Willpower"),
        ("merits", "Merits"),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].choices = self.CATEGORY_CHOICES
```

## Template Pattern (form.html)

```html
{% extends "core/form.html" %}
{% block creation_title %}
    {% if object %}Update{% else %}Create{% endif %} My Character
{% endblock %}
{% block contents %}
    <div class="tg-card">
        <div class="tg-card-header">
            <h2 class="tg-card-title {{ object.get_heading|default:'mta_heading' }}">Basic Information</h2>
        </div>
        <div class="tg-card-body" style="padding: 24px;">
            <div class="row mb-3">
                <div class="col-md-6">
                    <label for="{{ form.name.id_for_label }}" class="form-label">Name</label>
                    {{ form.name }}
                </div>
                <div class="col-md-6">
                    <label for="{{ form.concept.id_for_label }}" class="form-label">Concept</label>
                    {{ form.concept }}
                </div>
            </div>
        </div>
    </div>
{% endblock %}
```

## Checkbox Pattern

```html
<div class="row mb-3">
    <div class="col-md-12">
        <h6 class="{{ object.get_heading }} mb-2">Features</h6>
    </div>
    <div class="col-md-4">
        <div class="form-check">
            {{ form.feature_one }}
            <label class="form-check-label" for="{{ form.feature_one.id_for_label }}">Feature One</label>
        </div>
    </div>
</div>
```
