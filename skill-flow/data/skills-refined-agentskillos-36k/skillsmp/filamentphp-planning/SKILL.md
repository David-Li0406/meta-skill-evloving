---
name: filamentphp-planning
description: Expert knowledge for planning and architecting FilamentPHP 4.x applications. Covers resources, forms, tables, schemas, actions, notifications, widgets, authentication, tenancy, and best practices. Use this skill when designing FilamentPHP admin panels, planning feature implementation, or organizing application structure.
license: MIT
metadata:
  author: larament-project
  version: "1.0.0"
  framework: FilamentPHP 4.x
  compatibility: Requires FilamentPHP 4.x, Laravel 11.x, PHP 8.2+
allowed-tools: Read Write
---

# FilamentPHP Planning Skill

This skill provides comprehensive guidance for planning and architecting FilamentPHP 4.x applications. It uses a modular reference system to organize topics into focused, maintainable documentation.

## Overview

FilamentPHP is a full-stack framework and panel builder for Laravel that accelerates development of admin interfaces. This skill helps you:

- Plan resource structures and relationships
- Design forms, tables, and infolists
- Implement authentication and multi-tenancy
- Configure panels and navigation
- Build custom widgets and actions
- Follow code quality best practices

## Topic References

Each major topic area has dedicated reference documentation:

### Core Components

- **[Forms](references/FORMS.md)** - Form components, validation, relationships, file uploads
- **[Tables](references/TABLES.md)** - Columns, filters, search, actions, bulk operations
- **[Resources](references/RESOURCES.md)** - CRUD operations, navigation, relationships, authorization
- **[Infolists](references/INFOLISTS.md)** - Read-only data display, entries, customization

### Features & Configuration

- **[Notifications](references/NOTIFICATIONS.md)** - Creating and sending notifications, actions
- **[Widgets](references/WIDGETS.md)** - Stats overview, charts, custom widgets
- **[Schemas](references/SCHEMAS.md)** - Layout components, global configuration
- **[Actions](references/ACTIONS.md)** - Table actions, bulk actions, relationship actions

### Advanced Topics

- **[Panel Configuration](references/PANEL_CONFIGURATION.md)** - Authentication, MFA, SPA mode, navigation
- **[Tenancy](references/TENANCY.md)** - Multi-tenancy setup, scopes, middleware
- **[Global Search](references/GLOBAL_SEARCH.md)** - Configuration and customization
- **[Testing](references/TESTING.md)** - Resource, table, and form testing strategies

### Best Practices

- **[Code Quality](references/CODE_QUALITY.md)** - File organization, reusable components, patterns
- **[Migration Guide](references/MIGRATION.md)** - V3 to V4 upgrade strategies

## When to Use This Skill

### Planning Phase
- Designing admin panel structure
- Determining resource relationships
- Planning navigation and organization
- Selecting appropriate components

### Implementation Phase
- Implementing forms and validation
- Building table views with filters
- Creating custom widgets
- Setting up authentication flows

### Optimization Phase
- Refactoring for code quality
- Implementing global configurations
- Adding advanced features
- Performance tuning

## Common Patterns

### Resource Structure
```php
// Use separate classes for maintainability
public static function form(Schema $schema): Schema
{
    return CustomerForm::configure($schema);
}

public static function table(Table $table): Table
{
    return CustomersTable::configure($table);
}
```

### Global Configuration
```php
// Apply defaults in service provider
TextColumn::configureUsing(function (TextColumn $column): void {
    $column->toggleable();
});
```

### Conditional Features
```php
// Use feature flags for dynamic behavior
TextInput::make('name')
    ->autofocus(FeatureFlag::active())
```

## Architecture Principles

1. **Separation of Concerns** - Split forms, tables, and schemas into dedicated classes
2. **Reusability** - Use global configurations for common patterns
3. **Flexibility** - Leverage closures for dynamic behavior
4. **Performance** - Defer loading, eager load relationships, use Scout for search
5. **Maintainability** - Follow consistent naming and organization patterns

## Quick Reference

- **Forms:** TextInput, Select, FileUpload, RichEditor, Builder
- **Tables:** TextColumn, IconColumn, SelectColumn, ImageColumn
- **Layouts:** Grid, Section, Fieldset, Tabs, Wizard
- **Actions:** CreateAction, EditAction, DeleteAction, BulkActions
- **Widgets:** StatsOverview, ChartWidget, Custom Widgets

## Getting Started

1. Review the relevant reference documentation for your use case
2. Check the code quality guide for organizational patterns
3. Follow the examples in each reference file
4. Apply global configurations where appropriate
5. Test thoroughly using the testing guide

## Additional Resources

- [Official FilamentPHP Documentation](https://filamentphp.com/docs/4.x)
- [FilamentPHP GitHub Repository](https://github.com/filamentphp/filament)
- [Community Packages](https://filamentphp.com/plugins)

---

**Note:** This skill is optimized for FilamentPHP 4.x. For v3 compatibility, refer to the migration guide.
