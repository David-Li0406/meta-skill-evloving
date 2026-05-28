---
name: angular-material
description: Use this skill when implementing Angular Material components, theming, and building Material Design UIs in Angular 20+ applications.
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
- **Input & Text Fields**: `MatInput`, `MatFormField`
- **Select & Autocomplete**: `MatSelect`, `MatAutocomplete`
- **Checkboxes & Radio Buttons**: `MatCheckbox`, `MatRadioButton`
- **Date & Time Pickers**: `MatDatepicker`

### 2. Navigation Components
- **Toolbar**: `MatToolbar`
- **Sidenav**: `MatSidenav`
- **Tabs**: `MatTabs`

### 3. Layout Components
- **Cards**: `MatCard`
- **Grid List**: `MatGridList`

### 4. Buttons & Indicators
- **Buttons**: `MatButton`, `MatButtonToggle`
- **Progress Indicators**: `MatProgressSpinner`, `MatProgressBar`

### 5. Popups & Modals
- **Dialog**: `MatDialog`
- **Snackbar**: `MatSnackBar`
- **Bottom Sheet**: `MatBottomSheet`

### 6. Data Tables
- **Table with Sorting & Pagination**: `MatTable`, `MatSort`, `MatPaginator`

## 🎯 Best Practices

### 1. Import Only What You Need
```typescript
// ✅ Good - Import specific modules
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

// ❌ Bad - Don't import everything
import * as Material from '@angular/material';
```

### 2. Use Appearance Variants
```typescript
// Material form fields support different appearances
<mat-form-field appearance="fill">     <!-- Default -->
<mat-form-field appearance="outline">  <!-- Outlined -->
```

### 3. Leverage Color Themes
```scss
// Use color attribute for semantic styling
<button mat-raised-button color="primary">Primary</button>
```

### 4. Accessibility
```typescript
// Always provide labels and ARIA attributes
<button mat-icon-button aria-label="Delete item">
  <mat-icon>delete</mat-icon>
</button>
```

### 5. Responsive Design
```scss
// Use Material breakpoints
@use '@angular/material' as mat;

@media (max-width: mat.$small-breakpoint) {
  .sidenav {
    mode: 'over';
  }
}
```

## 🎨 Theming

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
/.github/skills/angular-material/SKILL.md
```

Copilot will load this when working with Angular Material components.