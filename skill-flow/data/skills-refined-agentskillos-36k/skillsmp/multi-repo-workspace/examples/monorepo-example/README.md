# Monorepo Example

This example demonstrates how to configure a monorepo workspace with multiple packages.

## Structure

```
monorepo/
├── packages/
│   ├── web-app/              # React frontend
│   │   └── .claude/
│   │       ├── config.json
│   │       └── context.md
│   ├── mobile-app/           # React Native mobile
│   │   └── .claude/
│   │       ├── config.json
│   │       └── context.md
│   ├── shared-ui/            # Shared components
│   │   └── .claude/
│   │       ├── config.json
│   │       └── context.md
│   └── api-client/           # API client library
│       └── .claude/
│           ├── config.json
│           └── context.md
├── .workspace/
│   └── config.json
└── package.json              # Root package.json
```

## Workspace Configuration

See `.workspace/config.json` for the complete workspace setup.

## Usage with Claude

```
@workspace init monorepo
# Claude will detect all packages in packages/

@workspace analyze
# Shows dependency graph and tech stack

@workspace task "Add dark mode support"
# Claude identifies: web-app, mobile-app, shared-ui need changes
```

## Key Features

- **Shared dependencies**: All packages use the same version of React
- **Internal packages**: Packages reference each other via workspace protocol
- **Consistent tooling**: ESLint, Prettier, TypeScript configs shared
- **Coordinated releases**: Version bumps coordinated across packages

## Dependencies

```
web-app → shared-ui, api-client
mobile-app → shared-ui, api-client
shared-ui → (no internal deps)
api-client → (no internal deps)
```

## Commands

```bash
# Install all dependencies
npm install

# Run all packages in dev mode
npm run dev

# Build all packages
npm run build

# Test all packages
npm test
```
