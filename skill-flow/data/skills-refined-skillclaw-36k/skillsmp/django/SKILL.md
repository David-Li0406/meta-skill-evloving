---
name: django
description: Django documentation optimized for AI coding agents
---

# Django Skill

Django documentation optimized for ai coding agents, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- Working with django
- Asking about django features or APIs
- Implementing django solutions
- Debugging django code
- Learning django best practices

## Quick Reference

### Common Patterns

**Pattern 1:** For example, if we reverse the order of the values() and annotate() clause from our previous example:

```
values()
```

**Pattern 2:** Take the following example:

```
>>> from django.db.models import F, Count, Greatest
>>> Book.objects.values(greatest_pages=Greatest("pages", 600)).annotate(
...     num_authors=Count("authors"),
...     pages_per_author=F("greatest_pages") / F("num_authors"),
... ).aggregate(Avg("pages_per_author"))
```

**Pattern 3:** If you want to call a part of Django that is still synchronous, you will need to wrap it in a sync_to_async() call

```
sync_to_async()
```

**Pattern 4:** For example:

```
from django.views.decorators.cache import never_cache


@never_cache
def my_sync_view(request): ...


@never_cache
async def my_async_view(request): ...
```

**Pattern 5:** The default is DEFERRED

```
DEFERRED
```

**Pattern 6:** Consider, for example, that you need to change a single database feature

```
base
```

**Pattern 7:** When creating objects, where possible, use the bulk_create() method to reduce the number of SQL queries

```
bulk_create()
```

**Pattern 8:** The following example:

```
entries[0].headline = "This is not a test"
entries[1].headline = "This is no longer a test"
Entry.objects.bulk_update(entries, ["headline"])
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **howto.md** - Howto documentation
- **http.md** - Http documentation
- **models.md** - Models documentation
- **ref.md** - Ref documentation
- **topics.md** - Topics documentation

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
Start with the getting_started or tutorials reference files for foundational concepts.

### For Specific Features
Use the appropriate category reference file (api, guides, etc.) for detailed information.

### For Code Examples
The quick reference section above contains common patterns extracted from the official docs.

## Resources

### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

### scripts/
Add helper scripts here for common automation tasks.

### assets/
Add templates, boilerplate, or example projects here.

## Notes

- This skill was automatically generated from official documentation
- Reference files preserve the structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference patterns are extracted from common usage examples in the docs

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
