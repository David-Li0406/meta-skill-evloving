/**
 * Commitlint Configuration - Conventional Commits
 *
 * Impose le format Conventional Commits pour tous les messages de commit.
 * @see https://www.conventionalcommits.org/
 * @see https://commitlint.js.org/
 *
 * Format: <type>(<scope>): <description>
 * Exemple: feat(auth): add OAuth2 login with Google
 */

/** @type {import('@commitlint/types').UserConfig} */
export default {
  extends: ['@commitlint/config-conventional'],

  rules: {
    // ===== Type =====
    'type-enum': [
      2, // error
      'always',
      [
        'feat',     // Nouvelle fonctionnalité
        'fix',      // Correction de bug
        'docs',     // Documentation uniquement
        'style',    // Formatage, pas de changement de code
        'refactor', // Refactoring du code
        'perf',     // Amélioration de performance
        'test',     // Ajout ou correction de tests
        'build',    // Changements du système de build
        'ci',       // Changements CI/CD
        'chore',    // Maintenance, pas de changement de code
        'revert',   // Revert un commit précédent
        'wip',      // Work in progress (usage limité)
      ],
    ],
    'type-case': [2, 'always', 'lower-case'],
    'type-empty': [2, 'never'],

    // ===== Scope =====
    'scope-case': [2, 'always', 'lower-case'],
    // scope-enum peut être personnalisé par projet :
    // 'scope-enum': [2, 'always', ['api', 'ui', 'auth', 'db', 'config']],

    // ===== Subject =====
    'subject-case': [2, 'always', 'lower-case'],
    'subject-empty': [2, 'never'],
    'subject-full-stop': [2, 'never', '.'],
    'subject-min-length': [2, 'always', 10],
    'subject-max-length': [2, 'always', 72],

    // ===== Header =====
    'header-max-length': [2, 'always', 100],

    // ===== Body =====
    'body-leading-blank': [2, 'always'],
    'body-max-line-length': [2, 'always', 100],

    // ===== Footer =====
    'footer-leading-blank': [2, 'always'],
    'footer-max-line-length': [2, 'always', 100],
  },

  // Prompts pour commitizen (optionnel)
  prompt: {
    questions: {
      type: {
        description: 'Sélectionnez le type de changement',
        enum: {
          feat: {
            description: 'Nouvelle fonctionnalité',
            title: 'Features',
            emoji: '✨',
          },
          fix: {
            description: 'Correction de bug',
            title: 'Bug Fixes',
            emoji: '🐛',
          },
          docs: {
            description: 'Changements de documentation uniquement',
            title: 'Documentation',
            emoji: '📚',
          },
          style: {
            description: 'Changements de style (formatage, espaces, etc.)',
            title: 'Styles',
            emoji: '💎',
          },
          refactor: {
            description: 'Refactoring sans ajout de fonctionnalité ni correction',
            title: 'Code Refactoring',
            emoji: '📦',
          },
          perf: {
            description: 'Amélioration de performance',
            title: 'Performance Improvements',
            emoji: '🚀',
          },
          test: {
            description: 'Ajout ou correction de tests',
            title: 'Tests',
            emoji: '🚨',
          },
          build: {
            description: 'Changements du système de build ou dépendances',
            title: 'Builds',
            emoji: '🛠',
          },
          ci: {
            description: 'Changements de configuration CI',
            title: 'Continuous Integration',
            emoji: '⚙️',
          },
          chore: {
            description: 'Autres changements (maintenance)',
            title: 'Chores',
            emoji: '♻️',
          },
          revert: {
            description: 'Revert un commit précédent',
            title: 'Reverts',
            emoji: '🗑',
          },
        },
      },
      scope: {
        description: 'Quel est le scope de ce changement (ex: api, ui, auth) ?',
      },
      subject: {
        description: 'Écrivez une description courte et impérative du changement',
      },
      body: {
        description: 'Fournissez une description plus détaillée du changement',
      },
      isBreaking: {
        description: 'Y a-t-il des BREAKING CHANGES ?',
      },
      breakingBody: {
        description: 'Un commit BREAKING CHANGE nécessite un body. Décrivez le changement',
      },
      breaking: {
        description: 'Décrivez les BREAKING CHANGES',
      },
      isIssueAffected: {
        description: 'Ce changement affecte-t-il des issues ouvertes ?',
      },
      issuesBody: {
        description: 'Si des issues sont fermées, un body est requis',
      },
      issues: {
        description: 'Ajoutez les références des issues (ex: "fix #123", "re #123")',
      },
    },
  },
};
