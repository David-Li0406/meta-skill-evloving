# Authentik Template Variables

Authentik uses Django template syntax for email templates. Per the official documentation at https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/email/

## Required Template Loading

All templates must load the i18n module for internationalization:

```django
{% load i18n %}
```

For templates using time formatting, also load humanize:

```django
{% load humanize %}
```

## Common Variables

### User Object
- `{{ user.username }}` - User's username (primary identifier)
- `{{ user.email }}` - User's email address
- `{{ user.uid }}` - User's unique identifier
- `{{ user.name }}` - User's display name (if set)

### Action Variables
- `{{ url }}` - The full URL for the user to click on
- `{{ expires }}` - Timestamp when the token expires (use with `naturaltime` filter)

## Using Variables with Internationalization

### Simple Translation
```django
<h1>{% trans 'Password Reset' %}</h1>
<p>{% trans 'Click the button below to reset your password.' %}</p>
```

### Translation with Variables
Use `blocktrans` for strings containing variables:

```django
{% blocktrans with username=user.username %}
<p>Hello {{ username }},</p>
{% endblocktrans %}
```

### Time Formatting
Use `naturaltime` filter for human-readable time:

```django
{% blocktrans with expires=expires|naturaltime %}
<p>This link expires {{ expires }}.</p>
{% endblocktrans %}
```

## Django Template Syntax

### Comments
```django
{# This is a comment #}
```

### Variables
```django
{{ variable_name }}
```

### Filters
```django
{{ user.username|title }}
{{ expires|naturaltime }}
{{ value|default:"fallback" }}
```

### Conditionals
```django
{% if user.username %}
    Hello {{ user.username }}
{% else %}
    Hello there
{% endif %}
```

### Loops
```django
{% for item in items %}
    {{ item }}
{% endfor %}
```

## Best Practices

1. **Always load i18n**: Start templates with `{% load i18n %}`
2. **Use blocktrans for variables**: Wrap user-specific text in `{% blocktrans %}...{% endblocktrans %}`
3. **Format timestamps**: Use `expires|naturaltime` instead of raw `expires`
4. **Use user.username**: This is the primary identifier, not `user.name`
5. **Provide plain text URLs**: Always include `{{ url }}` as plain text alongside buttons

## Template Examples

### Basic greeting with username
```django
{% blocktrans with username=user.username %}
<p>Hello {{ username }},</p>
{% endblocktrans %}
```

### Expiration warning
```django
{% blocktrans with expires=expires|naturaltime %}
<p>This link expires {{ expires }}. If you did not request this action, you can safely ignore this email.</p>
{% endblocktrans %}
```

### Action button with fallback URL
```django
<center>
    <a href="{{ url }}" class="button">{% trans 'Reset Password' %}</a>
</center>
<p>{% trans 'Or copy and paste this link into your browser:' %}</p>
<p style="word-break: break-all;">{{ url }}</p>
```

## References

- Authentik Email Stage Docs: https://docs.goauthentik.io/add-secure-apps/flows-stages/stages/email/
- Django Template Language: https://docs.djangoproject.com/en/stable/ref/templates/language/
- Django Humanize: https://docs.djangoproject.com/en/stable/ref/contrib/humanize/
