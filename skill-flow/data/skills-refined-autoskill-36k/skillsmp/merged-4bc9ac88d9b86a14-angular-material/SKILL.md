---
name: angular-material
description: Use this skill when implementing Angular Material components, theming, forms, tables, dialogs, and navigation in Angular 20+ applications.
---

# Angular Material Skill

## 🎯 Purpose
This skill provides comprehensive guidance on **Angular Material**, the official Material Design component library for Angular applications, including component usage, theming, customization, and best practices.

## 📦 What is Angular Material?

Angular Material is Angular's official UI component library that implements Material Design:
- **50+ Production-ready Components**: Buttons, forms, navigation, data tables, dialogs, and more
- **Accessibility Built-in**: ARIA support and keyboard navigation
- **Responsive Design**: Mobile-first, responsive layouts
- **Theming System**: Powerful SCSS-based theming
- **TypeScript Support**: Full type safety
- **Angular Integration**: Seamless integration with Angular features

## 🎨 When to Use This Skill

Use Angular Material guidance when:
- Building Angular applications with Material Design
- Implementing forms with Material form controls
- Creating data tables with sorting, pagination, and filtering
- Building navigation with Material sidenav and toolbars
- Implementing dialogs, snackbars, and bottom sheets
- Using Material icons and buttons
- Creating custom themes
- Ensuring accessibility compliance

## 🛠️ Installation & Setup

### Install Angular Material

```bash
# Using Angular CLI (recommended)
ng add @angular/material

# Or using npm/pnpm
pnpm install @angular/material @angular/cdk @angular/animations
```

### Configure in Application

```typescript
// app.config.ts (Angular 20+ standalone)
import { provideAnimations } from '@angular/platform-browser/animations';

export const appConfig: ApplicationConfig = {
  providers: [
    provideAnimations(),
    // ... other providers
  ]
};
```

### Import Components

```typescript
// In standalone component
import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [MatButtonModule, MatIconModule, MatToolbarModule],
  template: `
    <mat-toolbar color="primary">
      <span>My App</span>
      <span class="spacer"></span>
      <button mat-icon-button>
        <mat-icon>menu</mat-icon>
      </button>
    </mat-toolbar>
  `
})
export class HeaderComponent {}
```

## 📚 Core Component Categories

### 1. Form Controls
- **Input & Text Fields**: Use `MatInput` and `MatFormField` for input fields.
- **Select & Autocomplete**: Use `MatSelect` and `MatAutocomplete` for dropdowns and search fields.
- **Checkboxes & Radio Buttons**: Use `MatCheckbox` and `MatRadioButton` for selection options.
- **Date & Time Pickers**: Use `MatDatepicker` for date selection.

### 2. Navigation Components
- **Toolbar**: Use `MatToolbar` for application headers.
- **Sidenav**: Use `MatSidenav` for side navigation.
- **Tabs**: Use `MatTabs` for tabbed navigation.

### 3. Layout Components
- **Cards**: Use `MatCard` for card layouts.
- **Grid List**: Use `MatGridList` for grid layouts.

### 4. Buttons & Indicators
- **Buttons**: Use `MatButton` for various button types.
- **Progress Indicators**: Use `MatProgressSpinner` and `MatProgressBar` for loading indicators.

### 5. Popups & Modals
- **Dialog**: Use `MatDialog` for modal dialogs.
- **Snackbar**: Use `MatSnackBar` for temporary messages.
- **Bottom Sheet**: Use `MatBottomSheet` for bottom sheets.

### 6. Data Tables
- **Table with Sorting & Pagination**: Use `MatTable`, `MatSort`, and `MatPaginator` for data tables.

## 🎯 Best Practices

1. **Import Only What You Need**: Import specific modules instead of the entire library.
2. **Use Appearance Variants**: Leverage different appearances for form fields.
3. **Leverage Color Themes**: Use color attributes for semantic styling.
4. **Accessibility**: Always provide labels and ARIA attributes.
5. **Responsive Design**: Use Material breakpoints for responsive layouts.

## 🔧 Theming

### Custom Theme
```scss
@use '@angular/material' as mat;

$my-primary: mat.define-palette(mat.$indigo-palette);
$my-accent: mat.define-palette(mat.$pink-palette);
$my-warn: mat.define-palette(mat.$red-palette);

$my-theme: mat.define-light-theme((
  color: (
    primary: $my-primary,
    accent: $my-accent,
    warn: $my-warn,
  ),
));

@include mat.all-component-themes($my-theme);
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Animations not working | Import `provideAnimations()` or `BrowserAnimationsModule` |
| Icons not showing | Import Material Icons font in index.html |
| Styles not applying | Import `@angular/material/prebuilt-themes` in styles.scss |
| Form field errors | Wrap input in `<mat-form-field>` with `<mat-label>` |
| Table not sorting | Add `MatSort` directive and set `dataSource.sort` |
| Dialog not opening | Inject `MatDialog` service and import `MatDialogModule` |

## 📖 References

- [Angular Material Official Docs](https://material.angular.io/)
- [Component API Reference](https://material.angular.io/components/categories)
- [Material Design Guidelines](https://m3.material.io/)
- [Angular Material GitHub](https://github.com/angular/components)

---

## 📂 Recommended Placement

**Project-level skill:**
```
/github/skills/angular-material/SKILL.md
```

Copilot will load this when working with Angular Material components.