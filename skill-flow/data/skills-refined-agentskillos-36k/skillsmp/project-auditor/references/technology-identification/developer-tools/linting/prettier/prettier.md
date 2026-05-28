# Prettier

**Category**: developer-tools/linting
**Description**: Prettier - opinionated code formatter supporting many languages
**Homepage**: https://prettier.io

## Package Detection

### NPM
- `prettier`
- `@prettier/plugin-php`
- `@prettier/plugin-ruby`
- `prettier-plugin-tailwindcss`
- `prettier-plugin-organize-imports`

## Configuration Files

- `.prettierrc`
- `.prettierrc.js`
- `.prettierrc.cjs`
- `.prettierrc.mjs`
- `.prettierrc.json`
- `.prettierrc.yaml`
- `.prettierrc.yml`
- `.prettierrc.toml`
- `prettier.config.js`
- `prettier.config.cjs`
- `prettier.config.mjs`
- `.prettierignore`

## Detection Notes

- Look for prettier config files in repository root
- Check for prettier in devDependencies
- Often used alongside ESLint
- .prettierignore specifies files to skip

## Detection Confidence

- **Configuration File Detection**: 95% (HIGH)
- **Package Detection**: 95% (HIGH)
