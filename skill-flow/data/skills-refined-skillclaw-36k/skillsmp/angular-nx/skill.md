---
name: angular-nx
description: Specialized knowledge for working with Angular 19 and Nx in the Sentinel monorepo. Use when generating components, running tests/builds, or working with the frontend workspace structure.
---

# Nx Skill

This skill provides specialized knowledge for working with Nx in the Sentinel monorepo.

## Project Structure

The sentinel-frontend is an Nx monorepo with the following structure:
- **apps/sentinel**: Main Angular application
- **libs/**: Shared libraries and API clients
- **Nx workspace**: Angular 19 with standalone components

## Common Nx Commands

### Development
```bash
# Serve the main application (port 4200)
npx nx serve sentinel

# Serve with specific configuration
npx nx serve sentinel --configuration=development
npx nx serve sentinel --configuration=production
```

### Testing
```bash
# Run all tests
npx nx test sentinel

# Run tests for specific file
npx nx test sentinel --testFile=path/to/specific.spec.ts

# Run tests in watch mode
npx nx test sentinel --watch

# Run with coverage
npx nx test sentinel --coverage
```

### Building
```bash
# Build for development
npx nx build sentinel

# Build for production
npx nx build sentinel --configuration=production
npm run build:prod  # Shorthand defined in package.json
```

### Code Generation
```bash
# Generate component
npx nx generate @angular/core:component --name=my-component --project=sentinel --standalone=true

# Generate service
npx nx generate @angular/core:service --name=my-service --project=sentinel

# Generate library
npx nx generate @nx/angular:library --name=my-lib

# Generate interface
npx nx generate @angular/core:interface --name=my-interface --project=sentinel
```

### Linting & Formatting
```bash
# Lint the project
npx nx lint sentinel

# Lint and fix
npx nx lint sentinel --fix

# Format with prettier
npx nx format:write
```

### Dependency Graph
```bash
# View project dependency graph
npx nx graph

# Show affected projects
npx nx affected:graph
```

## Nx Workspace Configuration

The workspace is configured with:
- **Angular 19**: Latest version with standalone components
- **TypeScript**: Strict mode enabled
- **ESLint**: For linting
- **Jest**: For unit testing
- **Standalone components**: No NgModules

## Key Patterns for Sentinel

### Component Generation
When generating components for Sentinel, always use:
- `--standalone=true`: All components are standalone
- `--project=sentinel`: Target the main application
- Consider the route structure under `apps/sentinel/src/app/`

For detailed component generation examples and templates, see [component-generation.md](examples/component-generation.md).

## Forms
When generating forms, use the new **Signal Forms** package (`@angular/forms/signals`).

**Key points:**
- Use `form()` from `@angular/forms/signals` instead of FormGroup/FormControl
- Initialize form state with `signal()`
- Use the `Field` component in templates

For detailed examples and patterns, see [signal-forms.md](examples/signal-forms.md).

Reference implementation: [login.component.ts](../../sentinel-frontend/libs/shared/login/src/lib/login/login.component.ts)



### Library Structure
- **libs/sentinel/api-client**: Auto-generated TypeScript API clients
- **libs/sentinel/shared**: Shared utilities and components
- Keep libraries focused and single-purpose

### Testing
- Use Jest for unit tests
- Follow Angular testing best practices
- Mock API clients from libs/sentinel/api-client

### Build Optimization
- Use production configuration for optimized builds
- Leverage Nx caching for faster builds
- Run `nx affected` commands in CI/CD

## Integration with Other Services

### API Client Generation
After updating the Rails backend API:
```bash
cd sentinel-backend
rails rswag:specs:swaggerize
cd ..
./tools/generate-api-clients.sh
```
This regenerates TypeScript clients in `libs/sentinel/api-client/`

### Docker Integration
The frontend is containerized and served via nginx in production:
```bash
cd sentinel-frontend
docker build -t sentinel-frontend .
```

## Troubleshooting

### Clear Nx Cache
```bash
npx nx reset
```

### Reinstall Dependencies
```bash
rm -rf node_modules package-lock.json
npm install
```

### Check Nx Version
```bash
npx nx --version
```

## Best Practices

1. **Use Nx Console**: VS Code extension for visual Nx commands
2. **Leverage caching**: Nx caches build and test outputs
3. **Run affected commands**: Only build/test what changed
4. **Keep workspace updated**: Regularly update Nx and Angular
5. **Follow Angular style guide**: Use Angular CLI schematics through Nx

## When to Use This Skill

Invoke this skill when:
- Generating Angular components, services, or other artifacts
- Running tests or builds in the frontend
- Working with the Nx monorepo structure
- Debugging Nx-related issues
- Optimizing build performance
