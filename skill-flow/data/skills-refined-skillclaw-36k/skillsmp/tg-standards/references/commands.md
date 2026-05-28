# Management Command Patterns

## File Location

```
app_name/
└── management/
    ├── __init__.py
    └── commands/
        ├── __init__.py
        └── command_name.py
```

## Basic Command Template

```python
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Description of what this command does"

    def add_arguments(self, parser):
        parser.add_argument('chronicle_id', type=int)
        parser.add_argument('--verbose', action='store_true')
        parser.add_argument('--limit', type=int, default=100)

    def handle(self, *args, **options):
        verbose = options['verbose']
        try:
            # Command logic
            self.stdout.write(self.style.SUCCESS('Command completed'))
        except Exception as e:
            raise CommandError(f'Command failed: {e}')
```

## Output Styling

```python
self.stdout.write(self.style.SUCCESS('Operation successful'))  # Green
self.stdout.write(self.style.ERROR('Something failed'))        # Red
self.stdout.write(self.style.WARNING('Potential issue'))       # Yellow
self.stdout.write(self.style.NOTICE('Information'))            # Cyan
```

## Data Validation Command

```python
class Command(BaseCommand):
    help = "Validate data integrity across models"

    def add_arguments(self, parser):
        parser.add_argument('--fix', action='store_true')

    def handle(self, *args, **options):
        issues = []
        issues.extend(self.validate_characters(options['fix']))
        
        if issues:
            self.stdout.write(self.style.WARNING(f'Found {len(issues)} issues'))
            for issue in issues:
                self.stdout.write(f"  - {issue}")
        else:
            self.stdout.write(self.style.SUCCESS('No issues found'))

    def validate_characters(self, fix_mode):
        issues = []
        orphans = Character.objects.filter(owner__isnull=True)
        for char in orphans:
            issues.append(f"Character {char.id} has no owner")
            if fix_mode:
                char.delete()
        return issues
```

## Batch Processing

```python
def handle(self, *args, **options):
    batch_size = options['batch_size']
    dry_run = options['dry_run']
    
    queryset = Character.objects.filter(needs_processing=True)
    
    for batch in self.batch_iterator(queryset, batch_size):
        with transaction.atomic():
            for obj in batch:
                self.process_record(obj)

def batch_iterator(self, queryset, batch_size):
    start = 0
    while True:
        batch = list(queryset[start:start + batch_size])
        if not batch:
            break
        yield batch
        start += batch_size
```

## Testing Commands

```python
from io import StringIO
from django.core.management import call_command

class CommandTestCase(TestCase):
    def test_validate_command(self):
        out = StringIO()
        call_command('validate_data_integrity', stdout=out)
        self.assertIn('No issues found', out.getvalue())
```
