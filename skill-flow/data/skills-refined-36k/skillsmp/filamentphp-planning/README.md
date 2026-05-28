# FilamentPHP Planning Skill

Expert knowledge for planning and architecting FilamentPHP 4.x applications.

## Overview

This skill provides comprehensive guidance for all aspects of FilamentPHP 4.x development, from basic CRUD resources to advanced multi-tenancy and authentication systems.

### What's Included

- **14 Reference Files** covering all major FilamentPHP topics
- **Real-world examples** from FilamentPHP 4.x best practices
- **Modular structure** for easy navigation and maintenance
- **Code quality patterns** for scalable applications

### Quick Start

1. **Planning a new resource?** → See [references/RESOURCES.md](references/RESOURCES.md)
2. **Building a form?** → See [references/FORMS.md](references/FORMS.md)
3. **Creating a table?** → See [references/TABLES.md](references/TABLES.md)
4. **Adding notifications?** → See [references/NOTIFICATIONS.md](references/NOTIFICATIONS.md)
5. **Setting up multi-tenancy?** → See [references/TENANCY.md](references/TENANCY.md)

## Reference Files

### Core Components
- **[FORMS.md](references/FORMS.md)** - Form components, validation, relationships
- **[TABLES.md](references/TABLES.md)** - Columns, filters, search, actions
- **[RESOURCES.md](references/RESOURCES.md)** - CRUD operations, navigation, authorization
- **[INFOLISTS.md](references/INFOLISTS.md)** - Read-only data display

### Features
- **[NOTIFICATIONS.md](references/NOTIFICATIONS.md)** - Creating and sending notifications
- **[WIDGETS.md](references/WIDGETS.md)** - Stats overview, charts
- **[SCHEMAS.md](references/SCHEMAS.md)** - Layout components, configuration
- **[ACTIONS.md](references/ACTIONS.md)** - Table and bulk actions

### Advanced
- **[PANEL_CONFIGURATION.md](references/PANEL_CONFIGURATION.md)** - Authentication, MFA, SPA
- **[TENANCY.md](references/TENANCY.md)** - Multi-tenancy setup
- **[GLOBAL_SEARCH.md](references/GLOBAL_SEARCH.md)** - Search configuration
- **[TESTING.md](references/TESTING.md)** - Testing strategies

### Best Practices
- **[CODE_QUALITY.md](references/CODE_QUALITY.md)** - Organization patterns
- **[MIGRATION.md](references/MIGRATION.md)** - V3 to V4 upgrade guide

## Common Use Cases

### Creating a New Resource

```php
// 1. Generate the resource
php artisan make:filament-resource Post --generate

// 2. Customize the form (see FORMS.md)
public static function form(Schema $schema): Schema
{
    return PostForm::configure($schema);
}

// 3. Customize the table (see TABLES.md)
public static function table(Table $table): Table
{
    return PostsTable::configure($table);
}
```

See [RESOURCES.md](references/RESOURCES.md) for complete guidance.

### Adding Search to a Table

```php
// Enable global search
public function table(Table $table): Table
{
    return $table
        ->searchable()
        ->columns([
            TextColumn::make('title')->searchable(),
            TextColumn::make('author.name')->searchable(),
        ]);
}
```

See [TABLES.md](references/TABLES.md) for search patterns.

### Implementing Multi-Tenancy

```php
// 1. Configure panel with tenancy
public function panel(Panel $panel): Panel
{
    return $panel
        ->tenant(Team::class)
        ->tenantMiddleware([ApplyTenantScopes::class]);
}

// 2. Apply global scopes (see TENANCY.md)
```

See [TENANCY.md](references/TENANCY.md) for complete setup.

## Architecture Patterns

### Separation of Concerns

Keep your resources clean by separating forms and tables:

```
app/Filament/Resources/
└── Customers/
    ├── CustomerResource.php
    ├── Schemas/
    │   └── CustomerForm.php
    └── Tables/
        └── CustomersTable.php
```

See [CODE_QUALITY.md](references/CODE_QUALITY.md) for organization patterns.

### Global Configuration

Apply defaults in your service provider:

```php
use Filament\Tables\Columns\TextColumn;

TextColumn::configureUsing(function (TextColumn $column): void {
    $column->toggleable();
});
```

See [SCHEMAS.md](references/SCHEMAS.md) for configuration patterns.

## Version Compatibility

- **FilamentPHP:** 4.x
- **Laravel:** 11.x
- **PHP:** 8.2+

For v3 to v4 migration, see [MIGRATION.md](references/MIGRATION.md).

## Contributing

This skill is part of the Larament project. To contribute:

1. Follow the reference file structure
2. Include practical code examples
3. Cross-reference related topics
4. Test examples with FilamentPHP 4.x

## License

MIT License - See LICENSE file for details

---

**Need Help?**
- Check the [Executive Plan](EXECUTIVE_PLAN.md) for implementation roadmap
- Review specific reference files for detailed guidance
- Consult [FilamentPHP Documentation](https://filamentphp.com/docs/4.x)
