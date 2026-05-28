import { defineConfig } from '@arach/dewey'

/**
 * Example Dewey config for a CLI tool
 */
export default defineConfig({
  project: {
    name: 'mycli',
    tagline: 'A fast file processing CLI',
    type: 'cli-tool',
  },

  agent: {
    criticalContext: [
      'CLI uses commander.js for argument parsing',
      'Supports both --flag and -f short forms',
      'Exit codes: 0=success, 1=error, 2=invalid args',
    ],

    entryPoints: {
      'CLI Entry': 'src/cli/index.ts',
      'Commands': 'src/cli/commands/',
      'Core Logic': 'src/core/',
    },

    rules: [
      { pattern: 'src/cli/commands/*.ts', instruction: 'Each file is one command' },
      { pattern: 'src/core/*', instruction: 'Pure functions, no CLI dependencies' },
    ],

    sections: ['overview', 'quickstart', 'commands', 'options'],
  },

  docs: {
    path: './docs',
    output: './',
    required: ['overview.md', 'quickstart.md', 'commands.md'],
  },

  install: {
    objective: 'Install CLI globally and verify it runs',
    doneWhen: {
      command: 'mycli --version',
      expectedOutput: 'Version number (e.g., 1.0.0)',
    },
    prerequisites: ['Node.js 18+'],
    steps: [
      { description: 'Install globally', command: 'npm install -g mycli' },
      { description: 'Verify installation', command: 'mycli --version' },
      { description: 'Show help', command: 'mycli --help' },
    ],
  },
})
