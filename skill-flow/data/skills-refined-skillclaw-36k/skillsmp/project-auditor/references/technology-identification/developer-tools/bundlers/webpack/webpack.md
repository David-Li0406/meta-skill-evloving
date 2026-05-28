# Webpack

**Category**: developer-tools/bundlers
**Description**: Webpack - powerful module bundler for JavaScript applications
**Homepage**: https://webpack.js.org

## Package Detection

### NPM
- `webpack`
- `webpack-cli`
- `webpack-dev-server`
- `webpack-merge`
- `html-webpack-plugin`
- `mini-css-extract-plugin`
- `css-loader`
- `style-loader`
- `babel-loader`
- `ts-loader`

## Configuration Files

- `webpack.config.js`
- `webpack.config.ts`
- `webpack.config.cjs`
- `webpack.config.mjs`
- `webpack.common.js`
- `webpack.dev.js`
- `webpack.prod.js`

## Detection Notes

- Look for webpack.config.js in repository root
- Check for webpack in dependencies/devDependencies
- Often used with Babel for transpilation
- May be hidden behind framework CLI (Create React App, etc.)

## Detection Confidence

- **Configuration File Detection**: 95% (HIGH)
- **Package Detection**: 95% (HIGH)
