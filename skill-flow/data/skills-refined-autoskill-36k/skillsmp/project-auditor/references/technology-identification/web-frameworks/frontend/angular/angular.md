# Angular

**Category**: web-frameworks/frontend
**Description**: Platform for building mobile and desktop web applications - Google's enterprise-grade framework with TypeScript
**Homepage**: https://angular.io

## Package Detection

### NPM
*Core Angular packages - all @angular/* scoped*

- `@angular/core`
- `@angular/common`
- `@angular/platform-browser`

### YARN
*Core Angular package via Yarn*

- `@angular/core`

### PNPM
*Core Angular package via pnpm*

- `@angular/core`

### Related Packages
- `@ngrx/store`
- `@ngrx/effects`
- `rxjs`
- `zone.js`
- `@angular/material`
- `@angular/cdk`
- `ng-bootstrap`
- `primeng`
- `@ngx-translate/core`
- `angular-cli-ghpages`

## Import Detection

### Typescript
File extensions: .ts

**Pattern**: `import\s+\{[^}]*(Component|NgModule|Injectable|Directive)[^}]*\}\s+from\s+['"]@angular/core['"]`
- Angular core decorators
- Example: `import { Component, NgModule } from '@angular/core';`

**Pattern**: `import\s+.*\s+from\s+['"]@angular/(core|common|router|forms)['"]`
- Angular package imports
- Example: `import { RouterModule } from '@angular/router';`

**Pattern**: `@Component\(`
- Component decorator usage
- Example: `@Component({ selector: 'app-root' })`

**Pattern**: `@NgModule\(`
- NgModule decorator usage
- Example: `@NgModule({ declarations: [AppComponent] })`

**Pattern**: `@Injectable\(`
- Injectable service decorator
- Example: `@Injectable({ providedIn: 'root' })`

### Common Imports
- `Component`
- `NgModule`
- `Injectable`
- `Directive`
- `Pipe`
- `Input`
- `Output`
- `EventEmitter`
- `OnInit`
- `RouterModule`
- `FormsModule`
- `ReactiveFormsModule`
- `HttpClient`

## Environment Variables

*Angular CLI environment variables*

- Prefix: `NG_*`
*Standard Node.js environment variable used by Angular build*

- `NODE_ENV`

## Configuration Files

- `angular.json`
- `.angular-cli.json`
- `tsconfig.app.json`
- `tsconfig.spec.json`
- `tsconfig.json`
- `*.component.ts`
- `*.service.ts`
- `*.module.ts`
- `*.directive.ts`
- `*.pipe.ts`

## Detection Notes

- All Angular packages are scoped under @angular/*
- Presence of @angular/core is definitive indicator
- Angular always requires rxjs and zone.js
- Angular CLI projects have angular.json
- @ngrx is the official Redux-style state management

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 85% (HIGH)
- **Environment Variable Detection**: 65% (MEDIUM)
- **API Endpoint Detection**: 50% (MEDIUM)
