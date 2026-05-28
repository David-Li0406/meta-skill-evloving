---
name: angular-20
description: Angular 20 knowledge and best practices. Use this skill when asked about Angular 20 development, architecture, components, routing, state management, performance, testing, and deployment. Includes standalone components, signals, and modern Angular patterns.
license: MIT
---

# Angular 20 Skill for AI Agents

## 🧩 Purpose
This skill provides structured guidance and best practices for Angular 20 development, including typical workflows, common patterns, quality standards, and example templates.

## 🛠️ Angular 20 Core Concepts
- Angular 20 features & changes  
- TypeScript-first architecture  
- Standalone components  
- Signals and reactivity  
- Composition API  
- Angular CLI workflows

## 📚 Key Tasks & When to Use

### 1) Create a new Angular 20 app
Use Angular CLI to bootstrap projects, follow style/architecture rules:
```bash
ng new your-app --routing --style=scss
```

### 2) Component & Template Patterns
- Use standalone components where possible
- Keep templates clean & concise
- Enforce accessibility (a11y) guidelines

### 3) 🚦 Routing & Navigation
- Setup RouterModule with routes
- Use lazy-loaded routes for large modules
- Implement prefetching strategies for performance

### 4) 🔄 State & Reactivity
- Prefer Signals for local state
- Consider @ngrx/signals for global state
- Manage effects/rx workflows carefully

### 5) 📦 HTTP & REST
- Use HttpClient with typed responses
- Centralize API service layer with error handling

### 6) 📑 Testing
- Unit test with Jasmine/Karma or Jest
- E2E tests with Playwright

### 7) 🎯 Performance
- Use AOT compilation
- Optimize bundle with `ng build`
- Use OnPush change detection where applicable

### 8) 🚀 Deployment
- Build artifacts: `ng build`
- Serve with static hosts / CDNs
- Configure environment-specific settings

## 📌 Examples & Code Snippets

### Example Standalone Component
```typescript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-example',
  standalone: true,
  imports: [CommonModule],
  template: `
    @if (showContent()) {
      <div>Content here</div>
    }
  `
})
export class ExampleComponent {
  showContent = signal(true);
}
```

### Example Reactive Form
```typescript
import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  selector: 'app-form',
  standalone: true,
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="form">
      <input formControlName="name" />
    </form>
  `
})
export class FormComponent {
  private fb = inject(FormBuilder);
  
  form = this.fb.group({
    name: ['', Validators.required]
  });
}
```

### Example API Service
```typescript
import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);
  
  getData(): Observable<any[]> {
    return this.http.get<any[]>('/api/data');
  }
}
```

Refer to official Angular docs and community standards for evolving best practices.

---

## 📂 Installation Path

### 🎯 Project-specific skill
`.github/skills/angular-20/SKILL.md`

### 🎯 Personal global skill
`~/.github/skills/angular-20/SKILL.md`

💡 Copilot will automatically load this skill based on your prompt content.
