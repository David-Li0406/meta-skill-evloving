# Deferred Loading

> **Definition**: A performance optimization pattern that postpones the initialization, loading, or execution of resources until they are actually needed, reducing startup time and memory consumption.

**Navigation**: [← Dynamic Manifests](./dynamic-manifests.md) | [↑ Best Practices](../SKILL.md) | [← Progressive Disclosure](./progressive-disclosure.md)

---

## Table of Contents

- [What Is It?](#what-is-it) ← Start here
- [Why Defer?](#why-defer)
- [Basic Patterns](#basic-patterns) ← Quick implementation
- [Strategies](#strategies) ← For practitioners
- [Lazy Initialization](#lazy-initialization)
- [Advanced Techniques](#advanced-techniques) ← For architects
- [MCP Skills Implementation](#mcp-skills-implementation)
- [Performance Optimization](#performance-optimization)

---

## What Is It?

Deferred loading delays resource initialization until first use.

### Visual Comparison

```
EAGER LOADING (Traditional)
─────────────────────────────────────
App Starts
  ↓
Load Module A ──────── 2s
Load Module B ──────── 3s
Load Module C ──────── 2s
Load Module D ──────── 1s
Load Module E ──────── 2s
  ↓
App Ready ──────────── 10s total
Memory: 500 MB

User uses Module A only
  → Modules B, C, D, E wasted startup time


DEFERRED LOADING (Optimized)
─────────────────────────────────────
App Starts
  ↓
Minimal Initialization ── 0.5s
  ↓
App Ready ──────────── 0.5s total
Memory: 50 MB

User requests Module A
  ↓
Load Module A ──────── 2s
Use Module A
Memory: 150 MB

(Modules B, C, D, E never loaded!)
```

### Key Metrics

| Metric | Eager Loading | Deferred Loading | Improvement |
|--------|---------------|------------------|-------------|
| **Startup Time** | 10s | 0.5s | **95% faster** |
| **Initial Memory** | 500 MB | 50 MB | **90% less** |
| **Time to First Use** | 10s | 2.5s | **75% faster** |
| **Unused Resource Waste** | High | Zero | **100% efficient** |

---

## Why Defer?

### Problem 1: Slow Startup

```python
# BAD: Load everything at startup
import heavy_ml_library      # 5 seconds
import video_processing      # 3 seconds
import blockchain_tools      # 4 seconds
import data_analysis         # 2 seconds

# User wants to do simple text search...
# But waited 14 seconds for unused features!
```

### Problem 2: Memory Waste

```javascript
// BAD: Initialize all components
const videoEditor = new VideoEditor();        // 200 MB
const imageProcessor = new ImageProcessor();  // 150 MB
const audioMixer = new AudioMixer();          // 100 MB

// User only uses text editor
// But 450 MB wasted on unused features!
```

### Problem 3: Unused Resources

```java
// BAD: Connect to all services at startup
DatabaseConnection db = new DatabaseConnection();
CacheService cache = new CacheService();
PaymentGateway payments = new PaymentGateway();
EmailService email = new EmailService();
AnalyticsService analytics = new AnalyticsService();

// User views read-only content
// But connected to write services unnecessarily!
```

### The Solution

**Defer everything non-essential**:
- ✅ Fast startup
- ✅ Low memory footprint
- ✅ Load only what's used
- ✅ Better resource utilization

---

## Basic Patterns

### Pattern 1: Lazy Import (Python)

**Bad: Eager Import**
```python
# At module level - loads immediately
import pandas as pd
import numpy as np
import tensorflow as tf

def analyze_data(data):
    df = pd.DataFrame(data)
    return df.describe()
```

**Good: Deferred Import**
```python
# No imports at module level

def analyze_data(data):
    # Import only when function is called
    import pandas as pd
    df = pd.DataFrame(data)
    return df.describe()
```

**Even Better: Cached Lazy Import**
```python
_pandas = None

def get_pandas():
    global _pandas
    if _pandas is None:
        import pandas as pd
        _pandas = pd
    return _pandas

def analyze_data(data):
    pd = get_pandas()  # First call imports, subsequent calls use cache
    df = pd.DataFrame(data)
    return df.describe()
```

### Pattern 2: Lazy Initialization (JavaScript)

**Bad: Eager Initialization**
```javascript
class DataService {
    constructor() {
        // Initialize immediately
        this.database = new DatabaseConnection();
        this.cache = new CacheLayer();
        this.validator = new DataValidator();
    }
}

// Even if never used, all initialized!
const service = new DataService();
```

**Good: Deferred Initialization**
```javascript
class DataService {
    constructor() {
        // Don't initialize anything yet
        this._database = null;
        this._cache = null;
        this._validator = null;
    }

    get database() {
        // Initialize on first access
        if (!this._database) {
            this._database = new DatabaseConnection();
        }
        return this._database;
    }

    get cache() {
        if (!this._cache) {
            this._cache = new CacheLayer();
        }
        return this._cache;
    }

    get validator() {
        if (!this._validator) {
            this._validator = new DataValidator();
        }
        return this._validator;
    }
}

const service = new DataService();  // Fast, nothing initialized
service.database.query(...);         // Now database is initialized
```

### Pattern 3: Function Decorators (Python)

**Decorator for Lazy Loading**
```python
from functools import wraps

def lazy_load(loader_func):
    """Decorator that defers execution until first call"""
    _cached = None

    @wraps(loader_func)
    def wrapper(*args, **kwargs):
        nonlocal _cached
        if _cached is None:
            _cached = loader_func(*args, **kwargs)
        return _cached

    return wrapper

# Usage
@lazy_load
def load_ml_model():
    print("Loading ML model...")  # Only prints once
    import tensorflow as tf
    return tf.keras.models.load_model('model.h5')

# First call: loads model
model = load_ml_model()

# Subsequent calls: returns cached model
model = load_ml_model()  # Instant, uses cache
```

---

## Strategies

### Strategy 1: Tiered Loading

Load resources in priority order:

```python
class Application:
    def __init__(self):
        # Tier 1: Critical (load immediately)
        self.config = load_config()
        self.logger = setup_logging()

        # Tier 2: Important (load after startup)
        self._core_modules = None

        # Tier 3: Optional (load on demand)
        self._advanced_features = {}

    async def start(self):
        """Fast startup - only Tier 1"""
        print("App ready!")

        # Tier 2: Load in background
        asyncio.create_task(self._load_core_modules())

    async def _load_core_modules(self):
        """Load Tier 2 in background"""
        await asyncio.sleep(0)  # Yield to event loop
        self._core_modules = load_core_modules()

    def get_feature(self, feature_name):
        """Tier 3: Load on explicit request"""
        if feature_name not in self._advanced_features:
            self._advanced_features[feature_name] = load_feature(feature_name)
        return self._advanced_features[feature_name]
```

### Strategy 2: Dependency-Based Loading

Load dependencies only when needed:

```python
class SkillManager:
    def __init__(self):
        self.skills = {}
        self.skill_dependencies = {
            'data_analysis': ['pandas', 'numpy'],
            'ml_training': ['tensorflow', 'scikit-learn'],
            'web_scraping': ['requests', 'beautifulsoup4']
        }

    def load_skill(self, skill_name):
        """Load skill and its dependencies on demand"""
        if skill_name in self.skills:
            return self.skills[skill_name]

        # Load dependencies first
        deps = self.skill_dependencies.get(skill_name, [])
        for dep in deps:
            self._ensure_dependency(dep)

        # Load skill
        skill = self._import_skill(skill_name)
        self.skills[skill_name] = skill
        return skill

    def _ensure_dependency(self, dep_name):
        """Lazy load dependency"""
        if dep_name not in sys.modules:
            __import__(dep_name)

    def _import_skill(self, skill_name):
        """Dynamically import skill module"""
        module = __import__(f'skills.{skill_name}', fromlist=['Skill'])
        return module.Skill()
```

### Strategy 3: Code Splitting (JavaScript)

Split code into chunks loaded on demand:

```javascript
// main.js - Always loaded
import { setupApp } from './core.js';

setupApp();

// Features loaded on demand
async function enableAdvancedMode() {
    // Dynamic import - only loads when called
    const { AdvancedFeatures } = await import('./advanced.js');
    return new AdvancedFeatures();
}

async function startVideoEditing() {
    // Large dependency loaded only when needed
    const { VideoEditor } = await import('./video-editor.js');
    return new VideoEditor();
}

// User clicks "Advanced Mode"
button.onclick = async () => {
    const features = await enableAdvancedMode();
    features.activate();
};
```

### Strategy 4: Resource Pooling

Reuse loaded resources efficiently:

```python
from typing import Dict, Optional
import weakref

class ResourcePool:
    """Pool of lazily-loaded resources with weak references"""

    def __init__(self):
        self._resources: Dict[str, weakref.ref] = {}
        self._loaders: Dict[str, callable] = {}

    def register(self, name: str, loader: callable):
        """Register a resource loader"""
        self._loaders[name] = loader

    def get(self, name: str):
        """Get resource, loading if necessary"""
        # Check if already loaded
        if name in self._resources:
            resource = self._resources[name]()
            if resource is not None:
                return resource

        # Load resource
        if name not in self._loaders:
            raise ValueError(f"No loader for {name}")

        resource = self._loaders[name]()

        # Store weak reference (allows garbage collection)
        self._resources[name] = weakref.ref(resource)

        return resource

# Usage
pool = ResourcePool()
pool.register('ml_model', lambda: load_ml_model())
pool.register('database', lambda: DatabaseConnection())

# First call: loads
model = pool.get('ml_model')

# Second call: reuses if still in memory
model = pool.get('ml_model')

# If garbage collected, reloads automatically
```

---

## Lazy Initialization

### Pattern: Singleton with Lazy Loading

```python
class Singleton:
    _instance = None

    def __new__(cls):
        # Lazy initialization: create only on first access
        if cls._instance is None:
            print("Creating singleton instance...")
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Heavy initialization deferred until first use"""
        self.data = self._load_heavy_data()
        self.connection = self._establish_connection()

    def _load_heavy_data(self):
        print("Loading heavy data...")
        return [...]  # Expensive operation

    def _establish_connection(self):
        print("Establishing connection...")
        return Connection()  # Expensive operation

# First call: initializes
instance1 = Singleton()  # Prints: Creating singleton instance...

# Subsequent calls: reuses
instance2 = Singleton()  # No output, instant
```

### Pattern: Lazy Properties

```python
class LazyProperty:
    """Descriptor for lazy property loading"""

    def __init__(self, func):
        self.func = func
        self.attr_name = f'_lazy_{func.__name__}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self

        # Check if already loaded
        if not hasattr(obj, self.attr_name):
            # Load and cache
            value = self.func(obj)
            setattr(obj, self.attr_name, value)

        return getattr(obj, self.attr_name)

class DataProcessor:
    @LazyProperty
    def expensive_resource(self):
        """Only loaded on first access"""
        print("Loading expensive resource...")
        return load_expensive_resource()

    @LazyProperty
    def ml_model(self):
        """Only loaded on first access"""
        print("Loading ML model...")
        return load_ml_model()

# Usage
processor = DataProcessor()  # Fast, nothing loaded

# First access: loads
resource = processor.expensive_resource  # Prints: Loading expensive resource...

# Second access: cached
resource = processor.expensive_resource  # No output, instant

# ML model not accessed = never loaded
```

### Pattern: Lazy Collections

```python
class LazyList:
    """List that loads items on first access"""

    def __init__(self, loader_func):
        self._loader = loader_func
        self._items = None

    def _ensure_loaded(self):
        if self._items is None:
            print("Loading items...")
            self._items = self._loader()

    def __getitem__(self, index):
        self._ensure_loaded()
        return self._items[index]

    def __len__(self):
        self._ensure_loaded()
        return len(self._items)

    def __iter__(self):
        self._ensure_loaded()
        return iter(self._items)

# Usage
def load_large_dataset():
    print("Expensive database query...")
    return [1, 2, 3, 4, 5]

lazy_data = LazyList(load_large_dataset)  # Fast, nothing loaded

# First access triggers load
print(lazy_data[0])  # Prints: Loading items... then 1

# Subsequent access uses cache
print(lazy_data[1])  # Prints: 2 (no loading message)
```

---

## Advanced Techniques

### Technique 1: Asynchronous Lazy Loading

Load resources in background without blocking:

```python
import asyncio
from typing import Optional

class AsyncLazyLoader:
    def __init__(self, loader_coro):
        self._loader = loader_coro
        self._value: Optional[any] = None
        self._loading_task: Optional[asyncio.Task] = None

    async def get(self):
        """Get value, loading if necessary"""
        # Already loaded?
        if self._value is not None:
            return self._value

        # Already loading?
        if self._loading_task is not None:
            return await self._loading_task

        # Start loading
        self._loading_task = asyncio.create_task(self._load())
        return await self._loading_task

    async def _load(self):
        """Perform the actual loading"""
        print("Loading resource...")
        self._value = await self._loader()
        return self._value

# Usage
async def load_api_data():
    await asyncio.sleep(2)  # Simulate slow API
    return {"data": "loaded"}

loader = AsyncLazyLoader(load_api_data())

# Multiple concurrent calls share same load
results = await asyncio.gather(
    loader.get(),  # Starts loading
    loader.get(),  # Waits for same load
    loader.get()   # Waits for same load
)
# Only loads once!
```

### Technique 2: Preemptive Loading

Start loading before needed, based on predictions:

```python
class PreemptiveLoader:
    def __init__(self):
        self._cache = {}
        self._loading = {}

    def preload(self, resource_name, loader_func):
        """Start loading in background"""
        if resource_name not in self._cache and resource_name not in self._loading:
            self._loading[resource_name] = asyncio.create_task(
                self._load_resource(resource_name, loader_func)
            )

    async def _load_resource(self, name, loader):
        """Background loading"""
        self._cache[name] = await loader()
        del self._loading[name]

    async def get(self, resource_name, loader_func):
        """Get resource (may already be loaded!)"""
        # Already cached?
        if resource_name in self._cache:
            return self._cache[resource_name]

        # Currently loading?
        if resource_name in self._loading:
            await self._loading[resource_name]
            return self._cache[resource_name]

        # Start loading now
        self._cache[resource_name] = await loader_func()
        return self._cache[resource_name]

# Usage
loader = PreemptiveLoader()

# User hovers over "Advanced Features" button
# Predict they might click, start loading
loader.preload('advanced_features', load_advanced_features)

# User clicks button
# Already loaded (or nearly done)!
features = await loader.get('advanced_features', load_advanced_features)
```

### Technique 3: Conditional Loading with Context

Load different resources based on context:

```python
class ContextAwareLoader:
    def __init__(self):
        self._loaded_modules = {}

    def load_for_context(self, context):
        """Load only modules needed for this context"""
        required_modules = self._determine_required_modules(context)

        loaded = {}
        for module_name in required_modules:
            loaded[module_name] = self._get_or_load(module_name)

        return loaded

    def _determine_required_modules(self, context):
        """Figure out what's needed"""
        modules = ['core']  # Always needed

        if context.language == 'python':
            modules.extend(['python_linter', 'python_formatter'])

        if context.has_tests:
            modules.append('test_runner')

        if context.is_web_project:
            modules.extend(['http_server', 'browser_tools'])

        return modules

    def _get_or_load(self, module_name):
        """Lazy load with caching"""
        if module_name not in self._loaded_modules:
            print(f"Loading {module_name}...")
            self._loaded_modules[module_name] = self._import_module(module_name)
        return self._loaded_modules[module_name]

# Usage
loader = ContextAwareLoader()

# Python project: loads Python-specific tools
context = Context(language='python', has_tests=True)
modules = loader.load_for_context(context)
# Loads: core, python_linter, python_formatter, test_runner

# JavaScript project: different tools
context = Context(language='javascript', is_web_project=True)
modules = loader.load_for_context(context)
# Loads: core, http_server, browser_tools
```

### Technique 4: Priority-Based Loading

Load resources by priority, deferring low-priority items:

```python
import asyncio
from enum import Enum

class Priority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

class PriorityLoader:
    def __init__(self):
        self._resources = {}
        self._load_queue = {p: [] for p in Priority}

    def register(self, name, loader, priority=Priority.MEDIUM):
        """Register a resource to load"""
        self._load_queue[priority].append((name, loader))

    async def load_by_priority(self):
        """Load resources in priority order"""
        for priority in Priority:
            tasks = []
            for name, loader in self._load_queue[priority]:
                tasks.append(self._load_resource(name, loader))

            # Load all items at this priority level
            await asyncio.gather(*tasks)

            # Yield to event loop between priority levels
            await asyncio.sleep(0)

    async def _load_resource(self, name, loader):
        """Load a single resource"""
        print(f"Loading {name}...")
        self._resources[name] = await loader()

# Usage
loader = PriorityLoader()

# Register resources with priorities
loader.register('config', load_config, Priority.CRITICAL)
loader.register('logger', setup_logging, Priority.CRITICAL)
loader.register('database', connect_db, Priority.HIGH)
loader.register('cache', setup_cache, Priority.HIGH)
loader.register('analytics', init_analytics, Priority.LOW)
loader.register('ml_model', load_ml_model, Priority.LOW)

# Load in priority order
await loader.load_by_priority()
# Order: config, logger (critical) → database, cache (high) → analytics, ml_model (low)
```

---

## MCP Skills Implementation

### Pattern: Lazy MCP Skill Loading

```python
class MCPSkillManager:
    """Lazy loading manager for MCP skills"""

    def __init__(self):
        self._skills = {}
        self._skill_metadata = self._scan_available_skills()

    def _scan_available_skills(self):
        """Quick scan: only read metadata, don't load skills"""
        metadata = {}

        for skill_file in Path('skills').glob('*.md'):
            # Parse YAML frontmatter only (fast)
            meta = self._parse_frontmatter(skill_file)
            metadata[meta['name']] = {
                'file': skill_file,
                'triggers': meta.get('triggers', []),
                'description': meta.get('description', '')
            }

        return metadata

    def get_skill(self, skill_name):
        """Get skill, loading on first access"""
        # Already loaded?
        if skill_name in self._skills:
            return self._skills[skill_name]

        # Load now
        if skill_name not in self._skill_metadata:
            raise ValueError(f"Skill {skill_name} not found")

        skill = self._load_skill(skill_name)
        self._skills[skill_name] = skill
        return skill

    def _load_skill(self, skill_name):
        """Actually load the skill (expensive)"""
        meta = self._skill_metadata[skill_name]
        skill_file = meta['file']

        print(f"Loading skill: {skill_name}")

        # Read full content
        content = skill_file.read_text()

        # Initialize skill
        return Skill(name=skill_name, content=content, metadata=meta)

    def find_skills_for_trigger(self, trigger):
        """Find skills that match trigger (no loading!)"""
        matches = []

        for name, meta in self._skill_metadata.items():
            if trigger in meta['triggers']:
                matches.append(name)

        return matches

# Usage
manager = MCPSkillManager()  # Fast, scans metadata only

# User types "debug"
matching_skills = manager.find_skills_for_trigger('debug')  # Fast, no loading
# Returns: ['python-debugger', 'javascript-debugger']

# User selects 'python-debugger'
skill = manager.get_skill('python-debugger')  # Loads now
skill.execute()
```

### Pattern: Progressive Skill Loading

```python
class ProgressiveSkillLoader:
    """Load skills progressively based on usage patterns"""

    def __init__(self):
        self.tier1_skills = []  # Always loaded
        self.tier2_skills = []  # Load after startup
        self.tier3_skills = []  # Load on demand

    async def initialize(self):
        """Fast startup with tiered loading"""
        # Tier 1: Essential skills (load immediately)
        self.tier1_skills = [
            await self._load_skill('basic-search'),
            await self._load_skill('file-operations')
        ]

        # Tier 2: Common skills (load in background)
        asyncio.create_task(self._load_tier2())

        # Tier 3: Specialized skills (load on request)
        # Not loaded yet!

    async def _load_tier2(self):
        """Background loading of common skills"""
        await asyncio.sleep(0)  # Yield to event loop

        self.tier2_skills = [
            await self._load_skill('git-operations'),
            await self._load_skill('code-analysis')
        ]

    async def get_skill(self, skill_name):
        """Get skill from appropriate tier"""
        # Check Tier 1
        for skill in self.tier1_skills:
            if skill.name == skill_name:
                return skill

        # Check Tier 2
        for skill in self.tier2_skills:
            if skill.name == skill_name:
                return skill

        # Tier 3: Load on demand
        skill = await self._load_skill(skill_name)
        self.tier3_skills.append(skill)
        return skill
```

---

## Performance Optimization

### Optimization 1: Memoization

Cache expensive computations:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_calculation(n):
    """Result cached automatically"""
    print(f"Computing for {n}...")
    # Expensive operation
    return n ** 2

# First call: computes
result = expensive_calculation(5)  # Prints: Computing for 5...

# Second call: cached
result = expensive_calculation(5)  # No output, instant
```

### Optimization 2: Time-Based Caching

Refresh cache periodically:

```python
from datetime import datetime, timedelta

class TimedCache:
    def __init__(self, loader_func, ttl_seconds=300):
        self.loader = loader_func
        self.ttl = timedelta(seconds=ttl_seconds)
        self._cached_value = None
        self._cached_time = None

    def get(self):
        """Get value, reloading if expired"""
        now = datetime.now()

        # Cache miss or expired?
        if (self._cached_value is None or
            self._cached_time is None or
            now - self._cached_time > self.ttl):

            print("Reloading from source...")
            self._cached_value = self.loader()
            self._cached_time = now

        return self._cached_value

# Usage
def load_api_data():
    return fetch_from_api()

cache = TimedCache(load_api_data, ttl_seconds=60)

# First call: loads
data = cache.get()  # Prints: Reloading from source...

# Within 60 seconds: cached
data = cache.get()  # No output

# After 60 seconds: reloads
data = cache.get()  # Prints: Reloading from source...
```

### Optimization 3: Load Monitoring

Track what gets loaded:

```python
class MonitoredLoader:
    def __init__(self):
        self._load_stats = {}

    def load(self, name, loader_func):
        """Load with performance monitoring"""
        import time

        start = time.time()
        result = loader_func()
        elapsed = time.time() - start

        # Record stats
        self._load_stats[name] = {
            'load_time': elapsed,
            'loaded_at': datetime.now(),
            'size': sys.getsizeof(result)
        }

        print(f"Loaded {name} in {elapsed:.2f}s ({self._load_stats[name]['size']} bytes)")

        return result

    def print_stats(self):
        """Show loading statistics"""
        print("\nLoad Statistics:")
        for name, stats in self._load_stats.items():
            print(f"  {name}: {stats['load_time']:.2f}s, {stats['size']} bytes")

# Usage
loader = MonitoredLoader()

ml_model = loader.load('ml_model', load_ml_model)
database = loader.load('database', connect_database)

loader.print_stats()
# Load Statistics:
#   ml_model: 3.45s, 524288 bytes
#   database: 0.12s, 1024 bytes
```

---

## Related Concepts

### Deferred Loading ← [Dynamic Manifests](./dynamic-manifests.md)

- Dynamic manifests: Tell you **what's available**
- Deferred loading: Determines **when to load**

Flow:
1. Dynamic manifest query: "These tools are available"
2. Deferred loading decision: "Don't load yet, wait for first use"
3. User requests tool
4. Deferred loading: "Now load the tool"

### Deferred Loading ← [Progressive Disclosure](./progressive-disclosure.md)

- Progressive disclosure: **What to show** to users
- Deferred loading: **When to initialize** resources

Example:
- Progressive disclosure: "Show basic features, hide advanced"
- Deferred loading: "Don't load advanced feature code until user accesses it"

Both patterns work together:
```
User opens app
  ↓
[Progressive Disclosure]
  → UI shows: Basic features only

[Deferred Loading]
  → Code loaded: Basic modules only

User clicks "Advanced"
  ↓
[Progressive Disclosure]
  → UI reveals: Advanced features

[Deferred Loading]
  → Code loads: Advanced modules (now)
```

---

## Summary

Deferred loading optimizes performance by:

1. **Lazy Initialization**: Create objects only when needed
2. **Tiered Loading**: Load critical resources first, others later
3. **Code Splitting**: Split code into chunks loaded on demand
4. **Caching**: Reuse loaded resources efficiently
5. **Monitoring**: Track what gets loaded and when

Key principle: **Don't pay for what you don't use**

---

**Navigation**: [← Dynamic Manifests](./dynamic-manifests.md) | [↑ Best Practices](../SKILL.md) | [← Progressive Disclosure](./progressive-disclosure.md)

**Last Updated**: 2025-10-20
