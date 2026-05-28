# README for NPM Library

Complete README documentation for a React component library npm package.

## 📝 Prompt

```
Create a comprehensive README.md for an npm package called "react-ui-kit":

Context:
- Package: React UI component library
- Components: 20+ accessible, customizable components
- Tech stack: React, TypeScript, CSS Modules
- Target audience: React developers building web apps
- License: MIT

Include:
- Project badges (version, downloads, license, build status)
- Clear description and key features
- Installation instructions
- Quick start example
- API documentation for main components
- Customization guide
- Contributing guidelines
- License and credits
```

## 📄 Complete README.md

```markdown
<div align="center">
  <h1>React UI Kit</h1>
  <p>A modern, accessible React component library for building beautiful web applications</p>

  [![NPM Version](https://img.shields.io/npm/v/react-ui-kit.svg)](https://www.npmjs.com/package/react-ui-kit)
  [![NPM Downloads](https://img.shields.io/npm/dm/react-ui-kit.svg)](https://www.npmjs.com/package/react-ui-kit)
  [![Build Status](https://github.com/yourusername/react-ui-kit/workflows/CI/badge.svg)](https://github.com/yourusername/react-ui-kit/actions)
  [![Coverage Status](https://coveralls.io/repos/github/yourusername/react-ui-kit/badge.svg)](https://coveralls.io/github/yourusername/react-ui-kit)
  [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
  [![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)](https://www.typescriptlang.org/)
</div>

## ✨ Features

- 🎨 **20+ Components** - Buttons, inputs, modals, navigation, and more
- ♿ **Accessible** - WCAG 2.1 AA compliant with ARIA support
- 🎭 **Themeable** - Customizable design tokens and CSS variables
- 📱 **Responsive** - Mobile-first, works on all screen sizes
- 🌙 **Dark Mode** - Built-in dark theme support
- 🧩 **TypeScript** - Fully typed for better DX
- 📦 **Tree-shakeable** - Only import what you need
- ⚡ **Zero Dependencies** - No external runtime dependencies
- 🎯 **Developer Friendly** - Clear API, extensive documentation
- ✅ **Tested** - 95%+ test coverage

## 📦 Installation

```bash
# npm
npm install react-ui-kit

# yarn
yarn add react-ui-kit

# pnpm
pnpm add react-ui-kit
```

## 🚀 Quick Start

```tsx
import { Button, Input, Card } from 'react-ui-kit';
import 'react-ui-kit/dist/styles.css';

function App() {
  const [name, setName] = useState('');

  return (
    <Card>
      <h1>Welcome to React UI Kit</h1>
      <Input
        label="Your Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Enter your name"
      />
      <Button onClick={() => alert(`Hello, ${name}!`)}>
        Submit
      </Button>
    </Card>
  );
}
```

## 📚 Documentation

### Components

#### Button

Versatile button component with multiple variants and sizes.

```tsx
import { Button } from 'react-ui-kit';

<Button variant="primary" size="medium" onClick={handleClick}>
  Click Me
</Button>
```

**Props**

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `variant` | `'primary' \| 'secondary' \| 'tertiary' \| 'destructive'` | `'primary'` | Button style variant |
| `size` | `'small' \| 'medium' \| 'large'` | `'medium'` | Button size |
| `fullWidth` | `boolean` | `false` | Make button full width |
| `loading` | `boolean` | `false` | Show loading spinner |
| `disabled` | `boolean` | `false` | Disable button |
| `leftIcon` | `ReactNode` | - | Icon before text |
| `rightIcon` | `ReactNode` | - | Icon after text |
| `onClick` | `(event: MouseEvent) => void` | - | Click handler |

**Examples**

```tsx
// Primary button with loading state
<Button variant="primary" loading>
  Saving...
</Button>

// Secondary button with icon
<Button variant="secondary" leftIcon={<PlusIcon />}>
  Add Item
</Button>

// Destructive full-width button
<Button variant="destructive" fullWidth>
  Delete Account
</Button>
```

---

#### Input

Text input with label, error states, and icon support.

```tsx
import { Input } from 'react-ui-kit';

<Input
  label="Email"
  type="email"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
  error={errors.email}
  helperText="We'll never share your email"
/>
```

**Props**

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `string` | - | Input label |
| `type` | `string` | `'text'` | HTML input type |
| `value` | `string` | - | Input value |
| `onChange` | `(event: ChangeEvent) => void` | - | Change handler |
| `error` | `string` | - | Error message |
| `helperText` | `string` | - | Helper text below input |
| `placeholder` | `string` | - | Placeholder text |
| `disabled` | `boolean` | `false` | Disable input |
| `required` | `boolean` | `false` | Mark as required |
| `leftIcon` | `ReactNode` | - | Icon on left side |
| `rightIcon` | `ReactNode` | - | Icon on right side |
| `fullWidth` | `boolean` | `false` | Make input full width |

**Examples**

```tsx
// Input with error
<Input
  label="Username"
  value={username}
  onChange={handleChange}
  error="Username is already taken"
  required
/>

// Password input with icon
<Input
  label="Password"
  type="password"
  leftIcon={<LockIcon />}
  rightIcon={<EyeIcon />}
/>

// Search input
<Input
  placeholder="Search..."
  leftIcon={<SearchIcon />}
  fullWidth
/>
```

---

#### Card

Container component with optional header, body, and footer.

```tsx
import { Card, CardHeader, CardBody, CardFooter } from 'react-ui-kit';

<Card elevated hoverable>
  <CardHeader>
    <h3>Card Title</h3>
  </CardHeader>
  <CardBody>
    <p>Card content goes here</p>
  </CardBody>
  <CardFooter>
    <Button>Action</Button>
  </CardFooter>
</Card>
```

**Props**

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `padding` | `'none' \| 'small' \| 'medium' \| 'large'` | `'medium'` | Internal padding |
| `elevated` | `boolean` | `false` | Add shadow elevation |
| `hoverable` | `boolean` | `false` | Add hover effect |
| `onClick` | `() => void` | - | Make card clickable |

---

#### Modal

Accessible modal dialog with focus trap and backdrop.

```tsx
import { Modal } from 'react-ui-kit';

<Modal
  isOpen={isOpen}
  onClose={handleClose}
  title="Confirm Action"
  size="medium"
>
  <p>Are you sure you want to proceed?</p>
  <Button onClick={handleConfirm}>Confirm</Button>
  <Button variant="secondary" onClick={handleClose}>
    Cancel
  </Button>
</Modal>
```

**Props**

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `isOpen` | `boolean` | `false` | Control modal visibility |
| `onClose` | `() => void` | - | Close handler |
| `title` | `string` | - | Modal title |
| `size` | `'small' \| 'medium' \| 'large'` | `'medium'` | Modal width |
| `closeOnBackdrop` | `boolean` | `true` | Close when clicking backdrop |
| `closeOnEsc` | `boolean` | `true` | Close when pressing Escape |

---

### Theming

React UI Kit uses CSS custom properties for theming.

**Custom Theme**

```css
/* theme.css */
:root {
  /* Primary Colors */
  --color-primary-50: #E3F2FD;
  --color-primary-500: #2196F3;
  --color-primary-700: #1976D2;

  /* Typography */
  --font-sans: 'Inter', sans-serif;
  --font-size-base: 16px;

  /* Spacing */
  --space-4: 1rem;
  --space-6: 1.5rem;

  /* Border Radius */
  --radius-md: 8px;

  /* Shadows */
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Dark Theme */
[data-theme='dark'] {
  --color-gray-900: #F5F5F5;
  --color-gray-50: #1A1A1A;
}
```

**Apply Theme**

```tsx
import 'react-ui-kit/dist/styles.css';
import './theme.css'; // Your custom theme

function App() {
  const [theme, setTheme] = useState('light');

  return (
    <div data-theme={theme}>
      <Button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
        Toggle Theme
      </Button>
    </div>
  );
}
```

**Theme Provider** (Optional)

```tsx
import { ThemeProvider } from 'react-ui-kit';

const customTheme = {
  colors: {
    primary: {
      500: '#FF6B35',
    },
  },
};

function App() {
  return (
    <ThemeProvider theme={customTheme}>
      <YourApp />
    </ThemeProvider>
  );
}
```

## 🎨 Customization

### Import Specific Components

```tsx
// Instead of importing everything
import { Button, Input, Card } from 'react-ui-kit';

// Import from specific paths (better for tree-shaking)
import Button from 'react-ui-kit/Button';
import Input from 'react-ui-kit/Input';
```

### Custom Styles

```tsx
// Using className
<Button className="my-custom-button">
  Custom Button
</Button>

// Using style prop
<Button style={{ backgroundColor: '#FF6B35' }}>
  Inline Styled Button
</Button>

// Using CSS Modules
import styles from './MyComponent.module.css';

<Button className={styles.customButton}>
  Styled Button
</Button>
```

## 🏗️ Browser Support

- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest 2 versions)
- iOS Safari (latest 2 versions)
- Android Chrome (latest 2 versions)

## 📖 Full Documentation

Visit our [documentation site](https://react-ui-kit.dev) for:
- Interactive component playground
- Complete API reference
- Design guidelines
- Accessibility guide
- Migration guides

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

**Development Setup**

```bash
# Clone repository
git clone https://github.com/yourusername/react-ui-kit.git
cd react-ui-kit

# Install dependencies
npm install

# Start development server
npm run dev

# Run tests
npm test

# Build library
npm run build

# Run Storybook
npm run storybook
```

**Pull Request Guidelines**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write/update tests
5. Ensure tests pass (`npm test`)
6. Commit with conventional commits (`git commit -m 'feat: add amazing feature'`)
7. Push to your fork (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for release notes.

## 📄 License

MIT © [Your Name](https://github.com/yourusername)

See [LICENSE](LICENSE) for details.

## 🙏 Credits

- Built with [React](https://react.dev/)
- Inspired by [Radix UI](https://www.radix-ui.com/)
- Icons from [Lucide](https://lucide.dev/)
- Tested with [Vitest](https://vitest.dev/) and [Testing Library](https://testing-library.com/)

## 💬 Community

- [Discord](https://discord.gg/react-ui-kit)
- [GitHub Discussions](https://github.com/yourusername/react-ui-kit/discussions)
- [Twitter](https://twitter.com/react_ui_kit)

## ⭐ Show Your Support

If you find this project useful, please give it a ⭐ on [GitHub](https://github.com/yourusername/react-ui-kit)!

---

Made with ❤️ by the React UI Kit team
```

## ✅ README Components

This README includes:
1. ✅ Eye-catching header with badges
2. ✅ Clear feature list
3. ✅ Installation instructions (multiple package managers)
4. ✅ Quick start example
5. ✅ API documentation with tables
6. ✅ Code examples for each component
7. ✅ Theming and customization guide
8. ✅ Browser support information
9. ✅ Contributing guidelines
10. ✅ Development setup instructions
11. ✅ Links to additional resources
12. ✅ License and credits
13. ✅ Community links

## 📊 README Best Practices

**Structure**:
- Start with clear project name and description
- Add badges for quick information
- Include table of contents for long READMEs
- Provide quick start before detailed docs
- Use examples liberally
- Link to external documentation

**Writing Style**:
- Be concise and scannable
- Use emojis sparingly for visual markers
- Include code examples with syntax highlighting
- Use tables for API documentation
- Add screenshots or GIFs when helpful

**Maintenance**:
- Keep installation instructions up to date
- Update version badges automatically (CI/CD)
- Link to CHANGELOG for version history
- Provide migration guides for breaking changes

---

This README provides everything users need to get started while being well-organized and easy to navigate.
