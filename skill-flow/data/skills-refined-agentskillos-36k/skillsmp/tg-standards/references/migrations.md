# Migration Best Practices

## Core Principles

1. **Never edit applied migrations** - Once in production, migrations are immutable
2. **Test before deployment** - Test both forward and reverse migrations
3. **Keep migrations focused** - One logical change per migration
4. **Always provide reverse migrations** for `RunPython`

## Three-Step Pattern for New Required Fields

**Step 1: Add field as nullable**
```python
migrations.AddField(
    model_name='character',
    name='generation',
    field=models.IntegerField(null=True, blank=True),
)
```

**Step 2: Populate with data**
```python
def populate_generation(apps, schema_editor):
    Character = apps.get_model('characters', 'Character')
    for char in Character.objects.filter(generation__isnull=True):
        char.generation = 13
        char.save(update_fields=['generation'])

def reverse_populate(apps, schema_editor):
    Character = apps.get_model('characters', 'Character')
    Character.objects.update(generation=None)

operations = [
    migrations.RunPython(populate_generation, reverse_populate),
]
```

**Step 3: Make non-nullable**
```python
migrations.AlterField(
    model_name='character',
    name='generation',
    field=models.IntegerField(default=13),
)
```

## Use Historical Models

```python
def migrate_data(apps, schema_editor):
    # CORRECT - uses historical model state
    Character = apps.get_model('characters', 'Character')

    # WRONG - uses current model which may have different fields
    from characters.models import Character  # Don't do this!
```

## Handle Large Datasets

```python
def migrate_large_dataset(apps, schema_editor):
    Character = apps.get_model('characters', 'Character')
    
    # Use iterator() to prevent loading all into memory
    for char in Character.objects.iterator(chunk_size=1000):
        char.new_field = calculate_value(char)
        char.save(update_fields=['new_field'])
```

## Adding Constraints to Existing Data

```python
def validate_existing_data(apps, schema_editor):
    """Fix any existing data that violates constraints"""
    Character = apps.get_model('characters', 'Character')
    
    negative_xp = Character.objects.filter(xp__lt=0)
    if negative_xp.count() > 0:
        negative_xp.update(xp=0)  # Fix automatically

class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(validate_existing_data, migrations.RunPython.noop),
        migrations.AddConstraint(...),
    ]
```

## Squashing

```bash
# When app has 50+ migrations, all applied to production
python manage.py squashmigrations characters 0001 0050

# Test on fresh database
python manage.py migrate characters
```

## Commands

```bash
python manage.py makemigrations           # Create migrations
python manage.py migrate                  # Apply migrations
python manage.py showmigrations           # List status
python manage.py migrate app 0041         # Rollback to specific
python manage.py migrate app 0042 --fake  # Mark as applied without running
```
