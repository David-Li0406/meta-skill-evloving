# Config Integrations

## Priority
1. EditorConfig (whitespace/end_of_line)
2. ESLint
3. Prettier
4. TSConfig/jsconfig
5. Language-specific (pyproject, pom.xml, etc.)

## Conflict detection
- indent: ESLint vs EditorConfig
- quotes/semi/trailing_comma: ESLint vs Prettier
- line endings: EditorConfig vs .gitattributes
- TS strictness vs inferred patterns

## Recommendations
- Prefer EditorConfig for whitespace; align ESLint indent with it.
- Use eslint-config-prettier (or equivalent) when Prettier present.
- Surface required parser options from TSConfig into ESLint if missing.
- Flag config drift when multiple configs found in monorepos; scope by package.
