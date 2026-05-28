# Character Template System

Pre-configured character concepts from sourcebooks that speed up character creation.

## Template Data Structure

```python
CharacterTemplate(
    name="Template Name",
    gameline="mta",  # vtm, wta, mta, wto, ctd, dtf
    character_type="mage",
    concept="Concept Name",
    
    # Character Data (JSONFields)
    basic_info={"nature": "FK:Archetype:Name", "demeanor": "FK:Archetype:Name"},
    attributes={"strength": 2, "perception": 4, ...},
    abilities={"alertness": 2, "investigation": 3, ...},
    backgrounds=[{"name": "Contacts", "rating": 3}],
    powers={"auspex": 2, "celerity": 1},
    merits_flaws=[{"name": "Merit Name", "rating": 2}],
    specialties=["Ability (Specialty)"],
    languages=["English", "Latin"],
    
    is_official=True,
    is_public=True,
    times_used=0,
)
```

Use `"FK:Model:Name"` format for foreign key references (resolved during apply).

## Adding Template Selection

### 1. Form and View

```python
from core.models import CharacterTemplate

class CharacterTemplateSelectionForm(forms.Form):
    template = forms.ModelChoiceField(
        queryset=CharacterTemplate.objects.none(),
        required=False,
        empty_label="No template - build from scratch",
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, gameline="vtm", character_type="vampire", **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["template"].queryset = CharacterTemplate.objects.filter(
            gameline=gameline, character_type=character_type, is_public=True
        )

class VampireTemplateSelectView(LoginRequiredMixin, FormView):
    form_class = CharacterTemplateSelectionForm
    template_name = "characters/vampire/vampire/template_select.html"

    def form_valid(self, form):
        template = form.cleaned_data.get("template")
        if template:
            template.apply_to_character(self.object)
        self.object.creation_status = 1
        self.object.save()
        return redirect("characters:vampire:vampire_creation", pk=self.object.pk)
```

### 2. URL

```python
path("vampire/<int:pk>/template/", VampireTemplateSelectView.as_view(), name="vampire_template"),
```

### 3. Update Basics View success_url

```python
def get_success_url(self):
    return reverse("characters:vampire:vampire_template", kwargs={"pk": self.object.pk})
```

## Template Application Logic

`CharacterTemplate.apply_to_character(character)`:
1. Resolves `"FK:Model:Name"` → actual objects
2. Sets attributes and abilities directly
3. Creates BackgroundRating entries
4. Sets power ratings (disciplines/spheres/gifts)
5. Creates MeritFlawRating entries
6. Links Language objects
7. Creates Specialty entries
8. Creates TemplateApplication record
9. Increments times_used counter

## Loading Templates

```bash
python populate_db/character_templates/__init__.py      # All
python populate_db/character_templates/vampire_templates.py  # Specific gameline
```

## Reference Implementation

Mage (MtAHuman) is fully integrated:
- `characters/views/mage/mtahuman.py`
- `characters/urls/mage/detail.py`
- `characters/templates/characters/mage/mtahuman/template_select.html`
