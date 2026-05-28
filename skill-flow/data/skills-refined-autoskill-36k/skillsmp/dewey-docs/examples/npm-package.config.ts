import { defineConfig } from '@arach/dewey'

/**
 * Example Dewey config for an npm package
 */
export default defineConfig({
  project: {
    name: 'my-utils',
    tagline: 'A collection of utility functions for Node.js',
    type: 'npm-package',
  },

  agent: {
    criticalContext: [
      'This is a pure ESM package - no CommonJS',
      'All functions are tree-shakeable',
      'Minimum Node.js version: 18',
    ],

    entryPoints: {
      'Main Export': 'src/index.ts',
      'String Utils': 'src/string/',
      'Array Utils': 'src/array/',
      'Tests': 'tests/',
    },

    rules: [
      { pattern: 'src/**/*.ts', instruction: 'Use TypeScript strict mode' },
      { pattern: 'tests/**', instruction: 'Use vitest for testing' },
    ],

    sections: ['overview', 'quickstart', 'api', 'examples'],
  },

  docs: {
    path: './docs',
    output: './',
    required: ['overview.md', 'quickstart.md', 'api.md'],
  },

  install: {
    objective: 'Install and verify the package works',
    doneWhen: {
      command: 'node -e "import(\'my-utils\').then(m => console.log(Object.keys(m)))"',
      expectedOutput: 'Array of exported functions',
    },
    prerequisites: ['Node.js 18+'],
    steps: [
      { description: 'Install the package', command: 'npm install my-utils' },
      { description: 'Verify import works', command: 'node -e "import(\'my-utils\')"' },
    ],
  },
})
