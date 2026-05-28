# ESLint Configuration for JavaScript

当涉及 JavaScript 代码编写或修改时，必须遵循以下规范：

- **JSDoc 类型标注**: 必须使用 JSDoc 对所有公共变量、函数参数及返回值进行明确的类型标注。
- **ESLint 配置**: 基于 `airbnb-base` 的具体要求如下：

```javascript
{
  semi: ['error', 'always'],
  'semi-spacing': ['error', { before: false, after: true }],
  quotes: ['error', 'single', { avoidEscape: true }],
  indent: ['error', 2],
  'keyword-spacing': ['error', {
    before: true,
    after: true,
    overrides: {
      return: { after: true },
      throw: { after: true },
      case: { after: true },
    },
  }],
  'comma-dangle': ['error', {
    arrays: 'always-multiline',
    objects: 'always-multiline',
    imports: 'always-multiline',
    exports: 'always-multiline',
    functions: 'always-multiline',
  }],
  'object-curly-spacing': ['error', 'always'],
  'space-before-function-paren': ['error', {
    anonymous: 'always',
    named: 'never',
    asyncArrow: 'always',
  }],
  'space-unary-ops': ['error', { words: true, nonwords: false }],
  'space-in-parens': ['error', 'never'],
  'no-unused-vars': ['error', { caughtErrors: 'none' }],
  'quote-props': ['error', 'as-needed', {
    keywords: false,
    unnecessary: true,
    numbers: false,
  }],
  'import/no-commonjs': [0],
  'import/no-extraneous-dependencies': ['off'],
  'no-multi-spaces': ['error', { ignoreEOLComments: false }],
  'no-trailing-spaces': ['error'],
  'no-multiple-empty-lines': ['error', { max: 1, maxEOF: 1 }],
  'sort-imports': ['warn', { ignoreCase: true, ignoreDeclarationSort: true }],
  'max-len': 'off',
  'no-unsafe-optional-chaining': 'off',
  'no-param-reassign': ['error', {
    props: true,
    ignorePropertyModificationsFor: ['state', 'acc', 'e'],
  }],
  'import/no-cycle': 'warn',
}
```
