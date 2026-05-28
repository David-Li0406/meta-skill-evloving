# README Patterns

Detailed patterns for creating effective README files and project documentation.

## README Templates by Project Type

### TypeScript Library

```markdown
# library-name

Brief description of what the library does and its primary use case.

[![npm version](https://badge.fury.io/js/library-name.svg)](https://www.npmjs.com/package/library-name)
[![TypeScript](https://img.shields.io/badge/TypeScript-Ready-blue.svg)](https://www.typescriptlang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Feature 1** - Brief description
- **Feature 2** - Brief description
- **Feature 3** - Brief description

## Installation

\`\`\`bash
npm install library-name
# or
bun add library-name
# or
yarn add library-name
\`\`\`

## Quick Start

\`\`\`typescript
import { mainFunction } from 'library-name';

const result = mainFunction({
  option1: 'value',
  option2: true,
});

console.log(result);
\`\`\`

## API Reference

### `mainFunction(options)`

Brief description of the function.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `option1` | `string` | Yes | Description |
| `option2` | `boolean` | No | Description (default: `false`) |

**Returns:** `ResultType`

**Example:**

\`\`\`typescript
const result = mainFunction({ option1: 'test' });
\`\`\`

### `secondaryFunction(input)`

Brief description.

**Parameters:**
- `input` (`InputType`): Description

**Returns:** `OutputType`

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LIB_DEBUG` | Enable debug logging | `false` |
| `LIB_TIMEOUT` | Request timeout in ms | `5000` |

### Config File

Create `library-name.config.js`:

\`\`\`javascript
module.exports = {
  debug: true,
  timeout: 10000,
};
\`\`\`

## Examples

### Example 1: Basic Usage

\`\`\`typescript
import { mainFunction } from 'library-name';

const result = mainFunction({ option1: 'hello' });
console.log(result);
\`\`\`

### Example 2: Advanced Usage

\`\`\`typescript
import { mainFunction, configure } from 'library-name';

configure({ debug: true });

const result = mainFunction({
  option1: 'hello',
  option2: true,
});
\`\`\`

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## License

MIT - see [LICENSE](./LICENSE) for details.
```

### CLI Tool

```markdown
# cli-tool-name

Brief description of what the CLI does.

## Installation

\`\`\`bash
# Global installation
npm install -g cli-tool-name

# Or use npx
npx cli-tool-name <command>
\`\`\`

## Usage

\`\`\`bash
cli-tool-name <command> [options]
\`\`\`

### Commands

| Command | Description |
|---------|-------------|
| `init` | Initialize a new project |
| `build` | Build the project |
| `deploy` | Deploy to production |

### Global Options

| Option | Description |
|--------|-------------|
| `-v, --version` | Show version |
| `-h, --help` | Show help |
| `--debug` | Enable debug mode |

## Commands

### `init`

Initialize a new project.

\`\`\`bash
cli-tool-name init [project-name] [options]
\`\`\`

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `-t, --template` | Template to use | `default` |
| `--no-git` | Skip git initialization | `false` |

**Example:**

\`\`\`bash
cli-tool-name init my-project --template typescript
\`\`\`

### `build`

Build the project.

\`\`\`bash
cli-tool-name build [options]
\`\`\`

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --output` | Output directory | `dist` |
| `--minify` | Minify output | `true` |

## Configuration

Create `cli-tool.config.json`:

\`\`\`json
{
  "outputDir": "dist",
  "minify": true,
  "plugins": ["plugin-a", "plugin-b"]
}
\`\`\`

## License

MIT
```

### Web Application

```markdown
# app-name

Brief description of the web application.

![App Screenshot](./docs/screenshot.png)

## Features

- Feature 1
- Feature 2
- Feature 3

## Tech Stack

- **Frontend:** React, TypeScript, Tailwind CSS
- **Backend:** Node.js, Express
- **Database:** PostgreSQL
- **Deployment:** Docker, AWS

## Prerequisites

- Node.js 18+
- PostgreSQL 14+
- Docker (optional)

## Getting Started

### 1. Clone the repository

\`\`\`bash
git clone https://github.com/username/app-name.git
cd app-name
\`\`\`

### 2. Install dependencies

\`\`\`bash
npm install
\`\`\`

### 3. Set up environment

\`\`\`bash
cp .env.example .env
# Edit .env with your configuration
\`\`\`

### 4. Set up database

\`\`\`bash
npm run db:migrate
npm run db:seed
\`\`\`

### 5. Start development server

\`\`\`bash
npm run dev
\`\`\`

Open http://localhost:3000

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `JWT_SECRET` | Secret for JWT signing | Yes |
| `PORT` | Server port | No (default: 3000) |

## Project Structure

\`\`\`
app-name/
├── src/
│   ├── components/     # React components
│   ├── pages/          # Page components
│   ├── api/            # API routes
│   ├── lib/            # Utility functions
│   └── types/          # TypeScript types
├── prisma/             # Database schema
├── public/             # Static assets
└── tests/              # Test files
\`\`\`

## Available Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run start` | Start production server |
| `npm run test` | Run tests |
| `npm run lint` | Run linter |

## Deployment

### Docker

\`\`\`bash
docker build -t app-name .
docker run -p 3000:3000 app-name
\`\`\`

### Manual

\`\`\`bash
npm run build
npm run start
\`\`\`

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md)

## License

MIT
```

### Monorepo

```markdown
# monorepo-name

Brief description of the monorepo.

## Packages

| Package | Description | Version |
|---------|-------------|---------|
| [@scope/core](./packages/core) | Core functionality | [![npm](https://img.shields.io/npm/v/@scope/core.svg)](https://www.npmjs.com/package/@scope/core) |
| [@scope/cli](./packages/cli) | CLI tool | [![npm](https://img.shields.io/npm/v/@scope/cli.svg)](https://www.npmjs.com/package/@scope/cli) |
| [@scope/utils](./packages/utils) | Shared utilities | [![npm](https://img.shields.io/npm/v/@scope/utils.svg)](https://www.npmjs.com/package/@scope/utils) |

## Getting Started

\`\`\`bash
# Install dependencies
npm install

# Build all packages
npm run build

# Run tests
npm run test
\`\`\`

## Development

### Working on a specific package

\`\`\`bash
cd packages/core
npm run dev
\`\`\`

### Running tests

\`\`\`bash
# All packages
npm run test

# Specific package
npm run test --workspace=@scope/core
\`\`\`

## Publishing

\`\`\`bash
npm run release
\`\`\`

## License

MIT
```

## Section Patterns

### Installation Section

Always include multiple package managers:

```markdown
## Installation

\`\`\`bash
# npm
npm install package-name

# yarn
yarn add package-name

# pnpm
pnpm add package-name

# bun
bun add package-name
\`\`\`
```

### Quick Start Section

Minimal working example that can be copied:

```markdown
## Quick Start

\`\`\`typescript
import { createClient } from 'package-name';

const client = createClient({ apiKey: 'your-key' });
const result = await client.doSomething();
console.log(result);
\`\`\`
```

### API Reference Section

For inline API docs:

```markdown
## API

### `functionName(param1, param2?)`

Description of what the function does.

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `param1` | `string` | Yes | - | First parameter |
| `param2` | `Options` | No | `{}` | Configuration options |

**Returns:** `Promise<Result>`

**Throws:**
- `ValidationError` - If param1 is empty
- `NetworkError` - If request fails

**Example:**

\`\`\`typescript
const result = await functionName('value');
\`\`\`
```

### Configuration Section

Environment variables table format:

```markdown
## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `API_KEY` | API authentication key | Yes | - |
| `DEBUG` | Enable debug logging | No | `false` |
| `TIMEOUT` | Request timeout (ms) | No | `5000` |

### Configuration File

Create `config.json` in project root:

\`\`\`json
{
  "debug": false,
  "timeout": 5000,
  "plugins": []
}
\`\`\`
```

### Troubleshooting Section

Common issues table:

```markdown
## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `MODULE_NOT_FOUND` | Missing dependency | Run `npm install` |
| `ECONNREFUSED` | Server not running | Start the server first |
| `Invalid token` | Expired API key | Generate new key |
```

## Badge Patterns

### Standard Badge Set

```markdown
[![npm version](https://badge.fury.io/js/package-name.svg)](https://www.npmjs.com/package/package-name)
[![Build Status](https://github.com/username/repo/workflows/CI/badge.svg)](https://github.com/username/repo/actions)
[![Coverage Status](https://coveralls.io/repos/github/username/repo/badge.svg)](https://coveralls.io/github/username/repo)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![TypeScript](https://img.shields.io/badge/TypeScript-Ready-blue.svg)](https://www.typescriptlang.org/)
```

### Grouped Badges

```markdown
<!-- Badges -->
[![npm][npm-badge]][npm-url]
[![build][build-badge]][build-url]
[![coverage][coverage-badge]][coverage-url]

[npm-badge]: https://badge.fury.io/js/package-name.svg
[npm-url]: https://www.npmjs.com/package/package-name
[build-badge]: https://github.com/user/repo/workflows/CI/badge.svg
[build-url]: https://github.com/user/repo/actions
[coverage-badge]: https://coveralls.io/repos/github/user/repo/badge.svg
[coverage-url]: https://coveralls.io/github/user/repo
```

## CONTRIBUTING.md Template

```markdown
# Contributing to project-name

Thank you for your interest in contributing!

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/project-name`
3. Install dependencies: `npm install`
4. Create a branch: `git checkout -b feature/your-feature`

## Making Changes

1. Make your changes
2. Add tests for new functionality
3. Run tests: `npm test`
4. Run linter: `npm run lint`
5. Commit your changes (see commit guidelines below)

## Commit Guidelines

We use [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `test:` - Adding tests
- `refactor:` - Code refactoring
- `chore:` - Maintenance

Example: `feat: add support for custom templates`

## Pull Request Process

1. Update README.md if needed
2. Add entry to CHANGELOG.md
3. Ensure all tests pass
4. Request review from maintainers

## Code of Conduct

Be respectful and inclusive. See [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).
```

## ARCHITECTURE.md Template

```markdown
# Architecture

Overview of the system architecture.

## System Overview

\`\`\`
┌─────────────────────────────────────────────────────┐
│                     Client                          │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│                   API Gateway                       │
└─────────────────────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │ Service │    │ Service │    │ Service │
    │    A    │    │    B    │    │    C    │
    └─────────┘    └─────────┘    └─────────┘
         │               │               │
         └───────────────┼───────────────┘
                         ▼
                   ┌─────────┐
                   │ Database│
                   └─────────┘
\`\`\`

## Components

### Component A

**Purpose:** Brief description

**Responsibilities:**
- Responsibility 1
- Responsibility 2

**Dependencies:**
- Depends on Component B for X
- Uses Database for Y

### Component B

**Purpose:** Brief description

**Responsibilities:**
- Responsibility 1
- Responsibility 2

## Data Flow

1. Client sends request to API Gateway
2. Gateway routes to appropriate service
3. Service processes and returns response

## Key Decisions

| Decision | Rationale | Alternatives Considered |
|----------|-----------|-------------------------|
| Decision 1 | Reason | Alternative A, B |
| Decision 2 | Reason | Alternative C |

## Directory Structure

\`\`\`
src/
├── api/           # API layer
├── services/      # Business logic
├── models/        # Data models
├── utils/         # Utilities
└── config/        # Configuration
\`\`\`
```

## CHANGELOG.md Template

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature description

### Changed
- Change description

### Fixed
- Bug fix description

## [1.0.0] - 2024-01-15

### Added
- Initial release
- Feature A
- Feature B

### Changed
- Updated dependency X to version Y

### Fixed
- Fixed issue with Z

## [0.1.0] - 2024-01-01

### Added
- Initial beta release
```

## Best Practices

### Do

- Use consistent heading levels
- Include copy-paste-ready code examples
- Add tables for structured data
- Link to detailed docs where needed
- Keep Quick Start truly quick (< 10 lines)
- Test all code examples

### Don't

- Write walls of text
- Include implementation details in README
- Use outdated examples
- Skip installation instructions
- Forget to update after changes
- Include sensitive information
