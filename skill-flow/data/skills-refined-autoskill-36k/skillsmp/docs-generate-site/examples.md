# Documentation Site Generation Examples

Examples of Level 3 documentation site content from design docs.

## Example: effect-type-registry Site Docs

### Generated Structure

```text
website/docs/en/packages/effect-type-registry/
├── index.mdx                  # Landing page
├── _meta.json                 # Navigation
├── guides/
│   ├── getting-started.mdx   # Getting started
│   ├── caching.mdx           # Caching guide
│   └── performance.mdx       # Performance guide
├── concepts/
│   └── architecture.mdx      # Architecture overview
└── examples/
    ├── basic-usage.mdx       # Basic examples
    └── advanced.mdx          # Advanced examples
```

### Landing Page Features

The generated landing page (`index.mdx`) includes:

- Hero section with package name and tagline
- Feature cards highlighting key capabilities
- Quick code example preview
- Call-to-action buttons (Get Started, View on GitHub)
- Links to documentation sections

Content is extracted from design docs and simplified for users.

### Getting Started Guide

The getting started guide (`guides/getting-started.mdx`) provides:

- **Installation** - Package manager tabs (npm, pnpm, bun)
- **First Example** - Step-by-step working code
- **Understanding Basics** - Key concepts explained
- **Common Patterns** - Typical usage examples
- **Next Steps** - Links to deeper guides

Uses RSPress features like tabs and callouts for better UX.

### Concept Documentation

Concept docs (`concepts/architecture.mdx`) transform design architecture into
user-friendly explanations:

- High-level system overview
- Component descriptions (what they do, not how)
- Mermaid diagrams for visualization
- Benefits explained to users
- Links to related guides

Technical implementation details are simplified or omitted.

### Framework Features Used

#### Tabs

Used for multiple installation methods, code examples with different
approaches, or platform-specific instructions.

#### Callouts

- **Tip** - Helpful suggestions and best practices
- **Warning** - Important caveats to avoid issues
- **Note** - Additional context and information
- **Danger** - Critical warnings about destructive actions

#### Code Blocks

All code blocks include:

- Syntax highlighting
- Copy-to-clipboard button
- Language specification
- Inline comments for clarity

#### Mermaid Diagrams

Architecture and flow diagrams generated from design doc descriptions.

## Navigation Structure

Generated `_meta.json` organizes docs progressively:

```json
[
  {
    "text": "Getting Started",
    "link": "/guides/getting-started"
  },
  {
    "text": "Guides",
    "collapsible": true,
    "items": [
      {
        "text": "Caching",
        "link": "/guides/caching"
      },
      {
        "text": "Performance",
        "link": "/guides/performance"
      }
    ]
  },
  {
    "text": "Concepts",
    "collapsible": true,
    "items": [
      {
        "text": "Architecture",
        "link": "/concepts/architecture"
      }
    ]
  },
  {
    "text": "API Reference",
    "link": "/api/README"
  }
]
```

## Content Transformation Examples

### Architecture to User Concepts

**Design doc (technical):**

> Uses Effect-TS Layer system with three layers: HTTP, Cache, Registry.
> Layers composed via Layer.provide() for dependency injection.

**User concept (simplified):**

> The package has three main components that work together:
>
> 1. **HTTP Layer** - Fetches packages from npm
> 2. **Cache Layer** - Stores downloaded types locally
> 3. **Registry Layer** - Coordinates everything
>
> These work together automatically - no configuration needed.

### Implementation to Usage

**Design doc (internal):**

> VFS generation: pipe(packages, Effect.flatMap(fetchTypes),
> Effect.map(generateVFS))

**User guide (practical):**

> Generate a virtual file system:
>
> `const vfs = await registry.generateVFS(['zod@3.22.0']);`
>
> The VFS includes all type definitions for use with TypeScript tooling.

## Quality Checklist

Generated site docs meet these criteria:

- ✅ Engaging landing page with clear value
- ✅ Progressive getting started (beginner-friendly)
- ✅ Interactive elements (tabs, callouts, diagrams)
- ✅ Clear navigation structure
- ✅ Working, tested code examples
- ✅ Proper SEO metadata
- ✅ Mobile responsive
- ✅ Accessible heading structure
- ✅ Framework-specific syntax validated
- ✅ Cross-references functional
