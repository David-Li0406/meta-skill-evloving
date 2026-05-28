# Code Quality Skill

An AI skill for Claude Code that automatically analyzes, learns, and enforces code quality patterns within your codebase.

## Features

- **Pattern Detection**: Identifies naming conventions, import styles, API patterns, state management, and more
- **Anti-Pattern Detection**: Finds code smells, complexity issues, coupling problems, and security concerns
- **Config Integration**: Reads existing ESLint, Prettier, EditorConfig, TypeScript configs
- **Conflict Resolution**: Interactive MCQ-based resolution for ambiguous patterns
- **Metrics Collection**: LOC, function length, nesting depth, and complexity metrics
- **Multi-Language**: Supports JavaScript/TypeScript, Python, Go, Rust, and more

## Installation

### Using npx (Recommended)

```bash
npx add-skills code-quality
```

### Manual Installation

1. Clone this repository into your Claude Code skills directory:
```bash
git clone https://github.com/anthropics/code-quality-skills.git ~/.claude/skills/code-quality
```

2. Or copy the skill files to your project's `.claude/skills/` directory.

## Usage

### Triggering Code Analysis

There are several ways to trigger the code quality analysis:

#### 1. Direct Command

Ask Claude Code to analyze your code quality:

```
Analyze the code quality patterns in this project
```

```
What are the coding patterns used in this codebase?
```

```
Check this project for code smells and anti-patterns
```

#### 2. Pre-Code Generation

Before writing new code, ask Claude to learn the patterns first:

```
Learn the coding patterns in this project, then implement a new user service
```

```
What patterns should I follow when adding a new component to this project?
```

#### 3. Code Review Mode

Ask for a quality review of specific files or the entire project:

```
Review the code quality of src/services/
```

```
Find anti-patterns in the authentication module
```

#### 4. Specific Analysis Requests

Request specific types of analysis:

```
Analyze the naming conventions in this project
```

```
Check for complexity issues in the utils folder
```

```
What import patterns are used in this codebase?
```

### Thoroughness Levels

Specify how deep the analysis should go:

| Level | Command Example | Use Case |
|-------|-----------------|----------|
| Quick | `Do a quick code quality scan` | Pre-commit, CI checks |
| Medium | `Analyze code patterns` (default) | Regular analysis |
| Thorough | `Do a thorough code quality analysis` | Initial setup, major refactors |

### Example Workflows

#### Initial Project Setup

```
1. "Analyze the code quality patterns in this project thoroughly"
2. Review the generated patterns.md report
3. Approve or modify suggested patterns via MCQ prompts
4. Claude generates .code-quality.json with your preferences
5. Future code generation will follow these patterns
```

#### Pre-Commit Check

```
1. "Quick code quality check on my staged changes"
2. Claude scans only changed files
3. Reports any pattern violations or anti-patterns
4. Suggests fixes before commit
```

#### Code Review

```
1. "Review code quality in the new feature branch"
2. Claude analyzes all changes
3. Flags anti-patterns with severity levels
4. Provides specific fix suggestions
```

#### Learning Project Conventions

```
1. "What coding patterns should I follow in this project?"
2. Claude scans and summarizes existing patterns
3. Provides examples from the codebase
4. Ready to enforce patterns in new code
```

## Output Files

### patterns.md

Human-readable report containing:
- Summary statistics (files scanned, patterns found)
- Detected patterns by category
- Anti-patterns and code smells
- Recommendations

### .code-quality.json

Machine-readable configuration:
```json
{
  "version": "1.0",
  "generated": "2024-01-20T10:30:00Z",
  "project_type": "react-typescript",
  "patterns": {
    "naming": {
      "functions": "camelCase",
      "components": "PascalCase"
    },
    "api_calls": {
      "pattern": "react-query hooks",
      "confidence": "high"
    }
  },
  "custom_rules": [],
  "excluded_paths": ["node_modules/", "dist/"],
  "integrations": {
    "eslint": true,
    "prettier": true
  }
}
```

## Categories Analyzed

### Positive Patterns
- **Naming**: Variables, functions, classes, files, constants
- **Imports**: Ordering, paths, barrel exports, dynamic imports
- **API Calls**: Wrappers, error handling, caching
- **State Management**: Local, global, server, form state
- **Component Structure**: Organization, props, composition
- **Error Handling**: Boundaries, logging, recovery
- **Testing**: Location, naming, mocking strategies
- **Documentation**: Comments, JSDoc, type annotations
- **Async Patterns**: Promise handling, cancellation
- **Type Patterns**: Generics, type guards, utility types

### Anti-Patterns Detected
- **Code Smells**: God classes, feature envy, data clumps
- **Complexity**: Deep nesting, long functions, high cyclomatic complexity
- **Coupling**: Circular dependencies, tight coupling
- **Duplication**: Copy-paste code, repeated logic
- **Naming Issues**: Misleading names, magic numbers
- **Error Anti-Patterns**: Swallowed exceptions, generic catch
- **Security Smells**: Hardcoded secrets, SQL concatenation, eval usage

## Configuration

### Customizing Analysis

Create or edit `.code-quality.json` in your project root:

```json
{
  "excluded_paths": [
    "node_modules/",
    "dist/",
    "**/*.generated.ts"
  ],
  "custom_rules": [
    {
      "name": "API Response Wrapper",
      "category": "api_calls",
      "detection_regex": "ApiResponse<.*>",
      "enforcement": "required"
    }
  ],
  "thresholds": {
    "max_file_loc": 500,
    "max_function_loc": 50,
    "max_nesting_depth": 4,
    "max_parameters": 4
  }
}
```

### Integration with Existing Tools

The skill automatically reads and respects:
- `.editorconfig`
- `eslint.config.js` / `.eslintrc.*`
- `.prettierrc*`
- `tsconfig.json`
- `pyproject.toml`

## Confidence Scoring

Patterns are scored based on:
- Occurrence frequency (25%)
- Consistency ratio (25%)
- File coverage (20%)
- Recency of usage (10%)
- Author distribution (8%)
- Context consistency (7%)
- Config alignment (5%)

### Confidence Tiers

| Tier | Score | Action |
|------|-------|--------|
| High | 85-100 | Auto-applied |
| Medium-High | 70-84 | Applied with notification |
| Medium | 50-69 | MCQ confirmation required |
| Low | 25-49 | Flagged for manual review |
| Very Low | 0-24 | Report only |

## Troubleshooting

### Skill Not Triggering

Ensure the skill is properly installed:
```bash
# Check if skill is recognized
claude /skills
```

### Analysis Taking Too Long

Use a lower thoroughness level:
```
Do a quick code quality scan
```

### Too Many False Positives

Customize thresholds in `.code-quality.json`:
```json
{
  "thresholds": {
    "min_occurrences_for_pattern": 10,
    "min_consistency_ratio": 0.85
  }
}
```

### Excluding Files

Add paths to exclusion list:
```json
{
  "excluded_paths": [
    "**/*.test.ts",
    "legacy/**",
    "generated/**"
  ]
}
```

## Architecture

```
code-quality/
├── SKILL.md              # Main skill definition
├── agents/
│   ├── config-reader.md  # Config file parser (haiku)
│   ├── pattern-scanner.md # Code pattern analyzer (haiku)
│   └── conflict-resolver.md # Conflict resolution (sonnet)
├── references/
│   ├── pattern-categories.md
│   ├── confidence-scoring.md
│   ├── config-integrations.md
│   ├── shell-commands.md
│   └── best-practices/
│       ├── general.md
│       ├── javascript-typescript.md
│       ├── python.md
│       └── react.md
└── templates/
    ├── pattern-report.md
    ├── mcq-confirmation.md
    └── code-quality-config.json
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.
