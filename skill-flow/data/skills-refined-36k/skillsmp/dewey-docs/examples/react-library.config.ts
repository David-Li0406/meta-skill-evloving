import { defineConfig } from '@arach/dewey'

/**
 * Example Dewey config for a React component library
 */
export default defineConfig({
  project: {
    name: 'my-ui',
    tagline: 'React component library with Tailwind CSS',
    type: 'react-library',
  },

  agent: {
    criticalContext: [
      'Components use Tailwind CSS for styling',
      'All components support dark mode via class strategy',
      'Requires React 18+ and Tailwind CSS 3+',
      'Components are tree-shakeable - import individually',
    ],

    entryPoints: {
      'Main Export': 'src/index.ts',
      'Components': 'src/components/',
      'Hooks': 'src/hooks/',
      'Types': 'src/types/',
    },

    rules: [
      { pattern: 'src/components/*.tsx', instruction: 'One component per file, export default' },
      { pattern: 'src/hooks/*.ts', instruction: 'Custom hooks, start with "use"' },
    ],

    sections: ['overview', 'quickstart', 'components', 'theming'],
  },

  docs: {
    path: './docs',
    output: './',
    required: ['overview.md', 'quickstart.md', 'components.md'],
  },

  install: {
    objective: 'Install library and render a component',
    doneWhen: {
      command: 'npm run build',
      expectedOutput: 'Build successful',
    },
    prerequisites: ['Node.js 18+', 'React 18+', 'Tailwind CSS 3+'],
    steps: [
      { description: 'Install the library', command: 'npm install my-ui' },
      { description: 'Add Tailwind content path', command: 'Edit tailwind.config.js to include node_modules/my-ui' },
      { description: 'Import and use', command: 'import { Button } from "my-ui"' },
    ],
  },
})
