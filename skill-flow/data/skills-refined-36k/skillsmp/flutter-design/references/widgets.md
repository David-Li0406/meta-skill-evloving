# Flutter Widget Recipes

Common widget patterns aligned with Refactoring UI principles.

---

## Cards

### Flat Card

```dart
Container(
  padding: const EdgeInsets.all(16),
  decoration: BoxDecoration(
    color: context.colors.surface,
    borderRadius: BorderRadius.circular(12),
    border: Border.all(
      color: context.colors.outline.withOpacity(0.2),
    ),
  ),
  child: Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Text('Title', style: context.textTheme.titleMedium),
      const SizedBox(height: 8),
      Text('Content', style: context.textTheme.bodyMedium),
    ],
  ),
)
```

### Elevated Card

```dart
Container(
  padding: const EdgeInsets.all(16),
  decoration: BoxDecoration(
    color: context.colors.surface,
    borderRadius: BorderRadius.circular(12),
    boxShadow: [
      BoxShadow(
        color: Colors.black.withOpacity(0.08),
        blurRadius: 10,
        offset: const Offset(0, 2),
      ),
    ],
  ),
  child: child,
)
```

### Interactive Card

```dart
Material(
  color: context.colors.surface,
  borderRadius: BorderRadius.circular(12),
  child: InkWell(
    onTap: onTap,
    borderRadius: BorderRadius.circular(12),
    child: Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: context.colors.outline.withOpacity(0.2),
        ),
      ),
      child: child,
    ),
  ),
)
```

---

## Buttons

### Primary Button

```dart
ElevatedButton(
  onPressed: onPressed,
  child: const Text('Primary'),
)
```

### Secondary Button

```dart
OutlinedButton(
  onPressed: onPressed,
  child: const Text('Secondary'),
)
```

### Ghost Button

```dart
TextButton(
  onPressed: onPressed,
  child: const Text('Ghost'),
)
```

### Icon Button with Background

```dart
IconButton.filled(
  onPressed: onPressed,
  icon: const Icon(Icons.add),
)
```

---

## Input Fields

### Standard Input

```dart
TextField(
  decoration: const InputDecoration(
    labelText: 'Email',
    hintText: 'Enter your email',
  ),
)
```

### With Prefix Icon

```dart
TextField(
  decoration: InputDecoration(
    labelText: 'Search',
    prefixIcon: Icon(Icons.search, color: context.colors.onSurface.withOpacity(0.5)),
  ),
)
```

---

## List Items

### Simple List Item

```dart
ListTile(
  title: Text('Title', style: context.textTheme.bodyLarge),
  subtitle: Text('Subtitle', style: context.textTheme.bodySmall),
  trailing: const Icon(Icons.chevron_right),
  onTap: onTap,
)
```

### Custom List Item

```dart
InkWell(
  onTap: onTap,
  child: Padding(
    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
    child: Row(
      children: [
        CircleAvatar(backgroundImage: NetworkImage(imageUrl)),
        const SizedBox(width: 12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(title, style: context.textTheme.bodyLarge),
              Text(subtitle, style: context.textTheme.bodySmall?.copyWith(
                color: context.colors.onSurface.withOpacity(0.6),
              )),
            ],
          ),
        ),
        Icon(Icons.chevron_right, color: context.colors.onSurface.withOpacity(0.4)),
      ],
    ),
  ),
)
```

---

## Badges

### Status Badge

```dart
Container(
  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
  decoration: BoxDecoration(
    color: context.colors.primaryContainer,
    borderRadius: BorderRadius.circular(12),
  ),
  child: Text(
    'Active',
    style: context.textTheme.labelSmall?.copyWith(
      color: context.colors.onPrimaryContainer,
      fontWeight: FontWeight.w600,
    ),
  ),
)
```

### Semantic Badges

```dart
// Success
Container(
  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
  decoration: BoxDecoration(
    color: Colors.green.withOpacity(0.1),
    borderRadius: BorderRadius.circular(12),
  ),
  child: Text('Success', style: TextStyle(color: Colors.green.shade700)),
)

// Warning
Container(
  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
  decoration: BoxDecoration(
    color: Colors.amber.withOpacity(0.1),
    borderRadius: BorderRadius.circular(12),
  ),
  child: Text('Pending', style: TextStyle(color: Colors.amber.shade700)),
)

// Error
Container(
  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
  decoration: BoxDecoration(
    color: Colors.red.withOpacity(0.1),
    borderRadius: BorderRadius.circular(12),
  ),
  child: Text('Failed', style: TextStyle(color: Colors.red.shade700)),
)
```

---

## Empty State

```dart
Center(
  child: Padding(
    padding: const EdgeInsets.all(32),
    child: Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Icon(
          Icons.inbox_outlined,
          size: 64,
          color: context.colors.onSurface.withOpacity(0.3),
        ),
        const SizedBox(height: 16),
        Text(
          'No items yet',
          style: context.textTheme.titleMedium,
        ),
        const SizedBox(height: 8),
        Text(
          'Create your first item to get started.',
          style: context.textTheme.bodyMedium?.copyWith(
            color: context.colors.onSurface.withOpacity(0.6),
          ),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: 24),
        ElevatedButton.icon(
          onPressed: onCreate,
          icon: const Icon(Icons.add),
          label: const Text('Create Item'),
        ),
      ],
    ),
  ),
)
```
