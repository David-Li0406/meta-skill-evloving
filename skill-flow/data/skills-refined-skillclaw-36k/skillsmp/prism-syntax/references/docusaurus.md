# Prism Syntax Highlighting in Docusaurus

## Built-in Language Support

Docusaurus includes these languages by default:
- `javascript`, `typescript`, `jsx`, `tsx`
- `json`, `yaml`, `markdown`
- `bash`, `shell`
- `css`, `html`

## Adding Additional Languages

### Step 1: Configure docusaurus.config.js

```javascript
module.exports = {
  themeConfig: {
    prism: {
      additionalLanguages: [
        'java',
        'python',
        'ruby',
        'go',
        'rust',
        'csharp',
        'php'
      ],
    },
  },
};
```

### Step 2: For Custom Languages

Create the language definition:

```javascript
// src/prism/prism-mylang.js
(function (Prism) {
  Prism.languages.mylang = {
    'comment': /\/\/.*/,
    'string': /"(?:\\.|[^"\\])*"/,
    'keyword': /\b(?:schema|dataset|assume)\b/,
    'number': /\b\d+(?:\.\d+)?\b/,
    'operator': /[+\-*/%=<>!|&:]+/,
    'punctuation': /[{}[\]();,.]/
  };
})(Prism);
```

### Step 3: Create Language Inclusion Hook

```javascript
// src/theme/prism-include-languages.js
import siteConfig from '@generated/docusaurus.config';

export default function prismIncludeLanguages(PrismObject) {
  const {
    themeConfig: { prism },
  } = siteConfig;

  const { additionalLanguages } = prism;

  // Load additional languages
  globalThis.Prism = PrismObject;
  additionalLanguages.forEach((lang) => {
    require(`prismjs/components/prism-${lang}`);
  });

  // Load custom language
  require('./prism-mylang');

  delete globalThis.Prism;
}
```

### Step 4: Register the Language Alias (Optional)

```javascript
// In prism-mylang.js
Prism.languages.ml = Prism.languages.mylang;  // Alias
```

## Usage in Markdown

````markdown
```mylang
schema User {
  name: string,
  age: int in 18..100
}
```
````

## Custom Theme Colors

```css
/* src/css/custom.css */
.token.keyword {
  color: var(--ifm-color-primary);
}

.token.string {
  color: #22863a;
}

.token.comment {
  color: #6a737d;
  font-style: italic;
}

/* Dark mode */
[data-theme='dark'] .token.keyword {
  color: var(--ifm-color-primary-light);
}
```

## Using prism-react-renderer Themes

```javascript
// docusaurus.config.js
const { themes } = require('prism-react-renderer');

module.exports = {
  themeConfig: {
    prism: {
      theme: themes.github,
      darkTheme: themes.dracula,
    },
  },
};
```

Available themes:
- `themes.github`
- `themes.dracula`
- `themes.duotoneLight`
- `themes.duotoneDark`
- `themes.nightOwl`
- `themes.nightOwlLight`
- `themes.oceanicNext`
- `themes.okaidia`
- `themes.palenight`
- `themes.shadesOfPurple`
- `themes.synthwave84`
- `themes.ultramin`
- `themes.vsDark`
- `themes.vsLight`

## Line Highlighting

````markdown
```javascript {1,3-5}
const a = 1;  // Highlighted
const b = 2;
const c = 3;  // Highlighted
const d = 4;  // Highlighted
const e = 5;  // Highlighted
```
````

## Code Titles

````markdown
```javascript title="src/index.js"
console.log('Hello');
```
````

## Magic Comments

````markdown
```javascript
// highlight-next-line
const highlighted = true;

// highlight-start
const also = 'highlighted';
const both = 'lines';
// highlight-end
```
````

## Live Code Blocks

```bash
npm install @docusaurus/theme-live-codeblock
```

```javascript
// docusaurus.config.js
module.exports = {
  themes: ['@docusaurus/theme-live-codeblock'],
};
```

````markdown
```jsx live
function Demo() {
  return <button>Click me</button>;
}
```
````
