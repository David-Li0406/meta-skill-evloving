# JavaScript Best Practices

A structured repository for creating and maintaining JavaScript coding standards optimized for AI agents and LLMs.

## Structure

- `rules/` - Individual rule files (one per rule)
  - `_sections.md` - Section metadata (titles, impacts, descriptions)
  - `_template.md` - Template for creating new rules
  - `prefix-description.md` - Individual rule files
- `metadata.json` - Document metadata (version, organization, abstract)
- `SKILL.md` - Skill definition with triggers
- **`AGENTS.md`** - Compiled output (generated)
- **`test-cases.json`** - Test cases for LLM evaluation (generated)

## Getting Started

1. Build AGENTS.md from rules:
   ```bash
   npm run build
   ```

2. Validate rule files:
   ```bash
   npm run validate
   ```

3. Extract test cases:
   ```bash
   npm run extract-tests
   ```

## Creating a New Rule

1. Copy `rules/_template.md` to `rules/prefix-description.md`
2. Choose the appropriate prefix for your section
3. Fill in the frontmatter and content
4. Ensure you have clear Incorrect/Correct examples
5. Run `npm run build` to regenerate AGENTS.md

## Section Prefixes

- `perf-` - Performance optimization
- `async-` - Async patterns and promises
- `security-` - Security best practices
- `error-` - Error handling
- `module-` - ES modules
- `data-` - Data structures
- `dom-` - DOM manipulation
- `modern-` - Modern JavaScript features

## Impact Levels

- `CRITICAL` - Highest priority, major performance/security gains
- `HIGH` - Significant improvements
- `MEDIUM-HIGH` - Moderate-high gains
- `MEDIUM` - Moderate improvements
- `LOW-MEDIUM` - Low-medium gains
- `LOW` - Incremental improvements

## Contributing

When adding or modifying rules:
1. Use the correct filename prefix for your section
2. Follow the `_template.md` structure
3. Include clear bad/good examples with explanations
4. Add appropriate tags
5. Run `npm run build` to regenerate AGENTS.md
