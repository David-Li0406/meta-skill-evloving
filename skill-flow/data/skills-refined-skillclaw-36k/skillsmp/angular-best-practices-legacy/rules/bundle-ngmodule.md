---
title: Organize Code with Feature Modules
impact: CRITICAL
impactDescription: Better code organization, enables lazy loading
tags: ngmodule, modules, architecture
---

## Organize Code with Feature Modules

Feature modules group related components, services, and pipes. They enable lazy loading and keep the codebase organized. Each feature should have its own module.

**Incorrect (Everything in AppModule):**

```typescript
@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    UserListComponent,
    UserDetailComponent,
    ProductListComponent,
    ProductDetailComponent,
    CartComponent,
    CheckoutComponent,
    // ... 50 more components
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}
// Everything loaded upfront, huge initial bundle
```

**Correct (Feature modules with lazy loading):**

```typescript
// user.module.ts
@NgModule({
  declarations: [
    UserListComponent,
    UserDetailComponent,
    UserAvatarComponent,
  ],
  imports: [
    CommonModule,
    UserRoutingModule,
    SharedModule,
  ]
})
export class UserModule {}

// product.module.ts
@NgModule({
  declarations: [
    ProductListComponent,
    ProductDetailComponent,
  ],
  imports: [
    CommonModule,
    ProductRoutingModule,
    SharedModule,
  ]
})
export class ProductModule {}

// app-routing.module.ts
const routes: Routes = [
  {
    path: 'users',
    loadChildren: () => import('./user/user.module').then(m => m.UserModule)
  },
  {
    path: 'products',
    loadChildren: () => import('./product/product.module').then(m => m.ProductModule)
  }
];

// app.module.ts - minimal
@NgModule({
  declarations: [AppComponent, HeaderComponent, FooterComponent],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    CoreModule, // Singleton services
  ],
  bootstrap: [AppComponent]
})
export class AppModule {}
```

**SharedModule pattern:**

```typescript
@NgModule({
  declarations: [LoadingSpinnerComponent, ErrorMessageComponent],
  imports: [CommonModule],
  exports: [
    CommonModule,
    LoadingSpinnerComponent,
    ErrorMessageComponent,
  ]
})
export class SharedModule {}
```

Reference: [Angular Feature Modules](https://v16.angular.io/guide/feature-modules)
