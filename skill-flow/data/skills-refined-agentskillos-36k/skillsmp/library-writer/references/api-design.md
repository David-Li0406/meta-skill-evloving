# API Design

How to design clean, intuitive public interfaces for libraries.

## Core Principles

### Simple Things Should Be Simple

```
Good:
  # One line to get started
  client = MyLib.Client()
  result = client.fetch("data")

Bad:
  # Five steps before you can do anything
  config = MyLib.Config.create()
  config.validate()
  factory = MyLib.ClientFactory(config)
  client = factory.build()
  result = client.fetch("data")
```

### Progressive Disclosure

```
# Level 1: Basic usage (most users)
client = Client()
result = client.search("query")

# Level 2: Configuration (some users)
client = Client(timeout=60, retries=3)
result = client.search("query", limit=10)

# Level 3: Advanced (few users)
client = Client(
    timeout=60,
    retries=3,
    transport=CustomTransport(),
    serializer=CustomSerializer()
)
```

### Consistent Patterns

```
Good:
  # Same pattern throughout
  users.find(id)
  posts.find(id)
  comments.find(id)

Bad:
  # Different patterns for same operation
  users.find(id)
  posts.get_by_id(id)
  comments.fetch(comment_id=id)
```

## Naming Conventions

### Methods

```
Actions (verbs):
  client.connect()
  client.disconnect()
  client.fetch()
  client.send()

Queries (verbs that return):
  client.find(id)
  client.search(query)
  client.count()
  client.exists?(id)

Predicates (booleans):
  client.connected?
  client.valid?
  client.empty?
```

### Parameters

```
Good:
  def search(query, limit=10, offset=0):
  def connect(host, port=5432, timeout=30):

Bad:
  def search(q, l=10, o=0):  # Cryptic
  def connect(h, p=5432, t=30):  # Unclear
```

### Classes

```
Good:
  Client        # Main interface
  Config        # Configuration
  Response      # API response
  Error         # Base error

Bad:
  ClientManager         # Manager of what?
  ConfigurationHelper   # Helper how?
  ResponseHandler       # Handles how?
```

## Configuration API

### Simple Accessors

```
# Module-level configuration
MyLib.api_key = "secret"
MyLib.timeout = 30
MyLib.debug = True

# Or instance configuration
client = Client(api_key="secret", timeout=30)
```

### Environment Variables

```
# Automatic environment loading
api_key = os.environ.get("MYLIB_API_KEY")

# Clear naming convention
MYLIB_API_KEY
MYLIB_TIMEOUT
MYLIB_DEBUG
```

### Configuration Validation

```
def api_key=(value):
    if not value or len(value) != 32:
        raise ConfigError(
            "API key must be 32 characters. "
            "Get your key at https://mylib.com/api-keys"
        )
    _api_key = value
```

## Class Macro Pattern

### Single Configuration Method

The signature pattern for libraries that enhance classes:

```
# Usage - one method does everything
class Product:
    searchable(fields=['name', 'description'])

# Implementation
def searchable(**options):
    # Validate options
    unknown = set(options.keys()) - KNOWN_OPTIONS
    if unknown:
        raise ArgumentError(f"Unknown options: {unknown}")

    # Store configuration
    class_config[caller_class] = options

    # Add methods
    add_instance_methods(caller_class)
    add_class_methods(caller_class)
```

### Option Validation

```
KNOWN_OPTIONS = {'fields', 'index_name', 'callbacks'}

def searchable(**options):
    # Fail fast on unknown options
    unknown = set(options.keys()) - KNOWN_OPTIONS
    if unknown:
        raise ArgumentError(
            f"Unknown options: {unknown}. "
            f"Valid options: {KNOWN_OPTIONS}"
        )
```

### Method Addition

```
def add_search_methods(klass):
    # Instance method
    def search_data(self):
        return extract_searchable_fields(self)
    klass.search_data = search_data

    # Class method
    def search(cls, query):
        return search_index.query(cls, query)
    klass.search = classmethod(search)
```

## Error Design

### Error Hierarchy

```
class Error(Exception):
    """Base error for all library errors"""
    pass

class ConfigError(Error):
    """Configuration problems"""
    pass

class ValidationError(Error):
    """Invalid input"""
    pass

class ConnectionError(Error):
    """Network/connection problems"""
    pass
```

### Informative Messages

```
Good:
  raise ConfigError(
      f"API key must be 32 characters, got {len(key)}. "
      f"Get your key at https://mylib.com/api-keys"
  )

Bad:
  raise ConfigError("Invalid API key")
```

### Error Context

```
class APIError(Error):
    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response

# Usage
try:
    client.fetch()
except APIError as e:
    print(f"Status: {e.status_code}")
    print(f"Response: {e.response}")
```

## Return Values

### Consistent Return Types

```
Good:
  # Always returns same type
  def find(id):
      return object or None

  def search(query):
      return list (possibly empty)

Bad:
  # Returns different types
  def find(id):
      return object or False or None or raises
```

### Return Objects, Not Tuples

```
Good:
  result = client.fetch()
  print(result.data)
  print(result.metadata)

Bad:
  data, metadata, status = client.fetch()
  # Easy to mix up order
```

### Named Results

```
# For complex return values
@dataclass
class SearchResult:
    items: list
    total: int
    page: int
    has_more: bool

def search(query):
    return SearchResult(
        items=results,
        total=count,
        page=1,
        has_more=count > len(results)
    )
```

## Method Signatures

### Required vs Optional Parameters

```
# Required parameters are positional
def connect(host, port):
    pass

# Optional parameters have defaults
def connect(host, port=5432, timeout=30):
    pass

# Many options use keyword-only
def search(query, *, limit=10, offset=0, sort=None):
    pass
```

### Avoid Boolean Parameters

```
Bad:
  fetch(include_metadata=True, raw=False)
  # What do True/False mean at call site?
  fetch(True, False)

Good:
  fetch(format='json', include=['metadata'])
  # Clear what each parameter means
```

### Limit Parameters

```
Good:
  # Few, focused parameters
  def search(query, limit=10):
      pass

Bad:
  # Too many parameters
  def search(query, limit, offset, sort, order,
             include_deleted, include_drafts,
             filter_by, group_by, ...):
      pass
  # Use options object instead
```

## Versioning

### Semantic Versioning

```
MAJOR.MINOR.PATCH

MAJOR: Breaking changes
MINOR: New features (backward compatible)
PATCH: Bug fixes (backward compatible)
```

### Deprecation Warnings

```
def old_method():
    warnings.warn(
        "old_method is deprecated, use new_method instead. "
        "Will be removed in version 2.0.",
        DeprecationWarning
    )
    return new_method()
```

### Backward Compatibility

```
# Keep old name as alias
new_method = improved_method
old_method = new_method  # Deprecated alias

# Or wrapper with warning
def old_method(*args, **kwargs):
    warn_deprecated("old_method", "new_method")
    return new_method(*args, **kwargs)
```

## Documentation

### Docstrings

```
def search(query, limit=10):
    """
    Search the index for matching documents.

    Args:
        query: Search query string
        limit: Maximum results to return (default: 10)

    Returns:
        List of matching documents

    Raises:
        ValidationError: If query is empty
        ConnectionError: If search service unavailable

    Example:
        >>> client.search("python")
        [Document(id=1, title="Python Guide"), ...]
    """
```

### Type Hints

```
from typing import Optional, List

def search(
    query: str,
    limit: int = 10,
    offset: int = 0
) -> List[Document]:
    """Search for documents."""
    pass

def find(id: str) -> Optional[Document]:
    """Find document by ID, returns None if not found."""
    pass
```
