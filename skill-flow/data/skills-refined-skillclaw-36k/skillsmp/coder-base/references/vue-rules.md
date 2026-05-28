# ESLint Configuration for Vue 3

当涉及 Vue 3 代码编写或修改时，必须遵循以下规范：

- **API 风格**: 必须使用 **组合式 API (Composition API)** 及 **`<script setup>`** 语法糖。
- **ESLint 配置**: 除遵循 JS 规则外，还需遵循以下 Vue 特定配置 (基于 `vue/strongly-recommended`)：

```javascript
{
  'vue/multi-word-component-names': 'off',
  'vue/html-button-has-type': 'off',
  'vue/max-len': 'off',
  'vue/max-attributes-per-line': ['error', {
    singleline: { max: 5 },
    multiline: { max: 1 },
  }],
  'vuejs-accessibility/form-control-has-label': 'off',
  'vuejs-accessibility/label-has-for': 'off',
}
```

此外，编写 Vue Template、HTML 或 TSX 时，同一级别的并列结构尽量用**空行**隔开，以提升阅读体验。
