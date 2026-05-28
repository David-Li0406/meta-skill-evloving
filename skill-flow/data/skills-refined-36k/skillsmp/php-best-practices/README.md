# PHP Best Practices

A structured repository for creating and maintaining PHP coding standards optimized for AI agents and LLMs.

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

## Section Prefixes

- `security-` - Security best practices
- `error-` - Error handling patterns
- `perf-` - Performance optimization
- `types-` - Type safety
- `oop-` - OOP patterns
- `psr-` - PSR standards compliance
- `test-` - Testing patterns
- `modern-` - Modern PHP features

## Impact Levels

- `CRITICAL` - Highest priority, major security/performance gains
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
