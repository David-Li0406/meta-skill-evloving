// Commitlint configuration for conventional commits
// https://commitlint.js.org/

export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    // Type enum
    'type-enum': [
      2,
      'always',
      [
        'feat',     // New feature
        'fix',      // Bug fix
        'docs',     // Documentation only
        'style',    // Code style (formatting, missing semicolons, etc.)
        'refactor', // Code refactoring
        'perf',     // Performance improvement
        'test',     // Adding or updating tests
        'chore',    // Maintenance tasks
        'ci',       // CI/CD changes
        'build',    // Build system or dependencies
        'revert',   // Revert a previous commit
      ],
    ],

    // Header (subject line) rules
    'header-max-length': [2, 'always', 100],
    'header-case': [2, 'always', 'lower-case'],

    // Subject rules
    'subject-empty': [2, 'never'],
    'subject-full-stop': [2, 'never', '.'],

    // Body rules
    'body-leading-blank': [2, 'always'],
    'body-max-line-length': [2, 'always', 100],

    // Footer rules
    'footer-leading-blank': [2, 'always'],

    // Scope rules (optional)
    'scope-case': [2, 'always', 'lower-case'],
  },
}
