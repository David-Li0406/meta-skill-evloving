# Caching Patterns

## Cache Timeouts

```python
CACHE_TIMEOUT_SHORT = 60        # 1 minute
CACHE_TIMEOUT_MEDIUM = 300      # 5 minutes
CACHE_TIMEOUT_LONG = 900        # 15 minutes
CACHE_TIMEOUT_VERY_LONG = 3600  # 1 hour
```

## View-Level Caching

For static pages identical for all users:

```python
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

@method_decorator(cache_page(60 * 15), name='dispatch')
class MeritFlawListView(ListView):
    model = MeritFlaw
```

**Use for:** Reference data lists, public pages
**Don't use for:** User-specific pages, permission-gated content

## Manual Cache Access

```python
from django.core.cache import cache

cache.set('my_key', data, timeout=300)
data = cache.get('my_key', default=None)
cache.delete('my_key')
```

## Template Fragment Caching

```django
{% load cache %}
{% cache 900 character_details character.id %}
    <div class="character-details">{{ character.name }}</div>
{% endcache %}
```

## Cache Invalidation (On Model Save)

```python
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver([post_save, post_delete], sender=Character)
def invalidate_character_cache(sender, instance, **kwargs):
    cache.delete(f"tg:queryset:Character:id={instance.id}")
```

## What to Cache

| Content Type | Timeout | Example |
|-------------|---------|---------|
| Static reference | 15-60 min | Merit/flaw lists |
| Semi-static | 5-15 min | Character lists |
| News/updates | 1-5 min | Home page |
| Real-time | Don't cache | Chat, notifications |

## Configuration

### Development (LocMemCache)
```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}
```

### Production (Redis)
```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL"),
    }
}
```
