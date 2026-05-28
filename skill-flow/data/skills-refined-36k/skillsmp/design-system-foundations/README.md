# Design System Foundations Skill

Expert en Design Systems avec approche **Atomic Design** industrielle pour structurer les fondations, atomes, molécules et templates de manière cohérente et scalable.

## Quick Start

```bash
# Invoke the skill
/skill design-system-foundations

# Or ask directly
"Help me create a color palette for my design system"
"What spacing tokens should I define?"
"How do I structure a button component?"
```

## Architecture

```
design-system-foundations/
├── SKILL.md                    # Main orchestrator (entry point)
├── CHANGELOG.md                # Version history
├── README.md                   # This file
├── agents/
│   ├── foundations/            # Design tokens layer
│   │   ├── orchestrator.md
│   │   ├── colors.md           # Color system, palettes, semantics
│   │   ├── typography.md       # Font scale, loading, accessibility
│   │   ├── spacing.md          # 8pt system, radius, layout
│   │   └── shadows.md          # Elevation, z-index, focus rings
│   ├── atoms/                  # Smallest UI elements
│   │   ├── orchestrator.md
│   │   ├── buttons.md          # Variants, sizes, states
│   │   ├── inputs.md           # Form controls, validation
│   │   ├── labels.md           # Tags, chips, form labels
│   │   ├── icons.md            # Icon system, sizing
│   │   └── badges.md           # Status, notifications
│   ├── molecules/              # Composed components
│   │   ├── orchestrator.md
│   │   ├── forms.md            # FormField, validation patterns
│   │   ├── cards.md            # Product, user, stats cards
│   │   ├── navigation.md       # Navbar, tabs, breadcrumbs
│   │   ├── modals.md           # Dialog, sheet, popover
│   │   └── alerts.md           # Inline, banner, toast
│   └── templates/              # Page structures
│       ├── orchestrator.md
│       ├── hero-sections.md    # Landing page blocks
│       ├── layouts.md          # Dashboard, auth, marketing
│       └── pages.md            # List, detail, error pages
├── docs/
│   ├── getting-started.md      # Quick start guide + cn() utility
│   ├── naming-conventions.md   # BEM, tokens, CSS Nesting
│   ├── animation-performance.md # GPU-accelerated animations
│   ├── testing-guide.md        # Jest, Testing Library
│   ├── dark-mode.md            # Theme implementation
│   ├── bundle-optimization.md  # Tree-shaking, code-splitting
│   └── accessibility-checklist.md # WCAG AA compliance
├── tests/
│   ├── run-tests.sh            # Test runner (Node.js 14+)
│   ├── config.js               # Centralized test config
│   ├── utils.js                # Shared utilities
│   └── validate-*.test.js      # 5 validation suites
└── references/
    └── resources.md            # External tools and resources
```

## Key Features

### Foundations
- **Colors**: 10-level palettes (50-900), semantic tokens, WCAG AA contrast
- **Typography**: Modular scale (1.25), fluid typography, font loading optimization
- **Spacing**: 8pt grid system, semantic tokens (inset, stack, inline)
- **Shadows**: 5-level elevation, z-index scale, focus rings

### Components
- **21 agents** (4 orchestrators + 17 specialized) with CSS + React/TypeScript
- **Accessibility-first**: WCAG AA contrast ratios, ARIA attributes, keyboard navigation
- **Dark mode ready**: CSS custom properties with semantic tokens
- **Storybook examples**: Documentation patterns included

### Quality Assurance
- **5 validation test suites** with JSON output for CI
- **GitHub Actions workflow** for automated testing
- **YAML frontmatter** on all agents for metadata

### Documentation
- Migration guides (Bootstrap, Tailwind, legacy CSS)
- Common pitfalls and troubleshooting
- Bundle optimization strategies
- Testing patterns with jest-axe

## Relation to Other Skills

| Skill | Scope | Relation |
|-------|-------|----------|
| **design-system-foundations** | Token architecture, component patterns, CSS/React implementation | Core design system building |
| **web-dev-process** | Development workflow, phases, delivery | Uses design system in implementation phase |
| **wordpress-gutenberg-expert** | WordPress/Gutenberg development | Can apply design system tokens to WP themes |

This skill focuses on the **technical implementation** of design systems, not the visual design process itself. It's ideal for:
- Converting Figma/Sketch designs to code
- Establishing token architecture
- Building component libraries
- Auditing existing design systems

## Version

**v1.1.0** (2025-12-22)

See [CHANGELOG.md](./CHANGELOG.md) for full history.

## Usage Examples

### Creating a color system
```
"I have a brand color #2563eb. Help me create a complete color system with semantic tokens."
```

### Building a button component
```
"Create a button component with primary, secondary, and ghost variants following BEM naming."
```

### Auditing accessibility
```
"Review my badge component for WCAG AA compliance."
```

### Setting up dark mode
```
"How do I implement dark mode with CSS custom properties?"
```
