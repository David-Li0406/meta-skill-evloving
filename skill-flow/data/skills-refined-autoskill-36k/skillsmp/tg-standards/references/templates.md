# Template Patterns

## Template Tags

```html
{% load sanitize_text dots %}
{{ rating|dots }}       {# ●●●○○ (auto 5 or 10 max) #}
{{ rating|dots:10 }}    {# explicit max 10 #}
{{ value|boxes }}       {# ■■■□□ for temp values #}
{{ content|sanitize_html|linebreaks }}
```

## Always Use TG Components

| Use | NOT |
|-----|-----|
| `tg-card` | `card` |
| `tg-card-header` | `card-header` |
| `tg-card-body` | `card-body` |
| `tg-btn` | `btn` |
| `tg-badge` | `badge` |
| `tg-table` | `table` |

## Page Header Card

```html
<div class="tg-card header-card mb-4" data-gameline="{{ object.gameline|lower }}">
    <div class="tg-card-header">
        <h1 class="tg-card-title {{ object.get_heading }}">{{ object.name }}</h1>
        <p class="tg-card-subtitle mb-0">{{ object.concept }}</p>
    </div>
</div>
```

## Section Card

```html
<div class="tg-card">
    <div class="tg-card-header text-center">
        <h5 class="tg-card-title {{ object.get_heading }}">Section Title</h5>
    </div>
    <div class="tg-card-body text-center" style="padding: 20px;">
        <!-- Content -->
    </div>
</div>
```

## Stat Displays

### Inline Stat Box (Label Beside Value)
```html
<div style="display: inline-block; padding: 10px 24px; border-radius: 6px; background-color: rgba(0,0,0,0.05);">
    <span style="font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--theme-text-secondary); margin-right: 8px;">Label:</span>
    <span style="font-weight: 700; color: var(--theme-text-primary);">{{ value }}</span>
</div>
```

### Large Stat Display (Label Below Value)
```html
<div style="padding: 12px; border-radius: 6px; background-color: rgba(0,0,0,0.02);">
    <div style="font-size: 1.5rem; font-weight: 700; color: var(--theme-text-primary); margin-bottom: 4px;">{{ value }}</div>
    <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; color: var(--theme-text-secondary);">Label</div>
</div>
```

### Dots Row (Advantages)
```html
<div class="row mb-2 text-center">
    <div class="col-3" style="font-weight: 600; color: var(--theme-text-secondary);">Willpower:</div>
    <div class="col-3 dots">{{ object.willpower|dots:10 }}</div>
    <div class="col-3" style="font-weight: 600; color: var(--theme-text-secondary);">Temp:</div>
    <div class="col-3 dots">{{ object.temporary_willpower|boxes:10 }}</div>
</div>
```

## Boolean Features Grid

```html
<div class="col-6 mb-2">
    <div style="padding: 8px; border-radius: 4px; background-color: {{ object.feature|yesno:'rgba(0,255,0,0.1),rgba(0,0,0,0.02)' }};">
        <div style="font-size: 0.7rem; font-weight: 600; text-transform: uppercase; color: var(--theme-text-secondary); margin-bottom: 2px;">Feature</div>
        <div style="font-weight: 700; color: var(--theme-text-primary);">{{ object.feature|yesno:"Yes,No" }}</div>
    </div>
</div>
```

## Card Grid for Related Items

```html
<div class="row">
    {% for item in items %}
        <div class="col-sm-6 col-md-4 col-lg-3 mb-3">
            <div class="tg-card h-100">
                <div class="tg-card-body text-center" style="padding: 16px;">
                    <div class="mb-2">
                        <a href="{{ item.get_absolute_url }}" style="font-weight: 600; font-size: 0.875rem; color: var(--theme-text-primary);">{{ item.name }}</a>
                    </div>
                    <div class="dots" style="font-size: 0.875rem;">{{ item.rating|dots }}</div>
                </div>
            </div>
        </div>
    {% endfor %}
</div>
```

## Status Badge

```html
<span class="tg-badge badge-{{ object.status|lower }}">{{ object.get_status_display }}</span>
```

## List Template

```html
{% extends "core/base.html" %}
{% block content %}
<div class="container mt-4">
    <div class="tg-card">
        <div class="tg-card-header d-flex justify-content-between align-items-center">
            <h4 class="tg-card-title mb-0">{{ model_name_plural }}</h4>
            {% if user.profile.is_st %}
            <a href="{% url 'app:gameline:create:model_name' %}" class="btn btn-primary btn-sm">Create New</a>
            {% endif %}
        </div>
        <div class="tg-card-body">
            <table class="tg-table">
                <thead><tr><th>Name</th><th>Owner</th><th>Status</th></tr></thead>
                <tbody>
                    {% for obj in objects %}
                    <tr>
                        <td><a href="{{ obj.get_absolute_url }}">{{ obj.name }}</a></td>
                        <td>{{ obj.owner.username }}</td>
                        <td><span class="tg-badge badge-{{ obj.status|lower }}">{{ obj.get_status_display }}</span></td>
                    </tr>
                    {% empty %}
                    <tr><td colspan="3" class="text-center">No items found.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
```

## Style Rules

### Typography
- Labels: `font-weight: 600; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; color: var(--theme-text-secondary);`
- Values: `font-weight: 700; color: var(--theme-text-primary);`

### Spacing
- Card body: `padding: 20px;` (standard) or `padding: 24px;` (spacious)
- Section gaps: `mb-4` or `mb-5`
- Related items: `mb-3`

### Responsive Columns
- Two-column: `col-md-6`
- Three-column: `col-md-4`
- Card grid: `col-sm-6 col-md-4 col-lg-3`
- Equal height: add `h-100` to cards
