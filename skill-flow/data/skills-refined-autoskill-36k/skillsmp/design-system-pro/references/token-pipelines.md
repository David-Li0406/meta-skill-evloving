# Automated Token Pipelines

## The Design-to-Code Loop
In 2026, designers own the tokens in Figma, and they are automatically pushed to Git.

---

### 1. The Source: Tokens Studio (Figma)
- Designers use the "Tokens Studio" plugin to define layered tokens.
- Changes are pushed as a `tokens.json` to a GitHub repo.

---

### 2. The Transformer: Style Dictionary
Style Dictionary takes the JSON source and transforms it for various targets.

```javascript
// sd.config.js
module.exports = {
  source: ['tokens/**/*.json'],
  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: 'build/css/',
      files: [{ destination: 'variables.css', format: 'css/variables' }]
    },
    android: {
      transformGroup: 'android',
      buildPath: 'build/android/',
      files: [{ destination: 'tokens.xml', format: 'android/resources' }]
    }
  }
};
```

---

### 3. Automated Drift Detection
AI agents scan the PRs and compare the "Code Tokens" with the "Figma Tokens." If a developer uses a hex code not in the system, the agent flags it and suggests the correct semantic token.
