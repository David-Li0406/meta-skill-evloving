---
name: documentation-writing
description: Comprehensive guide for writing technical documentation including README files, API docs, user guides, architecture docs, and more. Use when creating or improving any form of documentation for software projects.
---

# Documentation Writing Skill

## When to Use This Skill

Use this skill when:

- Writing README files for projects
- Creating API documentation
- Writing user guides and tutorials
- Documenting architecture and design decisions
- Creating onboarding documentation
- Writing code comments and inline docs
- Developing knowledge base articles
- Creating changelogs and release notes

## Core Documentation Principles

### The 4 Types of Documentation

1. **Tutorials** - Learning-oriented (teaching)
   - Takes user through a series of steps
   - Helps beginners get started
   - Example: "Building Your First React App"

2. **How-To Guides** - Task-oriented (problem-solving)
   - Solves a specific problem
   - Assumes some knowledge
   - Example: "How to Add Authentication"

3. **Explanations** - Understanding-oriented (clarifying)
   - Explains concepts and context
   - Provides background knowledge
   - Example: "Understanding JWT Tokens"

4. **Reference** - Information-oriented (facts)
   - Technical descriptions
   - Accurate and complete
   - Example: "API Endpoint Reference"

### Writing Best Practices

**Clarity**

- Use simple, direct language
- Avoid jargon unless necessary
- Define technical terms on first use
- Use active voice: "Click the button" not "The button should be clicked"
- One idea per sentence

**Structure**

- Start with most important information
- Use headings to organize content
- Keep paragraphs short (3-5 sentences)
- Use lists for multiple items
- Add visual hierarchy

**Completeness**

- Answer who, what, when, where, why, and how
- Include prerequisites
- Provide examples
- Link to related documentation
- Include error handling

**Accuracy**

- Test all code examples
- Keep documentation updated with code
- Include version information
- Verify links work

## README File Templates

### Minimal README (Small Projects)

````markdown
# Project Name

Brief description of what this project does (1-2 sentences).

## Installation

```bash
npm install project-name
```
````

## Usage

```javascript
const project = require("project-name");
project.doSomething();
```

## License

MIT

````

### Standard README (Most Projects)
```markdown
# Project Name

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]
[![License](https://img.shields.io/badge/license-MIT-blue)]
[![Version](https://img.shields.io/badge/version-1.0.0-blue)]

Brief description of what this project does and why it exists.

## Features

- Feature one
- Feature two
- Feature three

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

- Node.js 18+
- npm or yarn
- PostgreSQL 14+

### Install Dependencies

```bash
npm install
````

### Environment Setup

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Required environment variables:

```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
API_KEY=your_api_key_here
PORT=3000
```

## Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Visit http://localhost:3000
```

## Usage

### Basic Example

```javascript
const { Client } = require("project-name");

const client = new Client({
  apiKey: "your-api-key",
});

await client.connect();
const result = await client.getData();
console.log(result);
```

### Advanced Example

```javascript
const client = new Client({
  apiKey: "your-api-key",
  timeout: 5000,
  retries: 3,
});

client.on("error", (error) => {
  console.error("Connection error:", error);
});

const data = await client.getData({
  filter: "active",
  limit: 100,
});
```

## API Documentation

See [API.md](./docs/API.md) for complete API reference.

## Configuration

| Option    | Type   | Default  | Description              |
| --------- | ------ | -------- | ------------------------ |
| `apiKey`  | string | required | Your API key             |
| `timeout` | number | 3000     | Request timeout in ms    |
| `retries` | number | 3        | Number of retry attempts |

## Project Structure

```
project-name/
├── src/
│   ├── index.js
│   ├── client.js
│   └── utils/
├── tests/
├── docs/
├── package.json
└── README.md
```

## Development

```bash
# Run tests
npm test

# Run linter
npm run lint

# Build for production
npm run build
```

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md).

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## Support

- Email: support@example.com
- Discord: [Join our community](https://discord.gg/example)
- Issues: [GitHub Issues](https://github.com/user/repo/issues)

## Acknowledgments

- Thanks to [contributor](https://github.com/contributor)
- Inspired by [project](https://github.com/project)

````

### Comprehensive README (Large Projects)
```markdown
# Project Name

<div align="center">
  <img src="logo.png" alt="Logo" width="200"/>

  <p>One-line tagline describing the project</p>

  [![Build](https://img.shields.io/github/workflow/status/user/repo/CI)]
  [![Coverage](https://img.shields.io/codecov/c/github/user/repo)]
  [![License](https://img.shields.io/badge/license-MIT-blue)]
  [![Downloads](https://img.shields.io/npm/dm/package-name)]
</div>

## Overview

Detailed description of what this project does, the problems it solves, and why someone should use it.

### Key Features

- **Fast** - Optimized for performance
- **Secure** - Built with security in mind
- **Lightweight** - Minimal dependencies
- **Customizable** - Highly configurable
- **Well-documented** - Comprehensive guides

### Live Demo

Try it out: [https://demo.example.com](https://demo.example.com)

### Screenshots

![Screenshot 1](screenshots/main.png)
![Screenshot 2](screenshots/feature.png)

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Examples](#examples)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [FAQ](#faq)
- [Roadmap](#roadmap)

## Installation

[Detailed installation instructions]

## Quick Start

[Step-by-step getting started guide]

## Documentation

- [User Guide](docs/USER_GUIDE.md)
- [API Reference](docs/API.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Contributing Guide](CONTRIBUTING.md)

## Examples

### Example 1: Basic Usage
[Code example]

### Example 2: Advanced Usage
[Code example]

See [examples/](examples/) directory for more.

## Configuration

[Configuration details]

## Deployment

[Deployment instructions]

## Contributing

[Contributing guidelines]

## FAQ

**Q: Common question?**
A: Answer to common question.

## Roadmap

- [x] Feature 1
- [x] Feature 2
- [ ] Feature 3
- [ ] Feature 4

## Performance

[Performance metrics and benchmarks]

## Security

[Security information]

## License

[License information]

## Team

[Team or author information]

## Acknowledgments

[Credits and acknowledgments]
````

## API Documentation

### REST API Documentation Template

```markdown
# API Documentation

## Base URL
```

https://api.example.com/v1

````

## Authentication

All requests require an API key in the header:

```bash
Authorization: Bearer YOUR_API_KEY
````

Get your API key from [Dashboard](https://example.com/dashboard).

## Endpoints

### Get Users

Retrieves a list of users.

**Endpoint:** `GET /users`

**Parameters:**

| Parameter | Type    | Required | Description                                 |
| --------- | ------- | -------- | ------------------------------------------- |
| `page`    | integer | No       | Page number (default: 1)                    |
| `limit`   | integer | No       | Items per page (default: 20, max: 100)      |
| `sort`    | string  | No       | Sort field (default: created_at)            |
| `order`   | string  | No       | Sort order: asc or desc (default: desc)     |
| `status`  | string  | No       | Filter by status: active, inactive, pending |

**Request Example:**

```bash
curl -X GET "https://api.example.com/v1/users?page=1&limit=20" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Response Example:**

```json
{
  "data": [
    {
      "id": "usr_123",
      "email": "user@example.com",
      "name": "John Doe",
      "status": "active",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "pages": 5
  }
}
```

**Response Codes:**

| Code | Description                             |
| ---- | --------------------------------------- |
| 200  | Success                                 |
| 400  | Bad Request - Invalid parameters        |
| 401  | Unauthorized - Invalid API key          |
| 429  | Too Many Requests - Rate limit exceeded |
| 500  | Server Error                            |

**Error Response:**

```json
{
  "error": {
    "code": "invalid_parameter",
    "message": "The 'limit' parameter must be between 1 and 100",
    "field": "limit"
  }
}
```

### Create User

Creates a new user.

**Endpoint:** `POST /users`

**Request Body:**

```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "role": "admin"
}
```

**Required Fields:**

- `email` (string) - Valid email address
- `name` (string) - User's full name

**Optional Fields:**

- `role` (string) - User role: admin, user (default: user)

**Response Example:**

```json
{
  "id": "usr_124",
  "email": "user@example.com",
  "name": "John Doe",
  "role": "user",
  "status": "pending",
  "created_at": "2024-01-15T10:30:00Z"
}
```

## Rate Limiting

- **Free tier:** 100 requests/hour
- **Pro tier:** 1,000 requests/hour
- **Enterprise:** Unlimited

Rate limit headers:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642252800
```

## Webhooks

Configure webhooks in your dashboard to receive real-time events.

**Events:**

- `user.created`
- `user.updated`
- `user.deleted`

**Webhook Payload:**

```json
{
  "event": "user.created",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "id": "usr_124",
    "email": "user@example.com"
  }
}
```

## SDKs

- [JavaScript/TypeScript](https://github.com/example/js-sdk)
- [Python](https://github.com/example/python-sdk)
- [Go](https://github.com/example/go-sdk)

````

### Function/Method Documentation Template
```javascript
/**
 * Fetches user data from the API
 *
 * @param {string} userId - The unique identifier of the user
 * @param {Object} options - Optional configuration
 * @param {boolean} options.includeMetadata - Include additional metadata (default: false)
 * @param {number} options.timeout - Request timeout in milliseconds (default: 5000)
 * @returns {Promise<User>} User object containing user data
 * @throws {NotFoundError} When user doesn't exist
 * @throws {AuthenticationError} When API key is invalid
 *
 * @example
 * // Basic usage
 * const user = await getUser('usr_123');
 *
 * @example
 * // With options
 * const user = await getUser('usr_123', {
 *   includeMetadata: true,
 *   timeout: 10000
 * });
 */
async function getUser(userId, options = {}) {
  // Implementation
}
````

## Architecture Documentation

### Architecture Decision Record (ADR) Template

```markdown
# ADR-001: Use PostgreSQL for Primary Database

## Status

Accepted

## Context

We need to choose a database for our application. Requirements:

- ACID compliance for financial transactions
- Complex querying capabilities
- Good performance for read-heavy workload
- Strong community support
- Mature ecosystem

## Decision

We will use PostgreSQL 15 as our primary database.

## Consequences

### Positive

- Strong ACID guarantees
- Excellent JSON support for flexible schema
- Advanced indexing options
- Mature replication solutions
- Great tooling ecosystem
- Free and open source

### Negative

- Requires more operational expertise than managed solutions
- Vertical scaling limitations
- Need to manage backups and replication

### Neutral

- Will use pgBouncer for connection pooling
- Planning to use TimescaleDB extension for time-series data

## Alternatives Considered

### MySQL

- Pros: Simpler replication, large community
- Cons: Weaker JSON support, less advanced features

### MongoDB

- Pros: Flexible schema, easier horizontal scaling
- Cons: No ACID guarantees across documents, less mature for our use case

## Notes

- Decision made: 2024-01-15
- Reviewed by: Engineering team
- Next review: 2024-07-15
```

### System Architecture Document

```markdown
# System Architecture

## Overview

High-level description of the system.

## Architecture Diagram
```

[Include diagrams using Mermaid, PlantUML, or images]

```

## Components

### Frontend
- **Technology:** React 18 with TypeScript
- **State Management:** Redux Toolkit
- **Styling:** Tailwind CSS
- **Hosting:** Vercel

### Backend API
- **Technology:** Node.js 18 with Express
- **Database:** PostgreSQL 15
- **Cache:** Redis 7
- **Authentication:** JWT tokens
- **Hosting:** AWS ECS

### Database Schema
[Include schema diagram or description]

### External Services
- **Email:** SendGrid
- **Payment:** Stripe
- **Storage:** AWS S3

## Data Flow

1. User makes request to frontend
2. Frontend calls backend API
3. Backend validates JWT token
4. Backend queries database
5. Backend returns response
6. Frontend updates UI

## Security

- TLS encryption for all connections
- JWT tokens with 1-hour expiration
- API rate limiting (100 req/min per IP)
- Database encryption at rest
- Regular security audits

## Scalability

- Horizontal scaling for API servers
- Database read replicas for read-heavy operations
- Redis cache for frequently accessed data
- CDN for static assets

## Monitoring

- Application logs → CloudWatch
- Metrics → Prometheus + Grafana
- Error tracking → Sentry
- Uptime monitoring → Pingdom
```

## User Guide Documentation

### Tutorial Template

````markdown
# Tutorial: Building Your First Widget

In this tutorial, you'll learn how to create a basic widget from scratch.

**What you'll build:** A simple counter widget
**Time to complete:** 15 minutes
**Prerequisites:**

- Basic JavaScript knowledge
- Node.js installed

## Step 1: Set Up Your Project

Create a new directory and initialize npm:

```bash
mkdir my-widget
cd my-widget
npm init -y
```
````

You should see output like:

```
Wrote to /path/to/my-widget/package.json
```

## Step 2: Install Dependencies

Install the widget framework:

```bash
npm install widget-framework
```

## Step 3: Create Your Widget

Create a new file called `counter.js`:

```javascript
const { Widget } = require("widget-framework");

class Counter extends Widget {
  constructor() {
    super();
    this.count = 0;
  }

  increment() {
    this.count++;
    this.render();
  }

  render() {
    return `Count: ${this.count}`;
  }
}

module.exports = Counter;
```

Let's break down what this code does:

- Line 1: Import the Widget class
- Line 3-6: Create a Counter class that extends Widget
- Line 5: Initialize count to 0
- Line 8-11: Define increment method
- Line 13-15: Define render method

## Step 4: Test Your Widget

Create `test.js`:

```javascript
const Counter = require("./counter");

const myCounter = new Counter();
console.log(myCounter.render()); // Count: 0

myCounter.increment();
console.log(myCounter.render()); // Count: 1
```

Run it:

```bash
node test.js
```

## Next Steps

Congratulations! You've created your first widget. Here's what to learn next:

- [Adding Event Listeners](./event-listeners.md)
- [Styling Your Widget](./styling.md)
- [Advanced Widget Patterns](./advanced.md)

## Troubleshooting

**Problem:** "Cannot find module 'widget-framework'"
**Solution:** Make sure you ran `npm install widget-framework`

**Problem:** Widget doesn't render
**Solution:** Check that you're calling the render() method

````

### How-To Guide Template
```markdown
# How to Add Authentication

This guide shows you how to add JWT authentication to your application.

**Prerequisites:**
- Existing Express.js application
- User model already set up

**Time:** ~20 minutes

## Install Dependencies

```bash
npm install jsonwebtoken bcrypt
````

## Step 1: Create Authentication Middleware

Create `middleware/auth.js`:

```javascript
const jwt = require("jsonwebtoken");

function authenticate(req, res, next) {
  const token = req.header("Authorization")?.replace("Bearer ", "");

  if (!token) {
    return res.status(401).json({ error: "No token provided" });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    res.status(401).json({ error: "Invalid token" });
  }
}

module.exports = authenticate;
```

## Step 2: Create Login Endpoint

Add to your routes:

```javascript
const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");
const User = require("./models/User");

app.post("/login", async (req, res) => {
  const { email, password } = req.body;

  // Find user
  const user = await User.findOne({ email });
  if (!user) {
    return res.status(401).json({ error: "Invalid credentials" });
  }

  // Check password
  const validPassword = await bcrypt.compare(password, user.password);
  if (!validPassword) {
    return res.status(401).json({ error: "Invalid credentials" });
  }

  // Generate token
  const token = jwt.sign(
    { id: user.id, email: user.email },
    process.env.JWT_SECRET,
    { expiresIn: "7d" },
  );

  res.json({ token });
});
```

## Step 3: Protect Routes

Use the middleware on protected routes:

```javascript
const authenticate = require("./middleware/auth");

app.get("/profile", authenticate, async (req, res) => {
  const user = await User.findById(req.user.id);
  res.json(user);
});
```

## Testing

Test the login endpoint:

```bash
curl -X POST http://localhost:3000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

Use the token:

```bash
curl http://localhost:3000/profile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Common Issues

**401 Unauthorized:** Check that you're including the token in the Authorization header

**500 Server Error:** Verify JWT_SECRET is set in your environment variables

## See Also

- [User Registration Guide](./registration.md)
- [Password Reset Flow](./password-reset.md)
- [OAuth Integration](./oauth.md)

````

## Code Comments

### Good Comment Examples

```javascript
// GOOD: Explains WHY, not WHAT
// Retry failed requests up to 3 times to handle transient network errors
const MAX_RETRIES = 3;

// BAD: States the obvious
// Set MAX_RETRIES to 3
const MAX_RETRIES = 3;

// GOOD: Provides context for non-obvious code
// Use binary search instead of linear - dataset is always sorted
// and can contain millions of records
function findUser(id, users) {
  // Implementation
}

// GOOD: Warns about gotchas
// Note: This function modifies the original array
function sortInPlace(arr) {
  // Implementation
}

// GOOD: Explains complex logic
// Calculate compound interest: A = P(1 + r/n)^(nt)
// P = principal, r = rate, n = compounds per year, t = years
function calculateInterest(principal, rate, years) {
  // Implementation
}

// GOOD: TODOs with context
// TODO: Optimize this query - currently takes 2s on large datasets
// Consider adding index on user_id column
function getOrders(userId) {
  // Implementation
}
````

### When to Comment

✅ **Do comment:**

- Complex algorithms or business logic
- Non-obvious workarounds
- Performance optimizations
- Security considerations
- Integration quirks
- Regex patterns
- Magic numbers

❌ **Don't comment:**

- Self-explanatory code
- Redundant information
- Outdated information
- Code that should be rewritten instead

## CHANGELOG Template

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Feature in development

## [1.2.0] - 2024-01-15

### Added

- New user dashboard with analytics
- Export data to CSV functionality
- Dark mode theme option

### Changed

- Improved performance of search by 50%
- Updated user profile layout
- Migrated to PostgreSQL 15

### Deprecated

- Old API endpoints (will be removed in v2.0)
  - `/api/v1/users/list` → use `/api/v1/users`

### Fixed

- Fixed memory leak in background worker
- Corrected timezone handling in reports
- Resolved issue with password reset emails

### Security

- Updated dependencies to patch vulnerabilities
- Added rate limiting to prevent brute force attacks

## [1.1.0] - 2023-12-01

### Added

- User authentication system
- Email notifications

### Fixed

- Fixed login redirect bug

## [1.0.0] - 2023-11-01

### Added

- Initial release
- Basic user management
- Dashboard features

[Unreleased]: https://github.com/user/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/user/repo/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/user/repo/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/user/repo/releases/tag/v1.0.0
```

## Contributing Guide Template

```markdown
# Contributing Guide

Thank you for considering contributing to this project!

## Code of Conduct

Be respectful, inclusive, and professional.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title** - "Login fails with 500 error" not "Bug in app"
- **Steps to reproduce** - Step-by-step instructions
- **Expected behavior** - What should happen
- **Actual behavior** - What actually happens
- **Environment** - OS, browser, version
- **Screenshots** - If applicable

**Example:**
```

Title: Login fails with 500 error when using special characters in password

Steps to reproduce:

1. Go to login page
2. Enter email: user@example.com
3. Enter password containing @#$
4. Click login

Expected: Should login successfully
Actual: Returns 500 Internal Server Error

Environment: Chrome 120, macOS 14

```

### Suggesting Features

Feature requests should include:
- **Use case** - Why is this needed?
- **Proposed solution** - How should it work?
- **Alternatives** - What else did you consider?

### Pull Requests

1. **Fork the repository**
2. **Create a branch** - `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Write tests**
5. **Run tests** - `npm test`
6. **Commit** - Use conventional commits
7. **Push** - `git push origin feature/amazing-feature`
8. **Open PR** - Fill out the template

#### Pull Request Guidelines

- Follow existing code style
- Write meaningful commit messages
- Add tests for new features
- Update documentation
- Keep PRs focused (one feature/fix per PR)
- Respond to review feedback

#### Commit Message Format

```

feat: add user profile page
fix: resolve login redirect bug
docs: update API documentation
test: add tests for auth service
refactor: simplify database queries

````

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/repo.git

# Install dependencies
npm install

# Create .env file
cp .env.example .env

# Run tests
npm test

# Start dev server
npm run dev
````

## Code Style

- Use ESLint configuration
- Run `npm run lint` before committing
- Use Prettier for formatting

## Testing

- Write unit tests for new features
- Maintain test coverage above 80%
- Run full test suite before submitting PR

## Questions?

Feel free to ask questions in:

- GitHub Discussions
- Discord: [link]
- Email: dev@example.com

````

## Documentation Checklist

### Before Publishing Documentation

- [ ] Spell check and grammar check
- [ ] All code examples tested and working
- [ ] All links verified and working
- [ ] Screenshots up to date
- [ ] Version numbers correct
- [ ] Prerequisites clearly stated
- [ ] Error messages documented
- [ ] Common pitfalls addressed
- [ ] Related documentation linked
- [ ] Table of contents updated
- [ ] Reviewed by someone else
- [ ] Accessible (clear language, alt text for images)

## Writing Style Guide

### Tone
- **Professional but friendly**
- Use "you" to address the reader
- Use "we" for inclusive language
- Avoid jargon when possible
- Be concise but complete

### Formatting
- **Bold** for UI elements: "Click the **Submit** button"
- `Code` for code, commands, filenames
- *Italics* for emphasis (sparingly)
- > Blockquotes for important notes

### Language
- Active voice: "Run the command" not "The command should be run"
- Present tense: "The function returns" not "The function will return"
- Second person: "You can configure" not "One can configure"
- Simple words: "use" not "utilize", "help" not "facilitate"

### Structure
```markdown
# Title (H1 - Only one per document)

Brief introduction paragraph.

## Main Section (H2)

Content for this section.

### Subsection (H3)

More specific content.

#### Sub-subsection (H4)

Even more specific.
````

## Tools and Resources

### Documentation Generators

- **JSDoc** - JavaScript documentation
- **Sphinx** - Python documentation
- **Swagger/OpenAPI** - API documentation
- **Docusaurus** - Documentation websites
- **MkDocs** - Markdown-based documentation

### Diagramming

- **Mermaid** - Text-based diagrams in Markdown
- **PlantUML** - UML diagrams
- **Draw.io** - Visual diagrams
- **Excalidraw** - Hand-drawn style diagrams

### Writing Tools

- **Grammarly** - Grammar and style
- **Hemingway** - Readability
- **Vale** - Linting for prose
- **markdownlint** - Markdown formatting

## Quick Reference

### Markdown Basics

````markdown
# Heading 1

## Heading 2

### Heading 3

**bold text**
_italic text_
`code`

- Bullet list

1. Numbered list

[Link text](https://example.com)
![Image alt text](image.png)

> Blockquote

`code block`

| Table | Header |
| ----- | ------ |
| Data  | Data   |
````

### Common Sections for README

- Title and description
- Badges (build, coverage, version)
- Features
- Installation
- Quick start
- Usage examples
- API documentation
- Configuration
- Contributing
- License
- Support/Contact

### API Documentation Sections

- Overview
- Authentication
- Base URL
- Endpoints (for each: method, parameters, examples, responses)
- Error codes
- Rate limiting
- Webhooks (if applicable)
- SDKs
- Changelog

## Tips for Effective Documentation

1. **Start with why** - Explain the purpose before the details
2. **Show, don't just tell** - Include examples
3. **Keep it current** - Update docs with code changes
4. **Make it scannable** - Use headings, lists, formatting
5. **Test everything** - Verify all code examples work
6. **Get feedback** - Have others review
7. **Version your docs** - Match docs to software versions
8. **Make it searchable** - Use descriptive headings
9. **Link related content** - Help users discover more
10. **Consider your audience** - Write for their skill level

## Common Documentation Mistakes

❌ **Assuming knowledge** - Always state prerequisites
❌ **Skipping examples** - Code examples are crucial
❌ **Outdated content** - Keep in sync with code
❌ **Too much detail** - Know when to link elsewhere
❌ **No context** - Explain why, not just how
❌ **Poor organization** - Use clear structure
❌ **Broken links** - Check links regularly
❌ **No error handling** - Document what can go wrong
❌ **Inconsistent style** - Follow a style guide
❌ **Writing for yourself** - Write for your users
