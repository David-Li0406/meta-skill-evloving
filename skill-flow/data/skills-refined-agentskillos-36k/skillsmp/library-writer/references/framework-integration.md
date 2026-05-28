# Framework Integration

How to integrate libraries with frameworks without creating tight coupling.

## Core Principle

**Never require frameworks directly.** The library should work:
- In framework applications (with integration)
- In plain applications (without framework)
- In test environments (isolated)

## Conditional Loading Pattern

### Check Before Loading

```
# Entry point
if framework_is_available():
    load_framework_integration()

# Framework integration loads only when:
# 1. Framework is installed
# 2. Framework is actually being used
```

### Detection Patterns

```
Python (Django):
  if 'django' in sys.modules:
      from .integrations.django import setup

JavaScript (Express):
  if (typeof require !== 'undefined') {
    try {
      require.resolve('express');
      // Express is available
    } catch (e) {
      // Express not installed
    }
  }

Ruby (Rails):
  if defined?(Rails)
    require_relative 'integrations/rails'
  end
```

## Lazy Initialization

### Don't Initialize at Import

```
Bad:
  # Runs immediately when library is imported
  import framework
  framework.register(MyLibrary)

Good:
  # Runs only when framework triggers it
  def on_framework_ready():
      register_with_framework()
```

### Framework Hooks

Most frameworks provide hooks for lazy initialization:

```
Django:
  # apps.py
  class MyLibConfig(AppConfig):
      def ready(self):
          # Called when Django is ready
          setup_mylib()

Rails:
  # railtie.rb
  class MyLibRailtie < Rails::Railtie
      initializer "mylib.setup" do
          # Called during Rails boot
          setup_mylib
      end
  end

Express:
  # middleware pattern
  app.use(mylib.middleware())
```

## Integration Structure

### Separate Integration Modules

```
lib/
  my_library/
    core/              # Framework-independent
      client.ext
      config.ext
    integrations/      # Framework-specific
      django.ext
      rails.ext
      express.ext
```

### Integration Module Pattern

```
# integrations/framework.ext

# Import framework (safe - only loaded when needed)
import framework

# Import library core
from ..core import Client, Config

def setup():
    """Register library with framework"""
    framework.register_extension(Client)

def middleware():
    """Framework middleware/plugin"""
    return FrameworkMiddleware()

class FrameworkMiddleware:
    """Framework-specific adapter"""
    def __init__(self):
        self.client = Client()

    def process_request(self, request):
        # Framework-specific logic
        pass
```

## Configuration Integration

### Environment-Based Config

```
# Works with or without framework
api_key = os.environ.get("MYLIB_API_KEY")

# Framework can override
if framework_available():
    api_key = framework.settings.get("MYLIB_API_KEY", api_key)
```

### Framework Config Adapters

```
# Django settings adapter
def get_django_config():
    from django.conf import settings
    return {
        'api_key': getattr(settings, 'MYLIB_API_KEY', None),
        'timeout': getattr(settings, 'MYLIB_TIMEOUT', 30),
    }

# Apply framework config
if django_available():
    config = get_django_config()
    MyLib.configure(**config)
```

## Model/ORM Integration

### Mixin Pattern

```
# Library provides a mixin
class SearchableMixin:
    @classmethod
    def search(cls, query):
        return search_index.query(cls, query)

# User includes in their model
class Product(Model, SearchableMixin):
    name = CharField()
```

### Decorator Pattern

```
# Library provides a decorator
@searchable(fields=['name', 'description'])
class Product(Model):
    name = CharField()
    description = TextField()
```

### Class Method Extension

```
# Library extends model class
def add_search_methods(model_class):
    model_class.search = classmethod(search_method)
    model_class.reindex = classmethod(reindex_method)

# Called during framework initialization
for model in registered_models:
    add_search_methods(model)
```

## Testing Integration Code

### Test Without Framework

```
# Unit tests don't need framework
def test_core_functionality():
    client = Client()
    result = client.process(data)
    assert result == expected
```

### Test With Framework

```
# Integration tests use framework
def test_django_integration():
    from django.test import TestCase

    class MyLibTestCase(TestCase):
        def test_model_integration(self):
            product = Product.objects.create(name="Test")
            results = Product.search("test")
            assert product in results
```

### Test Both Paths

```
# Test that library works without framework
def test_no_framework():
    # Ensure framework not loaded
    assert 'django' not in sys.modules

    # Library still works
    client = Client()
    assert client.ping() == "pong"
```

## Common Integration Points

### Web Frameworks

```
Middleware:
  - Request/response processing
  - Authentication hooks
  - Error handling

Configuration:
  - Settings integration
  - Environment loading

Models:
  - ORM hooks
  - Query extensions
  - Lifecycle callbacks
```

### Background Jobs

```
Job Frameworks:
  - Celery (Python)
  - Sidekiq (Ruby)
  - Bull (Node.js)

Integration:
  - Job registration
  - Queue configuration
  - Retry handling
```

### Logging

```
Framework Logging:
  - Use framework's logger if available
  - Fall back to standard logging
  - Configurable log level

MyLib.logger = framework.get_logger('mylib')
# Or
MyLib.logger = logging.getLogger('mylib')
```

## Version Compatibility

### Support Multiple Framework Versions

```
# Check framework version
framework_version = get_framework_version()

if framework_version >= (4, 0):
    use_new_api()
else:
    use_legacy_api()
```

### Graceful Degradation

```
try:
    # Try new framework feature
    framework.new_feature()
except AttributeError:
    # Fall back to old way
    framework.old_way()
```

## Documentation

### Document Framework-Specific Setup

```
README.md:
  ## Installation

  pip install mylib

  ## Django Integration

  1. Add to INSTALLED_APPS
  2. Configure settings
  3. Run migrations

  ## Flask Integration

  1. Initialize with app
  2. Configure

  ## Standalone Usage

  Works without any framework...
```
