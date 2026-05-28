---
name: angular-material
description: Use this skill when implementing Material Design components in Angular 20+ applications, including theming, forms, tables, dialogs, and navigation.
---

# Angular Material Component Library Skill

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
  template: `<mat-toolbar><button mat-button>Menu</button></mat-toolbar>`
})
export class HeaderComponent {}
```

## 📚 Core Components

### Form Controls
- MatInput
- MatSelect
- MatCheckbox
- MatRadioButton
- MatSlideToggle
- MatSlider
- MatDatepicker

### Navigation
- MatToolbar
- MatSidenav
- MatMenu
- MatTabs

### Layout
- MatCard
- MatDivider
- MatExpansionPanel
- MatGridList
- MatList
- MatStepper

### Buttons & Indicators
- MatButton
- MatButtonToggle
- MatBadge
- MatChip
- MatIcon
- MatProgressBar
- MatProgressSpinner

### Popups & Modals
- MatDialog
- MatSnackBar
- MatTooltip
- MatBottomSheet

### Data Tables
- MatTable
- MatSort
- MatPaginator

## 🎨 Theming

### Basic Theme Setup

```typescript
// styles.scss
@use '@angular/material' as mat;

@include mat.core();

$my-primary: mat.define-palette(mat.$indigo-palette);
$my-accent: mat.define-palette(mat.$pink-palette);
$my-warn: mat.define-palette(mat.$red-palette);

$my-theme: mat.define-light-theme((
  color: (
    primary: $my-primary,
    accent: $my-accent,
    warn: $my-warn,
  )
));

@include mat.all-component-themes($my-theme);
```

## 💡 Common Patterns

### Dialog Example

```typescript
import { Component, inject } from '@angular/core';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';

@Component({
  selector: 'app-example',
  standalone: true,
  imports: [MatDialogModule],
  template: `
    <button mat-raised-button (click)="openDialog()">
      Open Dialog
    </button>
  `
})
export class ExampleComponent {
  dialog = inject(MatDialog);
  
  openDialog() {
    this.dialog.open(MyDialogComponent, {
      width: '400px',
      data: { name: 'Example' }
    });
  }
}
```

### Form Field Example

```typescript
import { Component } from '@angular/core';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-form-example',
  standalone: true,
  imports: [MatFormFieldModule, MatInputModule, ReactiveFormsModule],
  template: `
    <mat-form-field>
      <mat-label>Input</mat-label>
      <input matInput placeholder="Enter something">
    </mat-form-field>
  `
})
export class FormExampleComponent {}
```