# ESLint

**Category**: developer-tools/linting
**Description**: ESLint - pluggable JavaScript and TypeScript linter for identifying and fixing code problems
**Homepage**: https://eslint.org

## Package Detection

### NPM
- `eslint`
- `@eslint/js`
- `eslint-config-prettier`
- `eslint-plugin-react`
- `eslint-plugin-vue`
- `eslint-plugin-import`
- `@typescript-eslint/eslint-plugin`
- `@typescript-eslint/parser`

## Configuration Files

- `.eslintrc`
- `.eslintrc.js`
- `.eslintrc.cjs`
- `.eslintrc.json`
- `.eslintrc.yaml`
- `.eslintrc.yml`
- `eslint.config.js` (flat config)
- `eslint.config.mjs`
- `eslint.config.cjs`
- `.eslintignore`

## Environment Variables

- `ESLINT_USE_FLAT_CONFIG`
- `ESLINT_CONFIG_LOOKUP`

## Detection Notes

- Look for eslint config files in repository root
- Check for eslint in devDependencies
- Flat config (eslint.config.js) is the new format for ESLint 9+
- Often used with Prettier for formatting

## Detection Confidence

- **Configuration File Detection**: 95% (HIGH)
- **Package Detection**: 95% (HIGH)
