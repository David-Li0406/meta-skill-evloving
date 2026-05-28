# Django Template Rules

## CRITICAL: This Project Uses Django Templates, NOT Jinja2

```python
# Confirmed in settings/base.py
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        ...
    }
]
```

## Template File Structure

Every template file MUST follow this structure:

```django
{% extends "layouts/some_layout.html" %}  {# Line 1: extends MUST be first #}
{% load i18n static humanize %}           {# Line 2+: load tags #}
{% comment %}
    Optional: Template documentation
    - Context variables
    - Usage notes
{% endcomment %}

{% block content %}
    {# Template content here #}
{% endblock %}
```

## Comment Syntax

### Single-Line Comments

```django
{# This is a single-line comment - works correctly #}
<div class="content">
    {# Another comment #}
</div>
```

### Multi-Line Comments

```django
{# ❌ WRONG: This will render as visible text on the page! #}
{#
    This multi-line comment
    will appear on the page
    as plain text!
#}

{# ✅ CORRECT: Use {% comment %} tag for multi-line #}
{% comment %}
    This multi-line comment
    will NOT appear on the page.

    Use this for:
    - Template documentation
    - Temporarily disabling code blocks
    - Developer notes
{% endcomment %}
```

## Conditional Logic

### No Parentheses Allowed

Django templates do NOT support parentheses for grouping conditions.

```django
{# ❌ WRONG: Parentheses cause TemplateSyntaxError #}
{% if (status == 'active' or status == 'pending') and user.is_authenticated %}
    Content
{% endif %}

{# ✅ CORRECT: Use nested if statements #}
{% if user.is_authenticated %}
    {% if status == 'active' or status == 'pending' %}
        Content
    {% endif %}
{% endif %}
```

### Complex Logic Solutions

For complex conditions, compute in the view:

```python
# views.py
def my_view(request):
    context = {
        'is_actionable': (
            status in ['active', 'pending'] and
            request.user.is_authenticated
        ),
    }
    return render(request, 'template.html', context)
```

```django
{# template.html - simple condition #}
{% if is_actionable %}
    Content
{% endif %}
```

## Common Errors and Fixes

### Error: "extends must be the first tag"

```django
{# ❌ Causes error #}
{% comment %}Documentation{% endcomment %}
{% extends "base.html" %}

{# ✅ Fix: Move extends to line 1 #}
{% extends "base.html" %}
{% comment %}Documentation{% endcomment %}
```

### Error: "Could not parse the remainder"

```django
{# ❌ Causes error - parentheses not allowed #}
{% if (a or b) %}

{# ✅ Fix: Remove parentheses #}
{% if a or b %}
```

### Error: "VariableDoesNotExist"

Check that the variable name matches the model field exactly:

```python
# Model has 'verification_status'
class Submission(models.Model):
    verification_status = models.CharField(...)
```

```django
{# ❌ Wrong field name #}
{% if submission.status == 'verified' %}

{# ✅ Correct field name #}
{% if submission.verification_status == 'verified' %}
```

### Error: Comment text appearing on page

```django
{# ❌ Multi-line {# #} renders as text #}
{#
    This shows on page!
#}

{# ✅ Use {% comment %} for multi-line #}
{% comment %}
    This is hidden
{% endcomment %}
```

## Template Tag Quick Reference

| Tag | Purpose | Must Be First? |
|-----|---------|----------------|
| `{% extends %}` | Inherit from parent | **YES** |
| `{% load %}` | Load tag library | No (after extends) |
| `{% block %}` | Define content block | No |
| `{% include %}` | Include template | No |
| `{% comment %}` | Multi-line comment | No |
| `{# #}` | Single-line comment | No |
| `{% if %}` | Conditional | No |
| `{% for %}` | Loop | No |
| `{% with %}` | Create local variable | No |
| `{% url %}` | Reverse URL | No |
| `{% static %}` | Static file path | No (needs `{% load static %}`) |
| `{% trans %}` | Translation | No (needs `{% load i18n %}`) |

## Filter Syntax

```django
{# Basic filter #}
{{ value|default:"N/A" }}

{# Chained filters #}
{{ text|truncatewords:30|safe }}

{# Filter with argument #}
{{ date|date:"Y-m-d" }}

{# ❌ WRONG: Space after pipe #}
{{ value| default:"N/A" }}

{# ❌ WRONG: Quotes around filter name #}
{{ value|"default":"N/A" }}
```

## Django vs Jinja2 Comparison

| Feature | Django | Jinja2 |
|---------|--------|--------|
| extends position | Must be first tag | Can be anywhere |
| Multi-line comment | `{% comment %}...{% endcomment %}` | `{# ... #}` |
| Condition grouping | Not supported | `(a or b) and c` |
| Calling functions | `{{ func }}` (no args) | `{{ func() }}` |
| Loop else | `{% empty %}` | `{% else %}` |
| Set variable | `{% with var=value %}` | `{% set var = value %}` |
| Include with context | `{% include "x.html" with y=z %}` | `{% include "x.html" %}` |

## Checklist Before Creating Templates

- [ ] `{% extends %}` is the FIRST line (if using inheritance)
- [ ] `{% load %}` tags come immediately after extends
- [ ] Multi-line comments use `{% comment %}...{% endcomment %}`
- [ ] No parentheses in `{% if %}` conditions
- [ ] Variable names match model field names exactly
- [ ] All translatable text wrapped in `{% trans %}` or `{% blocktrans %}`
- [ ] Required tag libraries are loaded (`{% load i18n static %}`)
