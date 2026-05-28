# README Templates and Best Practices

## Essential README Sections

### Project Title and Description

```markdown
# Project Name

[![Build Status](https://github.com/owner/repo/workflows/CI/badge.svg)](https://github.com/owner/repo/actions)
[![npm version](https://badge.fury.io/js/package-name.svg)](https://www.npmjs.com/package/package-name)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

One-paragraph description of what this project does and who it's for.
Focus on the problem it solves, not implementation details.
```

### Installation

```markdown
## Installation

### Prerequisites

- Node.js >= 18.0.0
- npm >= 9.0.0

### Quick Start

\`\`\`bash
npm install package-name
\`\`\`

### From Source

\`\`\`bash
git clone https://github.com/owner/repo.git
cd repo
npm install
npm run build
\`\`\`
```

### Usage

```markdown
## Usage

### Basic Example

\`\`\`javascript
import { Client } from 'package-name';

const client = new Client({ apiKey: 'your-key' });
const result = await client.doSomething();
console.log(result);
\`\`\`

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `apiKey` | string | required | Your API key |
| `timeout` | number | 5000 | Request timeout in ms |
| `retries` | number | 3 | Number of retry attempts |

### Advanced Usage

\`\`\`javascript
// Show a more complex example
const client = new Client({
  apiKey: process.env.API_KEY,
  timeout: 10000,
  onError: (err) => console.error(err)
});
\`\`\`
```

### API Reference

```markdown
## API Reference

### `Client(options)`

Creates a new client instance.

**Parameters:**
- `options.apiKey` (string, required): Authentication key
- `options.baseUrl` (string, optional): API base URL

**Returns:** Client instance

**Example:**
\`\`\`javascript
const client = new Client({ apiKey: 'xxx' });
\`\`\`

### `client.fetch(endpoint, params)`

Fetches data from the API.

**Parameters:**
- `endpoint` (string): API endpoint path
- `params` (object, optional): Query parameters

**Returns:** Promise<Response>

**Throws:**
- `AuthenticationError`: Invalid API key
- `RateLimitError`: Too many requests
```

### Contributing

```markdown
## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) first.

### Development Setup

\`\`\`bash
git clone https://github.com/owner/repo.git
cd repo
npm install
npm test
\`\`\`

### Running Tests

\`\`\`bash
npm test              # Run all tests
npm run test:watch    # Watch mode
npm run test:coverage # With coverage
\`\`\`

### Code Style

This project uses ESLint and Prettier. Run `npm run lint` before committing.
```

### License

```markdown
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

## Complete Template: Library/Package

```markdown
# @scope/package-name

[![npm](https://img.shields.io/npm/v/@scope/package-name)](https://www.npmjs.com/package/@scope/package-name)
[![CI](https://github.com/owner/repo/actions/workflows/ci.yml/badge.svg)](https://github.com/owner/repo/actions)
[![codecov](https://codecov.io/gh/owner/repo/branch/main/graph/badge.svg)](https://codecov.io/gh/owner/repo)

Brief description of what the library does and why someone would use it.

## Features

- Feature 1 with brief explanation
- Feature 2 with brief explanation
- Feature 3 with brief explanation

## Installation

\`\`\`bash
npm install @scope/package-name
\`\`\`

## Quick Start

\`\`\`javascript
import { something } from '@scope/package-name';

// Minimal working example
const result = something();
\`\`\`

## Documentation

- [API Reference](docs/api.md)
- [Examples](examples/)
- [Migration Guide](docs/migration.md)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

[MIT](LICENSE)
```

## Complete Template: Application/Service

```markdown
# Application Name

Brief description of what this application does.

## Features

- Feature 1
- Feature 2
- Feature 3

## Prerequisites

- Docker >= 20.10
- Node.js >= 18 (for local development)

## Quick Start

### Using Docker

\`\`\`bash
docker compose up -d
\`\`\`

The application will be available at http://localhost:3000

### Local Development

\`\`\`bash
cp .env.example .env
npm install
npm run dev
\`\`\`

## Configuration

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | required |
| `PORT` | Server port | 3000 |
| `LOG_LEVEL` | Logging verbosity | info |

## Architecture

\`\`\`
src/
├── api/          # REST API endpoints
├── services/     # Business logic
├── models/       # Data models
└── utils/        # Shared utilities
\`\`\`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/users` | List users |
| POST | `/api/users` | Create user |

See [API Documentation](docs/api.md) for complete reference.

## Deployment

### Production

\`\`\`bash
docker build -t app:latest .
docker run -p 3000:3000 --env-file .env.prod app:latest
\`\`\`

### Kubernetes

See [kubernetes/](kubernetes/) for Helm charts and manifests.

## Monitoring

- Health endpoint: `/api/health`
- Metrics: `/metrics` (Prometheus format)
- Logs: JSON format to stdout

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## License

[MIT](LICENSE)
```

## Complete Template: CLI Tool

```markdown
# cli-tool

Command-line tool for doing X.

## Installation

### Homebrew (macOS/Linux)

\`\`\`bash
brew install owner/tap/cli-tool
\`\`\`

### npm

\`\`\`bash
npm install -g cli-tool
\`\`\`

### Binary Download

Download the latest release from [Releases](https://github.com/owner/repo/releases).

## Usage

\`\`\`bash
cli-tool [command] [options]
\`\`\`

### Commands

#### `init`

Initialize a new project.

\`\`\`bash
cli-tool init [project-name]

Options:
  --template <name>  Project template (default: "basic")
  --no-git           Skip git initialization
\`\`\`

#### `build`

Build the project.

\`\`\`bash
cli-tool build [options]

Options:
  --output <dir>   Output directory (default: "dist")
  --watch          Watch for changes
  --minify         Minify output
\`\`\`

### Examples

\`\`\`bash
# Initialize new project
cli-tool init my-project --template typescript

# Build with options
cli-tool build --output ./build --minify

# Watch mode
cli-tool build --watch
\`\`\`

## Configuration

Create `cli-tool.config.js` in your project root:

\`\`\`javascript
module.exports = {
  output: './dist',
  minify: true,
  plugins: []
};
\`\`\`

## License

[MIT](LICENSE)
```

## Best Practices

| Do | Don't |
|----|-------|
| Start with what, not how | Begin with implementation details |
| Show working examples | Show incomplete snippets |
| Keep examples minimal | Include every option |
| Update with releases | Let docs go stale |
| Use consistent formatting | Mix styles |
| Include error messages | Assume happy path only |
| Link to detailed docs | Put everything in README |

## README Checklist

- [ ] Clear project name and description
- [ ] Badges (build, coverage, npm version)
- [ ] Installation instructions
- [ ] Minimal working example
- [ ] Configuration options documented
- [ ] Link to full documentation
- [ ] Contributing guidelines
- [ ] License information
- [ ] Prerequisites listed
- [ ] Screenshots/GIFs for visual tools
