# VitePress Configuration Template

## docs/.vitepress/config.ts

```typescript
import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

export default withMermaid(defineConfig({
  // Site metadata
  title: '{Project Title}',
  description: '{Project description}',
  lang: 'zh-CN',

  // Build output
  outDir: '../dist',

  // Theme configuration
  themeConfig: {
    // Navigation bar
    nav: [
      { text: 'Home', link: '/' },
      { text: '{Module 1}', link: '/{module1}/' },
      { text: '{Module 2}', link: '/{module2}/' },
      {
        text: 'Resources',
        items: [
          { text: 'Official Docs', link: '{official-docs-url}' },
          { text: 'GitHub', link: '{github-url}' }
        ]
      }
    ],

    // Sidebar configuration
    sidebar: {
      '/': [
        {
          text: 'Introduction',
          items: [
            { text: 'Overview', link: '/introduction/overview' },
            { text: 'Architecture', link: '/introduction/architecture' }
          ]
        },
        {
          text: '{Module 1}',
          items: [
            { text: 'Overview', link: '/{module1}/' },
            { text: '{Topic 1}', link: '/{module1}/{topic1}' },
            { text: '{Topic 2}', link: '/{module1}/{topic2}' },
            { text: '{Topic 3}', link: '/{module1}/{topic3}' }
          ]
        },
        {
          text: '{Module 2}',
          items: [
            { text: 'Overview', link: '/{module2}/' },
            { text: '{Topic 1}', link: '/{module2}/{topic1}' },
            { text: '{Topic 2}', link: '/{module2}/{topic2}' }
          ]
        }
      ]
    },

    // Social links
    socialLinks: [
      { icon: 'github', link: '{github-url}' }
    ],

    // Search
    search: {
      provider: 'local',
      options: {
        translations: {
          button: {
            buttonText: 'Search',
            buttonAriaLabel: 'Search'
          },
          modal: {
            noResultsText: 'No results',
            resetButtonTitle: 'Clear',
            footer: {
              selectText: 'Select',
              navigateText: 'Navigate',
              closeText: 'Close'
            }
          }
        }
      }
    },

    // Footer
    footer: {
      message: '{Footer message}',
      copyright: 'MIT License'
    },

    // Edit link (optional)
    editLink: {
      pattern: '{github-url}/edit/main/docs/:path',
      text: 'Edit this page'
    },

    // Last updated
    lastUpdated: {
      text: 'Last updated',
      formatOptions: {
        dateStyle: 'short',
        timeStyle: 'short'
      }
    },

    // Outline
    outline: {
      level: [2, 3],
      label: 'Table of Contents'
    },

    // Doc footer navigation
    docFooter: {
      prev: 'Previous',
      next: 'Next'
    }
  },

  // Markdown configuration
  markdown: {
    // Enable line numbers in code blocks
    lineNumbers: true,

    // Code block themes
    theme: {
      light: 'github-light',
      dark: 'github-dark'
    }
  },

  // Mermaid configuration
  mermaid: {
    // Mermaid options: https://mermaid.js.org/config/setup/modules/mermaidAPI.html#mermaidapi-configuration-defaults
    theme: 'default'
  },

  // Optional: customize mermaid plugin options
  mermaidPlugin: {
    class: 'mermaid'
  },

  // Head tags
  head: [
    ['link', { rel: 'icon', href: '/favicon.ico' }],
    ['meta', { name: 'theme-color', content: '#3c8772' }]
  ],

  // Sitemap (for SEO)
  sitemap: {
    hostname: '{site-url}'
  }
}))
```

## Configuration Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{Project Title}` | Site title | `Daytona Source Tutorial` |
| `{module1}` | First module path | `sandbox` |
| `{module2}` | Second module path | `agent` |
| `{github-url}` | GitHub repository URL | `https://github.com/daytonaio/daytona` |
| `{official-docs-url}` | Official documentation | `https://www.daytona.io/docs` |
| `{site-url}` | Deployed site URL | `https://tutorial.example.com` |

## Sidebar Patterns

### Flat Structure
```typescript
sidebar: [
  { text: 'Page 1', link: '/page1' },
  { text: 'Page 2', link: '/page2' }
]
```

### Grouped Structure
```typescript
sidebar: [
  {
    text: 'Group',
    collapsed: false,  // false = expanded by default
    items: [
      { text: 'Item 1', link: '/group/item1' },
      { text: 'Item 2', link: '/group/item2' }
    ]
  }
]
```

### Multi-Sidebar (different sidebars for different paths)
```typescript
sidebar: {
  '/module1/': [/* module1 sidebar */],
  '/module2/': [/* module2 sidebar */],
  '/': [/* default sidebar */]
}
```

## Deployment Configuration

### Vercel
No additional configuration needed. Vercel auto-detects VitePress.

### GitHub Pages
Add to `config.ts`:
```typescript
export default defineConfig({
  base: '/{repo-name}/',  // If deploying to github.io/{repo-name}
  // ...
})
```

### Netlify
Create `netlify.toml`:
```toml
[build]
  command = "pnpm build"
  publish = "docs/.vitepress/dist"
```
