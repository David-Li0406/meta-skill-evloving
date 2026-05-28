---
name: angular-material-v20
description: Angular Material v20 UI component library for Angular 20+ applications. Use when implementing Material Design components, theming, forms, tables, dialogs, navigation, or building Material-based UI. Covers component APIs, accessibility, and best practices for Material 20.
license: MIT
---

# Angular Material v20 Skill

## 🎯 Purpose
This skill provides guidance for working with **Angular Material v20** (`@angular/material: "~20.0.0"`), the official Material Design component library for Angular 20+ applications.

## 🛠️ Installation

```bash
ng add @angular/material
```

Or manually:
```bash
pnpm install @angular/material@~20.0.0 @angular/cdk@~20.0.0
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
  selector: 'app-form',
  standalone: true,
  imports: [MatFormFieldModule, MatInputModule, ReactiveFormsModule],
  template: `
    <mat-form-field appearance="outline">
      <mat-label>Email</mat-label>
      <input matInput [formControl]="email" />
      <mat-error *ngIf="email.hasError('required')">
        Email is required
      </mat-error>
    </mat-form-field>
  `
})
export class FormComponent {
  email = new FormControl('', Validators.required);
}
```

## 🚀 Best Practices

1. **Import modules** - Import specific component modules
2. **Use theming** - Leverage Material's theming system
3. **Accessibility** - Follow ARIA guidelines
4. **OnPush** - Use OnPush change detection
5. **Lazy loading** - Lazy load Material modules where possible

## 📖 Resources

- [Material Design Guidelines](https://material.io/design)
- [Angular Material Docs](https://material.angular.io)
- [Component API](https://material.angular.io/components/categories)

---

💡 This skill automatically loads when working with Angular Material v20 components.
