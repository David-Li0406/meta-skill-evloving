# Phase Development Checklist

## Pre-Implementation
- [ ] Read and understand the spec file
- [ ] Identify phase scope (backend/frontend/both)
- [ ] List all files to create/modify
- [ ] Identify external libraries needed
- [ ] Run exploration agents

## Exploration Verification
- [ ] Database schema understood (if needed)
- [ ] Similar patterns found in codebase
- [ ] Library documentation reviewed (if needed)
- [ ] No missing context

## Implementation Order

### Backend (if applicable)
1. [ ] Domain layer (entities, value objects, repository interfaces)
2. [ ] Application layer (use cases, DTOs)
3. [ ] Infrastructure layer (repository implementations, external services)
4. [ ] Presentation layer (handlers, middleware)

### Frontend (if applicable)
1. [ ] Types (interfaces, types)
2. [ ] API (api calls, react-query hooks)
3. [ ] Hooks (custom hooks)
4. [ ] Components (UI components)
5. [ ] Pages (page components)

## Post-Implementation
- [ ] Backend builds: `go build ./...`
- [ ] Backend lints: `go vet ./...`
- [ ] Frontend builds: `npm run build`
- [ ] Database verified (if changed)
- [ ] Spec file updated with completed items
