# Model Patterns

## Character Model Hierarchy

```python
from characters.models.core.character import Character
from characters.models.core.human import Human

class MyGamelineHuman(Human):
    """Base human for this gameline."""
    gameline = "mygameline"

    class Meta:
        verbose_name = "My Gameline Human"
        verbose_name_plural = "My Gameline Humans"


class MyCharacter(MyGamelineHuman):
    """Specific character type."""
    type = "my_character"

    class Meta:
        verbose_name = "My Character"
        verbose_name_plural = "My Characters"
```

## Item Model

```python
from items.models.core.item import ItemModel

class MyItem(ItemModel):
    type = "my_item"
    gameline = "mygameline"

    class Meta:
        verbose_name = "My Item"
        verbose_name_plural = "My Items"
```

## Location Model

```python
from locations.models.core.location import LocationModel

class MyLocation(LocationModel):
    type = "my_location"
    gameline = "mygameline"

    class Meta:
        verbose_name = "My Location"
        verbose_name_plural = "My Locations"
```

## Reference/Lookup Model

For factions, clans, disciplines, etc. Inherits from `core.models.Model`.

```python
from core.models import Model
from django.db import models
from django.urls import reverse


class MyReferenceModel(Model):
    """
    Inherited from Model: name, description, owner, chronicle, status, 
    display, sources (M2M), public_info, image, st_notes
    """
    type = "my_reference"
    gameline = "mygameline"

    # Only gameline-specific fields
    nickname = models.CharField(max_length=100, blank=True)
    special_ability = models.TextField(blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )

    class Meta:
        verbose_name = "My Reference"
        verbose_name_plural = "My References"
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("characters:mygameline:detail:my_reference", kwargs={"pk": self.pk})

    def get_update_url(self):
        return reverse("characters:mygameline:update:my_reference", kwargs={"pk": self.pk})

    @classmethod
    def get_creation_url(cls):
        return reverse("characters:mygameline:create:my_reference")
```

## Through Model (M2M with extra data)

```python
class MyRating(models.Model):
    """Through model for character -> reference relationship."""
    character = models.ForeignKey(
        "MyCharacter",
        on_delete=models.CASCADE,
        related_name="my_ratings"
    )
    reference = models.ForeignKey("MyReferenceModel", on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    note = models.TextField(blank=True, default="")

    class Meta:
        unique_together = ["character", "reference"]
        ordering = ["reference__name"]

    def __str__(self):
        return f"{self.character.name} - {self.reference.name} ({self.rating})"
```

## Key Rules

- Do NOT redefine fields inherited from `core.models.Model`: `name`, `description`, `owner`, `chronicle`, `status`, `display`, `sources` (M2M)
- Use `add_source(book_title, page_number)` method for sources
- `get_heading()` is inherited - do NOT override unless special behavior needed
