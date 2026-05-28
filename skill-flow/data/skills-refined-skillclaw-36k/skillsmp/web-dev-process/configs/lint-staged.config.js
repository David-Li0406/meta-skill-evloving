/**
 * lint-staged Configuration
 *
 * Alternative à lefthook pour les hooks pre-commit.
 * Exécute les linters uniquement sur les fichiers staged.
 *
 * @see https://github.com/lint-staged/lint-staged
 *
 * Installation:
 *   pnpm add -D lint-staged
 *
 * Utilisation avec husky:
 *   pnpm add -D husky
 *   pnpm husky init
 *   echo "pnpm lint-staged" > .husky/pre-commit
 */

/** @type {import('lint-staged').Config} */
export default {
  // ===== JavaScript / TypeScript =====
  '*.{js,jsx,mjs,cjs}': [
    'eslint --fix',
    'prettier --write',
  ],

  '*.{ts,tsx}': [
    'eslint --fix',
    'prettier --write',
    // Type-check seulement les fichiers modifiés
    () => 'tsc --noEmit',
  ],

  // ===== Styles =====
  '*.{css,scss,sass,less}': [
    'prettier --write',
    // Décommenter si stylelint est installé
    // 'stylelint --fix',
  ],

  // ===== Markup =====
  '*.{html,vue,svelte}': [
    'prettier --write',
  ],

  // ===== Data / Config =====
  '*.{json,yaml,yml}': [
    'prettier --write',
  ],

  // ===== Documentation =====
  '*.md': [
    'prettier --write',
    // Décommenter si markdownlint est installé
    // 'markdownlint --fix',
  ],

  // ===== Package.json =====
  'package.json': [
    'prettier --write',
    // Trier les clés du package.json
    // 'sort-package-json',
  ],

  // ===== Tests =====
  '*.{test,spec}.{js,jsx,ts,tsx}': [
    'eslint --fix',
    'prettier --write',
    // Exécuter les tests des fichiers modifiés
    // 'vitest related --run',
  ],
};

/**
 * ALTERNATIVES PAR FRAMEWORK
 *
 * Next.js:
 * '*.{js,jsx,ts,tsx}': ['next lint --fix', 'prettier --write']
 *
 * Nuxt:
 * '*.{js,ts,vue}': ['nuxt lint --fix', 'prettier --write']
 *
 * Avec Biome (alternative à ESLint + Prettier):
 * '*.{js,jsx,ts,tsx,json}': ['biome check --write']
 */
